#!/usr/bin/env python
from math import hypot
from time import sleep
# libraries
import numpy as np
from scipy.io import wavfile
from simpleaudio import play_buffer
# mine
import analyze_ddu as ad

sample_rate = 44_100 # Hz

# durations in seconds
def timespace(duration):
    n_frames = round(duration * sample_rate)
    return np.linspace(0, duration, n_frames, endpoint=False)

def sine_wave(frequency, amplitude, duration):
    #half_period = 1/(2 * frequency)
    #n_tacts = round(duration/half_period)
    #t = timespace(n_tacts * half_period)
    t = timespace(duration)
    return amplitude * np.sin(frequency * t * 2 * np.pi)

def sum_wave(waves):
    return sum(waves) # uhh

# accord = [(freq, amplitude)]
def accords2wave(accords, note_duration=0.5):
    wave = np.hstack([
        sum_wave(sine_wave(f, a, note_duration) for f, a in accord)
        for accord in accords
        ])
    return wave

def convert_wave(wave):
    wave *= (2**15 - 1) / np.max(np.abs(wave)) # normalize to 16-bit range
    audio = wave.astype(np.int16)
    return audio

def play_audio(audio):
    return play_buffer(audio, 1, 2, sample_rate) # 1-channel

def play_wave(wave):
    return play_audio(convert_wave(wave))

def save_audio(audio, filename="ddu-audio.wav"):
    wavfile.write(filename, sample_rate, audio)

def r2amplitude(radius):
    # 500 = large
    # 300 = average
    # 100 = small
    v = np.arctan(radius/100) / (np.pi/2) # in (0; 1) since r > 0
    a = 1.0*v
    #print(f"r={radius:.4f} -> {a:.4f}")
    return a

def center2freq(x, y):
    # normal hearing range is 20Hz-20kHz
    # good center for winter: (400, 640)
    d = hypot(x - 400, y - 640)
    v = min(1 + d/10, 1000) # [1; 1000]
    f = 20*v
    #print(f"d={d:.4f} -> {f:.4f}Hz")
    return f

def play_ddu(name="Winter", targets=[-3,-2,-1], note_duration=0.2, n_notes=200):
    ddu = ad.ddu_named(name)
    accords = []
    for _ in range(n_notes):
        accords.append(
            [
                (
                    center2freq(ddu.circles[tIx].x, ddu.circles[tIx].y),
                    r2amplitude(ddu.circles[tIx].r)
                ) for tIx in targets
            ]
        )
        ddu.step()
    audio = convert_wave(accords2wave(accords, note_duration))
    save_audio(audio)
    return play_audio(audio)

def play():
    #return play_ddu("Unknown lady", [6, 9]) <- bad
    #return play_ddu("Klein bottle", [4, -1])
    #return play_ddu("Sakura", [6, 22])
    return play_ddu(targets=[-3,-2,-1], note_duration=0.03, n_notes=2000)

if __name__ == '__main__':
    play()
