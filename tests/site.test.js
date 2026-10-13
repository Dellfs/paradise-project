// Bewaakt de site als geheel.
// 1. De 80%-draagnorm (eCRF 25b, 28, 32 en PARADISE_BRONNEN.md): norm = 80% van de waaktijd uit de
//    MoveMonitor-week bij de start; Hours/day in de Orthotimer = de norm; in de tool Therapietrouw vul je
//    de waaktijd in, zodat de 80% één keer toegepast wordt; eCRF 32 vraagt het percentage van de norm;
//    de patiënt hoort "altijd".
// 2. Het offline pakket voor de laptops van de centra draagt dezelfde code als therapietrouw.html.
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

const TT = lees('therapietrouw.html');
const OFFLINE = lees('offline/PARADISE_Therapietrouw/PARADISE_Therapietrouw.html');

console.log('Tool Therapietrouw (12/10/2026: beweeg- en draagpatroon samen)');
const NORM = 0.8;
const band = eval('(' + haal(TT, 'band') + ')');
check('norm gehaald vanaf 80% van de waaktijd (12,4 bij 15,5 u)', band(12.4, 15.5) === 'b-ok');
check('daaronder één stand, geen grens op 60%', band(12.3, 15.5) === 'b-mid' && band(1, 15.5) === 'b-mid');
check('de 80% staat op één plaats', /const NORM = 0\.8;/.test(TT) && !/\b0\.8\s*\*/.test(TT.replace(/const NORM = 0\.8;/, '')));
check('Hours/day uit het bestand wordt als norm gelezen (waaktijd = norm ÷ 0,8)', TT.includes('Math.round(normUitBestand / NORM * 10) / 10'));
check('vangnet tegen de dubbele 80% (norm ingevuld als waaktijd)', TT.includes('otNormKandidaat') && TT.includes('id="goalWarn"'));
// 13/10/2026: visite 3 tot 8 lezen alleen de Orthotimer uit; stap 2 is een eigen startpunt en vraagt de waaktijd.
const waaktijdVoorstel = eval('(' + haal(TT, 'waaktijdVoorstel') + ')');
check('stap 2 zonder stap 1: de tool vraagt de waaktijd vooraan (eCRF 28)',
      TT.includes('id="otWaak"') && TT.includes('Wat is de waaktijd van deze deelnemer?') && TT.includes("waaktijdVoorstel(bekend, parseFloat(String($('otWaak').value)"));
check('waaktijd: die van stap 1 gaat voor op wat ingevuld is', waaktijdVoorstel({uren:15.5}, 14, 12.4).bron === 'bekend' && waaktijdVoorstel({uren:15.5}, 14, 12.4).uren === 15.5);
check('waaktijd: ingevuld gaat voor op Hours/day uit het bestand', waaktijdVoorstel(null, 14.2, 12.4).bron === 'ingevuld' && waaktijdVoorstel(null, 14.2, 12.4).uren === 14.2);
check('waaktijd: niets ingevuld, dan Hours/day ÷ 0,8 (12,4 geeft 15,5)', waaktijdVoorstel(null, NaN, 12.4).bron === 'bestand' && waaktijdVoorstel(null, NaN, 12.4).uren === 15.5);
check('waaktijd: niets bekend, dan leeg en vult de clinicus in', waaktijdVoorstel(null, NaN, null).uren === null);
// Een ingevulde 12,4 terwijl de Orthotimer afgerond op 12 staat: wellicht de norm. Vragen, niet vervangen.
check('vooraan de norm ingevuld (ook bij een afgeronde Hours/day): de tool vraagt het na en vraagt een tweede klik',
      TT.includes('const NORM_MARGE = 0.6;') && TT.includes('Math.abs(vs.uren - normUitBestand) < NORM_MARGE') &&
      TT.includes('Math.abs(gv - otNormKandidaat) < NORM_MARGE') && TT.includes('const voorstel = vs.uren;'));
// 13/10/2026: "ik ga nog altijd niet automatisch van de McRoberts naar de Orthotimer".
check('na "Blad maken" in stap 1 gaat de tool meteen naar stap 2, met waaktijd en norm bovenaan',
      TT.includes('if(mmResultaat && mmResultaat.waaktijd) toonStap(2);') && TT.includes('id="otVanStap1"') &&
      TT.includes('function zetStap1Klaar(') && TT.includes('mmReset(); otReset(); zetStap1Klaar();') &&
      TT.includes('.kop, .klinisch, .stap1klaar { display: none !important; }'));
check('loopt het tekenen van een blad fout, dan een melding in plaats van een scherm dat stil blijft staan',
      TT.includes('try{ mmRender(mmModel); }') && TT.includes('try{ otRender(otModel); }'));
