"""Meet elke dia van een Slides-deck in de browser en schrijft wat PowerPoint nodig heeft.

    python meet.py <deckmap met project/> <werkmap> [dia-id ...]

Per dia: <werkmap>/meting/NN_id.json (tekst, vormen, tabellen, beelden, grafiekvakken, notities),
<werkmap>/achtergrond/NN_id.png als de dia verlopen of svg-decor heeft, en <werkmap>/embeds/id_k.html
voor elke canvas-animatie. Edge rekent de opmaak uit (--dump-dom), dus de posities zijn die van de browser.
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
BLOBS = Path(__file__).parent / 'blobs'
DECK, WERK = Path(sys.argv[1]), Path(sys.argv[2])
KEUZE = set(sys.argv[3:])
for sub in ('meting', 'achtergrond', 'embeds', 'paginas', 'export', 'vergelijk', 'gif'):
    (WERK / sub).mkdir(parents=True, exist_ok=True)
    if not KEUZE:
        # volledige run: bestanden van een vorige volgorde (andere nummering) opruimen
        for oud in (WERK / sub).iterdir():
            if oud.is_file():
                oud.unlink()

KOP = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
html,body{margin:0;background:#222}
section{position:relative;width:1920px;height:1080px;box-sizing:border-box;overflow:hidden}
section *{box-sizing:border-box}
section p,section h1,section h2,section h3,section table{margin:0}
aside{display:none} section ul{margin:0;padding-left:1.1em} section li{margin:0 0 6px 0}
table{border-collapse:collapse}
td,th{padding:.35em .6em;border:1px solid #21507A}
x-connector{display:block;height:0;border-top:3px solid currentColor}
</style></head><body>"""

METEN = r"""<pre id="meting" style="display:none"></pre><script>
(async function(){
await document.fonts.ready;
const MODUS='__MODUS__';
const S=document.querySelector('section'),R0=S.getBoundingClientRect();
const INL=new Set(['B','STRONG','I','EM','SPAN','A','BR','SUP','SUB','SMALL','U','CODE','MARK','S']);
function kl(c){const m=(c||'').match(/rgba?\(([^)]+)\)/);if(!m)return null;const p=m[1].split(/[\s,\/]+/).filter(Boolean).map(parseFloat);
 const a=p.length>3?p[3]:1;if(a===0)return null;return{hex:p.slice(0,3).map(v=>Math.round(v).toString(16).padStart(2,'0')).join(''),a:a}}
function rc(el){const r=el.getBoundingClientRect();return{x:r.left-R0.left,y:r.top-R0.top,w:r.width,h:r.height}}
function px(v){return parseFloat(v)||0}
function st(el){const cs=getComputedStyle(el);return{f:cs.fontFamily.split(',')[0].replace(/["']/g,'').trim(),s:px(cs.fontSize),
 b:parseInt(cs.fontWeight)||400,i:cs.fontStyle==='italic',c:kl(cs.color),ls:cs.letterSpacing==='normal'?0:px(cs.letterSpacing),tt:cs.textTransform,
 sw:px(cs.webkitTextStrokeWidth),sc:kl(cs.webkitTextStrokeColor)}}
function isInl(c){return INL.has(c.tagName)||(getComputedStyle(c).display.startsWith('inline')&&c.tagName!=='IMG'&&!(c.dataset&&c.dataset.embed!==undefined))}
function tekstblok(el){if(!el.textContent.trim())return false;for(const c of el.children){if(!isInl(c))return false}return true}
function runs(el,uit,basis){for(const n of el.childNodes){if(n.nodeType===3){uit.push(Object.assign({t:n.textContent},basis))}
 else if(n.nodeType===1){if(n.tagName==='BR')uit.push(Object.assign({t:'\n'},basis));else runs(n,uit,st(n))}}return uit}
function inh(cs,r){const l=px(cs.paddingLeft)+px(cs.borderLeftWidth),t=px(cs.paddingTop)+px(cs.borderTopWidth),
 rr=px(cs.paddingRight)+px(cs.borderRightWidth),b=px(cs.paddingBottom)+px(cs.borderBottomWidth);return{x:r.x+l,y:r.y+t,w:r.w-l-rr,h:r.h-t-b}}
const items=[];let raster=0;
function vorm(el,cs,r){const bg=kl(cs.backgroundColor);if(cs.backgroundImage!=='none'){raster++;el.dataset.raster='1'}
 const zij=['Top','Right','Bottom','Left'];const bw=zij.map(z=>cs['border'+z+'Style']==='none'?0:px(cs['border'+z+'Width']));
 const bc=zij.map(z=>kl(cs['border'+z+'Color']));const bs=zij.map(z=>cs['border'+z+'Style']);
 if(bg||bw.some((w,i)=>w>0&&bc[i]))items.push({type:'box',...r,bg,bw,bc,bs,
  rad:[px(cs.borderTopLeftRadius),px(cs.borderTopRightRadius),px(cs.borderBottomRightRadius),px(cs.borderBottomLeftRadius)],
  rot:cs.transform!=='none'?cs.transform:null,ow:el.offsetWidth,oh:el.offsetHeight,op:parseFloat(cs.opacity)})}
function tabel(t){const rows=[];for(const tr of t.rows){const cel=[];const trbg=kl(getComputedStyle(tr).backgroundColor);
 for(const td of tr.cells){const cs=getComputedStyle(td);cel.push({...rc(td),bg:kl(cs.backgroundColor)||trbg,runs:runs(td,[],st(td)),
  al:cs.textAlign,pad:[px(cs.paddingTop),px(cs.paddingRight),px(cs.paddingBottom),px(cs.paddingLeft)],
  bc:kl(cs.borderTopColor),bw:px(cs.borderTopWidth),va:cs.verticalAlign,lh:cs.lineHeight==='normal'?null:px(cs.lineHeight),cs:td.colSpan,rs:td.rowSpan})}
 rows.push(cel)}const cs=getComputedStyle(t);items.push({type:'table',...rc(t),rows,bc:kl(cs.borderTopColor),bw:px(cs.borderTopWidth)})}
function loop(el){const cs=getComputedStyle(el);if(cs.display==='none'||cs.visibility==='hidden')return;const tag=el.tagName.toUpperCase();
 if(['ASIDE','PRE','SCRIPT','STYLE'].includes(tag))return;const r=rc(el);
 if(tag==='IMG'){if(r.w>0&&r.h>0)items.push({type:'img',...r,src:el.getAttribute('src'),fit:cs.objectFit});return}
 if(el.dataset&&el.dataset.embed!==undefined){items.push({type:'embed',...r,k:+el.dataset.embed});return}
 if(tag==='X-CONNECTOR'){const at=n=>el.getAttribute(n);items.push({type:'line',...r,c:kl(cs.color)||kl(cs.borderTopColor),lw:px(cs.borderTopWidth),
  x1:at('x1'),y1:at('y1'),x2:at('x2'),y2:at('y2'),route:at('route'),head:at('head')});return}
 if(el instanceof SVGElement){raster++;el.dataset.raster='1';items.push({type:'raster',...r});return}
 if(r.w<=0||r.h<=0)return;
 if(tag==='TABLE'){tabel(el);return}
 vorm(el,cs,r);
 if(tekstblok(el)){items.push({type:'text',...inh(cs,r),runs:runs(el,[],st(el)),al:cs.textAlign,lh:cs.lineHeight==='normal'?null:px(cs.lineHeight),
  ws:cs.whiteSpace,op:parseFloat(cs.opacity)});return}
 for(const c of el.children)loop(c)}
for(const c of S.children)loop(c);
if(MODUS==='achtergrond'){for(const e of S.querySelectorAll('*'))e.style.visibility='hidden';
 for(const e of S.querySelectorAll('[data-raster], [data-raster] *'))e.style.visibility='visible';document.body.dataset.klaar='1';return}
const a=S.querySelector('aside');
document.getElementById('meting').textContent=JSON.stringify({bg:kl(getComputedStyle(S).backgroundColor),items,raster,
 notes:a?a.textContent.replace(/\s+/g,' ').trim():''});
})();
</script>"""


