// Regressietest voor protocol-analyse.html — domain/type-consistentie van de volledige
// eCRF-matrix, de dynamische tellers, en de zoek-/filtercombinatie (tekst + type-chip).
// Zie tests/README.md voor scope en beperkingen (geen CSS/layout-controle).
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const FILE = path.join(__dirname, '..', 'protocol-analyse.html');
const html = fs.readFileSync(FILE, 'utf8');
const start = html.indexOf('<script>') + 8;
const end = html.indexOf('</script>');
const js = html.slice(start, end);

let failures = 0;
function check(label, cond){
  if(cond){ console.log('  ok   - ' + label); }
  else { console.error('  FAIL - ' + label); failures++; }
}

// Een browser decodeert numerieke HTML-entities (bv. &#8211;) tot het echte teken wanneer
// innerHTML geparsed wordt. Deze nep-DOM doet dat ook, anders test #4 (streepje-normalisatie)
// niets echt.
function decodeEntities(s){ return s.replace(/&#(\d+);/g, (_, d) => String.fromCodePoint(parseInt(d, 10))); }

function makeRow(dataSearch, dataType){
  return {
    getAttribute: (name) => name === 'data-search' ? decodeEntities(dataSearch) : (name === 'data-type' ? dataType : null),
    style: { _d: '', set display(v){ this._d = v; }, get display(){ return this._d; } }
  };
}
function makeChip(typeVal){
  const classes = new Set(['fchip']);
  return {
    getAttribute: (name) => name === 'data-type-filter' ? typeVal : null,
    classList: { toggle: (n, f) => { if(f) classes.add(n); else classes.delete(n); }, has: (n) => classes.has(n) },
    _listeners: [],
    addEventListener: function(evt, fn){ this._listeners.push(fn); },
    click: function(){ this._listeners.forEach(fn => fn()); }
  };
}

let capturedHTML = '';
let rows = [], chips = [];
let searchValue = '', searchListener = null, noMatchDisplay = '';
const appEl = {
  set innerHTML(v){
    capturedHTML = v;
    // De rij draagt sinds de "geschrapt"-markering ook een class-attribuut, dus
    // niet vastpinnen op de volgorde van de attributen.
    rows = [...v.matchAll(/<tr\b[^>]*\bdata-search="([^"]*)"[^>]*\bdata-type="([^"]*)"/g)].map(m => makeRow(m[1], m[2]));
    chips = [...v.matchAll(/data-type-filter="([^"]*)"/g)].map(m => makeChip(m[1]));
  },
  get innerHTML(){ return capturedHTML; }
};
const langBtn = { textContent: '' };
const searchInputEl = {
  get value(){ return searchValue; }, set value(v){ searchValue = v; },
  addEventListener: (evt, fn) => { searchListener = fn; }
};
const noMatchEl = { style: { set display(v){ noMatchDisplay = v; }, get display(){ return noMatchDisplay; } } };

const sandbox = {
  window: { addEventListener: () => {} },
  localStorage: { getItem: () => null, setItem: () => {} },
  document: {
    documentElement: {},
    getElementById: (id) => id === 'app' ? appEl : (id === 'lang' ? langBtn : (id === 'ecrfSearch' ? searchInputEl : (id === 'ecrfNoMatch' ? noMatchEl : null))),
    querySelectorAll: (sel) => sel === '#ecrfMatrixBody tr' ? rows : (sel === '[data-type-filter]' ? chips : []),
    addEventListener: () => {},
    body: { classList: { add: () => {} } }
  },
  self: {}, top: {}, console
};
new vm.Script(js, { filename: 'protocol-analyse-inline.js' }).runInContext(vm.createContext(sandbox));

console.log('protocol-analyse.html');
console.log('  (' + rows.length + ' eCRF-rijen, ' + chips.length + ' type-chips gevonden)');

check('minstens 40 eCRF-rijen gerenderd', rows.length >= 40);
check('geen literale "undefined" in de output', !capturedHTML.includes('undefined'));
check('8 type-filterchips aanwezig', chips.length === 8);

const validTypes = ['vragenlijst','feedback','educatie','toestel','meting','classificatie','administratie','kwalitatief'];
const badType = rows.find(r => !validTypes.includes(r.getAttribute('data-type')));
check('elke rij heeft een geldig, herkend type', !badType);

function countVisible(){ return rows.filter(r => r.style.display !== 'none').length; }

searchValue = 'v3-v8'; // plain ASCII-streepje, tabel gebruikt lange streepjes (&#8211;)
searchListener();
check('streepje-normalisatie: "v3-v8" matcht rijen met V3–V8', countVisible() > 0);

searchValue = '';
searchListener();
check('zoekveld leegmaken -> alle rijen terug zichtbaar', countVisible() === rows.length);

const vChip = chips.find(c => c.getAttribute('data-type-filter') === 'vragenlijst');
vChip.click();
const afterChip = countVisible();
check('type-chip "vragenlijst" filtert naar minstens 1 rij', afterChip > 0 && afterChip < rows.length);
vChip.click();
check('chip nogmaals klikken schakelt filter weer uit', countVisible() === rows.length);

console.log(failures === 0 ? '\nAlle checks geslaagd.' : '\n' + failures + ' check(s) gefaald.');
process.exit(failures === 0 ? 0 : 1);
