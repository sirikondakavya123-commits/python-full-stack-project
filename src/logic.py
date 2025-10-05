# src/logic.py
from src.db import *

# ----------------------- Users -----------------------
class TravelDairy:
    def create_user(self, email: str, name: str, password: str):
        if not email or not name or not password:
            return {"Success": False, "Message": "All fields are required."}
        res = insert_user(email, name, password)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "User created successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to create user.")}

    def authenticate_user(self, name: str, password: str):
        if not name or not password:
            return {"Success": False, "Message": "Username and password are required."}
        res = authenticate_user(name, password)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "Signed in successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Authentication failed.")}

    def get_users(self):
        res = get_all_users()
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"]}
        else:
            return {"Success": False, "Message": res.get("Message", "No users found.")}

    def update_user(self, name: str, new_email=None, new_name=None, new_password=None):
        if not name:
            return {"Success": False, "Message": "Username required for update."}
        res = update_user_by_name(name, new_email, new_name, new_password)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "User updated successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to update user.")}

    def delete_user(self, name: str):
        if not name:
            return {"Success": False, "Message": "Username required for deletion."}
        res = delete_user_by_name(name)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "User deleted successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to delete user.")}


# ----------------------- Destinations -----------------------
class Destination:
    def add_destination(self, user_name: str, destination_name: str, country_name: str, is_visited=False, notes=None):
        res = insert_destination(user_name, destination_name, country_name, is_visited, notes)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "Destination added successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to add destination.")}

    def get_all_destinations(self, user_name: str):
        res = get_destinations_by_user_name(user_name)
        if res.get("Success"):
            return {"Success": True, "Data": res.get("Data")}
        else:
            return {"Success": False, "Message": res.get("Message", "No destinations found.")}

    def update_destination(self, destination_id: int, destination_name=None, country_name=None, is_visited=None, notes=None):
        res = update_destination_by_id(destination_id, destination_name, country_name, is_visited, notes)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "Destination updated successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to update destination.")}

    def delete_destination(self, destination_id: int):
        res = delete_destination_by_id(destination_id)
        if res.get("Success"):
            return {"Success": True, "Data": res["Data"], "Message": "Destination deleted successfully!"}
        else:
            return {"Success": False, "Message": res.get("Message", "Failed to delete destination.")}
