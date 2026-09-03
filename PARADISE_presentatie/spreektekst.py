# -*- coding: utf-8 -*-
"""Wat u bij elke dia zegt.

Zes huisregels, zodat het zich laat instuderen en elke gelijkaardige dia
hetzelfde klinkt:

1. **Vier zinnen, niet meer.** Wie meer nodig heeft, heeft twee dia's nodig.
2. **De eerste zin is de bewering**, niet wat er te zien is. Niet "hier ziet u
   de drukmeting", wel "elke sensor geeft een cijfer".
3. **Eén cijfer hardop.** De rest staat op de dia om gelezen te worden; noemt u
   ze allemaal, dan blijft er geen enkel hangen.
4. **De laatste zin is de brug** naar de volgende dia. Daar zit de opbouw in.
5. **Gelijkaardige dia's, gelijk stramien.** Elke hoofdstukdia opent met
   "Blok N", elke bezoekdia met het bezoeknummer, elke stapdia met "Stap x van
   y". Dat scheelt de helft van het instuderen.
6. **Spreektaal.** Korte zinnen, actieve vorm, geen bijzinnen. Cijfers voluit
   waar u ze uitspreekt.

De sleutel is de kop van de dia; voor de titeldia het diasoort. Ontbreekt er
een dia in dit bestand, dan meldt maak_pptx.py dat bij het bouwen.
"""


def sleutel(d):
    """De naam waaronder een dia zijn spreektekst vindt."""
    return d.get('kop') or d.get('titel') or d['t']


# Stapdia's worden gegenereerd uit de bezoeken; ze krijgen daarom een formule in
# plaats van een eigen tekst. Zo klinkt elke stap in elk bezoek hetzelfde.
def stap_tekst(nr, totaal, laatste):
    if laatste:
        return ('Stap %d van %d, de laatste van dit bezoek. Loop de formulieren '
                'af en herhaal de let-op in uw eigen woorden.' % (nr, totaal))
    return ('Stap %d van %d. Zeg de handeling in uw eigen woorden en wijs aan '
            'waar ze op het formulier terechtkomt.' % (nr, totaal))


