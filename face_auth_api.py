# -*- coding: utf-8 -*-
import numpy as np
import cv2
import io
import json
import os
import psycopg2
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from facenet_pytorch import MTCNN
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional

# --- Configuration ---
DATABASE_URL = os.environ.get("DATABASE_URL")
SIMILARITY_THRESHOLD = 0.5

app = FastAPI(title="Face Verification System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database ---
def get_db_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not set")
    return psycopg2.connect(DATABASE_URL)

def init_db():
    if not DATABASE_URL:
        print("WARNING: DATABASE_URL not set. Persistence disabled.")
        return
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(255) PRIMARY KEY,
                embedding TEXT NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("DB Initialized.")
    except Exception as e:
        print(f"DB Init Failed: {e}")

# --- AI Models ---
print("Loading AI Models...")
mtcnn = MTCNN(keep_all=False, device='cpu')
arcface = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
arcface.prepare(ctx_id=0, det_size=(640, 640))
print("Models Ready.")

# Initialize DB on startup
init_db()

# --- Helpers ---
def process_image(image_bytes):
    """Returns PIL Image (for MTCNN) and CV2 Image (for ArcFace)"""
    from PIL import Image
    
    # PIL
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # CV2
    nparr = np.frombuffer(image_bytes, np.uint8)
    cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
    return pil_img, cv_img

def get_embedding(img_rgb):
    faces = arcface.get(img_rgb)
    if len(faces) == 0: return None
    emb = faces[0].embedding
    return emb / np.linalg.norm(emb)

# --- Routes ---

@app.get("/")
async def read_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "Backend running. Please upload index.html"}

@app.post("/register")
async def register(username: str = Form(...), file: UploadFile = File(...)):
    conn = None
    try:
        img_bytes = await file.read()
        pil_img, cv_img = process_image(img_bytes)

        if mtcnn(pil_img) is None:
            raise HTTPException(400, "No face detected (MTCNN).")
        
        emb = get_embedding(cv_img)
        if emb is None:
            raise HTTPException(400, "No face detected (ArcFace).")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            raise HTTPException(400, "User already exists.")

        cur.execute("INSERT INTO users (username, embedding) VALUES (%s, %s)", 
                    (username, json.dumps(emb.tolist())))
        conn.commit()
        return {"status": "success", "message": f"User '{username}' registered."}

    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))
    finally:
        if conn: conn.close()

@app.post("/verify")
async def verify(username: Optional[str] = Form(None), file: UploadFile = File(...)):
    conn = None
    try:
        img_bytes = await file.read()
        pil_img, cv_img = process_image(img_bytes)
        
        if mtcnn(pil_img) is None:
            raise HTTPException(400, "No face detected.")
        
        new_emb = get_embedding(cv_img)
        if new_emb is None:
            raise HTTPException(400, "Feature extraction failed.")

        conn = get_db_connection()
        cur = conn.cursor()
        
        # LOGIC SWITCH: If username provided, verify 1:1. If not, Identify 1:N.
        
        match_found = False
        best_score = -1.0
        identified_user = "Unknown"

        if username:
            # 1:1 Verification
            cur.execute("SELECT embedding FROM users WHERE username = %s", (username,))
            res = cur.fetchone()
            if not res:
                raise HTTPException(404, "User not found.")
            
            stored_emb = np.array(json.loads(res[0]))
            score = cosine_similarity([stored_emb], [new_emb])[0][0]
            match_found = bool(score >= SIMILARITY_THRESHOLD)
            best_score = float(score)
            identified_user = username if match_found else "Unknown"
            
        else:
            # 1:N Identification (Search all users)
            cur.execute("SELECT username, embedding FROM users")
            all_users = cur.fetchall()
            
            best_score = -1.0
            best_user = None

            for user_row in all_users:
                db_user, db_emb_json = user_row
                db_emb = np.array(json.loads(db_emb_json))
                
                score = cosine_similarity([db_emb], [new_emb])[0][0]
                
                if score > best_score:
                    best_score = score
                    best_user = db_user
            
            if best_score >= SIMILARITY_THRESHOLD:
                match_found = True
                identified_user = best_user
            else:
                match_found = False
                identified_user = "Unknown"

        return {
            "status": "success",
            "match": match_found,
            "username": identified_user,
            "similarity_score": float(best_score),
            "message": f"✅ Identified: {identified_user}" if match_found else "❌ Identity Unknown"
        }

    except Exception as e:
        print(e)
        raise HTTPException(500, str(e))
    finally:
        if conn: conn.close()
