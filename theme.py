# theme.py (Version with High-Contrast Text)
import streamlit as st

def apply_pookie_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
        
        /* --- THIS IS THE MAIN FIX --- */
        /* Set a default dark color for all text */
        .stApp, .stApp p, .stMarkdown, .stAlert, .stExpander {
            color: #333333 !important; /* A very dark gray, almost black */
        }
        
        .stApp {
            background: linear-gradient(135deg, #ffeef8 0%, #ffe1f4 25%, #ffd7ef 50%, #ffb3d9 100%);
            font-family: 'Quicksand', sans-serif !important;
        }

        /* Keep the main title vibrant pink */
        .main-title {
            color: #d63384 !important;
            text-align: center; font-size: 3.5rem !important; font-weight: 700 !important; font-style: italic !important;
            text-shadow: 2px 2px 4px rgba(214, 51, 132, 0.3); margin-bottom: 0.5rem !important;
        }
        
        /* Make headings a darker, more readable pink */
        h2, h3, h4, .section-title, .cute-tagline {
            color: #880e4f !important; /* A very dark, rich pink */
            font-family: 'Quicksand', sans-serif !important;
            font-weight: 700 !important;
        }

        /* Sidebar Styling (already good, no changes needed) */
        .css-1d391kg { background: linear-gradient(180deg, #fff0f6, #fce4ec) !important; border-right: 2px solid #f8bbd9 !important; }
        .css-1d391kg .stAlert { border-radius: 15px; border-color: #f06292; background-color: #ffc1e3; }
        .css-1d391kg .stButton>button { background: linear-gradient(45deg, #ff6b9d, #e91e63) !important; color: white !important; border-radius: 25px !important; border: none !important; font-weight: 700 !important; }
        .css-1d391kg .stButton>button:hover { background: linear-gradient(45deg, #ff8fab, #f06292) !important; transform: scale(1.05); }

        /* The button centering class */
        .center-btn-container { display: flex; justify-content: center; padding-top: 1rem; }
        
        /* General Component Styles */
        .upload-section, .profile-dropdown, .food-result, .nutrition-card, .advice-card, .advice-section, .welcome-section, .encouragement-card, .daily-tip-card { border-radius: 25px; padding: 2rem; margin-bottom: 1.5rem; }

        /* Fix for metric cards to use the new dark text color */
        .nutrition-card div[data-testid="stMetric"], .nutrition-card div[data-testid="stMetric"] div {
             color: #333333 !important;
        }
        .daily-tip-card p {
            color: #333333 !important;
        }

    </style>
    """, unsafe_allow_html=True)