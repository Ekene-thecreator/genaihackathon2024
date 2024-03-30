import requests
import os
from text_detection import detect_text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_text_from_image(url):
    img_data = requests.get(url).content
    with open('resources/image.jpg', 'wb') as handler:
        handler.write(img_data)
    return detect_text()

def rating_prompt(url):
    print(get_text_from_image(url))