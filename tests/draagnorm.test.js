// Bewaakt de 80%-draagnorm over de hele site. De regel (eCRF 25b, 28, 32 en PARADISE_BRONNEN.md):
// norm = 80% van de waaktijd uit de MoveMonitor-week bij de start; Hours/day in de Orthotimer = de
// norm; in de draagtijdtool vul je de waaktijd in, zodat de 80% één keer toegepast wordt; eCRF 32
// vraagt het percentage van de norm; de patiënt hoort "altijd".
//
// Bewaakt ook dat het offline pakket voor de laptops van de centra dezelfde code draagt als de
// online uitleestools: het pakket bevat die als HTML-geëscapete kopie (srcdoc).
'use strict';
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..');
const lees = f => fs.readFileSync(path.join(SITE, f), 'utf8');
let fouten = 0;
function check(label, waar) {
  console.log((waar ? '  ok   - ' : '  FAIL - ') + label);
  if (!waar) fouten++;
}
// zelfde escape als Python html.escape(s, quote=True), waarmee het pakket gebouwd is
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
                  .replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
function haal(bron, naam) {
  const i = bron.indexOf('function ' + naam + '(');
  if (i < 0) throw new Error('niet gevonden: ' + naam);
  let d = 0;
  for (let k = bron.indexOf('{', i); k < bron.length; k++) {
    if (bron[k] === '{') d++;
    else if (bron[k] === '}' && --d === 0) return bron.slice(i, k + 1);
  }
  throw new Error('geen einde: ' + naam);
}

const ORTHO = lees('PARADISE_Draagpatroon_uploader.html');
const MCR = lees('McRoberts_Beweegpatroon_uploader.html');
const OFFLINE = lees('offline/PARADISE_Draagtijd/PARADISE_Draagtijd.html');

console.log('Uitleestool Orthotimer');
const band = eval('(' + haal(ORTHO, 'band') + ')');
check('norm gehaald vanaf 80% van de waaktijd (12,4 bij 15,5 u)', band(12.4, 15.5) === 'b-ok');
check('daaronder één stand, geen grens op 60%', band(12.3, 15.5) === 'b-mid' && band(1, 15.5) === 'b-mid');
check('Hours/day uit het bestand wordt als norm gelezen (waaktijd = norm ÷ 0,8)',
      ORTHO.includes('Math.round(goal/0.8*10)/10'));
check('vangnet tegen de dubbele 80% (norm ingevuld als waaktijd)', ORTHO.includes('pendingNormKandidaat') && ORTHO.includes('id="goalWarn"'));
check('kopregel toont het % van de norm voor eCRF 32', ORTHO.includes("'% van de norm</strong> (eCRF 32)'"));
check('grafiek toont een normlijn', ORTHO.includes('id="normLine"'));

console.log('Uitleestool MoveMonitor (stap 1)');
check('toont de norm voor Hours/day in de Orthotimer', MCR.includes('norm voor Hours/day in de Orthotimer'));

console.log('Offline pakket gelijk met de online tools');
for (const naam of ['band', 'validateOrthotimer', 'confirmAndRender', 'showConfirm', 'renderConsistency']) {
  check('Orthotimer: ' + naam + '() identiek', OFFLINE.includes(esc(haal(ORTHO, naam))));
}
check('MoveMonitor: toont de norm voor Hours/day', OFFLINE.includes(esc('norm voor Hours/day in de Orthotimer')));

console.log('Teksten op de site');
const paginas = ['index.html', 'meetinstrumenten.html', 'studie-protocol.html', 'patienten-educatie.html',
                 'resultaten-dashboard.html', 'gezondheidseconomie.html', 'drukmeting-demo.html',
                 'paradise-academy.html', 'visite-checklist.html'];
for (const p of paginas) {
  const x = lees(p);
  const fout = [
    [/60\\u201379|60–79/, 'kleurgrens 60–79%'],
    [/baseline \+ 6|zes maanden; levert|at six months/, 'MoveMonitor op maand 6'],
    [/herhaalde MoveMonitor|Enkel op maand 6/, 'MoveMonitor op maand 6 (checklist)'],
    [/vooraleer maatwerkschoeisel|pas bij ≥80%/, '"beschermt pas vanaf 80%"'],
    [/niet 80% daarvan; die 80% zit al/, 'Orthotimer op de volle waaktijd'],
  ].filter(([re]) => re.test(x)).map(([, l]) => l);
  check(p + ': geen verouderde formulering' + (fout.length ? ' (' + fout.join(', ') + ')' : ''), !fout.length);
}
const pe = lees('patienten-educatie.html');
check('patiëntenpagina: boodschap "altijd", geen ≥80% als doel voor de patiënt',
      pe.includes('Waarom altijd?') && !/\\u226580% van de tijd dat u op bent/.test(pe));
const mooc = lees('paradise-academy.html');
check('MOOC: juiste antwoord voor de Orthotimer-invoer is 80% van de waaktijd',
      /Welk getal vul je in als gewenste draagtijd in de Orthotimer\?[\s\S]{0,400}?\]\],c:1,/.test(mooc));
check('MOOC: eCRF 32-vraag rekent 90% van de norm als juist', mooc.includes('["90% van de norm — niet gehaald","90% of the norm — not met"]'));

console.log(fouten ? '\n' + fouten + ' check(s) gefaald.' : '\nAlle checks geslaagd.');
process.exitCode = fouten ? 1 : 0;
