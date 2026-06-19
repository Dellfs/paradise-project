# Projectinstructies voor Claude Code

> Plaats dit bestand in de **hoofdmap** van je project (de map die je in VS Code opent).
> Claude Code leest het automatisch in bij elke sessie. Pas de delen met « … » aan naar jouw situatie.

## Over dit project
- Een **bestaande statische website** (handgemaakte HTML/CSS/JS), gedeployed via **Netlify** (Git-gebaseerd).
- Inhoud: klinische **handleidingen** + een **MOOC** over de meetinstrumenten van de PARADISE-studie
  (F-Scan GO, Novel emed, MoveMonitor, Orthotimer).
- **Alle content is in het Nederlands.** Schrijf nieuwe teksten in het Nederlands.

## Omgeving — BELANGRIJK
- Besturingssysteem: **Windows**. Shell: **PowerShell**.
- Geef en gebruik **altijd PowerShell-commando's** (geen bash/Unix-syntax).
  - Ketenen met `;` (bv. `git add . ; git commit -m "..." ; git push`).
  - Gebruik PowerShell-cmdlets waar logisch (`Copy-Item`, `Remove-Item`, `New-Item`), niet `cp`/`rm`/`touch`.
- Toon **altijd een diff vóór** je bestanden wijzigt en **vraag bevestiging** vóór je een commando uitvoert.

## Structuur « pas aan naar jouw mappen »
- `index.html` — startpagina van de site
- `« /handleidingen/ »` — de instrumentpagina's (F-Scan, Novel emed, MoveMonitor, Orthotimer)
- `« /mooc/ »` — de cursus: `index.html`, modulepagina's, `exam.html`, `slides-*.html`, met gedeelde `mooc.css` + `mooc.js`
- `styles.css` / `mooc.css` — opmaak (één plek om te beheren)
- `mooc.js` — de quiz-engine

## Stijl & conventies
- **Design tokens:** navy `#13283f`, teal `#1c7e94`, papier `#f8f6f0`, lijn `#e3ddd0`;
  accent-boxen groen `#3f7a44`, amber `#b5701a`.
- **Lettertypes:** *Newsreader* (titels/serif) + *Public Sans* (tekst). Geen Arial/Inter/Roboto.
- HTML semantisch, toegankelijk, responsive en **print-vriendelijk** houden.
- Voor inbedding in bestaande pagina's: stijl staat **afgeschermd onder `.pfp-guide`** — niet globaal.
- Hergebruik de **gedeelde** `mooc.css`/`mooc.js`; dupliceer geen CSS per pagina.
- **Toon de URL `belgianfootpressure.be` NIET** in de pagina-inhoud (geen link in topbar/footer).
- Geen emoji's in klinische content tenzij expliciet gevraagd.
- Minimale opmaak; vermijd overbodige headers/bullets.

## Inhoudelijke juistheid — PARADISE-feiten (NIET wijzigen zonder bron)
Bron: FWO-TBM T000226N (+ doctoraatsplan). Bij twijfel: vragen, niet gokken.
- **Offloadingdoel:** piekdruk **< 200 kPa ÓF ≥ 25% reductie** t.o.v. baseline (NIET 20%; "óf", niet "én").
- **Twee co-primaire eindpunten:** (1) voetulcus-recidief over 18 maanden; (2) schoeisel-adherentie
  = **≥ 80%** van het gemiddelde activiteitenprofiel, **7 dagen/week**, elke 3 maanden uitgelezen,
  met **primair analysepunt op 12 maanden**.
- **F-Scan GO:** in-shoe, software **FootVIEW Pro**, **≥ 12 mid-gait stappen/voet**, comfortsnelheid (±5% bij follow-up),
  dunne naadloze katoenen sok, piekdruk per **7 regio's via Multimask**. **Afgenomen door het STUDIETEAM.**
  Usual Care = **geblindeerd** (niet tonen/bespreken).
- **Novel emed:** blootsvoets **platform**, **two-step** bij de risico-/neuropathische voet (anders midgait),
  ≥ 3 geldige beurten/voet, 7 regio's. **Afgenomen door de KLINIEKEN (DFC).**
  Status: later toegevoegd, **vervangt op termijn de F-Scan**, loopt nu **parallel ter vergelijking**.
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
