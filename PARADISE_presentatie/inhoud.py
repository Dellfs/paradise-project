# -*- coding: utf-8 -*-
"""PARADISE — opleidingssessie voor de zes diabetische voetklinieken.

De centra zitten al in het consortium; deze sessie leidt hun medewerkers op.
Het deck is daarom een werkdocument: plenair, met rolblokken, en bezoek per
bezoek met de eCRF-documenten erbij.

Ontwerpprincipes: dark mode, bento-grid, één kernboodschap per dia, typografie
als visueel element, geen opsommingstekens. Elke dia draagt een morph-overgang.

Bronnen. De handelingen komen uit de eCRF-set in (e)CRF\\Per nummer, met name
01 (screening), 09 en 24 (drukmetingen), 17 (SEBIA-script), 19b en 25b (de
SOP's) en 28 (activiteitenprofiel). De cijfers komen uit het protocol
(versie 1.0, 17/05/2026) en het geverifieerde manuscript.
"""

# Huisstijl PARADISE: par-dark #00407A, par-mid #1D8DB0, par-light #52BDEC,
# par-orange #FF7A00. De grond en de tegels zijn donkere tinten van par-dark,
# zodat het hele deck uit dezelfde blauwfamilie komt.
K = {
    'bg':      '04182A',
    'grond2':  '072138',
    'tegel':   '0A2A44',
    'tegel2':  '113A57',
    'glas':    '17486B',
    'rand':    '215B84',
    'ink':     'F2F8FC',
    'gedempt': '8FB6D0',
    'navy':    '00407A',
    'mid':     '1D8DB0',
    'licht':   '52BDEC',
    'oranje':  'FF7A00',
    'wit':     'FFFFFF',
}

FONT = 'Segoe UI'
FONT_L = 'Segoe UI Light'
FONT_M = 'Consolas'

MARGE, GOOT, KOLOM = 100, 24, 121.33


def kol(i, span=1):
    x = MARGE + i * (KOLOM + GOOT)
    w = span * KOLOM + (span - 1) * GOOT
    return x, w


# Het traject staat apart: vijf dia's tekenen hetzelfde canvas onder een andere
# camera-instelling, dus de gegevens mogen maar op één plek staan.
# De derde waarde is het soort moment; die bepaalt de kleur van de stip.
# Bezoekstructuur volgens protocol 5.5: screening vóór toestemming, dan visite 0
# tot 8. Het voorschrift valt op visite 1 en de aflevering op visite 2, tussen
# veertien dagen en één maand — niet op maand 1 en maand 3.
PUNTEN = [('Screen', 'geschiktheid', 'start'),
          ('V0', 'loting', 'start'),
          ('V1', 'baseline', 'meting'),
          ('V2', 'zool + sensor', 'meting'),
          ('M3', 'opvolging', 'zorg'),
          ('M6', 'meting', 'meting'),
          ('M9', 'opvolging', 'zorg'),
          ('M12', 'meting', 'meting'),
          ('M15', 'opvolging', 'zorg'),
          ('M18', 'meting + einde', 'eind')]

SOORT = [('meting', 'meetmoment'), ('zorg', 'begeleiding'),
         ('start', 'start en afronding')]

CENTRA = ['AZORG', 'AZ Sint-Jan Brugge', 'AZ Groeninge',
          'UZ Gent', 'UZ Leuven', 'UZ Antwerpen']


# Uit dezelfde inhoud worden zes decks gebouwd. Elke dia draagt een label `voor`
# met de letters van de decks waarin hij hoort:
#   o opleiding · b board · c congres · u outreach · k kort · e extern
DECKS = {
    'opleiding': dict(
        letter='o', bestand='PARADISE_opleidingssessie_voetklinieken.pptx',
        onder='Opleidingssessie · zes voetklinieken',
        duur='60 tot 75 minuten', uitklappen=True,
        wie='De medewerkers van de zes deelnemende voetklinieken.'),
    'board': dict(
        letter='b', bestand='PARADISE_board.pptx',
        onder='Stand van zaken · stuurgroep en directie',
        duur='15 tot 20 minuten',
        wie='Ziekenhuisdirectie, stuurgroep en financier. Wat het is, hoe groot, '
            'wat het van de organisatie vraagt.'),
    'congres': dict(
        letter='c', bestand='PARADISE_congres.pptx',
        onder='Studieopzet · wetenschappelijke sessie',
        duur='15 minuten',
        wie='Vakgenoten. Volgt de opbouw van het protocolmanuscript: rationale, '
            'ontwerp, eindpunten, power en analyseplan.'),
    'outreach': dict(
        letter='u', bestand='PARADISE_outreach.pptx',
        onder='Waarom deze studie er is',
        duur='10 minuten',
        wie='Breed publiek, patiëntenverenigingen, pers. Geen jargon, geen '
            'formuliernummers.'),
    'kort': dict(
        letter='k', bestand='PARADISE_centra_kort.pptx',
        onder='Opfrissing voor de centra',
        duur='20 minuten',
        wie='Medewerkers die de opleiding al volgden. Het traject, de regels en '
            'de contactgegevens.'),
    'extern': dict(
        letter='e', bestand='PARADISE_extern.pptx',
        onder='Het onderzoek en het netwerk',
        duur='15 minuten',
        wie='Externe partners, andere ziekenhuizen, industrie.'),
}


