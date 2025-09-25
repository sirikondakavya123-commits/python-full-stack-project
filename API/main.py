#frontend---->API---->logic.py---->db---->Response
#API/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys,os

# Importing TravelDairy and Destination ,categories classes from src 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import TravelDairy, Destination, Categories

#-----------------------------App Setup-----------------------------
app=FastAPI(title="TravelDairy API", version="1.0")

#-----------------------------Allow frontend(Streamlit/React) on the call of API------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#creating instances of TravelDairy, Destination and Categories classes
travel_dairy = TravelDairy()
destination = Destination()
categories = Categories()

#-----------------------------Data Models-----------------------------

class User(BaseModel):
    "Schema for creating a new user"
    email:str
    name:str
class UserUpdate(BaseModel):
    "Schema for updating user details"
    email:str
    name:str
    id:int  
class UserID(BaseModel):
    "Schema for fetching/deleting user by id"
    id:int  

class DestinationModel(BaseModel):
    "Schema for creating a new destination"
    name:str
    description:str
    location:str
    category_id:int
    user_id:int

class DestinationUpdate(BaseModel):
    "Schema for updating destination details"
    name:str
    description:str
    location:str
    category_id:int
    user_id:int
    id:int

class DestinationID(BaseModel):
    "Schema for fetching/deleting destination by id"
    id:int 

class Category(BaseModel):
    "Schema for creating a new category"
    name:str

class CategoryUpdate(BaseModel):
    "Schema for updating category details"
    name:str
    id:int

class CategoryID(BaseModel):
    "Schema for fetching/deleting category by id"
    id:int

#-----------------------------API Endpoints-----------------------------

#-----------------------------User-----------------------------
@app.get("/")
def home():
    """check if the API is running"""
    return {"message": "Welcome to the TravelDairy API!"}

@app.get("/users")
def get_all_users():
    """Fetch all users"""
    return travel_dairy.get_users()

@app.post("/user")
def create_user(user: User):
    """Create a new user"""
    result= travel_dairy.create_user(user.email, user.name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.get("/user/{id}")
def get_user_by_id(id: int):
    """Fetch a user by id"""
    result= travel_dairy.get_user_by_id(id)
    if not result.get("Success"):
        raise HTTPException(status_code=404, detail=result.get("Message"))
    else:
        return result

@app.put("/user")
def update_user(user: UserUpdate):
    """Update user details"""
    result= travel_dairy.update_user(user.email, user.name, user.id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.delete("/user/{id}")
def delete_user(id: int):
    """Delete a user by id"""
    result= travel_dairy.delete_user(id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

#-----------------------------Destination Endpoints-----------------------------  
    
@app.get("/destinations")
def get_all_destinations():
    """Fetch all destinations"""
    return destination.get_all_destinations()

@app.post("/destination")
def create_destination(dest: DestinationModel):
    """Create a new destination"""
    result= destination.add_destination(dest.user_id, dest.name, dest.location, False, dest.description, dest.category_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.get("/destination/{id}")
def get_destination_by_id(id: int): 
    """Fetch a destination by id"""
    result= destination.get_destination_by_id(id)   # NOTE: must exist in logic.py
    if not result.get("Success"):
        raise HTTPException(status_code=404, detail=result.get("Message"))
    else:
        return result

@app.put("/destination")
def update_destination(dest: DestinationUpdate):
    """Update destination details"""
    result= destination.update_destination(dest.id, dest.user_id, dest.name, dest.location, False, dest.description, dest.category_id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.delete("/destination/{id}")
def delete_destination(id: int):
    """Delete a destination by id"""
    result= destination.delete_destination(id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

#-----------------------------Categories Endpoints-----------------------------

@app.get("/categories")
def get_all_categories():
    """Fetch all categories"""
    return categories.get_all_categories()

@app.post("/category")
def create_category(cat: Category):
    """Create a new category"""
    result= categories.add_category(cat.name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.put("/category")
def update_category(cat: CategoryUpdate):
    """Update category details"""
    result= categories.update_category(cat.id, cat.name)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

@app.delete("/category/{id}")
def delete_category(id: int):
    """Delete a category by id"""
    result= categories.delete_category(id)
    if not result.get("Success"):
        raise HTTPException(status_code=400, detail=result.get("Message"))
    else:
        return result

#-----------------------------Run--------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)