// De online tool laadt pdf.js en JSZip uit vendor/; staan die niet in git, dan ontbreken ze op Netlify.
const inGit = require('child_process').execSync('git ls-files vendor', { cwd: SITE, encoding: 'utf8' });
const geladen = [...TT.matchAll(/src="(vendor\/[^"]+)"/g)].map(m => m[1]).concat(TT.includes("'vendor/pdf.worker.min.js'") ? ['vendor/pdf.worker.min.js'] : []);
check('alle bibliotheken die de tool laadt, staan in git (' + geladen.join(', ') + ')', geladen.length >= 3 && geladen.every(f => inGit.includes(f)));
// De knoppen van de kopbalk zijn wit op donker; op een witte kaart moet de knop een eigen stijl hebben (13/10/2026).
check('stap 1 wijst naar stap 2 voor visite 3 tot 8, met een knop die zichtbaar is op de witte kaart',
      TT.includes('onclick="toonStap(2)">Meteen naar stap 2: Orthotimer') &&
      /\.naar-stap2 \.btn \{[^}]*color: var\(--navy\)[^}]*background: #fff;/.test(TT));
check('stap 1: de waaktijd is opstaan tot slapengaan, uit de lig-periodes', TT.includes("periodes(t, 'LYING PERIODS'") && TT.includes('function opstaanUit(') && TT.includes('function slapengaanUit('));
check('stap 1: alleen volle kalenderdagen tellen (de eerste dag start om 7 u)', TT.includes("if(d.gemeten < 23.5){ r.reden = 'deeldag"));
check('stap 1: het blad zegt "altijd", de norm staat alleen in het vak voor de clinicus',
      TT.includes('altijd, van het moment dat u opstaat tot u gaat slapen') && TT.includes('<span>Norm (80%) <strong>'));
