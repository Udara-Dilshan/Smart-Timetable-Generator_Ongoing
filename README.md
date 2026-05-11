# Smart Timetable Generator

AI-powered university timetable scheduling system built using FastAPI, PostgreSQL, React, and Genetic Algorithms.

---

# Features

## Backend
- FastAPI REST API
- PostgreSQL database integration
- SQLAlchemy ORM
- CORS support
- Modular architecture

---

## Genetic Algorithm Engine
Implemented complete GA workflow:

- Population generation
- Fitness evaluation
- Selection
- Crossover
- Mutation
- Evolution optimization

---

## Timetable Features
- Random timetable generation
- Optimized timetable generation
- Conflict detection
- Fitness score calculation
- Multi-slot session handling
- Lunch break support
- Hall allocation
- Lecturer allocation

---

## Subject Management
CRUD operations for subjects.

Supports:

- Subject code
- Subject name
- Credits
- Session type
- Student groups
- Preferred hall type

---

## Lecturer Management
CRUD operations for lecturers.

Supports:

- Lecturer name
- Preferred days
- Unavailable days
- Unavailable slots
- Maximum working hours

---

## Frontend Dashboard
Modern React dashboard with:

- Sidebar navigation
- Timetable visualization
- Dynamic timetable rendering
- Fitness score display
- Subject management UI
- Responsive layout

---

# Tech Stack

## Backend
- FastAPI
- Python
- PostgreSQL
- SQLAlchemy

## Frontend
- React
- Axios
- CSS

## Algorithm
- Genetic Algorithm (GA)

---

# Project Structure

```bash
smart_scheduler/
│
├── app/
│   ├── ga/
│   ├── models/
│   ├── services/
│   ├── schemas/
│   ├── database.py
│   └── main.py
│
├── frontend/
│
├── venv/
│
└── README.md
```

---

# API Endpoints

## General
- `GET /test-db`
- `GET /seed-data`

---

## Timetable
- `GET /generate`
- `GET /ga-evolve`
- `GET /ga-optimize`

---

## Subjects
- `GET /subjects`
- `POST /subjects`
- `DELETE /subjects/{id}`

---

## Lecturers
- `GET /lecturers`
- `POST /lecturers`
- `DELETE /lecturers/{id}`

---

# Installation

## Backend Setup

```bash
git clone https://github.com/Udara-Dilshan/smart-timetable-generator.git

cd smart-timetable-generator

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

---

# Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# Current Development

Currently implementing:

- Multi-degree scheduling
- Semester-wise timetable generation
- University-wide conflict management
- CSV/Excel import support
- PDF export
- Analytics dashboard
- Admin panel

---

# Future Goals

- Fully automated university scheduling
- AI-based timetable optimization
- Lecturer workload balancing
- Student clash prevention
- Cloud deployment
- Role-based authentication

---

# Author

Udara Dilshan

BICT Undergraduate  
University Timetable Optimization Project

---

# License

This project is developed for educational and research purposes.
