# theme.py
import streamlit as st

def apply_pookie_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #ffeef8 0%, #ffe1f4 25%, #ffd7ef 50%, #ffb3d9 100%);
            font-family: 'Quicksand', sans-serif !important;
        }

        /* --- THIS IS THE NEW, GUARANTEED CENTERING STYLE --- */
        .center-btn-container {
            display: flex;
            justify-content: center;
            padding-top: 1rem;
        }

        /* Sidebar Styling */
        .css-1d391kg { background: linear-gradient(180deg, #fff0f6, #fce4ec) !important; border-right: 2px solid #f8bbd9 !important; }
        .css-1d391kg .stAlert { border-radius: 15px; border-color: #f06292; background-color: #ffc1e3; }
        .css-1d391kg .stButton>button { background: linear-gradient(45deg, #ff6b9d, #e91e63) !important; color: white !important; border-radius: 25px !important; border: none !important; font-weight: 700 !important; }
        .css-1d391kg .stButton>button:hover { background: linear-gradient(45deg, #ff8fab, #f06292) !important; transform: scale(1.05); }

        /* General Styles */
        .main-title { text-align: center; font-size: 3.5rem !important; font-weight: 700 !important; font-style: italic !important; color: #d63384 !important; text-shadow: 2px 2px 4px rgba(214, 51, 132, 0.3); margin-bottom: 0.5rem !important; font-family: 'Quicksand', sans-serif !important; }
        .cute-tagline { text-align: center; font-size: 1.3rem !important; color: #c2185b !important; font-weight: 600 !important; font-style: italic !important; margin-bottom: 2rem !important; }
        h1, h2, h3, h4 { color: #c2185b !important; font-family: 'Quicksand', sans-serif !important; font-weight: 700 !important; }
        .section-title { font-weight: 700 !important; font-style: italic !important; color: #d63384 !important; }
        .upload-section, .profile-dropdown, .food-result, .nutrition-card, .advice-card, .advice-section, .welcome-section, .encouragement-card, .daily-tip-card { border-radius: 25px; padding: 2rem; margin-bottom: 1.5rem; }
    </style>
    """, unsafe_allow_html=True)