check('stap 2: het vak voor eCRF 32 geeft draagtijd, norm, % van de norm en gehaald', /Voor eCRF 32[\s\S]{0,700}Percentage van de norm[\s\S]{0,200}Norm gehaald/.test(TT));
check('stap 2: gesprek volgt eCRF 32 (wat ging goed, wat is moeilijk, afspraak)', TT.includes('Afspraak tot het volgende bezoek'));
check('beide bladen passen op één A4 zonder marges', TT.includes('@page { size: A4; margin: 0; }'));
// 12/10/2026: na stap 1 "stopte" de tool; de weg naar stap 2 moet zichtbaar zijn, ook na scrollen.
check('na het blad van stap 1 een knop "Verder naar stap 2", en de kop met tabbladen blijft staan',
      TT.includes('id="btnStap2"') && TT.includes('onclick="toonStap(2)">Verder naar stap 2') &&
      TT.includes("$('btnStap2').style.display = stap === 1 && zichtbaar ? '' : 'none';") &&
      /\.kop \{ position: sticky; top: 0;/.test(TT) && TT.includes('<header class="kop">'));
check('de tool laadt de gedeelde huisstijl', TT.includes('<link rel="stylesheet" href="styles/tokens.css">'));
check('samenvattingen dragen het bezoek-ID van de visite-checklist', (TT.match(/bewaarSamenvatting\('pvc_(activity|wear)_summary'/g) || []).length === 2 && TT.includes("const ENCOUNTER_KEY = 'pvc_encounter_id';"));
check('de oude losse uitleesmodules zijn weg', !fs.existsSync(path.join(SITE, 'McRoberts_Beweegpatroon_uploader.html')) && !fs.existsSync(path.join(SITE, 'PARADISE_Draagpatroon_uploader.html')));

console.log('Offline pakket gelijk met de online tool');
const SCRIPT = TT.slice(TT.lastIndexOf('<script>'));
check('offline: dezelfde code als therapietrouw.html', OFFLINE.includes(SCRIPT));
check('offline: geen portaalslot en geen verwijzing naar losse bestanden',
      !OFFLINE.includes('PORTAALSLOT') && !/(src|href)="(vendor|styles|Image)\//.test(OFFLINE));

console.log('Teksten op de site');
const paginas = ['index.html', 'meetinstrumenten.html', 'studie-protocol.html', 'patienten-educatie.html',
                 'resultaten-dashboard.html', 'gezondheidseconomie.html', 'drukmeting-demo.html',
                 'paradise-academy.html', 'visite-checklist.html', 'protocol-analyse.html', 'therapietrouw.html',
                 'scripts/subpagina.js'];
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
    // 12/10/2026, review van de site tegen de beslissingen van 6, 8 en 12 oktober
    [/zonder (de )?CMFO op visite 2|without the CMFO at visit 2|Piekdruk zonder CMFO \(visite 2\)/, 'de 25% tegen visite 2 (sinds 6/10 per sessie)'],
    [/draagtijdtool|wear-time tool|Draagpatroon_uploader|Beweegpatroon_uploader/, 'oude draagtijdtool (nu: tool Therapietrouw)'],
    [/glasvezel|fibre-optic|Verwijder de meting nadien/, 'pedar-stappen niet volgens SOP 09b'],
    [/'M' \+ deelnemersnummer|WP3 gezonde|WP4 diabetes/, 'MoveMonitor-code met voorvoegsel (sinds 8/10 zonder)'],
    [/SEBIA stap 3 en 4|SEBIA 3 & 4|SEBIA Steps 3/, 'feedback alleen in SEBIA 3–4 (is elke opvolgvisite)'],
    [/Bij baseline: drukherverdelende|Geef bij baseline de CMFO/, 'CMFO bij baseline (aflevering is visite 2)'],
    [/Confectie met extra diepte","Extra-depth/, 'CMFO-tabel zonder semi-orthopedisch schoeisel'],
    [/eCRF-documenten\/Per nummer/, 'dode SOP-link (de map heet (e)CRF/Per nummer)'],
  ].filter(([re]) => re.test(x)).map(([, l]) => l);
  check(p + ': geen verouderde formulering' + (fout.length ? ' (' + fout.join(', ') + ')' : ''), !fout.length);
}
const pe = lees('patienten-educatie.html');
check('patiëntenpagina: boodschap "altijd", geen ≥80% als doel voor de patiënt',
      pe.includes('Waarom altijd?') && !/\\u226580% van de tijd dat u op bent/.test(pe));
check('patiëntenpagina: drukmeting per groep (iedereen bezoek 1 en maand 6; PARADISE-groep ook bezoek 2, maand 12 en 18)',
      pe.includes('bij iedereen op het eerste bezoek en na 6 maanden') && !pe.includes('Op het eerste en het tweede bezoek en op maand 6, 12 en 18'));
check('patiëntenpagina: de MoveMonitor dag en nacht', (pe.match(/dag en nacht/g) || []).length >= 2);
const mi = lees('meetinstrumenten.html');
check('handleidingen: CMFO-onderlaag zoals op 12/10 (microkurk of EVA shore 50; confectie of semi-orthopedisch)',
      mi.includes('5 mm microkurk of EVA shore 50') && mi.includes('"Confectie of semi-orthopedisch"'));
check('handleidingen: toegelaten schoenen buiten én binnen, één paar ook in huis, gedocumenteerd, plaats voor de zool',
      mi.includes('buiten én binnen') && mi.includes('ook in huis gedragen') && mi.includes("foto's en een beschrijving") && mi.includes('plaats zijn voor de zool'));
check('handleidingen: SOP-links naar 09b, 19b en 25b', ['09b_Werkinstructie drukmeting', '19b_Werkinstructie MoveMonitor', '25b_Werkinstructie Orthotimer']
      .every(s => mi.includes('sop:"(e)CRF/Per nummer/' + s) && fs.existsSync(path.join(SITE, '(e)CRF', 'Per nummer', mi.match(new RegExp('Per nummer/(' + s + '[^"]*)"'))[1]))));
check('handleidingen: geen emoji bij de rollen', !/\\ud83d\\udc64/.test(mi));
const pa = lees('protocol-analyse.html');
check('protocol-analyse: eCRF 27 alleen op V2, eCRF 32 op V3–V8 in Optimal Care (REDCap-mapping)',
      /"MoveMonitor &#8212; UDI tracking \(return\)"\]\),"V2",/.test(pa) && pa.includes('tr(["V3&#8211;V8 (alleen Optimal Care)"') && !/Adherence feedback"\]\),"V2&#8211;V8"/.test(pa));
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
check('portaal: alleen goedgekeurde leden in het ledenportaal en zijn tools',
      INDEX.includes("['members', 'academy', 'visite', 'therapietrouw'].includes(id) && !isMember") && INDEX.includes("profile.status !== 'approved'"));
check('portaal: één knop Therapietrouw in plaats van Draagpatroon en Beweegpatroon',
      INDEX.includes('id="ps-therapietrouw"') && INDEX.includes("tf.src='therapietrouw.html'") && !/ps-uploader|ps-mcroberts|_uploader\.html/.test(INDEX));
// 12/10/2026: geen editor meer op de site. Tekst staat alleen in de code; een oude
// lokale kopie mag nooit nog een nieuwere tekst uit de code overschrijven.
check('geen site-editor of bewerkmodus in de pagina',
  !/toggleEditMode|openEditor|edOverlay|editBanner|contentEditable|Site Editor/.test(INDEX));
check('geen lokale kopie die de tekst uit de code overschrijft',
  !INDEX.includes("localStorage.setItem('paradise_data'") && !INDEX.includes('localStorage.setItem("paradise_data"') &&
  INDEX.includes("localStorage.removeItem('paradise_data')"));
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
