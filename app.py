from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import texttospeech
from rating import rating_prompt

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
    
@app.route("/", methods=['GET', 'POST'])
def incoming_data():
    response = MessagingResponse()
    message = response.message()
    user_input = request.form.get("NumMedia")

    if user_input == "1":
        picture_url = request.form.get("MediaUr10")

        rating = rating_prompt(picture_url)
        text_to_audio(rating)

        message.media("./resources/output.mp3")
        message.body("Rating & Description")
        message.body(f"{rating}")

        return str(response), 200
    
    else:
        message.body("Please send a picture containing ingredients")
        return str("Please send a picture containing ingredients")

@app.route("/resources/<path:path>")
def send_resources(path):
    return send_from_directory("resources", path)

if __name__ == "__main__":
    app.run(host = "localhost", debug = True, port = 8080)

