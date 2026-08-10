# -*- coding: utf-8 -*-
"""Bouwt Figuur 2 (interventiepad) en Figuur 4 (PRECIS-2 wiel) in dezelfde
huisstijl als Figure1_CONSORT_flow.svg, Figure3_logic_model.svg en Figure5_CPTS.svg."""
import os
from math import cos, sin, radians

MAP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAVY, TEXT, MUT = '#1B3A5C', '#33475B', '#5A6B7D'
LICHT, RAND, ACC, ROOD = '#EAF1F7', '#C8D3DE', '#0E7C86', '#B04A3A'
GRIJS, GRIJSRAND, BAAN = '#F4F6F8', '#8FA3B5', '#FAFCFD'
FONT = 'Arial, Helvetica, sans-serif'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def txt(x, y, s, fs=11.5, fill=TEXT, bold=False, anchor='start', italic=False, ls=None):
    a = ' font-weight="bold"' if bold else ''
    a += ' font-style="italic"' if italic else ''
    a += ' text-anchor="%s"' % anchor if anchor != 'start' else ''
    a += ' letter-spacing="%s"' % ls if ls else ''
    return '<text x="%g" y="%g" font-size="%g" fill="%s"%s>%s</text>' % (x, y, fs, fill, a, esc(s))


# =====================================================================
# FIGUUR 2 — interventiepad over 18 maanden
# =====================================================================
W2, H2 = 1020, 640
KOL = ['Base', '1', '3', '6', '9', '12', '15', '18']
X0, X1 = 196, 974
BR = (X1 - X0) / len(KOL)


def cx(i):
    return X0 + BR * (i + 0.5)


f = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
     'font-family="%s">' % (W2, H2, W2, H2, FONT),
     '<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
     '<path d="M0,0 L0,6 L8,3 z" fill="%s"/></marker>'
     '<marker id="arT" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
     '<path d="M0,0 L0,6 L8,3 z" fill="%s"/></marker></defs>' % (NAVY, ACC),
     '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W2, H2)]

f.append(txt(30, 30, 'Figure 2. PARADISE intervention pathway across 18 months', 14, NAVY, bold=True))
f.append(txt(30, 49, 'Both arms receive usual care on an identical visit schedule; the components below are additional to it.', 11, MUT))

# ---- tijdas
f.append(txt(30, 78, 'MONTH', 11, NAVY, bold=True, ls='1.1'))
for i, k in enumerate(KOL):
    f.append(txt(cx(i), 78, k, 12, NAVY, bold=True, anchor='middle'))
f.append('<line x1="30" y1="86" x2="%g" y2="86" stroke="%s" stroke-width="1"/>' % (X1, RAND))
# kolomscheidingen lopen tot onderaan de laatste baan (510) en niet door de voetnootband
for i in range(len(KOL) + 1):
    x = X0 + BR * i
    f.append('<line x1="%g" y1="86" x2="%g" y2="510" stroke="#EDF2F6" stroke-width="1"/>' % (x, x))


def baan(y, h, label, badge, badgekleur, achtergrond=BAAN):
    s = ['<rect x="30" y="%g" width="%g" height="%g" rx="4" fill="%s" stroke="%s" stroke-width="1"/>'
         % (y, X1 - 30, h, achtergrond, RAND)]
    s.append(txt(44, y + 22, label[0], 12, NAVY, bold=True))
    if len(label) > 1:
        s.append(txt(44, y + 37, label[1], 12, NAVY, bold=True))
    bw = 6.2 * len(badge) + 12
    by = y + h - 24
    s.append('<rect x="44" y="%g" width="%g" height="14" rx="2" fill="%s"/>' % (by, bw, badgekleur))
    s.append(txt(50, by + 10.5, badge, 9.5, '#FFFFFF', bold=True))
    return '\n  '.join(s)


