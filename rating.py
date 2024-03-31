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
    prompt = "Evaluate the safety level of the product below out of 100, based on its ingredients. \
    List the top 5 ingredients with potential safety implications, ordered from most to least significant, \
    Product description: \n" + text_from_image
    response = model.generate_content(prompt)
    print(response.text)
    return response.text