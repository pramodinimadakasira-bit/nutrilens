# pages/login_page.py
import streamlit as st
import sys, os, time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from database import init_database

def show_page():
    apply_pookie_theme()
    db = init_database()

    st.markdown("<h1 class='main-title'>Welcome Back, Cutie! 💖</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cute-tagline'>Log in or sign up to continue your health journey! ✨</p>", unsafe_allow_html=True)

    # If the user is already logged in, show a success message instead of the forms
    if 'user' in st.session_state:
        st.success(f"You are already logged in as: {st.session_state.user.email} ✅")
        st.info("You can log out from the sidebar.")
        return # Stop the rest of the page from rendering

    login_tab, signup_tab = st.tabs(["Log In", "Sign Up"])

    # Log In Tab
    with login_tab:
        with st.form("login_form"):
            st.markdown('<h3 class="section-title">Log In to Your Account</h3>', unsafe_allow_html=True)
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log In")

            if submitted:
                try:
                    user = db.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = user.user
                    st.success("Logged in successfully! Let's get healthy! 🥳")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Oh no! Login failed: {e}")

    # Sign Up Tab
    with signup_tab:
        with st.form("signup_form"):
            st.markdown('<h3 class="section-title">Create a New Account</h3>', unsafe_allow_html=True)
            email = st.text_input("Your Email")
            password = st.text_input("Choose a Password", type="password")
            submitted = st.form_submit_button("Sign Up")

            if submitted:
                try:
                    user = db.auth.sign_up({"email": email, "password": password})
                    st.success("Yay! Your account was created successfully! Please log in now using the 'Log In' tab. 🎉")
                except Exception as e:
                    st.error(f"Oopsie! Something went wrong during sign up: {e}")