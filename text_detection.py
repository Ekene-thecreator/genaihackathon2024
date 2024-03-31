import io
import os
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def detect_text():
    """Detects text in the file."""
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = vision.ImageAnnotatorClient(credentials=credentials)

    file = os.path.abspath("resources/image.jpg")

    with io.open(file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        return texts[0].description
    else:
        return "No text found in the image."

# if __name__ == "__main__":
#     detect_text()