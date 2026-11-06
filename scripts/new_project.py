# Новый проект ролика: python new_project.py <папка> [ширина высота]
# Копирует шаблон film.html, three.min.js и рабочие скрипты, создаёт папки.
import sys, shutil, pathlib, re
here = pathlib.Path(__file__).resolve().parent.parent
dst = pathlib.Path(sys.argv[1]); w, h = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1920, 1080)
dst.mkdir(parents=True, exist_ok=True)
for d in ('ph', 'refs', 'logos', 'fonts', 'frames', 'results'): (dst / d).mkdir(exist_ok=True)
html = (here / 'templates/film.html').read_text(encoding='utf-8')
if (w, h) != (1920, 1080):
    html = html.replace('const W=1920,H=1080', f'const W={w},H={h}')
(dst / 'film.html').write_text(html, encoding='utf-8')
shutil.copy(here / 'templates/three.min.js', dst)
for s in ('render.py', 'snap.py', 'encode.sh', 'words.py', 'loudness.py', 'storyboard.py', 'ref_sheet.py', 'fetch_font.py', 'beats.py'):
    shutil.copy(here / 'scripts' / s, dst)
if (w, h) != (1920, 1080):
    for s in ('render.py', 'snap.py'):
        p = dst / s; p.write_text(p.read_text(encoding='utf-8').replace("'width':1920,'height':1080", f"'width':{w},'height':{h}"), encoding='utf-8')
print(f'Проект {dst} готов ({w}x{h}). Дальше: бриф → референсы → стиль-кадры (python snap.py check 1 5 9).')