ZEG = {

    # ------------------------------------------------------------ opening
    'titel_foto':
        'PARADISE gaat niet over genezen maar over terugkomen. Zes Belgische '
        'voetklinieken, honderdvierenveertig patiënten, achttien maanden per '
        'patiënt. Ik neem u mee langs het waarom, de meting en het traject. '
        'Onderbreek me gerust.',

    'Na vandaag kunt u dit zelf':
        'Dit is de lat voor vandaag. Zes handelingen, en na deze sessie doet u '
        'ze zelf. Herkent u er één waarvan u nu al denkt: dat durf ik niet — '
        'zeg het dan meteen. Daar is deze sessie voor.',

    'Vier blokken':
        'Vier blokken. Eerst waarom de studie zo is opgezet, dan de meting, dan '
        'het traject bezoek per bezoek, en tot slot de toestellen en de regels. '
        'Ik hou tijd vrij na elk blok.',

    '144 patiënten, 24 per centrum':
        'Elke stip is een patiënt. Vierentwintig daarvan komen uit úw kliniek, '
        'twaalf in elke arm. Zes keer vierentwintig is honderdvierenveertig. '
        'Blijft één centrum achter, dan haalt de studie het niet.',

    'PARADISE toetst geen werkzaamheid.\nPARADISE toetst overdracht.':
        'Eén zin, en dan ga ik door. Elk onderdeel van PARADISE bestaat al. '
        'Geen enkel onderdeel werkte alleen. Wat wij toetsen is of ze samen wél '
        'werken, in gewone klinieken en onder gewone caseload.',

    # ------------------------------------------------------------ board
    'Van pilot tot laatste patiënt':
        'Vier fasen. We zitten in de pilot; februari 2027 is de harde '
        'startdatum. Daarna twaalf maanden includeren, en achttien maanden '
        'opvolgen per patiënt. Alleen de inclusieperiode verschuift de '
        'einddatum.',

    'Vier toezeggingen':
        'Dit is wat we van uw organisatie vragen. Vierentwintig inclusies over '
        'twaalf maanden, dus gemiddeld twee per maand. Verder één vaste PI, tijd '
        'bij de baseline, en een looppad van tien meter. Wat we níét vragen is '
        'gegevensinvoer.',

    "Vier risico's, en wat we eraan doen":
        "Vier risico's, en wat we eraan doen. Het grootste is niet "
        'wetenschappelijk maar organisatorisch: of de centra hun vierentwintig '
        'halen. De andere drie zijn ingecalculeerd. Welk risico baart ú het '
        'meest zorgen?',

    # ------------------------------------------------------ blok 1, waarom
    # De boog van blok 1: inzet, spanning, mislukking, verklaring, omslag.
    # Elke dia geeft de volgende door; lees ze één keer na elkaar en u hoort het.
    'Waarom zo':
        'Blok één. Ik geef u vier cijfers. Na het vierde weet u waarom deze '
        'studie twee normen heeft in plaats van één, en waarom niemand die tot '
        'nu toe samen gehaald heeft.',

    'krijgt binnen een jaar\neen nieuw ulcus':
        'Veertig procent krijgt binnen één jaar een nieuw ulcus. Na vijf jaar is '
        'dat vijfenzestig. En de sterfte ligt tweeënhalf keer hoger dan bij '
        'diabetes zonder ulcus — na een amputatie zelfs boven de zeventig '
        'procent. Dit is geen wondprobleem. Dit is een overlevingsprobleem.',

    'Driekwart is te voorkomen.\nVeertig procent komt terug.':
        'En dan het cijfer dat het onverdraaglijk maakt. Driekwart van deze '
        'ulcera is in principe te voorkomen. Toch komt veertig procent binnen '
        'het jaar terug. Dat gat tussen wat kan en wat gebeurt — daar gaat deze '
        'studie over.',

    "Drie strategieën, één patroon":
        'Het is niet zo dat niemand het geprobeerd heeft. Drukgestuurd '
        'schoeisel haalde zijn eindpunt niet. Educatie alleen had zelfs een '
        'negatief mediaan effect. Digitale feedback werkte, maar opnieuw alleen '
        'bij wie het toestel bleef gebruiken.',

    'Waarom druk alléén niet volstaat':
        'Dit is de beste poging die er ligt: drukgeoptimaliseerd maatschoeisel, '
        'multicentrisch en gerandomiseerd. Over iedereen samen: geen verschil. '
        'Bij wie hem dróég: bijna gehalveerd. Het verschil zat dus niet in de '
        'schoen.',

    'draagtijd — gemeten,\nniet gevraagd':
        'Daar zit het. Eenenzeventig procent draagtijd, gemeten met een sensor '
        'en niet gevraagd. Thuis zakt het naar eenenzestig, en juist thuis '
        'worden de meeste stappen gezet. De schoen stond in de gang terwijl de '
        'patiënt door het huis liep.',

    'Belasting is een product,\ngeen optelsom':
        'Belasting is een product, geen optelsom. Piekdruk maal activiteit maal '
        'draagtijd. Eén factor op nul maakt het hele product nul. Een perfecte '
        'zool in de kast beschermt niets.',

    'Drie dingen zijn veranderd':
        'Waarom kan deze studie nu pas? Drie dingen zijn veranderd. De sensor '
        'maakt therapietrouw meetbaar, COM-B verklaart waaróm educatie faalde, '
        'en België heeft erkende voetklinieken met opleidingseisen. De '
        'onderdelen liggen er dus klaar.',

    'Eén dienst, geen drie losse maatregelen':
        'Daarom doen wij het anders. Geen drie losse maatregelen, maar één '
        'dienst met twee normen: de zool moet de druk hálen, én hij moet '
        'gedragen wórden. Beide gemeten, beide bijgestuurd, en beide door uw '
        'eigen team. Dat is nog nooit samen getoetst.',

    # ------------------------------------------------------ blok 2, meting
    'De meting':
        'Blok twee: de meting. Wat u meet, hoe u het meet, en wanneer het goed '
        'genoeg is.',

    'Elke sensor een cijfer':
        'Elke sensor geeft een cijfer. Dit is de baseline, blootsvoets: '
        'driehonderdtwaalf kilopascal onder metatarsaal twee-drie. Drie metingen '
        'per voet, waar de software één beeld van maakt. Hiertegen wordt alles '
        'afgezet.',

    "Acht regio's, drie doelregio's":
        "De software verdeelt de voet in acht regio's. Daarvan kiest u er drie "
        'als doelregio. Die drie zet u op het voorschrift. En alleen dáár wordt '
        'de norm getoetst, niet over de hele voet.',

    'Wanneer is het goed genoeg':
        'Zelfde voet, na aanpassing. Honderdzesentachtig kilopascal: veertig '
        'procent lager én onder de tweehonderd. De norm geldt per doelregio. '
        'Haalt u ze niet, dan past u aan en meet u opnieuw.',

    'Niet minder belasting.\nBelasting op een plek die het aankan.':
        'Even stilstaan. Het doel is niet minder belasting. Het doel is '
        'belasting op een plek die het aankan. Dat is de hele interventie.',

    'Drie condities bij de aflevering':
        'Drie condities, altijd in deze volgorde. Blootsvoets is uw referentie. '
        'In de schoen zonder zool toont wat het schoeisel alleen doet. In de '
        'schoen mét zool is de meting waarop de norm getoetst wordt — slaat u er '
        'één over, dan is de vergelijking onbruikbaar.',

    # ----------------------------------------------------- blok 3, traject
    'Het traject':
        'Blok drie: het traject. Negen contactmomenten. Per moment: wat u doet '
        'en wat u invult.',

    'Screening plus negen visites':
        'Screening en negen visites over achttien maanden. De eerste drie liggen '
        'dicht op elkaar. Daarna is het ritme elke drie maanden — hetzelfde '
        'ritme als de controle die deze patiënten toch al krijgen.',

    'Geschiktheid, toestemming, loting':
        'Screening en visite nul. De volgorde ligt vast: screenen, tekenen, '
        'geschiktheid bevestigen, en pas dan loten. Vul geen enkel ander '
        'formulier in vóór de handtekening. Ook een afwijzing noteert u, want '
        'ook dat is studiedata.',

    'Wie komt in aanmerking':
        'Categorie drie volgens IWGDF: een genezen plantair ulcus, of een kleine '
        'amputatie. Links wat toelaat, rechts wat uitsluit. De rode draad: '
        'offloading moet de juiste behandeling zijn, dus kritieke ischemie en '
        'actieve Charcot vallen af.',

    'Baseline — meten en voorschrijven':
        'Visite één, het langste bezoek van de studie. Meten, voorschrijven, '
        'vragenlijsten en het eerste educatiegesprek. Twee dingen liggen vast: '
        'het voorschrift gebeurt hier en niet later, en NAFF en HLS gaan vóór de '
        'educatie.',

    'Aflevering, optimalisatie en sensor':
        'Visite twee, veertien dagen tot één maand later. Technisch het zwaarste '
        'bezoek: afleveren, pasvorm in binnen- én buitenschoeisel, meten, '
        'aanpassen tot de norm gehaald is. Pas dán gaat de Orthotimer in de '
        'zool, en pas dan bestelt u het tweede paar.',

    'Driemaandelijkse opvolging':
        'Visites drie tot acht, elke drie maanden. Screenen, uitlezen, '
        'bespreken, en beide paren zolen beoordelen. Uitlezen kan alleen ter '
        'plaatse: een gemiste uitlezing verzwakt de draagtijd van die patiënt '
        'over de hele periode.',

    'Wat er drie keer extra bij komt':
        'Op maand zes, twaalf en achttien komt er een drukmeting bij. Drie keer, '
        'niet twee. Dezelfde drie condities, dezelfde toetsing per doelregio. '
        'Ligt de piekdruk er weer boven, dan past u opnieuw aan.',

    'Terug naar het geheel':
        'Tien contactmomenten, één zorgpad. Het verschil met vandaag zit niet in '
        'hoe vaak u de patiënt ziet, maar in wat u bij elk bezoek wéét: wat de '
        'zool doet, en wat er gedragen is.',

    # -------------------------------------------------- blok 4, toestellen
    'Toestellen en regels':
        'Blok vier: de toestellen en de regels. De instellingen, het gesprek, en '
        'de vier dingen die vastliggen.',

    'Drie toestellen':
        'Drie toestellen, drie taken. De pedar meet druk, de Orthotimer meet of '
        'de zool gedragen is, de MoveMonitor meet hoeveel er gestapt wordt. '
        'Alleen de pedar bedient u bij elke meting; de andere twee plaatst u één '
        'keer en leest u uit.',

    'Negen bij dertien millimeter.\nMeer merkt de patiënt niet.':
        'Zo klein is de sensor: negen bij dertien millimeter. Hij zit in de '
        'zool, meet alleen temperatuur, en de patiënt merkt er niets van. Noem '
        'hem tegenover de patiënt gewoon "uw sensor".',

    'Hoe de CMFO is opgebouwd':
        'De opbouw hangt af van het schoentype. In een volledig maatgemaakte '
        'schoen vijf millimeter kurk met vijf millimeter EVA; in een '
        'confectieschoen zes millimeter EVA, zonder kurk. De rest is gelijk. Dit '
        'staat op het voorschrift — u moet het herkennen, niet onthouden.',

    'Orthotimer instellen':
        'Interval vijftien minuten, batterij ongeveer honderd dagen. Daarom leest '
        'u elke drie maanden uit én vervangt u. Registreer het toestelnummer bij '
        'elke wissel, anders is de draagtijd niet toewijsbaar.',

    'MoveMonitor instellen':
        'Een volle week, op de onderrug. Op de baseline, en opnieuw op maand '
        'zes. Zeg expliciet dat hij niet waterdicht is. Uit deze week komt de '
        'tachtig-procentnorm van díe patiënt.',

    'Vijf gespreksmomenten':
        'SEBIA is vijf gesprekken, geen enkele sessie. Eerst kennis en educatie, '
        'dan teach-back bij de aflevering, dan tweemaal de sensordata samen '
        'bekijken, dan voordoen, en op achttien maanden afsluiten. Het verschil '
        'met gewone educatie: het herhaalt, en het staat op data.',

    'Meetwaarden gaan\nniet naar de\ncontrolegroep':
        'Dit is de enige regel die u écht moet onthouden. De controlegroep krijgt '
        'ook een meting en een sensor, maar die getallen blijven dicht. Bespreekt '
        'u ze, dan lévert u de interventie. Klinische bevindingen zijn géén '
        'meetwaarden: een laesie meldt en behandelt u meteen, in beide groepen.',

    # ------------------------------------------- blok 4 congres, statistiek
    'Eindpunten en analyse':
        'Blok vier: de eindpunten en de analyse. Twee eindpunten, één op één op '
        'het causale model.',

    'Twee eindpunten, twee berekeningen':
        'Twee eindpunten betekent twee berekeningen. Links recidief: vijftig '
        'tegenover vijfentwintig procent, wat eenenveertig events vraagt en '
        'honderddertig deelnemers. Rechts therapietrouw: vijftig per groep. '
        'Honderdvierenveertig komt uit de capaciteit per centrum en overtreft '
        'beide minima.',

    'De power die telt, is de gezamenlijke':
        'En dan de vraag die u anders uit de zaal krijgt. Apart hebben we '
        'vierentachtig en zevenentachtig procent power. Maar de studie is pas '
        'positief als béíde eindpunten halen, en dan zakt het naar vierenzeventig '
        'tot vierentachtig. Wij rapporteren dat zelf, want de losse cijfers '
        'overschatten de kans.',

    'Hoe we het toetsen':
        'Het analyseplan in vier regels. Recidief met Cox, gestratificeerd naar '
        'centrum, met sterfte als competing risk. Therapietrouw met '
        'beta-regressie, want het is een proportie met een plafond. En de twee '
        'eindpunten zijn elkaars intercurrente event: wie ulcereert, draagt '
        'terecht geen zool meer.',

    'Twee evaluaties, parallel':
        'Naast de trial lopen twee evaluaties. De economische rekent kosten per '
        'vermeden ulcus én per QALY, met een Markov-model tot vijf jaar. De '
        'procesevaluatie meet of de interventie werkelijk geleverd is. Die '
        'tweede is geen bijlage — bij een nulresultaat is zij het enige wat '
        'mechanisme van uitvoering onderscheidt.',

    'Een nulresultaat is ook een resultaat':
        'Ik sluit af met wat we hoe dan ook leren. Stijgt de therapietrouw maar '
        'het recidief niet, dan faalt de biomechanische premisse. Stijgt de '
        'therapietrouw niet, dan faalde het gedragsdeel. In beide gevallen weten '
        'we welke schakel breekt, en dat is precies wat dit veld nog niet weet.',

    # ------------------------------------------------------------- afronding
    'Voorvallen en afwijkingen':
        'Wat u meldt, en hoe snel. Een nieuw ulcus is de primaire uitkomst, dus '
        'dat meldt u altijd. Ernstige voorvallen binnen vierentwintig uur na '
        'kennisname. En onthoud dit: een afwijking die u meldt is een gegeven, '
        'een afwijking die u niet meldt is een fout in de data van de hele '
        'studie.',

    'Wie doet wat':
        'Vier rollen. De podoloog meet, leest uit en begeleidt. De pedorthist '
        'maakt en past aan. De arts bevestigt geschiktheid en beoordeelt laesies. '
        'Het management houdt tijd vrij en bewaakt de vierentwintig.',

    'Wat u van ons krijgt':
        'En dit krijgt u van ons. Training in motiverende gespreksvoering, '
        "SOP's per handeling, één contactpunt, en het onderzoeksteam voert de "
        'gegevens in. Nul sancties: wijkt u af, dan meldt u het, en dat wordt '
        'geregistreerd, niet afgestraft.',

    'Vooruitlopend':
        'Dit is een vangnet, geen programma. Toon hem alleen als de vragen '
        'opdrogen, en beantwoord dan alleen wat nog niet aan bod kwam.',

    'Vanaf de eerste patiënt\ndoet u dit zelf.':
        'Rustig zeggen; het is geen dreigement maar een vaststelling. Wij leiden '
        'op en wij voeren in. De handelingen zijn van u, vanaf de eerste '
        'patiënt.',

    'Kunt u dit nu zelf?':
        'Loop deze lijst met uzelf af. Bij elk punt: kunt u het nu zelf, of hebt '
        'u er nog een keer oefening voor nodig? Wie twijfelt, zegt het nu. Dat '
        'is geen probleem — het niet zeggen wel.',

    'Het opleidingsregister':
        'ISO 14155 vraagt dat per medewerker aantoonbaar is welke training hij '
        'kreeg en voor welke handelingen hij gedelegeerd is. Vandaag tekenen. Bij '
        'elke nieuwe medewerker opnieuw, en bij elke protocolwijziging opnieuw. '
        'Het register blijft bij u; wij krijgen een kopie.',

    'referenties':
        'Deze dia laat u staan tijdens de vragen. Alles wat u genoemd hebt, '
        'staat hier met nummer en citaat, in dezelfde nummering als het '
        'protocolmanuscript.',

    # ------------------------------------------------- werkplan sep-nov 2026
    'Wat er de komende dertien weken loopt':
        'Vier sporen, en ze lopen tegelijk. Opstart, materiaal, publiceren en het '
        'doctoraat. Wie ze na elkaar plant haalt februari niet, want het materiaal '
        'moet af zijn vóór de opleiding en de opleiding vóór de droogloop.',

    'Drie maanden, drie doelen':
        'September legt de basis, oktober is ontwerpen, november is de praktijk. '
        'Oktober is de zwaarste maand en het meeste ervan is ontwerpwerk. Februari '
        'staat vast — alles ervoor schuift, die datum niet.',

    'September':
        'Blok één: september. De basis leggen. Bijna alles in oktober hangt aan deze '
        'maand, dus wat hier blijft liggen, kost dubbel.',

    'Vijf dingen die af moeten':
        'Vijf dingen, en één ervan is stiller dan de rest. Het protocol sluitend '
        'maken kost drie dagen. Maar zonder aangestelde statisticus is er geen SAP, '
        'en het SAP moet vóór de eerste patiënt vastliggen. Die naam wil ik vandaag.',

    'Wie je nu moet vragen':
        'Twee commissies, en met opzet niet dezelfde mensen. De begeleidingscommissie '
        'draagt het doctoraat; de adjudicatiecommissie beoordeelt elk ulcus '
        'geblindeerd en moet daarom buiten de zes centra staan. Begin nu: mensen van '
        'buiten vragen bedenktijd.',

    'Oktober':
        'Blok twee: oktober. Ontwerpen en vastleggen. Alles wat in november gebruikt '
        'wordt, moet deze maand af zijn.',

    'Vastleggen wat november gebruikt':
        'Vier vaste punten deze maand. Registreren kan nu het protocol stabiel is, en '
        'dat nummer deblokkeert meteen de indiening van de paper. Het fotoplatform '
        'heeft de langste doorlooptijd buiten onze controle — daar begin ik in week '
        'vijf aan, ook al is het pas in november af.',

    'Wat er nog niet is':
        'Drie documenten bestaan niet en drie moeten om. De werkinstructie voor de '
        'pedar ontbreekt volledig, terwijl de centra dat toestel zelf bedienen. Reken '
        'ruim voor patiëntmateriaal: elke zin moet én kloppen én begrijpelijk zijn.',

    'November':
        'Blok drie: november. Van papier naar de meettafel. Zes opleidingen, zes '
        'drooglopen, en de paper de deur uit.',

    'Naar de praktijk':
        'Zes opleidingen en zes drooglopen, elk een halve dag. De droogloop is het '
        'punt van de hele maand: daar ontdek je dat het ziekenhuisnetwerk de '
        'uitleessoftware blokkeert, of dat het looppad als opslagruimte gebruikt '
        'wordt. Dat wil je nu weten en niet bij patiënt één.',

    'Foolproof maken':
        'Blok vier: foolproof maken. Zes regels, en elk ervan komt uit een fout die '
        'deze zomer werkelijk in dit project zat.',

    'Wat een fout onzichtbaar maakt':
        'Drie manieren waarop een fout onzichtbaar blijft. Dezelfde tekst op twee '
        'plaatsen loopt uit elkaar — dat gebeurde in de MOOC en een week lang stond er '
        'een verkeerd antwoord. Een veld dat zichzelf invult met twaalf uur levert '
        'percentages op die er normaal uitzien en nergens op slaan.',

    'Wat een fout tegenhoudt':
        'En drie manieren om ze tegen te houden. Laat het systeem liever niets doen '
        'dan iets aannemelijks. Druk de eenheid voor en maak van "niet gemeten" een '
        'vakje. En schrijf de instructie mét degene die de handeling doet, niet voor '
        'hem.',

    'Geef het aan iemand\ndie de studie\nniet kent':
        'Dit is de goedkoopste controle die er is. Geef het formulier en het toestel '
        'aan iemand die de studie niet kent, kijk toe en zeg niets. Waar hij aarzelt '
        'is het ontwerp fout, niet de collega. Een halve dag, en het vangt meer dan '
        'een week nalezen.',

    'Wie hoeveel':
        'De verdeling is scheef en dat hoort ook: voorbereidend werk is '
        'coördinatiewerk. Veertig dagen bij mij, vijf à zes bij Kevin, vijf bij de '
        'statisticus in oktober, en één dag per centrum. Die laatste is de enige die '
        'ik niet zelf in de hand heb.',

    'Waaraan u ziet dat het klaar is':
        'Acht punten, en ze zijn allemaal aantoonbaar. Geen inschattingen maar dingen '
        'die er zijn of niet zijn. Wat op één december nog openstaat, wordt in februari '
        'een protocolafwijking op een patiënt.',

    'Februari verschuift niet.\nAlles ervoor wel.':
        'Rustig zeggen en dan zwijgen. Dit is de reden dat het zware werk in oktober '
        'staat en niet in januari.',

    'Voor als er iets misloopt':
        'Tot slot: wie u aanspreekt. Praktische vragen — inclusies, metingen, '
        'formulieren, sensoren — komen bij mij. Wetenschappelijke vragen en '
        'afspraken op het niveau van uw centrum bij professor Deschamps. Dank u '
        'wel.',
}
