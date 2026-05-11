from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import SessionLocal, engine, Base

from app.models.subject import Subject
from app.models.lecturer import Lecturer
from app.models.hall import Hall
from app.models.timetable import Timetable

from app.services.generator import generate_random_timetable

from app.ga.population import generate_population
from app.ga.fitness import calculate_fitness
from app.ga.selection import select_best
from app.ga.crossover import crossover
from app.ga.mutation import mutate
from app.ga.evolution import evolve_timetable

from app.schemas.subject_schema import (
    SubjectCreate,
    SubjectResponse
)

app = FastAPI()

Base.metadata.create_all(bind=engine)


# DATABASE SESSION
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# CORS
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================
# PYDANTIC MODELS
# =========================

class LecturerCreate(BaseModel):

    lecturer_name: str

    max_hours_per_day: int

    preferred_days: str

    unavailable_day: str

    unavailable_slot: int


class LecturerResponse(BaseModel):

    id: int

    lecturer_name: str

    max_hours_per_day: int

    preferred_days: str

    unavailable_day: str

    unavailable_slot: int

    class Config:

        from_attributes = True


# =========================
# TEST DATABASE
# =========================

@app.get("/test-db")
def test_db():

    return {

        "message": "Database connected successfully"
    }


# =========================
# SEED SAMPLE DATA
# =========================

@app.get("/seed-data")
def seed_data(db: Session = Depends(get_db)):

    # CLEAR OLD DATA
    db.query(Timetable).delete()
    db.query(Subject).delete()
    db.query(Lecturer).delete()
    db.query(Hall).delete()

    db.commit()

    # SUBJECTS
    subjects = [

        Subject(

            subject_code="SE101",

            subject_name="Programming Fundamentals",

            credits=3,

            session_type="Practical",

            shared_subject=False,

            preferred_hall_type="ICT Lab",

            student_group="Y1S1-SE"
        ),

        Subject(

            subject_code="SE102",

            subject_name="Database Systems",

            credits=2,

            session_type="Lecture",

            shared_subject=False,

            preferred_hall_type="Lecture Hall",

            student_group="Y1S1-SE"
        ),

        Subject(

            subject_code="SE103",

            subject_name="Discrete Mathematics",

            credits=3,

            session_type="Lecture",

            shared_subject=False,

            preferred_hall_type="Lecture Hall",

            student_group="Y1S1-SE"
        ),

        Subject(

            subject_code="SE104",

            subject_name="Computer Architecture",

            credits=2,

            session_type="Lecture",

            shared_subject=False,

            preferred_hall_type="Smart Room",

            student_group="Y1S1-SE"
        ),

        Subject(

            subject_code="SE105",

            subject_name="Communication Skills",

            credits=1,

            session_type="Lecture",

            shared_subject=True,

            preferred_hall_type="Lecture Hall",

            student_group="ALL-Y1"
        )
    ]

    # LECTURERS
    lecturers = [

        Lecturer(

            lecturer_name="Dr. Nimal",

            max_hours_per_day=6,

            preferred_days="Monday,Wednesday",

            unavailable_day="Friday",

            unavailable_slot=6
        ),

        Lecturer(

            lecturer_name="Prof. Sachini",

            max_hours_per_day=5,

            preferred_days="Tuesday,Thursday",

            unavailable_day="Monday",

            unavailable_slot=1
        ),

        Lecturer(

            lecturer_name="Dr. Silva",

            max_hours_per_day=4,

            preferred_days="Friday",

            unavailable_day="Wednesday",

            unavailable_slot=3
        )
    ]

    # HALLS
    halls = [

        Hall(

            hall_name="ICT Lab 01",

            hall_type="ICT Lab",

            capacity=60
        ),

        Hall(

            hall_name="Lecture Hall A",

            hall_type="Lecture Hall",

            capacity=120
        ),

        Hall(

            hall_name="Smart Room 01",

            hall_type="Smart Room",

            capacity=80
        )
    ]

    db.add_all(subjects)

    db.add_all(lecturers)

    db.add_all(halls)

    db.commit()

    return {

        "message": "Sample data inserted successfully"
    }


# =========================
# RANDOM TIMETABLE
# =========================

@app.get("/generate")
def generate(db: Session = Depends(get_db)):

    timetable = generate_random_timetable(db)

    return {

        "generated_timetable": timetable
    }


# =========================
# GA EVOLVE
# =========================

@app.get("/ga-evolve")
def ga_evolve(db: Session = Depends(get_db)):

    population = generate_population(db, size=6)

    scored_population = []

    for timetable in population:

        fitness = calculate_fitness(timetable)

        scored_population.append({

            "fitness_score": fitness,

            "timetable": timetable
        })

    best = select_best(scored_population)

    parent1 = best[0]["timetable"]

    parent2 = best[1]["timetable"]

    child = crossover(parent1, parent2)

    mutated_child = mutate(child)

    child_fitness = calculate_fitness(mutated_child)

    return {

        "parent_1_fitness": best[0]["fitness_score"],

        "parent_2_fitness": best[1]["fitness_score"],

        "child_fitness": child_fitness,

        "child_timetable": mutated_child
    }


# =========================
# FULL OPTIMIZATION
# =========================

@app.get("/ga-optimize")
def ga_optimize(db: Session = Depends(get_db)):

    result = evolve_timetable(

        db=db,

        generations=30
    )

    return result


# =========================
# SUBJECT APIs
# =========================

@app.get("/subjects")
def get_subjects(db: Session = Depends(get_db)):

    subjects = db.query(Subject).all()

    return subjects


@app.post(
    "/subjects",
    response_model=SubjectResponse
)
def create_subject(

    subject: SubjectCreate,

    db: Session = Depends(get_db)
):

    new_subject = Subject(

        subject_code=subject.subject_code,

        subject_name=subject.subject_name,

        credits=subject.credits,

        session_type=subject.session_type,

        preferred_hall_type=subject.preferred_hall_type,

        student_group=subject.student_group
    )

    db.add(new_subject)

    db.commit()

    db.refresh(new_subject)

    return new_subject


@app.delete("/subjects/{subject_id}")
def delete_subject(

    subject_id: int,

    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(

        Subject.id == subject_id

    ).first()

    if not subject:

        return {

            "message": "Subject not found"
        }

    db.delete(subject)

    db.commit()

    return {

        "message": "Subject deleted"
    }


# =========================
# LECTURER APIs
# =========================

@app.get(
    "/lecturers",
    response_model=list[LecturerResponse]
)
def get_lecturers(db: Session = Depends(get_db)):

    return db.query(Lecturer).all()


@app.post(
    "/lecturers",
    response_model=LecturerResponse
)
def create_lecturer(

    lecturer: LecturerCreate,

    db: Session = Depends(get_db)
):

    new_lecturer = Lecturer(

        lecturer_name=lecturer.lecturer_name,

        max_hours_per_day=lecturer.max_hours_per_day,

        preferred_days=lecturer.preferred_days,

        unavailable_day=lecturer.unavailable_day,

        unavailable_slot=lecturer.unavailable_slot
    )

    db.add(new_lecturer)

    db.commit()

    db.refresh(new_lecturer)

    return new_lecturer


@app.delete("/lecturers/{lecturer_id}")
def delete_lecturer(

    lecturer_id: int,

    db: Session = Depends(get_db)
):

    lecturer = db.query(Lecturer).filter(

        Lecturer.id == lecturer_id

    ).first()

    if lecturer:

        db.delete(lecturer)

        db.commit()

    return {

        "message": "Lecturer deleted"
    }