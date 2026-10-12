// Toetst stap 1 van therapietrouw.html: de waaktijd uit het MoveMonitor-rapport.
// De waaktijd is de tijd tussen de twee nachten, van opstaan tot slapengaan (beslissing PI,
// 17 augustus 2026); 80% daarvan is de norm. De parser krijgt de tekst zoals pdf.js die
// aanlevert: het demorapport van McRoberts (tests/fixtures), plus nagebouwde pagina's voor
// de randgevallen van een PARADISE-meetweek (start om 7 u, toestel 's nachts af, laat naar bed).
'use strict';
const fs = require('fs');
const path = require('path');

const SITE = path.join(__dirname, '..');
const HTML = fs.readFileSync(path.join(SITE, 'therapietrouw.html'), 'utf8');

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

const consts = ['MENG', 'MAP', 'NACHT_KIER', 'OCHTEND_GRENS', 'LAAT_NAAR_BED', 'AVOND_VANAF', 'WAAK_MIN'];
const namen = ['nf', 'klok', 'hm', 'rijRegex', 'leafMin', 'leafBouts', 'leafHours', 'parseTitleDate', 'parseSteps',
               'minuten', 'periodes', 'parseLigperiodes', 'parseZitperiodes', 'parseActievePeriodes', 'parseDagdelen',
               'eersteActiviteit', 'laatsteActiviteit', 'opstaanUit', 'slapengaanUit', 'waaktijdPerDag', 'gemiddelde'];
// 'const WAAK_MIN = 8, WAAK_MAX = 20;' brengt beide grenzen mee
const bron = consts.map(haalConst).join('\n') + '\n' + namen.map(haal).join('\n') + '\n;({' + namen.join(',') + '})';
const F = eval(bron);

function toets(label, waar) {
  console.log((waar ? '  ok   - ' : '  FAIL - ') + label);
  if (!waar) process.exitCode = 1;
}
const klok = m => Math.floor(m / 60) + ':' + String(m % 60).padStart(2, '0');

// Een dag zoals mmParsePdf hem opbouwt
function dag(t) {
  const leaf = F.leafHours(t);
  const wear = ['lying', 'sitting', 'standing', 'shuffling', 'walking', 'stairs', 'cycling'].reduce((a, k) => a + leaf[k], 0);
  return { datum: F.parseTitleDate(t), steps: F.parseSteps(t), wear, gemeten: wear + leaf.notworn, leaf,
           lig: F.parseLigperiodes(t), zit: F.parseZitperiodes(t), actief: F.parseActievePeriodes(t) };
}

// ---- A. het demorapport van McRoberts --------------------------------------
console.log('Demorapport McRoberts (7 volle dagen, dag en nacht gedragen)');
const paginas = fs.readFileSync(path.join(__dirname, 'fixtures', 'mcroberts-demorapport.txt'), 'utf8')
  .split('\n').filter(r => r && !r.startsWith('#'));
const dagen = paginas.slice(1).map(dag);
toets('zeven dagpagina\'s met een datum', dagen.length === 7 && dagen.every(d => d.datum instanceof Date));
toets('elke dag is een volle kalenderdag (gemeten 24 u)', dagen.every(d => Math.abs(d.gemeten - 24) < 0.02));
toets('lig-periodes gelezen, met de nacht geknipt op middernacht',
      dagen[0].lig.length === 5 && dagen[0].lig[0].begin === 1 && dagen[0].lig[0].einde === 421 && dagen[0].lig[1].einde === 1440);
toets('actieve periodes gelezen (stappen, begin, einde)',
      dagen[0].actief.length === 5 && dagen[0].actief[0].stappen === 2726 && klok(dagen[0].actief[0].begin) === '7:54');

