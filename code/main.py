from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .utils.auth import authenticate_user, get_current_user
from .utils.security import create_access_token
from .utils.database import get_db
from .models import User, Patient
from .schemas import Token, Patient as PatientSchema
from sqlalchemy.orm import Session
from datetime import timedelta

app = FastAPI()


@app.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/patients", response_model=list[PatientSchema])
def get_patients(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if current_user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors can access this endpoint",
        )
    patients = db.query(Patient).all()
    if not patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No patients found"
        )
    return patients
