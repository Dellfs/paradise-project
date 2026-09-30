"""Zet de vijf webdecks om naar PowerPoint: meten, animaties opnemen, bouwen, en ter controle exporteren.

    python maak_alle.py [--bouw] [sleutel ...]        (zonder sleutels: alle vijf; --bouw: alleen opnieuw bouwen)

Bronnen: haal per deck de map `project/` van het Slides-artifact op (deck.json en slides/*.html) naar
bronnen/<sleutel>/project/, en de beelden (/_blob/<id>) als <id>.png naar blobs/. Werkbestanden komen in
werk/<sleutel>/; bronnen/, blobs/ en werk/ blijven buiten git. De PowerPoints komen in de map erboven.
"""
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).parent
DOEL = HIER.parent
DECKS = {
    'dfc': 'PARADISE_voetklinieken_12okt.pptx',
    'rekrutering': 'PARADISE_rekrutering_per_centrum.pptx',
    'tachtig': 'PARADISE_80_procent_van_wat.pptx',
    'theorie': 'PARADISE_theorie_en_protocol.pptx',
    'tech': 'PARADISE_technische_instrumenten.pptx',
}


def stap(*cmd):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=HIER)
    fouten = [l for l in (r.stdout + r.stderr).splitlines() if any(w in l for w in ('GEEN', 'ontbreekt', 'Error', 'Traceback', 'geen'))]
    if r.returncode or fouten:
        print('   ', ' '.join(str(c) for c in cmd[:2]), '->', r.returncode)
        print('    ' + '\n    '.join((fouten or (r.stdout + r.stderr).splitlines())[-12:]))
    return r


DOEL.mkdir(parents=True, exist_ok=True)
ALLEEN_BOUW = '--bouw' in sys.argv
for sleutel in ([a for a in sys.argv[1:] if not a.startswith('--')] or DECKS):
    deck, naam = HIER / 'bronnen' / sleutel, DECKS[sleutel]
    werk = HIER / 'werk' / sleutel
    print(f'== {sleutel}', flush=True)
    if not ALLEEN_BOUW:
        stap(sys.executable, 'meet.py', deck, werk)
        stap(sys.executable, 'gif.py', werk)
    uit = DOEL / naam
    r = stap(sys.executable, 'bouw.py', deck, werk, sleutel, uit)
    print('   ', r.stdout.strip().splitlines()[-1] if r.stdout.strip() else 'geen uitvoer')
    stap('powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', HIER / 'exporteer.ps1', uit, werk / 'export')
    stap(sys.executable, 'vergelijk.py', werk)
    print(f'    {uit.stat().st_size // 1024} kB', flush=True)
