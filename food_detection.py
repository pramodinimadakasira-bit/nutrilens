# food_detection.py (The new, professional version)

import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import base64

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Load environment variables
load_dotenv()

class FoodDetector:
    def __init__(self):
        """Initialize the Clarifai food detection model"""
        self.pat = os.getenv('CLARIFAI_PAT')
        if not self.pat:
            print("❌ Clarifai PAT (Personal Access Token) not found in .env file!")
            self.model_loaded = False
            return
            
        # These are standard values for the Clarifai General Food Model
        self.user_id = 'dino'
        self.app_id = 'nutrilens'
        self.model_id = 'food-item-recognition'
        self.model_version_id = '1d5fd481e0cf4826aa72ec3ff049e044'
        
        try:
            channel = ClarifaiChannel.get_grpc_channel()
            self.stub = service_pb2_grpc.V2Stub(channel)
            self.model_loaded = True
            print("✅ Clarifai Food Detector initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing Clarifai: {e}")
            self.model_loaded = False

    def detect_food(self, image):
        """
        Detect food items from an image using the Clarifai API.
        
        Args:
            image: PIL Image object.
            
        Returns:
            dict: The same format as your old detector for compatibility.
        """
        if not self.model_loaded:
            return {
                'success': False,
                'error': 'Clarifai Food Detector is not initialized. Check your API Key (PAT) in .env file.'
            }

        try:
            # Convert PIL image to bytes
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            image_bytes = buffered.getvalue()

            post_model_outputs_response = self.stub.PostModelOutputs(
                service_pb2.PostModelOutputsRequest(
                    user_app_id=resources_pb2.UserAppIDSet(user_id=self.user_id, app_id=self.app_id),
                    model_id=self.model_id,
                    version_id=self.model_version_id,
                    inputs=[
                        resources_pb2.Input(
                            data=resources_pb2.Data(
                                image=resources_pb2.Image(
                                    base64=image_bytes
                                )
                            )
                        )
                    ]
                ),
                metadata=(('authorization', 'Key ' + self.pat),)
            )

            if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
                raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

            # Parse the results
            output = post_model_outputs_response.outputs[0]
            concepts = output.data.concepts
            
            if not concepts:
                return {'success': False, 'error': 'No food items were detected in the image.'}

            # Format the output to be identical to your old detector
            top_result = concepts[0]
            food_name = self.clean_food_name(top_result.name)
            confidence = top_result.value

            alternatives = [
                {'name': self.clean_food_name(c.name), 'confidence': c.value}
                for c in concepts[1:3] # Get the next two alternatives
            ]

            return {
                'success': True,
                'food_name': food_name,
                'confidence': confidence,
                'alternatives': alternatives,
                'error': None
            }

        except Exception as e:
            print(f"❌ Clarifai detection error: {str(e)}")
            return {
                'success': False,
                'error': f'Error during AI food detection: {str(e)}. Please try again.'
            }

    def clean_food_name(self, food_name):
        """Cleans the food name from the API."""
        return ' '.join(word.capitalize() for word in food_name.split())

# Test function to make sure it works
def test_clarifai_detector():
    import requests
    detector = FoodDetector()
    if not detector.model_loaded:
        print("❌ Cannot run test, detector failed to load.")
        return
        
    print("🧪 Testing Clarifai Detector with a pizza image...")
    # A clear image of a pizza
    test_image_url = "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500"
    response = requests.get(test_image_url)
    image = Image.open(BytesIO(response.content))
    
    result = detector.detect_food(image)
    
    print("\n--- TEST RESULTS ---")
    if result['success']:
        print(f"✅ Success!")
        print(f"🍕 Detected Food: {result['food_name']} (Confidence: {result['confidence']:.2%})")
        print("🔄 Alternatives:")
        for alt in result['alternatives']:
            print(f"  - {alt['name']} ({alt['confidence']:.2%})")
    else:
        print(f"❌ Failure: {result['error']}")
    print("--- END TEST ---\n")

if __name__ == "__main__":
    test_clarifai_detector()