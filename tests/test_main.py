from fastapi import status
from code.utils.security import get_password_hash
from code.models import User, Patient
from datetime import date, datetime, timezone


def test_login_success(client, db_session):
    test_user = User(
        username="testdoctor",
        password_hash=get_password_hash("password"),
        role="doctor",
    )
    db_session.add(test_user)
    db_session.commit()

    response = client.post(
        "/login", data={"username": "testdoctor", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, db_session):

    test_user = User(
        username="testuser", password_hash=get_password_hash("password"), role="user"
    )
    db_session.add(test_user)
    db_session.commit()

    response = client.post(
        "/login", data={"username": "testuser", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_patients_success(client, db_session):
    test_doctor = User(
        username="testdoctor",
        password_hash=get_password_hash("password"),
        role="doctor",
    )
    db_session.add(test_doctor)
    db_session.commit()

    response = client.post(
        "/login", data={"username": "testdoctor", "password": "password"}
    )
    token = response.json()["access_token"]

    test_patient = Patient(
        date_of_birth=date(1990, 1, 1),
        diagnoses=["Flu"],
        created_at=datetime.now(timezone.utc),
    )
    db_session.add(test_patient)
    db_session.commit()

    response = client.get("/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == test_patient.id
    assert data[0]["diagnoses"] == ["Flu"]


def test_get_patients_forbidden(client, db_session):
    test_user = User(
        username="testuser", password_hash=get_password_hash("password"), role="user"
    )
    db_session.add(test_user)
    db_session.commit()

    response = client.post(
        "/login", data={"username": "testuser", "password": "password"}
    )
    token = response.json()["access_token"]

    response = client.get("/patients", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Only doctors can access this endpoint"
