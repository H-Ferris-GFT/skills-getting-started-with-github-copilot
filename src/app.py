"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
import uvicorn
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
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "category": "intellectual"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "category": "intellectual"
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
        "category": "sports"
    },
    "Soccer Team": {
        "description": "Practice teamwork and improve your ball control in weekly matches",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu"],
        "category": "sports"
    },
    "Basketball Club": {
        "description": "Develop shooting, defense, and game strategy skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu"],
        "category": "sports"
    },
    "Drama Club": {
        "description": "Explore acting, improvisation, and stage performance",
        "schedule": "Tuesdays, 3:45 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["zoe@mergington.edu"],
        "category": "artistic"
    },
    "Art Workshop": {
        "description": "Create drawings, paintings, and mixed media projects",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["mia@mergington.edu"],
        "category": "artistic"
    },
    "Math Olympiad": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["noah@mergington.edu"],
        "category": "intellectual"
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts in depth",
        "schedule": "Wednesdays, 3:30 PM - 4:45 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu"],
        "category": "intellectual"
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    activity = activities[activity_name]

    if normalized_email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already registered for this activity")

    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    normalized_email = email.strip().lower()
    if not normalized_email:
        raise HTTPException(status_code=400, detail="Email is required")

    activity = activities[activity_name]
    if normalized_email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student is not registered for this activity")

    activity["participants"] = [participant for participant in activity["participants"] if participant != normalized_email]
    return {"message": f"Unregistered {normalized_email} from {activity_name}"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
