# EduSnap AI — Smart Attendance System (React + FastAPI + PostgreSQL + AI)

EduSnap AI is a smart attendance system that uses **face recognition**
to automatically mark student attendance.

Instead of manually taking attendance, the backend detects faces using
AI models and records attendance directly into the database.

<img width="1024" height="1024" alt="edusnap-logo" src="https://github.com/user-attachments/assets/ab5b388c-5f23-47e1-939f-55345831af6a" />

Three main pieces work together:

```text
browser  →  frontend (React)  →  backend (FastAPI + AI)  →  database (PostgreSQL)
```

* **frontend** — React app built with Vite. Handles the user interface.
* **backend** — FastAPI application that handles APIs, authentication,
  attendance logic, and face recognition.
* **database** — PostgreSQL stores users, students, and attendance records.

The backend also uses:

* **InsightFace**
* **ONNX Runtime**
* **OpenCV**

for AI-based face detection and recognition.

---

# Features

* Face recognition attendance system
* Student registration
* Attendance tracking
* PostgreSQL database integration
* Dockerized frontend + backend + database
* Multi-stage Docker builds
* Persistent AI model storage using Docker volumes
* Docker Hub image deployment
* Docker Compose orchestration

---

# Tech Stack

| Layer            | Technology                  |
| ---------------- | --------------------------- |
| Frontend         | React + Vite + TypeScript   |
| Backend          | FastAPI                     |
| Database         | PostgreSQL                  |
| AI/ML            | InsightFace + ONNX + OpenCV |
| Containerization | Docker                      |
| Orchestration    | Docker Compose              |

---

# What You Need

Only these are required:

* Docker
* Docker Compose

You do NOT need to install:

* Node.js
* Python
* PostgreSQL

Everything runs inside containers.

---

# Part 1 — Manual Docker Setup (Learn How Containers Connect)

Run all commands from the project root.

---

## Step 1 — Create Docker Network

Containers communicate using a shared Docker network.

```bash
docker network create edusnap-net
```

---

## Step 2 — Build Images

Build frontend and backend images.

```bash
docker build -t edusnap-frontend:v1 ./edusnap-frontend

docker build -t edusnap-backend:v1 ./backend
```

The backend build may take several minutes because AI dependencies are large.

---

## Step 3 — Run PostgreSQL Container

```bash
docker run -d --name postgres \
  --network edusnap-net \
  -e POSTGRES_USER=pankaj \
  -e POSTGRES_PASSWORD=cant give \
  -e POSTGRES_DB=edusnap \
  -p 5432:5432 \
  postgres:16-alpine
```

---

## Step 4 — Run Backend Container

```bash
docker run -d --name backend \
  --network edusnap-net \
  -e DATABASE_URL="postgresql://pankaj:cant give@postgres:5432/edusnap" \
  -p 8000:8000 \
  edusnap-backend:v1
```

The backend automatically:

* loads AI models
* initializes FastAPI
* connects to PostgreSQL

---

## Step 5 — Run Frontend Container

```bash
docker run -d --name frontend \
  --network edusnap-net \
  -p 3000:80 \
  edusnap-frontend:v1
```

---

## Step 6 — Open The Application

Frontend:

```text
http://localhost:3000
```

Backend API Docs:

```text
http://localhost:8000/docs
```

---

## Step 7 — Stop Everything

```bash
docker rm -f frontend backend postgres

docker network rm edusnap-net
```

---

# Part 2 — Docker Compose (Recommended)

Docker Compose automates:

* networking
* container startup
* environment variables
* volumes

Start the full stack:

```bash
docker compose up -d
```

Stop everything:

```bash
docker compose down
```

---

# Services

| Service    | URL                        | Description      |
| ---------- | -------------------------- | ---------------- |
| Frontend   | http://localhost:3000      | React UI         |
| Backend    | http://localhost:8000/docs | FastAPI API Docs |
| PostgreSQL | localhost:5432             | Database         |

---

# Persistent AI Models

The backend downloads InsightFace models during the first startup.

Docker volumes are used so models are cached permanently:

```yaml
volumes:
  - insightface_models:/root/.insightface
```

This prevents repeated downloads on future restarts.

---

# Docker Hub Images

Images are available on Docker Hub.

Frontend:

```bash
docker pull pankajdikale/edusnap-frontend:v1
```

Backend:

```bash
docker pull pankajdikale/edusnap-backend:v1
```

---

# Folder Structure

```text
.
├── docker-compose.yml
├── edusnap-frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
│
└── storage/
```

---

# Future Improvements

* GitHub Actions CI/CD
* AWS EC2 deployment
* Nginx reverse proxy
* HTTPS with SSL
* GPU acceleration
* Kubernetes deployment

---

# Author

Pankaj Dikale


📞 Contact
Author: Pankaj Dikale

Email: [pankajdikale@gmail.com]

LinkedIn: [https://www.linkedin.com/in/pankajdikale1313]

GitHub: https://github.com/pankajdikale

⭐ Star this repo if you found it helpful! ⭐

Built with ❤️ using AI and modern web technologies.
