# Раскадровка готового MP4: кадр в секунду + поиск резких скачков между соседними кадрами
# python storyboard.py <файл.mp4> [колонок=8]
import subprocess, sys, json, os, tempfile
from PIL import Image, ImageChops, ImageStat
src = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 8
d = float(json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', src], capture_output=True, text=True).stdout)['format']['duration'])
n = int(d)
rows = (n + cols - 1) // cols
out = os.path.splitext(src)[0] + '_storyboard.jpg'
subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', f'fps=1,scale=320:-2,tile={cols}x{rows}:padding=4', '-frames:v', '1', out])
print('раскадровка:', out)
# скачки: сравниваем кадры через 1/10 с, ищем резкие разовые вспышки (мелькания)
tmp = tempfile.mkdtemp()
subprocess.check_call(['ffmpeg', '-v', 'error', '-i', src, '-vf', 'fps=10,scale=160:-2', f'{tmp}/f%05d.png'])
fs = sorted(os.listdir(tmp)); prev = None; diffs = []
for i, f in enumerate(fs):
    im = Image.open(os.path.join(tmp, f)).convert('L')
    if prev is not None: diffs.append((i / 10, ImageStat.Stat(ImageChops.difference(im, prev)).mean[0]))
    prev = im
spikes = [(t, v) for j, (t, v) in enumerate(diffs[1:-1], 1) if v > 25 and diffs[j - 1][1] < v / 3 and diffs[j + 1][1] > v / 2]
print('резкие смены (проверьте, что это задуманные склейки):', ', '.join(f'{t:.1f}с' for t, _ in spikes) or 'нет')
