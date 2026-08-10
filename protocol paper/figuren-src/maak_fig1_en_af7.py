# -*- coding: utf-8 -*-
"""Bouwt de ontbrekende Figuur 1 (CONSORT) en een nieuwe powerfiguur,
in dezelfde huisstijl als Figure3_logic_model.svg en Figure5_CPTS.svg."""
import io, os
from math import log, sqrt
from statistics import NormalDist

import os
MAP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVY, TEXT, MUT = '#1B3A5C', '#33475B', '#5A6B7D'
LICHT, RAND, ACC, ROOD = '#EAF1F7', '#C8D3DE', '#0E7C86', '#B04A3A'
FONT = 'Arial, Helvetica, sans-serif'

# ============================================================ FIGUUR 1: CONSORT
def doos(x, y, w, h, regels, vul=LICHT, rand=RAND, fs=11.5):
    s = ['<rect x="%g" y="%g" width="%g" height="%g" rx="4" fill="%s" stroke="%s"/>' % (x, y, w, h, vul, rand)]
    ty = y + 18
    for i, r in enumerate(regels):
        vet = ' font-weight="bold"' if i == 0 else ''
        s.append('<text x="%g" y="%g" font-size="%g" fill="%s"%s>%s</text>' % (x + 10, ty, fs, TEXT, vet, r))
        ty += 15
    return '\n  '.join(s)

def pijl(x1, y1, x2, y2):
    return ('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.4" '
            'marker-end="url(#ar)"/>' % (x1, y1, x2, y2, NAVY))

W, H = 1020, 700
f1 = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="%s">' % (W, H, W, H, FONT),
      '<defs><marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
      '<path d="M0,0 L0,6 L8,3 z" fill="%s"/></marker></defs>' % NAVY,
      '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H)]

f1.append('<text x="%d" y="30" font-size="14" font-weight="bold" fill="%s">Figure 1. Planned participant flow (CONSORT 2025)</text>' % (40, NAVY))

mid = 330
f1.append(doos(mid, 55, 360, 42, ['Assessed for eligibility (n = \u2026)'], '#FFFFFF'))
f1.append(pijl(mid + 180, 97, mid + 180, 130))

f1.append(doos(720, 108, 270, 92, ['Excluded (n = \u2026)',
                                   '\u2022 Not meeting inclusion criteria (n = \u2026)',
                                   '\u2022 Declined to participate (n = \u2026)',
                                   '\u2022 Other reasons (n = \u2026)'], '#F4F6F8'))
f1.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.4" marker-end="url(#ar)"/>'
          % (mid + 180, 118, 720, 118, NAVY))

f1.append(doos(mid, 130, 360, 42, ['Randomised (n = 144), stratified by centre'], LICHT, NAVY))
# stomp aansluiten op de verdeelbalk: een pijlpunt op een T-splitsing wijst nergens heen
f1.append('<line x1="%g" y1="172" x2="%g" y2="196" stroke="%s" stroke-width="1.4"/>'
          % (mid + 180, mid + 180, NAVY))
# de verdeelbalk eindigt boven het midden van de toewijzingsboxen (210 en 830),
# gelijk met alle pijlen daaronder
f1.append('<line x1="210" y1="196" x2="830" y2="196" stroke="%s" stroke-width="1.4"/>' % NAVY)
f1.append(pijl(210, 196, 210, 226))
f1.append(pijl(830, 196, 830, 226))

f1.append(doos(60, 226, 300, 74, ['Allocated to PARADISE (n = 72)',
                                  '\u2022 Received allocated intervention (n = \u2026)',
                                  '\u2022 Did not receive, with reasons (n = \u2026)'], LICHT))
f1.append(doos(680, 226, 300, 74, ['Allocated to usual care (n = 72)',
                                   '\u2022 Received allocated care (n = \u2026)',
                                   '\u2022 Did not receive, with reasons (n = \u2026)'], LICHT))

for x in (210, 830):
    f1.append(pijl(x, 300, x, 336))
f1.append(doos(60, 336, 300, 74, ['Follow-up to 18 months',
                                  '\u2022 Lost to follow-up, with reasons (n = \u2026)',
                                  '\u2022 Discontinued intervention (n = \u2026)'], '#FFFFFF'))
f1.append(doos(680, 336, 300, 74, ['Follow-up to 18 months',
                                   '\u2022 Lost to follow-up, with reasons (n = \u2026)',
                                   '\u2022 Discontinued study care (n = \u2026)'], '#FFFFFF'))

for x in (210, 830):
    f1.append(pijl(x, 410, x, 446))
f1.append(doos(60, 446, 300, 88, ['Analysed (intention to treat)',
                                  '\u2022 Co-primary: ulcer recurrence (n = \u2026)',
                                  '\u2022 Co-primary: footwear adherence (n = \u2026)',
                                  '\u2022 Excluded from analysis, with reasons (n = \u2026)'], LICHT))
f1.append(doos(680, 446, 300, 88, ['Analysed (intention to treat)',
                                   '\u2022 Co-primary: ulcer recurrence (n = \u2026)',
                                   '\u2022 Co-primary: footwear adherence (n = \u2026)',
                                   '\u2022 Excluded from analysis, with reasons (n = \u2026)'], LICHT))

f1.append('<text x="40" y="578" font-size="11" fill="%s">Planned flow. Observed numbers, exclusions and losses to '
          'follow-up will be reported in the results publication. Target enrolment is 24 participants at each of six</text>' % MUT)
