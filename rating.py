import requests
import io
from requests.auth import HTTPBasicAuth
from text_detection import detect_text
from dotenv import load_dotenv
from google.oauth2 import service_account
from dotenv import load_dotenv

from google.cloud import aiplatform
from google.cloud import vision
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

import pytesseract
from PIL import Image

from GeminiAPI import generate_response


client = vision.ImageAnnotatorClient()

def get_text_from_image(path):
   

   with io.open(path, 'rb') as image_file:
    content = image_file.read()
    image = vision.Image(content=content)

   response = client.text_detection(image=image)
   text = response.text_annotations


   if text: 
      return text[0].description

   return "No text detected"

def rating_prompt(path):
    """Generate a safety rating and description for a product based on its image URL."""
    # Extract text from the image at the given URL
    text_from_image = get_text_from_image(path)

    print(text_from_image)
    return text_from_image