"""Zet per dia het webdeck (boven) en de PowerPoint-export (onder) op één beeld.

    python vergelijk.py <werkmap> [dianummers]

Het webbeeld is een Edge-schermafdruk van <werkmap>/paginas/NN_id_meten.html met de canvas als GIF-eindbeeld
(de grafiekvakken blijven daar leeg; het gaat om tekst en vormen). Uitvoer: <werkmap>/vergelijk/NN.png.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
WERK = Path(sys.argv[1])
KIES = {int(x) for x in sys.argv[2:]}
(WERK / 'vergelijk').mkdir(exist_ok=True)
for pagina in sorted((WERK / 'paginas').glob('*_meten.html')):
    nr = int(pagina.name[:2])
    if KIES and nr not in KIES:
        continue
    web = WERK / 'vergelijk' / f'web{nr:02d}.png'
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--window-size=1920,1080',
                    '--virtual-time-budget=5000', f'--screenshot={web}', pagina.as_uri()], capture_output=True, timeout=120)
    ppt = WERK / 'export' / f'dia{nr:02d}.png'
    if not (web.exists() and ppt.exists()):
        continue
    a, b = Image.open(web).convert('RGB').resize((960, 540)), Image.open(ppt).convert('RGB').resize((960, 540))
    blad = Image.new('RGB', (960, 1090), 'white')
    blad.paste(a, (0, 0))
    blad.paste(b, (0, 550))
    blad.save(WERK / 'vergelijk' / f'{nr:02d}.png')
    print(nr, 'ok')
