# PARADISE-tooling — testsuite

Geen build-systeem, geen `package.json` — dit zijn zelfstandige Node-scripts (enkel de
Node-standaardbibliotheek, geen `npm install` nodig). Ze laden de betrokken HTML-bestanden,
voeren het ingebedde `<script>` uit in een `vm`-sandbox met een minimale nep-DOM, en
controleren het resultaat. Er wordt niets naar een echte browser gerenderd — dit dekt
logicafouten (state-machine, filters, encounter-ID-koppeling), **niet** CSS/layout/print.

## Draaien

```powershell
node tests/visite-checklist.test.js
node tests/protocol-analyse.test.js
node tests/check-ecrf-links.js
node tests/sensor-orthotimer.test.js
node tests/sensor-movemonitor.test.js
node tests/academy-sync.test.js
node tests/draagnorm.test.js
```

Elk script eindigt met exit code 0 bij succes, 1 bij een gefaalde assertie — geschikt om
later in een CI-stap te hangen als dat er ooit komt.

## Wanneer draaien

**Bij elke wijziging aan `paradise-academy.html`:** eerst de JS-data aanpassen, dan
`node maak_academy.js` draaien en het resultaat mee committen. De pagina draagt elke tekst
twee keer — in de data en als voorgerenderde HTML die zonder JavaScript leesbaar is — en
`maak_academy.js` genereert die tweede kopie uit de eerste. `tests/academy-sync.test.js`
faalt als ze uit de pas lopen.

**Bij elke wijziging aan `visite-checklist.html`, `protocol-analyse.html`, of één van de
twee uploader-bestanden:**

- [ ] `node tests/visite-checklist.test.js` slaagt
- [ ] `node tests/protocol-analyse.test.js` slaagt
- [ ] `node tests/check-ecrf-links.js` slaagt (of de nieuwe/verwijderde bestanden zijn bewust)
- [ ] Patiëntscheiding manueel gecontroleerd: nieuwe visite starten wist oude toestelgegevens
      (encounter-ID in localStorage verandert, `pvc_wear_summary`/`pvc_activity_summary`
      verdwijnen)
- [ ] Minstens één keer echt in de browser doorgeklikt (Live Server) — deze scripts
      controleren geen CSS, layout, printweergave of tabletgebruik
- [ ] Bestaande flows nog steeds correct (V0–V8 in beide armen, per arm alleen de eigen stappen)
- [ ] Bij een wijziging aan een uploader: dezelfde wijziging geëscapet in
      `offline/PARADISE_Draagtijd/PARADISE_Draagtijd.html`, en `node tests/draagnorm.test.js` slaagt

**De 80%-draagnorm** (`tests/draagnorm.test.js`): norm = 80% van de waaktijd uit de MoveMonitor-week
bij de start; Hours/day in de Orthotimer = de norm; in de draagtijdtool de waaktijd, zodat de 80%
één keer toegepast wordt; eCRF 32 vraagt het percentage van de norm; de patiënt hoort "altijd".

## Wat deze scripts wél en niet vangen

**Wel:** state-machine-fouten, verkeerde domain/type-toewijzing, kapotte zoekfilter,
encounter-ID-mismatches die stilzwijgend data zouden combineren, dode links in
`ECRF_FILES`, sensorexports op de schaal van de studie (kwartaaluitlezing van 92 dagen,
een week MoveMonitor, een lege batterij), drift tussen de twee tekstkopieën van de
MOOC, drift tussen de online uitleestools en het offline pakket, en verouderde formuleringen
van de 80%-norm.

**Niet:** CSS/visuele bugs, printlayout, tabletgedrag, toegankelijkheid, browsercompatibiliteit
buiten pure JS-syntax. Die blijven een manuele controle (zie checklist hierboven).
