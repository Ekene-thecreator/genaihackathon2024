import io
import os
from google.cloud import vision
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables from the .env file, specifically for Google Cloud credentials
load_dotenv()

def detect_text():
    """Function to detect text in an image using Google Cloud Vision API."""
    
    # Retrieve the path to the Google Cloud credentials JSON file from environment variables
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Load the credentials for Google Cloud services
    credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials_path))
    
    # Initialize the Google Cloud Vision API client with the loaded credentials
    client = vision.ImageAnnotatorClient(credentials=credentials)

    # Define the path to the image file from which to extract text
    file = os.path.abspath("resources/image.jpg")

    # Open the image file in binary-read mode and read its content
    with io.open(file, "rb") as image_file:
        content = image_file.read()

    # Create an Image object with the content of the read image file
    image = vision.Image(content=content)

    # Call the text_detection method of the Vision API client to detect text in the image
    response = client.text_detection(image=image)
    
    # Extract text annotations from the response
    texts = response.text_annotations
    
    # If any text is detected, return the description of the first annotation
    # The first element in `texts` contains the entire detected text block
    if texts:
        return texts[0].description
    else:
        # If no text is detected, return a placeholder message
        return "No text found in the image."
