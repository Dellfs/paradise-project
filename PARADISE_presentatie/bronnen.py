# -*- coding: utf-8 -*-
"""De referentielijst van het protocolmanuscript.

De nummering is **identiek** aan die in `protocol paper/
PARADISE_protocol_manuscript.docx`, zodat een dia en het manuscript naar
hetzelfde nummer verwijzen. Wijzigt de volgorde in het manuscript, dan wijzigt
ze hier mee — niet omgekeerd.

Per dia zet u in `inhoud.py` een veld `bron=(9, 13)`. De bouwer zet dan
linksonder een korte verwijzing op de dia, en verzamelt alle gebruikte nummers
in een referentiedia achteraan het deck.
"""

REF = {
 1: ('Armstrong 2017',
     'Armstrong DG, Boulton AJM, Bus SA. Diabetic foot ulcers and their '
     'recurrence. N Engl J Med. 2017;376(24):2367–75.'),
 2: ('Jupiter 2016',
     'Jupiter DC, Thorud JC, Buckley CJ, Shibuya N. The impact of foot '
     'ulceration and amputation on mortality in diabetic patients. Int Wound J. '
     '2016;13(5):892–903.'),
 3: ('Kerr 2019',
     'Kerr M, Barron E, Chadwick P, Evans T, Kong WM, Rayman G, et al. The cost '
     'of diabetic foot ulcers and amputations to the National Health Service in '
     'England. Diabet Med. 2019;36(8):995–1002.'),
 4: ('Prompers 2008',
     'Prompers L, Schaper N, Apelqvist J, Edmonds M, Jude E, Mauricio D, et al. '
     'Prediction of outcome in individuals with diabetic foot ulcers. '
     'Diabetologia. 2008;51(5):747–55.'),
 5: ('Bus & van Netten 2016',
     'Bus SA, van Netten JJ. A shift in priority in diabetic foot care and '
     'research: 75% of foot ulcers are preventable. Diabetes Metab Res Rev. '
     '2016;32(Suppl 1):195–200.'),
 6: ('Bus 2011',
     'Bus SA, Haspels R, Busch-Westbroek TE. Evaluation and optimization of '
     'therapeutic footwear for neuropathic diabetic foot patients using in-shoe '
     'plantar pressure analysis. Diabetes Care. 2011;34(7):1595–600.'),
 7: ('Bus 2020',
     'Bus SA, Zwaferink JB, Dahmen R, Busch-Westbroek T. State of the art '
     'design protocol for custom made footwear for people with diabetes and '
     'peripheral neuropathy. Diabetes Metab Res Rev. 2020;36(S1):e3237.'),
 8: ('IWGDF 2023, preventie',
     'Bus SA, Sacco ICN, Monteiro-Soares M, Raspovic A, Paton J, Rasmussen A, '
     'et al. Guidelines on the prevention of foot ulcers in persons with '
     'diabetes (IWGDF 2023 update). Diabetes Metab Res Rev. 2024;40(3):e3651.'),
 9: ('Bus 2013, DIAFOS',
     'Bus SA, Waaijman R, Arts M, de Haart M, Busch-Westbroek T, van Baal J, et '
     'al. Effect of custom-made footwear on foot ulcer recurrence in diabetes: '
     'a multicenter randomized controlled trial. Diabetes Care. '
     '2013;36(12):4109–16.'),
 10: ('van Netten 2016',
      'van Netten JJ, Price PE, Lavery LA, Monteiro-Soares M, Rasmussen A, '
      'Jubiz Y, et al. Prevention of foot ulcers in the at-risk patient with '
      'diabetes: a systematic review. Diabetes Metab Res Rev. '
      '2016;32(Suppl 1):84–98.'),
 11: ('Lincoln 2008',
      'Lincoln NB, Radford KA, Game FL, Jeffcoate WJ. Education for secondary '
      'prevention of foot ulcers in people with diabetes: a randomised '
      'controlled trial. Diabetologia. 2008;51(11):1954–61.'),
 12: ('Abbott 2019',
      'Abbott CA, Chatwin KE, Foden P, Hasan AN, Sange C, Rajbhandari SM, et '
      'al. Innovative intelligent insole system reduces diabetic foot ulcer '
      'recurrence at plantar sites. Lancet Digit Health. 2019;1(6):e308–18.'),
 13: ('Waaijman 2013',
      'Waaijman R, Keukenkamp R, de Haart M, Polomski WP, Nollet F, Bus SA. '
      'Adherence to wearing prescription custom-made footwear in patients with '
      'diabetes at high risk for plantar foot ulceration. Diabetes Care. '
      '2013;36(6):1613–8.'),
 14: ('van Netten 2018',
      'van Netten JJ, van Baal JG, Bril A, Wissink M, Bus SA. An exploratory '
      'study on differences in cumulative plantar tissue stress between healing '
      'and non-healing plantar neuropathic diabetic foot ulcers. Clin Biomech. '
      '2018;53:86–92.'),
 15: ('Hulshof 2024',
      'Hulshof CM, Page M, van Baal SG, Bus SA, Fernando ME, van '
      'Gemert-Pijnen L, et al. The stress of measuring plantar tissue stress in '
      'people with diabetes-related foot ulcers. Sensors. 2024;24(8):2411.'),
 16: ('Hulshof 2025',
      'Hulshof CM, van Netten JJ, Busch-Westbroek TE, Sabelis LWE, Peters EJG, '
      'Pijnappels M, et al. The predictive value of cumulative plantar tissue '
      'stress on future plantar foot ulceration in people with diabetes. '
      'Diabet Med. 2025;42:e70099.'),
 17: ('Waaijman 2014',
      'Waaijman R, de Haart M, Arts MLJ, Wever D, Verlouw AJWE, Nollet F, et '
      'al. Risk factors for plantar foot ulcer recurrence in neuropathic '
      'diabetic patients. Diabetes Care. 2014;37(6):1697–705.'),
 18: ('Lutjeboer 2018',
      'Lutjeboer T, van Netten JJ, Postema K, Hijmans JM. Validity and '
      'feasibility of a temperature sensor for measuring use and non-use of '
      'orthopaedic footwear. J Rehabil Med. 2018;50(10):920–6.'),
 19: ('Michie 2011, COM-B',
      'Michie S, van Stralen MM, West R. The behaviour change wheel: a new '
      'method for characterising and designing behaviour change interventions. '
      'Implement Sci. 2011;6:42.'),
 20: ('Morbach 2016',
      'Morbach S, Kersken J, Lobmann R, Nobels F, Doggen K, Van Acker K. The '
      'German and Belgian accreditation models for diabetic foot services. '
      'Diabetes Metab Res Rev. 2016;32(Suppl 1):318–25.'),
 21: ('SPIRIT 2025',
      'Chan A-W, Boutron I, Hopewell S, Moher D, Schulz KF, Collins GS, et al. '
      'SPIRIT 2025 statement: updated guideline for protocols of randomised '
      'trials. BMJ. 2025;389:e081477.'),
 22: ('TIDieR',
      'Hoffmann TC, Glasziou PP, Boutron I, Milne R, Perera R, Moher D, et al. '
      'Better reporting of interventions: the TIDieR checklist and guide. BMJ. '
      '2014;348:g1687.'),
 23: ('PRECIS-2',
      'Loudon K, Treweek S, Sullivan F, Donnan PT, Thorpe KE, Zwarenstein M. '
      'The PRECIS-2 tool: designing trials that are fit for purpose. BMJ. '
      '2015;350:h2147.'),
 24: ('CONSORT 2025',
      'Hopewell S, Chan A-W, Collins GS, Hróbjartsson A, Moher D, Schulz KF, '
      'et al. CONSORT 2025 statement: updated guideline for reporting '
      'randomised trials. BMJ. 2025;389:e081123.'),
 25: ('IWGDF 2023, definities',
      'van Netten JJ, Bus SA, Apelqvist J, Chen P, Chuter V, Fitridge R, et al. '
      'Definitions and criteria for diabetes-related foot disease (IWGDF 2023 '
      'update). Diabetes Metab Res Rev. 2024;40(3):e3654.'),
 26: ('Lincoln 2007, NAFF',
      'Lincoln NB, Jeffcoate WJ, Ince P, Smith M, Radford KA. Validation of a '
      'new measure of protective footcare behaviour: the Nottingham Assessment '
      'of Functional Footcare (NAFF). Pract Diabetes Int. 2007;24(4):207–11.'),
 27: ('Zwaferink 2024',
      'Zwaferink JBJ, Nollet F, Bus SA. In-shoe pressure measurements in '
      'diabetic footwear practice: success rate and facilitators of and '
      'barriers to implementation. Sensors. 2024;24(6):1795.'),
 28: ('van Netten 2025',
      'van Netten JJ, Vossen LE, Driebergen FM, Wolthuis D, Merkx MJM, Bus SA. '
      'Short-term efficacy of a multi-modal intervention program to improve '
      'custom-made footwear use in people at high risk of diabetes-related foot '
      'ulceration. J Clin Med. 2025;14(11):3635.'),
 29: ('Dahmen 2018',
      'Dahmen R, Siemonsma PC, Monteiro S, Roorda LD, Lankhorst GJ, Boers M. '
      'Evaluation of the wear-and-tear scale for therapeutic footwear. J '
      'Rehabil Med. 2018;50(6):569–74.'),
 30: ('Staniszewska 2024, COS',
      'Staniszewska A, Game F, Nixon J, Russell D, Armstrong DG, Ashmore C, et '
      'al. Development of a core outcome set for studies assessing '
      'interventions for diabetes-related foot ulceration. Diabetes Care. '
      '2024;47(11):1958–68.'),
 31: ('Keukenkamp 2022',
      'Keukenkamp R, van Netten JJ, Busch-Westbroek TE, Bus SA. Custom-made '
      'footwear designed for indoor use increases short-term and long-term '
      'adherence in people with diabetes at high ulcer risk. BMJ Open Diabetes '
      'Res Care. 2022;10(1):e002593.'),
 32: ('Staniszewska 2026, CDS',
      'Staniszewska A, Jones A, Davies L, Game F, Nixon J, Russell D, et al. '
      'Development of a core descriptor set for studies assessing interventions '
      'for diabetes-related foot ulcers. Diabetologia. 2026.'),
 33: ('Bus 2026, kosten',
      'Bus SA, van Netten JJ, Schouten DR, Dijkgraaf MGW. Cost-effectiveness of '
      'pressure-guided-offloading-improved custom-made footwear for people with '
      'diabetes at high risk of plantar foot ulceration. Diabetology. '
      '2026;7(4):70.'),
 34: ('CHEERS',
      'Husereau D, Drummond M, Petrou S, Carswell C, Moher D, Greenberg D, et '
      'al. Consolidated Health Economic Evaluation Reporting Standards (CHEERS) '
      'statement. Pharmacoeconomics. 2013;31(5):361–7.'),
 35: ('Kostenhandleiding 2024',
      'Hakkaart-van Roijen L, Peeters S, Kanters T. Kostenhandleiding voor '
      'economische evaluaties in de gezondheidszorg. Diemen: Zorginstituut '
      'Nederland; 2024.'),
 36: ('Prompers 2008, Eurodiale',
      'Prompers L, Huijberts M, Schaper N, Apelqvist J, Bakker K, Edmonds M, et '
      'al. Resource utilisation and costs associated with the treatment of '
      'diabetic foot ulcers. Diabetologia. 2008;51(10):1826–34.'),
 37: ('Ragnarson Tennvall 2001',
      'Ragnarson Tennvall G, Apelqvist J. Prevention of diabetes-related foot '
      'ulcers and amputations: a cost-utility analysis based on Markov model '
      'simulations. Diabetologia. 2001;44(11):2077–87.'),
 38: ('Ortegon 2004',
      'Ortegon MM, Redekop WK, Niessen LW. Cost-effectiveness of prevention and '
      'treatment of the diabetic foot: a Markov analysis. Diabetes Care. '
      '2004;27(4):901–7.'),
 39: ('van Netten 2024, kosten',
      'van Netten JJ, aan de Stegge WB, Dijkgraaf MGW, Bus SA. '
      'Cost-effectiveness of temperature monitoring to help prevent foot ulcer '
      'recurrence in people with diabetes. Diabetes Metab Res Rev. '
      '2024;40(4):e3805.'),
 40: ('MRC 2015',
      'Moore GF, Audrey S, Barker M, Bond L, Bonell C, Hardeman W, et al. '
      'Process evaluation of complex interventions: Medical Research Council '
      'guidance. BMJ. 2015;350:h1258.'),
}


