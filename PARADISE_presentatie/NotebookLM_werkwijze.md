# Een animatievideo van PARADISE maken in NotebookLM

Dit blad is voor jou, niet voor NotebookLM. **Upload alleen
`NotebookLM_bron_PARADISE.md`**; dit bestand niet.

---

## Waarom maar één bronbestand

NotebookLM maakt het script uit álles wat in het notebook zit. Gooi je het protocol,
de eCRF's of een deck er ook in, dan gaat het middelen tussen registers en komt er een
video uit die half naar een ethische commissie en half naar een schoolbezoek klinkt.

Eén bron die van begin tot eind in de juiste toon staat, geeft een veel scherper
resultaat dan tien bronnen die samen completer zijn. Wil je later een versie voor de
klinieken of voor een congres, maak dan een nieuw notebook met een nieuw bronbestand —
niet een tweede bron in ditzelfde notebook.

---

## De stappen

1. **Nieuw notebook** aanmaken op notebooklm.google.com.
2. **Uitvoertaal op Nederlands zetten** — dit doe je *vóór* je genereert. Klik op het
   tandwiel rechtsboven (of je profielafbeelding) → *Uitvoertaal* → Nederlands. Doe je
   dit niet, dan komt de video er in het Engels uit en moet je hem opnieuw genereren.
3. **Bron toevoegen** → `NotebookLM_bron_PARADISE.md` uploaden. Wacht tot hij verwerkt is.
4. Rechts in het Studio-paneel: **Video-overzicht** → op de drie puntjes of het
   instelicoon klikken → **Aanpassen**.
5. **De prompt hieronder plakken** in het aanpasvenster.
6. Kies de stijl **Uitleg** (Explainer), niet Kort/Brief — Kort levert ongeveer een minuut.
7. Genereren. Reken op vijf tot vijftien minuten; je kunt het tabblad sluiten.

---

## De prompt om te plakken

```
Maak een animatievideo van vier tot vijf minuten voor een breed publiek: mensen met
diabetes, hun familie, en bezoekers van een infostand. Geen medische voorkennis.

Volg de tien scènes uit de bron in die volgorde, van de wandeling in het park tot het
slot in het park. Elke scène is één beeld met één gedachte.

De regels die met "Beeld:" beginnen zijn regie voor de illustraties. Gebruik ze om te
bepalen wat er te zien is, maar lees ze niet voor.

Toon: warm en concreet, alsof je het aan een buurman uitlegt. Korte zinnen, rustig
tempo. Verwondering mag, medelijden niet. Frans is geen patiëntje maar een man die met
zijn hond wandelt en dat wil blijven doen.

Gebruik de getallen uit de bron precies zoals ze er staan, en verzin er geen bij. Geen
vakjargon: "zool op maat" en niet "orthese", "de zes ziekenhuizen" en niet "de centra".

Zeg nergens dat de aanpak werkt — de studie loopt nog en eindigt op een open vraag.
Haal de meetzool en de zool op maat niet door elkaar. Toon geen wonden of amputaties.

Stijl van de beelden: rustige, warme illustraties in vlakke kleuren. Geen foto's, geen
stockbeeld, geen schokkende medische afbeeldingen.
```

---

## Wat je daarna nakijkt

Bekijk de video één keer met dit lijstje ernaast. NotebookLM verzint zelden feiten bij,
maar het vereenvoudigt soms nét te ver.

- **Klopt het onderscheid tussen de twee zolen?** De meetzool meet, de zool op maat
  neemt de druk weg. Dit is de fout die het vaakst gemaakt wordt.
- **Staat er nergens dat het werkt?** Let ook op halve beloftes als "zo voorkomen we
  wonden". Het moet een vraag blijven.
- **Krijgen beide groepen dezelfde zorg?** Als de video suggereert dat de controlegroep
  iets tekortkomt, is dat een probleem — ethisch én feitelijk.
- **Kloppen 144, 6, 18 maanden, 200, 312 en 186?**
- **Is Frans een mens gebleven en geen casus?**

Klopt er iets niet, pas dan de bron aan op dat punt en genereer opnieuw. Dat werkt beter
dan het in de prompt proberen recht te zetten: NotebookLM hecht meer aan de bron dan aan
de instructie.

---

## Als de duur tegenvalt

De stijl *Uitleg* landt meestal tussen drie en zes minuten, maar NotebookLM stuurt daar
niet strak op. Valt hij te kort uit, dan ligt dat bijna altijd aan te weinig bronmateriaal
per scène — vul de scène die is weggevallen aan met twee of drie extra zinnen in de bron.
Valt hij te lang uit, schrap dan eerder een hele scène dan overal wat weg te halen; scène
8 en scène 10 kunnen samen zonder dat het verhaal breekt.

---

## Waar dit vandaan komt

De personages, de toon en de cijfers sluiten aan bij `animatie_voiceover.txt`, de
voice-over van de bestaande animatiefilm van 82 seconden. Deze video is daar de lange
versie van: dezelfde opening, maar met het tweede deel van het verhaal erbij — dat een
zool alleen helpt als hij gedragen wordt.

Alle inhoudelijke feiten komen uit `PARADISE_BRONNEN.md`. Wijzigt daar iets, werk dan
eerst de bron bij en genereer daarna pas opnieuw.
