from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    email = Column(String(200))
    phone = Column(String(30))
    skills = Column(Text)
    education = Column(Text)
    experience_years = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
