// Belast de Orthotimer-parser op de schaal die de clinici echt gaan gebruiken:
// een uitlezing per kwartaal, dus ~92 dagen in plaats van de 41 uit het
// voorbeeldrapport. Bouwt een .tef in exact het formaat dat de parser verwacht
// (DataContract-XML met MeasureDay-blokken) en draait de echte functies eruit.
'use strict';
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..');
const HTML = fs.readFileSync(path.join(SITE, 'PARADISE_Draagpatroon_uploader.html'), 'utf8');

// de zuivere parseerfuncties uit de pagina halen
function haal(naam) {
  const i = HTML.indexOf('function ' + naam + '(');
  if (i < 0) throw new Error('niet gevonden: ' + naam);
  let d = 0, j = HTML.indexOf('{', i);
  const start = i;
  for (let k = j; k < HTML.length; k++) {
    if (HTML[k] === '{') d++;
    else if (HTML[k] === '}') { d--; if (d === 0) return HTML.slice(start, k + 1); }
  }
  throw new Error('geen einde: ' + naam);
}

const namen = ['getField', 'getAll', 'parseDays', 'parseVoltages', 'parseTimes',
               'excludedDates'];
const bron = namen.map(haal).join('\n') + '\n;({' + namen.join(',') + '})';
const F = eval(bron);
const { getField, getAll, parseDays, parseVoltages, parseTimes, excludedDates } = F;

// ---- synthetische export: 92 dagen, kwartaaluitlezing --------------------
function veld(naam, waarde) {
  return '<_x003C_' + naam + '_x003E_k__BackingField>' + waarde +
         '</_x003C_' + naam + '_x003E_k__BackingField>';
}
function maakTef(dagen, start, opts) {
  opts = opts || {};
  let xml = '<ChipExport>';
  for (let i = 0; i < dagen; i++) {
    const d = new Date(start.getTime() + i * 86400000);
    // draagpatroon: doordeweeks ~11 u, zondag 0, en batterij die traag zakt
    const zondag = d.getDay() === 0;
    let uren = zondag ? 0 : 10.5 + Math.sin(i / 5) * 1.5;
    if (opts.batterijDoodVanaf && i >= opts.batterijDoodVanaf) uren = 0;
    const volt = 3.0 - (i / dagen) * (opts.batterijDoodVanaf ? 0.55 : 0.25);
    xml += '<MeasureDay>' + veld('MeasureDate', d.toISOString()) +
           veld('Hours', uren.toFixed(2)) + veld('Voltage', volt.toFixed(3)) +
           '</MeasureDay>';
  }
  xml += '</ChipExport>';
  return xml;
}

function toets(label, waar) {
  console.log((waar ? '  ok   - ' : '  FAIL - ') + label);
  if (!waar) process.exitCode = 1;
}

// ---- A. kwartaaluitlezing: 92 dagen -------------------------------------
const start = new Date(2027, 2, 1);
let xml = maakTef(92, start);
let dagen = parseDays(xml);
let volts = parseVoltages(xml);

console.log('A. Kwartaaluitlezing (92 dagen)');
toets('alle 92 dagen geparsed', dagen.length === 92);
toets('chronologisch gesorteerd', dagen[0].date < dagen[91].date);
toets('eerste datum klopt', dagen[0].date.toDateString() === start.toDateString());
toets('92 spanningswaarden', volts.length === 92);

const vol = dagen.filter(d => d.hours > 0);
const gem = vol.reduce((a, b) => a + b.hours, 0) / vol.length;
const doel = 16.0, norm = doel * 0.8;
const pct = Math.round(gem / doel * 100);
console.log('     gemiddeld ' + gem.toFixed(1) + ' u/dag over ' + vol.length +
            ' gedragen dagen -> ' + pct + '% van ' + doel + ' u waaktijd (norm ' +
            norm.toFixed(1) + ' u)');
toets('adherentie in een plausibel bereik', pct > 40 && pct < 100);

// ---- B. halfjaar in een keer (als een uitlezing overgeslagen wordt) ------
console.log('\nB. Twee kwartalen in een export (184 dagen)');
dagen = parseDays(maakTef(184, new Date(2027, 2, 1)));
toets('184 dagen geparsed, geen plafond', dagen.length === 184);

// ---- C. batterij sterft voor de uitlezing --------------------------------
console.log('\nC. Batterij leeg na 100 dagen, uitgelezen op dag 120');
xml = maakTef(120, new Date(2027, 2, 1), { batterijDoodVanaf: 100 });
dagen = parseDays(xml);
volts = parseVoltages(xml);
const stille = dagen.slice(100).every(d => d.hours === 0);
toets('alle 120 dagen aanwezig in het bestand', dagen.length === 120);
toets('de laatste 20 dagen staan op 0 u', stille);
toets('laagste spanning onder de waarschuwingsdrempel (2,5 V)',
      Math.min.apply(null, volts) < 2.5);
console.log('     LET OP: 20 lege dagen tellen mee als "niet gedragen" en drukken');
console.log('     het gemiddelde met ' + Math.round(20 / 120 * 100) + '%.');

// ---- D. uitgesloten periodes ---------------------------------------------
console.log('\nD. Uitgesloten periode (plaatsing/uitlezing)');
const tijden = '<Root><MeasureTime>' +
  veld('Exclude', 'true') +
  veld('StartDate', new Date(2027, 2, 1).toISOString()) +
  veld('EndDate', new Date(2027, 2, 2).toISOString()) +
  '</MeasureTime></Root>';
const uit = parseTimes(tijden);
toets('uitsluiting herkend', uit.length === 1);
toets('twee kalenderdagen uitgesloten', excludedDates(uit).size === 2);

console.log(process.exitCode ? 'Er faalden checks.' : 'Alle checks geslaagd.');
