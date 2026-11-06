# Скачать шрифт Google Fonts в проект: python fetch_font.py "Unbounded" 400,700,900 [--italic] [--out fonts]
# Создаёт fonts/<файлы>.woff2 и fonts/fonts.css с @font-face (кириллица и латиница).
import sys, re, urllib.request, pathlib
args = [a for a in sys.argv[1:] if not a.startswith('--')]
fam = args[0]; weights = (args[1] if len(args) > 1 else '400,700').split(',')
italic = '--italic' in sys.argv
out = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else pathlib.Path('fonts')
out.mkdir(parents=True, exist_ok=True)
axis = 'ital,wght@' + ';'.join(f'{i},{w}' for i in ((0, 1) if italic else (0,)) for w in weights) if italic else 'wght@' + ';'.join(weights)
url = f'https://fonts.googleapis.com/css2?family={fam.replace(" ", "+")}:{axis}&display=block'
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'
css = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': ua})).read().decode()
blocks = re.findall(r'/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*{[^}]+})', css)
keep = {'cyrillic', 'cyrillic-ext', 'latin', 'latin-ext'}
res = []; n = 0
for subset, block in blocks:
    if subset not in keep: continue
    src = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    w = re.search(r'font-weight:\s*(\d+)', block).group(1); st = re.search(r'font-style:\s*(\w+)', block).group(1)
    name = f'{fam.replace(" ", "")}-{w}{"i" if st == "italic" else ""}-{subset}.woff2'
    (out / name).write_bytes(urllib.request.urlopen(src).read()); n += 1
    res.append(block.replace(src, name))
css_path = out / 'fonts.css'
with open(css_path, 'a', encoding='utf-8') as f: f.write(f'/* {fam} */\n' + '\n'.join(res) + '\n')
print(f'{fam}: {n} файлов в {out}/, правила добавлены в {css_path}. Подключение: <link rel="stylesheet" href="{css_path.as_posix()}">')
if not any(s.startswith('cyrillic') for s, _ in blocks): print('  ВНИМАНИЕ: у шрифта нет кириллицы')
