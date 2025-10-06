# frontend/app.py
import streamlit as st
import sys, os

# Add parent directory to sys.path so 'src' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import TravelDairy, Destination

# Initialize classes
user_logic = TravelDairy()
destination_logic = Destination()

st.set_page_config(page_title="Travel Diary", page_icon="✈️")
st.title("✈️ Travel Diary")

# ----------------------------
# SESSION STATE
# ----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "show_add_detailed" not in st.session_state:
    st.session_state.show_add_detailed = True

# ----------------------------
# LOGIN / SIGNUP
# ----------------------------
if not st.session_state.user_name:
    st.subheader("Login / Register")
    mode = st.radio("Select Option", ["Sign In", "Sign Up"], horizontal=True)

    if mode == "Sign Up":
        email = st.text_input("Email")
        name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            res = user_logic.create_user(email, name, password)
            if res.get("Success"):
                st.success("Account created successfully! Please Sign In.")
            else:
                st.error(res.get("Message"))

    elif mode == "Sign In":
        name = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            res = user_logic.authenticate_user(name, password)
            if res.get("Success"):
                st.session_state.user_name = name
                st.session_state.page = "Destinations"
                st.success("Signed in successfully!")
                st.experimental_rerun()  # rerun to load Destinations page
            else:
                st.error(res.get("Message"))

# ----------------------------
# NAVIGATION AFTER LOGIN
# ----------------------------
if st.session_state.user_name:
    page = st.sidebar.radio(
        "Navigate",
        ["Destinations", "Profile"],
        index=["Destinations", "Profile"].index(st.session_state.page)
    )
    st.session_state.page = page

    # ---------------- DESTINATIONS PAGE ----------------
    if page == "Destinations":
        st.subheader(f"🌍 {st.session_state.user_name}'s Destinations")

        # Add Destination
        with st.expander("➕ Add New Destination"):
            if st.session_state.show_add_detailed:
                dest_name = st.text_input("Destination Name", key="dest_name")
                country = st.text_input("Country", key="country_name")
                notes = st.text_area("Notes", key="notes")
                visited = st.checkbox("Visited", key="visited")
                
                if st.button("Add Destination", key="add_dest_btn"):
                    if visited:
                        st.balloons()
                        
                    res = destination_logic.add_destination(
                        st.session_state.user_name, dest_name, country, visited, notes
                    )
                    if res.get("Success"):
                        st.success("Destination added successfully!")
                        
                        # Hide the form
                        st.session_state.show_add_detailed = False
                        st.experimental_rerun()
                    else:
                        st.error(res.get("Message"))
            else:
                # Show "Add Another Destination" button
                if st.button("Add Another Destination"):
                    st.session_state.show_add_detailed = True
                    st.experimental_rerun()

        # View Destinations
        st.write("---")
        st.write("📋 Your Destinations:")
        res = destination_logic.get_all_destinations(st.session_state.user_name)
        if res.get("Success"):
            for idx, dest in enumerate(res.get("Data", [])):
                dest_id = dest["destination_id"]  # Supabase primary key
                with st.expander(f"{dest['destination_name']} ({dest['country_name']})"):
                    st.write(f"**Visited:** {dest['is_visited']}")
                    st.write(f"**Notes:** {dest.get('notes', 'No notes')}")

                    # Update Destination
                    new_name = st.text_input(
                        "New Destination Name",
                        value=dest['destination_name'],
                        key=f"upd_name_{dest_id}_{idx}"
                    )
                    new_country = st.text_input(
                        "New Country",
                        value=dest['country_name'],
                        key=f"upd_country_{dest_id}_{idx}"
                    )
                    new_notes = st.text_area(
                        "New Notes",
                        value=dest.get('notes', ''),
                        key=f"upd_notes_{dest_id}_{idx}"
                    )
                    new_visited = st.checkbox(
                        "Visited",
                        value=dest['is_visited'],
                        key=f"upd_visited_{dest_id}_{idx}"
                    )

                    if st.button("Update", key=f"upd_btn_{dest_id}_{idx}"):
                        upd_res = destination_logic.update_destination(
                            dest_id, new_name, new_country, new_visited, new_notes
                        )
                        if upd_res.get("Success"):
                            st.success("Destination updated successfully!")
                            st.experimental_rerun()
                        else:
                            st.error(upd_res.get("Message"))

                    # Delete Destination
                    if st.button("🗑 Delete", key=f"del_btn_{dest_id}_{idx}"):
                        del_res = destination_logic.delete_destination(dest_id)
                        if del_res.get("Success"):
                            st.warning("Destination deleted successfully!")
                            st.experimental_rerun()
                        else:
                            st.error(del_res.get("Message"))
        if st.button("🚪 Logout"):
            st.session_state.user_name = ""
            st.session_state.page = "Login"
            st.experimental_rerun()
            st.success("Logged out successfully!")

    # ---------------- PROFILE PAGE ----------------
    elif page == "Profile":
        st.subheader(f"👤 Profile: {st.session_state.user_name}")

        new_password = st.text_input("Change Password", type="password", key="profile_pass")
        if st.button("Update Password"):
            if new_password:
                res = user_logic.update_user(st.session_state.user_name, new_password=new_password)
                if res.get("Success"):
                    st.success("Password updated successfully!")
                else:
                    st.error(res.get("Message"))
            else:
                st.error("Please enter a new password.")
  
    # ---------------- LOGOUT ----------------
    