# Welke dia op welke referentie steunt. De sleutel is de kop van de dia,
# dezelfde als in spreektekst.py. Een dia die geen externe bewering doet — een
# hoofdstukdia, het bezoekschema, de contactdia — staat hier niet in.
BIJ_DIA = {
    'krijgt binnen een jaar\neen nieuw ulcus': (1,),
    'Driekwart is te voorkomen.\nVeertig procent komt terug.': (1, 5),
    'Drie strategieën, één patroon': (9, 10, 12),
    'Waarom druk alléén niet volstaat': (9,),
    'draagtijd — gemeten,\nniet gevraagd': (13,),
    'Belasting is een product,\ngeen optelsom': (14, 16),
    'Drie dingen zijn veranderd': (18, 19, 20),
    'Eén dienst, geen drie losse maatregelen': (6, 7, 17),
    'Elke sensor een cijfer': (7, 27),
    "Acht regio's, drie doelregio's": (7,),
    'Wanneer is het goed genoeg': (6, 7),
    'Drie condities bij de aflevering': (7,),
    'Wie komt in aanmerking': (8, 25),
    'Drie toestellen': (18,),
    'Hoe de CMFO is opgebouwd': (7,),
    'Orthotimer instellen': (18,),
    'Vijf gespreksmomenten': (19, 26, 31),
    'Twee eindpunten, twee berekeningen': (9, 13),
    'De power die telt, is de gezamenlijke': (9,),
    'Hoe we het toetsen': (21, 24),
    'Twee evaluaties, parallel': (33, 34, 35, 40),
    'Een nulresultaat is ook een resultaat': (15, 16),
    'Het opleidingsregister': (21,),
    'Wat er drie keer extra bij komt': (7,),
    'Aflevering, optimalisatie en sensor': (6, 7),
    'Baseline — meten en voorschrijven': (7, 26),
    'Driemaandelijkse opvolging': (18, 29),
    'Wie doet wat': (8,),
    'Voorvallen en afwijkingen': (25,),
    'MoveMonitor instellen': (13,),
    'Meetwaarden gaan\nniet naar de\ncontrolegroep': (9,),
    'Van pilot tot laatste patiënt': (20,),
    "Vier risico's, en wat we eraan doen": (9, 13),
    'Vier toezeggingen': (20,),
    '144 patiënten, 24 per centrum': (20,),
    'PARADISE toetst geen werkzaamheid.\nPARADISE toetst overdracht.': (9, 10, 12),
    'Negen bij dertien millimeter.\nMeer merkt de patiënt niet.': (18,),
}


