# -*- coding: utf-8 -*-
"""PARADISE — informatiesessie voor de diabetische voetklinieken.

Ontwerpprincipes: dark mode, bento-grid, één kernboodschap per dia, typografie
als visueel element, geen opsommingstekens. Elke dia draagt een morph-overgang.

Alle cijfers komen uit het protocol (versie 1.0, 17/05/2026) en het
geverifieerde manuscript.
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
          ('18', 'afronding', 'eind')]

SOORT = [('meting', 'meetmoment'), ('zorg', 'begeleiding'),
         ('start', 'start en afronding')]


SLIDES = [

 dict(t='hero_titel', morph='fade',
      boven='PARADISE',
      onder='Druk. Trouw. Educatie.',
      staart='Eén zorgpad tegen het recidief van de diabetische voet',
      tegels=[('144', 'deelnemers'), ('6', 'voetklinieken'), ('18', 'maanden')],
      voet='Informatiesessie · KU Leuven · prof. dr. Kevin Deschamps · FWO T000226N',
      tip='Begin staand, zonder klikken. Laat de dia drie tellen staan voor u praat. '
          'De drie tegels zijn het enige wat ze hoeven onthouden.',
      interactie='Vraag bij binnenkomst: "wie heeft deze week een recidief gezien?" '
                 'Handen in de lucht. Dat is uw opening.'),

 dict(t='keuze', morph='morph',
      kicker='Deze sessie is modulair',
      kop='Waar wilt u beginnen?',
      tegels=[('01', 'Het probleem', 'Waarom betere zolen niet volstaan'),
              ('02', 'De interventie', 'Wat we precies gaan doen'),
              ('03', 'Uw rol', 'Wat er dinsdagmiddag verandert'),
              ('04', 'De afspraak', 'Wat we van uw kliniek vragen')],
      tip='Laat de zaal kiezen. Dit is geen lineaire deck. Wie kiest, luistert beter.',
      interactie='Handopsteking of Mentimeter. Begin met het blok dat wint.'),

 dict(t='sectie', morph='morph', nr='01', titel='Het probleem',
      regel='Genezing is geen eindpunt. Het is een pauze.'),

 dict(t='hero_cijfer', morph='morph',
      cijfer='40', suffix='%',
      kop='krijgt binnen een jaar\neen nieuw ulcus',
      tegels=[('60%', 'na drie jaar'), ('65%', 'na vijf jaar'), ('2,5×', 'hogere sterfte')],
      voet='Armstrong, Boulton & Bus · N Engl J Med 2017',
      accent='oranje',
      tip='Laat het getal even alleen staan. Zeg dan pas: "dit is uw eigen praktijk."',
      interactie='Morph vanaf de sectiedia: het cijfer groeit uit de titel.'),

 dict(t='splitsing', morph='morph',
      kicker='Dezelfde schoen, twee uitkomsten',
      kop='Het lag niet aan de zool',
      links=dict(titel='Iedereen', sub='intention-to-treat', groot='38,8',
                 ref=44.2, ref_lbl='Gewone maatzool', int_lbl='Drukgeoptimaliseerd',
                 slot='Geen verschil — p = 0,48', kleur='oranje'),
      rechts=dict(titel='Wie hem droeg', sub='≥ 80% van de stappen', groot='25,7',
                  ref=47.8, ref_lbl='Gewone maatzool', int_lbl='Drukgeoptimaliseerd',
                  slot='Bijna gehalveerd — p = 0,045', kleur='licht'),
      punchline='De interventie werkte. Bij de 46% die hem aandeed.',
      voet='Bus et al. · Diabetes Care 2013 · DIAFOS, 171 deelnemers',
      tip='Wijs eerst links aan, laat het bezinken, wijs dan rechts. '
          'De punchline zegt u, niet de dia.',
      interactie='Morph: beide blokken schuiven uit het midden uit elkaar.'),

 dict(t='hero_cijfer', morph='morph',
      cijfer='71', suffix='%',
      kop='draagtijd — gemeten,\nniet gevraagd',
      tegels=[('61%', 'thuis'), ('4000', 'stappen binnen'), ('2600', 'stappen buiten')],
      meter=dict(label='Draagtijd tegenover de norm van 80%',
                 staven=[('Gemiddeld', 71), ('Thuis', 61), ('Buitenshuis', 87)]),
      voet='Waaijman et al. · Diabetes Care 2013 · 107 patiënten',
      accent='licht',
      tip='Het venijn zit in de derde tegel: binnen zetten ze méér stappen dan buiten.',
      interactie='Vraag: "wat schat u dat úw patiënten halen?" Laat ze roepen voor u klikt.'),

 dict(t='formule', morph='morph',
      kicker='Het mechanisme',
      kop='Belasting is een product,\ngeen optelsom',
      delen=[('Piekdruk', 'per stap', 'licht', 'Bijgestuurd'),
             ('Activiteit', 'stappen per dag', 'gedempt', 'Gemeten'),
             ('Draagtijd', 'wérd hij gedragen', 'licht', 'Bijgestuurd')],
      slot='Eén factor op nul maakt het product nul. Daarom sturen we er twee bij.',
      tip='Teken het maalteken in de lucht. Product, niet som — dat is het hele punt.',
      interactie='Morph: de drie tegels komen samen uit één punt.'),

 dict(t='sectie', morph='morph', nr='02', titel='De interventie',
      regel='Twee componenten. Bovenop wat u al doet.'),

 dict(t='drukmeting', morph='morph', fase='voor',
      kicker='Wat u ziet bij de meting',
      kop='Elke sensor een cijfer',
      waarde='312', plek='piekdruk op metatarsaal 2-3',
      norm='Norm:  < 200 kPa   óf   ≥ 25% lager',
      regels=['Dit is een echte in-shoe meting: honderden sensoren onder de voet, '
              'elk met hun eigen piekdruk over minstens twaalf mid-gait stappen.',
              'De hete plek ligt waar de meeste plantaire ulcera ontstaan. '
              'Deze patiënt zit ruim boven de norm.'],
      voet='Novel pedar · in-shoe · piekdruk per regio via Multimask',
      tip='Wijs de rode plek aan. Zeg er niets bij. Klik dan pas door.',
      interactie='Vraag: "waar verwacht u de piek?" Laat ze wijzen voor u de dia toont.'),

 dict(t='drukzoom', morph='morph', fase='voor',
      kicker='Inzoomen op de voorvoet',
      kop='Waar de norm getoetst wordt',
      waarde='312',
      # naam, uitleg, en de plek op de voet (0-1 in de breedte, 0 = hiel tot 1 = teen)
      regios=[('Metatarsaal 1', 'onder de grote teen — tweede meest getroffen plek', 0.30, 0.68),
              ('Metatarsaal 2-3', 'de hete plek op deze meting, en de klassieke ulcusplek', 0.44, 0.66),
              ('Metatarsaal 4-5', 'laterale voorvoet, meestal lagere druk', 0.70, 0.63),
              ('Hallux', 'apart bekeken, niet meer samengeteld met de tenen', 0.28, 0.91),
              ('Tenen 2-5', 'eigen regio sinds de laatste maskerversie', 0.55, 0.90)],
      voet='Acht regio\'s via Multimask · hier vijf van de voorvoet in beeld',
      tip='De camera duikt de voet in. Zeg: "dit is wat de software eruit haalt — '
          'niet één getal voor de hele voet, maar acht."',
      interactie='Vraag de podologen of ze de maskers zelf al gelegd hebben.'),

 dict(t='drukmeting', morph='morph', fase='na',
      kicker='Wat de zool ermee doet',
      kop='Dezelfde voet, andere verdeling',
      waarde='186', plek='piekdruk na optimalisatie — norm gehaald',
      norm='40% lager  ·  onder 200 kPa  ·  beide criteria',
      regels=['Dezelfde sensoren, dezelfde patiënt. De maatzool haalt druk weg onder '
              'de metatarsaalkoppen en legt die terug in de voetboog.',
              'Dat is de hele interventie: niet minder belasting, maar belasting '
              'op een plek die het aankan.'],
      voet='Illustratief voorbeeld van een drukgestuurde aanpassing',
      tip='Dit is de morph waar het om draait: de hete plek koelt af terwijl de '
          'voetboog oplicht. Klik traag en zwijg tot de animatie klaar is.',
      interactie='Vraag daarna: "en hoe weet u of hij hem draagt?" Dat is de brug '
                 'naar de tweede component.'),

 dict(t='duo', morph='morph',
      kicker='PARADISE',
      kop='Meten én laten dragen',
      een=dict(nr='01', naam='Drukgestuurde optimalisatie',
               kern='< 200 kPa   óf   ≥ 25% lager',
               regels=['In-shoe meting met Novel pedar, door uw team',
                       'Zool aangepast tot de norm gehaald is',
                       'Herhaald op 6 en 12 maanden']),
      twee=dict(nr='02', naam='SEBIA — gedragsbegeleiding',
                kern='5 stappen   ·   18 maanden',
                regels=['Individueel, in het gewone consult',
                        'Sensordata samen bekijken, niet-veroordelend',
                        'COM-B: kennis, gelegenheid én motivatie']),
      tip='Benadruk "óf". Twee wegen naar dezelfde norm, geen dubbele eis.',
      interactie='Morph: de twee blokken kantelen naar voren.'),

 dict(t='statraster', morph='morph',
      kicker='De studie',
      kop='144 patiënten, willekeurig verdeeld',
      matrix=True,
      groot=[('144', 'deelnemers'), ('24', 'per kliniek'), ('18', 'maanden'), ('1:1', 'toewijzing')],
      klein=[('Ontwerp', 'Multicentrisch · open-label · superioriteit'),
             ('Controlegroep', 'Gebruikelijke zorg, onveranderd'),
             ('Co-primair', 'Recidief op 18 mnd  +  draagtijd op 12 mnd'),
             ('Positief', 'Alleen als béíde eindpunten halen')],
      tip='De laatste tegel is de belangrijkste: wij hebben twee eindpunten nodig, '
          'niet één. Dat maakt de lat hoog en dat weten we.',
      interactie='Geen. Laat ze lezen.'),

 dict(t='dubbelkolom', morph='morph',
      kicker='Selectie',
      kop='Wie komt in aanmerking',
      links=dict(titel='Wél', kleur='licht',
                 items=['IWGDF-risicocategorie 3',
                        'Genezen plantair ulcus of partiële amputatie',
                        'PEDIS-perfusie 1 of 2, stabiel',
                        'Stapt zelfstandig blootsvoets',
                        'Heeft of aanvaardt maatschoeisel',
                        'Begrijpt Nederlands']),
      rechts=dict(titel='Niet', kleur='oranje',
                  items=['Kritische ischemie',
                         'Actief ulcus of Charcot',
                         'Nierfunctievervanging',
                         'Immunosuppressie',
                         'Overleving < 18 maanden']),
      tip='Loop niet elk criterium af. Zeg: "categorie 3, vaatstatus in orde, '
          'spreekt Nederlands" — de rest staat op papier.',
      interactie='Deel de screeningskaart uit terwijl u praat.'),

 dict(t='traject', morph='morph',
      kicker='Het traject',
      kop='Negen contactmomenten',
      groot='18',
      punt='maanden, van screening tot afronding',
      slot='Het ritme is elke drie maanden: hetzelfde ritme als de controle die '
           'deze patiënten volgens de richtlijn al krijgen.',
      tip='Dit is voor een deel van de zaal de eerste kennismaking met het '
          'traject. Geef eerst het overzicht, klik dan door: de tijdlijn zoomt '
          'in op elke fase en komt op het eind weer terug.',
      interactie='Vraag voor u inzoomt: "over welke fase wilt u het meest weten?" '
                 'Zoom dan als eerste naar die fase.'),

 dict(t='zoom', morph='morph', schaal=2.4, mid=291,
      kicker='Fase 1 · vóór de eerste zool',
      kop='Screening en baseline',
      paneel=dict(titel='Wat er gebeurt',
                  regels=['Screening: risicocategorie 3, vaatstatus en of de patiënt '
                          'zelfstandig stapt. Kort, en vóór de toestemming.',
                          'Baseline: drukmeting met de pedar, een week MoveMonitor mee '
                          'naar huis, en het eerste SEBIA-gesprek.']),
      tip='Leg uit dat de screening vóór de toestemming gebeurt en dus kort is: '
          'u kijkt enkel of iemand in aanmerking komt.',
      interactie='Morph: de camera zoomt in op de eerste twee stippen.'),

 dict(t='zoom', morph='morph', schaal=2.4, mid=673,
      kicker='Fase 2 · de zool komt',
      kop='Maand 1 en maand 3',
      paneel=dict(titel='Wat er gebeurt',
                  regels=['Maand 1: het voorschrift voor de maatzool. Een kort '
                          'bezoek, zonder meting.',
                          'Maand 3: aflevering, de Orthotimer gaat in de zool, en de '
                          'meting wordt herhaald tot de norm gehaald is.']),
      tip='Hier zit het meeste werk voor de pedorthist. Kijk hem of haar aan.',
      interactie='Vraag aan de pedorthist hoeveel aanpassingsrondes realistisch zijn.'),

 dict(t='zoom', morph='morph', schaal=1.5, mid=1350, ox=1020,
      kicker='Fase 3 · de rest van het jaar',
      kop='Zes tot achttien maanden',
      paneel=dict(titel='Wat er gebeurt',
                  regels=['Elke drie maanden: sensor uitlezen, batterij vervangen, '
                          'SEBIA-gesprek in het gewone consult.',
                          'Op 6 en 12 maanden ook een drukmeting. Twaalf maanden is '
                          'het primaire analysepunt voor de draagtijd.']),
      tip='Benadruk: uitlezen en vervangen kan alleen ter plaatse, dus koppel het '
          'aan een bezoek dat toch al gepland is.',
      interactie='Morph: de camera trekt terug en toont de hele staart.'),

 dict(t='traject', morph='morph',
      kicker='Het traject',
      kop='Terug naar het geheel',
      groot='9',
      punt='momenten, één zorgpad',
      slot='Het verschil met vandaag zit niet in hoe vaak u de patiënt ziet, maar '
           'in wat u bij elk bezoek wéét: wat de zool doet en wat er gedragen is.',
      tip='Dit is dezelfde dia als het begin van het blok. De zaal herkent hem, '
          'en dat is precies het effect dat u wilt.',
      interactie='Laat hem staan tijdens de vragen over het traject.'),

 dict(t='vijfluik', morph='morph',
      kicker='SEBIA',
      kop='Vijf stappen',
      stappen=[('01', 'Baseline', 'Kennis meten. Educatie op maat, met oefenen.'),
               ('02', '3 mnd', 'Teach-back. Nadruk op bínnenshuis dragen.'),
               ('03', '6 · 12 mnd', 'Zelfinschatting, dan samen de data bekijken.'),
               ('04', '9 · 15 mnd', 'Voordoen. Uitdraai vergelijken met vorige keer.'),
               ('05', '18 mnd', 'Afsluiten en resultaten delen.')],
      tip='Stap 3 is het hart: eerst láát u hem schatten, dán toont u de data.',
      interactie='Rollenspel van twee minuten met een vrijwilliger uit de zaal.'),

 dict(t='aflopend', morph='morph',
      foto='sensor_vol.png',
      kicker='De tweede component, in het echt',
      kop='Negen bij dertien millimeter.\nMeer merkt de patiënt niet.',
      tip='Laat deze dia even staan zonder te praten. De sensor is fysiek zo klein '
          'dat het beeld het argument al maakt.',
      interactie='Geef er een door de zaal terwijl u praat.'),

 dict(t='drieluik', morph='morph',
      kicker='De techniek',
      kop='Drie toestellen',
      kaarten=[dict(naam='Novel pedar', sub='Druk', groot='8', onder='voetregio\'s',
                    foto='pedar.png',
                    regels=['Draadloze sensorzolen in de eigen schoen',
                            'Trublu-kalibratie op 6 bar, elke drie maanden',
                            'Minstens twaalf mid-gait stappen per voet'],
                    wie='Uw team meet'),
               dict(naam='Orthotimer', sub='Draagtijd', groot='15', onder='minuten',
                    foto='orthotimer.png',
                    regels=['In de zool, 9 × 13 × 4,5 mm',
                            'Batterij 100 dagen'],
                    wie='Heet: uw sensor'),
               dict(naam='MoveMonitor', sub='Activiteit', groot='7', onder='dagen',
                    foto='movemonitor.png', vlak='glas',
                    regels=['Op de onderrug, niet waterdicht',
                            'Baseline en 6 maanden'],
                    wie='Zet de 80%-norm')],
      tip='Benoem dat de Orthotimer géén GPS, microfoon of camera heeft. '
          'Die vraag komt gegarandeerd.',
      interactie='Laat de toestellen rondgaan. Fysiek werkt beter dan een dia.'),

 dict(t='sectie', morph='morph', nr='03', titel='Uw rol',
      regel='Minder dan u vreest. Maar niet niets.'),

 dict(t='vierluik', morph='morph',
      kicker='Verdeling',
      kop='Wie doet wat',
      kolommen=[('Podoloog', ['Voert de drukmeting uit', 'Levert SEBIA', 'Leest sensoren uit']),
                ('Pedorthist', ['Maakt de zool', 'Past aan tot de norm', 'Integreert de sensor']),
                ('Arts', ['Bevestigt geschiktheid', 'Beoordeelt laesies', 'Meldt voorvallen']),
                ('Management', ['Maakt tijd vrij', 'Faciliteert opleiding', 'Bewaakt 24 inclusies'])],
      tip='Kijk elke groep aan bij hun kolom. Namen noemen als u ze kent.',
      interactie='Vraag per kolom: "herkenbaar, of mis ik iets?"'),

 dict(t='statement', morph='morph',
      kicker='De enige regel die u écht moet onthouden',
      kop='Meetwaarden gaan\nniet naar de\ncontrolegroep',
      body='Ook zij krijgen een drukmeting en dragen een sensor — anders kunnen we de '
           'groepen niet vergelijken. Maar die getallen blijven dicht. Bespreekt u ze, '
           'dan lévert u de interventie.',
      uitzondering='Klinische bevindingen zijn géén meetwaarden. Elke laesie of '
                   'huiddefect meldt en behandelt u meteen. In beide groepen.',
      tip='Dit is de dia waar u stilvalt. Geen haast. Vraag of het helder is '
          'voordat u doorgaat.',
      interactie='Laat iemand het in eigen woorden herhalen. Zo weet u of het zit.'),

 dict(t='eerlijk', morph='morph',
      kicker='De vraag die u niet hardop stelt',
      kop='Wat kost dit mij?',
      intro='Geen verzonnen getal. Dit komt erbij:',
      rijen=[('Drukmeting', 'baseline · 6 · 12 maanden'),
             ('SEBIA', 'in het bestaande consult'),
             ('Sensor', 'uitlezen en vervangen per bezoek'),
             ('Opleiding', 'eenmalig, door ons verzorgd')],
      slot='Hoeveel het wérkelijk kost, meten we. Dat is precies wat een '
           'implementatiestudie hoort te doen.',
      tip='Wees hier eerlijk. Als u een getal verzint dat niet klopt, bent u ze kwijt.',
      interactie='Poll: "hoeveel minuten schat u?" Noteer de spreiding en kom er '
                 'na zes maanden op terug.'),

 dict(t='pauze', morph='morph',
      kicker='Rustpunt',
      kop='Vragen?',
      regel='Voor we naar de afspraken gaan.',
      tip='Plan hier vijf minuten. Als er geen vragen komen, stel er zelf één: '
          '"wat lijkt u het lastigst?"',
      interactie='Open moment. Noteer wat er komt — het voedt de procesevaluatie.'),

 dict(t='steun', morph='morph',
      kicker='Ondersteuning',
      kop='Wat u van ons krijgt',
      rijen=[('Motiverende gespreksvoering',
              'Training door een psycholoog — alle centra dezelfde'),
             ('Pedar en SEBIA',
              'Werkinstructie en draaiboek per handeling'),
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
             ('Zool haalt de norm niet', 'We noteren wat wél bereikt is en gaan door.'),
             ('Mag ik nog adviseren?', 'Alles wat u vandaag doet, blijft u doen.'),
             ('Wij zijn niet academisch', 'Drie van de zes centra ook niet. Dat wordt getoetst.'),
             ('Onze data?', 'Gepseudonimiseerd, tien jaar, binnen de toestemming.'),
             ('Zien wij resultaten?', 'Eén publicatie, ongeacht de uitkomst.')],
      tip='Sla over wat al gevraagd is. Deze dia is een vangnet, geen programma.',
      interactie='Toon hem alleen als de vragen opdrogen.'),

 dict(t='afspraak', morph='morph',
      kicker='De afspraak',
      kop='Vier dingen',
      tegels=[('24', 'deelnemers', 'over twaalf maanden'),
              ('1', 'vaste PI', 'plus gedelegeerd team'),
              ('10 m', 'looppad', 'meer ruimte is niet nodig'),
              ('1', 'dagboek', 'voor de procesevaluatie')],
      tip='Eindig hier als u tijd tekortkomt. Dit is de dia die telt.',
      interactie='Vraag ter plekke of het haalbaar lijkt. Twijfel nu is beter dan '
                 'uitval straks.'),

 dict(t='slot', morph='morph',
      kop='Doe mee',
      regel='PARADISE start zodra de goedkeuringen binnen zijn.',
      voet='Protocolversie 1.0 · 17 mei 2026 · S71769',
      tip='Twee woorden, verder niets. Dit is het moment waarop u vraagt of ze '
          'meedoen — laat de dia dat niet verzachten.',
      interactie='Deel de eenpager uit. Vraag wie een inclusiekandidaat in gedachten heeft.'),

 dict(t='contact', morph='morph',
      kicker='Wie u aanspreekt',
      kop='Voor als er iets misloopt',
      personen=[
          dict(naam='Janou De Buyser',
               rol='Doctoraatsonderzoeker · dagelijkse opvolging',
               waarvoor='Uw eerste aanspreekpunt: inclusies, metingen, REDCap, '
                        'sensoren en alles wat in de praktijk vastloopt.',
               bereik=['▮ e-mailadres', '▮ telefoonnummer']),
          dict(naam='prof. dr. Kevin Deschamps',
               rol='Promotor',
               waarvoor='Wetenschappelijke vragen, de opzet van de studie en '
                        'afspraken op het niveau van uw centrum.',
               bereik=['kevin.deschamps@kuleuven.be',
                       'KU Leuven · Campus Brugge']),
      ],
      voet='PARADISE · FWO TBM T000226N · S71769',
      tip='Laat deze dia staan tijdens het napraten. Zeg erbij dat kleine dingen '
          'ook mogen — een sensor die niet uitleest is geen domme vraag.',
      interactie='Loop rond terwijl de dia staat. Wie een vraag heeft, komt naar '
                 'het gezicht dat op het scherm staat.'),
]