f1.append('<text x="40" y="595" font-size="11" fill="%s">Diabetic Foot Clinics; adherence sensors are worn in both arms, '
          'with sensor-derived feedback delivered only in the PARADISE arm.</text>' % MUT)
f1.append('</svg>')
io.open(os.path.join(MAP, 'Figure1_CONSORT_flow.svg'), 'w', encoding='utf-8').write('\n  '.join(f1))

# ============================================================ POWERFIGUUR
Phi = NormalDist().cdf
z = 1.959964

def power(p1, n=122, p0=0.50):
    hr = log(1 - p1) / log(1 - p0)
    d = n * ((p0 + p1) / 2)
    return Phi(sqrt(d) * abs(log(hr)) / 2 - z)

W2, H2 = 900, 560
L, R, T, B = 90, 40, 70, 80
pw, ph = W2 - L - R, H2 - T - B
x0, x1 = 0.20, 0.40                     # aangenomen recidief onder PARADISE
def X(p): return L + (p - x0) / (x1 - x0) * pw
def Y(v): return T + (1 - v) * ph

f2 = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="%s">' % (W2, H2, W2, H2, FONT),
      '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W2, H2),
      '<text x="40" y="30" font-size="14" font-weight="bold" fill="%s">Additional file 7. Statistical power for ulcer recurrence '
      'across assumed intervention effects</text>' % NAVY,
      '<text x="40" y="48" font-size="11" fill="%s">n = 122 analysable participants; usual-care 18-month recurrence '
      'fixed at 50%%; two-sided \u03b1 = 0.05; log-rank test.</text>' % MUT]

for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0):
    f2.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1"/>' % (L, Y(v), L + pw, Y(v), '#EDF1F5'))
    f2.append('<text x="%g" y="%g" font-size="11" fill="%s" text-anchor="end">%d%%</text>' % (L - 10, Y(v) + 4, MUT, v * 100))
for p in (0.20, 0.25, 0.30, 0.35, 0.40):
    f2.append('<text x="%g" y="%g" font-size="11" fill="%s" text-anchor="middle">%g%%</text>' % (X(p), T + ph + 22, MUT, p * 100))

f2.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.3"/>' % (L, T + ph, L + pw, T + ph, MUT))
f2.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.3"/>' % (L, T, L, T + ph, MUT))

# 80%-referentielijn
f2.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.2" stroke-dasharray="5,4"/>'
          % (L, Y(0.80), L + pw, Y(0.80), ROOD))
f2.append('<text x="%g" y="%g" font-size="10.5" fill="%s">conventional 80%% power</text>' % (L + pw - 145, Y(0.80) - 7, ROOD))

# adherentie-power
f2.append('<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="1.2" stroke-dasharray="2,3"/>'
          % (L, Y(0.87), L + pw, Y(0.87), ACC))
f2.append('<text x="%g" y="%g" font-size="10.5" fill="%s">adherence endpoint, 87%%</text>' % (L + 510, Y(0.87) - 7, ACC))

pts = []
p = x0
while p <= x1 + 1e-9:
    pts.append('%g,%g' % (X(p), Y(power(p))))
    p += 0.0025
f2.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.4"/>' % (' '.join(pts), NAVY))

for p, lab, dy in [(0.25, 'primary assumption', 18.663), (0.30, '', 12),
                   (0.325, '', 12), (0.35, '', 12)]:
    v = power(p)
    f2.append('<circle cx="%g" cy="%g" r="5" fill="%s"/>' % (X(p), Y(v), NAVY))
    f2.append('<text x="%g" y="%g" font-size="11" font-weight="bold" fill="%s" text-anchor="middle">%d%%</text>'
              % (X(p), Y(v) - dy, NAVY, round(v * 100)))
    if lab:
        f2.append('<text x="%g" y="%g" font-size="10.5" fill="%s" text-anchor="middle">%s</text>' % (X(p), Y(v) - dy - 15, MUT, lab))

f2.append('<text x="%g" y="%g" font-size="12" fill="%s" text-anchor="middle">Assumed 18-month recurrence under PARADISE</text>'
          % (L + pw / 2, T + ph + 38, TEXT))
f2.append('<text x="20" y="%g" font-size="12" fill="%s" transform="rotate(-90 20 %g)" text-anchor="middle">Power</text>'
          % (T + ph / 2, TEXT, T + ph / 2))
f2.append('<text x="40" y="%d" font-size="11" fill="%s">Because the trial is declared positive only if both co-primary '
          'endpoints are met, the probability of succeeding on both is lower than either curve</text>' % (H2 - 26, MUT))
f2.append('<text x="40" y="%d" font-size="11" fill="%s">alone \u2014 approximately 74%% under the primary assumption if the '
          'endpoints are independent, and higher to the extent that they correlate.</text>' % (H2 - 10, MUT))
f2.append('</svg>')
io.open(os.path.join(MAP, 'Additional_file_7_power_curve.svg'), 'w', encoding='utf-8').write('\n  '.join(f2))

print('Figure1_CONSORT_flow.svg  aangemaakt')
print('Additional_file_7_power_curve.svg  aangemaakt')
print()
for p in (0.25, 0.30, 0.325, 0.35):
    print('  power bij %.1f%%: %.0f%%' % (100 * p, 100 * power(p)))
