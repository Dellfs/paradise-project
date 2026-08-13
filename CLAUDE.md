# Projectinstructies voor Claude Code

> Plaats dit bestand in de **hoofdmap** van je project (de map die je in VS Code opent).
> Claude Code leest het automatisch in bij elke sessie. Pas de delen met « … » aan naar jouw situatie.

## Over dit project
- Een **bestaande statische website** (handgemaakte HTML/CSS/JS), gedeployed via **Netlify** (Git-gebaseerd).
- Inhoud: klinische **handleidingen** + een **MOOC** over de meetinstrumenten van de PARADISE-studie
  (F-Scan GO, Novel pedar, MoveMonitor, Orthotimer).
- **Alle content is in het Nederlands.** Schrijf nieuwe teksten in het Nederlands.

## Omgeving — BELANGRIJK
- Besturingssysteem: **Windows**. Shell: **PowerShell**.
- Geef en gebruik **altijd PowerShell-commando's** (geen bash/Unix-syntax).
  - Ketenen met `;` (bv. `git add . ; git commit -m "..." ; git push`).
  - Gebruik PowerShell-cmdlets waar logisch (`Copy-Item`, `Remove-Item`, `New-Item`), niet `cp`/`rm`/`touch`.
- Toon **altijd een diff vóór** je bestanden wijzigt en **vraag bevestiging** vóór je een commando uitvoert.

## Structuur (huidige, platte lay-out)
- `index.html` — single-page app met de publieke navigatie (Home/About/Research/Publications/Team/
  Professionals/Patients/Contact) + het ledenportaal/adminpaneel (client-side routing via `showPage(id)`).
- Standalone instrumentpagina's/klinische inhoud, elk ook rechtstreeks bereikbaar en ingebed via
  `<iframe>` in index.html's Research-hub: `meetinstrumenten.html`, `drukmeting-demo.html`,
  `studie-protocol.html`, `resultaten-dashboard.html`, `gezondheidseconomie.html`, `patienten-educatie.html`.
- `paradise-academy.html` — de MOOC over de meetinstrumenten.
- `privacyverklaring.html`, `cookiebeleid.html` — juridische pagina's, gelinkt vanuit de footer.
- `styles/tokens.css` — **gedeelde design tokens + CSS-reset**, gelinkt vanuit elke pagina.
- `sitemap.xml`, `robots.txt`, `manifest.json`, `_headers` — SEO/hosting-configuratie.

## Stijl & conventies
- **Design tokens:** blauw-navy familie (`--par-dark #00407A`, `--par-mid #1D8DB0`, `--par-light #52BDEC`,
  `--par-orange #FF7A00`), gedefinieerd in `styles/tokens.css` — link dit bestand in nieuwe pagina's
  in plaats van kleuren te hardcoderen.
- **Lettertypes:** *DM Serif Display* (titels, via `var(--font-h)`) + *DM Sans* (tekst, via `var(--font-b)`).
  Geen Arial/Inter/Roboto/Newsreader/Public Sans.
- HTML semantisch, toegankelijk, responsive en **print-vriendelijk** houden.
- Hergebruik **`styles/tokens.css`**; dupliceer geen CSS-tokens per pagina.
- **Toon de URL `belgianfootpressure.be` NIET** in de pagina-inhoud (geen link in topbar/footer) —
  configuratiebestanden (`sitemap.xml`, `robots.txt`) mogen dit domein wel bevatten.
- Geen emoji's in klinische content tenzij expliciet gevraagd.
- Minimale opmaak; vermijd overbodige headers/bullets.

## Inhoudelijke juistheid — PARADISE-feiten (NIET wijzigen zonder bron)

> **Lees eerst `PARADISE_BRONNEN.md`.** Dat bestand bevat het volledige, nagelezen
> beeld uit het protocol en alle 47 eCRF-documenten: bezoekschema per visite met de
> bijhorende formulieren, geschiktheidscriteria, de opbouw van de CMFO per schoentype,
> de instellingen van beide toestellen, de SAE-termijnen, en de openstaande
> tegenstrijdigheden. Wijkt iets hieronder daarvan af, dan wint `PARADISE_BRONNEN.md`.

Bron: FWO-TBM T000226N (+ doctoraatsplan). Bij twijfel: vragen, niet gokken.
- **Offloadingdoel:** piekdruk **< 200 kPa ÓF ≥ 25% reductie** t.o.v. baseline (NIET 20%; "óf", niet "én").
- **Twee co-primaire eindpunten:** (1) voetulcus-recidief over 18 maanden; (2) schoeisel-adherentie
  = **≥ 80%** van het gemiddelde activiteitenprofiel, **7 dagen/week**, elke 3 maanden uitgelezen.
  **Beide worden op 18 maanden geëvalueerd.** Let op: protocolparagraaf 3.2.2.2 zegt nog
  "primary analysis timepoint at 12 months"; dat is een restant. De synopsis, de
  steekproefberekening (71% vs 85% op 18 maanden) en de statistische analyse zeggen alle drie
  18 maanden. Het protocol moet daar rechtgezet worden.