def blob_uri(m):
    p = BLOBS / f'{m.group(1)}.png'
    return p.as_uri() if p.exists() else m.group(0)


def edge(*args, timeout=120):
    return subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1920,1080',
                           '--virtual-time-budget=8000', *args], capture_output=True, timeout=timeout)


deck = json.loads((DECK / 'project' / 'deck.json').read_text(encoding='utf-8'))
for i, sid in enumerate(deck['order'], 1):
    if KEUZE and sid not in KEUZE:
        continue
    naam = f'{i:02d}_{sid}'
    s = (DECK / 'project' / 'slides' / f'{sid}.html').read_text(encoding='utf-8')
    embeds = []

    def vervang(m):
        embeds.append((m.group(1), m.group(2)))
        return f'<div data-embed="{len(embeds) - 1}" style="{m.group(1)}"></div>'

    s = re.sub(r'<x-embed style="([^"]*)">(.*?)</x-embed>', vervang, s, flags=re.S)
    s = re.sub(r'/_blob/([0-9a-f]{32})', blob_uri, s)
    for k, (stijl, inhoud) in enumerate(embeds):
        (WERK / 'embeds' / f'{sid}_{k}.html').write_text(inhoud, encoding='utf-8')
    for modus in ('meten', 'achtergrond'):
        (WERK / 'paginas' / f'{naam}_{modus}.html').write_text(
            KOP + s + METEN.replace('__MODUS__', modus) + '</body></html>', encoding='utf-8')
    uit = edge('--dump-dom', (WERK / 'paginas' / f'{naam}_meten.html').as_uri()).stdout.decode('utf-8', 'replace')
    m = re.search(r'<pre id="meting"[^>]*>(.*?)</pre>', uit, flags=re.S)
    if not m or not m.group(1).strip():
        print(f'{naam}: GEEN METING')
        continue
    meting = json.loads(html.unescape(m.group(1)))
    meting['embeds'] = [st for st, _ in embeds]
    (WERK / 'meting' / f'{naam}.json').write_text(json.dumps(meting, ensure_ascii=False, indent=1), encoding='utf-8')
    if meting['raster']:
        edge(f'--screenshot={WERK / "achtergrond" / (naam + ".png")}', (WERK / 'paginas' / f'{naam}_achtergrond.html').as_uri())
    soorten = {}
    for it in meting['items']:
        soorten[it['type']] = soorten.get(it['type'], 0) + 1
    print(naam, soorten, 'raster' if meting['raster'] else '')
