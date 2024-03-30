from flask import Flask, request, send_fron_directory
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import texttospeech

app = Flask(__name__)

client = texttospeech.TextToSpeechClient()

def respond(message):
    response = MessagingResponse()
    response.message(message)
    return str(response)

def text_to_audio(text):
    synthesis_input = texttospeech.SynthesisInput(text = text)

    voice = texttospeech.VoiceSelectionParams(
        language_code = "en-US", 
        ssml_gender = texttospeech.SsmlVoiceGender.MALE
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
    
@app.route("/ingredients", methods=['GET', 'POST'])
def incoming_data():
    response = MessagingResponse()
    message = response.message()
    user_input = request.form.get("NumMedia")

    if user_input == "1":
        pic_url = request.