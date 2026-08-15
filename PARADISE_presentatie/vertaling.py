# -*- coding: utf-8 -*-
"""Het congresdeck in het Engels, uit dezelfde bron.

De opzet: `inhoud.py` blijft in het Nederlands en blijft de enige plek waar de
structuur van een dia staat. Hier staat alleen een woordenboek Nederlands →
Engels. `vertaal()` loopt een diadefinitie recursief af en vervangt elke string
die in het woordenboek staat; alles wat er niet in staat blijft ongemoeid.

Dat laatste is met opzet. Kleurnamen, decklabels, toestelnamen en
eCRF-nummers hoeven niet vertaald te worden en staan er dus niet in. Wat er wél
in hoort maar ontbreekt, meldt de bouwer na het bouwen — dan ziet u meteen welke
zin nog Nederlands op het scherm zou komen.

Zelfde aanpak voor de spreektekst: `spreektekst.ZEG` gaat door dezelfde
vertaalslag heen.
"""

# Sleutels die nooit vertaald worden. Codes en namen spreken voor zich; `tip` en
# `interactie` blijven met opzet Nederlands, want die leest alleen de spreker.
NIET = {'t', 'voor', 'morph', 'kleur', 'kleur2', 'accent', 'vlak', 'foto',
        'fase', 'soort', 'schaal', 'mid', 'ox', 'nr', 'letter', 'bestand',
        'sleutel', 'kaart', 'uitklappen', 'bron', 'documenten', 'centra',
        'tip', 'interactie'}

ONVERTAALD = set()   # prozastrings zonder vertaling, gemeld na het bouwen


def _lijkt_tekst(s):
    """Een zin herkennen: meerdere woorden, en niet louter cijfers en tekens."""
    if len(s) < 5 or ' ' not in s.strip():
        return False
    return any(c.isalpha() for c in s)


def _str(s):
    if s in NL_EN:
        return NL_EN[s]
    if _lijkt_tekst(s):
        ONVERTAALD.add(s)
    return s


def vertaal(waarde, sleutel=None):
    """Vertaalt een dia, een lijst, een tuple of een losse string."""
    if sleutel in NIET:
        return waarde
    if isinstance(waarde, str):
        return _str(waarde)
    if isinstance(waarde, dict):
        return {k: vertaal(v, k) for k, v in waarde.items()}
    if isinstance(waarde, tuple):
        return tuple(vertaal(v) for v in waarde)
    if isinstance(waarde, list):
        return [vertaal(v) for v in waarde]
    return waarde


