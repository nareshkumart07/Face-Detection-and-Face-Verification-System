from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import ml_engine
import database
from database import User

# Initialize Database tables
database.init_db()

app = FastAPI(title="Face Verification System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Serve the HTML file at the root URL
@app.get("/")
def read_index():
    return FileResponse("index.html")

# 2. Separate endpoint for checking API status
@app.get("/health")
def health_check():
    return {"status": "System is running", "database_url": database.DATABASE_URL.split("://")[0]}

@app.post("/register")
def register_face(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    try:
        print(f"Start registration for: {name}")
        
        # Read file synchronously to avoid async loop blocking on CPU tasks
        file_bytes = file.file.read()
        
        # Process image
        cv2_img = ml_engine.process_image_bytes(file_bytes)

        # 1. Validate Face
        if not ml_engine.check_face_exists(cv2_img):
            raise HTTPException(status_code=400, detail="No face detected. Please look directly at the camera.")

        # 2. Generate Embedding
        try:
            embedding_list = ml_engine.get_embedding(cv2_img)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # 3. Save to DB
        new_user = User(name=name)
        new_user.set_embedding_list(embedding_list)
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"Successfully saved user {name} with ID {new_user.id}")
        return {"message": f"User {name} registered successfully", "user_id": new_user.id}

    except Exception as e:
        print(f"Error during register: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
def verify_face(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    try:
        print("Start verification")
        
        # Read file synchronously
        file_bytes = file.file.read()
        
        # Process image
        cv2_img = ml_engine.process_image_bytes(file_bytes)

        if not ml_engine.check_face_exists(cv2_img):
            raise HTTPException(status_code=400, detail="No face detected. Please adjust lighting or position.")

        try:
            current_embedding = ml_engine.get_embedding(cv2_img)
        except ValueError:
            raise HTTPException(status_code=400, detail="Could not extract features from face.")

        # Fetch all users
        users = db.query(User).all()
        if not users:
             return {"status": "success", "match": False, "person": "Unknown (Database Empty)", "similarity": 0.0}
        
        best_match = None
        highest_similarity = -1.0
        threshold = 0.5

        for user in users:
            db_embedding = user.get_embedding_list()
            sim = ml_engine.calculate_similarity(current_embedding, db_embedding)
            
            if sim > highest_similarity:
                highest_similarity = sim
                best_match = user

        print(f"Best match: {best_match.name if best_match else 'None'} with score {highest_similarity}")

        if best_match and highest_similarity >= threshold:
            return {
                "status": "success",
                "match": True,
                "person": best_match.name,
                "similarity": float(highest_similarity)
            }
        else:
            return {
                "status": "success",
                "match": False,
                "person": "Unknown",
                "similarity": float(highest_similarity)
            }

    except Exception as e:
        print(f"Error verify: {e}")
        raise HTTPException(status_code=500, detail=str(e))
