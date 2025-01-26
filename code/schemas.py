from datetime import date, datetime
import json
from typing import List
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Patient(BaseModel):
    id: int
    date_of_birth: date
    diagnoses: List[str]
    created_at: datetime

    class Config:
        from_attributes = True
