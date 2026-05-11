from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Subject(Base):

    __tablename__ = "subjects"


    id = Column(Integer, primary_key=True, index=True)

    subject_code = Column(
        String,
        unique=True
    )

    subject_name = Column(String)

    credits = Column(Integer)

    session_type = Column(String)

    shared_subject = Column(
        Boolean,
        default=False
    )

    preferred_hall_type = Column(String)

    student_group = Column(String)