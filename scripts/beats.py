# Темп и сетка долей трека: python beats.py music.wav  -> beats.json {bpm, beats:[...]}
import subprocess, sys, json, shutil
import numpy as np
SR = 22050
raw = subprocess.run([shutil.which('ffmpeg'), '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.float32)
hop = 512; n = len(x) // hop
e = np.array([np.sum(x[i * hop:(i + 1) * hop] ** 2) for i in range(n)])
on = np.maximum(0, np.diff(np.log1p(e * 1000), prepend=0))            # всплески энергии
fps = SR / hop
ac = np.correlate(on - on.mean(), on - on.mean(), 'full')[len(on) - 1:]
lags = np.arange(len(ac)); bpm_l = 60 * fps / np.maximum(lags, 1)
mask = (bpm_l >= 90) & (bpm_l <= 180)
L = int(lags[mask][np.argmax(ac[mask])])
# уточнение периода точнее одного отсчёта: перебор вокруг пика по сумме энергии на сетке долей
def score(p): return max(sum(on[int(o + k * p)] for k in range(int((n - o) / p))) for o in range(0, int(p), 2))
period = max(np.arange(L - 1, L + 1.01, .05), key=score); bpm = 60 * fps / period
best = max(range(int(period)), key=lambda o: sum(on[int(o + k * period)] for k in range(int((n - o) / period))))  # фаза долей
beats = [round((best + k * period) / fps, 3) for k in range(int((n - best) / period) + 1)]
json.dump({'bpm': round(bpm, 1), 'beats': beats}, open('beats.json', 'w'))
print(f'темп ≈ {bpm:.1f} BPM, первая доля {beats[0]:.2f} с, долей {len(beats)} → beats.json')
