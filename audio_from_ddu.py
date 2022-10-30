from math import hypot
from time import sleep
# libraries
import numpy as np
from simpleaudio import play_buffer
# mine
import analyze_ddu as ad

sample_rate = 44_100 # Hz

def timespace(duration):
    n_frames = round(duration * sample_rate)
    return np.linspace(0, duration, n_frames, endpoint=False)

# duration in seconds
def play_accord(freqs, amps, duration=0.5):
    t = timespace(duration)
    audio = sum(amp * np.sin(freq * t * 2 * np.pi) for freq, amp in zip(freqs, amps))
    audio *= (2**15 - 1) / np.max(np.abs(audio)) # normalize to 16-bit range
    audio = audio.astype(np.int16)
    return play_buffer(audio, 1, 2, sample_rate)

def r2amplitude(radius):
    # 500 = large
    # 300 = average
    # 100 = small
    v = np.arctan(radius/100) / (np.pi/2) # in (0; 1) since r > 0
    a = 1.5*v
    print(f"r={radius:.4f} -> {a:.4f}")
    return a

def center2freq(x, y):
    # normal hearing range is 20Hz-20kHz
    # good center for winter: (400, 640)
    d = hypot(x - 400, y - 640)
    v = min(1 + d/100, 1000) # [1; 1000]
    f = 20*v
    print(f"d={d:.4f} -> {f:.4f}Hz")
    return f

def play_ddu(ddu_filename="Winter.ddu"):
    frame_duration = 0.5 # seconds
    ddu = ad.Ddu.read_from(ad.dir_path + ddu_filename)
    target_index = -2 # any of the last 3 for winter
    # radius -> amplitude
    # distance -> frequency

    for _ in range(20):
        c = ddu.circles[target_index]
        a = r2amplitude(c['r'])
        f = center2freq(c['x'], c['y'])
        play_accord([f], [a], frame_duration).wait_done()
        ddu.step()


