# PARADISE — informatiesessie voetklinieken

De presentatie wordt gegenereerd, niet met de hand gemaakt. Alles blijft echte
PowerPoint-vormen en echte tekstvakken, dus u kunt achteraf nog alles aanpassen.

## Acht decks uit één bron

Dezelfde inhoud levert acht presentaties. Elke dia draagt een label `voor` met de
letters van de decks waarin hij hoort; de bouwer filtert daarop.

| Deck | Bestand | Duur | Voor wie |
| --- | --- | --- | --- |
| `opleiding` | `PARADISE_opleidingssessie_voetklinieken.pptx` | 60-75 min | De medewerkers van de zes centra. Volledig, met de stapreeks per bezoek. |
| `kort` | `PARADISE_centra_kort.pptx` | 20 min | Opfrissing voor wie de opleiding al volgde. Bezoeken compact op één dia. |
| `board` | `PARADISE_board.pptx` | 15-20 min | Directie, stuurgroep, financier. Met tijdlijn, de vier toezeggingen en de risico's. |
| `congres` | `PARADISE_congres.pptx` | 15 min | Vakgenoten, **in het Engels**. Volgt de opbouw van het protocolmanuscript. |
| `extern` | `PARADISE_extern.pptx` | 15 min | Externe partners, andere ziekenhuizen, industrie. |
| `outreach` | `PARADISE_outreach.pptx` | 10 min | Breed publiek en pers. Geen jargon, geen formuliernummers. |
| `kerngezond` | `PARADISE_kortrijk_kerngezond.pptx` | 10 min | Kortrijk Kerngezond 2026. Burgers, mensen met diabetes, zorgverleners en beleidsmakers. Eindigt op de stand. |
| `planning` | `PARADISE_planning_sep-nov.pptx` | 20 min | Het werkplan september-november 2026: vier sporen, wie wat doet, en hoe je het foolproof maakt. Eigen dia's, geen studie-inhoud. |

## Opnieuw bouwen

```powershell
python maak_beelden.py    # eenmalig: snijdt de toestelfoto's en logo's bij
python maak_alles.py      # bouwt alle decks uit DECKS
python maak_pptx.py board # of één deck apart
```

### Uw eigen wijzigingen gaan niet verloren

De decks worden **gegenereerd**. Wat u rechtstreeks in PowerPoint aanpast,
staat niet in `inhoud.py` en zou bij de volgende bouw verdwijnen. Daarom twee
beveiligingen:

- Is een `.pptx` **jonger** dan alle bronbestanden samen — het teken dat er met
  de hand aan gewerkt is — dan **stopt de bouw** voor dat deck. `maak_alles.py`
  slaat het over en zegt welke. Wilt u toch overschrijven:
  `python maak_pptx.py <deck> --overschrijf`, of `python maak_alles.py --overschrijf`.
