# -*- coding: utf-8 -*-
"""Maakt stockfoto's klaar voor het deck.

Zet uw gedownloade Adobe-foto's in beeld\\stock\\ en draai dit script. Van elke
foto komen er twee versies in beeld\\:

  <naam>_kleur.png    bijgesneden op de kaderverhouding, echte kleuren
  <naam>_duo.png      idem, maar omgezet naar de blauwfamilie van de huisstijl

Gebruik de kleurversie voor instructiebeeld waar de kleur informatie draagt —
de groene Orthotimer-sensor, een rode huidzone. Gebruik de duotoonversie voor
sfeerbeeld dat aflopend of als achtergrond gebruikt wordt; die valt dan niet uit
de toon van de rest van het deck.
"""
import io, os, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from PIL import Image, ImageOps

HIER = os.path.dirname(os.path.abspath(__file__))
STOCK = os.path.join(HIER, 'beeld', 'stock')
UIT = os.path.join(HIER, 'beeld')
os.makedirs(STOCK, exist_ok=True)

# Verhouding van het fotokader op de stapdia's: 700 bij 440 eenheden.
VERHOUDING = 700 / 440.0
BREED = 1600

DONKER = (0x04, 0x18, 0x2A)
LICHT = (0x9E, 0xD9, 0xF5)


def duotoon(bron):
    """Grijswaarden omzetten naar de blauwfamilie, zodat de foto bij het palet hoort."""
    g = bron.convert('L')
    lut = []
    for kanaal in range(3):
        lut += [int(round(DONKER[kanaal] +
                          (LICHT[kanaal] - DONKER[kanaal]) * i / 255.0))
                for i in range(256)]
    return Image.merge('RGB', (g, g, g)).point(lut)


bronnen = [p for p in sorted(glob.glob(os.path.join(STOCK, '*')))
           if os.path.splitext(p)[1].lower() in
           ('.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff')]

if not bronnen:
    print('Geen foto\'s gevonden in %s' % STOCK)
    print('Zet uw Adobe-downloads daar neer en draai dit script opnieuw.')
    raise SystemExit

for p in bronnen:
    naam = os.path.splitext(os.path.basename(p))[0]
    naam = ''.join(c if c.isalnum() or c in '-_' else '_' for c in naam)[:40]
    im = Image.open(p)
    im = ImageOps.exif_transpose(im).convert('RGB')
    # bijsnijden op de kaderverhouding, vanuit het midden
    im = ImageOps.fit(im, (BREED, int(round(BREED / VERHOUDING))),
                      method=Image.LANCZOS, centering=(0.5, 0.45))
    im.save(os.path.join(UIT, naam + '_kleur.png'))
    duotoon(im).save(os.path.join(UIT, naam + '_duo.png'))
    print('%-34s -> %s_kleur.png en %s_duo.png' % (os.path.basename(p), naam, naam))

print()
print('Klaar. Vervangen in PowerPoint: rechtsklik op het kader, Afbeelding')
print('wijzigen, en kies het bestand. Kader en uitsnede blijven behouden.')
