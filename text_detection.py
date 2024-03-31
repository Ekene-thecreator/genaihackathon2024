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
    credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials_path))
    client = vision.ImageAnnotatorClient(credentials=credentials)

    file = os.path.abspath(r"resources/test1.jpg")

    with io.open(file, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        # print("Texts:")
        # print(texts[0].description)
        return texts[0].description
    else:
        # print("No text found in the image.")
        return "No text found in the image."

# if __name__ == "__main__":
#     detect_text()