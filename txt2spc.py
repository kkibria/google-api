"""Synthesizes speech from the input string of text or ssml.
Make sure to be working in a virtual environment.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
from lib import get_tokens, CLOUD_PLATFORM_SCOPE
 
credentials = get_tokens(fetch=True, scope=CLOUD_PLATFORM_SCOPE)

# Instantiates a client
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Set the text input to be synthesized
# <prosody rate="x-slow" pitch="+5st">
# </prosody>

ssml = """<emphasis level="reduced">
Brad sings of love, Ana's heart will sway,
Three years strong, and forever to stay,
First date spot, where he'll get down on one knee,
Ana, my love, will you marry me?"
</emphasis>"""

synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
# synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    name="en-US-Wavenet-I"
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3,
    # effects_profile_id="headphone-class-device",
    speaking_rate=1.0
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')