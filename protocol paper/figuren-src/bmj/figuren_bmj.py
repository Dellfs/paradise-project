"""Figures 1-5 of the BMJ Open manuscript (PARADISE protocol), drawn with figlib.

usage: python -X utf8 figs_v2.py <out dir> [figure numbers...]
Writes FigureN.svg; render.py turns them into TIFF for submission.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *

OUT = sys.argv[1]
WANT = [int(a) for a in sys.argv[2:]] or [1, 2, 3, 4, 5]


def caps(f, x, y, s, col=MUTED, size=9.5, anchor='start'):
    f.text(x, y, s.upper(), size, col, True, anchor=anchor, spacing='0.8')


# ====================================================================== Figure 1: trial flow
def fig1():
    f = Fig(1000, 624)
    for y, s in ((54, 'Enrolment'), (318, 'Allocation'), (418, 'Follow-up'), (548, 'Analysis')):
        caps(f, 20, y, s)
    f.box(380, 26, 340, 46, 'Assessed for eligibility (n = …)', centre=True, pad=13)
    f.box(752, 84, 228, 78, 'Excluded (n = …)', ['Not meeting inclusion criteria (n = …)', 'Declined to participate (n = …)',
                                                 'Other reasons (n = …)'], kind='white', size=10.5, tsize=11.5)
    f.line([(550, 72), (550, 192)])
    f.line([(550, 129), (752, 129)])
    f.box(380, 192, 340, 62, 'Randomised (n = 144)', 'Stratified by clinic: 24 per clinic, 12:12, sealed opaque '
          'envelopes', centre=True, size=10.5)
    f.line([(550, 254), (550, 272)], arrow=False)
    f.line([(320, 272), (780, 272)], arrow=False)
    f.line([(320, 272), (320, 292)])
    f.line([(780, 272), (780, 292)])
    left, right = 140, 600
    f.box(left, 292, 360, 72, 'Usual care plus PARADISE (n = 72)', ['Received allocated intervention (n = …)',
          'Did not receive, with reasons (n = …)'], kind='paradise', size=10.5)
    f.box(right, 292, 360, 72, 'Usual care (n = 72)', ['Received usual care (n = …)', 'Did not receive, with reasons (n = …)'],
          size=10.5)
    for x in (320, 780):
        f.line([(x, 364), (x, 392)])
        f.line([(x, 500), (x, 524)])
    fu = ['Visit 2, then every 3 months to 18 months', 'Lost to follow-up, with reasons (n = …)',
          'Discontinued intervention (n = …)', 'Withdrew consent (n = …)', 'Died (n = …)']
    f.box(left, 392, 360, 108, 'Follow-up', fu, kind='white', size=10.5)
    f.box(right, 392, 360, 108, 'Follow-up', [fu[0], fu[1], fu[3], fu[4]], kind='white', size=10.5)
    an = ['Primary outcome: all randomised, as allocated', 'Mediator: adherence, months 9 to 12',
          'Excluded from analysis, with reasons (n = …)']
    f.box(left, 524, 360, 78, 'Analysed (n = …)', an, kind='white', size=10.5)
    f.box(right, 524, 360, 78, 'Analysed (n = …)', an, kind='white', size=10.5)
    return f


# ====================================================================== Figure 2: conceptual framework
def fig2():
    f = Fig(1000, 650)
    caps(f, 30, 24, 'Intervention')
    caps(f, 250, 24, 'Determinants targeted or observed')
    caps(f, 712, 24, 'Integrated load')
    caps(f, 880, 24, 'Outcome')
    f.rect(16, 36, 968, 222, BAND, 'none', 0, rx=4)
    f.rect(16, 268, 968, 236, BAND, 'none', 0, rx=4)
    f.rect(16, 514, 968, 120, BAND, 'none', 0, rx=4)
    caps(f, 30, 56, 'Biomechanical layer', LINE, 9)
    caps(f, 30, 288, 'Behavioural layer', LINE, 9)
    caps(f, 30, 534, 'Implementation layer', LINE, 9)

    f.box(30, 70, 190, 132, 'Pressure-guided optimisation', 'CMFO modified until every target region is below '
          '200 kPa or at least 25% lower than without it', kind='paradise', tag='PARADISE arm', size=11)
    f.box(258, 70, 204, 132, 'Offloading delivered', 'In-shoe peak pressure at the target regions',
          'Novel pedar, without and with CMFO, at four sessions', kind='white', size=11)
    f.box(500, 154, 180, 92, 'Weight-bearing activity', 'Steps and standing time', 'MoveMonitor, 7 days from baseline',
          kind='white', tag='Observed, not targeted', size=11)
    f.box(722, 186, 140, 132, 'Cumulative plantar tissue stress', 'Pressure and activity accumulated while the foot '
          'is unprotected', kind='white', tag='Exploratory', size=10.5, tsize=12)
    f.box(888, 186, 92, 132, 'Ulcer recurrence', 'Time to first ulcer within 18 months', kind='primary', tag='Primary',
          size=10.5, tsize=12, centre=True, pad=8)
    f.box(888, 332, 92, 56, 'Death', 'competing event', kind='muted', size=10, tsize=11, centre=True, pad=8)

    f.box(30, 302, 190, 156, 'SEBIA and wear feedback', 'Five steps at all eight visits; review of the participant\'s '
          'own wear data from month 3; motivational interviewing', kind='paradise', tag='PARADISE arm', size=11)
    # COM-B box drawn by hand: three determinants
    x, y, w, h = 258, 302, 214, 190
    f.rect(x, y, w, h, '#FFFFFF', RULE, 1.2)
    f.text(x + 10, y + 21, 'COM-B determinants of wear', 12.5, INK, True)
    rows = [('Capability', 'foot-care skills and knowledge', 'NAFF; teach-back'),
            ('Opportunity', 'wearing at home, at work and indoors', 'barrier inventory'),
            ('Motivation', 'importance and confidence', '0–10 rulers')]
    yy = y + 46
    for head, body, meas in rows:
        f.text(x + 10, yy, head, 11, TEAL, True)
        f.text(x + 10, yy + 15, body, 11, INK)
        f.text(x + 10, yy + 29, meas, 10, MUTED, italic=True)
        yy += 48
    f.box(510, 340, 172, 118, 'Footwear wear', 'Share of waking time the prescribed footwear is worn',
          'Orthotimer with MoveMonitor waking time', kind='mediator', tag='Mediator', size=11)

    f.line([(220, 136), (258, 136)])
    f.line([(220, 380), (258, 380)])
    f.line([(472, 399), (510, 399)])
    f.line([(462, 112), (772, 112), (772, 186)])
    f.line([(680, 214), (722, 214)])
    f.line([(682, 420), (792, 420), (792, 318)])
    f.line([(862, 252), (888, 252)])

    f.text(30, 562, 'Both components are delivered by the clinics\' own staff under routine caseloads. Fidelity', 11, INK)
    f.text(30, 578, '(pressure reduction achieved, SEBIA checklist), dose and reach are examined in the process', 11, INK)
    f.text(30, 594, 'evaluation (figure 3). Usual care receives the same CMFO and sensor, without pressure-guided', 11, INK)
    f.text(30, 610, 'modification or use of the wear data.', 11, INK)
    f.text(560, 562, 'Pre-specified effect modifiers', 11, INK, True)
    f.text(560, 578, 'Diabetes type · minor amputation versus healed ulcer only', 11, INK)
    f.text(560, 594, 'Health literacy · academic versus non-academic clinic', 11, INK)
    return f


# ====================================================================== Figure 3: optimisation algorithm
def fig3():
    f = Fig(1000, 800)
    cx, bw = 360, 400
    bx = cx - bw / 2
    f.box(bx, 20, bw, 56, 'Baseline, both arms', 'In-shoe peak pressure in eight foot regions', centre=True, size=11)
    f.line([(cx, 76), (cx, 100)])
    f.box(bx, 100, bw, 78, 'Define up to three target regions per foot', 'The previous ulcer site, plus the two forefoot '
          'or midfoot regions with the highest peak pressure above 200 kPa; the heel only if it was the ulcer site',
          kind='white', centre=True, size=11)
    f.rect(118, 204, 864, 580, 'none', TEAL, 1.2, rx=6, dash='5,4')
    caps(f, 966, 226, 'Each session in the PARADISE arm: CMFO delivery (visit 2) and 6, 12 and 18 months', TEAL, 9.5,
         anchor='end')
    f.line([(cx, 178), (cx, 244)])
    f.box(bx, 244, bw, 46, '1   Measure without the CMFO', kind='paradise', centre=True, pad=15)
    f.line([(cx, 290), (cx, 314)])
    f.box(bx, 314, bw, 46, '2   Measure with the CMFO', kind='paradise', centre=True, pad=15)
    f.line([(cx, 360), (cx, 384)])
    d1 = 452
    f.diamond(cx, d1, 380, 136)
    for i, s in enumerate(['At every target region, is peak', 'pressure below 200 kPa or at least',
                           '25% lower than without the CMFO?']):
        f.text(cx, d1 - 14 + i * 15, s, 11, INK, anchor='middle')
    f.line([(cx, d1 + 68), (cx, 554)])
    f.text(cx + 8, d1 + 84, 'Yes', 10.5, LINE, True)
    d2 = 618
    f.diamond(cx, d2, 380, 128)
    for i, s in enumerate(['Follow-up sessions: has peak', 'pressure at any target region risen',
                           'by 5% or more since the previous session?']):
        f.text(cx, d2 - 14 + i * 15, s, 11, INK, anchor='middle')
    f.line([(cx, d2 + 64), (cx, 700)])
    f.text(cx - 8, d2 + 78, 'No', 10.5, LINE, True, anchor='end')
    f.box(bx, 700, bw, 66, 'Offloading adequate', 'The reduction achieved is recorded; at the first adequate session an '
          'identical second pair is made', kind='white', centre=True, size=11)
    mx, mw = 680, 270
    f.box(mx, 418, mw, 68, 'Pedorthist modifies the CMFO', 'Up to three modifications per session', kind='paradise',
          size=11)
    f.line([(cx + 190, d1), (mx, d1)])
    f.text(cx + 200, d1 - 7, 'No', 10.5, LINE, True)
    f.line([(cx + 190, d2), (760, d2), (760, 486)])
    f.text(cx + 200, d2 - 7, 'Yes', 10.5, LINE, True)
    f.line([(880, 418), (880, 337), (cx + bw / 2, 337)])
    f.text(890, 382, 'Measure again', 10.5, MUTED, italic=True)
    f.line([(950, 452), (968, 452), (968, 733), (cx + bw / 2, 733)], dash='4,3')
    f.text(958, 556, 'After the third', 10.5, MUTED, italic=True, anchor='end')
    f.text(958, 571, 'modification, the', 10.5, MUTED, italic=True, anchor='end')
    f.text(958, 586, 'reduction achieved', 10.5, MUTED, italic=True, anchor='end')
    f.text(958, 601, 'is recorded', 10.5, MUTED, italic=True, anchor='end')
    return f


# ====================================================================== Figure 4: what each arm receives
def fig4():
    f = Fig(1000, 672)
    cols = ['Screening', 'Baseline', 'Visit 2', '3', '6', '9', '12', '15', '18']
    x0, x1 = 330, 962
    X = [x0 + i * (x1 - x0) / 8 for i in range(9)]
    for x, c in zip(X, cols):
        f.text(x, 46, c, 11, INK, True, anchor='middle')
    f.text(X[2], 61, '2–4 weeks', 9.5, MUTED, anchor='middle')
    f.text((X[3] + X[8]) / 2, 22, 'Months from randomisation', 10, MUTED, anchor='middle')
    f.line([(X[3] - 20, 28), (X[8] + 20, 28)], color=RULE, sw=1, arrow=False)
    for x in X:
        f.line([(x, 70), (x, 658)], color='#E3E7EA', sw=1, arrow=False)

    def band(y, h, label, col):
        f.rect(16, y, 968, h, BAND, 'none', 0, rx=4)
        caps(f, 28, y + 18, label, col, 9.5)

    def row(y, label):
        f.text(28, y + 4, label, 11, INK)

    def bar(xa, xb, y, fill, dash=None):
        if dash:
            f.line([(xa, y), (xb, y)], color=fill, sw=3, arrow=False, dash=dash)
        else:
            f.rect(xa, y - 4, xb - xa, 8, fill, 'none', 0, rx=4)

    def chip(x, y, s, fill, col='#FFFFFF', w=None):
        w = w or max(20, tw(s, 10, True) + 12)
        f.rect(x - w / 2, y - 9, w, 18, fill, 'none', 0, rx=9)
        f.text(x, y + 3.5, s, 10, col, True, anchor='middle')

    band(74, 264, 'Both arms', LINE)
    y = 112
    row(y, 'Eligibility, consent, randomisation'); chip(X[0], y, 'consent', LINE); chip(X[1], y, 'randomise', LINE)
    y += 38
    row(y, 'Podiatric care and screening every 3 months'); bar(X[1], X[8], y, '#C4CDD4'); y += 38
    row(y, 'Ulcer surveillance, unscheduled visits')
    for x in X[1:]:
        f.circle(x, y, 5, LINE)
    y += 38
    row(y, 'New CMFO with embedded wear sensor'); chip(X[2], y, 'fitted', LINE)
    for x in X[3:]:
        chip(x, y, 'read', '#C4CDD4', INK)
    y += 38
    row(y, 'MoveMonitor, 7 days'); chip(X[1], y, '7 days', LINE); chip(X[2], y, 'returned', '#C4CDD4', INK); y += 38
    row(y, 'EQ-5D-5L; costs from month 3')
    for x in [X[1]] + X[3:]:
        f.circle(x, y, 5, '#FFFFFF', LINE)

    band(350, 196, 'PARADISE arm only', TEAL)
    y = 388
    row(y, 'Pressure-guided CMFO optimisation'); chip(X[1], y, 'targets', TEAL)
    for x in (X[2], X[4], X[6], X[8]):
        chip(x, y, 'optimise', TEAL)
    y += 38
    row(y, 'Second identical pair, serviced in turn'); bar(X[2] + 36, X[8], y, '#A9D3D7')
    y += 38
    row(y, 'SEBIA step')
    for x, s in zip(X[1:], ['1', '2', '3', '4', '3', '4', '3', '5']):
        chip(x, y, s, TEAL, w=22)
    y += 38
    row(y, 'Review of own wear data')
    for x in X[3:]:
        f.circle(x, y, 5, TEAL)

    band(558, 100, 'Usual care arm only', MUTED)
    y = 596
    row(y, 'In-shoe pressure, values hidden')
    for x in (X[1], X[4]):
        f.circle(x, y, 5, '#FFFFFF', MUTED)
    y += 38
    row(y, 'Wear data recorded, not shown or discussed'); bar(X[2], X[8], y, MUTED, dash='5,4')
    return f


# ====================================================================== Figure 5: logic model
def fig5():
    f = Fig(1000, 548)
    xs = [20, 216, 412, 608, 804]
    w = 176
    heads = ['Inputs', 'Activities', 'Outputs', 'Short and medium term', 'Long term']
    for x, h in zip(xs, heads):
        caps(f, x, 26, h, LINE, 10)
    cols = [
        [('Six recognised diabetic foot clinics and their staff', 'shared'),
         ('Certified pedorthists; reimbursed protective footwear', 'shared'),
         ('Novel pedar, Orthotimer and MoveMonitor', 'shared'),
         ('Training in measurement, SEBIA and motivational interviewing', 'shared')],
        [('Pressure-guided CMFO optimisation at visit 2 and 6, 12 and 18 months', 'paradise'),
         ('Second pair; both pairs serviced every 3 months', 'paradise'),
         ('Five SEBIA steps at all eight visits', 'paradise'),
         ('Review of own wear data from month 3', 'paradise')],
        [('Pressure reduction achieved per target region', 'white'),
         ('Sessions delivered, duration and fidelity scores', 'white'),
         ('Sensor completeness; review below 70%', 'white'),
         ('Reach: share of eligible patients enrolled', 'white')],
        [('Foot-care behaviour (NAFF)', 'white'),
         ('Capability, opportunity and motivation to wear the footwear', 'white'),
         ('Footwear adherence', 'mediator', 'Mediator'),
         ('Cumulative plantar tissue stress', 'white', 'Exploratory')],
        [('Ulcer recurrence', 'primary', 'Primary'),
         ('Quality of life, costs and cost-utility', 'white'),
         ('Sustained delivery in routine care', 'white')],
    ]
    h, gap, top = 64, 10, 44
    full = 4 * h + 3 * gap
    mid = top + full / 2
    for ci, (x, items) in enumerate(zip(xs, cols)):
        y0 = top + (full - (len(items) * h + (len(items) - 1) * gap)) / 2
        for k, it in enumerate(items):
            y = y0 + k * (h + gap)
            tag = it[2] if len(it) > 2 else None
            if tag:
                f.box(x, y, w, h, it[0], kind=it[1], tag=tag, size=11, tsize=11.5)
            else:
                f.box(x, y, w, h, body=it[0], kind=it[1], size=11, pad=10)
        if ci < 4:
            f.line([(x + w + 4, mid), (xs[ci + 1] - 5, mid)], sw=2)
    f.rect(16, 346, 968, 140, BAND, 'none', 0, rx=4)
    caps(f, 30, 368, 'Context expected to moderate delivery and effect', LINE, 9.5)
    ctx = [('Participant', ['Health literacy and language', 'Foot deformity and activity level', 'Comorbidity',
                            'Routines at home and at work']),
           ('Professional', ['Motivational interviewing skill', 'Pedorthist experience', 'Spread of techniques to usual care']),
           ('Clinic and system', ['Academic or non-academic clinic', 'Caseload, clinic time, staff continuity',
                                  'Footwear reimbursed; pressure measurement and counselling time not'])]
    for k, (hd, items) in enumerate(ctx):
        x = 30 + k * 322
        f.text(x, 392, hd, 11.5, INK, True)
        yy = 410
        for it in items:
            yy = f.para(x, yy, '· ' + it, 300, 11, INK, lead=15)
    f.text(30, 512, 'Assumptions: offloading protects the foot only while it is worn; wear depends on capability, '
                    'opportunity and motivation, which counselling can change;', 10.5, MUTED, italic=True)
    f.text(30, 528, 'routine clinic teams can deliver both components with fidelity.', 10.5, MUTED, italic=True)
    return f

FIGS = {1: fig1, 2: fig2, 3: fig5, 4: fig4, 5: fig3}   # numbered by first citation
os.makedirs(OUT, exist_ok=True)
for n in WANT:
    open(os.path.join(OUT, 'Figure%d.svg' % n), 'w', encoding='utf-8').write(FIGS[n]().svg())
    print('Figure%d.svg' % n)
