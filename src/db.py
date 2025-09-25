#db_manager.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv


#load environmental variables
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
supabase:Client=create_client(url,key)

#create task
def insert_users(email,name):
    data=supabase.table("users").insert({"email":email,"name":name}).execute()
    return data

#get users by specified id
def get_users_by_id(id):
    data=supabase.table("users").select("*").eq("id",id).execute()
    return data
#get all users
def get_users():
    data=supabase.table("users").select("*").execute()
    return data

#update users
def update_users(id,email,name):
    data=supabase.table("users").update({"email":email,"name":name}).eq("id",id).execute()
    return data

#delete users
def delete_users(id):
    data=supabase.table("users").delete().eq("id",id).execute()
    return data

#-------------
#destination table operations
#-------------

# insert destination details into destination table.

def insert_destination(
    user_id: str,
    destination_name: str,
    country_name: str,
    is_visited: bool = False,
    notes: str = None,
    category_id: int = None
):
    """Insert a new destination into the destinations table"""
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
        print(" Destination inserted:", response.data)
        return response.data
    else:
        print(" Error inserting destination:", response.error)
        return None
# get all destinations from the destinations table.
def get_all_destinations():
    """Retrive all destinations fron the destinations table"""
    response=supabase.table("destinations").select("*").execute()
    return response.data
# get destination by user_id
def get_destinations_by_user_id(user_id):
    response=supabase.table("destinations").select("*").eq("user_id",user_id).execute()
    return response.data
#get destination by id
def get_destination_by_id(destination_id):
    response=supabase.table("destinations").select("*").eq("id",destination_id).execute()
    return response.data
#update destination by id
def update_destination(
    destination_id: int,
    destination_name: str = None,
    country_name: str = None,
    is_visited: bool = None,
    notes: str = None,
    category_id: int = None
):
    """Update destination details by ID"""
    update_data = {}
    if destination_name is not None:
        update_data["destination_name"] = destination_name
    if country_name is not None:
        update_data["country_name"] = country_name
    if is_visited is not None:
        update_data["is_visited"] = is_visited
    if notes is not None:
        update_data["notes"] = notes
    if category_id is not None:
        update_data["category_id"] = category_id

    if not update_data:
        return print(" No fields to update")

    response = supabase.table("destinations").update(update_data).eq("id", destination_id).execute()

    if response.data:
        print(" Destination updated:", response.data)
        return response.data
    else:
        print(" Error:", response.error)
        return None

#delete destination by id
def delete_destination(destination_id):
    response=supabase.table("destinations").delete().eq("id",destination_id).execute()
    return response.data
#----------------
#categories table operations
#----------------

#insert category
def insert_category(category_name: str):
    """Insert a new category into the categories table"""
    response = supabase.table("categories").insert({"category_name": category_name}).execute()
    if response.data:
        print("✅ Category inserted:", response.data)
        return response.data
    else:
        print("❌ Error inserting category:", response.error)
        return None

# Example usage:
# insert_category("Beach")
#get all categories
def get_all_categories():
    response=supabase.table("categories").select("*").execute()
    return response.data
#get category by id
def get_category_by_id(category_id: int):
    """Fetch a category from the categories table by ID"""
    response = supabase.table("categories").select("*").eq("category_id", category_id).execute()
    return response.data

# Example usage:
# category = get_category_by_id(1)
# print(category)

#update category by id
def update_category(category_id: int, category_name: str):
    """Update category name by ID"""
    response = supabase.table("categories").update({"category_name": category_name}).eq("category_id", category_id).execute()
    return response.data
# Example usage:
# update_category(1, "Mountain")

#delete category by id
def delete_category(category_id: int):
    """Delete a category from the categories table by ID"""
    response = supabase.table("categories").delete().eq("category_id", category_id).execute()
    return response.data

# Example usage:
# delete_category(1)

