🚀 EduSnap AI: AI-Powered Smart Face Recognition Attendance System

Revolutionizing attendance with cutting-edge AI face recognition technology. Built for modern educational institutions.
<img width="1024" height="1024" alt="edusnap-logo" src="https://github.com/user-attachments/assets/ab5b388c-5f23-47e1-939f-55345831af6a" />
✨ Features

🤖 AI-Powered Recognition: Face detection and matching using InsightFace (ArcFace) with 98% accuracy.

🎨 Modern UI: Responsive React frontend with glassmorphism design, animations, and dark mode support.

🔐 Secure Backend: FastAPI with JWT authentication, role-based access (Admin/Faculty), and PostgreSQL database.

📊 Smart Reports: Auto-generate CSV/PDF reports with student details, department info, and attendance stats.

📱 Mobile-Friendly: Fully responsive design for desktops, tablets, and phones.

🐳 DevOps Ready: Containerized with Docker, CI/CD pipelines, deployable on Heroku/AWS.

📈 Real-Time Processing: Instant attendance marking from classroom images.

🖼️ Screenshots

Landing Page
<img width="1516" height="941" alt="Screenshot 2026-01-22 150136" src="https://github.com/user-attachments/assets/bad35994-0fbc-4ea8-b206-a9d44d075b0a" />

Login Form
<img width="1920" height="1140" alt="Screenshot 2026-01-22 150531" src="https://github.com/user-attachments/assets/5659e934-8cfc-4640-acfc-e47c77bd1120" />

Attendance Results
<img width="967" height="1144" alt="Screenshot 2026-01-22 151113" src="https://github.com/user-attachments/assets/6fc72b2c-c9cf-40d3-a3ed-53edd3141c24" />

More screenshots in the screenshots/ folder.

🛠️ Tech Stack

Frontend
React (TypeScript) - Dynamic UI components
Zustand - State management
Axios - API communication
CSS3 - Custom styling with animations

Backend
FastAPI (Python) - High-performance API
SQLAlchemy - ORM for database
InsightFace - AI face recognition
OpenCV - Image processing

Database & DevOps
PostgreSQL - Relational database
Docker - Containerization
GitHub Actions - CI/CD (optional)
Heroku/AWS - Cloud deployment

📦 Installation & Setup
Prerequisites
Python 3.10+
Node.js 18+
PostgreSQL
Docker (optional)

1. Clone the Repository
bash
Copy code
git clone https://github.com/pankajdikale/edusnap-ai.git
cd edusnap-ai

 3. Backend Setup
bash
Copy code
cd backend
pip install -r requirements.txt
set up PostgreSQL DB (local or cloud)
uvicorn app.main:app --reload
API runs on: http://localhost:8000
Docs: http://localhost:8000/docs

4. Frontend Setup
bash
Copy code
cd ../frontend
npm install
npm run dev
App runs on: http://localhost:3000

5. Database Setup
Create a PostgreSQL database.
Run migrations or create tables manually (see backend/app/core/models.py).

7. Docker (Optional)
bash
Copy code
docker-compose up --build

🎯 Usage
Register/Login: Create an account as Faculty or Admin.
Add Students: Upload student photos for face encoding.
Upload Attendance: Capture classroom image → AI detects faces → Marks attendance.
View Results: See processed image, student list, and stats.
Download Reports: Get latest CSV/PDF with attendance data.

API Endpoints
POST /api/auth/login - User login
POST /api/attendance/upload - Upload image/CSV
GET /api/attendance/results - Get results
GET /api/attendance/download/latest/csv - Download CSV
GET /api/attendance/download/latest/pdf - Download PDF

🚀 Deployment
Heroku (Easy)
Create Heroku app: heroku create edusnap-backend
Add PostgreSQL: heroku addons:create heroku-postgresql
Push: git push heroku main
Access: https://edusnap-backend.herokuapp.com
AWS (Production)
Use ECS/Fargate for containers.
RDS for PostgreSQL.
S3 for static files.

🤝 Contributing
We welcome contributions! 🚀

Fork the repo.
Create a feature branch: git checkout -b feature/amazing-feature
Commit changes: git commit -m 'Add amazing feature'
Push: git push origin feature/amazing-feature
Open a Pull Request.

Guidelines
Follow PEP8 for Python.
Use TypeScript for React.
Add tests for new features.


📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


🙏 Acknowledgments
InsightFace for AI models.
FastAPI community for awesome docs.
React for building UIs.
Inspired by modern attendance systems.


📞 Contact
Author: Pankaj Dikale

Email: [pankajdikale@gmail.com]

LinkedIn: [https://www.linkedin.com/in/pankajdikale1313]

GitHub: https://github.com/pankajdikale

⭐ Star this repo if you found it helpful! ⭐

Built with ❤️ using AI and modern web technologies.