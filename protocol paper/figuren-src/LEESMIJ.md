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

**In een tekeneditor.** De SVG's zijn gewone SVG en openen in Inkscape (gratis)
of Illustrator. Handig om iets te verslepen, maar let op: voor figuur 1, 2, 4 en
de powercurve overschrijft het script je werk bij de volgende run.

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
blik op het resultaat: ze vinden overlap, geen scheve compositie.

## Huisstijl

Kleuren en lettertype staan bovenaan elk generatorscript en zijn gelijk voor de
hele set: navy `#1B3A5C`, tekst `#33475B`, gedempt `#5A6B7D`, lichtblauw vlak
`#EAF1F7`, randen `#C8D3DE`, accent teal `#0E7C86`, signaalrood `#B04A3A`.
Lettertype Arial/Helvetica, zoals tijdschriften voor figuren vragen — dit is
bewust een andere set dan `styles/tokens.css`, dat voor de website geldt.