def chip(i, y, regels, vul=LICHT, rand=NAVY, kop=NAVY, h=None):
    x = cx(i) - 45
    h = h or (14 + 13 * len(regels))
    s = ['<rect x="%g" y="%g" width="90" height="%g" rx="3" fill="%s" stroke="%s" stroke-width="1.4"/>'
         % (x, y, h, vul, rand)]
    ty = y + 16
    for j, r in enumerate(regels):
        s.append(txt(cx(i), ty, r, 9.8 if j else 10.2, TEXT if j else kop,
                     bold=(j == 0), anchor='middle'))
        ty += 12.6
    return '\n  '.join(s)


# ---- baan 1: drukgestuurde schoeiseloptimalisatie
f.append(baan(98, 96, ['Pressure-guided footwear', 'optimisation'], 'PARADISE ARM ONLY', ACC))
f.append(chip(0, 112, ['Baseline pressure', 'Novel pedar,', '8-region mask']))
f.append(chip(1, 112, ['CMFO', 'prescription']))
f.append(chip(2, 112, ['CMFO delivery', '+ Orthotimer', 'integration']))
f.append(chip(3, 112, ['Re-measurement', '+ CMFO', 'replacement']))
f.append(chip(5, 112, ['Re-measurement', '+ CMFO', 'replacement']))
f.append(chip(7, 112, ['CMFO', 'replacement']))
f.append(txt(X0 + 4, 184, 'Target: peak pressure < 200 kPa or \u2265 25% reduction', 9.5, MUT, italic=True))

# ---- baan 2: SEBIA
f.append(baan(206, 96, ['SEBIA behavioural', 'programme'], 'PARADISE ARM ONLY', ACC))
f.append(chip(0, 220, ['Step 1', 'Education, NAFF,', 'health literacy'], '#E6F4F4', ACC, ACC))
f.append(chip(2, 220, ['Step 2', 'Indoor-wear educ.', 'teach-back'], '#E6F4F4', ACC, ACC))
f.append(chip(3, 220, ['Step 3', 'Self-assessment', '+ sensor review'], '#E6F4F4', ACC, ACC))
f.append(chip(4, 220, ['Step 4', 'Skills demo', '+ sensor review'], '#E6F4F4', ACC, ACC))
f.append(chip(5, 220, ['Step 3', 'repeat'], '#E6F4F4', ACC, ACC))
f.append(chip(6, 220, ['Step 4', 'repeat'], '#E6F4F4', ACC, ACC))
f.append(chip(7, 220, ['Step 5', 'Final review,', 'results shared'], '#E6F4F4', ACC, ACC))
f.append(txt(X0 + 4, 292, 'COM-B: capability (1, 2, 4) \u00b7 opportunity (3, 4) \u00b7 motivation (3, 4)', 9.5, MUT, italic=True))

# ---- baan 3: sensormonitoring (beide armen)
f.append(baan(314, 92, ['Sensor-based', 'monitoring'], 'BOTH ARMS', GRIJSRAND, GRIJS))
xA = cx(2) - 45
# label boven de balk, niet erin: de uitleespunten liggen anders over de tekst
f.append(txt(xA, 334, 'Orthotimer \u2014 continuous wear-time recording, read out every three months', 10, NAVY, bold=True))
f.append('<rect x="%g" y="342" width="%g" height="12" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>'
         % (xA, cx(7) + 45 - xA, '#DCE9F2', NAVY))
for i in (2, 3, 4, 5, 6, 7):
    f.append('<circle cx="%g" cy="348" r="4" fill="%s"/>' % (cx(i), NAVY))
for i in (0, 3):
    f.append('<rect x="%g" y="364" width="90" height="20" rx="3" fill="%s" stroke="%s" stroke-width="1.2"/>'
             % (cx(i) - 45, '#EDF1F4', GRIJSRAND))
    f.append(txt(cx(i), 378, 'MoveMonitor 7 d', 9.8, TEXT, anchor='middle'))
f.append(txt(xA, 396, 'Wear-time data withheld in usual care', 9.5, MUT, italic=True))

