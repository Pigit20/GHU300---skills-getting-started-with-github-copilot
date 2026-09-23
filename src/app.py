"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:45 PM - 5:15 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "noah@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Practice soccer drills and compete in school matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["liam@mergington.edu", "zoe@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Work on shooting, passing, and team play in basketball sessions",
        "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "mia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities")
def create_activity(activity: dict):
    """Create a new activity after validating the required fields."""
    name = str(activity.get("name", "")).strip()
    description = str(activity.get("description", "")).strip()
    schedule = str(activity.get("schedule", "")).strip()
    max_participants = activity.get("max_participants")

    if not name or not description or not schedule:
        raise HTTPException(status_code=400, detail="Name, description, and schedule are required")

    if not isinstance(max_participants, int) or max_participants <= 0:
        raise HTTPException(status_code=400, detail="max_participants must be a positive integer")

    if name.lower() in {existing_name.lower() for existing_name in activities}:
        raise HTTPException(status_code=400, detail="Activity already exists")

    activities[name] = {
        "description": description,
        "schedule": schedule,
        "max_participants": max_participants,
        "participants": []
    }
    return activities[name]


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Normalize email to avoid duplicate registrations with case differences
    normalized_email = email.strip().lower()
    activity = activities[activity_name]
    participants = activity["participants"]

    # Prevent duplicate registrations
    if normalized_email in [participant.lower() for participant in participants]:
        raise HTTPException(
            status_code=400,
            detail="Student already registered for this activity"
        )

    # Prevent exceeding the maximum number of participants
    if len(participants) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    participants.append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}
