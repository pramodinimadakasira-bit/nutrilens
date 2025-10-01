# pages/my_profile_page.py
import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from database import init_database, get_user_profile, update_user_profile

def show_page():
    apply_pookie_theme()
    st.markdown("<h1 class='main-title'>My Profile 👑</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cute-tagline'>This is all about you, beautiful!</p>", unsafe_allow_html=True)

    db = init_database()
    user_id = st.session_state.user.id
    
    # Fetch existing profile data
    existing_profile = get_user_profile(db, user_id)
    if existing_profile is None:
        existing_profile = {} # Set to empty dict if no profile exists yet

    with st.form("profile_form"):
        st.markdown('<h3 class="section-title">Your Health Goals & Stats</h3>', unsafe_allow_html=True)
        
        goal = st.selectbox("💖 My Goal", ["Lose Weight", "Gain Weight", "Stay Healthy", "Build Muscle"], index=["Lose Weight", "Gain Weight", "Stay Healthy", "Build Muscle"].index(existing_profile.get("goal", "Lose Weight")))
        age = st.number_input("🎂 My Age", 13, 100, existing_profile.get("age", 25))
        height_cm = st.number_input("📏 My Height (cm)", 100, 250, existing_profile.get("height_cm", 160))
        weight_kg = st.number_input("⚖️ My Weight (kg)", 30, 200, existing_profile.get("weight_kg", 60))
        
        activity_options = {
            "Couch Queen (Low) 🛋️": "Low", "Gentle Stroller (Light) 🚶‍♀️": "Light",
            "Busy Bee (Active) 🏃‍♀️": "Active", "Fitness Fanatic (High) 💪": "High",
            "Pro Athlete (Super Active) 🏆": "Super Active"
        }
        activity_keys = list(activity_options.keys())
        # Find the index of the saved activity level to pre-select it
        current_activity_key = next((key for key, value in activity_options.items() if value == existing_profile.get("activity")), activity_keys[0])
        selected_activity_key = st.selectbox("💃 My Activity Level", activity_keys, index=activity_keys.index(current_activity_key))
        activity = activity_options[selected_activity_key]

        submitted = st.form_submit_button("Save My Profile ✨")
        
        if submitted:
            profile_data = {
                "goal": goal, "age": age, "height_cm": height_cm,
                "weight_kg": weight_kg, "activity": activity
            }
            update_user_profile(db, user_id, profile_data)
            st.success("Your profile has been saved, pookie! 🎉")
            st.balloons()