# ---- baan 4: co-primaire uitkomsten
f.append(baan(414, 96, ['Co-primary', 'outcomes'], 'BOTH ARMS', GRIJSRAND, GRIJS))
yC = 434
f.append('<rect x="%g" y="%g" width="%g" height="22" rx="3" fill="#FFFFFF" stroke="%s" stroke-width="1.3"/>'
         % (cx(1) - 45, yC, cx(7) + 45 - (cx(1) - 45), RAND))
f.append(txt(cx(1) - 36, yC + 15, 'Ulcer surveillance at every visit (PEDIS / WIfI) \u2014 blinded adjudication', 10, TEXT))
f.append('<rect x="%g" y="%g" width="90" height="34" rx="3" fill="#F7E9E5" stroke="%s" stroke-width="1.6"/>'
         % (cx(5) - 45, 466, ROOD))
f.append(txt(cx(5), 480, 'Co-primary 2', 10, ROOD, bold=True, anchor='middle'))
f.append(txt(cx(5), 492, 'adherence', 9.8, TEXT, anchor='middle'))
f.append('<rect x="%g" y="%g" width="90" height="34" rx="3" fill="#F7E9E5" stroke="%s" stroke-width="1.6"/>'
         % (cx(7) - 45, 466, ROOD))
f.append(txt(cx(7), 480, 'Co-primary 1', 10, ROOD, bold=True, anchor='middle'))
f.append(txt(cx(7), 492, 'recurrence', 9.8, TEXT, anchor='middle'))

# ---- voetnootband
f.append('<line x1="30" y1="530" x2="%g" y2="530" stroke="%s" stroke-width="1"/>' % (X1, RAND))
f.append(txt(30, 552, 'Reading this figure', 12, NAVY, bold=True))
for j, r in enumerate([
    'Usual care comprises three-monthly podiatric review, protective footwear with a custom-made foot orthosis, and foot-care education. Its degree of offloading is not quantified',
    'and is not disclosed to the treating team or the participant. Adherence sensors are worn in both arms because the between-arm comparison of adherence is a co-primary endpoint,',
    'but wear-time data are neither shown to nor discussed with usual-care participants or their clinicians, so the behavioural component is not delivered in that arm.',
    'The trial is declared positive only if both co-primary endpoints are met. CMFO, custom-made foot orthosis; SEBIA, Structured Education and Behavioural Intervention Approach.',
]):
    f.append(txt(30, 574 + j * 18, r, 11, TEXT))

f.append('</svg>')
open(os.path.join(MAP, 'Figure2_intervention_pathway.svg'), 'w', encoding='utf-8').write('\n  '.join(f))
print('Figure2_intervention_pathway.svg geschreven')


# =====================================================================
# FIGUUR 4 — PRECIS-2 wiel
# =====================================================================
W4, H4 = 1020, 700
CXW, CYW = 336, 330
DOMEINEN = [
    ('Eligibility', 3, 'IWGDF category 3 only; dialysis and ischaemia excluded'),
    ('Recruitment', 4, 'From routine clinic schedules and referrals; no special drive'),
    ('Setting', 4, 'Six recognised Belgian diabetic foot clinics, academic and not'),
    ('Organisation', 3, 'Existing clinical staff, but MI training and pedar hardware added'),
    ('Flexibility: delivery', 3, 'Five-step SEBIA protocol; individually tailored from Step 3'),
    ('Flexibility: adherence', 4, 'Adherence support is the intervention, not a trial measure'),
    ('Follow-up', 3, 'Extra visits at screening and month 1; far heavier measurement'),
    ('Primary outcome', 4, 'Recurrence is patient-relevant; the adherence co-primary is not'),
    ('Primary analysis', 5, 'Intention-to-treat, all randomised participants retained'),
]


def rad(s):
    return 34 + (s - 1) * 40


def punt(i, r):
    a = radians(-90 + i * 40)
    return CXW + r * cos(a), CYW + r * sin(a)


g = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
     'font-family="%s">' % (W4, H4, W4, H4, FONT),
     '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W4, H4)]