- Vóór elke keer overschrijven gaat de vorige versie naar **`vorige\`**, met
  datum en uur in de naam. Daar blijven de laatste vijf per deck staan. Die map
  gaat niet mee in Git.

Een wijziging die moet blijven, hoort in `inhoud.py`. Alles wat daar staat,
overleeft elke bouw; alles wat u in PowerPoint typt, niet.

### Een dia aan een ander deck toevoegen

Pas het veld `voor=` aan bij die dia in `inhoud.py`:

```python
dict(t='statement', voor='ock', ...)   # opleiding, congres, kort
```

De letters: **o** opleiding · **b** board · **c** congres · **u** outreach ·
**k** kort · **e** extern · **p** planning · **g** kerngezond. De titeldia hoort in
alle decks behalve kerngezond en krijgt per deck een eigen ondertitel; die staat
in `DECKS` bovenaan `inhoud.py`, samen met de bestandsnaam en de richttijd.
Kerngezond heeft een eigen opening (`hero_titel`), met de drukmat als beeld in
plaats van een foto.

Alleen het opleidingsdeck klapt de bezoeken uit tot één dia per handeling
(`uitklappen=True` in `DECKS`). De andere decks tonen het bezoek compact op één
dia.

De hoofdstuknummers op de tussendia's worden **per deck opnieuw genummerd**.
Valt een hoofdstuk buiten een deck, dan schuift de rest op; er staat dus nooit
een gat als 01 - 03 in de reeks. Het cijfer in `inhoud.py` doet er alleen toe
voor de leesvolgorde van het bestand.

### Wat elk deck als enige heeft

| Dia | Deck | Waarom daar |
| --- | --- | --- |
| Van pilot tot laatste patiënt | board, extern | De vier fasen met de lopende fase in oranje. De enige dia die zegt wanneer het klaar is. |
| Vier toezeggingen | board | De concrete vraag aan de organisatie: 24 inclusies, één PI, tijd, een looppad van tien meter. |
| Vier risico's | board, extern | Met het inclusierisico bovenaan, zodat u het zelf benoemt. |
| PARADISE toetst overdracht | congres | De these van het manuscript, meteen na het puntenraster. |
| Drie strategieën, één patroon | congres | Offloading, educatie en digitale feedback, elk met hun cijfer. |
| Drie dingen zijn veranderd | congres | Waarom de studie nu pas kan: sensor, COM-B, RIZIV-erkenning. |
| Twee eindpunten, twee berekeningen | congres | De twee steekproefberekeningen naast elkaar. |
| De power die telt, is de gezamenlijke | congres | 74% tot 84%. Het cijfer dat protocollen doorgaans niet noemen. |
| Hoe we het toetsen | congres | Cox met Fine-Gray, beta-regressie, estimands, imputatie. |
| Twee evaluaties, parallel | congres | Gezondheidseconomie en procesevaluatie. |
| Een nulresultaat is ook een resultaat | congres | Wat elke uitkomst betekent. De slotdia. |

Het congresdeck volgt de opbouw van `protocol paper/PARADISE_protocol_manuscript.docx`
en gebruikt de cijfers daaruit. Wijzigt het manuscript, dan wijzigen die dia's mee —
de betrokken velden staan in `inhoud.py` bij de dia's met `voor='c'`.

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

## Getekende iconen in plaats van een plaatshouder

Een kaart waar geen echte foto voor bestaat, zet beter een icoon dan de grijze
plaatshouder. Vervang op een kaart in `inhoud.py` het veld `foto=` door
`icoon=` met een van deze namen:

| Naam | Wat het toont |
| --- | --- |
| `druk` | een voet met één hete plek onder de bal |
| `gevoel` | dezelfde voet met een verbodsteken erover |
| `tijd` | een klok |
| `huis` | een huis met de schoen die binnen blijft staan |
| `wandel` | twee voetstappen die weglopen |
| `ziekenhuis` | een gebouw met een groen kruis |
| `vraag` | een tekstballon met een vraagteken |

Ze werken op de kaarten van `drieluik` en op de twee kaarten van `duo`, worden
getekend uit echte PowerPoint-vormen in de huiskleuren, en blijven dus scherp
op elk scherm. Een nieuwe tekent u erbij in `pictogram()` in `maak_pptx.py`, in
een raster van honderd bij honderd.

## Wat waar staat

| Bestand | Inhoud |
| --- | --- |
| `inhoud.py` | alle tekst, cijfers, presentatietips en interactiemomenten. Hier past u de inhoud aan. |
| `spreektekst.py` | wat u bij elke dia zegt. Hier studeert u uit. |
| `bronnen.py` | de referentielijst van het manuscript, en welke dia op welke referentie steunt. |
| `vertaling.py` | het woordenboek Nederlands-Engels voor het congresdeck. |
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

## De spreektekst

Elke dia draagt in het notitieveld drie dingen, in deze volgorde:

```text
WAT U ZEGT        de uitgeschreven spreektekst, hoogstens vier zinnen
PRESENTATIETIP    waar u op moet letten terwijl u het zegt
INTERACTIE        wat u aan de zaal vraagt, of "geen"
```

De spreektekst staat in **`spreektekst.py`**, niet in `inhoud.py`. Dat is met
opzet: zo hebt u één bestand om uit te studeren, los van de opmaak. De sleutel
is de kop van de dia.

Zes huisregels houden het instudeerbaar. Ze staan bovenaan `spreektekst.py` en
komen hierop neer: vier zinnen per dia, de eerste zin is de bewering en niet wat
er te zien is, één cijfer hardop, de laatste zin is de brug naar de volgende
dia, gelijkaardige dia's krijgen hetzelfde stramien, en alles in spreektaal.

Dat laatste doet het meeste werk. Elke hoofdstukdia opent met "Blok N", elke
bezoekdia met het bezoeknummer, en elke stapdia met "Stap x van y" — die laatste
worden gegenereerd door `stap_tekst()`, zodat de veertig stapdia's van het
opleidingsdeck letterlijk dezelfde zinsbouw hebben.

Vergeet u een dia, dan meldt `maak_pptx.py` dat bij het bouwen:

```text
Geen spreektekst in spreektekst.py voor: <kop van de dia>
```

## Referenties

Elke dia die een externe bewering doet, draagt linksonder een bronregel:

```text
Bron  9 · Bus 2013, DIAFOS   |   13 · Waaijman 2013
```

Achteraan elk deck staat automatisch een **referentiedia** met de volledige
citaties van alles wat in dát deck geclaimd is — alleen die, niet de hele lijst.
De nummering is identiek aan die van `protocol paper/
PARADISE_protocol_manuscript.docx`, zodat dia en manuscript naar hetzelfde
nummer verwijzen.

Welke dia op welke referentie steunt, staat in `BIJ_DIA` in `bronnen.py`, met de
kop van de dia als sleutel. Een dia die niets externs beweert — een
hoofdstukdia, het bezoekschema, de contactdia — staat er niet in. De citaties
worden op de dia ingekort tot eerste auteur, tijdschrift en jaar; de volledige
auteurslijst hoort in het manuscript.

## Het congresdeck in het Engels

`inhoud.py` blijft Nederlands. Het congresdeck draagt `taal='en'` in `DECKS`, en
dan gaat elke dia door `vertaling.py`: een woordenboek Nederlands → Engels dat
recursief over de diadefinitie loopt. Wat in het woordenboek staat wordt
vervangen, de rest blijft ongemoeid — daarom hoeven kleurnamen, toestelnamen en
eCRF-nummers er niet in.

De spreektekst gaat door dezelfde vertaalslag. De **presentatietips en de
interactiemomenten blijven met opzet Nederlands**: die leest alleen u.

Ontbreekt er een zin, dan meldt de bouwer welke:

```text
Nog niet vertaald in vertaling.py (1):
   Zes centra maal 24 is 144.
```

Zolang die melding leeg blijft, staat er geen Nederlands op het Engelse scherm.
