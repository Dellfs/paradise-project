# PARADISE — informatiesessie voetklinieken

De presentatie wordt gegenereerd, niet met de hand gemaakt. Alles blijft echte
PowerPoint-vormen en echte tekstvakken, dus u kunt achteraf nog alles aanpassen.

## Opnieuw bouwen

```powershell
python maak_beelden.py    # eenmalig: snijdt de toestelfoto's en logo's bij
python maak_pptx.py       # bouwt PARADISE_opleidingssessie_voetklinieken.pptx
```

## Foto's inplakken

Acht stapdia's hebben een fotokader. De plaatshouder is een **echte afbeelding**,
dus vervangen gaat met **rechtsklik → Afbeelding wijzigen**: kader, positie en
uitsnede blijven behouden en de lay-out verschuift niet.

Stockfoto's eerst klaarmaken:

```powershell
# zet de gedownloade foto's in beeld\stock\
python verwerk_stock.py
```

Van elke foto komen er twee versies in `beeld\`:

| Bestand | Wanneer gebruiken |
| --- | --- |
| `<naam>_kleur.png` | Instructiebeeld waar de kleur informatie draagt: de groene sensor, een rode huidzone. |
| `<naam>_duo.png` | Sfeerbeeld en achtergronden. Omgezet naar de blauwfamilie, zodat het niet uit de toon valt. |

Beide zijn bijgesneden op de verhouding van het kader (700 × 440), dus ze passen
zonder vervorming.

Wilt u ergens anders ook een kader, maak van die handeling in `inhoud.py` een
tuple: `('de handeling', 'wat er op de foto staat')`. De dia wordt dan
tweekolommig met kader en bijschrift.

## Wat waar staat

| Bestand | Inhoud |
| --- | --- |
| `inhoud.py` | alle tekst, cijfers, presentatietips en interactiemomenten. Hier past u de inhoud aan. |
| `maak_pptx.py` | de opmaak: één blok per diatype. Hier past u de vormgeving aan. |
| `beeld.py` | de getekende beelden: de drukmat en het trajectcanvas. |
| `maak_beelden.py` | snijdt de productfoto's uit de hoofdmap bij. |
| `beeld\` | de bijgesneden foto's die in de dia's terechtkomen. |

## De drie technieken die het geheel dragen

**1 — Morph met gedwongen koppeling (`!!`-namen).**
PowerPoint raadt normaal zelf welke vorm bij welke hoort. Dat gaat mis zodra
twee dia's veel op elkaar lijken. Elke vorm die moet morphen krijgt daarom een
naam die met `!!` begint en op beide dia's identiek is; dan koppelt PowerPoint
gegarandeerd één op één. Dat is de officiële methode van Microsoft.

**2 — De drukmat als morph (dia 9 → 10).**
De sensormatrix is geen plaatje maar 330 losse vormen, op beide dia's met
dezelfde namen. Alleen de kleur verschilt. Bij het doorklikken kóélt de hete
plek onder metatarsaal 2-3 dus letterlijk af terwijl de voetboog oplicht. De
waarden zijn zo geschaald dat de heetste cel exact op het genoemde cijfer
uitkomt (312 kPa vóór, 186 kPa na).

**3 — Het trajectcanvas als camerabeweging (dia 14 → 18).**
Dia 14 tot 18 tekenen hetzelfde traject, alleen met een andere camera-instelling
(schaal en middelpunt). Omdat alle stippen, labels en de aslijn hun `!!`-naam
behouden, ziet de zaal geen dia-wissel maar een camera die inzoomt op fase 1,
doorschuift naar fase 2, uitzoomt over de staart en op het eind weer terugkomt
bij het geheel. De schaal en het middelpunt staan per zoomdia in `inhoud.py`
(`schaal`, `mid`, `ox`).

## Zelf aanpassen

- **Tekst of cijfers**: `inhoud.py`, de dia's staan in leesvolgorde.
- **Een zoomdia anders kadreren**: verhoog `schaal` om verder in te zoomen,
  verschuif `mid` om een ander moment in beeld te nemen.
- **De drukhaarden**: `VOOR` en `NA` in `beeld.py`, per haard
  `(x, y, sterkte, spreiding)` op een genormaliseerde voet (0 = hiel, 1 = teen).
- **Kleuren**: `K` bovenaan `inhoud.py`; de kleurband van de drukmat is `BAND`
  in `beeld.py`.

Elke dia draagt in het notitieveld een presentatietip en een interactiemoment.
