# database.py (The Final, Corrected Version)

import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import datetime

# Load the .env file
load_dotenv()

@st.cache_resource
def init_supabase():
    """Initializes and returns the Supabase client."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Supabase URL or Key not found. Please check your .env file.")
        return None
        
    try:
        _client = create_client(url, key)
        print("✅ Supabase connection initialized successfully!")
        return _client
    except Exception as e:
        st.error(f"Failed to initialize Supabase: {e}")
        return None

def save_meal(db: Client, user_id, meal_data, advice):
    """Saves a user's meal to the 'meals' table in Supabase."""
    if not db: return
    try:
        data_to_save = {
            'user_id': user_id, 'food_name': meal_data.get('food_name', 'Unknown'),
            'calories': meal_data.get('calories', 0), 'protein': meal_data.get('protein', 0),
            'carbs': meal_data.get('total_carbs', 0), 'fat': meal_data.get('total_fat', 0),
            'advice': advice
        }
        db.table('meals').insert(data_to_save).execute()
        print(f"✅ Meal saved to Supabase for user {user_id}")
    except Exception as e:
        print(f"❌ Error saving meal to Supabase: {e}")

def get_meals_today(db: Client, user_id):
    """Fetches all meals logged by a user for the current day from Supabase."""
    if not db: return []
    try:
        today = datetime.datetime.utcnow().date()
        start_of_day = datetime.datetime.combine(today, datetime.time.min).isoformat()
        end_of_day = datetime.datetime.combine(today, datetime.time.max).isoformat()
        response = db.table('meals').select("*").eq('user_id', user_id).gte('created_at', start_of_day).lte('created_at', end_of_day).order('created_at', desc=False).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching today's meals from Supabase: {e}")
        return []

def get_user_profile(db: Client, user_id):
    """Fetches a user's profile from the 'profiles' table."""
    if not db: return None
    try:
        response = db.table('profiles').select("*").eq('id', user_id).single().execute()
        return response.data
    except Exception:
        return None

def update_user_profile(db: Client, user_id, profile_data):
    """Creates or updates a user's profile."""
    if not db: return
    try:
        db.table('profiles').upsert({**profile_data, 'id': user_id}).execute()
        print(f"✅ Profile updated for user {user_id}")
    except Exception as e:
        print(f"❌ Error updating profile: {e}")

def get_meals_for_date(db: Client, user_id, date):
    """Fetches all meals logged by a user for a specific date from Supabase."""
    if not db: return []
    try:
        start_of_day = datetime.datetime.combine(date, datetime.time.min).isoformat()
        end_of_day = datetime.datetime.combine(date, datetime.time.max).isoformat()
        response = db.table('meals').select("*").eq('user_id', user_id).gte('created_at', start_of_day).lte('created_at', end_of_day).order('created_at', desc=False).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching meals for date {date}: {e}")
        return []

def get_meals_for_date_range(db: Client, user_id, start_date, end_date):
    """Fetches all meals for a user within a specific date range."""
    if not db: return []
    try:
        start_iso = datetime.datetime.combine(start_date, datetime.time.min).isoformat()
        end_iso = datetime.datetime.combine(end_date, datetime.time.max).isoformat()
        response = db.table('meals').select("*").eq('user_id', user_id).gte('created_at', start_iso).lte('created_at', end_iso).execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching meals for date range: {e}")
        return []

# A simple wrapper function to keep the naming consistent across the app
def init_database():
    return init_supabase()