NL_EN = {

    # ------------------------------------------------------------- titeldia
    'Studieopzet · wetenschappelijke sessie': 'Trial design · scientific session',
    'Protocolversie 1.0 · 17 mei 2026 · S71769':
        'Protocol version 1.0 · 17 May 2026 · S71769',

    # ------------------------------------------------------- puntenraster
    'Waar we staan': 'Where we stand',
    '144 patiënten, 24 per centrum': '144 participants, 24 per centre',
    'Per centrum': 'Per centre',
    '24 deelnemers — 12 PARADISE en 12 gebruikelijke zorg':
        '24 participants — 12 PARADISE and 12 usual care',
    'Controlegroep': 'Control arm',
    'Gebruikelijke zorg, onveranderd': 'Usual care, unchanged',
    'Co-primair': 'Co-primary',
    'Recidief op 18 maanden, draagtijd op 12':
        'Recurrence at 18 months, adherence at 12',
    'Positief': 'Positive',
    'Alleen als béíde eindpunten halen': 'Only if bóth endpoints are met',
    'De zes deelnemende voetklinieken': 'The six participating foot clinics',

    # ----------------------------------------------------------- de these
    'PARADISE toetst geen werkzaamheid.\nPARADISE toetst overdracht.':
        'PARADISE does not test efficacy.\nPARADISE tests translation.',
    'Elk onderdeel bestaat al. Geen enkel onderdeel werkte alleen.':
        'Every component already exists. No component worked on its own.',

    # ------------------------------------------------------------- blok 1
    'Waarom zo': 'Why this design',
    'Vier cijfers verklaren waarom er twee normen zijn.':
        'Four numbers explain why there are two targets, not one.',
    'krijgt binnen een jaar\neen nieuw ulcus':
        'develop a new ulcer\nwithin one year',
    'na vijf jaar': 'at five years',
    'hogere sterfte': 'higher mortality',
    'sterfte na amputatie': 'mortality after amputation',
    'Armstrong, Boulton & Bus · N Engl J Med 2017':
        'Armstrong, Boulton & Bus · N Engl J Med 2017',

    'Driekwart is te voorkomen.\nVeertig procent komt terug.':
        'Three quarters are preventable.\nForty per cent come back.',
    'Dat gat is waar deze studie over gaat.':
        'That gap is what this trial is about.',

    'Wat er al geprobeerd is': 'What has already been tried',
    'Drie strategieën, één patroon': 'Three strategies, one pattern',
    'Drukgestuurd schoeisel': 'Pressure-guided footwear',
    'De pivotale multicentrische trial haalde haar primaire eindpunt niet: '
    '38,8% tegenover 44,2% recidief. Het verschil zat bij wie de schoen dróég.':
        'The pivotal multicentre trial missed its primary endpoint: 38.8% '
        'versus 44.2% recurrence. The difference was in who actually wore the '
        'footwear.',
    'Patienteneducatie': 'Patient education',
    'In de IWGDF-review had losstaande educatie geen aantoonbaar preventief '
    'effect. Het mediane behandeleffect was negatief.':
        'In the IWGDF review, stand-alone education showed no demonstrable '
        'preventive effect. The median treatment effect was negative.',
    'mediaan −13,4%': 'median −13.4%',
    'Continue digitale feedback': 'Continuous digital feedback',
    'Een slimme inlegzool met realtime waarschuwingen verminderde recidief — '
    'opnieuw vooral bij wie het toestel bleef gebruiken.':
        'An intelligent insole with real-time alerts reduced recurrence — '
        'again mainly among those who kept using the device.',
    'Het patroon': 'The pattern',
    'Elk onderdeel adresseert een noodzakelijke voorwaarde. Geen enkel '
    'onderdeel adresseert een voldoende voorwaarde.':
        'Each component addresses a necessary condition. None addresses a '
        'sufficient one.',
    'Geen drie teleurstellingen maar één: telkens echt, telkens voorwaardelijk.':
        'Not three disappointments but one: the effect is real every time, and '
        'conditional every time.',

    'Dezelfde schoen, twee uitkomsten': 'The same shoe, two outcomes',
    'Waarom druk alléén niet volstaat': 'Why pressure alone is not enough',
    'Iedereen': 'Everyone',
    'intention-to-treat': 'intention-to-treat',
    'Gewone maatzool': 'Standard custom insole',
    'Drukgeoptimaliseerd': 'Pressure-optimised',
    'Geen verschil — p = 0,48': 'No difference — p = 0.48',
    'Wie hem droeg': 'Those who wore it',
    '≥ 80% van de stappen': '≥ 80% of steps',
    'Bijna gehalveerd — p = 0,045': 'Almost halved — p = 0.045',
    'Daarom meten we niet alleen druk, maar ook draagtijd.':
        'That is why we measure not only pressure, but wear time.',
    'Bus et al. · Diabetes Care 2013 · DIAFOS, 171 deelnemers':
        'Bus et al. · Diabetes Care 2013 · DIAFOS, 171 participants',

    'draagtijd — gemeten,\nniet gevraagd': 'adherence — measured,\nnot asked',
    'thuis': 'at home',
    'stappen binnen': 'steps indoors',
    'stappen buiten': 'steps outdoors',
    'Draagtijd tegenover de norm van 80%': 'Adherence against the 80% target',
    'Gemiddeld': 'Overall',
    'Thuis': 'At home',
    'Buitenshuis': 'Outdoors',
    'Waaijman et al. · Diabetes Care 2013 · 107 patiënten':
        'Waaijman et al. · Diabetes Care 2013 · 107 patients',

    'Het mechanisme': 'The mechanism',
    'Belasting is een product,\ngeen optelsom':
        'Loading is a product,\nnot a sum',
    'Piekdruk': 'Peak pressure',
    'per stap': 'per step',
    'Bijgestuurd': 'Modified',
    'Activiteit': 'Activity',
    'stappen per dag': 'steps per day',
    'Gemeten': 'Measured',
    'Draagtijd': 'Wear time',
    'wérd hij gedragen': 'was it worn',
    'Eén factor op nul maakt het product nul. Daarom heeft PARADISE twee '
    'normen: een druknorm én een draagtijdnorm.':
        'One factor at zero makes the whole product zero. That is why PARADISE '
        'has two targets: one for pressure and one for wear time.',

    'Waarom deze studie nu pas kan': 'Why this trial is possible only now',
    'Drie dingen zijn veranderd': 'Three things have changed',
    'Therapietrouw is meetbaar': 'Adherence is measurable',
    'De temperatuursensor in orthopedisch schoeisel is gevalideerd. '
    'Zelfrapportage overschat systematisch; nu is draagtijd een toetsbaar doel '
    'in plaats van een aanname.':
        'The temperature sensor in orthopaedic footwear has been validated. '
        'Self-report systematically overestimates; wear time is now a testable '
        'target rather than an assumption.',
    'sensor': 'sensor',
    'De mislukking is verklaarbaar': 'The failure is explicable',
    'Kennisoverdracht raakt onder COM-B enkel capability. Opportunity en '
    'motivation — wat thuis gebeurt, jarenlang, ongezien — bleven onaangeroerd.':
        'Under COM-B, knowledge transfer addresses capability alone. '
        'Opportunity and motivation — what happens at home, for years, unseen — '
        'were left untouched.',
    'De context bestaat': 'The setting exists',
    'België erkent multidisciplinaire voetklinieken met opleidingseisen en '
    'minimumvolumes. Dat is de plek waar preventie uiteindelijk moet landen.':
        'Belgium accredits multidisciplinary foot clinics with training '
        'requirements and minimum caseloads. That is where prevention '
        'ultimately has to land.',
    'RIZIV-INAMI': 'RIZIV-INAMI',
    'Daarom is therapietrouw hier een co-primair eindpunt, en geen mediator '
    'die je achteraf afleidt.':
        'That is why adherence here is a co-primary endpoint, not a mediator '
        'inferred after the fact.',

    'Wat PARADISE anders doet': 'What PARADISE does differently',
    'Eén dienst, geen drie losse maatregelen':
        'One service, not three separate measures',
    'De zool háált de norm': 'The insole méets the target',
    '< 200 kPa óf 25% lager': '< 200 kPa ór 25% lower',
    'Gemeten bij de aflevering, in drie condities.':
        'Measured at delivery, in three conditions.',
    "Aangepast tot de norm gehaald is in elk van de drie doelregio's.":
        'Modified until the target is met in each of the three target regions.',
    'Herhaald op maand 6, 12 en 18.': 'Repeated at months 6, 12 and 18.',
    'En hij wórdt gedragen': 'And it ís worn',
    '80% van zijn eigen activiteitenprofiel':
        '80% of the participant’s own activity profile',
    'Een sensor in de zool meet de draagtijd, continu.':
        'A sensor in the insole records wear time continuously.',
    'Elke drie maanden uitgelezen en samen bekeken.':
        'Read out every three months and reviewed together.',
    'Vijf gesprekken die op die data staan, niet op goede raad.':
        'Five conversations built on that data, not on good advice.',

    # ------------------------------------------------------------- blok 2
    'De meting': 'The measurement',
    'Wat u meet, hoe u het meet, en wanneer het goed genoeg is.':
        'What is measured, how, and when it is good enough.',
    'Baseline · blootsvoets': 'Baseline · barefoot',
    'Elke sensor een cijfer': 'Every sensor a number',
    'piekdruk op metatarsaal 2-3': 'peak pressure at metatarsal 2-3',
    'Norm:': 'Target:',
    'óf': 'or',
    '≥ 25% lager': '≥ 25% lower',
    'Baseline meet u blootsvoets: de sensoren gaan met dubbelzijdige tape '
    'rechtstreeks op de voet, daarover een standaardkous.':
        'Baseline is measured barefoot: sensors are taped directly to the foot '
        'with double-sided tape, with a standardised sock over them.',
    'Drie metingen per voet, links en rechts apart. Daaruit berekent de '
    'software één gemiddeld piekdrukbeeld.':
        'Three measurements per foot, left and right separately, from which '
        'the software derives one averaged peak-pressure map.',
    'eCRF-document 09 · Meting plantaire druk, baseline':
        'eCRF document 09 · Plantar pressure measurement, baseline',

    'Inzoomen op de voorvoet': 'Zooming in on the forefoot',
    "Acht regio's, drie doelregio's": 'Eight regions, three target regions',
    'Metatarsaal 1': 'Metatarsal 1',
    'onder de grote teen — tweede meest getroffen plek':
        'under the great toe — second most affected site',
    'Metatarsaal 2-3': 'Metatarsal 2-3',
    'de hete plek op deze meting, en de klassieke ulcusplek':
        'the hot spot in this measurement, and the classic ulcer site',
    'Metatarsaal 4-5': 'Metatarsal 4-5',
    'laterale voorvoet, meestal lagere druk':
        'lateral forefoot, usually lower pressure',
    'Hallux': 'Hallux',
    'apart bekeken, niet meer samengeteld met de tenen':
        'scored separately, no longer combined with the lesser toes',
    'Tenen 2-5': 'Toes 2-5',
    'eigen regio sinds de laatste maskerversie':
        'a region of its own since the latest mask version',

    'Na optimalisatie': 'After optimisation',
    'Wanneer is het goed genoeg': 'When is it good enough',
    'piekdruk in de doelregio na aanpassing':
        'peak pressure in the target region after modification',
    '40% lager': '40% lower',
    'onder 200 kPa': 'below 200 kPa',
    'beide criteria gehaald': 'both criteria met',
    'De norm geldt per doelregio: piekdruk onder 200 kPa óf minstens 25% lager '
    'dan de baselinemeting van diezelfde regio.':
        'The target applies per region: peak pressure below 200 kPa or at '
        'least 25% lower than the baseline value for that same region.',
    'Haalt u de norm niet, dan past u aan en meet u opnieuw. Het formulier '
    'voorziet twee extra ontlastingstests.':
        'If the target is not met, modify and measure again. The form provides '
        'for two further offloading attempts.',
    'eCRF-document 24 · Meting drukherverdeling voetorthese':
        'eCRF document 24 · Pressure redistribution of the orthosis',

    'Niet minder belasting.\nBelasting op een plek die het aankan.':
        'Not less loading.\nLoading where the tissue can take it.',
    'Dat is de hele interventie.': 'That is the entire intervention.',

    'Het meetprotocol': 'The measurement protocol',
    'Drie condities bij de aflevering': 'Three conditions at delivery',
    'Blootsvoets': 'Barefoot',
    'Sensoren met dubbelzijdige tape op de voet, standaardkous erover. Dit is '
    'het referentiebeeld.':
        'Sensors taped to the foot, standardised sock over them. This is the '
        'reference map.',
    'In de schoen, zónder de zool': 'In the shoe, wíthout the insole',
    'Toont wat het schoeisel alleen doet. Dit is de vergelijking die de laat '
    'zien of de zool iets toevoegt.':
        'Shows what the footwear does on its own. This is the comparison that '
        'reveals whether the insole adds anything.',
    'In de schoen, mét de zool': 'In the shoe, wíth the insole',
    'De meting waarop de norm getoetst wordt, per doelregio.':
        'The measurement against which the target is tested, per region.',
    'Alle drie de condities staan op hetzelfde formulier. Slaat u er één over, '
    'dan is de vergelijking onbruikbaar.':
        'All three conditions are on the same form. Skip one and the '
        'comparison is unusable.',
    'eCRF-document 24 · de norm wordt per doelregio getoetst, niet over de hele voet':
        'eCRF document 24 · the target is tested per region, not across the '
        'whole foot',

    # ------------------------------------------------------------- blok 3
    'Het traject': 'The pathway',
    'Negen contactmomenten. Per moment: wat u doet en wat u invult.':
        'Nine contacts. For each: what is done and what is recorded.',
    'Screening plus negen visites': 'Screening plus nine visits',
    'maanden, van screening tot afronding':
        'months, from screening to completion',
    'Visite 0 tot 2 liggen dicht op elkaar: toestemming, baseline, en de zool '
    'binnen de maand. Daarna is het ritme elke drie maanden, hetzelfde ritme '
    'als de controle die deze patiënten al krijgen.':
        'Visits 0 to 2 fall close together: consent, baseline, and the insole '
        'within the month. After that the rhythm is three-monthly — the same '
        'rhythm as the review these patients already receive.',
    'meetmoment': 'measurement',
    'begeleiding': 'behavioural support',
    'start en afronding': 'start and completion',

    'Screening': 'Screening',
    'Wie komt in aanmerking': 'Who is eligible',
    'wél': 'in',
    'niet': 'out',
    'Volwassen, begrijpt Nederlands': 'Adult, understands Dutch',
    'Diabetes type 1 of 2': 'Diabetes type 1 or 2',
    'Risicocategorie 3 volgens IWGDF: genezen plantair ulcus, partiële '
    'amputatie of resectie van een metatarsaalkop — niet de eerste — tussen 18 '
    'maanden en 2 weken geleden':
        'IWGDF risk category 3: healed plantar ulcer, or partial amputation or '
        'resection of a metatarsal head — not the first — between 18 months '
        'and 2 weeks ago',
    'Stapt zelfstandig blootsvoets, zonder hulpmiddelen':
        'Walks barefoot independently, without walking aids',
    'Heeft beschermend schoeisel, of aanvaardt het: volledig maatwerk, of '
    'maatzolen in semi-orthopedisch of extra-diep confectieschoeisel':
        'Has protective footwear, or accepts it: fully custom-made, or custom '
        'insoles in semi-orthopaedic or extra-depth off-the-shelf footwear',
    'Amputatie proximaal van de MTP-gewrichten':
        'Amputation proximal to the MTP joints',
    'Actief ulcus of Charcot-deformiteit':
        'Active ulcer or Charcot deformity',
    'Kritische ischemie — PEDIS graad 3': 'Critical ischaemia — PEDIS grade 3',
    'Immunosuppressieve therapie': 'Immunosuppressive therapy',
    'Nierfunctievervangende therapie': 'Renal replacement therapy',
    'Overleving < 18 maanden, beoordeeld door de arts':
        'Survival < 18 months, in the judgement of the treating physician',
    'Kan geen toestemming geven of instructies volgen':
        'Unable to consent or to follow instructions',
    'Hulpmiddel dat druksensoren belemmert, bv. een EVO':
        'A device preventing sensor application, e.g. an ankle-foot orthosis',
    'Weigert het voorgeschreven schoeisel te dragen':
        'Declines the prescribed footwear',

    'Terug naar het geheel': 'Back to the whole',
    'contactmomenten, één zorgpad': 'contacts, one care pathway',
    'Het verschil met vandaag zit niet in hoe vaak u de patiënt ziet, maar in '
    'wat u bij elk bezoek wéét: wat de zool doet en wat er gedragen is.':
        'The difference from today is not how often the patient is seen, but '
        'what is known at each visit: what the insole does, and what was '
        'actually worn.',

    # ------------------------------------------------------------ toestellen
    'De techniek': 'The technology',
    'Drie toestellen': 'Three devices',
    'Novel pedar': 'Novel pedar',
    'druk': 'pressure',
    '8 voetregio’s': '8 foot regions',
    'uw team meet': 'your team measures',
    'Blootsvoets met tape, en in de schoen met en zonder zool':
        'Barefoot with tape, and in the shoe with and without the insole',
    'Trublu-kalibratie minstens elke drie maanden':
        'Trublu calibration at least every three months',
    'De F-Scan GO is een aparte meting van het studieteam':
        'F-Scan GO: a separate study-team measurement',
    'Orthotimer': 'Orthotimer',
    'draagtijd': 'wear time',
    '15  minuten': '15  minutes',
    'In de zool, 9 × 13 × 4,5 mm': 'In the insole, 9 × 13 × 4.5 mm',
    'Batterij 100 dagen': 'Battery 100 days',
    'meet: uw sensor': 'call it: your sensor',
    'MoveMonitor': 'MoveMonitor',
    'activiteit': 'activity',
    '7  dagen': '7  days',
    'Om het middel, op de onderrug': 'At the waist, on the lower back',
    'Baseline en 6 maanden': 'Baseline and 6 months',
    'zet de norm per patiënt': 'sets the target per patient',

    'SEBIA · eCRF-document 17': 'SEBIA · eCRF document 17',
    'Vijf gespreksmomenten': 'Five conversations',
    'Baseline': 'Baseline',
    'Vragenlijsten eerst, dan educatie op maat, met voordoen.':
        'Questionnaires first, then tailored education, with demonstration.',
    '3 mnd': '3 mo',
    'Teach-back. Nadruk op binnenshuis dragen.':
        'Teach-back, with emphasis on indoor wear.',
    '6 · 12 mnd': '6 · 12 mo',
    'Zelfinschatting, dan samen de data bekijken.':
        'Self-assessment, then reviewing the data together.',
    '9 · 15 mnd': '9 · 15 mo',
    'Voordoen. Uitdraai vergelijken met vorige keer.':
        'Demonstration, comparing the printout with the previous visit.',
    '18 mnd': '18 mo',
    'Afsluiten en resultaten delen.': 'Closing, and sharing the results.',

    'De enige regel die u écht moet onthouden':
        'The one rule that really matters',
    'Meetwaarden gaan\nniet naar de\ncontrolegroep':
        'Measured values do\nnot go to the\ncontrol arm',
    'Ook zij krijgen een drukmeting en dragen een sensor — anders kunnen we de '
    'groepen niet vergelijken. Maar die getallen blijven dicht. Bespreekt u ze, '
    'dan lévert u de interventie en is die patiënt niet meer bruikbaar als '
    'controle.':
        'They too undergo pressure measurement and wear a sensor — otherwise '
        'the arms cannot be compared. But those numbers stay closed. Discuss '
        'them and you have delivered the intervention, and that participant is '
        'no longer usable as a control.',
    'Uitzondering': 'Exception',
    'Klinische bevindingen zijn géén meetwaarden. Elke laesie of huiddefect '
    'meldt en behandelt u meteen. In beide groepen.':
        'Clinical findings are not measured values. Any lesion or skin defect '
        'is reported and treated immediately. In both arms.',

    # ------------------------------------------------ blok 4, eindpunten
    'Eindpunten en analyse': 'Endpoints and analysis',
    'Twee eindpunten, één op één op het causale model.':
        'Two endpoints, mapped one to one onto the causal model.',

    'Steekproefberekening': 'Sample size',
    'Twee eindpunten, twee berekeningen': 'Two endpoints, two calculations',
    'Co-primair 1': 'Co-primary 1',
    'Ulcusrecidief op 18 maanden': 'Ulcer recurrence at 18 months',
    'Aanname controle': 'Assumed, control',
    '50% recidief': '50% recurrence',
    'Aanname interventie': 'Assumed, intervention',
    '25%, hazard ratio 0,42': '25%, hazard ratio 0.42',
    'Toets': 'Test',
    'log-rank, tweezijdig, α = 0,05': 'log-rank, two-sided, α = 0.05',
    'Power': 'Power',
    '80% → 41 events nodig': '80% → 41 events required',
    'Uitval': 'Attrition',
    '15%': '15%',
    '108 → 127 met uitval → 130 gestratificeerd':
        '108 → 127 with attrition → 130 stratified',
    'Co-primair 2': 'Co-primary 2',
    'Therapietrouw op 12 maanden': 'Footwear adherence at 12 months',
    '71%, SD 25%': '71%, SD 25%',
    '85%, effectgrootte 0,56': '85%, effect size 0.56',
    't-toets, tweezijdig, α = 0,05': 't-test, two-sided, α = 0.05',
    '80% → 50 per groep': '80% → 50 per group',
    '100 → 118 met uitval': '100 → 118 with attrition',
    'Zes centra maal 24 is 144. Dat cijfer komt niet uit de berekening maar '
    'uit de rekruteringscapaciteit per centrum, en het overtreft beide minima.':
        'Six centres times 24 is 144. That figure comes from per-centre '
        'recruitment capacity rather than from the calculation, and it exceeds '
        'both minima.',
    'Waarom dan 144': 'So why 144',
    'Manuscript, steekproefberekening · exponentieel verdeelde tijden tot '
    'recidief aangenomen':
        'Manuscript, sample size · exponentially distributed times to '
        'recurrence assumed',

    'Wat het co-primaire criterium kost': 'What the co-primary criterion costs',
    'De power die telt, is de gezamenlijke': 'The power that counts is the joint one',
    'De studie is pas positief als béíde eindpunten significant zijn.':
        'The trial is positive only if bóth endpoints reach significance.',
    'Recidief apart': 'Recurrence alone',
    '84% — en 90% bij volledige opvolging':
        '84% — and 90% with complete follow-up',
    'Therapietrouw apart': 'Adherence alone',
    '87% — en 92% bij volledige opvolging':
        '87% — and 92% with complete follow-up',
    'Beide samen': 'Both together',
    '74% tot 84%, naargelang de correlatie':
        '74% to 84%, depending on the correlation',
    'Bij een half zo groot effect': 'At half the effect size',
    '64% bij 30% · 40% bij 35%': '64% at 30% · 40% at 35%',
    'Protocollen met co-primaire eindpunten rapporteren doorgaans alleen het '
    'cijfer per eindpunt. Dat overschat de kans op het criterium waarop de '
    'studie werkelijk beoordeeld wordt.':
        'Protocols with co-primary endpoints usually report only the '
        'endpoint-specific figure. That overstates the prospect on the '
        'criterion by which the trial will actually be judged.',

    'Analyseplan': 'Analysis plan',
    'Hoe we het toetsen': 'How we test it',
    'Recidief': 'Recurrence',
    'Cox-regressie gestratificeerd naar centrum, met de toewijzing als enige '
    'covariaat. Sterfte is een competing risk, geen censuur: Fine-Gray en '
    'cumulatieve incidentie ernaast.':
        'Cox regression stratified by centre, with allocation as the only '
        'covariate. Death is a competing risk, not censoring: Fine-Gray and '
        'cumulative incidence alongside.',
    'co-primair': 'co-primary',
    'Therapietrouw': 'Adherence',
    'Beta-regressie met logit-link, want het is een proportie met een plafond. '
    'Lineaire regressie als gevoeligheidsanalyse.':
        'Beta regression with a logit link, since it is a proportion with a '
        'ceiling. Linear regression as a sensitivity analysis.',
    'Intercurrente events': 'Intercurrent events',
    'De twee eindpunten zijn elkaars intercurrente event: wie ulcereert draagt '
    'terecht geen zool meer. Hypothetische strategie voor therapietrouw.':
        'The two endpoints are intercurrent events for one another: a '
        'participant who ulcerates rightly stops wearing the insole. '
        'Hypothetical strategy for adherence.',
    'estimand': 'estimand',
    'Ontbrekende data': 'Missing data',
    'Multipele imputatie, 50 datasets. Een tipping-pointanalyse toont hoe '
    'extreem het moet worden om de conclusie te kantelen.':
        'Multiple imputation, 50 datasets. A tipping-point analysis shows how '
        'extreme a departure would have to be to overturn the conclusion.',
    'Positief alleen als beide eindpunten significant zijn. Daarom blijft de '
    'familiegewijze fout onder 0,05 en is geen correctie nodig.':
        'Positive only if both endpoints are significant. The family-wise error '
        'rate therefore stays below 0.05 and no adjustment is applied.',

    'Wat er naast de trial loopt': 'What runs alongside the trial',
    'Twee evaluaties, parallel': 'Two evaluations, in parallel',
    'Gezondheidseconomische evaluatie': 'Health-economic evaluation',
    'Kosten-utiliteit, betalersperspectief': 'Cost-utility, payer perspective',
    'EQ-5D-5L elke drie maanden, gewaardeerd met de Belgische waardeset.':
        'EQ-5D-5L every three months, valued with the Belgian value set.',
    'Zorggebruik prospectief met iMCQ en iPCQ, plus dagboek en dossier.':
        'Resource use collected prospectively with the iMCQ and iPCQ, plus '
        'diary and medical records.',
    'Markov tot vijf jaar. Kosten per vermeden ulcus én per QALY, naast elkaar.':
        'Markov extrapolation to five years. Cost per ulcer prevented and cost '
        'per QALY, reported side by side.',
    'Procesevaluatie': 'Process evaluation',
    'MRC-kader, drie domeinen': 'MRC framework, three domains',
    'Implementatie: fideliteit, dosis, bereik, aanpassingen.':
        'Implementation: fidelity, dose, reach, adaptations.',
    'Mechanismen en context: wat de uitvoering per centrum bepaalt.':
        'Mechanisms and context: what governs delivery at each centre.',
    'Interviews, gestructureerde observatie en therapeutendagboeken.':
        'Interviews, structured observation and therapist diaries.',

    'Wat we hoe dan ook leren': 'What we learn either way',
    'Een nulresultaat is ook een resultaat': 'A null result is also a result',
    'Therapietrouw stijgt, recidief niet': 'Adherence rises, recurrence does not',
    'Dan faalt de biomechanische premisse: geoptimaliseerd schoeisel drágen '
    'volstaat niet. Het veld moet stoppen preventiefalen aan de patiënt toe te '
    'schrijven.':
        'Then the biomechanical premise fails: wearing optimised footwear is '
        'not enough. The field should stop attributing prevention failures to '
        'patient behaviour.',
    'Therapietrouw stijgt niet': 'Adherence does not rise',
    'Dan faalde de gedragscomponent. De fideliteitsdata zeggen of het ontwerp '
    'tekortschoot of de uitvoering.':
        'Then the behavioural component failed. The fidelity data distinguish '
        'inadequate design from inadequate delivery.',
    'Beide stijgen': 'Both rise',
    'Dan werkt een geïntegreerde dienst onder routineomstandigheden — zonder '
    'dat we weten welk onderdeel het deed. Ontleden vraagt een factoriële '
    'opzet die het Belgische netwerk niet kan leveren.':
        'Then an integrated service works under routine conditions — without '
        'our knowing which component did it. Decomposition would require a '
        'factorial design the Belgian network cannot supply.',
    'Hoe dan ook': 'Either way',
    'Druk, activiteit en draagtijd worden bij 144 deelnemers over achttien '
    'maanden gelijktijdig gemeten. Dat is de eerste dataset van die omvang, '
    'ongeacht de uitkomst.':
        'Pressure, activity and wear time are recorded concurrently in 144 '
        'participants over eighteen months. That is the first dataset of that '
        'size, whatever the result.',

    # ------------------------------------------------------------- contact
    'Wie u aanspreekt': 'Who to contact',
    'Voor als er iets misloopt': 'If something goes wrong',
    'Doctoraatsonderzoeker · dagelijkse opvolging':
        'Doctoral researcher · day-to-day conduct',
    'Uw eerste aanspreekpunt: inclusies, metingen, formulieren, sensoren en '
    'alles wat u in de praktijk vastloopt.':
        'Your first point of contact: inclusions, measurements, forms, sensors '
        'and anything that gets stuck in practice.',
    'Promotor': 'Principal investigator',
    'Wetenschappelijke vragen, de opzet van de studie en afspraken op het '
    'niveau van uw centrum.':
        'Scientific questions, trial design, and arrangements at the level of '
        'your centre.',
    'Revalidatiewetenschappen': 'Rehabilitation Sciences',
    'KU Leuven · Campus Brugge': 'KU Leuven · Bruges Campus',
    'PARADISE · FWO TBM T000226N · S71769':
        'PARADISE · FWO TBM T000226N · S71769',
    'Spoorwegstraat 12 · Brugge': 'Spoorwegstraat 12 · Bruges',
    'Janou De Buyser': 'Janou De Buyser',
    'prof. dr. Kevin Deschamps': 'Prof. Dr Kevin Deschamps',
    'Consortium: KU Leuven — Revalidatiewetenschappen (Musculoskeletal Research '
    'Group) en Volksgezondheid en Eerstelijnszorg · Vrije Universiteit Brussel '
    '— Geneeskunde en Farmacie. Co-promotoren: Fabienne Dobbels, Maaike Fobelets '
    'en Koen Putman.':
        'Consortium: KU Leuven — Rehabilitation Sciences (Musculoskeletal '
        'Research Group) and Public Health and Primary Care · Vrije '
        'Universiteit Brussel — Medicine and Pharmacy. Co-promotors: Fabienne '
        'Dobbels, Maaike Fobelets and Koen Putman.',

    # -------------------------------------- tijdlijnlabels en losse opmaak
    'Elke stip is een patiënt die u zelf includeert.\n24 per kliniek.':
        'Every dot is a participant your clinic includes.\n24 per centre.',
    'norm 80%': '80% target',
    'Uitzondering': 'Exception',
    'Gevolg': 'Consequence',
    'geschiktheid': 'eligibility',
    'loting': 'allocation',
    'baseline': 'baseline',
    'zool + sensor': 'insole + sensor',
    'opvolging': 'follow-up',
    'meting': 'measure',
    'meting + einde': 'measure + end',
    'meetmoment': 'measurement',
    'begeleiding': 'behavioural support',
    'start en afronding': 'start and completion',
    'minuten': 'minutes',
    'dagen': 'days',
    "voetregio's": 'foot regions',
    'Druk': 'Pressure',
    'Uw eerste aanspreekpunt: inclusies, metingen, formulieren, sensoren en '
    'alles wat in de praktijk vastloopt.':
        'Your first point of contact: inclusions, measurements, forms, sensors '
        'and anything that gets stuck in practice.',

    # ----------------------------------------- losse labels op de meetdia's
    'Norm:  < 200 kPa   óf   ≥ 25% lager':
        'Target:  < 200 kPa   or   ≥ 25% lower',
    '40% lager  ·  onder 200 kPa  ·  beide criteria gehaald':
        '40% lower  ·  below 200 kPa  ·  both criteria met',
    "Acht regio's via Multimask · hiel en mediale en laterale middenvoet vallen "
    'buiten beeld':
        'Eight regions via Multimask · heel and medial and lateral midfoot fall '
        'outside the frame',
    'Risicocategorie 3 met genezen plantair ulcus, partiële amputatie of '
    'resectie van een metatarsaalkop — niet de eerste — tussen 18 maanden en 2 '
    'weken geleden':
        'IWGDF risk category 3 with a healed plantar ulcer, or partial '
        'amputation or resection of a metatarsal head — not the first — between '
        '18 months and 2 weeks ago',
    'Toont wat het schoeisel alleen doet. Dit is de vergelijking die laat zien '
    'of de zool iets toevoegt.':
        'Shows what the footwear does on its own. This is the comparison that '
        'reveals whether the insole adds anything.',
    'Teach-back. Nadruk op bínnenshuis dragen.':
        'Teach-back, with the emphasis on índoor wear.',
    'Uw team meet': 'Your team measures',
    'Zet de norm per patiënt': 'Sets the target per patient',
    'Heet: uw sensor': 'Call it: your sensor',
    'p = 0,48': 'p = 0.48',
    'proof of concept': 'proof of concept',

    # ---------------------------------------------------------------------
    # De spreektekst. Zelfde huisregels als in spreektekst.py: vier zinnen,
    # de eerste is de bewering, de laatste is de brug.
    # ---------------------------------------------------------------------
    'PARADISE gaat niet over genezen maar over terugkomen. Zes Belgische '
    'voetklinieken, honderdvierenveertig patiënten, achttien maanden per '
    'patiënt. Ik neem u mee langs het waarom, de meting en het traject. '
    'Onderbreek me gerust.':
        'PARADISE is not about healing. It is about coming back. Six Belgian '
        'foot clinics, one hundred and forty-four participants, eighteen '
        'months each. I will take you through the rationale, the measurement '
        'and the pathway.',

    'Elke stip is een patiënt. Vierentwintig daarvan komen uit úw kliniek, '
    'twaalf in elke arm. Zes keer vierentwintig is honderdvierenveertig. '
    'Blijft één centrum achter, dan haalt de studie het niet.':
        'Every dot is a participant. Twenty-four come from each clinic, twelve '
        'in each arm. Six times twenty-four is one hundred and forty-four. If '
        'one centre falls behind, the trial does not get there.',

    'Eén zin, en dan ga ik door. Elk onderdeel van PARADISE bestaat al. Geen '
    'enkel onderdeel werkte alleen. Wat wij toetsen is of ze samen wél werken, '
    'in gewone klinieken en onder gewone caseload.':
        'One sentence, then I move on. Every component of PARADISE already '
        'exists. Not one of them worked on its own. What we test is whether '
        'they work together, in ordinary clinics under ordinary caseloads.',

    'Blok één. Ik geef u vier cijfers. Na het vierde weet u waarom deze studie '
    'twee normen heeft in plaats van één, en waarom niemand die tot nu toe '
    'samen gehaald heeft.':
        'Chapter one. I will give you four numbers. After the fourth you will '
        'know why this trial has two targets rather than one, and why nobody '
        'has met both at once.',

    'Veertig procent krijgt binnen één jaar een nieuw ulcus. Na vijf jaar is '
    'dat vijfenzestig. En de sterfte ligt tweeënhalf keer hoger dan bij '
    'diabetes zonder ulcus — na een amputatie zelfs boven de zeventig procent. '
    'Dit is geen wondprobleem. Dit is een overlevingsprobleem.':
        'Forty per cent develop a new ulcer within one year. At five years it '
        'is sixty-five. Mortality is two and a half times that of diabetes '
        'without ulceration, and after amputation it exceeds seventy per cent. '
        'This is not a wound problem. It is a survival problem.',

    'En dan het cijfer dat het onverdraaglijk maakt. Driekwart van deze ulcera '
    'is in principe te voorkomen. Toch komt veertig procent binnen het jaar '
    'terug. Dat gat tussen wat kan en wat gebeurt — daar gaat deze studie over.':
        'And then the number that makes it intolerable. Three quarters of '
        'these ulcers are preventable in principle. Yet forty per cent return '
        'within the year. That gap, between what is possible and what happens, '
        'is what this trial is about.',

    'Het is niet zo dat niemand het geprobeerd heeft. Drukgestuurd schoeisel '
    'haalde zijn eindpunt niet. Educatie alleen had zelfs een negatief mediaan '
    'effect. Digitale feedback werkte, maar opnieuw alleen bij wie het toestel '
    'bleef gebruiken.':
        'It is not that nobody has tried. Pressure-guided footwear missed its '
        'endpoint. Education alone had a negative median effect. Digital '
        'feedback worked, but again only among those who kept using the '
        'device.',

    'Dit is de beste poging die er ligt: drukgeoptimaliseerd maatschoeisel, '
    'multicentrisch en gerandomiseerd. Over iedereen samen: geen verschil. Bij '
    'wie hem dróég: bijna gehalveerd. Het verschil zat dus niet in de schoen.':
        'This is the best attempt on record: pressure-optimised custom '
        'footwear, multicentre and randomised. Across everyone: no difference. '
        'Among those who wore it: almost halved. The difference was not in the '
        'shoe.',

    'Daar zit het. Eenenzeventig procent draagtijd, gemeten met een sensor en '
    'niet gevraagd. Thuis zakt het naar eenenzestig, en juist thuis worden de '
    'meeste stappen gezet. De schoen stond in de gang terwijl de patiënt door '
    'het huis liep.':
        'There it is. Seventy-one per cent adherence, measured by sensor and '
        'not asked for. At home it falls to sixty-one, and home is where most '
        'steps are taken. The footwear sat in the hallway while the patient '
        'walked through the house.',

    'Belasting is een product, geen optelsom. Piekdruk maal activiteit maal '
    'draagtijd. Eén factor op nul maakt het hele product nul. Een perfecte zool '
    'in de kast beschermt niets.':
        'Loading is a product, not a sum. Peak pressure times activity times '
        'wear time. One factor at zero makes the whole product zero. A perfect '
        'insole in the cupboard protects nothing.',

    'Waarom kan deze studie nu pas? Drie dingen zijn veranderd. De sensor maakt '
    'therapietrouw meetbaar, COM-B verklaart waaróm educatie faalde, en België '
    'heeft erkende voetklinieken met opleidingseisen. De onderdelen liggen er '
    'dus klaar.':
        'Why is this trial possible only now? Three things have changed. The '
        'sensor makes adherence measurable, COM-B explains why education '
        'failed, and Belgium has accredited foot clinics with training '
        'requirements. The components are on the table.',

    'Daarom doen wij het anders. Geen drie losse maatregelen, maar één dienst '
    'met twee normen: de zool moet de druk hálen, én hij moet gedragen wórden. '
    'Beide gemeten, beide bijgestuurd, en beide door uw eigen team. Dat is nog '
    'nooit samen getoetst.':
        'So we do it differently. Not three separate measures, but one service '
        'with two targets: the insole must méet the pressure target, and it '
        'must be wórn. Both measured, both corrected, both by the clinic’s own '
        'team. That has never been tested together.',

    'Blok twee: de meting. Wat u meet, hoe u het meet, en wanneer het goed '
    'genoeg is.':
        'Chapter two: the measurement. What is measured, how, and when it is '
        'good enough.',

    'Elke sensor geeft een cijfer. Dit is de baseline, blootsvoets: '
    'driehonderdtwaalf kilopascal onder metatarsaal twee-drie. Drie metingen '
    'per voet, waar de software één beeld van maakt. Hiertegen wordt alles '
    'afgezet.':
        'Every sensor gives a number. This is baseline, barefoot: three '
        'hundred and twelve kilopascals under metatarsal two-three. Three '
        'measurements per foot, from which the software builds one map. '
        'Everything else is referenced against this.',

    "De software verdeelt de voet in acht regio's. Daarvan kiest u er drie als "
    'doelregio. Die drie zet u op het voorschrift. En alleen dáár wordt de norm '
    'getoetst, niet over de hele voet.':
        'The software divides the foot into eight regions. Three of them are '
        'designated target regions and written on the prescription. The target '
        'is tested there, and nowhere else.',

    'Zelfde voet, na aanpassing. Honderdzesentachtig kilopascal: veertig '
    'procent lager én onder de tweehonderd. De norm geldt per doelregio. Haalt '
    'u ze niet, dan past u aan en meet u opnieuw.':
        'Same foot, after modification. One hundred and eighty-six '
        'kilopascals: forty per cent lower and below two hundred. The target '
        'applies per region. If it is not met, you modify and measure again.',

    'Even stilstaan. Het doel is niet minder belasting. Het doel is belasting '
    'op een plek die het aankan. Dat is de hele interventie.':
        'A moment on this one. The aim is not less loading. The aim is loading '
        'where the tissue can take it. That is the entire intervention.',

    'Drie condities, altijd in deze volgorde. Blootsvoets is uw referentie. In '
    'de schoen zonder zool toont wat het schoeisel alleen doet. In de schoen '
    'mét zool is de meting waarop de norm getoetst wordt — slaat u er één over, '
    'dan is de vergelijking onbruikbaar.':
        'Three conditions, always in this order. Barefoot is the reference. In '
        'the shoe without the insole shows what the footwear does alone. In '
        'the shoe with the insole is the measurement the target is tested on. '
        'Skip one and the comparison is unusable.',

    'Blok drie: het traject. Negen contactmomenten. Per moment: wat u doet en '
    'wat u invult.':
        'Chapter three: the pathway. Nine contacts. For each one: what is done '
        'and what is recorded.',

    'Screening en negen visites over achttien maanden. De eerste drie liggen '
    'dicht op elkaar. Daarna is het ritme elke drie maanden — hetzelfde ritme '
    'als de controle die deze patiënten toch al krijgen.':
        'Screening and nine visits across eighteen months. The first three '
        'fall close together. After that the rhythm is three-monthly, the same '
        'rhythm as the review these patients already receive.',

    'Categorie drie volgens IWGDF: een genezen plantair ulcus, of een kleine '
    'amputatie. Links wat toelaat, rechts wat uitsluit. De rode draad: '
    'offloading moet de juiste behandeling zijn, dus kritieke ischemie en '
    'actieve Charcot vallen af.':
        'IWGDF risk category three: a healed plantar ulcer, or a minor '
        'amputation. On the left what admits, on the right what excludes. The '
        'logic throughout: offloading must be the appropriate treatment, so '
        'critical ischaemia and active Charcot are out.',

    'Tien contactmomenten, één zorgpad. Het verschil met vandaag zit niet in '
    'hoe vaak u de patiënt ziet, maar in wat u bij elk bezoek wéét: wat de zool '
    'doet, en wat er gedragen is.':
        'Ten contacts, one care pathway. The difference from today is not how '
        'often the patient is seen, but what is known at each visit: what the '
        'insole does, and what was actually worn.',

    'Drie toestellen, drie taken. De pedar meet druk, de Orthotimer meet of de '
    'zool gedragen is, de MoveMonitor meet hoeveel er gestapt wordt. Alleen de '
    'pedar bedient u bij elke meting; de andere twee plaatst u één keer en '
    'leest u uit.':
        'Three devices, three jobs. The pedar measures pressure, the '
        'Orthotimer records whether the insole was worn, the MoveMonitor '
        'records how much walking is done. Only the pedar is operated at every '
        'measurement; the other two are fitted once and read out.',

    'SEBIA is vijf gesprekken, geen enkele sessie. Eerst kennis en educatie, '
    'dan teach-back bij de aflevering, dan tweemaal de sensordata samen '
    'bekijken, dan voordoen, en op achttien maanden afsluiten. Het verschil met '
    'gewone educatie: het herhaalt, en het staat op data.':
        'SEBIA is five conversations, not one session. First knowledge and '
        'education, then teach-back at delivery, then two joint reviews of the '
        'sensor data, then demonstration, and closure at eighteen months. What '
        'separates it from conventional education: it repeats, and it stands '
        'on data.',

    'Dit is de enige regel die u écht moet onthouden. De controlegroep krijgt '
    'ook een meting en een sensor, maar die getallen blijven dicht. Bespreekt u '
    'ze, dan lévert u de interventie. Klinische bevindingen zijn géén '
    'meetwaarden: een laesie meldt en behandelt u meteen, in beide groepen.':
        'This is the one rule that really matters. The control arm is measured '
        'and wears a sensor too, but those numbers stay closed. Discuss them '
        'and you have delivered the intervention. Clinical findings are not '
        'measured values: a lesion is reported and treated immediately, in '
        'both arms.',

    'Blok vier: de eindpunten en de analyse. Twee eindpunten, één op één op het '
    'causale model.':
        'Chapter four: endpoints and analysis. Two endpoints, mapped one to '
        'one onto the causal model.',

    'Twee eindpunten betekent twee berekeningen. Links recidief: vijftig '
    'tegenover vijfentwintig procent, wat eenenveertig events vraagt en '
    'honderddertig deelnemers. Rechts therapietrouw: vijftig per groep. '
    'Honderdvierenveertig komt uit de capaciteit per centrum en overtreft beide '
    'minima.':
        'Two endpoints means two calculations. On the left, recurrence: fifty '
        'versus twenty-five per cent, requiring forty-one events and one '
        'hundred and thirty participants. On the right, adherence: fifty per '
        'group. One hundred and forty-four comes from per-centre capacity and '
        'exceeds both minima.',

    'En dan de vraag die u anders uit de zaal krijgt. Apart hebben we '
    'vierentachtig en zevenentachtig procent power. Maar de studie is pas '
    'positief als béíde eindpunten halen, en dan zakt het naar vierenzeventig '
    'tot vierentachtig. Wij rapporteren dat zelf, want de losse cijfers '
    'overschatten de kans.':
        'And now the question you would otherwise get from the floor. '
        'Separately we have eighty-four and eighty-seven per cent power. But '
        'the trial is positive only if both endpoints are met, and then it '
        'falls to between seventy-four and eighty-four. We report that '
        'ourselves, because the separate figures overstate the prospect.',

    'Het analyseplan in vier regels. Recidief met Cox, gestratificeerd naar '
    'centrum, met sterfte als competing risk. Therapietrouw met '
    'beta-regressie, want het is een proportie met een plafond. En de twee '
    'eindpunten zijn elkaars intercurrente event: wie ulcereert, draagt terecht '
    'geen zool meer.':
        'The analysis plan in four lines. Recurrence by Cox, stratified by '
        'centre, with death as a competing risk. Adherence by beta regression, '
        'because it is a proportion with a ceiling. And the two endpoints are '
        'intercurrent events for one another: a participant who ulcerates '
        'rightly stops wearing the insole.',

    'Naast de trial lopen twee evaluaties. De economische rekent kosten per '
    'vermeden ulcus én per QALY, met een Markov-model tot vijf jaar. De '
    'procesevaluatie meet of de interventie werkelijk geleverd is. Die tweede '
    'is geen bijlage — bij een nulresultaat is zij het enige wat mechanisme van '
    'uitvoering onderscheidt.':
        'Two evaluations run alongside the trial. The economic one reports cost '
        'per ulcer prevented and cost per QALY, with a Markov model out to five '
        'years. The process evaluation measures whether the intervention was '
        'actually delivered. That second one is not an appendix — under a null '
        'result it is the only thing separating mechanism from delivery.',

    'Ik sluit af met wat we hoe dan ook leren. Stijgt de therapietrouw maar het '
    'recidief niet, dan faalt de biomechanische premisse. Stijgt de '
    'therapietrouw niet, dan faalde het gedragsdeel. In beide gevallen weten we '
    'welke schakel breekt, en dat is precies wat dit veld nog niet weet.':
        'I will close with what we learn either way. If adherence rises but '
        'recurrence does not, the biomechanical premise fails. If adherence '
        'does not rise, the behavioural component failed. Either way we learn '
        'which link in the chain gives way — and that is exactly what this '
        'field does not yet know.',

    'Deze dia laat u staan tijdens de vragen. Alles wat u genoemd hebt, staat '
    'hier met nummer en citaat, in dezelfde nummering als het '
    'protocolmanuscript.':
        'Leave this slide up during questions. Everything cited is listed here '
        'with its number and full citation, in the same numbering as the '
        'protocol manuscript.',

    'Tot slot: wie u aanspreekt. Praktische vragen — inclusies, metingen, '
    'formulieren, sensoren — komen bij mij. Wetenschappelijke vragen en '
    'afspraken op het niveau van uw centrum bij professor Deschamps. Dank u '
    'wel.':
        'Finally, who to contact. Practical questions — inclusions, '
        'measurements, forms, sensors — come to me. Scientific questions and '
        'arrangements at centre level go to Professor Deschamps. Thank you.',
}
