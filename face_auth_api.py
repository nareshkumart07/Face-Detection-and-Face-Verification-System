# -*- coding: utf-8 -*-
import numpy as np
import cv2
import io
import json
import os
import base64
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from facenet_pytorch import MTCNN
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---
EMBEDDINGS_DB_FILE = "face_embeddings.json"
SIMILARITY_THRESHOLD = 0.5

app = FastAPI(title="Face Verification System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Model Initialization ---
print("Loading Models... This may take a moment.")
mtcnn = MTCNN(keep_all=False, device='cpu')
arcface = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
arcface.prepare(ctx_id=0, det_size=(640, 640))
print("Models Loaded Successfully.")

# --- Database Helpers ---
def load_db():
    if not os.path.exists(EMBEDDINGS_DB_FILE):
        return {}
    with open(EMBEDDINGS_DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(EMBEDDINGS_DB_FILE, 'w') as f:
        json.dump(data, f)

# --- Image Processing Helpers ---
def process_image_for_mtcnn(image_bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return image

def process_image_for_arcface(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def get_embedding(img_rgb):
    faces = arcface.get(img_rgb)
    if len(faces) == 0:
        return None
    embedding = faces[0].embedding
    embedding = embedding / np.linalg.norm(embedding)
    return embedding

# --- Routes ---

# SERVE FRONTEND (Added for Render)
@app.get("/")
async def read_index():
    # Looks for index.html in the same directory
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return {"message": "index.html not found. Please upload it."}

@app.post("/register")
async def register_user(username: str = Form(...), file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        pil_img = process_image_for_mtcnn(image_bytes)
        if mtcnn(pil_img) is None:
             raise HTTPException(status_code=400, detail="No face detected by MTCNN.")

        cv_img = process_image_for_arcface(image_bytes)
        embedding = get_embedding(cv_img)
        
        if embedding is None:
            raise HTTPException(status_code=400, detail="No face detected by ArcFace.")

        db = load_db()
        if username in db:
            raise HTTPException(status_code=400, detail="Username already exists.")
        
        db[username] = embedding.tolist()
        save_db(db)

        return {"message": f"User '{username}' registered successfully.", "status": "success"}

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
async def verify_user(username: str = Form(...), file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        db = load_db()
        if username not in db:
             raise HTTPException(status_code=404, detail="User not found. Please register first.")
        
        stored_embedding = np.array(db[username])
        pil_img = process_image_for_mtcnn(image_bytes)
        if mtcnn(pil_img) is None:
             raise HTTPException(status_code=400, detail="No face detected in verification image.")

        cv_img = process_image_for_arcface(image_bytes)
        new_embedding = get_embedding(cv_img)

        if new_embedding is None:
            raise HTTPException(status_code=400, detail="No face detected by ArcFace.")

        similarity = cosine_similarity([stored_embedding], [new_embedding])[0][0]
        is_match = bool(similarity >= SIMILARITY_THRESHOLD)
        
        return {
            "status": "success",
            "username": username,
            "similarity_score": float(similarity),
            "match": is_match,
            "message": "✅ Identity Verified" if is_match else "❌ Identity Mismatch"
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
