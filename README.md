# Smart Timetable Generator

AI-powered university timetable scheduling system using Genetic Algorithms and Constraint-Based Optimization.

---

# Project Overview

This project is a Smart University Timetable Generator developed using:

* FastAPI
* PostgreSQL
* SQLAlchemy
* Genetic Algorithm Optimization
* Constraint-Based Scheduling

The system automatically generates optimized university timetables while avoiding conflicts between:

* Lecturers
* Lecture halls
* Student groups
* Sessions
* Time slots

---

# Main Features

## Genetic Algorithm Engine

* Population generation
* Fitness calculation
* Selection
* Crossover
* Mutation
* Evolution generations
* Repair-based optimization

## Constraint Handling

### Hard Constraints

* No lecturer overlaps
* No hall overlaps
* No timetable overlaps
* Lunch hour restrictions
* Hall type matching
* Lecturer unavailable slots
* Maximum teaching hours per day
* Continuous lecture blocks

### Soft Constraints

* Minimize idle time
* Avoid late evening classes
* Balance lecturer workload
* Preferred teaching days
* Resource optimization

---

# System Architecture

```text
FastAPI Backend
    ↓
Genetic Algorithm Engine
    ↓
Constraint Validator
    ↓
PostgreSQL Database
```

---

# Technologies Used

| Technology        | Purpose             |
| ----------------- | ------------------- |
| FastAPI           | Backend API         |
| PostgreSQL        | Database            |
| SQLAlchemy        | ORM                 |
| Python            | Core Language       |
| Genetic Algorithm | Optimization Engine |
| GitHub            | Version Control     |

---

# Project Structure

```text
app/
│
├── ga/
│   ├── crossover.py
│   ├── evolution.py
│   ├── fitness.py
│   ├── mutation.py
│   ├── population.py
│   ├── repair.py
│   └── selection.py
│
├── models/
│   ├── faculty.py
│   ├── department.py
│   ├── lecturer.py
│   ├── hall.py
│   ├── subject.py
│   └── timetable.py
│
├── services/
│   ├── conflict_checker.py
│   └── generator.py
│
├── database.py
└── main.py
```

---

# API Endpoints

| Endpoint       | Description                   |
| -------------- | ----------------------------- |
| `/test-db`     | Test database connection      |
| `/seed-data`   | Insert sample university data |
| `/generate`    | Generate random timetable     |
| `/ga-evolve`   | Run single GA evolution       |
| `/ga-optimize` | Generate optimized timetable  |

---

# Installation

## Clone Repository

```bash
git clone https://github.com/Udara-Dilshan/smart-timetable-generator.git
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```

---

# Future Improvements

* React frontend dashboard
* Drag & drop timetable editor
* PDF export
* Excel export
* Lecturer portal
* Student portal
* Advanced analytics
* AI-assisted scheduling
* Multi-campus support

---

# Author

Udara Dilshan

---

# License

This project is developed for educational and research purposes.
