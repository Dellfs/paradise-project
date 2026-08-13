# -*- coding: utf-8 -*-
"""Snijdt de toestelfoto's bij tot wat bruikbaar is op een donkere dia.

De bronbestanden staan in de hoofdmap van de site. Deze stap draait één keer;
het resultaat komt in beeld/ en wordt door maak_pptx.py ingevoegd.
"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image, ImageChops

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

# Het merk: de voetafdruk uit het logo. De slagschaduw is lichtgrijs en zou op
# een donkere dia als een vlek oplichten. We wissen hem van de rand naar binnen
# toe: alles wat vanaf de beeldrand bereikbaar is zonder een verzadigde kleur te
# passeren, hoort niet bij het merk. Zo blijven de lichtvlekken bínnen de vorm
# wel staan.
im = Image.open(os.path.join(BRON, 'logo_transparent.png')).convert('RGBA')
pix = im.load()
bw, bh = im.size


def vaal(x, y):
    r, g, b, a = pix[x, y]
    return a == 0 or max(r, g, b) - min(r, g, b) < 60


stapel = [(x, y) for x in range(bw) for y in (0, bh - 1) if vaal(x, y)]
stapel += [(x, y) for y in range(bh) for x in (0, bw - 1) if vaal(x, y)]
gezien = set(stapel)
while stapel:
    x, y = stapel.pop()
    r, g, b, _ = pix[x, y]
    pix[x, y] = (r, g, b, 0)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < bw and 0 <= ny < bh and (nx, ny) not in gezien and vaal(nx, ny):
            gezien.add((nx, ny))
            stapel.append((nx, ny))
bewaar(im.crop(im.getbbox()), 'merk.png')


# Duotoon: grijswaarden omzetten naar de blauwfamilie van de huisstijl, zodat
# een foto die aflopend over de dia ligt bij het palet hoort in plaats van
# ertegen te vloeken.
def duotoon(bron, donker=(0x04, 0x18, 0x2A), licht=(0x8F, 0xD6, 0xF5)):
    g = bron.convert('L')
    lut = []
    for kanaal in range(3):
        lut += [int(round(donker[kanaal] + (licht[kanaal] - donker[kanaal]) * i / 255.0))
                for i in range(256)]
    return Image.merge('RGB', (g, g, g)).point(lut)


im = Image.open(os.path.join(BRON, 'content_products-orthotimer_en.webp')).convert('RGB')
bewaar(duotoon(im.crop((110, 800, 1990, 1460))), 'sensor_vol.png')

# Portret voor de contactdia, bijgesneden op de verhouding van het vak zodat
# er niets hoeft te worden opgerekt.
im = Image.open(os.path.join(BRON, 'janou.jpeg')).convert('RGB')
bewaar(im.crop((0, 46, 1024, 1369)), 'janou.png')


# De instellingslogo's staan op wit met donkerblauwe letters. Ze op de donkere
# dia leggen zou ze onleesbaar maken en hun huisstijl schenden, dus ze komen in
# een wit vlak. Hier zetten we ze plat op wit en snijden we de witrand weg.
def op_wit(bron):
    im = Image.open(bron).convert('RGBA')
    vlak = Image.new('RGBA', im.size, (255, 255, 255, 255))
    vlak.alpha_composite(im)
    vlak = vlak.convert('RGB')
    # witrand wegsnijden: alles wat van zuiver wit afwijkt hoort bij het merk
    verschil = ImageChops.invert(vlak)
    kader = verschil.getbbox()
    return vlak.crop(kader) if kader else vlak


bewaar(op_wit(os.path.join(BRON, 'kuleuven-brugge.png')), 'kuleuven.png')
bewaar(op_wit(os.path.join(BRON, 'Vrije_Universiteit_Brussel_logo.svg.webp')), 'vub.png')
