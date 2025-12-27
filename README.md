FaceAuth: Face Detection & Verification System

A robust, web-based Face Verification System built with FastAPI and InsightFace. This application allows users to register their faces via a live camera interface and verify their identity against a database of stored embeddings.

It is designed to be mobile-friendly and easily deployable on cloud platforms like Railway.

🚀 Features

Live Camera Interface: Capture photos directly from your webcam or mobile selfie camera.

Face Registration: Detects faces, generates embeddings, and stores them in a database.

Identity Verification: Compares a live capture against all registered users to find a match.

Dual-Stack ML: Uses MTCNN for reliable face detection and ArcFace (InsightFace) for high-accuracy feature extraction.

Database Agnostic: Automatically switches between SQLite (local development) and PostgreSQL (production/Railway).

Mobile Optimized: Responsive UI with Tailwind CSS, specifically tuned for mobile portrait modes and iOS security constraints.

🛠️ Tech Stack

Backend: Python 3.9+, FastAPI, SQLAlchemy

Machine Learning: PyTorch, InsightFace (ArcFace), MTCNN

Frontend: HTML5, JavaScript, Tailwind CSS (served via FastAPI)

Database: PostgreSQL (Production) / SQLite (Dev)

Deployment: Docker / Railway (Procfile included)

📂 Project Structure

/
├── main.py           # FastAPI entry point and API endpoints
├── database.py       # Database connection and User model
├── ml_engine.py      # Core logic for Face Detection & Embedding generation
├── index.html        # Frontend UI (served at root /)
├── requirements.txt  # Python dependencies
└── Procfile          # Deployment command for Railway/Heroku


⚡ Local Setup & Installation

Clone the Repository

git clone [https://github.com/yourusername/face-auth-system.git](https://github.com/yourusername/face-auth-system.git)
cd face-auth-system


Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies
Note: On Windows, you might need C++ build tools installed.

pip install -r requirements.txt


Run the Application

uvicorn main:app --reload


The app will start at http://127.0.0.1:8000.

Important: To use the camera on mobile devices connecting to your local computer, you must use HTTPS (or localhost). Mobile browsers block camera access on non-secure HTTP connections (except localhost).

☁️ Deployment on Railway

Push to GitHub: Ensure your code is in a GitHub repository.

Create Project: Login to Railway and create a "New Project" > "Deploy from GitHub repo".

Add Database:

Right-click on the canvas or click "New" > "Database" > "PostgreSQL".

Railway will automatically inject the DATABASE_URL environment variable into your app.

Wait for Build:

The first build may take a few minutes as it downloads the ML models (specifically buffalo_l).

Public Domain:

Go to "Settings" > "Networking" and generate a domain.

Open the link on your phone to test the camera.

🔌 API Endpoints

Method

Endpoint

Description

GET

/

Serves the index.html frontend.

GET

/health

Returns system status and database connection type.

POST

/register

Accepts name (string) and file (image) to register a user.

POST

/verify

Accepts file (image) and returns the best matching user.

📱 Mobile Compatibility Notes

iOS/Safari: The application includes playsinline attributes and specific facingMode: "user" constraints to ensure the selfie camera works correctly on iPhones.

HTTPS Required: Camera access is blocked by browsers on non-secure (HTTP) connections. When deployed on Railway, HTTPS is provided automatically.

🛡️ License

This project is open-source. Feel free to use and modify it.
