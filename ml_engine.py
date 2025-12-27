import numpy as np
import cv2
from facenet_pytorch import MTCNN
from insightface.app import FaceAnalysis
from PIL import Image
import io

# Initialize models globally to load them only once
print("Loading ML models... this may take a moment.")

# MTCNN for validation (CPU is safer for free tier deployments)
mtcnn = MTCNN(keep_all=False, device='cpu')

# ArcFace for embeddings
arcface = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
arcface.prepare(ctx_id=0, det_size=(640, 640))

print("Models loaded successfully.")

def process_image_bytes(file_bytes):
    """
    Converts uploaded file bytes to:
    1. PIL Image (for MTCNN)
    2. CV2 Image (for ArcFace)
    """
    # Convert to PIL
    pil_image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    
    # Convert to CV2 (OpenCV uses BGR)
    nparr = np.frombuffer(file_bytes, np.uint8)
    cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return pil_image, cv2_image

def check_face_exists(pil_image):
    """
    Returns True if MTCNN detects a face.
    """
    face = mtcnn(pil_image)
    return face is not None

def get_embedding(cv2_image):
    """
    Returns the embedding of the primary face detected by ArcFace.
    """
    # InsightFace expects BGR image (standard OpenCV format)
    faces = arcface.get(cv2_image)

    if len(faces) == 0:
        raise ValueError("No face detected by ArcFace during embedding generation.")

    # Get the face with the highest detection score (most likely the main subject)
    # faces.sort(key=lambda x: x.det_score, reverse=True)
    
    embedding = faces[0].embedding
    
    # Normalize the embedding
    embedding = embedding / np.linalg.norm(embedding)
    
    # Convert numpy float32 to standard python float for JSON serialization
    return embedding.tolist()

def calculate_similarity(emb1, emb2):
    """
    Calculates Cosine Similarity between two embeddings.
    """
    # Convert back to numpy arrays
    e1 = np.array(emb1)
    e2 = np.array(emb2)
    
    return np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
