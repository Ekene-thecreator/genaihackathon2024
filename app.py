from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import texttospeech
from rating import rating_prompt
import os

app = Flask(__name__)

client = texttospeech.TextToSpeechClient()

resources_dir = 'resources'
if not os.path.exists(resources_dir):
    os.makedirs(resources_dir)

def text_to_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text = text)

    voice = texttospeech.VoiceSelectionParams(
        language_code = "en-US", 
        ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding = texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input = synthesis_input, 
        voice = voice, 
        audio_config = audio_config
    )

    with open("resources/output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content wrtten to file output.mp3")
    
@app.route("/", methods=['GET', 'POST'])
def incoming_data():
    response = MessagingResponse()
    message = response.message()
    user_input = request.form.get("NumMedia")

    if user_input == "1":
        picture_url = request.form.get("MediaUrl0")
        rating = rating_prompt(picture_url)
        text_to_audio(rating)
            
        message.body("Rating & Description")
        message.body(f"{rating}")
        message.media("resources/output.mp3") 
        return str(response), 200
    else:
        return "Please send a picture containing ingredients", 400


@app.route("/resources/<path:path>")
def send_resources(path):
    return send_from_directory("resources", path)

if __name__ == "__main__":
    app.run(host = "localhost", debug = True, port = 8080)

