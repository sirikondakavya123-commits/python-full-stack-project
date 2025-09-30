# src/logic.py
from src.db import (
    insert_user, get_all_users, get_user_by_id, update_user, delete_user,
    insert_destination, get_all_destinations, get_destination_by_id, update_destination, delete_destination,
    insert_category, get_all_categories, update_category, delete_category
)

class TravelDairy:
    """User operations"""
    
    def create_user(self, email, name):
        response = insert_user(email, name)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def get_users(self):
        response = get_all_users()
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def get_user_by_id(self, user_id):
        response = get_user_by_id(user_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def update_user(self, user_id, email=None, name=None):
        response = update_user(user_id, email, name)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def delete_user(self, user_id):
        response = delete_user(user_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}


class Destination:
    """Destination operations"""
    
    def add_destination(self, user_name, destination_name, country_name, is_visited=False, notes=None, category_id=None):
        response = insert_destination(user_name, destination_name, country_name, is_visited, notes, category_id)
        return response

    def get_all_destinations(self):
        response = get_all_destinations()
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def get_destination_by_id(self, dest_id):
        response = get_destination_by_id(dest_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def update_destination(self, dest_id, destination_name=None, country_name=None, is_visited=None, notes=None, category_id=None):
        response = update_destination(dest_id, destination_name, country_name, is_visited, notes, category_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def delete_destination(self, dest_id):
        response = delete_destination(dest_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}


class Categories:
    """Category operations"""

    def add_category(self, name):
        response = insert_category(name)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def get_all_categories(self):
        response = get_all_categories()
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def update_category(self, category_id, name):
        response = update_category(category_id, name)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}

    def delete_category(self, category_id):
        response = delete_category(category_id)
        if not response.data:
            return {"Success": False, "Message": getattr(response, 'error', 'Unknown error')}
        return {"Success": True, "Data": response.data}
