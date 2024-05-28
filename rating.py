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

def get_text_from_image(path):
   
   return f"image in {path} received!\n"

def rating_prompt(path):
    """Generate a safety rating and description for a product based on its image URL."""
    # Extract text from the image at the given URL
    text_from_image = get_text_from_image(path)

    print(text_from_image)
    return text_from_image