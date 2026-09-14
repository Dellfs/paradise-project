# -*- coding: utf-8 -*-
"""Bouwt alle decks in één keer.

Dezelfde inhoud, elk zijn eigen publiek. Elke dia in inhoud.py draagt een label
`voor` met de letters van de decks waarin hij hoort; maak_pptx.py filtert daarop.

De lijst komt uit DECKS zelf en staat hier niet meer getypt: een nieuw deck
werd anders wel aangemaakt maar nooit meegebouwd.
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inhoud import DECKS

HIER = os.path.dirname(os.path.abspath(__file__))

print('%-11s %-46s %s' % ('DECK', 'BESTAND', 'DUUR'))
print('-' * 84)
for naam in DECKS:
    r = subprocess.run([sys.executable, os.path.join(HIER, 'maak_pptx.py'), naam],
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    if r.returncode:
        print('%-11s MISLUKT' % naam)
        print(r.stderr.strip()[-800:])
        continue
    regel = r.stdout.strip().splitlines()[-1]
    aantal = regel.split(" dia's")[0]
    print('%-11s %-46s %-14s %s dia\'s'
          % (naam, DECKS[naam]['bestand'], DECKS[naam]['duur'], aantal))

print()
print('De decks openen op dezelfde titeldia met een eigen ondertitel; alleen')
print('Kortrijk Kerngezond heeft een eigen opening, met de drukmat als beeld.')
print('Aanpassen wie welke dia krijgt: het veld voor= bij de dia in inhoud.py.')
