import requests
import os
from requests.auth import HTTPBasicAuth
from text_detection import detect_text
from dotenv import load_dotenv
import google.generativeai as genai
from google.oauth2 import service_account
from dotenv import load_dotenv

from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel

from GeminiAPI import generate_response

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials_path))

aiplatform.init(project="genai-hackathon-2024-418816", credentials=credentials)

model = GenerativeModel("gemini-1.0-pro")

def get_text_from_image(url):
    img_data = requests.get(url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content
    with open('resources/image.jpg', 'wb') as handler:
        handler.write(img_data)
    return detect_text()

def rating_prompt(url):
    text_from_image = get_text_from_image(url)
    prompt = "I have a product that I want to consume, below is the nutritional infromation or ingredients used. Please let me know how safe this product is for consumption. Please note that the nutritional information could be in any language however respond in English. Lastly, please limit your response to a 100 words. Nutritional Information: \n" + text_from_image
    response = model.generate_content(prompt)
    # response = generate_response(prompt, text_from_image)
    response_without_asterisks = response.text.replace("*", "")
    print(response_without_asterisks)
    return response_without_asterisks