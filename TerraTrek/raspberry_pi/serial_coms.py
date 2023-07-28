import serial
import speech_recog_to_coords as srtc
import time
import gc
import Google_tts as gtts
import gpt35_text_generator as chatGPT



class FakeSerial:
    def __init__(self):
        self.in_waiting = 0
    
    def write(self, text : bytearray):
        print("Wrote: {}".format(text.decode("utf-8")))
    
    def readline(self):
        print("Cant readline")
        pass

gc.enable()
if __name__ == "__main__":
    # Uncomment when rasppi is being used
    # s = serial.Serial("/dev/ttyUSB0",9600,timeout=1)
    # s.flush()
    
    # Comment when rasppi is being used
    s = FakeSerial()
    text = "0"
    shut_up = 0
    
    while text.lower() != "goodbye":
        if s.in_waiting > 0:
            shut_up = s.readline().decode("utf-8").rstrip()
            print(shut_up)
        if s.in_waiting <= 0 and shut_up == 0: 
            print("listening") 
            text, lat, long = srtc.speech_to_coord()
            if text.lower() == "goodbye": gtts.speak("exiting now.")
            elif text.lower() != "default" and lat != None:
                prompt = chatGPT.generate_fact(text)
                gtts.speak(prompt)
                        
                s.write(str.encode("{},{}".format(lat, long)))
        gc.collect()