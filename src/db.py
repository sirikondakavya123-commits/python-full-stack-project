# src/db_manager.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# ---------------- USERS ----------------

def insert_user(email: str, name: str, password: str):
    resp = supabase.table("users").insert({
        "user_email": email,
        "user_name": name,
        "password": password
    }).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to create user"}

def authenticate_user(name: str, password: str):
    resp = supabase.table("users").select("*").eq("user_name", name).execute()
    if resp.data:
        user = resp.data[0]
        if user["password"] == password:
            return {"Success": True, "Data": user}
        return {"Success": False, "Message": "Incorrect password"}
    return {"Success": False, "Message": "User not found"}

def get_all_users():
    resp = supabase.table("users").select("*").execute()
    if resp.data:
        return {"Success": True, "Data": resp.data}
    return {"Success": False, "Message": "No users found"}

def update_user_by_name(name: str, new_email=None, new_name=None, new_password=None):
    updates = {}
    if new_email: updates["user_email"] = new_email
    if new_name: updates["user_name"] = new_name
    if new_password: updates["password"] = new_password
    if not updates: return {"Success": False, "Message": "Nothing to update."}

    resp = supabase.table("users").update(updates).eq("user_name", name).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to update user"}

def delete_user_by_name(name: str):
    resp = supabase.table("users").delete().eq("user_name", name).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to delete user"}

# ---------------- DESTINATIONS ----------------

def insert_destination(user_name: str, destination_name: str, country_name: str, is_visited=False, notes=None):
    user_resp = supabase.table("users").select("*").eq("user_name", user_name).execute()
    if not user_resp.data:
        return {"Success": False, "Message": "User not found"}
    user_id = user_resp.data[0]["user_id"]

    resp = supabase.table("destinations").insert({
        "user_id": user_id,
        "destination_name": destination_name,
        "country_name": country_name,
        "is_visited": is_visited,
        "notes": notes
    }).execute()

    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to add destination"}

def get_destinations_by_user_name(user_name: str):
    user_resp = supabase.table("users").select("*").eq("user_name", user_name).execute()
    if not user_resp.data:
        return {"Success": False, "Message": "User not found"}
    user_id = user_resp.data[0]["user_id"]

    resp = supabase.table("destinations").select("*").eq("user_id", user_id).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data}
    return {"Success": False, "Message": "No destinations found"}

def update_destination_by_id(destination_id: int, destination_name=None, country_name=None, is_visited=None, notes=None):
    updates = {}
    if destination_name: updates["destination_name"] = destination_name
    if country_name: updates["country_name"] = country_name
    if is_visited is not None: updates["is_visited"] = is_visited
    if notes: updates["notes"] = notes
    if not updates: return {"Success": False, "Message": "Nothing to update."}

    resp = supabase.table("destinations").update(updates).eq("destination_id", destination_id).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to update destination"}

def delete_destination_by_id(destination_id: int):
    resp = supabase.table("destinations").delete().eq("destination_id", destination_id).execute()
    if resp.data:
        return {"Success": True, "Data": resp.data[0]}
    return {"Success": False, "Message": "Failed to delete destination"}
