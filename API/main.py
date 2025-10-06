import sys, os
from fastapi import FastAPI
from pydantic import BaseModel

# --- Add project root to path so imports work ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your db_manager
from src import db as db

app = FastAPI(title="Travel Diary API")

# -----------------------
# Models
# -----------------------

class SignUpModel(BaseModel):
    email: str
    name: str
    password: str

class SignInModel(BaseModel):
    name: str
    password: str

class DestinationModel(BaseModel):
    user_name: str
    destination_name: str
    country_name: str
    is_visited: bool = False
    notes: str = None

# -----------------------
# Auth Endpoints
# -----------------------

@app.post("/signup")
def signup(user: SignUpModel):
    res = db.insert_user(user.email, user.name, user.password)
    return res

@app.post("/signin")
def signin(credentials: SignInModel):
    res = db.authenticate_user(credentials.name, credentials.password)
    return res

# -----------------------
# Destination Endpoints
# -----------------------

@app.post("/destinations/add")
def add_destination(destination: DestinationModel):
    res = db.insert_destination(
        destination.user_name,
        destination.destination_name,
        destination.country_name,
        destination.is_visited,
        destination.notes
    )
    return res

@app.get("/destinations/{user_name}")
def get_destinations_by_user(user_name: str):
    res = db.get_destinations_by_user_name(user_name)
    return res

@app.put("/destinations/{dest_id}")
def update_destination(dest_id: int, destination: DestinationModel):
    res = db.update_destination_by_id(
        dest_id,
        destination_name=destination.destination_name,
        country_name=destination.country_name,
        is_visited=destination.is_visited,
        notes=destination.notes
    )
    return res

@app.delete("/destinations/{dest_id}")
def delete_destination(dest_id: int):
    res = db.delete_destination_by_id(dest_id)
    return res

# -----------------------
# Root endpoint
# -----------------------

@app.get("/")
def home():
    return {"message": "Welcome to Travel Diary API"}