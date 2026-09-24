# -*- coding: utf-8 -*-
"""Bouwt het offline pakket 'PARADISE Draagtijd' voor de laptops van de centra.

Waarom: de twee uitleesmodules van de site - het beweegpatroon (McRoberts) en het
draagpatroon (Orthotimer) - moeten ook werken als de site of het netwerk in het
ziekenhuis wegvalt. Een .exe loopt op ziekenhuislaptops vaak vast op de
IT-beveiliging; een HTML-bestand dat in Edge opent, vraagt geen installatie en
geen beheerdersrechten.

Wat het doet: het neemt beide modules ONGEWIJZIGD over en zet ze als ingebedde
documenten (srcdoc) in een startpagina. Ingebedde documenten delen de opslag
van de startpagina, zodat het draagdoel uit stap 1 zeker in stap 2 aankomt,
ook zonder internet en ook als losse bestanden die opslag niet zouden delen.
De rekenregels blijven die van de site; pas ze daar aan en bouw dit pakket
daarna opnieuw.

Gebruik (vanuit de hoofdmap van de site):
    python offline/bouw_offline_pakket.py

Uitvoer:
    offline/PARADISE_Draagtijd/PARADISE_Draagtijd.html
    offline/PARADISE_Draagtijd/PARADISE Draagtijd starten.cmd
    offline/PARADISE_Draagtijd/LEES MIJ.txt
    offline/PARADISE_Draagtijd_offline.zip
"""

import datetime
import html
import io
import os
import zipfile

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UIT = os.path.join(SITE, 'offline', 'PARADISE_Draagtijd')
ZIP = os.path.join(SITE, 'offline', 'PARADISE_Draagtijd_offline.zip')

BEWEEG = os.path.join(SITE, 'McRoberts_Beweegpatroon_uploader.html')
DRAAG = os.path.join(SITE, 'PARADISE_Draagpatroon_uploader.html')
TOKENS = os.path.join(SITE, 'styles', 'tokens.css')


def lees(pad):
    with io.open(pad, encoding='utf-8') as f:
        return f.read()


def stempel(pad):
    return datetime.datetime.fromtimestamp(os.path.getmtime(pad)).strftime('%d/%m/%Y')


def inline_script(pad):
    """Een bibliotheek uit vendor/ als ingebed script. Een ingebed document
    (srcdoc) kan vendor/ niet relatief laden; daarom gaat de code er zelf in."""
    code = lees(pad)
    # zou de HTML-parser het script te vroeg laten sluiten
    code = code.replace('</script', '<\\/script').replace('<!--', '<\\!--')
    return '<script>/* %s, ingebed voor de offline versie */\n%s\n</script>' % (
        os.path.basename(pad), code)


def zonder_vendor(tekst, naam):
    """Vervangt <script src="vendor/..."> door de ingebedde bibliotheek.

    pdf.js 3.11 zoekt zijn worker eerst in globalThis.pdfjsWorker; staat de
    worker-code als gewoon script op de pagina, dan rekent pdf.js in de pagina
    zelf en heeft het geen apart worker-bestand nodig. Een worker uit een
    lokaal bestand wordt door Edge en Chrome geweigerd.
    """
    vendor = os.path.join(SITE, 'vendor')
    vervang = {
        '<script src="vendor/pdf.min.js"></script>':
            inline_script(os.path.join(vendor, 'pdf.min.js')) +
            inline_script(os.path.join(vendor, 'pdf.worker.min.js')),
        '<script src="vendor/jszip.min.js"></script>':
            inline_script(os.path.join(vendor, 'jszip.min.js')),
    }
    for tag, inhoud in vervang.items():
        tekst = tekst.replace(tag, inhoud)
    over = [m for m in ('src="vendor/',) if m in tekst]
    if over:
        raise SystemExit('%s laadt nog iets uit vendor/ dat niet ingebed is' % naam)
    return tekst


