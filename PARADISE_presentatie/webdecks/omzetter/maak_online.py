"""Bouwt de online versies van Theorie en Technologie: de PowerPoint uit bouw.py, icoontjes per toestel, cameo op elke dia.

    python maak_online.py [theorie] [tech]        (zonder sleutels: beide)

Eerst meet.py en gif.py draaien, in PowerShell op de voorgrond (zie maak_alle.py). De bron is bronnen/<sleutel>/project,
met de correcties van 4 november 2026: die staan niet in de webversie, dus niet opnieuw ophalen.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

import cameo
import iconen

HIER = Path(__file__).parent
DOEL = HIER.parent
# sleutel: uitvoer, icoontjes die de tekst niet verraadt of die alleen in het voorbijgaan vallen, slotdia met grote cameo
DECKS = {
    'theorie': ('PARADISE_theorie_online_cameo.pptx',
                {14: '-N', 33: '+N', 34: '+N', 35: '+N', 45: '+N', 46: '+M', 60: '+N', 62: '+NO', 71: '+N'}, 78),
    'tech': ('PARADISE_technologie_online_cameo.pptx',
             {27: '+N', 42: '-N', 47: '+O', 48: '+M', 56: '+O', 59: '+N', 60: '+N', 61: '+N', 62: '+N', 64: '+M', 65: '+N'}, 66),
}

for sleutel in sys.argv[1:] or DECKS:
    naam, extra, slot = DECKS[sleutel]
    with tempfile.TemporaryDirectory() as klad:
        basis, tussen = Path(klad) / 'basis.pptx', Path(klad) / 'iconen.pptx'
        subprocess.run([sys.executable, 'bouw.py', HIER / 'bronnen' / sleutel, HIER / 'werk' / sleutel, sleutel, basis],
                       cwd=HIER, check=True, capture_output=True)
        iconen.zet(basis, tussen, extra, {slot: 1792})
        cameo.main(tussen, DOEL / naam, {slot: (1372, 280, 420)})
