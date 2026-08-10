# Figuren van de protocolpaper — bron en controle

De SVG's in `protocol paper/` zijn **gegenereerd uit de scripts in deze map**.
Wie een figuur met de hand aanpast en daarna het script opnieuw draait, verliest
die aanpassing. Pas dus bij voorkeur het script aan, niet de SVG.

## Wat hoort bij wat

| Figuur | Bestand | Bron |
| --- | --- | --- |
| Figuur 1 — CONSORT-stroomschema | `Figure1_CONSORT_flow.svg` | `maak_fig1_en_af7.py` |
| Figuur 2 — interventiepad | `Figure2_intervention_pathway.svg` | `maak_fig2_en_fig4.py` |
| Figuur 3 — logisch model | `Figure3_logic_model.svg` | met de hand geschreven SVG |
| Figuur 4 — PRECIS-2 wiel | `Figure4_PRECIS2.svg` | `maak_fig2_en_fig4.py` |
| Figuur 5 — cumulatieve weefselbelasting | `Figure5_CPTS.svg` | met de hand geschreven SVG |
| Additional file 7 — powercurve | `Additional_file_7_power_curve.svg` | `maak_fig1_en_af7.py` |

Figuur 3 en 5 hebben geen generatorscript: die bewerk je rechtstreeks in de SVG.

## Zelf aanpassen

**In het script** (aanbevolen voor figuur 1, 2, 4 en de powercurve).
Alle teksten staan als gewone strings bovenaan de betreffende blokken. De
PRECIS-2 scores bijvoorbeeld staan in `maak_fig2_en_fig4.py` in de lijst
`DOMEINEN`, als tupels van naam, score en motivering. Aanpassen en opnieuw
draaien:

```powershell
cd "protocol paper"
python figuren-src\maak_fig2_en_fig4.py
python figuren-src\maak_fig1_en_af7.py
```

**In Inkscape.** Alle zes de figuren openen gewoon in Inkscape of Illustrator —
het is standaard SVG zonder scripts of externe verwijzingen, dus alles is
selecteerbaar en versleepbaar. Voor figuur 3 en 5 is dit de aangewezen weg.

Voor figuur 1, 2, 4 en de powercurve kan het ook, maar dan geldt: het
generatorscript overschrijft je werk zodra iemand het opnieuw draait. Kies dus
één van beide. Wil je in Inkscape blijven werken, verwijder of hernoem dan het
bijbehorende script, zodat niemand er per ongeluk overheen gaat.

Twee praktische punten bij Inkscape:

- Sla op als **Plain SVG**, niet als Inkscape SVG. Dat laatste voegt eigen
  metadata toe die tijdschriften soms weigeren en die het bestand fors groter maakt.
- Zet tekst niet om naar paden tenzij de uitgever daarom vraagt. Zolang het
  tekst blijft, blijven de controlescripts werken en kan de redactie de figuur
  nog corrigeren.

**In een teksteditor.** SVG is platte tekst. Een label verplaatsen is de `x` of
`y` van dat `<text>`-element wijzigen. Coördinaten lopen van linksboven.

## Controleren na een wijziging

Drie scripts, elk met een eigen blik. Draai ze op alle figuren:

```powershell
cd "protocol paper"
python figuren-src\controle_overlap.py (Get-ChildItem *.svg).FullName
```

PowerShell vult `*.svg` niet zelf in voor een extern programma, vandaar de
`Get-ChildItem`-vorm. Eén bestand controleren mag gewoon:
`python figuren-src\controle_overlap.py Figure2_intervention_pathway.svg`

- `controle_overloop.py` — tekst die buiten het canvas of buiten zijn eigen kader valt.
- `controle_kruising.py` — lijnen die door tekst lopen.
- `controle_overlap.py` — het volledige beeld: tekst tegen lijnen, cirkels, curves
  en tegen andere tekst. Houdt rekening met tekenvolgorde, dekkende
  achtergrondvlakken en rotatie, zodat afgedekte elementen geen valse melding geven.

`controle_overlap.py` omvat de andere twee; de losse scripts zijn er voor als je
gericht één soort probleem zoekt.

De breedtemeting gebruikt Helvetica-metriek. Arial wijkt daar minimaal van af,
dus een marge van enkele pixels blijft verstandig. Deze controles vervangen geen
blik op het resultaat: ze vinden overlap, geen scheve compositie. Een losse
pijlpunt of een scheve pijl komt er niet uit, want daar zit geen tekst bij —
die twee fouten in figuur 1 zijn pas gevonden door de figuur te bekijken.

## Snel naar PNG kijken

Er staat geen SVG-rasterizer op het systeem, maar Edge kan het headless. Handig
om een figuur te bekijken zonder Inkscape te openen, en om een PNG te maken als
een tijdschrift daarom vraagt:

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$map  = "C:/Users/janou/OneDrive - KU Leuven/Documents/PhD Brugge/Site/protocol paper"
& $edge --headless --disable-gpu --screenshot="fig2.png" --window-size=1020,640 `
        "file:///$map/Figure2_intervention_pathway.svg"
```

Geef bij `--window-size` de afmetingen uit de `viewBox` van het bestand op,
anders wordt de figuur afgesneden of komt er witruimte omheen. Draai je er
meerdere achter elkaar, geef dan elk een eigen `--user-data-dir`, anders slaat
alleen de eerste aan.

## Huisstijl

Kleuren en lettertype staan bovenaan elk generatorscript en zijn gelijk voor de
hele set: navy `#1B3A5C`, tekst `#33475B`, gedempt `#5A6B7D`, lichtblauw vlak
`#EAF1F7`, randen `#C8D3DE`, accent teal `#0E7C86`, signaalrood `#B04A3A`.
Lettertype Arial/Helvetica, zoals tijdschriften voor figuren vragen — dit is
bewust een andere set dan `styles/tokens.css`, dat voor de website geldt.
