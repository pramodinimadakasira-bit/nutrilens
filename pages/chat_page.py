# pages/chat_page.py
import streamlit as st
import sys, os

# Allow the page to import modules from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from gpt_advisor import GPTAdvisor
from database import init_database, get_meals_today, get_user_profile

# This is now the main function for this page
def show_page():
    apply_pookie_theme()
    
    st.markdown("<h1 class='main-title'>Chat with Pookie! 💬</h1>", unsafe_allow_html=True)
    st.markdown("<p class='cute-tagline'>Ask me for advice, like 'What's a good low-calorie snack?' 💕</p>", unsafe_allow_html=True)

    # Initialization
    db = init_database()
    
    # Get the real user ID from the session state (set during login)
    user_id = st.session_state.user.id
    
    # --- THIS IS THE UPGRADE ---
    # Fetch the REAL user profile from the database
    user_profile = get_user_profile(db, user_id)
    
    # If the user is new and hasn't created a profile, guide them!
    if user_profile is None:
        st.warning("Please set up your profile on the 'My Profile' page for the best advice! 💖")
        # Create a default profile so the app doesn't crash
        user_profile = {"goal": "Stay Healthy", "age": 25}
    # --- END UPGRADE ---

    # Initialize chat history for this specific page if it doesn't exist
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display past chat messages from the history
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input from the chat box at the bottom
    if prompt := st.chat_input("What can I help you with, beautiful?"):
        # Add user's message to history and display it
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare and display the AI's response
        with st.chat_message("assistant"):
            with st.spinner("Pookie is thinking... 💭"):
                # 1. Fetch the latest meal history from the database
                meal_history = get_meals_today(db, user_id)
                
                # 2. Initialize the AI advisor
                advisor = GPTAdvisor()
                
                # 3. Get the AI's suggestion, now using the REAL user profile
                ai_response = advisor.get_chat_suggestion(meal_history, user_profile, prompt)
                
                # 4. Display the AI's response
                st.markdown(ai_response)
        
        # Add the AI's response to the chat history
        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})