// Bewaakt de site als geheel.
// 1. De 80%-draagnorm (eCRF 25b, 28, 32 en PARADISE_BRONNEN.md): norm = 80% van de waaktijd uit de
//    MoveMonitor-week bij de start; Hours/day in de Orthotimer = de norm; in de draagtijdtool vul je
//    de waaktijd in, zodat de 80% één keer toegepast wordt; eCRF 32 vraagt het percentage van de norm;
//    de patiënt hoort "altijd".
// 2. Het offline pakket voor de laptops van de centra draagt dezelfde code als de online uitleestools
//    (als HTML-geëscapete kopie, srcdoc).
// 3. Geen verouderde studiefeiten in de teksten.
// 4. De zes subpagina's gebruiken één gedeeld sjabloon (styles/subpagina.css, scripts/subpagina.js)
//    en dragen er geen eigen kopie van.
// 5. De F-Scan GO (validatiedeelstudie van het studieteam) staat niet op de site of in de MOOC.
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
    [/baseline \+ 6|zes maanden; levert|at six months|at baseline and at 6 months|na 6 maanden; niet/, 'MoveMonitor op maand 6'],
    [/herhaalde MoveMonitor|Enkel op maand 6/, 'MoveMonitor op maand 6 (checklist)'],
    [/vooraleer maatwerkschoeisel|pas bij ≥80%/, '"beschermt pas vanaf 80%"'],
    [/niet 80% daarvan; die 80% zit al/, 'Orthotimer op de volle waaktijd'],
    // de noemer van de 25%-regel is de meting zonder CMFO op visite 2; "baseline" is visite 1
    [/lager dan baseline|t\.o\.v\. (de )?baseline|vs\. baseline|than baseline|below baseline|met de baseline|Baseline piekdruk/i, '25% "t.o.v. baseline"'],
    [/independent in-shoe reference|onafhankelijke in-shoe referentiemeting/, 'pedar als referentie i.p.v. klinisch toestel'],
    [/healing outcomes/, 'draagtijd als determinant van genezing'],
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

console.log('Gedeeld sjabloon van de subpagina\'s');
const vm = require('vm');
const SJABLOON = lees('scripts/subpagina.js');
const SUBPAGINAS = ['meetinstrumenten.html', 'studie-protocol.html', 'patienten-educatie.html',
                    'resultaten-dashboard.html', 'gezondheidseconomie.html', 'drukmeting-demo.html'];
