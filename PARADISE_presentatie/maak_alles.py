# -*- coding: utf-8 -*-
"""Bouwt alle decks in één keer.

Dezelfde inhoud, elk zijn eigen publiek. Elke dia in inhoud.py draagt een label
`voor` met de letters van de decks waarin hij hoort; maak_pptx.py filtert daarop.

De lijst komt uit DECKS zelf en staat hier niet meer getypt: een nieuw deck
werd anders wel aangemaakt maar nooit meegebouwd.

Een deck dat na de laatste broncodewijziging nog met de hand is aangepast,
wordt overgeslagen in plaats van overschreven. Wil u het toch opnieuw bouwen:
`python maak_alles.py --overschrijf`.
"""
import os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from inhoud import DECKS

HIER = os.path.dirname(os.path.abspath(__file__))
EXTRA = ['--overschrijf'] if '--overschrijf' in sys.argv else []

print('%-11s %-46s %s' % ('DECK', 'BESTAND', 'DUUR'))
print('-' * 84)
handwerk, open_ = [], []
for naam in DECKS:
    r = subprocess.run([sys.executable, os.path.join(HIER, 'maak_pptx.py'), naam]
                       + EXTRA,
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    if r.returncode:
        fout = r.stderr.strip()
        if 'staat open in PowerPoint' in fout:
            print('%-11s OVERGESLAGEN — staat open in PowerPoint' % naam)
            open_.append(naam)
        elif 'met de' in fout and 'hand' in fout:
            print('%-11s OVERGESLAGEN — met de hand aangepast' % naam)
            handwerk.append(naam)
        else:
            print('%-11s MISLUKT' % naam)
            print(fout[-800:])
        continue
    regel = r.stdout.strip().splitlines()[-1]
    aantal = regel.split(" dia's")[0]
    print('%-11s %-46s %-14s %s dia\'s'
          % (naam, DECKS[naam]['bestand'], DECKS[naam]['duur'], aantal))

print()
if open_:
    print('Staat open in PowerPoint, dus niet gebouwd: %s.' % ', '.join(open_))
    print('Sluit het daar en draai dit script opnieuw.')
    print()
if handwerk:
    print('Sinds de laatste bouw met de hand gewijzigd: %s.' % ', '.join(handwerk))
    print('Zet die wijzigingen in inhoud.py, of bouw met --overschrijf.')
    print('De vorige versies staan hoe dan ook in vorige\\.')
    print()
print('De decks openen op dezelfde titeldia met een eigen ondertitel; alleen')
print('Kortrijk Kerngezond heeft een eigen opening, met de drukmat als beeld.')
print('Aanpassen wie welke dia krijgt: het veld voor= bij de dia in inhoud.py.')
