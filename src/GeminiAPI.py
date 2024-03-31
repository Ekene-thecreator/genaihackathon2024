# TODO(developer): Vertex AI SDK - uncomment below & run
# pip3 install --upgrade --user google-cloud-aiplatform
# gcloud auth application-default login
import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, Part

#load environment variables from .env file
load_dotenv()

vertexai.init(project= os.getenv("PROJECT_ID"), location=os.getenv("LOCATION"))
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Image,
    Part,
)

# Comment out this part because I am not input image as a parameter, but the implementation is here if you want image as an input
"""
# Restart kernel after installs so that your environment can access the new packages
import IPython
import time

app = IPython.Application.instance()
app.kernel.do_shutdown(True)


import sys

# Additional authentication is required for Google Colab
if "google.colab" in sys.modules:
    # Authenticate user to Google Cloud
    from google.colab import auth

    auth.authenticate_user()

# Define project information
# You can use Colab secrets if you wish to keep it hidden
from google.colab import userdata
my_project = userdata.get('GCP_PROJECT_ID')

print(PROJECT_ID)
"""

# Load the model
multimodal_model = GenerativeModel("gemini-1.0-pro-vision") #gemini-1.0-pro-vision (if for image)
# Prepare contents
prompt = "Analyze the ingredients of the skincare products, and give feedback on how healthy each one is?"
ingredient_text = "Hyaluronic Acid, Retinol (Vitamin A)"


"""
Generate a response based on the provided ingredient text.
This function uses a generative model with a predefined configuration to generate the response.
Args:
    ingredient_text (str): The text containing the ingredient information.
Returns:
    list of str: A list of generated responses based on the provided ingredient text.
Example:
    >>> ingredient_text = "Hyaluronic Acid: Very healthy. Moisturizes and hydrates the skin."
    >>> responses = generate_response(ingredient_text)
    >>> print(responses)
"""
def generate_response(ingredient_text):
    contents = [prompt,ingredient_text]
    # Use a more deterministic configuration with a low temperature
    # https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini
    generation_config = GenerationConfig(
        temperature=0.9,          # higher = more creative (default 0.0)
        top_p=0.8,                # higher = more random responses, response drawn from more possible next tokens (default 0.95)
        top_k=40,                 # higher = more random responses, sample from more possible next tokens (default 40)
        candidate_count=1,
        max_output_tokens=1024,
    )
    safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }
    #BLOCK_ONLY_HIGH - block when high probability of unsafe content is detected
    #BLOCK_MEDIUM_AND_ABOVE - block when medium or high probablity of content is detected
    #BLOCK_LOW_AND_ABOVE - block when low, medium, or high probability of unsafe content is detected
    #BLOCK_NONE - always show, regardless of probability of unsafe content

    # Query the model
    responses = multimodal_model.generate_content(
        contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False
    )
    #for response in responses:
    #    print(response, end="")
    return responses
