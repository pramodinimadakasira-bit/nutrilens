# pages/log_meal_page.py
import streamlit as st
from PIL import Image
import sys, os, time

# Allow imports from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from food_detection import FoodDetector
from nutrition_api import NutritionAPI
from gpt_advisor import GPTAdvisor
from database import init_database, save_meal

# --- Cached Model Loading ---
@st.cache_resource
def load_food_detector(): return FoodDetector()
@st.cache_resource
def load_nutrition_api(): return NutritionAPI()
@st.cache_resource
def load_gpt_advisor(): return GPTAdvisor()

def reset_analysis_state():
    """Resets session state for a new analysis."""
    keys_to_reset = ['analysis_triggered', 'detection_result', 'final_food_name', 'analysis_complete', 'image_to_analyze']
    for key in keys_to_reset:
        if key in st.session_state:
            del st.session_state[key]

# --- Main Page Function ---
def show_page():
    apply_pookie_theme()
    
    st.markdown("<h1 class='main-title'>Log Your Meal 📸</h1>", unsafe_allow_html=True)
    
    # --- Profile Section ---
    with st.container():
        st.markdown('<div class="profile-dropdown">', unsafe_allow_html=True)
        st.markdown('<h3 class="section-title">👑 Your Quick Profile</h3>', unsafe_allow_html=True)
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        with col_p1: goal = st.selectbox("💖 Goal", ["Lose Weight", "Gain Weight", "Stay Healthy", "Build Muscle"], key="log_goal")
        with col_p2: age = st.number_input("🎂 Age", 13, 100, 25, key="log_age")
        with col_p3: diet_type = st.selectbox("🌱 Diet", ["Vegetarian", "Non-Vegetarian", "Vegan", "Keto", "Flexible"], key="log_diet")
        with col_p4:
            activity_options = {
                "Couch Queen (Low) 🛋️": "Low", "Gentle Stroller (Light) 🚶‍♀️": "Light",
                "Busy Bee (Active) 🏃‍♀️": "Active", "Fitness Fanatic (High) 💪": "High",
                "Pro Athlete (Super Active) 🏆": "Super Active"
            }
            selected_activity = st.selectbox("💃 Activity", list(activity_options.keys()), key="log_activity")
            activity = activity_options[selected_activity]
        st.markdown('</div>', unsafe_allow_html=True)
        
    user_profile = {'goal': goal, 'age': age, 'diet_type': diet_type, 'activity': activity}

    # --- Image Upload Section ---
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop your food pic here, cutie! 💕", type=['png', 'jpg', 'jpeg'], on_change=reset_analysis_state)
    
    if uploaded_file:
        st.image(uploaded_file, caption="Your Beautiful Food! 🌟", use_container_width=True)
        
        # --- THE FINAL, UNBREAKABLE, GUARANTEED CENTERING METHOD ---
        # We create a container and apply our new CSS class to it.
        with st.container():
            st.markdown("<div class='center-btn-container'>", unsafe_allow_html=True)
            # The button is placed inside this centered div.
            if st.button("🔍 Analyze My Food! 💖", key="analyze_btn"):
                st.session_state.analysis_triggered = True
                st.session_state.image_to_analyze = uploaded_file
            st.markdown("</div>", unsafe_allow_html=True)
        # --- END OF BUTTON FIX ---

        if st.session_state.get('analysis_triggered', False):
            analyze_food(st.session_state.image_to_analyze, user_profile)
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- Analysis Function (Complete and Unabridged) ---
def analyze_food(image, user_profile):
    detector, nutrition_api, advisor = load_food_detector(), load_nutrition_api(), load_gpt_advisor()
    db = init_database()

    if 'detection_result' not in st.session_state or st.session_state.detection_result is None:
        with st.spinner("🌸 Working some magic... ✨"):
            pil_image = Image.open(image)
            st.session_state.detection_result = detector.detect_food(pil_image)
    
    result = st.session_state.detection_result
        
    if not result['success']:
        st.markdown(f'<div class="error-message"><h4>🌸 Oopsie! Something went wrong! 💕</h4><p>Error: {result["error"]}</p></div>', unsafe_allow_html=True)
        return

    food_options = [result['food_name']] + [alt['name'] for alt in result['alternatives']]
    food_options.append("Other (please specify)")
    
    st.markdown('<div class="food-result">', unsafe_allow_html=True)
    st.markdown('<h3 class="section-title">🤔 Is this correct, honey?</h3>', unsafe_allow_html=True)
    
    selection = st.radio(
        "Please pick the correct food:",
        options=food_options, horizontal=True, key="food_confirm_radio"
    )

    if selection == "Other (please specify)":
        manual_food = st.text_input("Please tell me what it is, cutie! 💖", key="manual_food_input")
        if manual_food:
            st.session_state.final_food_name = manual_food
        else:
            st.info("☝️ Type the food name above and press Enter to continue!")
            return
    else:
        st.session_state.final_food_name = selection
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    final_food_name = st.session_state.get('final_food_name')

    if final_food_name and not st.session_state.get('analysis_complete', False):
        with st.spinner(f"✨ Analyzing {final_food_name} for you..."):
            nutrition_data = nutrition_api.get_nutrition(final_food_name)
            advice = advisor.generate_advice(final_food_name, nutrition_data, user_profile)
            
            st.session_state.nutrition_data = nutrition_data
            st.session_state.advice = advice
            st.session_state.analysis_complete = True
            st.rerun()

    if st.session_state.get('analysis_complete', False):
        nutrition_data = st.session_state.nutrition_data
        advice = st.session_state.advice
        
        if nutrition_data['success']:
            st.markdown('<div class="nutrition-card"><h3 class="section-title">📊 Nutrition Magic!</h3></div>', unsafe_allow_html=True)
            cols = st.columns(4)
            macros = {'🔥': ('Calories', f"{nutrition_data['calories']:.0f}"), '💪': ('Protein', f"{nutrition_data['protein']:.1f}g"), '🌾': ('Carbs', f"{nutrition_data['total_carbs']:.1f}g"), '🥑': ('Fat', f"{nutrition_data['total_fat']:.1f}g")}
            for i, (emoji, (label, value)) in enumerate(macros.items()):
                with cols[i]:
                    st.markdown(f'<div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #fff0f6, #fce4ec); border-radius: 15px; border: 2px solid #f8bbd9;"><div style="font-size: 2rem;">{emoji}</div><div style="color: #e91e63; font-weight: 700; font-style: italic; font-size: 1.5rem;">{value}</div><div style="color: #c2185b; font-weight: 600; font-style: italic;">{label}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="nutrition-card"><h3 class="section-title">📊 Nutrition Info:</h3><p style="color: #c2185b;">😔 Couldn\'t find nutrition data. Try a more common name! 💕</p></div>', unsafe_allow_html=True)

        if advice['success']:
            st.markdown('<div class="advice-card"><h3 class="section-title">💬 Your Personal AI Advice:</h3></div>', unsafe_allow_html=True)
            advice_sections = {'🔄 Healthy Swap:': advice['healthy_swap'], '💡 Diet Tip:': advice['diet_tip'], '🍽️ Portion Advice:': advice['portion_advice'], '💪 Motivation:': advice['motivation']}
            for title, text in advice_sections.items():
                st.markdown(f'<div class="advice-section"><h4 style="color: #e91e63;">{title}</h4><p style="color: #c2185b;">{text}</p></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="advice-card"><h3 class="section-title">💬 Your Personal Advice:</h3><p style="color: #c2185b;">🚧 {advice["error"]}</p></div>', unsafe_allow_html=True)

        st.balloons()
        st.markdown('<div class="encouragement-card"><h4 style="color: #e91e63;">🌟 You\'re doing great, queen! 🌟</h4></div>', unsafe_allow_html=True)
        
        user_id = st.session_state.user.id
        save_meal(db, user_id, st.session_state.nutrition_data, st.session_state.advice)