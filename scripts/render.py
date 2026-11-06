# python render.py <папка> <с_сек> <по_сек> [fps=60] [sub=2]
import sys,asyncio
from pathlib import Path
from playwright.async_api import async_playwright
OUT=Path(sys.argv[1]);T0,T1=float(sys.argv[2]),float(sys.argv[3]);FPS=int(sys.argv[4]) if len(sys.argv)>4 else 60;SUB=int(sys.argv[5]) if len(sys.argv)>5 else 2
OUT.mkdir(exist_ok=True);A,B=int(T0*FPS*SUB),int(T1*FPS*SUB);W=6
subT=lambda i:max(0,(i//SUB)/FPS+((i%SUB)-(SUB-1)/2)/(FPS*SUB))
async def worker(pw,q):
    b=await pw.chromium.launch(args=['--ignore-gpu-blocklist','--use-angle=swiftshader','--enable-unsafe-swiftshader']);pg=await b.new_page(viewport={'width':1920,'height':1080})
    pg.on('pageerror',lambda e:print('PAGEERR',e,flush=True))
    await pg.goto(Path('film.html').resolve().as_uri());await pg.evaluate('window.READY')
    for i in q:
        f=OUT/f's{i:05d}.jpg'
        if f.exists() and f.stat().st_size>1000:continue
        await pg.evaluate(f'seek({subT(i)})');await pg.screenshot(path=str(f),type='jpeg',quality=94)
    await b.close()
async def main():
    async with async_playwright() as pw:
        await asyncio.gather(*[worker(pw,range(A+k,B,W)) for k in range(W)])
asyncio.run(main());print('кадры готовы',A,B,flush=True)