- **Drukmeting herhaald op maand 6, 12 én 18** (protocol 5.4.2.2), niet alleen 6 en 12.
- **CMFO-opbouw hangt af van het schoentype** (protocol 5.4.2, eCRF 23 deel A1):
  in een **volledig op maat gemaakte schoen** 5 mm microkurk (shore 55) + 5 mm EVA (shore 35-40);
  in een **confectieschoen** 6 mm EVA (shore 35-40), zónder kurk. Deklaag in beide gevallen
  3 mm gesloten-cellig op 3 mm open-cellig, volledige lengte. Metatarsaalbalk 9-10 mm hoog,
  6-11 mm proximaal van de kopjes — of een lokale pad als maar één regio hoog ligt.
  Pasvorm wordt apart beoordeeld in **binnen- én buitenschoeisel**, met fotodocumentatie.
- **Twee paren CMFO:** zodra de drukdoelen gehaald zijn wordt een identiek duplicaatpaar gemaakt.
  Vanaf maand 3 worden beide paren per kwartaal beoordeeld en om beurt onderhouden; de patiënt
  wisselt **niet dagelijks**.
- **Schoeiselcriterium = drie situaties:** volledig maatwerk ('orthopedisch schoeisel'), óf maatzolen
  in semi-orthopedisch schoeisel, óf maatzolen in adequaat confectieschoeisel met extra diepte.
- **F-Scan GO:** in-shoe, software **FootVIEW Pro**, **≥ 12 mid-gait stappen/voet**, comfortsnelheid (±5% bij follow-up),
  dunne naadloze katoenen sok, piekdruk per **8 regio's via Multimask** (hiel, mediale middenvoet,
  laterale middenvoet, metatarsaal 1, metatarsaal 2-3, metatarsaal 4-5, hallux, tenen 2-5 — hallux en
  tenen 2-5 apart, niet meer samengevoegd). **Afgenomen door het STUDIETEAM.**
  Usual Care = **geblindeerd** (niet tonen/bespreken).
- **Novel pedar:** draadloze **in-shoe** druksensor-inlegzolen, gekoppeld aan de **novel database**-software.
  Kalibratie via het **trublu**-toestel (belasten tot 6 bar; softwaarde binnen **5%** van de manometer = ok,
  anders herkalibreren; controle minstens elke 3 maanden). **Afgenomen door de KLINIEKEN (DFC).**
  Status: later toegevoegd, **vervangt op termijn de F-Scan**, loopt nu **parallel ter vergelijking**.
  (Voorheen liep hier de Novel emed, een blootsvoets platformsysteem — dat is vervangen door de pedar.)
- **MoveMonitor (McRoberts):** draagtijd + stappen, **volledige week** op baseline én 6 maanden;
  levert de **80%-adherentiebenchmark**. Dragen op de onderrug, **niet waterdicht**.
- **Orthotimer:** temperatuursensor in de **CMFO**, interval **15 min**, ~100 dagen batterij →
  **elke 3 maanden uitlezen + vervangen**. Framing naar patiënt: **"uw sensor"** (enkel temperatuur; geen GPS/geluid/camera).

## Werkwijze & commando's (PowerShell)
- **Lokaal bekijken:** open de map in VS Code en gebruik de **Live Server**-extensie
  (rechterklik op een `.html` → *Open with Live Server*). Hou alle bestanden in dezelfde map (relatieve links).
- **Deployen naar Netlify (Git):**
  ```powershell
  git add .
  git commit -m "« korte beschrijving van de wijziging »"
  git push
  ```
  Netlify bouwt en publiceert daarna automatisch.

## Werkafspraken met de agent
- Bewerk **enkel de gevraagde bestanden**; meld het als je gedeelde bestanden (`mooc.css`, `mooc.js`) wil aanpassen.
- Bij een nieuwe pagina: **hergebruik de bestaande structuur en klassen** voor een consistente huisstijl.
- Wijzig nooit de bovenstaande PARADISE-feiten zonder dat ik een bron geef.
- Vat na een taak kort samen wat er gewijzigd is.
- **Altijd committen en pushen na een voltooide taak** — `git add` (gericht, enkel de bestanden die je zelf bewerkte
  of aanmaakte — nooit blind `git add .`, want de werkmap bevat vaak losse persoonlijke/kopie-bestanden die niet
  gepusht mogen worden), dan `git commit` met een korte beschrijving, dan `git push`. Dit gebeurt automatisch,
  zonder telkens expliciet te vragen — deze afspraak overschrijft voor de commit/push-stap specifiek de algemene
  regel om bevestiging te vragen vóór een commando.
