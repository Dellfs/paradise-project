// Regressietest voor visite-checklist.html — state-machine, zorgarm-filtering, de 80%-norm
// (één keer toegepast, met het percentage van de norm voor eCRF 32) en (het belangrijkste)
// de encounter-ID-koppeling die moet verhinderen dat toesteldata van de ene patiënt zich
// met een andere patiënt vermengt.
//
// Draait de tweede <script> uit het bestand in een vm-sandbox met een minimale nep-DOM.
// Test enkel JS-logica, geen CSS/layout — zie tests/README.md.
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const FILE = path.join(__dirname, '..', 'visite-checklist.html');
const html = fs.readFileSync(FILE, 'utf8');
const blocks = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).filter(s => s.trim().length);
const js = blocks[blocks.length - 1];

let failures = 0;
function check(label, cond){
  if(cond){ console.log('  ok   - ' + label); }
  else { console.error('  FAIL - ' + label); failures++; }
}

function runWith(seedState, seedSummaries){
  let capturedHTML = '';
  const appEl = { set innerHTML(v){ capturedHTML = v; }, get innerHTML(){ return capturedHTML; } };
  const subEl = { _t:'', set textContent(v){ this._t = v; }, get textContent(){ return this._t; } };
  const actionsEl = { _h:'', set innerHTML(v){ this._h = v; }, get innerHTML(){ return this._h; } };
  const verEl = { _t:'', set textContent(v){ this._t = v; }, get textContent(){ return this._t; }, title:'' };
  const store = {};
  if(seedState) store['pvc_state'] = JSON.stringify(seedState);
  if(seedSummaries){
    if(seedSummaries.wear) store['pvc_wear_summary'] = JSON.stringify(seedSummaries.wear);
    if(seedSummaries.activity) store['pvc_activity_summary'] = JSON.stringify(seedSummaries.activity);
    if(seedSummaries.encounterId) store['pvc_encounter_id'] = seedSummaries.encounterId;
  }
  const sandbox = {};
  sandbox.window = { addEventListener: () => {}, parent: {}, self: {}, top: {}, print: () => {} };
  sandbox.localStorage = {
    getItem: (k) => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = v; },
    removeItem: (k) => { delete store[k]; }
  };
  sandbox.document = {
    documentElement: {},
    getElementById: (id) => id === 'app' ? appEl : (id === 'tbSub' ? subEl : (id === 'tbActions' ? actionsEl : (id === 'tbVersion' ? verEl : null))),
    addEventListener: () => {},
    body: { classList: { add: () => {} }, style: {} }
  };
  sandbox.self = {};
  sandbox.top = {};
  sandbox.console = console;
  const ctx = vm.createContext(sandbox);
  new vm.Script(js, { filename: 'visite-checklist-inline.js' }).runInContext(ctx);
  return { html: capturedHTML, sub: subEl._t, store };
}

console.log('visite-checklist.html');

// A. Care-arm selectie
let r = runWith(null);
check('geen state -> toont Optimal Care + Usual Care kaarten', r.html.includes('Optimal Care') && r.html.includes('Usual Care'));

