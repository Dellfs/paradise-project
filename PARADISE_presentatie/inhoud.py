# -*- coding: utf-8 -*-
"""PARADISE — informatiesessie voor de diabetische voetklinieken.

Ontwerpprincipes: dark mode, bento-grid, één kernboodschap per dia, typografie
als visueel element, geen opsommingstekens. Elke dia draagt een morph-overgang.

Alle cijfers komen uit het protocol (versie 1.0, 17/05/2026) en het
geverifieerde manuscript.
"""

K = {
    'bg':      '0B1622',
    'tegel':   '16242F',
    'tegel2':  '1E3040',
    'glas':    '223749',
    'rand':    '2C4356',
    'ink':     'F4F8FB',
    'gedempt': '93A9BA',
    'teal':    '2BB9AD',
    'teal_d':  '0E7C86',
    'amber':   'E0A33D',
    'koraal':  'E4674E',
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
      accent='koraal',
      tip='Laat het getal even alleen staan. Zeg dan pas: "dit is uw eigen praktijk."',
      interactie='Morph vanaf de sectiedia: het cijfer groeit uit de titel.'),

 dict(t='splitsing', morph='morph',
      kicker='Dezelfde schoen, twee uitkomsten',
      kop='Het lag niet aan de zool',
      links=dict(titel='Iedereen', sub='intention-to-treat', groot='38,8',
                 klein='tegenover 44,2%', slot='Geen verschil', kleur='koraal'),
      rechts=dict(titel='Wie hem droeg', sub='≥ 80% van de stappen', groot='25,7',
                  klein='tegenover 47,8%', slot='Bijna gehalveerd', kleur='teal'),
      punchline='De interventie werkte. Bij de 46% die hem aandeed.',
      voet='Bus et al. · Diabetes Care 2013 · DIAFOS, 171 deelnemers',
      tip='Wijs eerst links aan, laat het bezinken, wijs dan rechts. '
          'De punchline zegt u, niet de dia.',
      interactie='Morph: beide blokken schuiven uit het midden uit elkaar.'),

 dict(t='hero_cijfer', morph='morph',
      cijfer='71', suffix='%',
      kop='draagtijd — gemeten,\nniet gevraagd',
      tegels=[('61%', 'thuis'), ('4000', 'stappen binnen'), ('2600', 'stappen buiten')],
      voet='Waaijman et al. · Diabetes Care 2013 · 107 patiënten',
      accent='amber',
      tip='Het venijn zit in de derde tegel: binnen zetten ze méér stappen dan buiten.',
      interactie='Vraag: "wat schat u dat úw patiënten halen?" Laat ze roepen voor u klikt.'),

 dict(t='formule', morph='morph',
      kicker='Het mechanisme',
      kop='Belasting is een product,\ngeen optelsom',
      delen=[('Piekdruk', 'per stap', 'teal', 'Bijgestuurd'),
             ('Activiteit', 'stappen per dag', 'gedempt', 'Gemeten'),
             ('Draagtijd', 'wérd hij gedragen', 'teal', 'Bijgestuurd')],
      slot='Eén factor op nul maakt het product nul. Daarom sturen we er twee bij.',
      tip='Teken het maalteken in de lucht. Product, niet som — dat is het hele punt.',
      interactie='Morph: de drie tegels komen samen uit één punt.'),

 dict(t='sectie', morph='morph', nr='02', titel='De interventie',
      regel='Twee componenten. Bovenop wat u al doet.'),

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
      kop='In één oogopslag',
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
      links=dict(titel='Wél', kleur='teal',
                 items=['IWGDF-risicocategorie 3',
                        'Genezen plantair ulcus of partiële amputatie',
                        'PEDIS-perfusie 1 of 2, stabiel',
                        'Stapt zelfstandig blootsvoets',
                        'Heeft of aanvaardt maatschoeisel',
                        'Begrijpt Nederlands']),
      rechts=dict(titel='Niet', kleur='koraal',
                  items=['Kritische ischemie',
                         'Actief ulcus of Charcot',
                         'Nierfunctievervanging',
                         'Immunosuppressie',
                         'Overleving < 18 maanden']),
      tip='Loop niet elk criterium af. Zeg: "categorie 3, vaatstatus in orde, '
          'spreekt Nederlands" — de rest staat op papier.',
      interactie='Deel de screeningskaart uit terwijl u praat.'),

 dict(t='tijdlijn', morph='morph',
      kicker='Het traject',
      kop='Negen momenten',
      punten=[('Screen', ''), ('Base', 'meting'), ('1', 'voorschrift'),
              ('3', 'zool + sensor'), ('6', 'meting'), ('9', ''),
              ('12', 'meting'), ('15', ''), ('18', 'einde')],
      slot='Acht van de negen vallen samen met de controle die de patiënt sowieso '
           'al krijgt. Alleen screening en maand 1 komen erbij.',
      tip='Dit is uw belangrijkste geruststelling. Zeg het traag.',
      interactie='Morph: de tijdlijn schuift in vanaf links.'),

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

 dict(t='drieluik', morph='morph',
      kicker='De techniek',
      kop='Drie toestellen',
      kaarten=[dict(naam='pedar', sub='Druk', groot='8', onder='voetregio\'s',
                    regels=['Trublu-kalibratie, 6 bar', '≥ 12 mid-gait stappen'],
                    wie='Uw team meet'),
               dict(naam='Orthotimer', sub='Draagtijd', groot='15', onder='minuten',
                    regels=['In de zool, 9 × 13 × 4,5 mm', 'Batterij 100 dagen'],
                    wie='Heet: uw sensor'),
               dict(naam='MoveMonitor', sub='Activiteit', groot='7', onder='dagen',
                    regels=['Op de onderrug', 'Baseline en 6 maanden'],
                    wie='Zet de norm')],
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

 dict(t='statraster', morph='morph',
      kicker='Ondersteuning',
      kop='Wat u van ons krijgt',
      groot=[('MI', 'training'), ('SOP', 'per handeling'), ('1', 'contactpunt'), ('0', 'sancties')],
      klein=[('Motiverende gespreksvoering', 'Training door een psycholoog, alle centra gelijk'),
             ('Pedar en SEBIA', 'Werkinstructie en draaiboek per stap'),
             ('REDCap', 'Instructie plus testomgeving om te oefenen'),
             ('Protocolafwijkingen', 'Melden. Ze worden geregistreerd, niet afgestraft')],
      tip='De laatste tegel ontspant de zaal. Zeg hem expliciet.',
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
      contact=['Janou De Buyser · doctoraatsonderzoeker',
               'KU Leuven · Revalidatiewetenschappen · Campus Brugge',
               'prof. dr. Kevin Deschamps · kevin.deschamps@kuleuven.be'],
      voet='Protocolversie 1.0 · 17 mei 2026 · S71769',
      tip='Laat deze staan tijdens het napraten. Contactgegevens moeten zichtbaar '
          'blijven terwijl mensen naar u toe komen.',
      interactie='Deel de eenpager uit. Vraag wie een inclusiekandidaat in gedachten heeft.'),
]