SLIDES = [

 dict(t='titel_foto', voor='obcuke', morph='fade', foto='plaatshouder.png',
      boven='PARADISE', onder='Opleidingssessie \u00b7 zes voetklinieken',
      voet='Protocolversie 1.0 \u00b7 17 mei 2026 \u00b7 S71769',
      tip='Het beeld draagt deze dia, dus de foto moet raak zijn. Zet hem in '
          'beeld\\stock\\, draai verwerk_stock.py, en vervang het kader met '
          'rechtsklik en Afbeelding wijzigen. Liggend, koele tonen, en rustig '
          'onderaan \u2014 daar staat de titel.',
      interactie='Laat de dia staan terwijl de zaal binnenkomt. Zeg pas iets als '
                 'iedereen zit.'),

 dict(t='doel', voor='ok', morph='morph',
      kicker='Waarom u hier zit',
      kop='Na vandaag kunt u dit zelf',
      doelen=[('Screenen', 'beoordelen of een patiënt in aanmerking komt, en de '
                           'screening vastleggen vóór de toestemming'),
              ('Meten', 'een drukmeting uitvoeren die aan het protocol voldoet, '
                        'en de drie doelregio\'s bepalen'),
              ('Optimaliseren', 'de zool aanpassen tot de norm gehaald is, en '
                                'vastleggen wat u aangepast hebt'),
              ('Uitlezen', 'de Orthotimer en de MoveMonitor correct instellen, '
                           'uitlezen en terugkoppelen'),
              ('Begeleiden', 'een SEBIA-gesprek voeren, inclusief teach-back'),
              ('Vastleggen', 'de formulieren volledig invullen, en weten wat u '
                             'meldt als er iets afwijkt')],
      slot='Wie een van deze zes niet aandurft na vandaag, moet dat zeggen. '
           'Daar is deze sessie voor.',
      tip='Loop de zes titels traag door. Dit is de belofte van de dag en het '
          'is ook precies de bekwaamheidscheck op het eind.',
      interactie='Laat iedereen op een blad de zes overschrijven en aanduiden '
                 'welke ze al beheersen. Op het eind vullen ze dat opnieuw in.'),

 dict(t='keuze', voor='o', morph='morph',
      kicker='Programma van vandaag',
      kop='Vier blokken',
      tegels=[('01', 'Waarom zo', 'De vier cijfers achter de twee normen'),
              ('02', 'De meting', 'Drukmeting, doelregio\'s en de norm'),
              ('03', 'Het traject', 'Bezoek per bezoek, met de formulieren'),
              ('04', 'Toestellen en regels', 'SOP\'s, SEBIA, blindering, melden')],
      tip='Blok 3 is het langste en het belangrijkste. Plan uw tijd zo dat u '
          'daar niet doorheen moet jagen.',
      interactie='Vraag of iemand een blok wil ruilen van plaats. Wie kiest, '
                 'luistert beter.'),

 dict(t='statraster', voor='obcuke', morph='morph',
      kicker='Waar we staan',
      kop='144 patiënten, 24 per centrum',
      klein=[('Per centrum', '24 deelnemers — 12 PARADISE en 12 gebruikelijke zorg'),
             ('Controlegroep', 'Gebruikelijke zorg, onveranderd'),
             ('Co-primair', 'Recidief op 18 maanden, draagtijd op 12'),
             ('Positief', 'Alleen als béíde eindpunten halen')],
      centra=CENTRA,
      centra_label='De zes deelnemende voetklinieken',
      tip='Wijs hun eigen centrum aan: 24 van die 144 stippen zijn van hen. Zes '
          'keer 24 is 144 — als één centrum achterblijft, haalt de studie het niet.',
      interactie='Vraag of ze de andere vijf centra kennen. Het maakt van zes '
                 'losse klinieken één netwerk.'),

 dict(t='fasen', voor='be', morph='morph',
      kicker='Waar we staan',
      kop='Van pilot tot laatste patiënt',
      fasen=[('sep 2026 \u2013 feb 2027', 'Pilot',
              'Protocol en meetprocedures uitproberen in de zes centra. '
              'Opleiding en bekwaamheidscheck.', True),
             ('feb 2027 \u2013 feb 2028', 'Inclusie',
              'Twaalf maanden rekruteren. 24 deelnemers per centrum, twee per '
              'maand.', False),
             ('tot sep 2029', 'Opvolging',
              'Elke deelnemer achttien maanden. De laatste inclusie bepaalt '
              'de einddatum.', False),
             ('2029 \u2013 2030', 'Analyse',
              'Uitkomsten, gezondheidseconomie en procesevaluatie. \u00c9\u00e9n '
              'publicatie, ongeacht de uitkomst.', False)],
      slot='De inclusieperiode is het enige wat de einddatum verschuift. Elke '
           'maand vertraging in de rekrutering is een maand later klaar.',
      tip='Dit is de dia waar het board naar kijkt. Zeg expliciet dat de pilot '
          'nu loopt en dat februari 2027 de harde startdatum is.',
      interactie='Vraag of hun centrum de twee inclusies per maand haalbaar acht.'),

 dict(t='melden', voor='b', morph='morph',
      kicker='Wat we van uw organisatie vragen',
      kop='Vier toezeggingen',
      rijen=[('24 inclusies', 'Over twaalf maanden, dus gemiddeld twee per maand. '
                              'Onder de twaalf per centrum wordt de studie '
                              'onderbemand.', '24'),
             ('Eén vaste PI', 'Plus een gedelegeerd team dat de opleiding volgt en '
                              'het opleidingsregister tekent.', '1'),
             ('Tijd per bezoek', 'Baseline loopt uit; de andere bezoeken vallen '
                                 'samen met de controle die de patiënt al krijgt.',
                                 '9'),
             ('Een looppad', 'Tien meter volstaat. Meer ruimte of extra apparatuur '
                             'is niet nodig.', '10 m')],
      slot='Wat we níét vragen: gegevensinvoer. Dat doet het onderzoeksteam.',
      tip='Dit is de vraag. Wees concreet en beloof niets over wat u niet weet.',
      interactie='Vraag per punt of het haalbaar is. Twijfel nu is beter dan '
                 'uitval straks.'),

 dict(t='melden', voor='be', morph='morph',
      kicker='Wat er mis kan gaan',
      kop='Vier risico\'s, en wat we eraan doen',
      rijen=[('Te trage inclusie', 'Gefaseerde rekrutering is voorzien; de '
                                   'haalbaarheid per centrum wordt in de pilot '
                                   'getoetst.', 'hoog'),
             ('Contaminatie tussen de armen', 'Blindering in de software van alle '
                                              'toestellen, aparte formulieren per '
                                              'arm, en een SEBIA-boekje ook in de '
                                              'controlegroep.', 'middel'),
             ('Uitval', 'Vijftien procent is ingecalculeerd in de '
                        'steekproefberekening.', 'middel'),
             ('Beide eindpunten moeten halen', 'De lat ligt hoog en dat is een '
                                               'bewuste keuze: druk zonder '
                                               'draagtijd zegt niets.', 'laag')],
      slot='Het grootste risico is niet wetenschappelijk maar organisatorisch: '
           'of de centra hun 24 halen.',
      tip='Benoem het inclusierisico eerst en zelf. Als het board het moet '
          'opmerken, bent u de regie kwijt.',
      interactie='Vraag welk risico zij zelf het grootst achten.'),

 dict(t='knal', voor='c', morph='morph', kleur='licht', kleur2='mid',
      kop='PARADISE toetst geen werkzaamheid.\nPARADISE toetst overdracht.',
      onder='Elk onderdeel bestaat al. Geen enkel onderdeel werkte alleen.'),

 dict(t='sectie', voor='obcue', morph='morph', nr='01', titel='Waarom zo',
      regel='Vier cijfers verklaren waarom er twee normen zijn.'),

 dict(t='hero_cijfer', voor='obcuke', morph='morph',
      cijfer='40', suffix='%',
      kop='krijgt binnen een jaar\neen nieuw ulcus',
      tegels=[('65%', 'na vijf jaar'), ('2,5×', 'hogere sterfte'),
              ('> 70%', 'sterfte na amputatie')],
      voet='Armstrong, Boulton & Bus · N Engl J Med 2017',
      accent='oranje',
      tip='Dit is het probleem waar de hele studie op staat. Eén dia, dan door.',
      interactie='Geen. Dit is context, geen discussie.'),

 dict(t='knal', voor='obcuke', morph='morph',
      kop='Driekwart is te voorkomen.\nVeertig procent komt terug.',
      onder='Dat gat is waar deze studie over gaat.',
      tip='Zeg dit traag en zwijg dan twee tellen. Dit is de enige dia in blok '
          '1 waar de zaal niet leest maar luistert.',
      interactie='Geen. De stilte doet het werk.'),

 dict(t='melden', voor='c', morph='morph',
      kicker='Wat er al geprobeerd is',
      kop='Drie strategie\u00ebn, \u00e9\u00e9n patroon',
      rijen=[('Drukgestuurd schoeisel',
              'De pivotale multicentrische trial haalde haar primaire eindpunt '
              'niet: 38,8% tegenover 44,2% recidief. Het verschil zat bij wie de '
              'schoen dr\u00f3\u00e9g.', 'p = 0,48'),
             ('Patienteneducatie',
              'In de IWGDF-review had losstaande educatie geen aantoonbaar '
              'preventief effect. Het mediane behandeleffect was negatief.',
              'mediaan \u221213,4%'),
             ('Continue digitale feedback',
              'Een slimme inlegzool met realtime waarschuwingen verminderde '
              'recidief \u2014 opnieuw vooral bij wie het toestel bleef gebruiken.',
              'proof of concept'),
             ('Het patroon', 'Elk onderdeel adresseert een noodzakelijke '
                             'voorwaarde. Geen enkel onderdeel adresseert een '
                             'voldoende voorwaarde.', '\u2014')],
      slot='Geen drie teleurstellingen maar \u00e9\u00e9n: telkens echt, telkens voorwaardelijk.',
      tip='Dit is de dia die de zaal het argument geeft. Neem er tijd voor; de '
          'rest van de studieopzet volgt hieruit.',
      interactie='Geen.'),

 dict(t='splitsing', voor='obce', morph='morph',
      kicker='Dezelfde schoen, twee uitkomsten',
      kop='Waarom druk alléén niet volstaat',
      links=dict(titel='Iedereen', sub='intention-to-treat', groot='38,8',
                 ref=44.2, ref_lbl='Gewone maatzool', int_lbl='Drukgeoptimaliseerd',
                 slot='Geen verschil — p = 0,48', kleur='oranje'),
      rechts=dict(titel='Wie hem droeg', sub='≥ 80% van de stappen', groot='25,7',
                  ref=47.8, ref_lbl='Gewone maatzool', int_lbl='Drukgeoptimaliseerd',
                  slot='Bijna gehalveerd — p = 0,045', kleur='licht'),
      punchline='Daarom meten we niet alleen druk, maar ook draagtijd.',
      voet='Bus et al. · Diabetes Care 2013 · DIAFOS, 171 deelnemers',
      tip='Hier komt de tweede norm vandaan. Zonder deze dia is 80% draagtijd '
          'een willekeurig getal.',
      interactie='Geen.'),

 dict(t='hero_cijfer', voor='obce', morph='morph',
      cijfer='71', suffix='%',
      kop='draagtijd — gemeten,\nniet gevraagd',
      tegels=[('61%', 'thuis'), ('4000', 'stappen binnen'), ('2600', 'stappen buiten')],
      meter=dict(label='Draagtijd tegenover de norm van 80%',
                 staven=[('Gemiddeld', 71), ('Thuis', 61), ('Buitenshuis', 87)]),
      voet='Waaijman et al. · Diabetes Care 2013 · 107 patiënten',
      accent='licht',
      tip='Binnenshuis wordt het schoeisel het minst gedragen, en juist daar '
          'worden veel stappen gezet. Dat is uw belangrijkste gesprekspunt bij '
          'SEBIA.',
      interactie='Vraag wat zij schatten bij hun eigen patiënten.'),

 dict(t='formule', voor='obcuke', morph='morph',
      kicker='Het mechanisme',
      kop='Belasting is een product,\ngeen optelsom',
      delen=[('Piekdruk', 'per stap', 'licht', 'Bijgestuurd'),
             ('Activiteit', 'stappen per dag', 'gedempt', 'Gemeten'),
             ('Draagtijd', 'wérd hij gedragen', 'licht', 'Bijgestuurd')],
      slot='Eén factor op nul maakt het product nul. Daarom heeft PARADISE twee '
           'normen: een druknorm én een draagtijdnorm.',
      tip='Dit is het scharnier van blok 1. Wie dit snapt, snapt waarom de '
          'meting én de sensor allebei moeten kloppen.',
      interactie='Morph: de drie tegels komen samen uit één punt.'),

 dict(t='melden', voor='c', morph='morph',
      kicker='Waarom deze studie nu pas kan',
      kop='Drie dingen zijn veranderd',
      rijen=[('Therapietrouw is meetbaar',
              'De temperatuursensor in orthopedisch schoeisel is gevalideerd. '
              'Zelfrapportage overschat systematisch; nu is draagtijd een '
              'toetsbaar doel in plaats van een aanname.', 'sensor'),
             ('De mislukking is verklaarbaar',
              'Kennisoverdracht raakt onder COM-B enkel capability. Opportunity '
              'en motivation \u2014 wat thuis gebeurt, jarenlang, ongezien \u2014 bleven '
              'onaangeroerd.', 'COM-B'),
             ('De context bestaat',
              'Belgi\u00eb erkent multidisciplinaire voetklinieken met '
              'opleidingseisen en minimumvolumes. Dat is de plek waar preventie '
              'uiteindelijk moet landen.', 'RIZIV-INAMI')],
      slot='Daarom is therapietrouw hier een co-primair eindpunt, en geen '
           'mediator die je achteraf afleidt.',
      tip='Drie redenen, drie zinnen. Dit is het scharnier naar de opzet.',
      interactie='Geen.'),

 dict(t='duo', voor='obcuke', morph='morph',
      kicker='Wat PARADISE anders doet',
      kop='E\u00e9n dienst, geen drie losse maatregelen',
      een=dict(nr='01', naam='De zool h\u00e1\u00e1lt de norm',
               kern='< 200 kPa \u00f3f 25% lager',
               regels=['Gemeten bij de aflevering, in drie condities.',
                       "Aangepast tot de norm gehaald is in elk van de drie "
                       "doelregio's.",
                       'Herhaald op maand 6, 12 en 18.']),
      twee=dict(nr='02', naam='En hij w\u00f3rdt gedragen',
                kern='80% van zijn eigen activiteitenprofiel',
                regels=['Een sensor in de zool meet de draagtijd, continu.',
                        'Elke drie maanden uitgelezen en samen bekeken.',
                        'Vijf gesprekken die op die data staan, niet op goede '
                        'raad.']),
      tip='Dit is de kanteldia. Alles ervoor is het probleem, alles erna is de '
          'uitvoering. Zeg met zoveel woorden dat dit nog nooit samen getoetst '
          'is.',
      interactie='Vraag welke van de twee normen zij het moeilijkst achten. '
                 'Het antwoord is bijna altijd de tweede.'),

 dict(t='sectie', voor='obce', morph='morph', nr='02', titel='De meting',
      regel='Wat u meet, hoe u het meet, en wanneer het goed genoeg is.'),

 dict(t='drukmeting', voor='obcuke', morph='morph', fase='voor',
      kicker='Baseline · blootsvoets',
      kop='Elke sensor een cijfer',
      waarde='312', plek='piekdruk op metatarsaal 2-3',
      norm='Norm:  < 200 kPa   óf   ≥ 25% lager',
      regels=['Baseline meet u blootsvoets: de sensoren gaan met dubbelzijdige '
              'tape rechtstreeks op de voet, daarover een standaardkous.',
              'Drie metingen per voet, links en rechts apart. Daaruit berekent '
              'de software één gemiddeld piekdrukbeeld.'],
      voet='eCRF-document 09 · Meting plantaire druk, baseline',
      tip='De meest gemaakte fout is één meting per voet. Het protocol vraagt er '
          'drie, en het gemiddelde telt.',
      interactie='Vraag wie al blootsvoets gemeten heeft met sensoren op de voet.'),

 dict(t='drukzoom', voor='oc', morph='morph', fase='voor',
      kicker='Inzoomen op de voorvoet',
      kop='Acht regio\'s, drie doelregio\'s',
      waarde='312',
      regios=[('Metatarsaal 1', 'onder de grote teen — tweede meest getroffen plek', 0.30, 0.68),
              ('Metatarsaal 2-3', 'de hete plek op deze meting, en de klassieke ulcusplek', 0.44, 0.66),
              ('Metatarsaal 4-5', 'laterale voorvoet, meestal lagere druk', 0.70, 0.63),
              ('Hallux', 'apart bekeken, niet meer samengeteld met de tenen', 0.28, 0.91),
              ('Tenen 2-5', 'eigen regio sinds de laatste maskerversie', 0.55, 0.90)],
      voet='Acht regio\'s via Multimask · hiel en mediale en laterale middenvoet vallen buiten beeld',
      tip='Uit deze acht kiest u er drie om te ontlasten: de regio met de '
          'ulcusvoorgeschiedenis, plus één of twee met de hoogste piekdruk. '
          'Die drie legt u vast — daarop wordt de norm getoetst.',
      interactie='Laat ze op deze dia aanwijzen welke drie zij zouden kiezen.'),

 dict(t='drukmeting', voor='obcuke', morph='morph', fase='na',
      kicker='Na optimalisatie',
      kop='Wanneer is het goed genoeg',
      waarde='186', plek='piekdruk in de doelregio na aanpassing',
      norm='40% lager  ·  onder 200 kPa  ·  beide criteria gehaald',
      regels=['De norm geldt per doelregio: piekdruk onder 200 kPa óf minstens '
              '25% lager dan de baselinemeting van diezelfde regio.',
              'Haalt u de norm niet, dan past u aan en meet u opnieuw. Het '
              'formulier voorziet twee extra ontlastingstests.'],
      voet='eCRF-document 24 · Meting drukherverdeling voetorthese',
      tip='Zeg expliciet: "óf". Twee wegen naar dezelfde norm, geen dubbele eis. '
          'En de vergelijking gebeurt per regio, niet over de hele voet.',
      interactie='Vraag de pedorthisten hoeveel aanpassingsrondes realistisch zijn.'),

 dict(t='knal', voor='obcuke', morph='morph', kleur='oranje', kleur2='oranje',
      kop='Niet minder belasting.\nBelasting op een plek die het aankan.',
      onder='Dat is de hele interventie.',
      tip='Zeg deze twee zinnen en zwijg dan. Laat de dia staan tot iemand '
          'ongemakkelijk wordt. Dit is het enige moment in blok 2 waarop de '
          'zaal niets te lezen heeft.',
      interactie='Geen. Bewust geen.'),

 dict(t='meetreeks', voor='oc', morph='morph',
      kicker='Het meetprotocol',
      kop='Drie condities bij de aflevering',
      condities=[('01', 'Blootsvoets',
                  'Sensoren met dubbelzijdige tape op de voet, standaardkous '
                  'erover. Dit is het referentiebeeld.'),
                 ('02', 'In de schoen, zónder de zool',
                  'Toont wat het schoeisel alleen doet. Dit is de vergelijking '
                  'die laat zien of de zool iets toevoegt.'),
                 ('03', 'In de schoen, mét de zool',
                  'De meting waarop de norm getoetst wordt, per doelregio.')],
      slot='Alle drie de condities staan op hetzelfde formulier. Slaat u er één '
           'over, dan is de vergelijking onbruikbaar.',
      voet='eCRF-document 24 · de norm wordt per doelregio getoetst, niet over de hele voet',
      tip='Dit is de dia waar in de praktijk de meeste fouten gemaakt worden. '
          'Loop de drie condities traag door en benoem dat conditie 2 vaak '
          'vergeten wordt. Dezelfde drie condities komen terug op maand 6, 12 en 18.',
      interactie='Vraag: "wie meet er vandaag al in de schoen zonder zool?"'),

 dict(t='sectie', voor='obcke', morph='morph', nr='03', titel='Het traject',
      regel='Negen contactmomenten. Per moment: wat u doet en wat u invult.'),

 dict(t='traject', voor='obcuke', morph='morph',
      kicker='Het traject',
      kop='Screening plus negen visites',
      groot='18',
      punt='maanden, van screening tot afronding',
      slot='Visite 0 tot 2 liggen dicht op elkaar: toestemming, baseline, en de '
           'zool binnen de maand. Daarna is het ritme elke drie maanden, hetzelfde '
           'ritme als de controle die deze patiënten al krijgen.',
      tip='Geef eerst het overzicht. De volgende dia\'s lopen elk moment af.',
      interactie='Geen. De detaildia\'s komen hierna.'),

 dict(t='bezoek', voor='ok', morph='morph',
      kicker='Screening en visite 0',
      kop='Geschiktheid, toestemming, loting',
      wanneer='Kort \u00b7 in het gewone consult',
      handelingen=['Screening v\u00f3\u00f3r de toestemming: beoordeel de in- en '
                   'exclusiecriteria en noteer de pati\u00ebnt op de identificatielijst.',
                   'Is de pati\u00ebnt geschikt, overloop dan de informatie- en '
                   'toestemmingsformulieren en laat tekenen.',
                   'Visite 0: bevestig de geschiktheid met het baselineformulier.',
                   'De PI opent de volgende verzegelde envelop en deelt de pati\u00ebnt '
                   'in. Pas dan is bekend in welke arm hij zit.',
                   'Niet geschikt? Noteer de reden. Ook dat is studiedata.'],
      documenten=[('00', 'Identificatielijst'), ('01', 'Screening'),
                  ('02', 'Toestemming'), ('06', 'Geschiktheid')],
      letop='De volgorde ligt vast: screenen, tekenen, geschiktheid bevestigen, dan '
            'pas loten. Vul geen enkel ander formulier in voordat de pati\u00ebnt '
            'getekend heeft.',
      wie='Arts bevestigt geschiktheid \u00b7 PI loot \u00b7 podoloog vult in',
      tip='Benadruk dat de loting door de PI gebeurt met verzegelde enveloppen, vier '
          'blokken van zes per centrum. Niemand kiest zelf.',
      interactie='Deel het screeningsformulier uit en laat ze het invullen voor een '
                 'pati\u00ebnt die ze vorige week zagen.'),
 dict(t='dubbelkolom', voor='oc', morph='morph',
      kicker='Screening',
      kop='Wie komt in aanmerking',
      links=dict(titel='Wél', kleur='licht',
                 items=['Volwassen, begrijpt Nederlands',
                        'Diabetes type 1 of 2',
                        'Risicocategorie 3 met genezen plantair ulcus, partiële '
                        'amputatie of resectie van een metatarsaalkop — niet de '
                        'eerste — tussen 18 maanden en 2 weken geleden',
                        'Stapt zelfstandig blootsvoets, zonder hulpmiddelen',
                        'Heeft beschermend schoeisel, of aanvaardt het: volledig '
                        'maatwerk, of maatzolen in semi-orthopedisch of '
                        'extra-diep confectieschoeisel']),
      rechts=dict(titel='Niet', kleur='oranje',
                  items=['Amputatie proximaal van de MTP-gewrichten',
                         'Actief ulcus of Charcot-deformiteit',
                         'Kritische ischemie — PEDIS graad 3',
                         'Immunosuppressieve therapie',
                         'Nierfunctievervangende therapie',
                         'Overleving < 18 maanden, beoordeeld door de arts',
                         'Kan geen toestemming geven of instructies volgen',
                         'Hulpmiddel dat druksensoren belemmert, bv. een EVO',
                         'Weigert het voorgeschreven schoeisel te dragen']),
      tip='Twee criteria worden het vaakst gemist: de resectie mag niet de eerste '
          'metatarsaalkop betreffen, en een enkel-voetorthese sluit uit omdat de '
          'sensoren er niet in passen.',
      interactie='Vraag per criterium of het in hun patiëntenbestand vaak voorkomt.'),

 dict(t='bezoek', voor='ok', morph='morph',
      kicker='Visite 1',
      kop='Baseline \u2014 meten en voorschrijven',
      wanneer='Het langste bezoek van de studie',
      handelingen=['Demografie en voorgeschiedenis, inclusief nierfunctie, eGFR, '
                   'hartaandoening en diabetesmedicatie.',
                   'Voet- en schoeiselscreening, en klasseer een eventueel ulcus.',
                   ('Drukmeting blootsvoets: drie metingen per voet.',
                    'Sensoren met dubbelzijdige tape op de blote voet, kous erover'),
                   ('Bepaal de drie doelregio\'s en schrijf de zool voor, m\u00e9t die '
                    'regio\'s op het voorschrift.',
                    'Schermafdruk van de multimask met de drie regio\'s aangeduid'),
                   'Vragenlijsten v\u00f3\u00f3r het educatiegesprek: NAFF en HLS-EU-6. '
                   'Daarna tevredenheid, schoeiselgebruik en EQ-5D-5L.',
                   'SEBIA stap 1: educatie op maat, voordoen, en de pati\u00ebnt het '
                   'zelf laten uitvoeren. Leg dat vast in het logboek.',
                   ('Geef de MoveMonitor mee voor zeven dagen en registreer het '
                    'toestelnummer.',
                    'Toestel om het middel, ter hoogte van L5')],
      documenten=[('07', 'Demografie'), ('08', 'Voet en schoeisel'),
                  ('09', 'Drukmeting'), ('10', 'Voorschrift CMFO'),
                  ('12', 'Tevredenheid'), ('13', 'Schoeiselgebruik'),
                  ('14', 'NAFF'), ('15', 'HLS-EU-6'),
                  ('16', 'Educatieboekje'), ('18', 'Logboek educatie'),
                  ('19', 'MoveMonitor'), ('20', 'UDI MoveMonitor'),
                  ('21', 'EQ-5D-5L'), ('48', 'Voetzorgfolder')],
      letop='Het voorschrift van de zool gebeurt hier, op de baseline \u2014 niet later. '
            'En NAFF en HLS-EU-6 gaan v\u00f3\u00f3r de educatie, anders meet u uw '
            'eigen uitleg in plaats van de voorkennis van de pati\u00ebnt.',
      wie='Podoloog meet \u00b7 arts schrijft voor \u00b7 het onderzoeksteam verwerkt',
      tip='Dit bezoek loopt uit. Zeg hoeveel tijd u ervoor moet inplannen en waarom de '
          'volgorde vastligt.',
      interactie='Laat ze in duo\'s de volgorde van de handelingen leggen met de '
                 'formulieren op tafel.'),
 dict(t='bezoek', voor='ok', morph='morph',
      kicker='Visite 2 \u00b7 veertien dagen tot \u00e9\u00e9n maand',
      kop='Aflevering, optimalisatie en sensor',
      wanneer='Het technisch zwaarste bezoek',
      handelingen=[('Lever de zool af. Controleer de pasvorm in het b\u00ednnenschoeisel '
                    '\u00e9n het b\u00faitenschoeisel, en neem de foto\'s.',
                    'De zool in de schoen, boven- en onderaanzicht'),
                   'Meet de drukherverdeling en toets de norm per doelregio.',
                   'Niet gehaald? Pas aan en meet opnieuw. Is ze gehaald, laat dan een '
                   'tweede, identiek paar maken.',
                   ('Plaats en activeer de Orthotimer in de zool en registreer het '
                    'toestelnummer.',
                    'De uitsparing in de zool met de sensor erin'),
                   'Neem de MoveMonitor terug en registreer de teruggave.',
                   'SEBIA stap 2: bespreek het activiteitenprofiel, doe de teach-back '
                   'en geef de sensorfolder mee.',
                   'Bevraag de overtuigingen en gewoontes rond schoeisel.'],
      documenten=[('23', 'Aanpassing'), ('24', 'Drukherverdeling'),
                  ('24b', 'Opvolgtool'), ('25', 'UDI Orthotimer'),
                  ('26', 'Overtuigingen'), ('27', 'Teruggave MoveMon.'),
                  ('28', 'Activiteitsprofiel'), ('29', 'Teach-back'),
                  ('30', 'Sensorfolder')],
      letop='De Orthotimer gaat pas in de zool nadat de norm gehaald is. En de uren per '
            'dag die u instelt komen uit het activiteitenprofiel van d\u00ede '
            'pati\u00ebnt \u2014 daarom moet de MoveMonitor eerst terug zijn.',
      wie='Pedorthist past aan \u00b7 podoloog meet, plaatst de sensor en begeleidt',
      tip='Plan hier de meeste tijd van de sessie voor. Dit bezoek bepaalt of de '
          'primaire uitkomst bruikbaar wordt.',
      interactie='Demonstreer het plaatsen en activeren van een Orthotimer op een '
                 'losse zool.'),
 dict(t='bezoek', voor='ok', morph='morph',
      kicker='Visites 3 tot 8 \u00b7 maand 3 tot 18',
      kop='Driemaandelijkse opvolging',
      wanneer='In het gewone consult',
      handelingen=['Voet- en schoeiselscreening, zoals bij de baseline.',
                   ('Bevraag de therapietrouw, lees de Orthotimer uit en bespreek de '
                    'uitdraai niet-veroordelend.',
                    'De pen op de sensor, of de uitdraai op het scherm'),
                   ('Beoordeel beide paren zolen. Het paar dat onderhoud nodig heeft '
                    'gaat naar de pedorthist, deklaag inbegrepen.',
                    'Twee paren naast elkaar, versleten en nieuw'),
                   'Vervang zool of sensor als dat nodig is en leg dat vast.',
                   'Neem de vragenlijsten af: levenskwaliteit, medische consumptie en '
                   'productiviteit.',
                   'Op maand 6 een tweede week MoveMonitor.'],
      documenten=[('08', 'Voet en schoeisel'), ('31', 'Therapietrouw'),
                  ('25', 'Uitlezing sensor'), ('32', 'Feedback'),
                  ('33', 'Vervanging'), ('21', 'EQ-5D-5L'),
                  ('34', 'iMCQ'), ('35', 'iPCQ'), ('45b', 'Kostendagboek')],
      letop='Uitlezen kan alleen ter plaatse. Koppel het aan een bezoek dat toch al '
            'gepland is \u2014 een gemiste uitlezing verzwakt de draagtijd van die '
            'pati\u00ebnt over de hele periode.',
      wie='Podoloog leest uit en begeleidt \u00b7 arts beoordeelt laesies',
      tip='Dit zijn zes identieke bezoeken. Zeg dat expliciet: het ritme is elke drie '
          'maanden en de handelingen zijn elke keer dezelfde.',
      interactie='Vraag hoe zij een gemiste afspraak in de praktijk opvangen.'),

 dict(t='bezoek', voor='ok', morph='morph',
      kicker='Visites 4, 6 en 8 \u00b7 maand 6, 12 en 18',
      kop='Wat er drie keer extra bij komt',
      wanneer='Bovenop de driemaandelijkse opvolging',
      handelingen=[('Herhaal de drukmeting in de drie condities en toets opnieuw per '
                    'doelregio.',
                    'De drie condities naast elkaar op het scherm'),
                   'Ligt de piekdruk boven 200 kPa, of is er nog winst haalbaar, pas '
                   'dan opnieuw aan volgens dezelfde procedure.',
                   'Op maand 18 ook de tevredenheidsschaal opnieuw afnemen, zodat de '
                   'verandering tegenover baseline gemeten kan worden.'],
      documenten=[('24', 'Drukherverdeling'), ('24b', 'Opvolgtool'),
                  ('12', 'Tevredenheid \u2014 maand 18')],
      letop='Drie extra meetmomenten, niet twee. Maand 18 telt mee: het recidief '
            'wordt over de volle achttien maanden geteld.',
      wie='Podoloog meet \u00b7 pedorthist past aan',
      tip='Dit is de dia die het vaakst vergeten wordt bij het inplannen. Zet de drie '
          'data nu al in de agenda van de pati\u00ebnt.',
      interactie='Laat elk centrum benoemen wie de drukmeting op maand 18 zal doen.'),
 dict(t='traject', voor='obke', morph='morph',
      kicker='Het traject',
      kop='Terug naar het geheel',
      groot='10',
      punt='contactmomenten, één zorgpad',
      slot='Het verschil met vandaag zit niet in hoe vaak u de patiënt ziet, maar '
           'in wat u bij elk bezoek wéét: wat de zool doet en wat er gedragen is.',
      tip='Sluit blok 3 hiermee af. De zaal herkent de dia van het begin.',
      interactie='Vraag welk moment hun het meest zorgen baart.'),

 dict(t='sectie', voor='obue', morph='morph', nr='04', titel='Toestellen en regels',
      regel='De instellingen, het gesprek, en de vier regels die vastliggen.'),

 dict(t='drieluik', voor='obcuke', morph='morph',
      kicker='De techniek',
      kop='Drie toestellen',
      kaarten=[dict(naam='Novel pedar', sub='Druk', groot='8', onder='voetregio\'s',
                    foto='pedar.png',
                    regels=['Blootsvoets met tape, en in de schoen met en zonder zool',
                            'Trublu-kalibratie minstens elke drie maanden',
                            'De F-Scan GO is een aparte meting van het studieteam'],
                    wie='Uw team meet'),
               dict(naam='Orthotimer', sub='Draagtijd', groot='15', onder='minuten',
                    foto='orthotimer.png',
                    regels=['In de zool, 9 × 13 × 4,5 mm',
                            'Batterij 100 dagen'],
                    wie='Heet: uw sensor'),
               dict(naam='MoveMonitor', sub='Activiteit', groot='7', onder='dagen',
                    foto='movemonitor.png', vlak='glas',
                    regels=['Om het middel, op de onderrug',
                            'Baseline en 6 maanden'],
                    wie='Zet de norm per patiënt')],
      tip='Benoem dat de Orthotimer géén GPS, microfoon of camera heeft. Die '
          'vraag komt gegarandeerd.',
      interactie='Laat de toestellen rondgaan. Fysiek werkt beter dan een dia.'),

 dict(t='aflopend', voor='obue', morph='morph',
      foto='sensor_vol.png',
      kicker='De sensor in het echt',
      kop='Negen bij dertien millimeter.\nMeer merkt de patiënt niet.',
      tip='Laat deze dia even staan zonder te praten. De sensor is fysiek zo '
          'klein dat het beeld het argument al maakt.',
      interactie='Geef er een door de zaal terwijl u praat.'),

 dict(t='sop', voor='o', morph='morph',
      kicker='De zool · protocol 5.4.2 en eCRF 23',
      kop='Hoe de CMFO is opgebouwd',
      instellingen=[('Basis in maatschoen', '5 mm microkurk (55) + 5 mm EVA'),
                    ('Basis in confectie', '6 mm EVA — géén kurk'),
                    ('Deklaag, in beide', '3 mm gesloten + 3 mm open cel'),
                    ('Metatarsaalbalk', '9-10 mm hoog, shore ~55'),
                    ('Positie van de balk', '6-11 mm proximaal'),
                    ('Of lokale pad', 'als maar één regio hoog ligt')],
      stappen=['Controleer de pasvorm in het bínnenschoeisel én het '
               'búitenschoeisel. Beide staan als apart deel op het formulier.',
               'Neem de foto\'s: orthese van boven, onder en opzij, in beide '
               'schoenen, plus de schoenen zelf.',
               'Pas aan zolang de norm niet gehaald is, of zolang podoloog en '
               'pedorthist samen oordelen dat er nog winst te halen is.',
               'Is de norm gehaald, maak dan een tweede, identiek paar.'],
      valkuil='De opbouw hangt af van de schoen. In een volledig op maat gemaakte '
              'schoen is de basis 5 mm microkurk plus 5 mm EVA; in een confectieschoen '
              'is het 6 mm EVA zonder kurk. Wisselt de patiënt van schoentype, dan '
              'klopt de zool niet meer.',
      tip='Dit is de dia voor de pedorthisten. Benadruk dat de zool anders is in een '
          'orthopedische schoen dan in een confectieschoen, en dat de pasvorm in '
          'bínnen- én buitenschoeisel apart beoordeeld wordt.',
      interactie='Vraag of deze opbouw afwijkt van wat ze vandaag maken. Waar het '
                 'afwijkt, noteer dat: het is input voor de procesevaluatie.'),

 dict(t='sop', voor='o', morph='morph',
      kicker='SOP · eCRF-document 25b',
      kop='Orthotimer instellen',
      instellingen=[('Type', 'Insole'),
                    ('Interval', '900 seconden — 15 minuten'),
                    ('Eenheid', 'Celsius'),
                    ('Temperatuurbereik', '25 tot 38,5 °C'),
                    ('Min. aaneengesloten uren', '0'),
                    ('Uren per dag', 'per patiënt · 80% van het actieve profiel')],
      stappen=['Maak de patiënt aan: naam = het deelnemersnummer, geboortedatum '
               '1/1/1999, geslacht vrouwelijk. Noteer in de opmerking dat die '
               'twee geclassificeerd zijn.',
               'Wijs de groep toe: Usual care of Optimal care.',
               'Houd de pen op de O van het Orthotimer-logo tot de balk groen wordt.',
               'Activeer, en laat de sensor één testmeting doen: haal hem iets '
               'langer dan het interval van de lezer af.'],
      valkuil='De uren per dag zijn géén vast getal. Ze komen uit het '
              'activiteitenprofiel van díé patiënt — 80% van zijn gemiddelde '
              'actieve tijd. Zet u er een standaardwaarde in, dan meet u de '
              'verkeerde norm.',
      tip='Dit is de dia waar de meeste vragen op komen. Neem de tijd voor de '
          'uren per dag: dat is de brug tussen de MoveMonitor en de Orthotimer.',
      interactie='Laat iemand de instellingen voordoen op een testsensor.'),

 dict(t='sop', voor='o', morph='morph',
      kicker='SOP · eCRF-document 19b',
      kop='MoveMonitor instellen',
      instellingen=[('Testtype', 'MoviMonitor'),
                    ('Start', 'de dag nadien om 7 uur'),
                    ('Duur', '7 dagen'),
                    ('Deelnemerscode', 'M + deelnemersnummer'),
                    ('Geboortejaar', '1900'),
                    ('Dragen', 'om het middel, op de onderrug')],
      stappen=['Laad volledig op: circa drie uur. Knipperend groen is laden, '
               'groen is vol.',
               'Sluit het toestel aan, kies het in de portaalsite en stel de '
               'meting in.',
               'Geef mee en spreek af wanneer het terugkomt: één visite na zeven dagen.',
               'Sluit bij teruggave aan op de pc; de data uploadt vanzelf via '
               'DynaPort Manager.'],
      valkuil='Niet waterdicht. Zeg dat expliciet tegen de patiënt: uit tijdens '
              'het douchen. Een toestel dat een week in de badkamer lag levert '
              'geen activiteitenprofiel, en dus ook geen norm voor de Orthotimer.',
      tip='Vermeld dat een ongebruikt toestel elke drie maanden opgeladen moet '
          'worden, anders zakt de batterijprestatie.',
      interactie='Vraag wie de toestellen in hun centrum beheert. Dat moet één '
                 'persoon zijn.'),

 dict(t='vijfluik', voor='oce', morph='morph',
      kicker='SEBIA · eCRF-document 17',
      kop='Vijf gespreksmomenten',
      stappen=[('01', 'Baseline', 'Vragenlijsten eerst, dan educatie op maat, '
                                  'met voordoen.'),
               ('02', '3 mnd', 'Teach-back. Nadruk op bínnenshuis dragen.'),
               ('03', '6 · 12 mnd', 'Zelfinschatting, dan samen de data bekijken.'),
               ('04', '9 · 15 mnd', 'Voordoen. Uitdraai vergelijken met vorige keer.'),
               ('05', '18 mnd', 'Afsluiten en resultaten delen.')],
      tip='Het script begint met toestemming vragen voor het gesprek zelf, en '
          'duurt twintig tot dertig minuten. Wie nee zegt, krijgt de brochure '
          'mee en een nieuwe afspraak.',
      interactie='Rollenspel van twee minuten met een vrijwilliger uit de zaal.'),

 dict(t='statement', voor='ock', morph='morph',
      kicker='De enige regel die u écht moet onthouden',
      kop='Meetwaarden gaan\nniet naar de\ncontrolegroep',
      body='Ook zij krijgen een drukmeting en dragen een sensor — anders kunnen we de '
           'groepen niet vergelijken. Maar die getallen blijven dicht. Bespreekt u ze, '
           'dan lévert u de interventie en is die patiënt niet meer bruikbaar als '
           'controle.',
      uitzondering='Klinische bevindingen zijn géén meetwaarden. Elke laesie of '
                   'huiddefect meldt en behandelt u meteen. In beide groepen.',
      tip='Dit is de dia waar u stilvalt. Geen haast. Vraag of het helder is '
          'voordat u doorgaat.',
      interactie='Laat iemand het in eigen woorden herhalen. Zo weet u of het zit.'),

 dict(t='sectie', voor='c', morph='morph', nr='04',
      titel='Eindpunten en analyse',
      regel='Twee eindpunten, \u00e9\u00e9n op \u00e9\u00e9n op het causale model.'),

 dict(t='power', voor='c', morph='morph',
      kicker='Steekproefberekening',
      kop='Twee eindpunten, twee berekeningen',
      kanten=[dict(tag='Co-primair 1', naam='Ulcusrecidief op 18 maanden',
                   rijen=[('Aanname controle', '50% recidief'),
                          ('Aanname interventie', '25%, hazard ratio 0,42'),
                          ('Toets', 'log-rank, tweezijdig, \u03b1 = 0,05'),
                          ('Power', '80% \u2192 41 events nodig'),
                          ('Uitval', '15%')],
                   nodig='108 \u2192 127 met uitval \u2192 130 gestratificeerd'),
              dict(tag='Co-primair 2', naam='Therapietrouw op 12 maanden',
                   rijen=[('Aanname controle', '71%, SD 25%'),
                          ('Aanname interventie', '85%, effectgrootte 0,56'),
                          ('Toets', 't-toets, tweezijdig, \u03b1 = 0,05'),
                          ('Power', '80% \u2192 50 per groep'),
                          ('Uitval', '15%')],
                   nodig='100 \u2192 118 met uitval')],
      slot='Zes centra maal 24 is 144. Dat cijfer komt niet uit de berekening '
           'maar uit de rekruteringscapaciteit per centrum, en het overtreft '
           'beide minima.',
      slotlabel='Waarom dan 144',
      voet='Manuscript, steekproefberekening \u00b7 exponentieel verdeelde tijden tot recidief aangenomen',
      tip='Dit is de dia waar de vraag komt. Benoem de gezamenlijke power zelf, '
          'v\u00f3\u00f3r iemand in de zaal het doet \u2014 de volgende dia doet dat.',
      interactie='Geen. Laat de vraag komen.'),

 dict(t='eerlijk', voor='c', morph='morph',
      kicker='Wat het co-primaire criterium kost',
      kop='De power die telt, is de gezamenlijke',
      intro='De studie is pas positief als b\u00e9\u00edde eindpunten significant zijn.',
      rijen=[('Recidief apart', '84% \u2014 en 90% bij volledige opvolging'),
             ('Therapietrouw apart', '87% \u2014 en 92% bij volledige opvolging'),
             ('Beide samen', '74% tot 84%, naargelang de correlatie'),
             ('Bij een half zo groot effect', '64% bij 30% \u00b7 40% bij 35%')],
      slot='Protocollen met co-primaire eindpunten rapporteren doorgaans alleen '
           'het cijfer per eindpunt. Dat overschat de kans op het criterium '
           'waarop de studie werkelijk beoordeeld wordt.',
      tip='Dit is de dia die u onderscheidt van de rest van het programma. '
          'Niemand rapporteert dit uit zichzelf.',
      interactie='Geen.'),

 dict(t='melden', voor='c', morph='morph',
      kicker='Analyseplan',
      kop='Hoe we het toetsen',
      rijen=[('Recidief', 'Cox-regressie gestratificeerd naar centrum, met de '
                          'toewijzing als enige covariaat. Sterfte is een '
                          'competing risk, geen censuur: Fine-Gray en cumulatieve '
                          'incidentie ernaast.', 'co-primair'),
             ('Therapietrouw', 'Beta-regressie met logit-link, want het is een '
                               'proportie met een plafond. Lineaire regressie als '
                               'gevoeligheidsanalyse.', 'co-primair'),
             ('Intercurrente events', 'De twee eindpunten zijn elkaars '
                                      'intercurrente event: wie ulcereert draagt '
                                      'terecht geen zool meer. Hypothetische '
                                      'strategie voor therapietrouw.', 'estimand'),
             ('Ontbrekende data', 'Multipele imputatie, 50 datasets. Een '
                                  'tipping-pointanalyse toont hoe extreem het '
                                  'moet worden om de conclusie te kantelen.',
                                  'MAR')],
      slot='Positief alleen als beide eindpunten significant zijn. Daarom blijft '
           'de familiegewijze fout onder 0,05 en is geen correctie nodig.',
      tip='Kort houden. Wie meer wil weten vraagt het, en dan hebt u het SAP.',
      interactie='Geen.'),

 dict(t='duo', voor='c', morph='morph',
      kicker='Wat er naast de trial loopt',
      kop='Twee evaluaties, parallel',
      een=dict(nr='01', naam='Gezondheidseconomische evaluatie',
               kern='Kosten-utiliteit, betalersperspectief',
               regels=['EQ-5D-5L elke drie maanden, gewaardeerd met de Belgische '
                       'waardeset.',
                       'Zorggebruik prospectief met iMCQ en iPCQ, plus dagboek en '
                       'dossier.',
                       'Markov tot vijf jaar. Kosten per vermeden ulcus \u00e9n per '
                       'QALY, naast elkaar.']),
      twee=dict(nr='02', naam='Procesevaluatie',
                kern='MRC-kader, drie domeinen',
                regels=['Implementatie: fideliteit, dosis, bereik, aanpassingen.',
                        'Mechanismen en context: wat de uitvoering per centrum '
                        'bepaalt.',
                        'Interviews, gestructureerde observatie en '
                        'therapeutendagboeken.']),
      tip='De procesevaluatie is geen bijlage. Bij een nulresultaat is zij het '
          'enige wat mechanisme van uitvoering onderscheidt.',
      interactie='Geen.'),

 dict(t='vraagraster', voor='c', morph='morph',
      kicker='Wat we hoe dan ook leren',
      kop='Een nulresultaat is ook een resultaat',
      paren=[('Therapietrouw stijgt, recidief niet',
              'Dan faalt de biomechanische premisse: geoptimaliseerd schoeisel '
              'dr\u00e1gen volstaat niet. Het veld moet stoppen preventiefalen aan '
              'de pati\u00ebnt toe te schrijven.'),
             ('Therapietrouw stijgt niet',
              'Dan faalde de gedragscomponent. De fideliteitsdata zeggen of het '
              'ontwerp tekortschoot of de uitvoering.'),
             ('Beide stijgen',
              'Dan werkt een ge\u00efntegreerde dienst onder routineomstandigheden '
              '\u2014 zonder dat we weten welk onderdeel het deed. Ontleden vraagt '
              'een factori\u00eble opzet die het Belgische netwerk niet kan leveren.'),
             ('Hoe dan ook',
              'Druk, activiteit en draagtijd worden bij 144 deelnemers over '
              'achttien maanden gelijktijdig gemeten. Dat is de eerste dataset '
              'van die omvang, ongeacht de uitkomst.')],
      tip='Sluit hiermee af. Dit is het antwoord op de vraag of de studie de '
          'moeite waard is als ze negatief uitvalt.',
      interactie='Geen.'),

 dict(t='melden', voor='ok', morph='morph',
      kicker='Wat u meldt, en hoe snel',
      kop='Voorvallen en afwijkingen',
      rijen=[('Nieuw ulcus', 'Ulcus-vervolgformulier plus PEDIS- en WIfI-classificatie. '
                             'Dit is de primaire uitkomst — meld het altijd.', '47 · 36 · 38'),
             ('Ongewenst voorval', 'AE-SAE-formulier. Ernstige voorvallen binnen '
                                   '24 uur na kennisname.', '46'),
             ('Protocolafwijking', 'Melden zoals ze gebeurd is. Wordt geregistreerd, '
                                   'niet afgestraft.', '—'),
             ('Toestel defect', 'Vervangingsformulier, met het oude en het nieuwe '
                                'toestelnummer.', '33')],
      slot='Een afwijking die u meldt is een gegeven. Een afwijking die u niet '
           'meldt is een fout in de data van de hele studie.',
      tip='Dit is de dia die de zaal ontspant én scherpt. Zeg het zinnetje '
           'onderaan letterlijk.',
      interactie='Vraag of iemand een situatie kan bedenken waarvan hij niet '
                 'weet of het gemeld moet worden. Bespreek er twee.'),

 dict(t='vierluik', voor='obk', morph='morph',
      kicker='Verdeling',
      kop='Wie doet wat',
      kolommen=[('Podoloog', ['Voert de drukmetingen uit', 'Levert SEBIA',
                              'Leest de sensoren uit']),
                ('Pedorthist', ['Maakt de zool', 'Past aan tot de norm',
                                'Plaatst de sensor']),
                ('Arts', ['Bevestigt geschiktheid', 'Beoordeelt laesies',
                          'Meldt voorvallen']),
                ('Management', ['Maakt tijd vrij', 'Bewaakt 24 inclusies',
                                'Houdt het opleidingsregister bij'])],
      tip='Kijk elke groep aan bij hun rij. Namen noemen als u ze kent.',
      interactie='Vraag per rij: "herkenbaar, of mis ik iets?" Pas de '
                 'taakverdeling ter plekke aan als dat nodig is.'),

 dict(t='steun', voor='obk', morph='morph',
      kicker='Ondersteuning',
      kop='Wat u van ons krijgt',
      rijen=[('Motiverende gespreksvoering',
              'Training door een psycholoog — alle centra dezelfde'),
             ('SOP\'s en draaiboeken',
              'Per handeling, met de eCRF-nummers erbij'),
             ('Gegevensinvoer',
              'Doet het onderzoeksteam. U vult de formulieren in, verder niets'),
             ('Eén contactpunt',
              'Eén nummer, één mailadres, voor alles')],
      cijfer='0', cijfer_label='sancties',
      cijfer_regel='Wijkt u af van het protocol, dan meldt u dat. '
                   'Het wordt geregistreerd, niet afgestraft.',
      tip='Het cijfer rechts ontspant de zaal. Zeg het expliciet en wacht even. '
          'Vraagt iemand hoe de ingevulde formulieren bij ons raken: zeg dat daar '
          'bericht over volgt. Beloof geen werkwijze, want die ligt nog niet vast.',
      interactie='Geen.'),

 dict(t='vraagraster', voor='ok', morph='morph',
      kicker='Wat u gaat vragen',
      kop='Vooruitlopend',
      paren=[('Patiënt wil de sensor niet', 'Dan niet geschikt. Draagtijd ís een hoofduitkomst.'),
             ('Zool haalt de norm niet', 'Twee extra tests, dan noteert u wat wél bereikt is.'),
             ('Mag ik nog adviseren?', 'Alles wat u vandaag doet, blijft u doen.'),
             ('En de ingevulde formulieren?', 'Daar volgt bericht over. Invoeren '
                                              'doet het onderzoeksteam.'),
             ('Onze data?', 'Gepseudonimiseerd, tien jaar, binnen de toestemming.'),
             ('Zien wij resultaten?', 'Eén publicatie, ongeacht de uitkomst.')],
      tip='Sla over wat al gevraagd is. Deze dia is een vangnet, geen programma.',
      interactie='Toon hem alleen als de vragen opdrogen.'),

 dict(t='knal', voor='ok', morph='morph', kleur='licht', kleur2='mid',
      kop='Vanaf de eerste pati\u00ebnt\ndoet u dit zelf.',
      onder='Wij leiden op, wij voeren in. De handelingen zijn van u.',
      tip='Dit is de overgang naar de bekwaamheidscheck. Zeg het rustig; het '
          'is geen dreigement maar een vaststelling.',
      interactie='Geen.'),

 dict(t='check', voor='o', morph='morph',
      kicker='Bekwaamheidscheck',
      kop='Kunt u dit nu zelf?',
      items=['Beoordelen of een patiënt geschikt is, en dat vastleggen vóór de toestemming',
             'Een drukmeting uitvoeren in de drie condities, drie metingen per voet',
             'De drie doelregio\'s bepalen en op het voorschrift zetten',
             'De norm toetsen per regio en aanpassen tot ze gehaald is',
             'De Orthotimer instellen met de juiste uren per dag voor díé patiënt',
             'De MoveMonitor instellen, meegeven en uitlezen',
             'Een SEBIA-gesprek voeren met teach-back',
             'De formulieren volledig invullen en weten wat u meldt, aan wie en '
             'binnen welke termijn'],
      slot='Acht handelingen. Wie er één niet aandurft, meldt dat nu — dan plannen '
           'we een tweede sessie. Dat is geen zwakte, dat is hoe u fouten in de '
           'data voorkomt.',
      tip='Laat dit stil invullen. Iemand die twijfelt zegt dat niet hardop in '
          'een volle zaal, wel op papier.',
      interactie='Verzamel de blaadjes. Waar drie of meer mensen dezelfde '
                 'handeling aanvinken, plant u een extra sessie.'),

 dict(t='register', voor='ob', morph='morph',
      kicker='Voor het dossier',
      kop='Het opleidingsregister',
      body='ISO 14155 vraagt dat per medewerker aantoonbaar is welke training hij '
           'gekregen heeft, wanneer, en voor welke handelingen hij gedelegeerd is. '
           'Zonder dat register is uw centrum niet inspectieklaar, hoe goed u het '
           'ook doet.',
      regels=[('Vandaag tekenen', 'Naam, functie, datum, en de handelingen '
                                  'waarvoor u gedelegeerd bent.'),
              ('Bij elke nieuwe medewerker', 'Dezelfde opleiding, dezelfde '
                                             'handtekening, vóór de eerste patiënt.'),
              ('Bij elke protocolwijziging', 'Kort bijscholingsmoment, opnieuw '
                                             'tekenen.')],
      slot='Het register blijft in uw centrum. Wij krijgen een kopie voor het '
           'studiedossier.',
      tip='Laat het register rondgaan tijdens deze dia, niet erna. Anders vertrekt '
          'de helft zonder te tekenen.',
      interactie='Tel hardop hoeveel handtekeningen u nodig hebt en hoeveel er al '
                 'staan.'),

 dict(t='contact', voor='obcuke', morph='morph',
      kicker='Wie u aanspreekt',
      kop='Voor als er iets misloopt',
      personen=[
          dict(naam='Janou De Buyser',
               rol='Doctoraatsonderzoeker · dagelijkse opvolging',
               waarvoor='Uw eerste aanspreekpunt: inclusies, metingen, formulieren, '
                        'sensoren en alles wat in de praktijk vastloopt.',
               bereik=['janou.debuyser@kuleuven.be',
                       'Spoorwegstraat 12 · Brugge']),
          dict(naam='prof. dr. Kevin Deschamps',
               rol='Promotor',
               waarvoor='Wetenschappelijke vragen, de opzet van de studie en '
                        'afspraken op het niveau van uw centrum.',
               bereik=['Revalidatiewetenschappen',
                       'KU Leuven · Campus Brugge']),
      ],
      consortium='Consortium: KU Leuven — Revalidatiewetenschappen (Musculoskeletal '
                 'Research Group) en Volksgezondheid en Eerstelijnszorg · Vrije '
                 'Universiteit Brussel — Geneeskunde en Farmacie. Co-promotoren: '
                 'Fabienne Dobbels, Maaike Fobelets en Koen Putman.',
      voet='PARADISE · FWO TBM T000226N · S71769',
      tip='Laat deze dia staan tijdens het napraten. Zeg erbij dat kleine dingen '
          'ook mogen — een sensor die niet uitleest is geen domme vraag.',
      interactie='Loop rond terwijl de dia staat. Wie een vraag heeft, komt naar '
                 'het gezicht dat op het scherm staat.'),
]
