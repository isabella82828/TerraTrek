import pvporcupine

import serial
import speech_recog_to_coords as srtc
import time
# import gc
import Google_tts as gtts
import gpt35_text_generator as chatGPT
import pygame
from pygame import mixer as pm
import play_sound
pm.init()

def play_listening_notes():  
    play_sound.play_note(2083//2,  50)
    play_sound.play_note(3130//2, 100)

def play_stop_listening_notes():  
    play_sound.play_note(3130//2,  50)
    play_sound.play_note(2083//2, 100)


class FakeSerial:
    def __init__(self, path, baud_rate, timeout):
        self.in_waiting = 0
    
    def write(self, text : bytearray):
        print("Wrote: {}".format(text.decode("utf-8")))
    
    def readline(self):
        print("Cant readline")
        pass
    
    def flush(self):
        pass
    
s = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)
s.flush()
text = "0"
shut_up = 0

access_key = "PORCUPINE_KEY"

for keyword in pvporcupine.KEYWORDS:
    print(keyword)
    
# import pvporcupine
from pvrecorder import PvRecorder

porcupine = pvporcupine.create(
    access_key=access_key,
    keyword_paths = ["/home/pi/Desktop/MIE438_Final_Project/hey-globe-bot_en_raspberry-pi_v2_1_0/hey-globe-bot_en_raspberry-pi_v2_1_0.ppn"]
    )
print(porcupine.frame_length)
recoder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)


try:
    recoder.start()


    while True:
        keyword_index = porcupine.process(recoder.read())

        if keyword_index >= 0 and shut_up == 0:
            print(f"Detected 'hey globe bot'")
            play_listening_notes()
            recoder.stop()           
         #   if s.in_waiting <= 0: 
            print("listening") 
            text, lat, long = srtc.speech_to_coord()
            #lat, long = 45, 45
            if text.lower() == "goodbye": gtts.speak("exiting now.")
            elif text.lower() != "default" and lat != None:
                
                #s.write(b"45,45")
                coords_str = "{},{}".format(lat, long)
                s.write(coords_str.encode('utf-8'))
                prompt = chatGPT.generate_fact(text)
                gtts.speak(prompt)
            else: gtts.speak("Could not understand.")
            play_stop_listening_notes()
            print("re-enabled")
            recoder.start()
            print("re-enabled2")
        time.sleep(0.01)
except KeyboardInterrupt:
    recoder.stop()
finally:
    porcupine.delete()
    recoder.delete()
