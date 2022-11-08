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
    wave = sum(sin_wave(freq, amp) for freq, amp in zip(freqs, amps))
    return play_wave(wave)

# fas = (freq, amplitude) iterator
def play_seq(fas, note_duration=0.5):
    wave = np.hstack([sin_wave(f, a, note_duration) for (f,a) in fas])
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
    v = min(1 + d/20, 1000) # [1; 1000]
    f = 20*v
    #print(f"d={d:.4f} -> {f:.4f}Hz")
    return f

def play_ddu(name="Winter"):
    frame_duration = 0.2
    ddu = ad.ddu_named(name)
    target_index = -3 # any of the last 3 for winter
    fas = []
    for _ in range(100):
        c = ddu.circles[target_index]
        a = r2amplitude(c.r) # radius -> amplitude
        f = center2freq(c.x, c.y) # distance -> frequency
        #play_accord([f], [a], frame_duration).wait_done()
        fas.append((f, a))
        ddu.step()
    return play_seq(fas, frame_duration)



