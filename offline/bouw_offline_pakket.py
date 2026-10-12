# -*- coding: utf-8 -*-
"""Bouwt het offline pakket 'PARADISE Therapietrouw' voor de laptops van de centra.

Waarom: de tool Therapietrouw van het ledenportaal (therapietrouw.html: stap 1 MoveMonitor,
waaktijd en norm; stap 2 Orthotimer, het therapietrouwblad) moet ook werken als de site of
het netwerk in het ziekenhuis wegvalt. Een .exe loopt op ziekenhuislaptops vaak vast op de
IT-beveiliging; een HTML-bestand dat in Edge opent, vraagt geen installatie en geen
beheerdersrechten.

Wat het doet: het neemt therapietrouw.html ONGEWIJZIGD over en maakt het zelfstandig:
de huisstijl (styles/tokens.css), pdf.js, de pdf.js-worker, JSZip en het logo gaan in het
bestand zelf, en het portaalslot en de knop terug naar de visite-checklist vallen weg.
De rekenregels blijven die van de site; pas ze daar aan en bouw dit pakket daarna opnieuw.

Gebruik (vanuit de hoofdmap van de site):
    python offline/bouw_offline_pakket.py

Uitvoer:
    offline/PARADISE_Therapietrouw/PARADISE_Therapietrouw.html
    offline/PARADISE_Therapietrouw/PARADISE Therapietrouw starten.cmd
    offline/PARADISE_Therapietrouw/LEES MIJ.txt
    offline/PARADISE_Therapietrouw_offline.zip
"""

import base64
import datetime
import io
import os
import re
import zipfile

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAAM = 'PARADISE_Therapietrouw'
UIT = os.path.join(SITE, 'offline', NAAM)
ZIP = os.path.join(SITE, 'offline', NAAM + '_offline.zip')
TOOL = os.path.join(SITE, 'therapietrouw.html')


def lees(pad):
    with io.open(pad, encoding='utf-8') as f:
        return f.read()


def vervang_een(tekst, oud, nieuw):
    """Vervangt een stuk dat er precies één keer in moet staan; anders stopt de bouw."""
    n = tekst.count(oud)
    if n != 1:
        raise SystemExit('verwacht precies één keer, gevonden %d keer: %s' % (n, oud[:70]))
    return tekst.replace(oud, nieuw)


def ingebed_script(pad):
    """Een bibliotheek uit vendor/ als ingebed script. pdf.js 3.11 zoekt zijn worker eerst in
    globalThis.pdfjsWorker; staat de worker-code als gewoon script op de pagina, dan rekent
    pdf.js in de pagina zelf. Een worker uit een lokaal bestand weigeren Edge en Chrome."""
    code = lees(pad).replace('</script', '<\\/script').replace('<!--', '<\\!--')
    return '<script>/* %s, ingebed voor de offline versie */\n%s\n</script>' % (os.path.basename(pad), code)


def bouw_pagina():
    t = lees(TOOL)
    vendor = os.path.join(SITE, 'vendor')
    t = vervang_een(t, '<link rel="stylesheet" href="styles/tokens.css">',
                    '<style>/* styles/tokens.css, ingebed */\n%s\n</style>' % lees(os.path.join(SITE, 'styles', 'tokens.css')))
    t = vervang_een(t, '<script src="vendor/pdf.min.js"></script>',
                    ingebed_script(os.path.join(vendor, 'pdf.min.js')) + ingebed_script(os.path.join(vendor, 'pdf.worker.min.js')))
    t = vervang_een(t, '<script src="vendor/jszip.min.js"></script>', ingebed_script(os.path.join(vendor, 'jszip.min.js')))
    with open(os.path.join(SITE, 'Image', 'logo_transparent.png'), 'rb') as f:
        logo = 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')
    if t.count('src="Image/logo_transparent.png"') < 1:
        raise SystemExit('logo niet gevonden in therapietrouw.html')
    t = t.replace('src="Image/logo_transparent.png"', 'src="%s"' % logo)
    # buiten het portaal: geen slot en geen weg terug naar de checklist
    t, n = re.subn(r'<!-- PORTAALSLOT.*?<!-- /PORTAALSLOT -->\n?', '', t, flags=re.S)
    if n != 1:
        raise SystemExit('portaalslot niet gevonden')
    t, n = re.subn(r'\s*<button class="btn" type="button" id="btnChecklist"[^>]*>.*?</button>', '', t, flags=re.S)
    if n != 1:
        raise SystemExit('knop naar de visite-checklist niet gevonden')
    t = vervang_een(t, '<title>PARADISE · Therapietrouw</title>', '<title>PARADISE · Therapietrouw (offline)</title>')
    over = re.findall(r'(?:src|href)="(?!data:|https:|#)[^"]+"', t)
    if over:
        raise SystemExit('nog een verwijzing naar een los bestand: %s' % over[:3])
    return t


