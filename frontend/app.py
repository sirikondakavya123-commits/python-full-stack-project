# frontend/app.py
import streamlit as st
import sys, os

# Add parent directory to sys.path so 'src' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import TravelDairy, Destination, Categories

# Initialize classes
user_logic = TravelDairy()
destination_logic = Destination()
category_logic = Categories()

st.set_page_config(page_title="Travel Dairy", layout="wide")
st.title("🌍 Travel Dairy")

menu = ["Home", "Users", "Destinations", "Categories"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- Users ----------------
if choice == "Users":
    st.header("Users Management")
    action = st.selectbox("Actions", ["Add User", "View Users", "Update User", "Delete User"])

    if action == "Add User":
        email = st.text_input("Email")
        name = st.text_input("Name")
        if st.button("Add User"):
            if email and name:
                result = user_logic.create_user(email, name)
                if result.get("Success"):
                    st.success("User added successfully!")
                else:
                    st.error(result.get("Message"))
            else:
                st.warning("Email and Name are required")

    elif action == "View Users":
        result = user_logic.get_users()
        if result.get("Success"):
            st.table(result.get("Data"))
        else:
            st.error(result.get("Message"))

    elif action == "Update User":
        user_id = st.text_input("User ID")
        email = st.text_input("New Email")
        name = st.text_input("New Name")
        if st.button("Update User"):
            result = user_logic.update_user(user_id, email, name)
            if result.get("Success"):
                st.success("User updated successfully!")
            else:
                st.error(result.get("Message"))

    elif action == "Delete User":
        user_id = st.text_input("User ID")
        if st.button("Delete User"):
            result = user_logic.delete_user(user_id)
            if result.get("Success"):
                st.success("User deleted successfully!")
            else:
                st.error(result.get("Message"))

# ---------------- Destinations ----------------
elif choice == "Destinations":
    st.header("Destinations Management")
    action = st.selectbox("Actions", ["Add Destination", "View Destinations", "Update Destination", "Delete Destination"])

    if action == "Add Destination":
        user_name = st.text_input("User Name")
        destination_name = st.text_input("Destination Name")
        country_name = st.text_input("Country Name")
        is_visited = st.checkbox("Visited?")
        notes = st.text_area("Notes")
        category_id = st.text_input("Category ID (optional)")
        if st.button("Add Destination"):
            result = destination_logic.add_destination(user_name, destination_name, country_name, is_visited, notes, category_id or None)
            if result.get("Success"):
                st.success("Destination added successfully!")
            else:
                st.error(result.get("Message"))

    elif action == "View Destinations":
        result = destination_logic.get_all_destinations()
        if result.get("Success"):
            st.table(result.get("Data"))
        else:
            st.error(result.get("Message"))

    elif action == "Update Destination":
        dest_id = st.text_input("Destination ID")
        destination_name = st.text_input("New Destination Name")
        country_name = st.text_input("New Country Name")
        is_visited = st.checkbox("Visited?", value=False)
        notes = st.text_area("New Notes")
        category_id = st.text_input("New Category ID")
        if st.button("Update Destination"):
            result = destination_logic.update_destination(dest_id, destination_name, country_name, is_visited, notes, category_id or None)
            if result.get("Success"):
                st.success("Destination updated successfully!")
            else:
                st.error(result.get("Message"))

    elif action == "Delete Destination":
        dest_id = st.text_input("Destination ID")
        if st.button("Delete Destination"):
            result = destination_logic.delete_destination(dest_id)
            if result.get("Success"):
                st.success("Destination deleted successfully!")
            else:
                st.error(result.get("Message"))

# ---------------- Categories ----------------
elif choice == "Categories":
    st.header("Categories Management")
    action = st.selectbox("Actions", ["Add Category", "View Categories", "Update Category", "Delete Category"])

    if action == "Add Category":
        category_name = st.text_input("Category Name")
        if st.button("Add Category"):
            result = category_logic.add_category(category_name)
            if result.get("Success"):
                st.success("Category added successfully!")
            else:
                st.error(result.get("Message"))

    elif action == "View Categories":
        result = category_logic.get_all_categories()
        if result.get("Success"):
            st.table(result.get("Data"))
        else:
            st.error(result.get("Message"))

    elif action == "Update Category":
        category_id = st.text_input("Category ID")
        category_name = st.text_input("New Category Name")
        if st.button("Update Category"):
            result = category_logic.update_category(category_id, category_name)
            if result.get("Success"):
                st.success("Category updated successfully!")
            else:
                st.error(result.get("Message"))

    elif action == "Delete Category":
        category_id = st.text_input("Category ID")
        if st.button("Delete Category"):
            result = category_logic.delete_category(category_id)
            if result.get("Success"):
                st.success("Category deleted successfully!")
            else:
                st.error(result.get("Message"))
