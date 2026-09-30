"""Neemt elke canvas-animatie beeld per beeld op en maakt er een GIF van.

    python gif.py <werkmap> [embed-naam ...]      (embed-naam = bestandsnaam zonder .html, bv. tempo_0)

De klok van de pagina wordt vervangen door een virtuele klok: performance.now, Date.now, requestAnimationFrame,
setTimeout en IntersectionObserver lopen op onze stappen. Zo is elk beeld scherp en even ver als in de browser.
Een animatie die stopt, speelt één keer; een animatie die blijft lopen (simulaties) wordt een lus van MAX seconden.
"""
import base64
import html
import io
import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
WERK = Path(sys.argv[1])
KEUZE = set(sys.argv[2:])
SCHAAL, FPS, MAX = 1.5, 15, 12

KLOK = r"""<script>(function(){const echt=window.setTimeout.bind(window);window.__echt=echt;let nu=0,id=0;const q=new Map(),tm=[];
performance.now=()=>nu;const D0=Date.now();Date.now=()=>D0+nu;
window.requestAnimationFrame=cb=>{id++;q.set(id,cb);return id};window.cancelAnimationFrame=i=>q.delete(i);
window.setTimeout=(cb,ms)=>{id++;tm.push({t:nu+(+ms||0),cb,id});return id};window.clearTimeout=i=>{const k=tm.findIndex(x=>x.id===i);if(k>=0)tm.splice(k,1)};
window.setInterval=()=>0;
window.IntersectionObserver=class{constructor(cb){this.cb=cb}observe(el){tm.push({t:0,cb:()=>this.cb([{isIntersecting:true,target:el}]),id:-1})}unobserve(){}disconnect(){}};
window.__stap=ms=>{nu+=ms;const nu_=nu;const due=tm.filter(x=>x.t<=nu_);for(const x of due)tm.splice(tm.indexOf(x),1);due.forEach(x=>x.cb());
 const b=[...q.values()];q.clear();b.forEach(cb=>cb(nu));return q.size>0||tm.length>0};
})();</script>"""

OPNAME = r"""<pre id="beelden" style="display:none"></pre><script>(function(){
__echt(async()=>{await document.fonts.ready;const c=document.querySelector('canvas');const f=[];
 // een lus met een vaste periode (const TOT in de grafiek) wordt precies één periode lang opgenomen: naadloos herhalen
 let P=null;try{P=(typeof TOT!=='undefined'&&TOT>0&&TOT<20000)?TOT:null}catch(e){}
 const N=P?Math.round(P/1000*__FPS__)-1:__MAX__*__FPS__;const beeld=()=>f.push(c.toDataURL('image/webp',0.92));
 __stap(0);__stap(0);beeld();let actief=true,n=0;
 while(n<N){actief=__stap(1000/__FPS__);beeld();n++;if(!actief)break}
 document.getElementById('beelden').textContent=JSON.stringify({klaar:!actief,periode:P,beelden:f});},200)})();</script>"""


def neem_op(bron: Path, doel: Path):
    inhoud = bron.read_text(encoding='utf-8')
    pagina = bron.with_suffix('.opname.html')
    pagina.write_text('<!doctype html><html><head><meta charset="utf-8">' + KLOK + '</head><body style="margin:0">' + inhoud
                      + OPNAME.replace('__MAX__', str(MAX)).replace('__FPS__', str(FPS)) + '</body></html>', encoding='utf-8')
    uit = subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--force-device-scale-factor={SCHAAL}',
                          '--window-size=1920,1200', '--virtual-time-budget=30000', '--dump-dom', pagina.as_uri()],
                         capture_output=True, timeout=600).stdout.decode('utf-8', 'replace')
    m = re.search(r'<pre id="beelden"[^>]*>(.*?)</pre>', uit, flags=re.S)
    if not m or not m.group(1).strip():
        print(f'{bron.stem}: GEEN BEELDEN')
        return None
    data = json.loads(html.unescape(m.group(1)))
    beelden = [Image.open(io.BytesIO(base64.b64decode(b.split(',', 1)[1]))).convert('RGB') for b in data['beelden']]
    # dubbele beelden aan het eind weglaten (stilstand) en één gedeeld palet, zonder dithering: vlakke kleuren blijven vlak
    while data['klaar'] and len(beelden) > 2 and beelden[-1].tobytes() == beelden[-2].tobytes():
        beelden.pop()
    palet = beelden[-1].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    p = [b.quantize(palette=palet, dither=Image.Dither.NONE) for b in beelden]
    extra = {} if data['klaar'] else {'loop': 0}
    p[0].save(doel, save_all=True, append_images=p[1:], duration=round(1000 / FPS), optimize=True, **extra)
    lus = 'één keer' if data['klaar'] else (f"lus van {data['periode'] / 1000:.1f} s" if data.get('periode') else 'lus')
    print(f'{bron.stem}: {len(p)} beelden, {lus}, {doel.stat().st_size // 1024} kB, '
          f'{beelden[0].width}x{beelden[0].height}')
    return data['klaar']


(WERK / 'gif').mkdir(exist_ok=True)
for bron in sorted((WERK / 'embeds').glob('*.html')):
    if bron.name.endswith('.opname.html') or (KEUZE and bron.stem not in KEUZE):
        continue
    neem_op(bron, WERK / 'gif' / f'{bron.stem}.gif')