const per = F.waaktijdPerDag(dagen);
const verwacht = [['7:01', '22:55'], ['6:35', '22:09'], ['7:33', '23:54'], null, ['10:07', '21:55'], ['7:12', '21:02'], ['7:31', '23:19']];
verwacht.forEach((v, i) => {
  const r = per[i];
  const label = ['wo', 'do', 'vr', 'za', 'zo', 'ma', 'di'][i];
  if (!v) toets(label + ': geen nacht in de vijf langste lig-periodes -> telt niet mee', r.waak === null && /geen nacht/.test(r.reden));
  else toets(label + ': opstaan ' + v[0] + ', slapengaan ' + v[1], klok(r.opstaan) === v[0] && klok(r.slapen) === v[1]);
});
toets('do: kort weer liggen na het opstaan (6:29–6:35) hoort nog bij de nacht', klok(per[1].opstaan) === '6:35');
toets('do: liggen dat vóór 22:57 drie kwartier onderbroken werd, hoort niet bij de nacht', klok(per[1].slapen) === '22:09');
const waak = F.gemiddelde(per.filter(r => r.waak !== null).map(r => r.waak));
console.log('  waaktijd ' + waak.toFixed(2) + ' u/dag, norm ' + (0.8 * waak).toFixed(2) + ' u/dag');
// (15:54 + 15:34 + 16:21 + 11:48 + 13:50 + 15:48) / 6 = 14,875 u
toets('waaktijd 14,9 u/dag over zes dagen', Math.abs(waak - 14.875) < 0.01);
toets('norm 11,9 u/dag (80%, één keer toegepast)', Math.abs(0.8 * waak - 11.9) < 0.01);
const deel = F.parseDagdelen(paginas[0]);
toets('overzicht: % bewegend per dagdeel (voormiddag 10,8 · namiddag 14,2 · avond 9,4 · nacht 2,0)',
      deel && deel.MORNING === 10.8 && deel.AFTERNOON === 14.2 && deel.EVENING === 9.4 && deel.NIGHT === 2.0);
toets('traplopen: aantal keer per dag gelezen', dagen[0].leaf.stairBouts === 33);

// ---- B. randgevallen van een PARADISE-meetweek ------------------------------
// pagina zoals pdf.js hem levert, met de rijen die de parser gebruikt
function pagina(titel, u, lig, zit) {
  const tijd = x => Math.floor(x) + 'h ' + String(Math.round((x % 1) * 60)).padStart(2, '0') + 'm';
  const rij = (naam, n, x) => ' ' + naam + ' ' + n + ' ' + tijd(x) + ' ' + tijd(x) + ' 1.0% 0.010g';
  return 'Physical activity ' + titel + ' Physical activity ' + titel + ' Activity Amount Total time' +
    rij('Lying', 3, u.lying) + rij('Sitting', 90, u.sitting) + rij('Standing', 900, u.standing) + rij('Shuffling', 500, 0.4) +
    rij('Walking', 400, u.walking) + rij('Stair walking', 12, 0.1) + rij('Cycling', 0, 0) + ' Not worn 1 ' + tijd(u.notworn) + ' ' + tijd(u.notworn) + ' 1.0% -' +
    ' Steps 6500 6500 ACTIVE PERIODS (most steps) steps steps duration duration start start end end 900 0h 20m 10:00 10:20' +
    ' SITTING PERIODS (longest period) duration duration start start end end ' + (zit || []).map(p => '0h 40m ' + p[0] + ' ' + p[1]).join(' ') +
    ' LYING PERIODS (longest period) duration duration start start end end ' + lig.map(p => '1h 00m ' + p[0] + ' ' + p[1]).join(' ') + ' * The Movement';
}
const vol = (titel, lig) => pagina(titel, { lying: 8, sitting: 8.5, standing: 4.5, walking: 2.5, notworn: 0 }, lig);

