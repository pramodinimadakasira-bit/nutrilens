import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class NutritionAPI:
    def __init__(self):
        """Initialize with Nutritionix API credentials"""
        self.app_id = os.getenv('NUTRITIONIX_APP_ID')
        self.app_key = os.getenv('NUTRITIONIX_APP_KEY')
        self.base_url = "https://trackapi.nutritionix.com/v2"
        
        # Headers for API requests
        self.headers = {
            'x-app-id': self.app_id,
            'x-app-key': self.app_key,
            'Content-Type': 'application/json'
        }
        
        # Check if API keys are loaded
        if not self.app_id or not self.app_key:
            print("⚠️ Nutritionix API keys not found! Please check your .env file")
    
    def get_nutrition(self, food_name, serving_size="1 serving"):
        """
        Get nutrition information for a food item
        
        Args:
            food_name (str): Name of the food
            serving_size (str): Serving size (e.g., "1 cup", "100g")
            
        Returns:
            dict: Nutrition information or error
        """
        try:
            # Clean food name for better API results
            cleaned_food = self.clean_food_name(food_name)
            
            # API endpoint for natural language nutrition
            url = f"{self.base_url}/natural/nutrients"
            
            # Request payload
            payload = {
                "query": f"{serving_size} {cleaned_food}",
                "timezone": "US/Eastern"
            }
            
            # Make API request with proper encoding
            response = requests.post(
                url, 
                headers=self.headers, 
                json=payload,
                timeout=10
            )
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('foods') and len(data['foods']) > 0:
                    food_data = data['foods'][0]
                    
                    # Extract nutrition information
                    nutrition_info = {
                        'success': True,
                        'food_name': food_data.get('food_name', cleaned_food),
                        'brand_name': food_data.get('brand_name'),
                        'serving_qty': food_data.get('serving_qty', 1),
                        'serving_unit': food_data.get('serving_unit', 'serving'),
                        'serving_weight_grams': food_data.get('serving_weight_grams'),
                        'calories': food_data.get('nf_calories', 0),
                        'total_fat': food_data.get('nf_total_fat', 0),
                        'saturated_fat': food_data.get('nf_saturated_fat', 0),
                        'cholesterol': food_data.get('nf_cholesterol', 0),
                        'sodium': food_data.get('nf_sodium', 0),
                        'total_carbs': food_data.get('nf_total_carbohydrate', 0),
                        'dietary_fiber': food_data.get('nf_dietary_fiber', 0),
                        'sugars': food_data.get('nf_sugars', 0),
                        'protein': food_data.get('nf_protein', 0),
                        'potassium': food_data.get('nf_potassium', 0),
                        'photo_url': food_data.get('photo', {}).get('thumb') if food_data.get('photo') else None,
                        'error': None
                    }
                    
                    return nutrition_info
                else:
                    return {
                        'success': False,
                        'error': 'No nutrition data found for this food item'
                    }
            else:
                return {
                    'success': False,
                    'error': f'API request failed with status code: {response.status_code}'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def clean_food_name(self, food_name):
        """
        Clean food name for better API results
        
        Args:
            food_name (str): Raw food name from image detection
            
        Returns:
            str: Cleaned food name
        """
        # Remove underscores and special characters
        cleaned = food_name.replace('_', ' ').replace('-', ' ')
        
        # Remove numbers and extra spaces
        cleaned = ' '.join(word for word in cleaned.split() if not word.isdigit())
        
        # Handle common AI detection quirks
        food_mappings = {
            'paneer butter masala': 'paneer makhani',
            'dal makhani': 'dal makhani',
            'chicken tikka masala': 'chicken tikka masala',
            'biryani': 'chicken biryani',  # Default to chicken
            'dosa': 'plain dosa',
            'idli': 'idli sambar',
            'roti': 'chapati',
            'naan': 'garlic naan',
        }
        
        # Check if we have a better mapping
        cleaned_lower = cleaned.lower().strip()
        for key, value in food_mappings.items():
            if key in cleaned_lower:
                return value
        
        return cleaned.strip()
    
    def format_nutrition_display(self, nutrition_data):
        """
        Format nutrition data for pretty display
        
        Args:
            nutrition_data (dict): Nutrition information
            
        Returns:
            dict: Formatted display data
        """
        if not nutrition_data['success']:
            return nutrition_data
        
        return {
            'macros': {
                'Calories': f"{nutrition_data['calories']:.0f} kcal",
                'Protein': f"{nutrition_data['protein']:.1f}g",
                'Carbs': f"{nutrition_data['total_carbs']:.1f}g",
                'Fat': f"{nutrition_data['total_fat']:.1f}g"
            },
            'details': {
                'Fiber': f"{nutrition_data['dietary_fiber']:.1f}g",
                'Sugar': f"{nutrition_data['sugars']:.1f}g",
                'Sodium': f"{nutrition_data['sodium']:.0f}mg",
                'Cholesterol': f"{nutrition_data['cholesterol']:.0f}mg"
            },
            'serving': {
                'Size': f"{nutrition_data['serving_qty']} {nutrition_data['serving_unit']}",
                'Weight': f"{nutrition_data['serving_weight_grams']:.0f}g" if nutrition_data['serving_weight_grams'] else "N/A"
            }
        }

# Test function
def test_nutrition_api():
    """Test the nutrition API with sample foods"""
    api = NutritionAPI()
    
    test_foods = ["pizza", "apple", "chicken biryani", "paneer butter masala"]
    
    for food in test_foods:
        print(f"\n🧪 Testing: {food}")
        result = api.get_nutrition(food)
        
        if result['success']:
            print(f"✅ Calories: {result['calories']}")
            print(f"✅ Protein: {result['protein']}g")
            print(f"✅ Carbs: {result['total_carbs']}g")
            print(f"✅ Fat: {result['total_fat']}g")
        else:
            print(f"❌ Error: {result['error']}")

if __name__ == "__main__":
    test_nutrition_api()