STARTPAGINA = u"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PARADISE Draagtijd</title>
<meta name="description" content="Offline versie van de uitleesmodules beweegpatroon en draagpatroon, voor de laptops van de centra.">
<style>
/* styles/tokens.css, ingevoegd bij het bouwen zodat dit ene bestand zelfstandig werkt */
__TOKENS__
</style>
<style>
  html, body { margin:0; height:100%; background:var(--off-white, #f6f8fa); }
  body { font-family:var(--font-b, 'DM Sans', system-ui, sans-serif); color:var(--text, #1b2630);
         display:flex; flex-direction:column; }
  header.balk { background:var(--par-dark, #00407A); color:#fff; padding:10px 18px;
                display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
  header.balk h1 { font-family:var(--font-h, 'DM Serif Display', Georgia, serif); font-weight:400;
                   font-size:1.25rem; margin:0; letter-spacing:.2px; }
  header.balk .sub { font-size:.8rem; opacity:.85; }
  header.balk .ruimte { flex:1; }
  button { font:inherit; cursor:pointer; }
  .knop-nieuw { background:var(--par-orange, #FF7A00); color:#fff; border:0; border-radius:6px;
                padding:7px 14px; font-weight:700; }
  .knop-nieuw:focus-visible, nav.stappen button:focus-visible { outline:3px solid var(--par-light, #52BDEC); outline-offset:2px; }
  nav.stappen { display:flex; gap:0; background:#fff; border-bottom:1px solid #d8e2ea; flex-wrap:wrap; }
  nav.stappen button { background:none; border:0; border-bottom:3px solid transparent;
                       padding:10px 18px; text-align:left; color:var(--text, #1b2630); }
  nav.stappen button b { display:block; font-size:.95rem; }
  nav.stappen button span { font-size:.78rem; color:#5a6a78; }
  nav.stappen button[aria-selected="true"] { border-bottom-color:var(--par-mid, #1D8DB0); }
  nav.stappen button[aria-selected="true"] b { color:var(--par-dark, #00407A); }
  .status { font-size:.82rem; padding:7px 18px; background:#eef6fa; color:#24303b;
            border-bottom:1px solid #d8e2ea; }
  .status strong { color:var(--par-dark, #00407A); }
  main { flex:1; position:relative; min-height:0; }
  main iframe { position:absolute; inset:0; width:100%; height:100%; border:0; background:#fff; }
  main iframe[hidden] { display:none; }
  footer { font-size:.72rem; color:#5a6a78; padding:5px 18px; background:#fff; border-top:1px solid #d8e2ea; }
  @media print { header.balk, nav.stappen, .status, footer { display:none; } }
</style>
</head>
<body>
<header class="balk">
  <div>
    <h1>PARADISE &middot; draagdoel en draagpatroon</h1>
    <div class="sub">Offline versie &middot; werkt zonder internet &middot; alles blijft op deze laptop</div>
  </div>
  <div class="ruimte"></div>
  <button class="knop-nieuw" id="nieuw" type="button"
          title="Wist het draagdoel van de vorige pati&euml;nt en begint opnieuw">Nieuwe pati&euml;nt</button>
</header>

<nav class="stappen" role="tablist" aria-label="Stappen">
  <button role="tab" id="t1" aria-controls="f1" aria-selected="true" type="button">
    <b>1 &middot; Beweegpatroon</b><span>MoveMonitor-rapport &rarr; waaktijd = draagdoel</span></button>
  <button role="tab" id="t2" aria-controls="f2" aria-selected="false" type="button">
    <b>2 &middot; Draagpatroon</b><span>Orthotimer-export &rarr; dagen boven 80% van het draagdoel</span></button>
</nav>

<div class="status" id="status" aria-live="polite"></div>

<main>
  <iframe id="f1" role="tabpanel" aria-labelledby="t1" title="Beweegpatroon (McRoberts)" srcdoc="__BEWEEG__"></iframe>
  <iframe id="f2" role="tabpanel" aria-labelledby="t2" title="Draagpatroon (Orthotimer)" srcdoc="__DRAAG__" hidden></iframe>
</main>

<footer>
  Draagdoel = gemiddelde waaktijd tussen de twee nachten, uit het MoveMonitor-rapport. Norm = 80% daarvan, elke dag.
  &middot; Gebouwd op __BOUWDATUM__ uit de site-versies van het beweegpatroon (__D1__) en het draagpatroon (__D2__).
</footer>

<script>
(function(){
  var SLEUTELS = ['pvc_activity_summary', 'pvc_wear_summary', 'pvc_encounter_id'];
  var f = {1: document.getElementById('f1'), 2: document.getElementById('f2')};
  var t = {1: document.getElementById('t1'), 2: document.getElementById('t2')};
  var bronnen = {1: f[1].getAttribute('srcdoc'), 2: f[2].getAttribute('srcdoc')};

  function toon(n){
    [1,2].forEach(function(i){
      f[i].hidden = (i !== n);
      t[i].setAttribute('aria-selected', i === n ? 'true' : 'false');
    });
    status();
  }

  function nf(x){ return (Math.round(x*10)/10).toString().replace('.', ','); }

  function status(){
    var el = document.getElementById('status'), s = null;
    try { s = JSON.parse(localStorage.getItem('pvc_activity_summary') || 'null'); } catch(e) {}
    if (s && s.avgWakeHours) {
      var d = new Date(s.savedAt);
      el.innerHTML = 'Draagdoel in het geheugen: <strong>' + nf(s.avgWakeHours) + ' u/dag</strong>' +
        ' &middot; norm ' + nf(0.8 * s.avgWakeHours) + ' u/dag' +
        ' &middot; uit het beweegpatroon van ' + d.toLocaleDateString('nl-BE') + ' ' +
        d.toLocaleTimeString('nl-BE', {hour:'2-digit', minute:'2-digit'}) +
        '. Hoort dit niet bij deze pati&euml;nt, klik dan eerst op <em>Nieuwe pati&euml;nt</em>.';
    } else {
      el.innerHTML = 'Nog geen draagdoel. Doe eerst stap 1, of vul het draagdoel in stap 2 zelf in.';
    }
  }

  t[1].addEventListener('click', function(){ toon(1); });
  t[2].addEventListener('click', function(){ toon(2); });

  // De modules vragen de site om te navigeren; hier vangt de startpagina dat op.
  window.addEventListener('message', function(e){
    var d = e.data || {};
    if (d.type !== 'px_navigate') return;
    if (d.page === 'uploader') toon(2);
    else toon(1);
  });
  window.addEventListener('storage', status);

  document.getElementById('nieuw').addEventListener('click', function(){
    if (!confirm('Het draagdoel en de resultaten van de vorige pati\\u00ebnt worden gewist. Doorgaan?')) return;
    SLEUTELS.forEach(function(k){ try { localStorage.removeItem(k); } catch(e) {} });
    [1,2].forEach(function(i){ f[i].setAttribute('srcdoc', bronnen[i]); });
    toon(1);
  });

  setInterval(status, 2000);
  toon(1);
})();
</script>
</body>
</html>
"""

STARTER = (u'@echo off\r\n'
           u'rem Opent de PARADISE-draagtijdtool als apart venster in Microsoft Edge.\r\n'
           u'rem Werkt zonder internet en zonder beheerdersrechten.\r\n'
           u'start "" msedge --app="file:///%~dp0PARADISE_Draagtijd.html"\r\n')

LEESMIJ = u"""PARADISE - draagdoel en draagpatroon (offline versie)
======================================================

Wat het is
  De twee uitleesmodules van de PARADISE-site in een bestand, voor als de site
  of het netwerk niet beschikbaar is.
  Stap 1 - beweegpatroon: het MoveMonitor-rapport ("Physical activity overview",
           PDF, Engels) geeft de gemiddelde waaktijd tussen de twee nachten.
           Dat is het draagdoel.
  Stap 2 - draagpatroon: de Orthotimer-export (.tef of .zip) toont per dag de
           draagtijd, getoetst aan de norm van 80% van het draagdoel.

Installeren
  Kopieer de map PARADISE_Draagtijd naar de laptop, bijvoorbeeld naar het
  bureaublad. Er is geen installatie, geen beheerdersrecht en geen internet nodig.

Starten
  Dubbelklik op "PARADISE Draagtijd starten.cmd". De tool opent als apart
  venster in Microsoft Edge.
  Lukt dat niet, open dan PARADISE_Draagtijd.html met Edge of Chrome
  (rechtermuisklik > Openen met).

Werkwijze per patient
  1. Klik op "Nieuwe patient". Dat wist het draagdoel van de vorige patient.
  2. Stap 1: sleep het MoveMonitor-rapport in het venster. De waaktijd verschijnt;
     dat is het draagdoel.
  3. Klik op "Volgende: draagpatroon", of op het tabblad 2.
  4. Stap 2: sleep de Orthotimer-export in het venster. Het draagdoel staat
     voorgevuld; controleer het en pas het zo nodig aan.
  5. "Afdrukken / PDF" maakt het feedbackdocument.

Privacy
  Alles wordt in de browser op deze laptop verwerkt. Er wordt niets verstuurd.
  Sla afgedrukte documenten op volgens de procedure van het centrum.

Versie
  Gebouwd op __BOUWDATUM__ uit de site-versies van het beweegpatroon (__D1__)
  en het draagpatroon (__D2__). Wijzigt de site, dan wordt dit pakket opnieuw
  gebouwd en verdeeld.
"""


def main():
    os.makedirs(UIT, exist_ok=True)
    bouwdatum = datetime.date.today().strftime('%d/%m/%Y')
    d1, d2 = stempel(BEWEEG), stempel(DRAAG)

    pagina = (STARTPAGINA
              .replace('__TOKENS__', lees(TOKENS))
              .replace('__BEWEEG__', html.escape(zonder_vendor(lees(BEWEEG), 'beweegpatroon'), quote=True))
              .replace('__DRAAG__', html.escape(zonder_vendor(lees(DRAAG), 'draagpatroon'), quote=True))
              .replace('__BOUWDATUM__', bouwdatum).replace('__D1__', d1).replace('__D2__', d2))

    bestanden = {
        'PARADISE_Draagtijd.html': pagina,
        'PARADISE Draagtijd starten.cmd': STARTER,
        'LEES MIJ.txt': (LEESMIJ.replace('__BOUWDATUM__', bouwdatum)
                         .replace('__D1__', d1).replace('__D2__', d2)).replace('\n', '\r\n'),
    }
    for naam, inhoud in bestanden.items():
        with io.open(os.path.join(UIT, naam), 'w', encoding='utf-8', newline='') as f:
            f.write(inhoud)

    with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
        for naam in bestanden:
            z.write(os.path.join(UIT, naam), os.path.join('PARADISE_Draagtijd', naam))

    print('gebouwd:', os.path.relpath(UIT, SITE))
    for naam in bestanden:
        print('   %-32s %8d bytes' % (naam, os.path.getsize(os.path.join(UIT, naam))))
    print('zip   :', os.path.relpath(ZIP, SITE), '%d bytes' % os.path.getsize(ZIP))


if __name__ == '__main__':
    main()