STARTER = (u'@echo off\r\n'
           u'rem Opent de PARADISE-tool Therapietrouw als apart venster in Microsoft Edge.\r\n'
           u'rem Werkt zonder internet en zonder beheerdersrechten.\r\n'
           u'start "" msedge --app="file:///%~dp0' + NAAM + u'.html"\r\n')

LEESMIJ = u"""PARADISE - Therapietrouw (offline versie)
=========================================

Wat het is
  De tool Therapietrouw van het ledenportaal in een bestand, voor als de site of
  het netwerk niet beschikbaar is. Twee stappen:
  Stap 1 - visite 2: het MoveMonitor-rapport ("Physical activity overview", PDF)
           geeft per dag opstaan en slapengaan. De tijd daartussen is de
           waaktijd; 80% daarvan is de norm. De norm gaat bij Hours/day in de
           Orthotimer; waaktijd en norm gaan op eCRF 28.
  Stap 2 - visite 3 tot 8: de Orthotimer-export (.tef) geeft de draagtijd per
           dag, tegenover de waaktijd en de norm. Het donkere vak boven het blad
           geeft de cijfers voor eCRF 32.

De drie getallen, met een voorbeeld
  Waaktijd   15,5 u/dag   uit de MoveMonitor-week bij de start; geldt de hele studie
  Norm       12,4 u/dag   80% van de waaktijd; staat in de Orthotimer (Hours/day)
  Resultaat  11,2 u/dag   = 72% van de waaktijd = 90% van de norm: niet gehaald
  Op eCRF 32 noteert u het percentage van de norm (hier 90%).

Installeren
  Kopieer de map PARADISE_Therapietrouw naar de laptop, bijvoorbeeld naar het
  bureaublad. Er is geen installatie, geen beheerdersrecht en geen internet nodig.
  Staat er nog een oudere map PARADISE_Draagtijd, verwijder die dan.

Starten
  Dubbelklik op "PARADISE Therapietrouw starten.cmd". De tool opent als apart
  venster in Microsoft Edge. Lukt dat niet, open dan PARADISE_Therapietrouw.html
  met Edge of Chrome (rechtermuisklik > Openen met).

Werkwijze per patient
  1. Klik op "Nieuwe patient". Dat wist alles van de vorige patient.
  2. Visite 2: stap 1, sleep het MoveMonitor-rapport in het venster.
  3. Visite 3 tot 8: stap 2, sleep de Orthotimer-export in het venster en vul
     de waaktijd van eCRF 28 in als de tool ze niet voorstelt. Vul de WAAKTIJD
     in, niet de norm: de tool rekent zelf 80%.
  4. "Afdrukken / PDF" maakt het blad (A4, zonder marges).
     Optimal Care: bespreek het zonder oordeel (SEBIA).
     Usual Care: uitlezen en bewaren, maar niet tonen, bespreken of meegeven.

Privacy
  Alles wordt in de browser op deze laptop verwerkt. Er wordt niets verstuurd.
  Sla afgedrukte documenten op volgens de procedure van het centrum.

Versie
  Gebouwd op __BOUWDATUM__ uit therapietrouw.html van __DATUM_TOOL__. Wijzigt de
  site, dan wordt dit pakket opnieuw gebouwd en verdeeld.
"""


def main():
    os.makedirs(UIT, exist_ok=True)
    bouwdatum = datetime.date.today().strftime('%d/%m/%Y')
    datum_tool = datetime.datetime.fromtimestamp(os.path.getmtime(TOOL)).strftime('%d/%m/%Y')
    bestanden = {
        NAAM + '.html': bouw_pagina(),
        'PARADISE Therapietrouw starten.cmd': STARTER,
        'LEES MIJ.txt': LEESMIJ.replace('__BOUWDATUM__', bouwdatum).replace('__DATUM_TOOL__', datum_tool).replace('\n', '\r\n'),
    }
    for naam, inhoud in bestanden.items():
        with io.open(os.path.join(UIT, naam), 'w', encoding='utf-8', newline='') as f:
            f.write(inhoud)
    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for naam in bestanden:
            z.write(os.path.join(UIT, naam), os.path.join(NAAM, naam))
    print('gebouwd:', os.path.relpath(UIT, SITE))
    for naam in bestanden:
        print('   %-38s %8d bytes' % (naam, os.path.getsize(os.path.join(UIT, naam))))
    print('zip   :', os.path.relpath(ZIP, SITE), '%d bytes' % os.path.getsize(ZIP))


if __name__ == '__main__':
    main()