r = runWith({ care: 'optimal', visit: null, checked: {}, values: {} });
check('optimal care -> alle 10 visitekaarten (V0-V8 + ulcer)', (r.html.match(/data-visit="/g) || []).length === 10);

r = runWith({ care: 'usual', visit: null, checked: {}, values: {} });
check('usual care -> ook alle 10 visitekaarten (zelfde visites, protocol §5.4)', (r.html.match(/data-visit="/g) || []).length === 10);
check('usual care -> toont V4', r.html.includes('V4 ·'));

// A2. Per arm alleen de eigen stappen
r = runWith({ care: 'usual', visit: 'v2', checked: {}, values: {} });
check('usual care V2 -> geblindeerde drukmeting zichtbaar', r.html.includes('Plantaire drukmeting (geblindeerd)'));
check('usual care V2 -> geen SEBIA-feedback op het activiteitsprofiel', !r.html.includes('Activiteitsprofiel en feedback'));
check('usual care V2 -> geen drukgestuurde aanpassing', !r.html.includes('Drukherverdeling CMFO beoordelen'));
r = runWith({ care: 'usual', visit: 'v3', checked: {}, values: {} });
check('usual care V3 -> geen feedback op therapietrouw', !r.html.includes('Feedback therapietrouw geven'));
check('usual care V3 -> Orthotimer wel uitlezen', r.html.includes('data-open="orthotimer"'));
r = runWith({ care: 'optimal', visit: 'v2', checked: {}, values: {} });
check('optimal care V2 -> geen geblindeerde Usual Care-stap', !r.html.includes('Plantaire drukmeting (geblindeerd)'));
check('optimal care V2 -> drukgestuurde aanpassing zichtbaar', r.html.includes('Drukherverdeling CMFO beoordelen'));

// B. Uitleesstap met een draagpatroon van een ANDERE patiënt (encounter-ID klopt niet)
r = runWith(
  { care: 'optimal', visit: 'v3', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: new Date().toISOString(), meanWearHours: 7.5, goalHours: 8.0, pct: 94, encounterId: 'enc_ANDERE_PATIENT' }
  }
);
check('mismatch encounterId -> geen resultaat getoond', r.html.includes('Nog niet verwerkt') && !r.html.includes('van de waaktijd ·'));
check('mismatch encounterId -> de vervuilde wear-summary wordt zelf opgeruimd', !('pvc_wear_summary' in r.store));

// C. Uitleesstap MET correcte encounter-ID: % van de waaktijd én % van de norm (eCRF 32)
r = runWith(
  { care: 'optimal', visit: 'v3', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: new Date().toISOString(), meanWearHours: 7.5, goalHours: 8.0, pct: 94, encounterId: 'enc_huidig' }
  }
);
check('matching encounterId -> resultaat verschijnt', r.html.includes('✓ Verwerkt'));
check('rekent op de waaktijd (7.5/8.0 -> 94% van de waaktijd)', r.html.includes('94% van de waaktijd'));
check('de 80% wordt één keer toegepast (7.5/6.4 -> 117% van de norm)', r.html.includes('117% van de norm (eCRF 32)'));
check('norm gehaald bij 94% van de waaktijd', r.html.includes('norm gehaald'));

// C2. Onder de norm: 6.0 u bij 8.0 u waaktijd = 75% van de waaktijd = 94% van de norm
r = runWith(
  { care: 'optimal', visit: 'v3', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: new Date().toISOString(), meanWearHours: 6.0, goalHours: 8.0, pct: 75, encounterId: 'enc_huidig' }
  }
);
check('onder de norm -> 94% van de norm, niet gehaald', r.html.includes('94% van de norm (eCRF 32)') && r.html.includes('norm niet gehaald'));

// D. Verlopen data (correcte encounterId, maar te oud)
const oldDate = new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(); // 6 u geleden
r = runWith(
  { care: 'optimal', visit: 'v3', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: oldDate, meanWearHours: 7.5, goalHours: 8.0, pct: 94, encounterId: 'enc_huidig' }
  }
);
check('verlopen wear-summary (>4u oud) -> geen resultaat', r.html.includes('Nog niet verwerkt'));

// D2. V4 (maand 6): geen MoveMonitor meer, sinds de beslissing van 30 september 2026
r = runWith({ care: 'optimal', visit: 'v4', checked: {}, values: {} });
check('v4 heeft geen mcroberts-actie meer', !r.html.includes('data-open="mcroberts"'));
check('v4 leest de Orthotimer gewoon uit en heeft de extra drukcontrole',
      r.html.includes('data-open="orthotimer"') && r.html.includes('Drukherverdeling CMFO beoordelen (extra controle)'));

// D3. V2: de MoveMonitor wordt terugbezorgd en verwerkt (de enige keer)
r = runWith({ care: 'optimal', visit: 'v2', checked: {}, values: {} });
check('v2 verwerkt het beweegpatroon', r.html.includes('data-open="mcroberts"'));

// E. V3 (routine, enkel Orthotimer)
r = runWith({ care: 'optimal', visit: 'v3', checked: {}, values: {} });
check('v3 heeft een orthotimer-actie en geen mcroberts-actie', r.html.includes('data-open="orthotimer"') && !r.html.includes('data-open="mcroberts"'));

// F. V6 (major, wél drukcontrole, geen MoveMonitor — die gaat alleen bij de start mee)
r = runWith({ care: 'optimal', visit: 'v6', checked: {}, values: {} });
check('v6 heeft drukcontrole maar geen mcroberts-actie', r.html.includes('Drukherverdeling CMFO beoordelen (extra controle)') && !r.html.includes('data-open="mcroberts"'));

console.log(failures === 0 ? '\nAlle checks geslaagd.' : '\n' + failures + ' check(s) gefaald.');
process.exit(failures === 0 ? 0 : 1);
