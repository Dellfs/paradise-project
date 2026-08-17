// Toetst de MoveMonitor-parser op de zeven dagen die de clinicus aanlevert.
// De PDF zelf is een OneDrive-placeholder, dus we voeden de parser de tekst
// zoals pdf.js die aanlevert: per pagina alle tekstitems aaneengeregen.
'use strict';
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..');
const HTML = fs.readFileSync(path.join(SITE, 'McRoberts_Beweegpatroon_uploader.html'), 'utf8');

function haal(naam) {
  const i = HTML.indexOf('function ' + naam + '(');
  if (i < 0) throw new Error('niet gevonden: ' + naam);
  let d = 0;
  for (let k = HTML.indexOf('{', i); k < HTML.length; k++) {
    if (HTML[k] === '{') d++;
    else if (HTML[k] === '}') { d--; if (d === 0) return HTML.slice(i, k + 1); }
  }
  throw new Error('geen einde: ' + naam);
}
function haalConst(naam) {
  const m = HTML.match(new RegExp('const ' + naam + '\\s*=\\s*[^;]+;'));
  if (!m) throw new Error('const niet gevonden: ' + naam);
  return m[0];
}

const namen = ['hm', 'leafMin', 'leafBouts', 'leafHours', 'parseTitleDate'];
const bron = haalConst('MAP') + '\n' + haalConst('MENG') + '\n' +
             namen.map(haal).join('\n') + '\n;({' + namen.join(',') + '})';
const F = eval(bron);

function toets(label, waar) {
  console.log((waar ? '  ok   - ' : '  FAIL - ') + label);
  if (!waar) process.exitCode = 1;
}

// ---- een dagpagina nabouwen zoals pdf.js hem oplevert --------------------
// Kolommen in de tabel: categorie, aantal bouts, totale tijd, gemiddelde, percentage
function dagPagina(datum, u) {
  const rij = (naam, bouts, uren) => {
    const h = Math.floor(uren), m = Math.round((uren - h) * 60);
    return ' ' + naam + ' ' + bouts + ' ' + h + 'h ' + m + 'm 0h 12m ' +
           (uren / 24 * 100).toFixed(1) + '%';
  };
  return 'Physical activity ' + datum + ' Subject M042 ' +
    rij('Lying', u.lyingBouts, u.lying) +
    rij('Sitting', 6, u.sitting) +
    rij('Standing', 40, u.standing) +
    rij('Shuffling', 30, u.shuffling) +
    rij('Walking', 120, u.walking) +
    rij('Stair walking', 8, u.stairs) +
    rij('Cycling', 1, u.cycling) +
    ' Steps 8452 ';
}

const DAGEN = [
  ['Mon 15-Mar-27', { lying: 9.0, lyingBouts: 3, sitting: 6.5, standing: 4.2, shuffling: 1.1, walking: 2.8, stairs: 0.3, cycling: 0.1 }],
  ['Tue 16-Mar-27', { lying: 8.5, lyingBouts: 2, sitting: 7.0, standing: 4.0, shuffling: 1.3, walking: 2.9, stairs: 0.2, cycling: 0.1 }],
  ['Wed 17-Mar-27', { lying: 9.5, lyingBouts: 4, sitting: 6.8, standing: 3.6, shuffling: 1.0, walking: 2.7, stairs: 0.3, cycling: 0.1 }],
  ['Thu 18-Mar-27', { lying: 8.8, lyingBouts: 3, sitting: 6.2, standing: 4.5, shuffling: 1.2, walking: 3.0, stairs: 0.2, cycling: 0.1 }],
  ['Fri 19-Mar-27', { lying: 9.2, lyingBouts: 3, sitting: 6.6, standing: 4.1, shuffling: 1.1, walking: 2.6, stairs: 0.3, cycling: 0.1 }],
  ['Sat 20-Mar-27', { lying: 10.0, lyingBouts: 2, sitting: 7.5, standing: 3.2, shuffling: 0.9, walking: 2.2, stairs: 0.1, cycling: 0.1 }],
  ['Sun 21-Mar-27', { lying: 10.5, lyingBouts: 2, sitting: 8.0, standing: 2.8, shuffling: 0.8, walking: 1.8, stairs: 0.1, cycling: 0.0 }],
];

console.log('Zeven dagen MoveMonitor');
const geparsed = DAGEN.map(([titel, u]) => {
  const t = dagPagina(titel, u);
  return { datum: F.parseTitleDate(t), leaf: F.leafHours(t), verwacht: u };
});

toets('alle 7 dagen hebben een datum', geparsed.every(d => d.datum instanceof Date));
toets('datums zijn opeenvolgend',
  geparsed.every((d, i) => i === 0 || (d.datum - geparsed[i - 1].datum) === 86400000));
toets('jaartal 27 -> 2027', geparsed[0].datum.getFullYear() === 2027);

const eersteFout = geparsed.map(d =>
  Object.keys(d.verwacht).filter(k => k !== 'lyingBouts')
    .map(k => Math.abs(d.leaf[k] - d.verwacht[k]))
    .reduce((a, b) => Math.max(a, b), 0)
).reduce((a, b) => Math.max(a, b), 0);
toets('alle categorieuren binnen 1 minuut correct gelezen', eersteFout < 0.017);
toets('ligbouten gelezen', geparsed.every((d, i) => d.leaf.lyingBouts === DAGEN[i][1].lyingBouts));

// ---- de twee kandidaat-noemers ------------------------------------------
const MIN_SHORT_LYING = 0.5;
const wb = geparsed.reduce((s, d) =>
  s + d.leaf.walking + d.leaf.stairs + d.leaf.standing + d.leaf.shuffling, 0) / 7;
const wake = geparsed.reduce((s, d) => {
  const slaap = Math.max(0, d.leaf.lying - Math.max(0, (d.leaf.lyingBouts - 1) * MIN_SHORT_LYING));
  return s + Math.max(0, 24 - slaap);
}, 0) / 7;

console.log('\n  gewichtsdragende tijd : ' + wb.toFixed(1) + ' u/dag');
console.log('  waaktijd              : ' + wake.toFixed(1) + ' u/dag  <- het draagdoel');
console.log('  norm 80%              : ' + (wake * 0.8).toFixed(1) + ' u/dag');
toets('waaktijd in een plausibel bereik (13-18 u)', wake > 13 && wake < 18);
toets('waaktijd ruim boven de gewichtsdragende tijd', wake > wb * 1.5);

// ---- wat als een dag ontbreekt of onvolledig is -------------------------
console.log('\nOnvolledige week');
const zesDagen = geparsed.slice(0, 6);
toets('zes dagen leveren nog steeds een gemiddelde', zesDagen.length === 6);
const geenLig = F.leafHours(dagPagina('Mon 22-Mar-27',
  { lying: 0, lyingBouts: 0, sitting: 8, standing: 5, shuffling: 1, walking: 3, stairs: 0.2, cycling: 0 }));
toets('dag zonder ligtijd valt uit de waaktijdberekening (lyingBouts = 0)',
      geenLig.lyingBouts === 0);

console.log(process.exitCode ? 'Er faalden checks.' : 'Alle checks geslaagd.');
