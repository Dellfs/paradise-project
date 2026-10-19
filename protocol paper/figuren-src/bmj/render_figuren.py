"""Render FigureN.svg to TIFF (about 600 dpi at 17 cm, LZW) and a small PNG preview, with headless Edge.

usage: python -X utf8 render.py <svg dir> <tiff out dir> <preview dir> [figure numbers...]
"""
import sys, os, re, subprocess
from PIL import Image

SVG, OUT, PREV = sys.argv[1:4]
WANT = [int(a) for a in sys.argv[4:]] or [1, 2, 3, 4, 5]
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
SCALE = 4
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREV, exist_ok=True)
for n in WANT:
    svg = os.path.join(SVG, 'Figure%d.svg' % n)
    s = open(svg, encoding='utf-8').read()
    w, h = [float(v) for v in re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s).groups()]
    html = svg + '.html'
    open(html, 'w', encoding='utf-8').write(
        '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#fff}'
        'img{display:block;width:%dpx;height:%dpx}</style></head><body><img src="%s"></body></html>'
        % (w, h, os.path.basename(svg)))
    png = os.path.join(PREV, 'Figure%d_full.png' % n)
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=%d' % SCALE,
                    '--window-size=%d,%d' % (round(w), round(h)), '--screenshot=' + png, 'file:///' + html.replace('\\', '/')],
                   check=True, capture_output=True, timeout=120)
    im = Image.open(png).convert('RGB')
    im.save(os.path.join(OUT, 'Figure%d.tif' % n), compression='tiff_lzw', dpi=(600, 600))
    im.resize((1300, round(1300 * im.size[1] / im.size[0])), Image.LANCZOS).save(os.path.join(PREV, 'Figure%d.png' % n))
    print('Figure%d' % n, im.size)
