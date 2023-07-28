import numpy as np
import pygame
from pygame import mixer as pm

pm.init(channels = 2)

rate = 44100
dur = 100 # ms
freq = 880 # Hz
def play_note(freq, dur):
    t = np.arange(int(dur/1000 * rate))
    l = np.sin(2 * np.pi * freq * t / rate)
    r = np.sin(2 * np.pi * freq * t / rate + np.pi/2)
    note = np.vstack((l, r)).T
    note = (note * 32767/np.max(np.abs(note))).astype(np.int16)
    note = np.ascontiguousarray(note)


    sound = pygame.sndarray.make_sound(note)
    sound.set_volume(0.3)
    sound.play()
    pygame.time.wait(dur+10)
if __name__ == "__main__":
    play_note(2083//2, 50)
    play_note(3130//2, 100)
