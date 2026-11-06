# Громкость готового файла: python loudness.py <файл>
# Цель для соцсетей: около -14 LUFS, пик не выше -1 dBFS, самые громкие 3 с на 1-3 LU выше среднего
import subprocess, sys, re
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', sys.argv[1], '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   capture_output=True, text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', r)[-1])
P = float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', r)[-1])
S = [(float(a), float(b)) for a, b in re.findall(r't: ([\d.]+)\s.*?S:\s*(-?[\d.]+)', r)]
t, s = max(S, key=lambda x: x[1])
print(f'Средняя громкость {I} LUFS, пик {P} dBFS, самый громкий момент {t:.1f} с ({s - I:+.1f} LU)')
if not -16 <= I <= -12: print('  громкость вне -16..-12 LUFS')
if P > -1: print('  пик выше -1 dBFS, возможны искажения')
if s - I < .6: print('  нет выделенной кульминации: сделайте финал на 2-3 дБ громче')
