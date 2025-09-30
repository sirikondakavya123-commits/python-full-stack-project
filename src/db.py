# src/db.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# ----------------- USERS -----------------

def insert_user(email: str, name: str):
    response = supabase.table("users").insert({
        "user_email": email,
        "user_name": name
    }).execute()
    return response

def get_user_by_id(user_id: str):
    response = supabase.table("users").select("*").eq("user_id", user_id).execute()
    return response

def get_all_users():
    response = supabase.table("users").select("*").execute()
    return response

def update_user(user_id: str, email: str = None, name: str = None):
    update_data = {}
    if email:
        update_data["user_email"] = email
    if name:
        update_data["user_name"] = name
    if not update_data:
        return None
    response = supabase.table("users").update(update_data).eq("user_id", user_id).execute()
    return response

def delete_user(user_id: str):
    response = supabase.table("users").delete().eq("user_id", user_id).execute()
    return response

# ----------------- DESTINATIONS -----------------

def insert_destination(user_name, destination_name, country_name, is_visited=False, notes=None, category_id=None):
    """Insert a new destination by using user_name instead of user_id"""
    
    # First, get user_id from user_name
    user_data = supabase.table("users").select("user_id").eq("user_name", user_name).execute()
    
    if not user_data.data or len(user_data.data) == 0:
        return {"Success": False, "Message": f"User '{user_name}' not found"}
    
    user_id = user_data.data[0]["user_id"]
    
    new_destination = {
        "user_id": user_id,
        "destination_name": destination_name,
        "country_name": country_name,
        "is_visited": is_visited,
        "notes": notes,
        "category_id": category_id
    }

    response = supabase.table("destinations").insert(new_destination).execute()
    
    if response.data:
        return {"Success": True, "Data": response.data}
    else:
        return {"Success": False, "Message": str(response.error)}


def get_all_destinations():
    response = supabase.table("destinations").select("*").execute()
    return response

def get_destination_by_id(dest_id):
    response = supabase.table("destinations").select("*").eq("id", dest_id).execute()
    return response

def get_destinations_by_user_id(user_id):
    response = supabase.table("destinations").select("*").eq("user_id", user_id).execute()
    return response

def update_destination(dest_id, destination_name=None, country_name=None, is_visited=None, notes=None, category_id=None):
    update_data = {}
    if destination_name: update_data["destination_name"] = destination_name
    if country_name: update_data["country_name"] = country_name
    if is_visited is not None: update_data["is_visited"] = is_visited
    if notes: update_data["notes"] = notes
    if category_id: update_data["category_id"] = category_id
    if not update_data: return None
    response = supabase.table("destinations").update(update_data).eq("id", dest_id).execute()
    return response

def delete_destination(dest_id):
    response = supabase.table("destinations").delete().eq("id", dest_id).execute()
    return response

# ----------------- CATEGORIES -----------------

def insert_category(category_name: str):
    response = supabase.table("categories").insert({"category_name": category_name}).execute()
    return response

def get_all_categories():
    response = supabase.table("categories").select("*").execute()
    return response

def get_category_by_id(category_id):
    response = supabase.table("categories").select("*").eq("category_id", category_id).execute()
    return response

def update_category(category_id, category_name):
    response = supabase.table("categories").update({"category_name": category_name}).eq("category_id", category_id).execute()
    return response

def delete_category(category_id):
    response = supabase.table("categories").delete().eq("category_id", category_id).execute()
    return response
