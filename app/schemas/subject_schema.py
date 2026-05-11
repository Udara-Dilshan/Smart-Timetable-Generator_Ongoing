from pydantic import BaseModel


class SubjectCreate(BaseModel):

    subject_code: str
    subject_name: str
    credits: int
    session_type: str
    preferred_hall_type: str
    student_group: str


class SubjectResponse(BaseModel):

    id: int
    subject_code: str
    subject_name: str
    credits: int
    session_type: str
    preferred_hall_type: str
    student_group: str

    class Config:

        from_attributes = True