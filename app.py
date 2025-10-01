# app.py (Cleaned-Up Version)
import streamlit as st
from streamlit_option_menu import option_menu
import time
import random

from theme import apply_pookie_theme
from pages import log_meal_page, chat_page, dashboard_page, login_page, my_profile_page

st.set_page_config(
    page_title="NutriLens 🌸 Your AI Nutritionist",
    page_icon="🌸",
    layout="wide"
)

apply_pookie_theme()

selected = option_menu(
    menu_title=None,
    options=["Home", "Log Meal", "AI Chat", "Dashboard", "My Profile", "Login"],
    icons=["house-heart-fill", "camera-fill", "chat-dots-fill", 'clipboard-data-fill', "person-badge-fill", "person-circle"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fce4ec"},
        "icon": {"color": "#e91e63", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#f8bbd9", "color": "#880e4f", "font-weight": "600"},
        "nav-link-selected": {"background-color": "#e91e63", "color": "white"},
    }
)

def display_page(page_name):
    if 'user' not in st.session_state:
        st.warning("You need to log in to access this page, pookie! 💖")
        login_page.show_page()
    else:
        page_modules = {
            "Log Meal": log_meal_page, "AI Chat": chat_page,
            "Dashboard": dashboard_page, "My Profile": my_profile_page
        }
        page_modules[page_name].show_page()

if selected == "Home":
    st.markdown("<h1 class='main-title'>Welcome to NutriLens! 🌸</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cute-tagline'>Your adorable AI nutritionist bestie! 💕</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<h2 class="section-title" style="text-align:center;">What Pookie Can Do For You</h2>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='food-result' style='text-align:center; height: 250px;'><h3>📸 Snap & Analyze</h3><p>Upload a photo of your meal and get instant nutritional insights. It's like magic!</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='food-result' style='text-align:center; height: 250px;'><h3>💬 Chat with AI</h3><p>Ask Pookie for snack ideas or dietary advice based on your daily logs. I'm here to help!</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='food-result' style='text-align:center; height: 250px;'><h3>📊 Track Your Day</h3><p>See your daily totals and macro breakdowns on a beautiful dashboard. Stay on track, cutie!</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    tips = [
        "Did you know? Drinking a glass of water before a meal can help with digestion and portion control! 💧",
        "Feeling snacky? A handful of almonds is a great source of protein and healthy fats to keep you full! 🐿️",
        "Try to 'eat the rainbow'! Colorful fruits and veggies are packed with different vitamins and minerals. 🌈",
        "A little walk after dinner is a wonderful way to aid digestion and get some gentle movement in. 🚶‍♀️✨",
        "Good sleep is a secret ingredient for good health! Aim for 7-8 hours to feel your best. 😴💖"
    ]
    # CLEANED: Removed inline style from the <p> tag
    st.markdown(f"<div class='daily-tip-card'><h4>💖 Pookie's Tip of the Day 💖</h4><p>{random.choice(tips)}</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    if 'user' in st.session_state:
        st.success("You're logged in and ready to go! What's on your plate today?")
        st.info("Click 'Log Meal' in the top menu to analyze your next meal! 📸")
    else:
        st.warning("You're not logged in! Create an account to start your personalized health journey.")
        st.info("Click 'Login' in the top menu to get started! 👤")

elif selected in ["Log Meal", "AI Chat", "Dashboard", "My Profile"]:
    display_page(selected)
elif selected == "Login":
    login_page.show_page()

if 'user' in st.session_state:
    st.sidebar.success(f"Logged in as {st.session_state.user.email} ✅")
    if st.sidebar.button("Log Out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("You've been logged out, cutie! See you soon! 👋")
        time.sleep(1)
        st.rerun()