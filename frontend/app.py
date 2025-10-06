# frontend/app.py
import streamlit as st
import sys
import os
import pandas as pd

# Add parent directory to sys.path so 'src' can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.logic import TravelDairy, Destination

# ----------------------------
# Initialize classes
# ----------------------------
user_logic = TravelDairy()
destination_logic = Destination()

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Travel Diary", 
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .destination-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 1rem 0;
        background-color: #f9f9f9;
    }
    .stats-card {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">✈️ Travel Diary</h1>', unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "page" not in st.session_state:
    st.session_state.page = "Login"
if "show_add_detailed" not in st.session_state:
    st.session_state.show_add_detailed = True
if "destinations" not in st.session_state:
    st.session_state.destinations = []
if "filter_visited" not in st.session_state:
    st.session_state.filter_visited = "All"

# ----------------------------
# Helper Functions
# ----------------------------
def rerun():
    """Safe rerun function"""
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.rerun()

def refresh_destinations():
    """Refresh destinations from backend"""
    try:
        result = destination_logic.get_all_destinations(st.session_state.user_name)
        if result.get("Success"):
            st.session_state.destinations = result.get("Data", [])
        else:
            st.error("Failed to refresh destinations")
    except Exception as e:
        st.error(f"Error refreshing destinations: {str(e)}")

def normalize_country_name(country_name):
    """Normalize country names for consistent counting"""
    if not country_name:
        return ""
    
    # Convert to lowercase and strip whitespace
    normalized = country_name.strip().lower()
    
    # Common normalization rules
    country_aliases = {
        'usa': 'united states',
        'u.s.a.': 'united states',
        'us': 'united states',
        'u.s.': 'united states',
        'uk': 'united kingdom',
        'u.k.': 'united kingdom',
        'england': 'united kingdom',
        'scotland': 'united kingdom',
        'wales': 'united kingdom',
    }
    
    return country_aliases.get(normalized, normalized)

def get_travel_stats():
    """Calculate travel statistics with proper country counting"""
    destinations = st.session_state.destinations
    if not destinations:
        return {"total": 0, "visited": 0, "countries": 0, "percentage": 0}
    
    total = len(destinations)
    visited = len([d for d in destinations if d.get('is_visited', False)])
    
    # Count unique countries with normalization
    unique_countries = set()
    for dest in destinations:
        country = dest.get('country_name', '').strip()
        if country:  # Only add non-empty country names
            normalized_country = normalize_country_name(country)
            unique_countries.add(normalized_country)
    
    countries_count = len(unique_countries)
    
    return {
        "total": total,
        "visited": visited,
        "countries": countries_count,
        "percentage": (visited / total * 100) if total > 0 else 0,
        "unique_countries": list(unique_countries)
    }

# ----------------------------
# LOGIN / SIGNUP
# ----------------------------
if not st.session_state.user_name:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🌍 Welcome to Travel Diary")
        mode = st.radio("Select Option", ["Sign In", "Sign Up"], horizontal=True)

        if mode == "Sign Up":
            with st.form("signup_form"):
                email = st.text_input("📧 Email", key="signup_email")
                name = st.text_input("👤 Username", key="signup_name")
                password = st.text_input("🔒 Password", type="password", key="signup_pass")
                confirm_password = st.text_input("🔒 Confirm Password", type="password", key="signup_confirm_pass")
                
                submitted = st.form_submit_button("Create Account")
                if submitted:
                    if not email or not name or not password:
                        st.error("Please fill in all fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    else:
                        with st.spinner("Creating account..."):
                            res = user_logic.create_user(email, name, password)
                            if res.get("Success"):
                                st.success("🎉 Account created successfully! Please Sign In.")
                            else:
                                st.error(f"❌ {res.get('Message')}")

        elif mode == "Sign In":
            with st.form("signin_form"):
                name = st.text_input("👤 Username", key="signin_name")
                password = st.text_input("🔒 Password", type="password", key="signin_pass")
                
                submitted = st.form_submit_button("Sign In")
                if submitted:
                    if not name or not password:
                        st.error("Please enter both username and password")
                    else:
                        with st.spinner("Signing in..."):
                            res = user_logic.authenticate_user(name, password)
                            if res.get("Success"):
                                st.session_state.user_name = name
                                st.session_state.page = "🏠 Dashboard"
                                refresh_destinations()
                                st.success(f"✅ Welcome back, {name}!")
                                rerun()
                            else:
                                st.error(f"❌ {res.get('Message')}")

# ----------------------------
# MAIN APP AFTER LOGIN
# ----------------------------
if st.session_state.user_name:
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### 👋 Hello, {st.session_state.user_name}!")
        st.write("---")
        
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "🌍 Destinations", "📊 Statistics", "👤 Profile"],
            index=["🏠 Dashboard", "🌍 Destinations", "📊 Statistics", "👤 Profile"].index(
                st.session_state.page if st.session_state.page in ["🏠 Dashboard", "🌍 Destinations", "📊 Statistics", "👤 Profile"] 
                else "🏠 Dashboard"
            )
        )
        st.session_state.page = page
        
        # Quick Stats in Sidebar
        stats = get_travel_stats()
        st.write("---")
        st.markdown("### 📈 Quick Stats")
        st.markdown(f"**Total Destinations:** {stats['total']}")
        st.markdown(f"**Visited:** {stats['visited']}")
        st.markdown(f"**Unique Countries:** {stats['countries']}")
        
        st.write("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user_name = ""
            st.session_state.page = "Login"
            st.session_state.destinations = []
            st.success("Logged out successfully!")
            rerun()

    # ----------------------------
    # DASHBOARD PAGE
    # ----------------------------
    if page == "🏠 Dashboard":
        st.subheader("🏠 Travel Dashboard")
        
        # Statistics Cards
        stats = get_travel_stats()
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="stats-card"><h3>🗺️</h3><h2>{stats["total"]}</h2><p>Total Destinations</p></div>', 
                       unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stats-card"><h3>✅</h3><h2>{stats["visited"]}</h2><p>Visited</p></div>', 
                       unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stats-card"><h3>🌎</h3><h2>{stats["countries"]}</h2><p>Unique Countries</p></div>', 
                       unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stats-card"><h3>📊</h3><h2>{stats["percentage"]:.1f}%</h2><p>Completed</p></div>', 
                       unsafe_allow_html=True)
        
        # Quick Actions
        st.write("---")
        st.subheader("🚀 Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Add New Destination", use_container_width=True):
                st.session_state.page = "🌍 Destinations"
                st.session_state.show_add_detailed = True
                rerun()
        
        with col2:
            if st.button("📊 View Statistics", use_container_width=True):
                st.session_state.page = "📊 Statistics"
                rerun()
        
        with col3:
            if st.button("✏️ Manage Destinations", use_container_width=True):
                st.session_state.page = "🌍 Destinations"
                rerun()
        
        # Recent Destinations Preview
        st.write("---")
        st.subheader("📍 Recent Destinations")
        if st.session_state.destinations:
            recent_destinations = st.session_state.destinations[-5:]  # Show last 5
            for dest in reversed(recent_destinations):
                status = "✅ Visited" if dest.get('is_visited', False) else "🟡 Planned"
                st.markdown(f"""
                <div class="destination-card">
                    <h4>🌍 {dest['destination_name']} ({dest['country_name']})</h4>
                    <p><strong>Status:</strong> {status}</p>
                    <p><strong>Notes:</strong> {dest.get('notes', 'No notes')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No destinations added yet. Start by adding your first destination!")

    # ----------------------------
    # DESTINATIONS PAGE
    # ----------------------------
    elif page == "🌍 Destinations":
        st.subheader("🌍 Manage Destinations")
        
        # Add Destination Section
        with st.expander("➕ Add New Destination", expanded=st.session_state.show_add_detailed):
            with st.form(key="add_dest_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    dest_name = st.text_input("📍 Destination Name *", key="form_dest_name")
                    country = st.text_input("🇺🇳 Country *", key="form_country_name")
                with col2:
                    visited = st.checkbox("✅ Visited", key="form_visited")
                    notes = st.text_area("📝 Notes", key="form_notes", height=100)
                
                submitted = st.form_submit_button("Add Destination")
                if submitted:
                    if not dest_name or not country:
                        st.error("Please fill in destination name and country")
                    else:
                        with st.spinner("Adding destination..."):
                            res = destination_logic.add_destination(
                                st.session_state.user_name, dest_name, country, visited, notes
                            )
                            if res.get("Success"):
                                st.success("✅ Destination added successfully!")
                                refresh_destinations()
                                st.session_state.show_add_detailed = False
                                rerun()
                            else:
                                st.error(f"❌ {res.get('Message')}")

        # Filter and Search Section
        st.write("---")
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search destinations...", placeholder="Search by name or country")
        
        with col2:
            filter_visited = st.selectbox(
                "Filter by status",
                ["All", "Visited", "Not Visited"],
                key="filter_visited"
            )
        
        with col3:
            st.write("")  # Spacer
            if st.button("🔄 Refresh", use_container_width=True):
                refresh_destinations()
                st.success("Destinations refreshed!")

        # Display Destinations
        st.write("### 📋 Your Destinations")
        
        filtered_destinations = st.session_state.destinations
        
        # Apply filters
        if search_term:
            filtered_destinations = [
                d for d in filtered_destinations 
                if search_term.lower() in d['destination_name'].lower() 
                or search_term.lower() in d['country_name'].lower()
            ]
        
        if filter_visited == "Visited":
            filtered_destinations = [d for d in filtered_destinations if d.get('is_visited', False)]
        elif filter_visited == "Not Visited":
            filtered_destinations = [d for d in filtered_destinations if not d.get('is_visited', False)]

        if not filtered_destinations:
            st.info("No destinations found matching your criteria.")
        
        for idx, dest in enumerate(filtered_destinations):
            dest_id = dest["destination_id"]
            status = "✅ Visited" if dest.get('is_visited', False) else "🟡 Planned"
            
            with st.expander(f"🌍 {dest['destination_name']} ({dest['country_name']}) - {status}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Country:** {dest['country_name']}")
                    st.write(f"**Status:** {status}")
                    st.write(f"**Notes:** {dest.get('notes', 'No notes')}")
                
                with col2:
                    if dest.get('is_visited', False):
                        st.success("✅ Visited")
                    else:
                        st.warning("🟡 Planned")
                
                # Update/Delete Form
                with st.form(key=f"upd_form_{dest_id}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Destination Name", value=dest['destination_name'], key=f"name_{dest_id}")
                        new_country = st.text_input("Country", value=dest['country_name'], key=f"country_{dest_id}")
                    with col2:
                        new_visited = st.checkbox("Visited", value=dest['is_visited'], key=f"visited_{dest_id}")
                        new_notes = st.text_area("Notes", value=dest.get('notes', ''), key=f"notes_{dest_id}", height=100)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        update_submitted = st.form_submit_button("💾 Update", use_container_width=True)
                    with col2:
                        delete_submitted = st.form_submit_button("🗑️ Delete", use_container_width=True)

                    if update_submitted:
                        with st.spinner("Updating destination..."):
                            upd_res = destination_logic.update_destination(
                                dest_id, new_name, new_country, new_visited, new_notes
                            )
                            if upd_res.get("Success"):
                                st.success("✅ Destination updated successfully!")
                                refresh_destinations()
                                rerun()
                            else:
                                st.error(f"❌ {upd_res.get('Message')}")

                    if delete_submitted:
                        # Double confirmation for delete
                        st.warning(f"Are you sure you want to delete {dest['destination_name']}?")
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Yes, Delete", key=f"confirm_del_{dest_id}"):
                                with st.spinner("Deleting destination..."):
                                    del_res = destination_logic.delete_destination(dest_id)
                                    if del_res.get("Success"):
                                        st.success("✅ Destination deleted successfully!")
                                        refresh_destinations()
                                        rerun()
                                    else:
                                        st.error(f"❌ {del_res.get('Message')}")
                        with col2:
                            if st.button("❌ Cancel", key=f"cancel_del_{dest_id}"):
                                rerun()

    # ----------------------------
    # STATISTICS PAGE
    # ----------------------------
    elif page == "📊 Statistics":
        st.subheader("📊 Travel Statistics")
        
        stats = get_travel_stats()
        
        if stats["total"] == 0:
            st.info("No travel data available yet. Start adding destinations to see statistics!")
        else:
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Destinations", stats["total"])
            with col2:
                st.metric("Visited Destinations", stats["visited"])
            with col3:
                st.metric("Unique Countries", stats["countries"])
            with col4:
                st.metric("Completion Rate", f"{stats['percentage']:.1f}%")
            
            # Visualization
            col1, col2 = st.columns(2)
            
            with col1:
                # Visited vs Not Visited Chart
                visited_count = stats["visited"]
                not_visited_count = stats["total"] - stats["visited"]
                
                chart_data = pd.DataFrame({
                    'Status': ['Visited', 'Not Visited'],
                    'Count': [visited_count, not_visited_count]
                })
                st.bar_chart(chart_data.set_index('Status'))
                st.caption("Visited vs Not Visited Destinations")
            
            with col2:
                # Countries breakdown
                countries = {}
                for dest in st.session_state.destinations:
                    country = dest['country_name']
                    countries[country] = countries.get(country, 0) + 1
                
                if countries:
                    country_data = pd.DataFrame({
                        'Country': list(countries.keys()),
                        'Destinations': list(countries.values())
                    })
                    # Show top 10 countries only to avoid clutter
                    top_countries = country_data.nlargest(10, 'Destinations')
                    st.bar_chart(top_countries.set_index('Country'))
                    st.caption("Top Countries by Destinations")
            
            # Country List
            st.write("---")
            st.subheader("🌍 Countries Visited")
            if stats["unique_countries"]:
                countries_per_row = 4
                unique_countries = sorted(stats["unique_countries"])
                
                # Display countries in a grid
                rows = [unique_countries[i:i + countries_per_row] for i in range(0, len(unique_countries), countries_per_row)]
                
                for row in rows:
                    cols = st.columns(countries_per_row)
                    for idx, country in enumerate(row):
                        with cols[idx]:
                            # Count destinations per country
                            country_dest_count = len([d for d in st.session_state.destinations 
                                                    if normalize_country_name(d['country_name']) == country])
                            st.metric(
                                label=country.title(),
                                value=country_dest_count
                            )
            else:
                st.info("No countries added yet.")
            
            # Detailed Statistics
            st.write("---")
            st.subheader("📋 Detailed Breakdown")
            
            # Create a DataFrame for better display
            df_data = []
            for dest in st.session_state.destinations:
                df_data.append({
                    'Destination': dest['destination_name'],
                    'Country': dest['country_name'],
                    'Status': 'Visited' if dest.get('is_visited', False) else 'Planned',
                    'Notes': dest.get('notes', '')[:50] + '...' if len(dest.get('notes', '')) > 50 else dest.get('notes', '')
                })
            
            if df_data:
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

    # ----------------------------
    # PROFILE PAGE
    # ----------------------------
    elif page == "👤 Profile":
        st.subheader(f"👤 Profile: {st.session_state.user_name}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔒 Change Password")
            with st.form("password_form"):
                current_password = st.text_input("Current Password", type="password", key="current_pass")
                new_password = st.text_input("New Password", type="password", key="new_pass")
                confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pass")
                
                submitted = st.form_submit_button("Update Password")
                if submitted:
                    if not current_password or not new_password or not confirm_password:
                        st.error("Please fill in all password fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    elif len(new_password) < 6:
                        st.error("New password must be at least 6 characters long")
                    else:
                        # First verify current password
                        auth_res = user_logic.authenticate_user(st.session_state.user_name, current_password)
                        if auth_res.get("Success"):
                            with st.spinner("Updating password..."):
                                res = user_logic.update_user(st.session_state.user_name, new_password=new_password)
                                if res.get("Success"):
                                    st.success("✅ Password updated successfully!")
                                else:
                                    st.error(f"❌ {res.get('Message')}")
                        else:
                            st.error("❌ Current password is incorrect")
        
        with col2:
            st.markdown("### 📊 Account Summary")
            stats = get_travel_stats()
            st.info(f"""
            **Username:** {st.session_state.user_name}
            **Total Destinations:** {stats['total']}
            **Unique Countries:** {stats['countries']}
            **Completion Rate:** {stats['percentage']:.1f}%
            **Account Status:** Active
            """)
            
            st.markdown("### 🏆 Travel Achievements")
            if stats["countries"] >= 10:
                st.success("🎖️ World Traveler: Visited 10+ countries!")
            elif stats["countries"] >= 5:
                st.info("✈️ Frequent Flyer: Visited 5+ countries!")
            elif stats["countries"] >= 1:
                st.info("🌍 Explorer: Started your travel journey!")
            else:
                st.info("🛄 Ready to explore! Add your first destination.")
            
            st.markdown("### ⚠️ Account Actions")
            if st.button("🗑️ Delete Account", type="secondary"):
                st.error("This action cannot be undone! Please contact support for account deletion.")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "✈️ Travel Diary App • Made with Streamlit"
    "</div>",
    unsafe_allow_html=True
)