from datetime import datetime, timezone
from sqlalchemy import DATE, Column, DateTime, Integer, String, JSON
from .utils.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    date_of_birth = Column(DATE)
    diagnoses = Column(JSON)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
