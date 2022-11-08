from math import hypot
from time import sleep
# libraries
import numpy as np
from simpleaudio import play_buffer
# mine
import analyze_ddu as ad

sample_rate = 44_100 # Hz

# durations in seconds
def timespace(duration):
    n_frames = round(duration * sample_rate)
    return np.linspace(0, duration, n_frames, endpoint=False)

def sin_wave(frequency, amplitude, duration):
    t = timespace(duration)
    return amplitude * np.sin(frequency * t * 2 * np.pi)

def play_wave(audio):
    audio *= (2**15 - 1) / np.max(np.abs(audio)) # normalize to 16-bit range
    audio = audio.astype(np.int16)
    return play_buffer(audio, 1, 2, sample_rate) # 1-channel

def play_accord(freqs, amps, duration=0.5):
    wave = sum(sin_wave(freq, amp, duration) for freq, amp in zip(freqs, amps))
    return play_wave(wave)

# accord = [(freq, amplitude)]
def play_accords(accords, note_duration=0.5):
    wave = np.hstack([
        sum(sin_wave(f, a, note_duration) for f, a in accord)
        for accord in accords
        ])
    return play_wave(wave)

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
    return play_accords(accords, note_duration)

def play():
    #return play_ddu("Unknown lady", [6, 9]) <- bad
    #return play_ddu("Klein bottle", [4, -1])
    #return play_ddu("Sakura", [6, 22])
    return play_ddu(note_duration=0.05, n_notes=500)
