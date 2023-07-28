import os
from unicodedata import name
from urllib import response
from google.cloud import texttospeech_v1 as tts
import sys
import pygame
pygame.init()

print(sys.version)

# help(tts)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'PROJECT_ACCESS_JSON_FILE.json'
client = tts.TextToSpeechClient()

pygame.mixer.music.set_volume(1) 
# text = '''This is a test?'''

# synthesis_input = tts.SynthesisInput(text=text)

voice1 = tts.VoiceSelectionParams(language_code="en-GB",
                                  ssml_gender=tts.SsmlVoiceGender.FEMALE)

# print(client.list_voices)
audio_config = tts.AudioConfig(audio_encoding = tts.AudioEncoding.MP3)

# response1 = client.synthesize_speech(input = synthesis_input,
#                                      voice = voice1,
#                                      audio_config = audio_config)

def speak(text):
    synthesis_input = tts.SynthesisInput(text=text)
    response1 = client.synthesize_speech(input = synthesis_input,
                                         voice = voice1,
                                         audio_config = audio_config)
    
    with open("audio.mp3", 'wb',) as output:
        output.write(response1.audio_content)

    pygame.mixer.music.load("audio.mp3")
    # channel = audio.play()
    pygame.mixer.music.play()
    # wait for audio to finish playing
    # So the program doesnt end before the audio is played
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100) # this is 100ms
    pygame.mixer.music.stop()

if __name__ == '__main__':
    speak("TEST")

