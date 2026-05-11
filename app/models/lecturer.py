from sqlalchemy import Column, Integer, String

from app.database import Base


class Lecturer(Base):

    __tablename__ = "lecturers"

    id = Column(Integer, primary_key=True, index=True)

    lecturer_name = Column(String, nullable=False)

    max_hours_per_day = Column(Integer, default=4)

    preferred_days = Column(String)

    unavailable_day = Column(String)

    unavailable_slot = Column(Integer)