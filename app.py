from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import texttospeech
from rating import rating_prompt
import os

# Initialize the Flask application
app = Flask(__name__)

# Retrieve and set the path for Google Cloud credentials from environment variables
credentials_path = os.path.expanduser(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Initialize the Google Cloud Text-to-Speech client with credentials
client = texttospeech.TextToSpeechClient.from_service_account_json(credentials_path)

# Check if the 'resources' directory exists, create it if not
resources_dir = 'resources'
if not os.path.exists(resources_dir):
    os.makedirs(resources_dir)

# Function to convert text to audio using Google Text-to-Speech
def text_to_audio(text):
    # Configure the text input, voice parameters, and audio configuration
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Generate the speech synthesis response
    response = client.synthesize_speech(input=synthesis_input, 
                                        voice=voice, 
                                        audio_config=audio_config)

    # Save the audio content to an MP3 file in the 'resources' directory
    with open("resources/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file output.mp3")

# Define the route for incoming data (e.g., from Twilio SMS)
@app.route("/", methods=['GET', 'POST'])
def incoming_data():
    response = MessagingResponse()
    message = response.message()
    user_input = request.form.get("NumMedia")

    # If there's at least one media item, process it
    if user_input == "1":
        picture_url = request.form.get("MediaUrl0")
        rating = rating_prompt(picture_url)
        text_to_audio(rating)
        
        # Append the rating text and the audio file URL to the response message
        message.body("Rating & Description")
        message.body(f"{rating}")
        message.media("resources/output.mp3")
        return str(response), 200
    else:
        # If no image is sent, ask the user to send one
        return "Please send a picture containing ingredients", 400

# Serve files from the 'resources' directory under the '/resources' path
@app.route("/resources/<path:path>")
def send_resources(path):
    return send_from_directory("resources", path)

# Main entry point for the application
if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
