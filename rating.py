import requests
import os
from requests.auth import HTTPBasicAuth
from text_detection import detect_text
from dotenv import load_dotenv
from google.oauth2 import service_account
from dotenv import load_dotenv

from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

from GeminiAPI import generate_response

load_dotenv()

# Retrieve Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# Retrieve Google Cloud credentials path from environment variables
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials_path))

aiplatform.init(project="genai-hackathon-2024-418816", credentials=credentials)

# Initialize the generative model using Vertex AI with the specified model name
model = GenerativeModel("gemini-1.0-pro")

def get_text_from_image(url):
    """Download an image from the provided URL using Twilio credentials and detect text within it."""
    # Download the image content using HTTP GET request with Basic Auth for Twilio access
    img_data = requests.get(url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content
    # Save the downloaded image to a file
    with open('resources/image.jpg', 'wb') as handler:
        handler.write(img_data)
    
    # Return the detected text from the image
    return detect_text()

def rating_prompt(url):
    """Generate a safety rating and description for a product based on its image URL."""
    # Extract text from the image at the given URL
    text_from_image = get_text_from_image(url)

    prompt = "I have a product that I want to consume, below is the nutritional information or ingredients used. Please let me know how safe this product is for consumption. Please note that the nutritional information could be in any language however respond in English. Lastly, please limit your response to a 100 words. Nutritional Information: \n" + text_from_image
    
    # Generate a response based on the prompt
    response = model.generate_content(prompt)
    # response = generate_response(prompt, text_from_image)
    
    response_without_asterisks = response.text.replace("*", "")
    # Print and return the cleaned response
    print(response_without_asterisks)
    return response_without_asterisks