g.append(txt(30, 30, 'Figure 4. PRECIS-2 wheel for PARADISE', 14, NAVY, bold=True))
g.append(txt(30, 49, 'Position on the explanatory\u2013pragmatic continuum. 1 = very explanatory, 5 = very pragmatic.', 11, MUT))

# ringen
for s in range(1, 6):
    g.append('<circle cx="%g" cy="%g" r="%g" fill="none" stroke="%s" stroke-width="%g"/>'
             % (CXW, CYW, rad(s), RAND if s < 5 else GRIJSRAND, 1 if s < 5 else 1.4))
# spaken
for i in range(9):
    x, y = punt(i, rad(5))
    g.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1"/>' % (CXW, CYW, x, y, RAND))
# ringcijfers op de verticale as
for s in range(1, 6):
    g.append(txt(CXW + 4, CYW - rad(s) + 11, str(s), 9.5, MUT))

# polygoon
pts = []
for i, (_, sc, _) in enumerate(DOMEINEN):
    pts.append('%g,%g' % punt(i, rad(sc)))
g.append('<polygon points="%s" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2.4"/>'
         % (' '.join(pts), ACC, ACC))
for i, (_, sc, _) in enumerate(DOMEINEN):
    x, y = punt(i, rad(sc))
    g.append('<circle cx="%g" cy="%g" r="5" fill="%s" stroke="#FFFFFF" stroke-width="1.5"/>' % (x, y, ACC))

# domeinlabels
for i, (naam, sc, _) in enumerate(DOMEINEN):
    a = radians(-90 + i * 40)
    lx, ly = CXW + 214 * cos(a), CYW + 214 * sin(a)
    c = cos(a)
    anchor = 'middle' if abs(c) < 0.25 else ('start' if c > 0 else 'end')
    dy = 4 if abs(sin(a)) < 0.25 else (13 if sin(a) > 0 else -4)
    g.append(txt(lx, ly + dy, naam, 11.5, NAVY, bold=True, anchor=anchor))
    g.append(txt(lx, ly + dy + 14, str(sc), 11.5, ACC, bold=True, anchor=anchor))

# rechterpaneel
PX = 690
g.append('<line x1="%g" y1="86" x2="%g" y2="596" stroke="%s" stroke-width="1"/>' % (PX - 16, PX - 16, RAND))
g.append(txt(PX, 108, 'DOMAIN RATINGS AND BASIS', 11, NAVY, bold=True, ls='1.1'))
y = 136
for naam, sc, motief in DOMEINEN:
    g.append('<rect x="%g" y="%g" width="22" height="18" rx="3" fill="%s"/>' % (PX, y - 13, ACC))
    g.append(txt(PX + 11, y, str(sc), 11.5, '#FFFFFF', bold=True, anchor='middle'))
    g.append(txt(PX + 32, y, naam, 11.5, NAVY, bold=True))
    g.append(txt(PX + 32, y + 15, motief, 10.2, TEXT))
    y += 44

# voetnootband
g.append('<line x1="30" y1="614" x2="990" y2="614" stroke="%s" stroke-width="1"/>' % RAND)
g.append(txt(30, 636, 'Ratings were assigned by the trial team against the design as specified in this protocol. PARADISE is pragmatic in whom it recruits, where it is delivered and how it is', 11, TEXT))
g.append(txt(30, 654, 'analysed, and more explanatory in organisation, flexibility of delivery and follow-up: the trial adds motivational-interviewing training and in-shoe pressure measurement to', 11, TEXT))
g.append(txt(30, 672, 'routine practice, delivers SEBIA as a five-step protocol, and measures far more at each visit than usual care does. That is the trade-off a trial of an unreimbursed service makes.', 11, TEXT))

g.append('</svg>')
open(os.path.join(MAP, 'Figure4_PRECIS2.svg'), 'w', encoding='utf-8').write('\n  '.join(g))
print('Figure4_PRECIS2.svg geschreven')
