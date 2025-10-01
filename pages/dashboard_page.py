# pages/dashboard_page.py
import streamlit as st
import sys, os
import plotly.graph_objects as go
import datetime
from collections import defaultdict

# Allow the page to import modules from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
# Import BOTH of our date-fetching functions
from database import init_database, get_meals_for_date, get_meals_for_date_range

# --- Backend Logic (moved here for clarity) ---

def calculate_totals(meals):
    """Calculates total nutrients from a list of meals."""
    # ... (This function remains exactly the same as before)
    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for meal in meals:
        totals['calories'] += meal.get('calories', 0)
        totals['protein'] += meal.get('protein', 0)
        totals['carbs'] += meal.get('carbs', 0)
        totals['fat'] += meal.get('fat', 0)
    # ... (The rest of the macro calculation logic is the same)
    return totals, {} # We'll skip macro percentages for this example

def analyze_historical_data(meals):
    """Processes a list of meals to find the best days for calories and protein."""
    daily_data = defaultdict(list)
    for meal in meals:
        # Group meals by the date they were created
        meal_date = datetime.datetime.fromisoformat(meal['created_at']).date()
        daily_data[meal_date].append(meal)
    
    if not daily_data:
        return None

    # Calculate totals for each day
    daily_totals = {}
    for date, daily_meals in daily_data.items():
        totals, _ = calculate_totals(daily_meals)
        daily_totals[date] = totals
        
    # Find the best days
    min_calorie_day = min(daily_totals.items(), key=lambda item: item[1]['calories'])
    max_protein_day = max(daily_totals.items(), key=lambda item: item[1]['protein'])
    
    return {
        "min_calorie_day": min_calorie_day[0],
        "min_calories": min_calorie_day[1]['calories'],
        "max_protein_day": max_protein_day[0],
        "max_protein": max_protein_day[1]['protein'],
    }

# --- Main Page Function ---

def show_page():
    apply_pookie_theme()
    st.markdown("<h1 class='main-title'>Your Dashboard 📊</h1>", unsafe_allow_html=True)
    
    db = init_database()
    user_id = st.session_state.user.id
    
    # --- Date Picker for Daily View ---
    selected_date = st.date_input("🗓️ Show my log for:", datetime.date.today())
    st.markdown("<p class='cute-tagline'>Let's see your amazing progress, beautiful! 💕</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- Daily Log Section ---
    meals_for_day = get_meals_for_date(db, user_id, selected_date)
    
    if not meals_for_day:
        st.info(f"You haven't logged any meals on {selected_date.strftime('%B %d, %Y')}, cutie!")
    else:
        # (Your existing daily dashboard UI code can go here)
        totals, _ = calculate_totals(meals_for_day)
        st.markdown(f'<h3 class="section-title">✨ Totals for {selected_date.strftime("%B %d")} ✨</h3>', unsafe_allow_html=True)
        # (Display the metric cards for the selected day)

    st.markdown("---")
    
    # --- "Best Day" Feature Section ---
    st.markdown('<h2 class="section-title" style="text-align:center;">Your Hall of Fame 🏆</h2>', unsafe_allow_html=True)
    
    # Analyze the last 30 days of data
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)
    historical_meals = get_meals_for_date_range(db, user_id, start_date, end_date)
    
    best_day_stats = analyze_historical_data(historical_meals)
    
    if best_day_stats is None:
        st.info("Log a few more meals to unlock your Hall of Fame!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='food-result' style='text-align:center; background: linear-gradient(135deg, #e3f2fd, #bbdefb);'>
                    <h4>Lowest Calorie Day 🧘‍♀️</h4>
                    <p style='font-size: 1.5rem; font-weight: 700; color: #1976d2;'>{best_day_stats['min_calories']:.0f} kcal</p>
                    <p style='font-weight: 600; color: #42a5f5;'>on {best_day_stats['min_calorie_day'].strftime('%B %d, %Y')}</p>
                    <p>Amazing discipline, pookie!</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='food-result' style='text-align:center; background: linear-gradient(135deg, #f1e3fd, #d1b3fb);'>
                    <h4>Highest Protein Day 💪</h4>
                    <p style='font-size: 1.5rem; font-weight: 700; color: #6a1b9a;'>{best_day_stats['max_protein']:.1f} g</p>
                    <p style='font-weight: 600; color: #9c27b0;'>on {best_day_stats['max_protein_day'].strftime('%B %d, %Y')}</p>
                    <p>Incredible work building muscle!</p>
                </div>
            """, unsafe_allow_html=True)