console.log('\nMeetweek die om 7 u start');
const week = [
  pagina('Tue 16-Mar-27', { lying: 1, sitting: 9, standing: 4, walking: 2.6, notworn: 0 }, [['23:00', '24:00']]),   // 7–24 u
  vol('Wed 17-Mar-27', [['0:00', '6:50'], ['23:10', '24:00']]),
  vol('Thu 18-Mar-27', [['0:00', '2:10'], ['2:20', '7:05'], ['22:40', '24:00']]),
  vol('Fri 19-Mar-27', [['0:00', '7:15'], ['23:50', '24:00']]),
  vol('Sat 20-Mar-27', [['0:40', '8:30']]),                                        // laat naar bed (0:40), geen liggen tot middernacht
  vol('Sun 21-Mar-27', [['0:00', '8:00'], ['22:30', '24:00']]),
  pagina('Mon 22-Mar-27', { lying: 6.9, sitting: 0.1, standing: 0, walking: 0, notworn: 0 }, [['0:00', '6:55']])   // 0–7 u
].map(dag);
const w = F.waaktijdPerDag(week);
toets('eerste dag (start 7 u) is een deeldag en telt niet mee', w[0].waak === null && /deeldag/.test(w[0].reden));
toets('laatste dag (tot 7 u) is een deeldag en telt niet mee', w[6].waak === null && /deeldag/.test(w[6].reden));
toets("toiletbezoek 's nachts (2:10–2:20) breekt de nacht niet: opstaan 7:05", klok(w[2].opstaan) === '7:05');
toets('vrijdag: kort liggen tot middernacht is het slapengaan (23:50)', klok(w[3].slapen) === '23:50');
toets('de vijf volle dagen leveren elk een waaktijd', w.slice(1, 6).every(r => r.waak !== null));
toets('waaktijd over die vijf dagen 15,7 u', Math.abs(F.gemiddelde(w.slice(1, 6).map(r => r.waak)) - 15.7) < 0.05);

console.log('\nLaat naar bed, op de volgende dagpagina');
const laat = [vol('Fri 19-Mar-27', [['0:00', '7:00']]), vol('Sat 20-Mar-27', [['0:40', '8:30'], ['22:50', '24:00']])].map(dag);
const l = F.waaktijdPerDag(laat);
toets('vrijdag: slapengaan 0:40 de volgende dag, waaktijd 17,7 u', l[0].slapen === 1440 + 40 && Math.abs(l[0].waak - 17.67) < 0.01);

console.log('\nToestel \'s nachts af (zoals in de pilootmeting van maart 2026)');
const af = [pagina('Wed 18-Mar-26', { lying: 0.5, sitting: 6, standing: 3, walking: 1, notworn: 13.5 }, [['12:25', '12:48'], ['7:58', '8:04']])].map(dag);
const a = F.waaktijdPerDag(af);
toets('toestel al om 12.48 u af: de nacht valt niet te schatten', a[0].waak === null && /laatste activiteit om 12\.48 u/.test(a[0].reden));

console.log('\nToestel \'s nachts af, maar overdag gedragen: de nacht is de tijd tussen de laatste en de eerste activiteit');
// aan om 7:20, af om 22:40: 7 u 20 en 1 u 20 niet gedragen (8,7 u)
const nachtAf = dag(pagina('Wed 17-Mar-27', { lying: 0.3, sitting: 8, standing: 4.6, walking: 2, notworn: 8.67 },
  [['13:10', '13:28']], [['7:20', '8:00'], ['20:30', '22:40']]));
const n = F.waaktijdPerDag([nachtAf])[0];
toets('opstaan 7:20 en slapengaan 22:40, als geschat gemarkeerd', klok(n.opstaan) === '7:20' && klok(n.slapen) === '22:40' && n.geschat === true);
toets('waaktijd 15,3 u', Math.abs(n.waak - 15.33) < 0.01);
const vroegAf = dag(pagina('Wed 17-Mar-27', { lying: 0.3, sitting: 6, standing: 4, walking: 2, notworn: 11.3 },
  [['13:10', '13:28']], [['7:20', '8:00'], ['17:00', '18:40']]));
toets('toestel om 18.40 u af (vóór 20 u): geen schatting', F.waaktijdPerDag([vroegAf])[0].waak === null);
const gedragen = dag(pagina('Wed 17-Mar-27', { lying: 0.3, sitting: 15, standing: 5.7, walking: 2.6, notworn: 0 },
  [['13:10', '13:28']], [['7:20', '8:00'], ['20:30', '22:40']]));
toets('wel gedragen maar niet gelegen (bv. in de zetel geslapen): geen schatting', F.waaktijdPerDag([gedragen])[0].waak === null);

console.log(process.exitCode ? 'Er faalden checks.' : 'Alle checks geslaagd.');
