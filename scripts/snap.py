import sys,asyncio
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
OUT=sys.argv[1];TS=[float(x) for x in sys.argv[2:]]
async def main():
    O=Path(OUT);O.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--ignore-gpu-blocklist','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1920,'height':1080})
        pg.on('pageerror',lambda e:print('PAGEERR',e));pg.on('console',lambda m:print('CON',m.text) if m.type=='error' else None)
        await pg.goto(Path('film.html').resolve().as_uri());await pg.evaluate('window.READY')
        for t in TS:
            await pg.evaluate(f'seek({t})');await pg.screenshot(path=str(O/f'{t:06.2f}.jpg'),type='jpeg',quality=85)
        await b.close()
    fs=[O/f'{t:06.2f}.jpg' for t in TS];im0=Image.open(fs[0]);c=4 if im0.width>=im0.height else 6;w=480 if im0.width>=im0.height else 270;h=round(w*im0.height/im0.width);r=(len(fs)+c-1)//c
    S=Image.new('RGB',(c*(w+4),r*(h+4)),'#444')
    for i,f in enumerate(fs):S.paste(Image.open(f).resize((w,h)),(i%c*(w+4),i//c*(h+4)))
    S.save(f'{OUT}_sheet.jpg',quality=88)
asyncio.run(main())
