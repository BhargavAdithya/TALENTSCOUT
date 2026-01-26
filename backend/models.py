# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from sqlalchemy.orm import Session
from database import get_db

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    phone = Column(String(20), unique=True, index=True)
    experience = Column(Float)
    position = Column(String(100))
    location = Column(String(200))
    tech_stack = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    interviews = relationship("Interview", back_populates="candidate")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    status = Column(String(50))
    candidate_rating = Column(Float, nullable=True)  # Rating out of 5 based on overall performance
    violations = Column(Integer, default=0)

    candidate = relationship("Candidate", back_populates="interviews")
    questions = relationship("Question", back_populates="interview")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    question_text = Column(Text)
    answer_text = Column(Text)
    difficulty = Column(Float)
    score = Column(Float) # Score out of 10 for the answer
    answered_at = Column(DateTime, default=datetime.utcnow)

    interview = relationship("Interview", back_populates="questions")