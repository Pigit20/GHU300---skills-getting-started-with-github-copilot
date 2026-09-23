from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 2,
                "participants": ["michael@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 2,
                "participants": ["emma@mergington.edu"],
            },
        }
    )


def test_duplicate_registration_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already registered for this activity"


def test_duplicate_activity_creation_is_rejected():
    response = client.post(
        "/activities",
        json={
            "name": "Chess Club",
            "description": "Duplicate activity",
            "schedule": "Mondays, 4:00 PM",
            "max_participants": 8,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity already exists"
