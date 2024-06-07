from flask import Flask, request, send_from_directory
from google.cloud import texttospeech
from rating import rating_prompt
import os
import pytesseract

# Initialize the Flask application
app = Flask(__name__)


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Check if the 'resources' directory exists, create it if not
resources_dir = 'resources'
if not os.path.exists(resources_dir):
    os.makedirs(resources_dir)

# Define the route for incoming data (e.g., from Twilio SMS)
@app.route("/", methods=['GET', 'POST'])
def incoming_data():
        picture_path = "test_images/test1.jpg"
        rating = rating_prompt(picture_path)

        return rating

# Save files from the 'resources' directory under the '/resources' path
@app.route("/resources/<path:path>")
def send_resources(path):
    return send_from_directory("resources", path)

# Main entry point for the application
if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
