import google.generativeai as genai
from google.oauth2 import service_account
from dotenv import load_dotenv

from google.cloud import aiplatform
from google.oauth2 import service_account
from vertexai import generative_models
from vertexai.generative_models import GenerativeModel


import os


load_dotenv()


credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
credentials = service_account.Credentials.from_service_account_file(os.path.expanduser(credentials_path))

aiplatform.init(project="genai-hackathon-2024-418816", credentials=credentials)


model = GenerativeModel("gemini-1.0-pro")
response = model.generate_content('Introduce yourself')



if __name__ == "__main__":
    print(response.text)
    