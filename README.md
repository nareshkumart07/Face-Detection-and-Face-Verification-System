<div align="center">

# 🔐 FaceAuth: Face Detection & Verification System

**A robust, web-based face verification system built with FastAPI and InsightFace.**<br/>
Register faces via live camera and verify identity against a stored embeddings database.

<br/>

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

[![Railway](https://img.shields.io/badge/Deploy%20on%20Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)
[![AWS](https://img.shields.io/badge/Deploy%20on%20AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![DigitalOcean](https://img.shields.io/badge/Deploy%20on%20DigitalOcean-0080FF?style=for-the-badge&logo=digitalocean&logoColor=white)](https://digitalocean.com)

</div>

---

## 🌟 Overview

FaceAuth is a mobile-friendly, cloud-deployable face verification system that uses **MTCNN** for reliable face detection and **ArcFace (InsightFace)** for high-accuracy feature extraction. Users can register their face via a live camera and verify identity against a database of stored embeddings — all through a clean browser interface.

---

## 🚀 Features

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>📷 <strong>Live Camera Interface</strong></td>
      <td>Capture photos directly from your webcam or mobile selfie camera.</td>
    </tr>
    <tr>
      <td>🧾 <strong>Face Registration</strong></td>
      <td>Detects faces, generates embeddings, and stores them in a database.</td>
    </tr>
    <tr>
      <td>✅ <strong>Identity Verification</strong></td>
      <td>Compares a live capture against all registered users to find the best match.</td>
    </tr>
    <tr>
      <td>🧠 <strong>Dual-Stack ML</strong></td>
      <td>MTCNN for face detection + ArcFace (InsightFace) for high-accuracy feature extraction.</td>
    </tr>
    <tr>
      <td>🗄️ <strong>Database Agnostic</strong></td>
      <td>Auto-switches between SQLite (local dev) and PostgreSQL (production).</td>
    </tr>
    <tr>
      <td>📱 <strong>Mobile Optimized</strong></td>
      <td>Responsive Tailwind CSS UI, tuned for mobile portrait modes and iOS Safari constraints.</td>
    </tr>
  </tbody>
</table>

---

## 🛠️ Tech Stack

<table>
  <thead>
    <tr><th>Domain</th><th>Technologies</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Backend</strong></td>
      <td>
        <img src="https://img.shields.io/badge/Python_3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white"/>
        <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white"/>
        <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white"/>
      </td>
    </tr>
    <tr>
      <td><strong>Machine Learning</strong></td>
      <td>
        <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white"/>
        <img src="https://img.shields.io/badge/InsightFace_(ArcFace)-6366F1?style=flat-square"/>
        <img src="https://img.shields.io/badge/MTCNN-009688?style=flat-square"/>
      </td>
    </tr>
    <tr>
      <td><strong>Frontend</strong></td>
      <td>
        <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white"/>
        <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black"/>
        <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white"/>
      </td>
    </tr>
    <tr>
      <td><strong>Database</strong></td>
      <td>
        <img src="https://img.shields.io/badge/PostgreSQL_(Prod)-4169E1?style=flat-square&logo=postgresql&logoColor=white"/>
        <img src="https://img.shields.io/badge/SQLite_(Dev)-003B57?style=flat-square&logo=sqlite&logoColor=white"/>
      </td>
    </tr>
    <tr>
      <td><strong>Deployment</strong></td>
      <td>
        <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/>
        <img src="https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white"/>
        <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonaws&logoColor=white"/>
        <img src="https://img.shields.io/badge/DigitalOcean-0080FF?style=flat-square&logo=digitalocean&logoColor=white"/>
      </td>
    </tr>
  </tbody>
</table>

---

## 📂 Project Structure

```
📦 face-auth-system/
├── main.py           # FastAPI entry point and API endpoints
├── database.py       # Database connection and User model
├── ml_engine.py      # Core logic for face detection and embedding generation
├── index.html        # Frontend UI (served at root /)
├── requirements.txt  # Python dependencies
└── Procfile          # Deployment command for Railway / Heroku
```

---

## ⚡ Local Setup & Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/face-auth-system.git
cd face-auth-system
```

**2. Create a virtual environment**

<table>
<tr><th>Windows</th><th>macOS / Linux</th></tr>
<tr>
<td>

```bash
python -m venv venv
venv\Scripts\activate
```

</td>
<td>

```bash
python3 -m venv venv
source venv/bin/activate
```

</td>
</tr>
</table>

**3. Install dependencies**

> **Note:** On Windows, you may need [C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) installed first.

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
uvicorn main:app --reload
```

The app starts at `http://127.0.0.1:8000`.

> **Important:** To use the camera on mobile devices over your local network, you must use HTTPS or `localhost`. Mobile browsers block camera access on plain HTTP connections.

---

## ☁️ Deployment on Railway

<table>
  <thead>
    <tr><th>Step</th><th>Action</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>1. Push to GitHub</strong></td>
      <td>Make sure your code is in a GitHub repository.</td>
    </tr>
    <tr>
      <td><strong>2. Create Project</strong></td>
      <td>Login to Railway → <strong>New Project</strong> → <strong>Deploy from GitHub repo</strong>.</td>
    </tr>
    <tr>
      <td><strong>3. Add PostgreSQL</strong></td>
      <td>Click <strong>New</strong> → <strong>Database</strong> → <strong>PostgreSQL</strong>. Railway auto-injects <code>DATABASE_URL</code>.</td>
    </tr>
    <tr>
      <td><strong>4. Wait for Build</strong></td>
      <td>First build may take a few minutes — it downloads the <code>buffalo_l</code> ML model.</td>
    </tr>
    <tr>
      <td><strong>5. Get Public Domain</strong></td>
      <td>Go to <strong>Settings</strong> → <strong>Networking</strong> → Generate a domain. Open on your phone to test the camera.</td>
    </tr>
  </tbody>
</table>

---

## 🔌 API Endpoints

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Endpoint</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GET</code></td>
      <td><code>/</code></td>
      <td>Serves the <code>index.html</code> frontend.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/health</code></td>
      <td>Returns system status and active database connection type.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/register</code></td>
      <td>Accepts <code>name</code> (string) and <code>file</code> (image) to register a user.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/verify</code></td>
      <td>Accepts <code>file</code> (image) and returns the best matching registered user.</td>
    </tr>
  </tbody>
</table>

---

## 📱 Mobile Compatibility Notes

<table>
  <tr>
    <td>🍎 <strong>iOS / Safari</strong></td>
    <td>Includes <code>playsinline</code> attributes and <code>facingMode: "user"</code> constraints to ensure the selfie camera works correctly on iPhones.</td>
  </tr>
  <tr>
    <td>🔒 <strong>HTTPS Required</strong></td>
    <td>Camera access is blocked on non-secure HTTP connections. Railway provides HTTPS automatically on deployment.</td>
  </tr>
</table>

---

## 🤝 Contributing

Contributions are welcome and greatly appreciated!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <em>Built for developers who need fast, private, and deployable face verification — without the complexity.</em>
</div>
