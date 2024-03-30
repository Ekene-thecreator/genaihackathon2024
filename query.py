import google.generativeai as genai
from google.oauth2 import service_account
from dotenv import load_dotenv


import os


load_dotenv()

key = os.environ.get('API_KEY')

if key is None:
    print("API_KEY env variable is not set")

else:
    key = "AIzaSyBO2RVp8lJ3AVYpPdvIKWzMC1WkGDXEfPs"

genai.configure(api_key=key)
 
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Introduce yourself')



if __name__ == "__main__":
    print(response.text)
    