function element() {
  return { innerHTML: '', textContent: '', value: '300', style: {}, dataset: {}, classList: { add() {}, toggle() {} },
           addEventListener() {}, querySelectorAll: () => [], closest: () => null };
}
for (const p of SUBPAGINAS) {
  const x = lees(p);
  check(p + ': laadt styles/subpagina.css en scripts/subpagina.js',
        x.includes('href="styles/subpagina.css"') && x.includes('src="scripts/subpagina.js"'));
  const kopie = ['tr', 'setLang', 'boot', 'footMap', 'calc', 'wireCalc'].filter(n => new RegExp('function ' + n + '\\(').test(x));
  check(p + ': geen eigen kopie van het sjabloon' + (kopie.length ? ' (' + kopie.join(', ') + ')' : ''), !kopie.length);
  // draait het gedeelde script en het paginascript samen, met een minimale nep-DOM
  const els = {};
  const ctx = vm.createContext({
    console, localStorage: { getItem: () => null, setItem() {} },
    document: { getElementById: id => (els[id] = els[id] || element()), addEventListener() {},
                querySelectorAll: () => [], documentElement: {}, body: { classList: { add() {}, contains: () => false } } },
  });
  ctx.window = ctx; ctx.self = ctx; ctx.top = ctx; ctx.addEventListener = () => {};
  const paginaJs = [...x.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join('\n');
  let fout = null;
  try { vm.runInContext(SJABLOON + '\n' + paginaJs, ctx); if (ctx.POST) ctx.POST(); } catch (e) { fout = e.message; }
  check(p + ': start op met het gedeelde script' + (fout ? ' (' + fout + ')' : ''),
        !fout && els.app && els.app.innerHTML.length > 200 && typeof ctx.repaint === 'function');
}

console.log('Professionele afwerking (review 6/10/2026)');
const INDEX = lees('index.html');
check('site start in het Nederlands', INDEX.includes('<html lang="nl">') && INDEX.includes('let lang = "nl";'));
check('iframes krijgen de taal van het document, niet het lege lang-attribuut van het iframe',
      !/onload="[^"]*lang:lang[^"]*"/.test(INDEX));
check('geen "patiënten opgenomen" vóór de inclusie', !/Pati(&#235;|ë)nten opgenomen|Patients included/.test(INDEX));
check('één uitleg van het acroniem: de officiële titel', !/Advancing|Research And Diabetic|Naar Druktherapietrouw/.test(INDEX));
check('alle zes voetklinieken in de affiliaties', ['AZ Sint-Jan Brugge', 'AZ Groeninge', 'AZORG', 'UZ Gent', 'UZ Antwerpen', 'UZ Leuven']
      .every(c => /affiliations:"[^"]*/.exec(INDEX)[0].includes(c)));
check('geen emoji als icoon', !/&#1(29462|28202|27973|28218|28205|27963);|&#9993;/.test(INDEX.replace(/<script[\s\S]*?<\/script>/g, '')));
const RES = lees('resultaten-dashboard.html');
check('resultatenpagina zonder sjabloon of ontwikkelaarsnotities', !/vul aan|Chart\.js|Sjabloon|to fill/.test(RES));
const PAT = lees('patienten-educatie.html');
check('patiëntenpagina: acht visites, geen "bezoek 5 = primair analysepunt"', !/Primair analysepunt|Primary analysis point/.test(PAT) && PAT.includes('Bezoek 8'));
check('patiëntenpagina: de sensor in de zool is waterdicht', !/sensor in uw orthese is niet waterdicht/.test(PAT));
check('patiëntenpagina: geen lege belofte van brochures', !/Binnenkort beschikbaar|Coming soon/.test(PAT));
// elke lokale afbeelding waarnaar de site verwijst, bestaat (de verhuis naar Image/ mag niets breken)
const ontbreekt = [];
for (const p of ['index.html', '404.html', 'cookiebeleid.html', 'privacyverklaring.html', 'manifest.json', 'paradise-academy.html', ...SUBPAGINAS]) {
  const x = lees(p);
  for (const m of x.matchAll(/(?:src|href)\s*[=:]\s*["']([^"'#?:]+\.(?:png|jpe?g|webp|jfif|svg|gif))["']|photo:"([^"]+)"/g)) {
    const pad = m[1] || m[2];
    if (pad && !/^e\.g\./.test(pad) && !fs.existsSync(path.join(SITE, pad))) ontbreekt.push(p + ': ' + pad);
  }
}
check('alle verwezen afbeeldingen bestaan' + (ontbreekt.length ? ' (' + ontbreekt.slice(0, 4).join('; ') + ')' : ''), !ontbreekt.length);

// Site en MOOC tonen alleen wat de clinici in de DFC doen (beslissing Janou 6/10/2026). De F-Scan GO
// (validatiedeelstudie) en de trublu-kalibratie van de pedar doet het studieteam; ze horen er niet op.
console.log('Alleen wat de clinici doen: geen F-Scan, geen kalibratie (6/10/2026)');
for (const p of ['index.html', 'paradise-academy.html', ...SUBPAGINAS]) {
  const x = lees(p);
  check(p + ': geen F-Scan', !/F-?Scan|Tekscan|FootVIEW|tekscan1/i.test(x));
  check(p + ': geen kalibratie', !/trublu|kalibr|calibrat|manometer/i.test(x));
}
check('MOOC: voetdrukkaart en offloadingdoel staan bij de pedar', /if\(key==='pedar'\)h\+=[^\n]*footMapHTML\(\)[^\n]*calcHTML\(\)/.test(mooc));
check('MOOC-tijdlijn: MoveMonitor alleen bij de start', (mooc.match(/'volle week':'full week'/g) || []).length === 1);
check('MOOC: voortgang telt alleen bestaande modules', mooc.includes('if(MODS.indexOf(k)>=0)done.add(k)'));
check('nieuws: geen inclusie "van start" vóór februari 2027', !/inclusie van pati|is now under way/.test(INDEX));

// Adviezen uit de review, goedgekeurd door Janou op 6/10/2026
console.log('Adviezen review (6/10/2026)');
check('framing: een multicentrische studie, geen "PhD-project"', !/PhD[ -]project|PhD Research Project|doctoraatsproject|interdisciplinary PhD/i.test(INDEX));
check('team: Fobelets en Putman zijn promotor, ook in de JSON-LD',
      ['Maaike Fobelets', 'Koen Putman'].every(n => new RegExp('name:"Prof\\. Dr\\. ' + n + '", role:"Promotor"[^\\n]*nl:\\{role:"Promotor"').test(INDEX)
        && INDEX.includes('"name":"' + n + '","jobTitle":"Promotor"')));
check('team: elk lid heeft Nederlandse labels', (INDEX.match(/nl:\{role:"[^"]*", tags:"/g) || []).length === 5);
check('portaal: nieuwe accounts wachten op goedkeuring', !/role: 'member',\s*status: 'approved'/.test(INDEX) && !/Instant activation|Directe activatie/.test(INDEX));
check('portaal: alleen goedgekeurde leden in het ledenportaal', INDEX.includes("(id === 'members' && !isMember)") && INDEX.includes("profile.status !== 'approved'"));
check('Site Editor zegt dat hij alleen in de eigen browser bewaart', INDEX.includes('alleen in deze browser bewaard'));
check('elke publieke pagina heeft een eigen adres', INDEX.includes('function pageFromHash()') && INDEX.includes("addEventListener('popstate', volgAdres)"));
check('evidentiesynthese zoals in het doctoraatsplan, geen meta-analyses', !/meta-anal|amputation prevention|amputatiepreventie/i.test(INDEX));
check('nieuwskaart herhaalt de titel niet', !INDEX.includes('nc-img-txt">${t.title}'));
check('Materialen: geen toestelnaam en onderschrift onder de foto', !/margin-bottom:8px">(Novel pedar|McRoberts DynaPort|Orthotimer)<\/div>/.test(INDEX));
check('één naam: MoveMonitor, niet "McRoberts DynaPort" als titel', !/dyna_title:"McRoberts DynaPort"/.test(INDEX));
check('geen emoji als icoon bij Professionals of het wachtwoordveld',
      !/&#1(28203|28274|27891|28196|28226|28172|28065);/.test(INDEX.replace(/<script[\s\S]*?<\/script>/g, '')));
const GE = lees('gezondheidseconomie.html');
check('gezondheidseconomie: geen kostcijfer zonder bron en geen rekenmodule', !/10\.000|type="range"/.test(GE) && GE.includes('iMCQ'));

console.log(fouten ? '\n' + fouten + ' check(s) gefaald.' : '\nAlle checks geslaagd.');
process.exitCode = fouten ? 1 : 0;
