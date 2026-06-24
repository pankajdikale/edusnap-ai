# EduSnap AI — AI Powered Attendance Management System

EduSnap AI is a full-stack AI-powered attendance management system that uses face recognition to automatically identify students and mark attendance.

The project is fully containerized using Docker and includes an automated CI/CD pipeline with GitHub Actions and Docker Hub.

<img width="1024" height="1024" alt="edusnap-logo" src="https://github.com/user-attachments/assets/ab5b388c-5f23-47e1-939f-55345831af6a" />

---

# Features

* AI-powered face recognition attendance
* FastAPI backend
* React + Vite frontend
* PostgreSQL database
* Dockerized architecture
* Docker Compose support
* GitHub Actions CI/CD pipeline
* Docker Hub image publishing
* Swagger API documentation
* Multi-container deployment ready

---

# Tech Stack

## Frontend

* React
* TypeScript
* Vite
* TailwindCSS
* Zustand

## Backend

* FastAPI
* SQLAlchemy
* InsightFace
* OpenCV
* ONNX Runtime
* PostgreSQL

## DevOps

* Docker
* Docker Compose
* GitHub Actions
* Docker Hub

---

# System Architecture

```text
Browser
   ↓
Frontend (React + Vite)
   ↓
Backend API (FastAPI + AI)
   ↓
PostgreSQL Database
```

---

# Project Structure

```text
edusnap-ai/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── edusnap-frontend/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
│
└── .github/workflows/
    └── docker-ci.yml
```

---

# Run Locally With Docker

## Requirements

Install:

* Docker
* Docker Compose

You do NOT need:

* Node.js
* Python
* PostgreSQL

Everything runs inside containers.

---

# Step 1 — Clone Repository

```bash
git clone git@github.com:pankajdikale/edusnap-ai.git

cd edusnap-ai
```

---

# Step 2 — Start Containers

```bash
docker-compose up -d
```

This starts:

* frontend
* backend
* postgres database

---

# Step 3 — Open Application

## Frontend

```text
http://localhost:3000
```

## Backend Swagger Docs

```text
http://localhost:8000/docs
```

---

# Stop Containers

```bash
docker-compose down
```

---

# View Logs

```bash
docker-compose logs -f
```

---

# Docker Images

The project images are available on Docker Hub.

## Frontend Image

```text
pankajdikale/edusnap-frontend:v1
```

## Backend Image

```text
pankajdikale/edusnap-backend:v1
```

---

# Run Using Docker Hub Images

```bash
docker-compose up -d
```

Docker automatically pulls the images from Docker Hub.

---

# Build Images Manually

## Frontend

```bash
cd edusnap-frontend

docker build -t edusnap-frontend:v1 .
```

## Backend

```bash
cd backend

docker build -t edusnap-backend:v1 .
```

---

# CI/CD Pipeline

This project includes a GitHub Actions CI/CD pipeline.

Whenever code is pushed to the `main` branch:

1. GitHub Actions starts automatically
2. Frontend Docker image is built
3. Backend Docker image is built
4. Images are pushed to Docker Hub automatically

Workflow file:

```text
.github/workflows/docker-ci.yml
```

---

# Deploy On AWS EC2

## Step 1 — Launch EC2 Instance

Recommended:

* Ubuntu Server 22.04
* t2.medium or higher

---

# Step 2 — Install Docker

```bash
sudo apt update

sudo apt install docker.io docker-compose -y
```

Enable Docker:

```bash
sudo systemctl enable docker

sudo systemctl start docker
```

---

# Step 3 — Clone Repository

```bash
git clone git@github.com:pankajdikale/edusnap-ai.git

cd edusnap-ai
```

---

# Step 4 — Start Containers

```bash
docker-compose up -d
```

Docker will:

* pull images from Docker Hub
* create containers
* start services automatically

---

# Step 5 — Open Security Group Ports

Allow:

| Port | Purpose     |
| ---- | ----------- |
| 3000 | Frontend    |
| 8000 | Backend API |
| 22   | SSH         |

---

# Step 6 — Access Application

```text
http://EC2_PUBLIC_IP:3000
```

Swagger docs:

```text
http://EC2_PUBLIC_IP:8000/docs
```

---

# Useful Commands

## Running Containers

```bash
docker ps
```

## Stop Everything

```bash
docker-compose down
```

## Restart Containers

```bash
docker-compose restart
```

## Rebuild Containers

```bash
docker-compose up --build
```

---

# Future Improvements

* Nginx reverse proxy
* HTTPS with SSL
* Domain setup
* Kubernetes deployment
* Monitoring with Prometheus/Grafana
* Auto deployment to EC2
* GPU acceleration for AI inference

---

📞 Contact
Author: Pankaj Dikale

Email: [pankajdikale@gmail.com]

LinkedIn: [https://www.linkedin.com/in/pankajdikale1313]

GitHub: https://github.com/pankajdikale

⭐ Star this repo if you found it helpful! ⭐

Built with ❤️ using AI and modern web technologies.
