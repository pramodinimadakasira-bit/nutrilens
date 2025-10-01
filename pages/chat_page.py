# pages/chat_page.py (Cleaned-Up Version)
import streamlit as st
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from gpt_advisor import GPTAdvisor
from database import init_database, get_meals_today, get_user_profile

def show_page():
    apply_pookie_theme()
    
    st.markdown("<h1 class='main-title'>Chat with Pookie! 💬</h1>", unsafe_allow_html=True)
    # CLEANED: The cute-tagline class from the theme handles the styling now
    st.markdown("<p class='cute-tagline'>Ask me for advice, like 'What's a good low-calorie snack?'</p>", unsafe_allow_html=True)

    db = init_database()
    user_id = st.session_state.user.id
    user_profile = get_user_profile(db, user_id)
    
    if user_profile is None:
        st.warning("Please set up your profile on the 'My Profile' page for the best advice! 💖")
        user_profile = {"goal": "Stay Healthy", "age": 25}

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What can I help you with, beautiful?"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pookie is thinking... 💭"):
                meal_history = get_meals_today(db, user_id)
                advisor = GPTAdvisor()
                ai_response = advisor.get_chat_suggestion(meal_history, user_profile, prompt)
                st.markdown(ai_response)
        
        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})