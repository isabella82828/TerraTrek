import pvporcupine
# hey-globe-bot_en_raspberry-pi_v2_1_0.ppn

porcupine = pvporcupine.create(
    access_key='auNBcBCNJ1ohyzV9V+UXDCT4B8X3AOgLrCGsLCBYH2MgleRcbWfb8A==',
    keyword_paths = ["/home/pi/Desktop/MIE438_Final_Project/hey-globe-bot_en_raspberry-pi_v2_1_0/hey-globe-bot_en_raspberry-pi_v2_1_0.ppn"]
    )

import pyaudio
import numpy as np

# Define audio parameters
SAMPLE_RATE = 16000
BLOCK_SIZE = 512

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=BLOCK_SIZE)

def get_next_audio_frame():
    # Read audio data from stream
    block = stream.read(BLOCK_SIZE)
    # Convert audio data to a NumPy array
    pcm = np.frombuffer(block, dtype=np.int16)
    return pcm

def wake_word_callback():
    print("detected")


while True:
    try:
        pcm = get_next_audio_frame()
        keyword_idx = porcupine.process(pcm)
        if keyword_idx >= 0:
            wake_word_callback()
    except KeyboardInterrupt:    
        porcupine.delete()
        break