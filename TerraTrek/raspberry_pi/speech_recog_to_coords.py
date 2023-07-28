# Reference: https://maker.pro/raspberry-pi/projects/speech-recognition-using-google-speech-api-and-python

import speech_recognition as sr
import pyaudio
import MIE_Google_Maps_API as gma

import gc
gc.enable()

def speech_to_coord():
    a = sr.Recognizer()
    print(a.pause_threshold, a.non_speaking_duration, a.energy_threshold)
    a.energy_threshold = 100
    a.operation_timeout = 5
    with sr.Microphone() as source:
        data = "default"
        lat, long = None, None
        audio = a.adjust_for_ambient_noise(source, 0.5)
        audio=a.listen(source)
        try:
            data=a.recognize_google(audio)
            print(data)
            lat, long = gma.extract_lat_long(data)
            print(lat, long)

        except TimeoutError:
            print("Timed out")
        except sr.UnknownValueError:
            print("could not understand")
        except sr.RequestError as e:
            print("couldn't request from Google - {}".format(e))
        gc.collect()
    
    return data, lat, long
