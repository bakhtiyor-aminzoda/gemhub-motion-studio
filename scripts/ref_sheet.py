# Лист кадров референса: python ref_sheet.py <файл или ссылка на mp4> <выход.jpg> [кадров=24]
import subprocess, sys, json
src, out = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 24
d = float(json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', src],
                                    capture_output=True, text=True).stdout)['format']['duration'])
step = max(.3, d / n)
subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf',
                       f'fps=1/{step:.3f},scale=400:-2,tile=6x{(n + 5) // 6}:padding=4', '-frames:v', '1', out])
print(f'{out}: {n} кадров, шаг {step:.2f} с, длина {d:.1f} с')
