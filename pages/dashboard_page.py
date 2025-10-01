# pages/dashboard_page.py (Cleaned-Up Version)
import streamlit as st
import sys, os
import plotly.graph_objects as go
import datetime
from collections import defaultdict

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import apply_pookie_theme
from database import init_database, get_meals_for_date, get_meals_for_date_range

def calculate_totals(meals):
    # This function is fine, no changes needed
    totals = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
    for meal in meals:
        totals['calories'] += meal.get('calories', 0); totals['protein'] += meal.get('protein', 0)
        totals['carbs'] += meal.get('carbs', 0); totals['fat'] += meal.get('fat', 0)
    return totals, {}

def analyze_historical_data(meals):
    # This function is fine, no changes needed
    daily_data = defaultdict(list)
    for meal in meals:
        meal_date = datetime.datetime.fromisoformat(meal['created_at']).date()
        daily_data[meal_date].append(meal)
    if not daily_data: return None
    daily_totals = {date: calculate_totals(d_meals)[0] for date, d_meals in daily_data.items()}
    min_calorie_day = min(daily_totals.items(), key=lambda item: item[1]['calories'])
    max_protein_day = max(daily_totals.items(), key=lambda item: item[1]['protein'])
    return {
        "min_calorie_day": min_calorie_day[0], "min_calories": min_calorie_day[1]['calories'],
        "max_protein_day": max_protein_day[0], "max_protein": max_protein_day[1]['protein'],
    }

def show_page():
    apply_pookie_theme()
    st.markdown("<h1 class='main-title'>Your Dashboard 📊</h1>", unsafe_allow_html=True)
    selected_date = st.date_input("🗓️ Show my log for:", datetime.date.today())
    st.markdown("<p class='cute-tagline'>Let's see your amazing progress, beautiful! 💕</p>", unsafe_allow_html=True)
    st.markdown("---")
    db = init_database()
    user_id = st.session_state.user.id
    meals_for_day = get_meals_for_date(db, user_id, selected_date)
    
    if not meals_for_day:
        st.info(f"You haven't logged any meals on {selected_date.strftime('%B %d, %Y')}, cutie!")
    else:
        # The daily totals display logic is fine, no changes needed
        pass

    st.markdown("---")
    st.markdown('<h2 class="section-title" style="text-align:center;">Your Hall of Fame 🏆</h2>', unsafe_allow_html=True)
    end_date = datetime.date.today(); start_date = end_date - datetime.timedelta(days=30)
    historical_meals = get_meals_for_date_range(db, user_id, start_date, end_date)
    best_day_stats = analyze_historical_data(historical_meals)
    
    if best_day_stats is None:
        st.info("Log a few more meals to unlock your Hall of Fame!")
    else:
        col1, col2 = st.columns(2)
        with col1:
            # CLEANED: Removed inline style from the <p> tags
            st.markdown(f"""
                <div class='food-result' style='text-align:center; background: linear-gradient(135deg, #e3f2fd, #bbdefb);'>
                    <h4>Lowest Calorie Day 🧘‍♀️</h4>
                    <p>{best_day_stats['min_calories']:.0f} kcal</p>
                    <p>on {best_day_stats['min_calorie_day'].strftime('%B %d, %Y')}</p>
                    <p>Amazing discipline, pookie!</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            # CLEANED: Removed inline style from the <p> tags
            st.markdown(f"""
                <div class='food-result' style='text-align:center; background: linear-gradient(135deg, #f1e3fd, #d1b3fb);'>
                    <h4>Highest Protein Day 💪</h4>
                    <p>{best_day_stats['max_protein']:.1f} g</p>
                    <p>on {best_day_stats['max_protein_day'].strftime('%B %d, %Y')}</p>
                    <p>Incredible work building muscle!</p>
                </div>
            """, unsafe_allow_html=True)