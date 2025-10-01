# gpt_advisor.py
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class GPTAdvisor:
    def __init__(self):
        """Initialize OpenAI GPT advisor"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            print("⚠️ OpenAI API key not found! Please add OPENAI_API_KEY to your .env file")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ GPT Advisor initialized!")
    
    # --- THIS IS THE NEW FUNCTION WE ARE ADDING ---
    def get_chat_suggestion(self, meal_history, user_profile, user_query):
        """Generates a conversational response based on meal history."""
        if not self.client:
            return "Sorry, my AI brain is taking a little nap! 😴 Please check the API keys."

        history_str = ""
        total_calories = 0
        if meal_history:
            history_str = "So far today, you have logged:\n"
            for meal in meal_history:
                history_str += f"- {meal['food_name']} ({meal.get('calories', 0):.0f} kcal)\n"
                total_calories += meal.get('calories', 0)
            history_str += f"Your total for today is approximately {total_calories:.0f} calories."
        else:
            history_str = "You haven't logged any meals yet today."

        prompt = f"""
You are NutriLens, a cute, encouraging, and knowledgeable AI nutritionist. Your nickname is Pookie.
The user's profile: Their goal is '{user_profile['goal']}' and they are {user_profile['age']} years old.
Today's meal history:
{history_str}

The user just asked you: "{user_query}"

Based on their history and goal, provide a helpful, friendly, and practical response.
If they ask for a snack, suggest 2-3 specific, healthy options, explaining why they are a good choice (e.g., "it has protein to keep you full!").
Keep it conversational and use emojis naturally! 🌸 Your response should be encouraging and cute.
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=250
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ GPT Chat Error: {e}")
            return f"Oh no, pookie! I had a little hiccup trying to think! Please try again. 💕"

    # --- ALL YOUR ORIGINAL FUNCTIONS ARE STILL HERE ---
    def generate_advice(self, food_name, nutrition_data, user_profile):
        """Generate personalized nutrition advice using GPT"""
        if not self.client:
            return { 'success': False, 'error': 'OpenAI API not configured.' }
        
        try:
            prompt = self._build_prompt(food_name, nutrition_data, user_profile)
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are NutriLens, a cute, friendly, and knowledgeable AI nutritionist who specializes in Indian diets and personalized health advice. You're encouraging, warm, and give practical tips. Use emojis naturally but not excessively. Keep responses concise and actionable."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, max_tokens=500
            )
            advice_text = response.choices[0].message.content.strip()
            parsed_advice = self._parse_advice(advice_text)
            return { 'success': True, **parsed_advice, 'error': None }
        except Exception as e:
            print(f"❌ GPT Error: {str(e)}")
            return { 'success': False, 'error': f'Could not generate advice: {str(e)}' }
    
    def _build_prompt(self, food_name, nutrition_data, user_profile):
        """Build a detailed prompt for GPT"""
        goal = user_profile.get('goal', 'Stay Healthy')
        age = user_profile.get('age', 25)
        diet_type = user_profile.get('diet_type', 'Flexible')
        activity = user_profile.get('activity', 'Moderate')
        
        if nutrition_data.get('success'):
            nutrition_info = f"""
Nutrition Facts:
- Calories: {nutrition_data.get('calories', 0):.0f} kcal, Protein: {nutrition_data.get('protein', 0):.1f}g, Carbs: {nutrition_data.get('total_carbs', 0):.1f}g, Fat: {nutrition_data.get('total_fat', 0):.1f}g
"""
        else:
            nutrition_info = "Nutrition data not available for this food."
        
        return f"""
The user just ate: **{food_name}**
{nutrition_info}
User Profile:
- Goal: {goal}, Age: {age}, Diet: {diet_type}, Activity: {activity}

Please provide personalized advice in the following format:
**HEALTHY SWAP:** [Suggest ONE healthier alternative to this food.]
**DIET TIP:** [ONE practical, actionable tip related to this meal.]
**PORTION ADVICE:** [Quick guidance about portion size for this food.]
**MOTIVATION:** [A short, encouraging message.]
Keep it warm, friendly, and specific to Indian context where relevant.
"""
    
    def _parse_advice(self, advice_text):
        """Parse GPT response into structured format"""
        sections = {'healthy_swap': '', 'diet_tip': '', 'portion_advice': '', 'motivation': ''}
        try:
            lines = advice_text.split('\n')
            current_section = None
            for line in lines:
                line = line.strip()
                if 'HEALTHY SWAP' in line.upper(): current_section = 'healthy_swap'
                elif 'DIET TIP' in line.upper(): current_section = 'diet_tip'
                elif 'PORTION ADVICE' in line.upper(): current_section = 'portion_advice'
                elif 'MOTIVATION' in line.upper(): current_section = 'motivation'
                elif line and current_section:
                    sections[current_section] = sections[current_section] + ' ' + line if sections[current_section] else line
            
            for key in sections: sections[key] = sections[key].strip().replace('**', '').replace('[', '').replace(']', '')
            if not any(sections.values()): return self._get_fallback_advice(advice_text)
        except Exception:
            return self._get_fallback_advice(advice_text)
        return sections

    def _get_fallback_advice(self, text):
        return {
            'healthy_swap': text[:200] if text else "Great food choice!",
            'diet_tip': "Stay hydrated and eat mindfully! 💧",
            'portion_advice': "Moderate portions work best.",
            'motivation': "You're on the right track! 🌸"
        }
    
    def generate_daily_tip(self, user_profile):
        """Generate a daily health tip based on user profile"""
        if not self.client:
            return "Remember to stay hydrated today! 💧"
        try:
            goal = user_profile.get('goal', 'Stay Healthy')
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a friendly nutritionist. Give one short, actionable daily health tip."},
                    {"role": "user", "content": f"Give me one daily health tip for someone whose goal is: {goal}. Keep it to one sentence with an emoji."}
                ],
                temperature=0.8, max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"❌ Daily tip error: {e}")
            return "Eat colorful fruits and veggies today! 🌈"