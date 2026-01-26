# backend/schemas.py
from pydantic import BaseModel

class CandidateCreate(BaseModel):
    name: str
    email: str
    phone: str
    experience: float
    position: str
    location: str
    tech_stack: str

class AnswerRequest(BaseModel):
    interview_id: int
    question: str
    answer: str