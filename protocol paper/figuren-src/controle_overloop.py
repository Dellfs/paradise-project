# -*- coding: utf-8 -*-
"""Controleert SVG-tekst op overloop buiten het canvas en buiten de chips,
met Helvetica/Arial-breedtemetriek (AFM, per 1000 em)."""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AFM = {
 ' ':278,'!':278,'"':355,'#':556,'$':556,'%':889,'&':667,"'":191,'(':333,')':333,'*':389,
 '+':584,',':278,'-':333,'.':278,'/':278,'0':556,'1':556,'2':556,'3':556,'4':556,'5':556,
 '6':556,'7':556,'8':556,'9':556,':':278,';':278,'<':584,'=':584,'>':584,'?':556,'@':1015,
 'A':667,'B':667,'C':722,'D':722,'E':667,'F':611,'G':778,'H':722,'I':278,'J':500,'K':667,
 'L':556,'M':833,'N':722,'O':778,'P':667,'Q':778,'R':722,'S':667,'T':611,'U':722,'V':667,
 'W':944,'X':667,'Y':667,'Z':611,'[':278,'\\':278,']':278,'^':469,'_':556,'`':333,
 'a':556,'b':556,'c':500,'d':556,'e':556,'f':278,'g':556,'h':556,'i':222,'j':222,'k':500,
 'l':222,'m':833,'n':556,'o':556,'p':556,'q':556,'r':333,'s':500,'t':278,'u':556,'v':500,
 'w':722,'x':500,'y':500,'z':500,'{':334,'|':260,'}':334,'~':584,
 '—':1000,'–':556,'‘':222,'’':222,'“':333,'”':333,
 '·':278,'≥':549,'≤':549,'×':584,'∫':400,'→':987,'°':400,
}
BOLD = {'A':722,'B':722,'C':722,'D':722,'E':667,'F':611,'G':778,'H':722,'I':278,'J':556,
 'K':722,'L':611,'M':833,'N':722,'O':778,'P':667,'Q':778,'R':722,'S':667,'T':611,'U':722,
 'V':667,'W':944,'X':667,'Y':667,'Z':611,'a':556,'b':611,'c':556,'d':611,'e':556,'f':333,
 'g':611,'h':611,'i':278,'j':278,'k':556,'l':278,'m':889,'n':611,'o':611,'p':611,'q':611,
 'r':389,'s':556,'t':333,'u':611,'v':556,'w':778,'x':556,'y':556,'z':500,' ':278,'0':556,
 '1':556,'2':556,'3':556,'4':556,'5':556,'6':556,'7':556,'8':556,'9':556,'.':278,',':278,
 '-':333,'/':278,':':333,'(':333,')':333,'%':889,'+':584,'<':584,'>':584,'≥':549,
 '—':1000,'–':556,'·':278,}


def breedte(s, fs, bold=False, ls=0.0):
    t = BOLD if bold else AFM
    w = sum(t.get(c, AFM.get(c, 556)) for c in s) / 1000.0 * fs
    return w + ls * max(0, len(s) - 1)


def check(pad):
    src = open(pad, encoding='utf-8').read()
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', src)
    W, H = int(m.group(1)), int(m.group(2))
    rects = []
    for r in re.finditer(r'<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"', src):
        rects.append(tuple(float(g) for g in r.groups()))
    fouten = []
    for t in re.finditer(
            r'<text x="([-\d.]+)" y="([-\d.]+)" font-size="([\d.]+)"[^>]*?>(.*?)</text>', src, re.S):
        x, y, fs = float(t.group(1)), float(t.group(2)), float(t.group(3))
        attrs, body = t.group(0), t.group(4)
        bold = 'font-weight="bold"' in attrs
        ls = 0.0
        lsm = re.search(r'letter-spacing="([\d.]+)"', attrs)
        if lsm: ls = float(lsm.group(1))
        anchor = 'start'
        if 'text-anchor="middle"' in attrs: anchor = 'middle'
        elif 'text-anchor="end"' in attrs: anchor = 'end'
        s = body.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        w = breedte(s, fs, bold, ls)
        if anchor == 'middle': x0 = x - w / 2
        elif anchor == 'end':  x0 = x - w
        else:                  x0 = x
        x1 = x0 + w
        if x0 < 4 or x1 > W - 4:
            fouten.append('CANVAS  x=[%.0f..%.0f] (W=%d) fs=%.1f  %r' % (x0, x1, W, fs, s[:60]))
            continue
        # binnen welke chip valt het baseline-punt?
        for rx, ry, rw, rh in rects:
            if rw <= 200 and ry < y < ry + rh + 2 and rx - 2 <= x <= rx + rw + 2:
                if x0 < rx - 1 or x1 > rx + rw + 1:
                    fouten.append('CHIP    tekst [%.0f..%.0f] buiten rect [%.0f..%.0f]  %r'
                                  % (x0, x1, rx, rx + rw, s[:60]))
                break
    print('=== %s  (%dx%d, %d tekstelementen) ===' % (pad.split('\\')[-1], W, H, len(re.findall(r'<text', src))))
    if fouten:
        for f in fouten: print('  ' + f)
    else:
        print('  geen overloop gevonden')
    print()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        check(p)
