import requests
import os
from requests.auth import HTTPBasicAuth
from text_detection import detect_text
from dotenv import load_dotenv

dotenv_path = '/absolute/path/to/your/.env'
load_dotenv(dotenv_path=dotenv_path)

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

def get_text_from_image(url):
    img_data = requests.get(url, auth=HTTPBasicAuth(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)).content
    with open('resources/image.jpg', 'wb') as handler:
        handler.write(img_data)
    return detect_text()

def rating_prompt(url):
    text_from_image = get_text_from_image(url)
    print(text_from_image)
    return text_from_image