def regel(nummers, label='Bron'):
    """De korte verwijzing linksonder op de dia: 'Bron 9 · Bus 2013, DIAFOS'."""
    if not nummers:
        return ''
    delen = ['%d · %s' % (n, REF[n][0]) for n in nummers]
    return '%s  %s' % (label, '   |   '.join(delen))


def beknopt(citaat):
    """De citatie ingekort tot wat op een dia leesbaar blijft.

    'Armstrong DG, Boulton AJM, Bus SA. Diabetic foot ulcers and their
    recurrence. N Engl J Med. 2017;376(24):2367–75.' wordt 'Armstrong DG et al.
    N Engl J Med. 2017;376(24):2367–75.' — de volledige auteurslijst en de titel
    horen in het manuscript, niet op het scherm.

    De splitsing werkt omdat initialen zonder punt geschreven worden, zodat het
    eerste '. ' altijd het einde van de auteurslijst is. Klopt dat niet, dan
    blijft de volledige citatie staan.
    """
    delen = citaat.split('. ')
    if len(delen) < 3:
        return citaat
    auteurs = delen[0]
    eerste = auteurs.split(',')[0].strip()
    meer = ' et al.' if ',' in auteurs else '.'
    return '%s%s %s' % (eerste, meer, '. '.join(delen[2:]))


def lijst(nummers, kort=True):
    """De citaties voor de referentiedia, op nummer gesorteerd."""
    return [(n, beknopt(REF[n][1]) if kort else REF[n][1])
            for n in sorted(set(nummers))]
