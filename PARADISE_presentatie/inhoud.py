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
PUNTEN = [('Screening', 'geschiktheid', 'start'),
          ('Baseline', 'meting', 'meting'),
          ('1', 'voorschrift', 'zorg'),
          ('3', 'zool + sensor', 'meting'),
          ('6', 'meting', 'meting'),
          ('9', 'begeleiding', 'zorg'),
          ('12', 'meting', 'meting'),
          ('15', 'begeleiding', 'zorg'),
          ('18', 'meting + einde', 'eind')]

SOORT = [('meting', 'meetmoment'), ('zorg', 'begeleiding'),
         ('start', 'start en afronding')]

CENTRA = ['AZORG', 'AZ Sint-Jan Brugge', 'AZ Groeninge',
          'UZ Gent', 'UZ Leuven', 'UZ Antwerpen']


SLIDES = [

 dict(t='hero_titel', morph='fade',
      boven='PARADISE',
      onder='Opleidingssessie',
      staart='Zo voert u het protocol uit — bezoek per bezoek, formulier per formulier',
      tegels=[('6', 'centra'), ('24', 'inclusies per centrum'), ('18', 'maanden')],
      voet='Opleiding studiepersoneel · protocolversie 1.0 · 17 mei 2026 · S71769',
      tip='U hoeft niemand meer te overtuigen: de centra zitten al in het '
          'consortium. Zeg dat expliciet in de eerste zin, dan weet de zaal dat '
          'dit een werksessie is en geen pitch.',
      interactie='Vraag wie vandaag voor het eerst van de studie hoort. Dat '
                 'bepaalt hoeveel tijd u aan blok 1 besteedt.'),

 dict(t='doel', morph='morph',
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
              ('Registreren', 'invoeren in REDCap, en weten wat u meldt als er '
                              'iets afwijkt')],
      slot='Wie een van deze zes niet aandurft na vandaag, moet dat zeggen. '
           'Daar is deze sessie voor.',
      tip='Loop de zes titels traag door. Dit is de belofte van de dag en het '
          'is ook precies de bekwaamheidscheck op het eind.',
      interactie='Laat iedereen op een blad de zes overschrijven en aanduiden '
                 'welke ze al beheersen. Op het eind vullen ze dat opnieuw in.'),

 dict(t='keuze', morph='morph',
      kicker='Programma van vandaag',
      kop='Vier blokken',
      tegels=[('01', 'Waarom zo', 'De vier cijfers achter de twee normen'),
              ('02', 'De meting', 'Drukmeting, doelregio\'s en de norm'),
              ('03', 'Het traject', 'Bezoek per bezoek, met de formulieren'),
              ('04', 'Toestellen en regels', 'SOP\'s, SEBIA, blindering, REDCap')],
      tip='Blok 3 is het langste en het belangrijkste. Plan uw tijd zo dat u '
          'daar niet doorheen moet jagen.',
      interactie='Vraag of iemand een blok wil ruilen van plaats. Wie kiest, '
                 'luistert beter.'),

 dict(t='statraster', morph='morph',
      kicker='Waar we staan',
      kop='144 patiënten, 24 per centrum',
      klein=[('Per centrum', '24 deelnemers — 12 PARADISE en 12 gebruikelijke zorg'),
             ('Controlegroep', 'Gebruikelijke zorg, onveranderd'),
             ('Co-primair', 'Recidief én draagtijd, beide op 18 maanden'),
             ('Positief', 'Alleen als béíde eindpunten halen')],
      centra=CENTRA,
      centra_label='De zes deelnemende voetklinieken',
      tip='Wijs hun eigen centrum aan: 24 van die 144 stippen zijn van hen. Zes '
          'keer 24 is 144 — als één centrum achterblijft, haalt de studie het niet.',
      interactie='Vraag of ze de andere vijf centra kennen. Het maakt van zes '
                 'losse klinieken één netwerk.'),

 dict(t='sectie', morph='morph', nr='01', titel='Waarom zo',
      regel='Vier cijfers verklaren waarom er twee normen zijn.'),

 dict(t='hero_cijfer', morph='morph',
      cijfer='40', suffix='%',
      kop='krijgt binnen een jaar\neen nieuw ulcus',
      tegels=[('60%', 'na drie jaar'), ('65%', 'na vijf jaar'), ('2,5×', 'hogere sterfte')],
      voet='Armstrong, Boulton & Bus · N Engl J Med 2017',
      accent='oranje',
      tip='Dit is het probleem waar de hele studie op staat. Eén dia, dan door.',
      interactie='Geen. Dit is context, geen discussie.'),

 dict(t='splitsing', morph='morph',
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

 dict(t='hero_cijfer', morph='morph',
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

 dict(t='formule', morph='morph',
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

 dict(t='sectie', morph='morph', nr='02', titel='De meting',
      regel='Wat u meet, hoe u het meet, en wanneer het goed genoeg is.'),

 dict(t='drukmeting', morph='morph', fase='voor',
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

 dict(t='drukzoom', morph='morph', fase='voor',
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

 dict(t='drukmeting', morph='morph', fase='na',
      kicker='Na optimalisatie',
      kop='Wanneer is het goed genoeg',
      waarde='186', plek='piekdruk in de doelregio na aanpassing',
      norm='40% lager  ·  onder 200 kPa  ·  beide criteria',
      regels=['De norm geldt per doelregio: piekdruk onder 200 kPa óf minstens '
              '25% lager dan de baselinemeting van diezelfde regio.',
              'Haalt u de norm niet, dan past u aan en meet u opnieuw. Het '
              'formulier voorziet twee extra ontlastingstests.'],
      voet='eCRF-document 24 · Meting drukherverdeling voetorthese',
      tip='Zeg expliciet: "óf". Twee wegen naar dezelfde norm, geen dubbele eis. '
          'En de vergelijking gebeurt per regio, niet over de hele voet.',
      interactie='Vraag de pedorthisten hoeveel aanpassingsrondes realistisch zijn.'),

 dict(t='meetreeks', morph='morph',
      kicker='Het meetprotocol',
      kop='Drie condities op maand 3',
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
          'vergeten wordt.',
      interactie='Vraag: "wie meet er vandaag al in de schoen zonder zool?"'),

 dict(t='sectie', morph='morph', nr='03', titel='Het traject',
      regel='Negen contactmomenten. Per moment: wat u doet en wat u invult.'),

 dict(t='traject', morph='morph',
      kicker='Het traject',
      kop='Negen contactmomenten',
      groot='18',
      punt='maanden, van screening tot afronding',
      slot='Het ritme is elke drie maanden: hetzelfde ritme als de controle die '
           'deze patiënten volgens de richtlijn al krijgen.',
      tip='Geef eerst het overzicht. De volgende dia\'s lopen elk moment af.',
      interactie='Geen. De detaildia\'s komen hierna.'),

 dict(t='bezoek', morph='morph',
      kicker='Moment 1',
      kop='Screening, vóór de toestemming',
      wanneer='Kort · in het gewone consult',
      handelingen=['Beoordeel de in- en exclusiecriteria op het screeningsformulier.',
                   'Noteer de patiënt op de identificatielijst en ken een '
                   'deelnemerscode toe.',
                   'Is de patiënt geschikt, geef dan de informatie- en '
                   'toestemmingsformulieren mee.',
                   'Niet geschikt? Noteer de reden. Ook dat is studiedata.'],
      documenten=[('00', 'Identificatielijst'),
                  ('01', 'Screening'),
                  ('02', 'Toestemming')],
      letop='Screening gebeurt vóór de toestemming en blijft daarom beperkt tot '
            'wat nodig is om geschiktheid te beoordelen. Vul geen andere '
            'formulieren in voordat de patiënt getekend heeft.',
      wie='Arts bevestigt geschiktheid · podoloog of studiemedewerker vult in',
      tip='Benadruk de volgorde: screenen, dan pas toestemming, dan pas de rest. '
          'Andersom is een protocolafwijking.',
      interactie='Deel het screeningsformulier uit en laat ze het invullen voor '
                 'een patiënt die ze vorige week zagen.'),

 dict(t='dubbelkolom', morph='morph',
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

 dict(t='bezoek', morph='morph',
      kicker='Moment 2',
      kop='Baseline',
      wanneer='Het langste bezoek van de studie',
      handelingen=['Bevestig de geschiktheid en leg demografie en '
                   'voorgeschiedenis vast.',
                   'Screen voet en schoeisel, en klasseer een eventueel ulcus.',
                   'Voer de drukmeting blootsvoets uit: drie metingen per voet.',
                   'Bepaal en noteer de drie doelregio\'s.',
                   'Neem de vragenlijsten af vóór het educatiegesprek: NAFF en '
                   'HLS-EU-6, daarna EQ-5D-5L.',
                   'Geef de MoveMonitor mee voor zeven dagen en registreer het '
                   'toestelnummer.',
                   'Voer het eerste SEBIA-gesprek en geef het educatieboekje mee.'],
      documenten=[('06', 'Geschiktheid'), ('07', 'Demografie'),
                  ('08', 'Voet en schoeisel'), ('09', 'Drukmeting'),
                  ('14', 'NAFF'), ('15', 'HLS-EU-6'), ('16', 'Educatieboekje'),
                  ('19', 'MoveMonitor'), ('20', 'UDI MoveMonitor'),
                  ('21', 'EQ-5D-5L'), ('26', 'Overtuigingen')],
      letop='NAFF en HLS-EU-6 gaan vóór de educatie. Neemt u ze erna af, dan meet '
            'u uw eigen uitleg in plaats van de voorkennis van de patiënt.',
      wie='Podoloog meet en begeleidt · arts bevestigt · studiemedewerker registreert',
      tip='Dit is het bezoek dat uitloopt. Zeg hoeveel tijd u ervoor moet '
          'inplannen en waarom de volgorde vastligt.',
      interactie='Laat ze in duo\'s de volgorde van de zeven handelingen leggen '
                 'met de formulieren op tafel.'),

 dict(t='bezoek', morph='morph',
      kicker='Moment 3 · maand 1',
      kop='Het voorschrift',
      wanneer='Kort bezoek, geen meting',
      handelingen=['Schrijf de aangepaste voetorthese voor op basis van het '
                   'baselinebeeld en de drie doelregio\'s.',
                   'Noteer de doelregio\'s expliciet op het voorschrift, zodat de '
                   'pedorthist weet waar de ontlasting moet komen.',
                   'Spreek de afleverafspraak op maand 3 af.'],
      documenten=[('10', 'Voorschrift CMFO')],
      letop='Zonder de drie doelregio\'s op het voorschrift maakt de pedorthist '
            'een zool op gevoel. Dan is de meting op maand 3 niet toetsbaar.',
      wie='Arts of podoloog schrijft voor · pedorthist ontvangt',
      tip='Dit is het kortste bezoek en tegelijk het scharnier tussen meting en '
          'zool. Benadruk de overdracht.',
      interactie='Vraag de pedorthisten wat zij nu op een voorschrift missen.'),

 dict(t='bezoek', morph='morph',
      kicker='Moment 4 · maand 3',
      kop='Aflevering, optimalisatie en sensor',
      wanneer='Het technisch zwaarste bezoek',
      handelingen=['Lever de zool af en controleer pasvorm en aandrukpunten.',
                   'Meet de drie condities: blootsvoets, in de schoen zonder '
                   'zool, in de schoen met zool.',
                   'Toets de norm per doelregio. Niet gehaald? Pas aan en meet '
                   'opnieuw — twee extra tests zijn voorzien.',
                   'Noteer welke aanpassingen u hebt uitgevoerd.',
                   'Is de norm gehaald, laat dan een tweede, identiek paar zolen '
                   'maken. Beide paren blijven in gebruik.',
                   'Plaats en activeer de Orthotimer in de zool en registreer het '
                   'toestelnummer.',
                   'Voer het SEBIA-gesprek met teach-back en geef de sensorfolder mee.'],
      documenten=[('23', 'Aanpassing'), ('24', 'Drukherverdeling'),
                  ('24b', 'Opvolgtool'), ('25', 'UDI Orthotimer'),
                  ('25b', 'SOP Orthotimer'), ('29', 'Teach-back'),
                  ('30', 'Sensorfolder')],
      letop='De Orthotimer gaat pas in de zool nadat de norm gehaald is. Anders '
            'meet u draagtijd van een zool die nog aangepast wordt.',
      wie='Pedorthist past aan · podoloog meet en plaatst de sensor',
      tip='Plan hier het meeste tijd in de sessie. Dit bezoek bepaalt of de '
          'primaire uitkomst bruikbaar wordt.',
      interactie='Demonstreer het plaatsen en activeren van een Orthotimer op '
                 'een losse zool.'),

 dict(t='bezoek', morph='morph',
      kicker='Momenten 5 tot 9 · maand 6 tot 18',
      kop='Opvolging, elke drie maanden',
      wanneer='In het gewone consult',
      handelingen=['Elk bezoek: lees de Orthotimer uit, vervang de batterij en '
                   'registreer de uitlezing.',
                   'Bevraag de therapietrouw en bespreek de uitdraai '
                   'niet-veroordelend.',
                   'Op maand 6, 12 én 18: herhaal de drukmeting in de drie '
                   'condities en pas opnieuw aan als de norm niet gehaald is.',
                   'Op maand 6: tweede week MoveMonitor.',
                   'Beoordeel beide paren zolen. Het paar dat onderhoud nodig '
                   'heeft gaat naar de pedorthist, inclusief toplaag.',
                   'Vervang zool of sensor als dat nodig is, en leg dat vast.',
                   'Vul de kwaliteit-van-leven- en kostenvragenlijsten aan.'],
      documenten=[('24', 'Drukherverdeling'), ('28', 'Activiteit'),
                  ('31', 'Therapietrouw'), ('32', 'Feedback'),
                  ('33', 'Vervanging'), ('21', 'EQ-5D-5L'),
                  ('45b', 'Kostendagboek')],
      letop='Beide co-primaire uitkomsten worden op 18 maanden geëvalueerd, maar '
            'de draagtijd is een gemiddelde over de hele periode. Elke gemiste '
            'uitlezing verzwakt dus het eindresultaat van die patiënt.',
      wie='Podoloog leest uit en begeleidt · arts beoordeelt laesies',
      tip='Benadruk dat uitlezen enkel ter plaatse kan. Koppel het aan een '
          'bezoek dat toch al gepland is.',
      interactie='Vraag hoe zij een gemiste afspraak in de praktijk opvangen.'),

 dict(t='traject', morph='morph',
      kicker='Het traject',
      kop='Terug naar het geheel',
      groot='9',
      punt='momenten, één zorgpad',
      slot='Het verschil met vandaag zit niet in hoe vaak u de patiënt ziet, maar '
           'in wat u bij elk bezoek wéét: wat de zool doet en wat er gedragen is.',
      tip='Sluit blok 3 hiermee af. De zaal herkent de dia van het begin.',
      interactie='Vraag welk moment hun het meest zorgen baart.'),

 dict(t='sectie', morph='morph', nr='04', titel='Toestellen en regels',
      regel='De instellingen, het gesprek, en de vier regels die vastliggen.'),

 dict(t='drieluik', morph='morph',
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

 dict(t='aflopend', morph='morph',
      foto='sensor_vol.png',
      kicker='De sensor in het echt',
      kop='Negen bij dertien millimeter.\nMeer merkt de patiënt niet.',
      tip='Laat deze dia even staan zonder te praten. De sensor is fysiek zo '
          'klein dat het beeld het argument al maakt.',
      interactie='Geef er een door de zaal terwijl u praat.'),

 dict(t='sop', morph='morph',
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

 dict(t='sop', morph='morph',
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

 dict(t='sop', morph='morph',
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

 dict(t='vijfluik', morph='morph',
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

 dict(t='statement', morph='morph',
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

 dict(t='melden', morph='morph',
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

 dict(t='vierluik', morph='morph',
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

 dict(t='steun', morph='morph',
      kicker='Ondersteuning',
      kop='Wat u van ons krijgt',
      rijen=[('Motiverende gespreksvoering',
              'Training door een psycholoog — alle centra dezelfde'),
             ('SOP\'s en draaiboeken',
              'Per handeling, met de eCRF-nummers erbij'),
             ('REDCap',
              'Instructie plus een testomgeving om in te oefenen'),
             ('Eén contactpunt',
              'Eén nummer, één mailadres, voor alles')],
      cijfer='0', cijfer_label='sancties',
      cijfer_regel='Wijkt u af van het protocol, dan meldt u dat. '
                   'Het wordt geregistreerd, niet afgestraft.',
      tip='Het cijfer rechts ontspant de zaal. Zeg het expliciet en wacht even.',
      interactie='Geen.'),

 dict(t='vraagraster', morph='morph',
      kicker='Wat u gaat vragen',
      kop='Vooruitlopend',
      paren=[('Patiënt wil de sensor niet', 'Dan niet geschikt. Draagtijd ís een hoofduitkomst.'),
             ('Zool haalt de norm niet', 'Twee extra tests, dan noteert u wat wél bereikt is.'),
             ('Mag ik nog adviseren?', 'Alles wat u vandaag doet, blijft u doen.'),
             ('Wie leest de sensor uit?', 'Uw team, ter plaatse, bij elk bezoek.'),
             ('Onze data?', 'Gepseudonimiseerd, tien jaar, binnen de toestemming.'),
             ('Zien wij resultaten?', 'Eén publicatie, ongeacht de uitkomst.')],
      tip='Sla over wat al gevraagd is. Deze dia is een vangnet, geen programma.',
      interactie='Toon hem alleen als de vragen opdrogen.'),

 dict(t='check', morph='morph',
      kicker='Bekwaamheidscheck',
      kop='Kunt u dit nu zelf?',
      items=['Beoordelen of een patiënt geschikt is, en dat vastleggen vóór de toestemming',
             'Een drukmeting uitvoeren in de drie condities, drie metingen per voet',
             'De drie doelregio\'s bepalen en op het voorschrift zetten',
             'De norm toetsen per regio en aanpassen tot ze gehaald is',
             'De Orthotimer instellen met de juiste uren per dag voor díé patiënt',
             'De MoveMonitor instellen, meegeven en uitlezen',
             'Een SEBIA-gesprek voeren met teach-back',
             'Weten wat u meldt, aan wie, en binnen welke termijn'],
      slot='Acht handelingen. Wie er één niet aandurft, meldt dat nu — dan plannen '
           'we een tweede sessie. Dat is geen zwakte, dat is hoe u fouten in de '
           'data voorkomt.',
      tip='Laat dit stil invullen. Iemand die twijfelt zegt dat niet hardop in '
          'een volle zaal, wel op papier.',
      interactie='Verzamel de blaadjes. Waar drie of meer mensen dezelfde '
                 'handeling aanvinken, plant u een extra sessie.'),

 dict(t='register', morph='morph',
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

 dict(t='contact', morph='morph',
      kicker='Wie u aanspreekt',
      kop='Voor als er iets misloopt',
      personen=[
          dict(naam='Janou De Buyser',
               rol='Doctoraatsonderzoeker · dagelijkse opvolging',
               waarvoor='Uw eerste aanspreekpunt: inclusies, metingen, REDCap, '
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
