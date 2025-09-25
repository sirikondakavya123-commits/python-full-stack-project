# src/logic.py 
from src.db import DatabaseManager
import re  # Needed for regex checks if any (optional)

class TravelDairy:
    """Acts as bridge between frontend(Steamlit/FastAPI) and database(supabase)"""
    def __init__(self):
        # create a database manager instance (this will handle actual db operations)
        self.db = DatabaseManager()
    
    #-----create----------
    def create_user(self, email, name):
        """Create a new user in the database's users table
        Return the success message if the user is created successfully"""
        if not email and not name:
            return {"Success": False, "Message": "Email and Name are required"}
        result = self.db.insert_users(email, name)
        if result.get("Success"):
            return {"Success": True, "Message": "User created successfully"}
        else:
            return {"Success": False, "Message": "Failed to create user"}
    
    #----get users by id------
    def get_user_by_id(self, id):
        """Fetch a user from the database's users table by id"""
        result = self.db.get_users_by_id(id)
        if result.get("Success"):
            return {"Success": True, "Message": "User fetched successfully", "Data": result.get("Data")}
        else:
            return {"Success": False, "Message": "Failed to fetch users"}
    
    #----get all users------
    def get_users(self):
        """Fetch all users from the database's users table"""
        result = self.db.get_users()
        if result.get("Success"):
            return {"Success": True, "Message": "Users fetched successfully", "Data": result.get("Data")}
        else:
            return {"Success": False, "Message": "Failed to fetch users"}
    
    #---update------
    def update_user(self, email, name, id):
        """Update user details in the database's users table"""
        result = self.db.update_user(email, name, id)
        if result.get("Success"):
            return {"Success": True, "Message": "User details updated successfully"}
        else:
            return {"Success": False, "Message": "Failed to update user details"}
    
    #----delete------
    def delete_user(self, id):
        """Delete a user from the database's users table"""
        result = self.db.delete_user(id)
        if result.get("Success"):
            return {"Success": True, "Message": "User details deleted successfully"}
        else:
            return {"Success": False, "Message": "Failed to delete user details"}


class Destination:
    def __init__(self):
        self.db = DatabaseManager()
    
    #-----destination table operations------
    def add_destination(self, user_id, destination_name, country_name, is_visited=False, notes=None, category_id=None):
        """Add a new destination to the database's destinations table"""
        result = self.db.add_destination(user_id, destination_name, country_name, is_visited, notes, category_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Destination added successfully"}
        else:
            return {"Success": False, "Message": "Failed to add destination"}
    
    #-----get all destinations------
    def get_all_destinations(self):
        """Fetch all destinations from the database's destinations table"""
        result = self.db.get_all_destinations()
        if result.get("Success"):
            return {"Success": True, "Message": "Destinations fetched successfully", "Data": result.get("Data")}
        else:
            return {"Success": False, "Message": "Failed to fetch destinations"}
    
    #-----get destinations by user id------
    def get_destinations_by_user_id(self, user_id):
        """Fetch all destinations for a specific user from the database's destinations table"""
        result = self.db.get_destinations_by_user_id(user_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Destinations fetched successfully", "Data": result.get("Data")}
        else:
            return {"Success": False, "Message": "Failed to fetch destinations"}
    
    #-----update destination------
    def update_destination(self, id, user_id=None, destination_name=None, country_name=None, is_visited=None, notes=None, category_id=None):
        """Update destination details in the database's destinations table"""
        result = self.db.update_destination(id, user_id, destination_name, country_name, is_visited, notes, category_id)
        if result.get("Success"):
            return {"Success": True, "Message": "Destination details updated successfully"}
        else:
            return {"Success": False, "Message": "Failed to update destination details"}
    
    #-----delete destination------
    def delete_destination(self, id):
        """Delete a destination from the database's destinations table"""
        result = self.db.delete_destination(id)
        if result.get("Success"):
            return {"Success": True, "Message": "Destination deleted successfully"}
        else:
            return {"Success": False, "Message": "Failed to delete destination"}


class Categories:
    def __init__(self):
        self.db = DatabaseManager()
    
    #-----category table operations------
    def add_category(self, category_name):
        """Add a new category to the database's categories table"""
        result = self.db.add_category(category_name)
        if result.get("Success"):
            return {"Success": True, "Message": "Category added successfully"}
        else:
            return {"Success": False, "Message": "Failed to add category"}
    
    #-----get all categories------
    def get_all_categories(self):
        """Fetch all categories from the database's categories table"""
        result = self.db.get_all_categories()
        if result.get("Success"):
            return {"Success": True, "Message": "Categories fetched successfully", "Data": result.get("Data")}
        else:
            return {"Success": False, "Message": "Failed to fetch categories"}
    
    #-----update category------
    def update_category(self, id, category_name):
        """Update category details in the database's categories table"""
        result = self.db.update_category(id, category_name)
        if result.get("Success"):
            return {"Success": True, "Message": "Category details updated successfully"}
        else:
            return {"Success": False, "Message": "Failed to update category details"}
    
    #-----delete category------
    def delete_category(self, id):
        """Delete a category from the database's categories table"""
        result = self.db.delete_category(id)
        if result.get("Success"):
            return {"Success": True, "Message": "Category deleted successfully"}
        else:
            return {"Success": False, "Message": "Failed to delete category"}
