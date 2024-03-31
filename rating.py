import requests
import os
from text_detection import detect_text
from dotenv import load_dotenv
from query import generate_answer

# Load environment variables from .env file
load_dotenv()


def get_text_from_image():
    # img_data = requests.get(url).content
    # with open('resources/image.jpg', 'wb') as handler:
    #     handler.write(img_data)
    return detect_text()

def rating_prompt(ingredients):
    prompt = "Below is a description of the item I am consuming, please provide a rating on how safe this item is to consume. \n" + ingredients
    return prompt



if __name__ == "__main__":
    ingredients = get_text_from_image()
    prompt = rating_prompt(ingredients)
    response = generate_answer(prompt)
    print(response)