# -*- coding: utf-8 -*-
"""Snijdt de toestelfoto's bij tot wat bruikbaar is op een donkere dia.

De bronbestanden staan in de hoofdmap van de site. Deze stap draait één keer;
het resultaat komt in beeld/ en wordt door maak_pptx.py ingevoegd.
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image

HIER = os.path.dirname(os.path.abspath(__file__))
BRON = os.path.dirname(HIER)
UIT = os.path.join(HIER, 'beeld')
os.makedirs(UIT, exist_ok=True)


def bewaar(im, naam):
    pad = os.path.join(UIT, naam)
    im.save(pad)
    print('%-22s %s' % (naam, im.size))
    return pad


# pedar: transparante productrender, kan zo op de donkere achtergrond
im = Image.open(os.path.join(BRON, 'pedar-system.png')).convert('RGBA')
bewaar(im.crop(im.getbbox()), 'pedar.png')

# orthotimer: enkel de onderste foto — de reader met de sensoren, donkere tafel
im = Image.open(os.path.join(BRON, 'content_products-orthotimer_en.webp')).convert('RGB')
bewaar(im.crop((110, 770, 1990, 1470)), 'orthotimer.png')

# MoveMonitor: witte achtergrond, komt op een lichte tegel te staan
im = Image.open(os.path.join(BRON, 'mcroberts.jpg')).convert('RGB')
bewaar(im.crop((14, 10, 285, 160)), 'movemonitor.png')
