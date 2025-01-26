from .utils.database import SessionLocal
from .models import User, Patient
from datetime import date, datetime, timezone

db = SessionLocal()

users = [
    User(username="doctor1", password_hash="hashed_password1", role="doctor"),
    User(username="nurse1", password_hash="hashed_password2", role="nurse"),
]

patients = [
    Patient(
        date_of_birth=date(1990, 1, 1),
        diagnoses="Diagnosis1,Diagnosis2",
        created_at=datetime.now(timezone.utc),
    ),
    Patient(
        date_of_birth=date(1985, 5, 5),
        diagnoses="Diagnosis3",
        created_at=datetime.now(timezone.utc),
    ),
]

db.add_all(users)
db.add_all(patients)
db.commit()
