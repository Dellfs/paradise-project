// Regressietest voor visite-checklist.html — state-machine, zorgarm-filtering, de V4-combo-
// stap en (het belangrijkste) de encounter-ID-koppeling die moet verhinderen dat toesteldata
// van de ene patiënt zich met een andere patiënt vermengt.
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
check('usual care -> enkel 2 kaarten (V0 + ulcer)', (r.html.match(/data-visit="/g) || []).length === 2);
check('usual care -> verbergt V4', !r.html.includes('V4 ·'));

// B. V4-combo-stap zonder encounter-ID-koppeling (oude/vreemde data)
r = runWith(
  { care: 'optimal', visit: 'v4', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: new Date().toISOString(), meanWearHours: 7.5, pct: 94, encounterId: 'enc_ANDERE_PATIENT' },
    activity: { savedAt: new Date().toISOString(), avgWBHours: 8.0, encounterId: 'enc_huidig' }
  }
);
check('mismatch encounterId -> GEEN gecombineerd rapport getoond', !r.html.includes('Gezamenlijk feedbackdocument'));
check('mismatch encounterId -> valt terug op "volgende stap" (enkel activity klopt)', r.html.includes('Volgende: draagpatroon'));
check('mismatch encounterId -> de vervuilde wear-summary wordt zelf opgeruimd', !('pvc_wear_summary' in r.store));

// C. V4-combo-stap MET correcte encounter-ID-koppeling
r = runWith(
  { care: 'optimal', visit: 'v4', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: new Date().toISOString(), meanWearHours: 7.5, pct: 94, encounterId: 'enc_huidig' },
    activity: { savedAt: new Date().toISOString(), avgWakeHours: 8.0, avgWBHours: 5.0, encounterId: 'enc_huidig' }
  }
);
check('matching encounterId -> gecombineerd rapport verschijnt', r.html.includes('Gezamenlijk feedbackdocument'));
const scoreMatch = r.html.match(/combo-score \w+">(\d+)%/);
check('combo-score rekent op de waaktijd, niet op WB (7.5/8.0 -> 94%)', scoreMatch && scoreMatch[1] === '94');

// D. Verlopen data (correcte encounterId, maar te oud)
const oldDate = new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(); // 6 u geleden
r = runWith(
  { care: 'optimal', visit: 'v4', checked: {}, values: {} },
  {
    encounterId: 'enc_huidig',
    wear: { savedAt: oldDate, meanWearHours: 7.5, pct: 94, encounterId: 'enc_huidig' },
    activity: { savedAt: new Date().toISOString(), avgWBHours: 8.0, encounterId: 'enc_huidig' }
  }
);
check('verlopen wear-summary (>4u oud) -> geen gecombineerd rapport', !r.html.includes('Gezamenlijk feedbackdocument'));

// E. V3 (routine, enkel Orthotimer, geen combo-stap)
r = runWith({ care: 'optimal', visit: 'v3', checked: {}, values: {} });
check('v3 heeft losse orthotimer-actie, geen combo-kaart', r.html.includes('data-open="orthotimer"') && !r.html.includes('combo-report'));

// F. V6 (major, wél drukcontrole, geen MoveMonitor — enkel baseline+6mnd per protocol)
r = runWith({ care: 'optimal', visit: 'v6', checked: {}, values: {} });
check('v6 heeft drukcontrole maar geen mcroberts-actie', r.html.includes('Drukherverdeling CMFO beoordelen (extra controle)') && !r.html.includes('data-open="mcroberts"'));

console.log(failures === 0 ? '\nAlle checks geslaagd.' : '\n' + failures + ' check(s) gefaald.');
process.exit(failures === 0 ? 0 : 1);
