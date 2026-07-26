#!/usr/bin/env python3
"""
PARADISE – Schoeisel-adherentieanalyse
=======================================
Methodologie: Jarl et al. (2023, Sensors) + Bus/van Netten

Installatie:
    pip install pymupdf

Gebruik:
    python paradise_adherentie.py
    python paradise_adherentie.py --pdf "M004_visit1.pdf" --tef "M004_chip.tef"
    python paradise_adherentie.py --map "data/"   # verwerkt alle PDF+TEF-paren in een map

Output per deelnemer:
    adh_OOB   – proportie out-of-bed-tijd met schoeisel    (PRIMAIR met beschikbare data)
    adh_WB    – proportie gewichtsdragende tijd met schoen  (BENADERING; zie noot)
    doel_h    – Orthotimer-draagdoel in uur/dag (= gem. OOB-tijd × 80 %)

Noot adh_WB:
    Exacte berekening vereist epoch-niveau synchronisatie (McRoberts DataLOG-CSV +
    Orthotimer raw 15-min export). Met dagelijkse totalen wordt aangenomen dat het
    schoeisel uniform verdeeld is over de OOB-periode. adh_WB ≈ adh_OOB in dat geval.
    Voor publicatie: rapporteer adh_OOB als primaire maat; vermeld de beperking.
"""

import re
import zipfile
import argparse
import statistics
from pathlib import Path
from datetime import date, datetime, timedelta

# ─────────────────────────────────────────────────────────
# PARAMETERS  (aanpasbaar)
# ─────────────────────────────────────────────────────────
WEAR_MIN_H      = 12      # min. accelerometerdraagtijd voor een geldige dag
MIN_VALID_DAYS  = 4       # min. geldige dagen per deelnemer
CUTOFF          = 0.80    # drempel hoog/laag adherent
MIN_LYING_BOUT  = 0.50    # min. 30 min per extra ligperiode (voor slaapschatting)

# ─────────────────────────────────────────────────────────
# PDF-PARSER  (McRoberts Physical Activity Overview)
# ─────────────────────────────────────────────────────────
MONTHS = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,
           'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

ACTIVITIES = [
    ('walking',   'Walking'),
    ('stair',     'Stair walking'),
    ('cycling',   'Cycling'),
    ('standing',  'Standing'),
    ('shuffling', 'Shuffling'),
    ('sitting',   'Sitting'),
    ('lying',     'Lying'),
]


def _hm(s: str) -> float:
    """'4h 30m' → 4.5  |  '0h 05m' → 0.083"""
    m = re.search(r'(\d+)h\s*(\d+)m', s)
    return int(m.group(1)) + int(m.group(2)) / 60 if m else 0.0


def _debold(s: str) -> str:
    """Verwijdert PDF-vetdruk-duplicatie: 'M004M004' → 'M004'."""
    if not s:
        return s
    h = len(s) // 2
    if len(s) >= 2 and len(s) % 2 == 0 and s[:h] == s[h:]:
        return s[:h]
    if len(s) >= 4 and len(s) % 2 == 0:
        half = ''.join(c for i, c in enumerate(s) if i % 2 == 0)
        if ''.join(c + c for c in half) == s:
            return half
    return s


def _extract_activity(text: str, name: str):
    """→ (bouts: int, totaal_uur: float)"""
    pat = rf'(?:^|\s){re.escape(name)}\s+(\d+)\s+(\d+h\s*\d+m)\s+(\d+h\s*\d+m)\s+([\d.]+)%'
    m = re.search(pat, text)
    return (int(m.group(1)), _hm(m.group(2))) if m else (0, 0.0)


def _page_date(text: str):
    """'Physical activity Tue 17-Mar-26' → date(2026, 3, 17)"""
    m = re.search(r'Physical activity\s+\w+\s+(\d{1,2})-([A-Za-z]{3})-(\d{2,4})', text, re.I)
    if not m:
        return None
    d, mo_str, y = int(m.group(1)), m.group(2)[:3].lower(), int(m.group(3))
    mo = MONTHS.get(mo_str)
    if mo is None:
        return None
    return date(y + 2000 if y < 100 else y, mo, d)


def parse_mcroberts_pdf(path: Path) -> dict:
    """
    Parseert McRoberts 'Physical activity overview' PDF.
    Retourneert dict: subject, visit, project, days (list of day-dicts).
    """
    try:
        import fitz
    except ImportError:
        raise ImportError(
            "PyMuPDF niet gevonden. Installeer met:  pip install pymupdf"
        )

    doc  = fitz.open(str(path))
    p1   = doc[0].get_text('text').replace('\n', ' ')

    def field(label):
        m = re.search(rf'{re.escape(label)}:\s+(\S+)', p1)
        return _debold(m.group(1)) if m else ''

    subject = field('Subject code')
    visit   = field('Visit')
    project = field('Project name')

    days = []
    for i in range(1, len(doc)):
        t = doc[i].get_text('text').replace('\n', ' ')
        pg_date = _page_date(t)
        if pg_date is None:
            continue

        acts = {k: _extract_activity(t, label) for k, label in ACTIVITIES}
        # acts[k] = (bouts, uren)

        wear_h = sum(v[1] for v in acts.values())
        if wear_h == 0:
            continue  # niet-gedragen dag (bv. weekend)

        m_steps = re.search(r'Steps\s+([\d,.]+)', t)
        steps   = int(re.sub(r'[,.]', '', m_steps.group(1).split()[0])) if m_steps else None

        days.append({
            'date':          pg_date,
            'walking_h':     acts['walking'][1],
            'stair_h':       acts['stair'][1],
            'cycling_h':     acts['cycling'][1],
            'standing_h':    acts['standing'][1],
            'shuffling_h':   acts['shuffling'][1],
            'sitting_h':     acts['sitting'][1],
            'lying_h':       acts['lying'][1],
            'lying_bouts':   acts['lying'][0],
            'wear_h':        wear_h,
            'steps':         steps,
        })

    doc.close()
    return {'subject': subject, 'visit': visit, 'project': project, 'days': days}


# ─────────────────────────────────────────────────────────
# TEF-PARSER  (Orthotimer)
# ─────────────────────────────────────────────────────────
def _xml_field(block: str, name: str) -> str:
    """DataContract XML: _x003C_Name_x003E_k__BackingField"""
    pat = rf'_x003C_{re.escape(name)}_x003E_k__BackingField[^>]*>(.*?)</'
    m   = re.search(pat, block, re.DOTALL)
    return m.group(1).strip() if m else ''


def parse_tef(path: Path) -> dict:
    """
    Parseert Orthotimer .tef (ZIP met XML-bestanden).
    Retourneert: serial, export_date, goal_h, days [{date, hours}],
                 sessions [{start, end, hours}]
    """
    with zipfile.ZipFile(str(path.with_suffix('.tef'))) as z:
        def read(name):
            return z.read(name).decode('utf-8', errors='replace') if name in z.namelist() else ''
        days_xml  = read('days.tyf')
        times_xml = read('times.ttf')
        chips_xml = read('chips.tdf')
        info_xml  = read('info_ng.tnf')
        rules_xml = read('rules.twf')

    serial      = _xml_field(chips_xml, 'Serial')
    export_date = _xml_field(info_xml,  'ExportDate')[:10]

    # Draagdoel uit rules.twf (General-regel)
    goal_h = 12.0
    for block in re.findall(r'<WearingRule\b[\s\S]*?</WearingRule>', rules_xml):
        if 'true' in _xml_field(block, 'General').lower():
            g = float(_xml_field(block, 'Hours') or '0')
            if g > 0:
                goal_h = g
            break

    # Dagelijkse draaguren (days.tyf)
    days = []
    for block in re.findall(r'<MeasureDay\b[\s\S]*?</MeasureDay>', days_xml):
        raw_date = _xml_field(block, 'MeasureDate')
        raw_h    = _xml_field(block, 'Hours')
        try:
            days.append({
                'date':  date.fromisoformat(raw_date[:10]),
                'hours': float(raw_h),
            })
        except (ValueError, TypeError):
            pass
    days.sort(key=lambda d: d['date'])

    # Sessies (times.ttf) — StartDate / EndDate
    sessions = []
    for block in re.findall(r'<MeasureTime\b[\s\S]*?</MeasureTime>', times_xml):
        if 'true' in _xml_field(block, 'Exclude').lower():
            continue
        try:
            start = datetime.fromisoformat(_xml_field(block, 'StartDate'))
            end   = datetime.fromisoformat(_xml_field(block, 'EndDate'))
            hours = (end - start).total_seconds() / 3600
            sessions.append({'start': start, 'end': end, 'hours': hours})
        except (ValueError, TypeError):
            pass

    return {
        'serial':      serial,
        'export_date': export_date,
        'goal_h':      goal_h,
        'days':        days,
        'sessions':    sessions,
    }


# ─────────────────────────────────────────────────────────
# ADHERENTIEBEREKENING
# ─────────────────────────────────────────────────────────
def sleep_estimate(lying_h: float, lying_bouts: int) -> float:
    """
    Langste aaneengesloten ligperiode (= slaap).
    = totale ligtijd − (bouts − 1) × MIN_LYING_BOUT
    """
    return max(0.0, lying_h - max(0, lying_bouts - 1) * MIN_LYING_BOUT)


def analyse(mcr: dict, tef: dict, pid: str) -> dict:
    """Koppelt McRoberts + Orthotimer per dag en berekent adherentiematen."""

    ortho_by_date = {d['date']: d['hours'] for d in tef['days']}

    valid, skipped = [], []

    for day in mcr['days']:
        d     = day['date']
        wear  = day['wear_h']

        # Geldigheidsfilter accelerometer
        if wear < WEAR_MIN_H:
            skipped.append((d, f'McRoberts draagtijd {wear:.1f}u < {WEAR_MIN_H}u'))
            continue

        # Orthotimer-data aanwezig?
        if d not in ortho_by_date:
            skipped.append((d, 'Geen Orthotimer-data voor deze datum'))
            continue

        ortho_h = ortho_by_date[d]

        # WB-tijd en OOB-tijd
        wb_h   = day['walking_h'] + day['standing_h'] + day['shuffling_h'] + day['stair_h']
        sleep  = sleep_estimate(day['lying_h'], day['lying_bouts'])
        oob_h  = max(0.0, wear - sleep)

        # Uren schoeisel begrenzen (kan max. gelijk zijn aan het window)
        ortho_oob = min(ortho_h, oob_h)
        ortho_wb  = min(ortho_h, wb_h)

        valid.append({
            'date':       d,
            'wear_h':     wear,
            'wb_h':       wb_h,
            'oob_h':      oob_h,
            'sleep_h':    sleep,
            'lying_h':    day['lying_h'],
            'lying_bouts':day['lying_bouts'],
            'ortho_h':    ortho_h,
            'ortho_oob':  ortho_oob,
            'ortho_wb':   ortho_wb,
            'steps':      day['steps'],
        })

    n = len(valid)
    out = {
        'pid':          pid,
        'subject':      mcr['subject'],
        'visit':        mcr['visit'],
        'n_valid':      n,
        'n_skipped':    len(skipped),
        'skipped':      skipped,
        'voldoende':    n >= MIN_VALID_DAYS,
    }

    if n < MIN_VALID_DAYS:
        return out

    # ── Gemiddelden
    avg_wb    = statistics.mean(d['wb_h']    for d in valid)
    avg_oob   = statistics.mean(d['oob_h']   for d in valid)
    avg_sleep = statistics.mean(d['sleep_h'] for d in valid)
    avg_ortho = statistics.mean(d['ortho_h'] for d in valid)

    # ── adh_OOB: per dag berekend, dan gemiddeld (Jarl et al.)
    adh_oob_days = [d['ortho_oob'] / d['oob_h'] for d in valid if d['oob_h'] > 0]
    adh_oob = statistics.mean(adh_oob_days) if adh_oob_days else None

    # ── adh_WB: benadering (uniform-verdeling-aanname)
    adh_wb_days = [d['ortho_wb'] / d['wb_h'] for d in valid if d['wb_h'] > 0]
    adh_wb = statistics.mean(adh_wb_days) if adh_wb_days else None

    # ── Orthotimer-doel = gem. OOB-tijd × 80 %
    doel_h = round(avg_oob * CUTOFF, 1)

    out.update({
        'avg_wb_h':    round(avg_wb,    2),
        'avg_oob_h':   round(avg_oob,   2),
        'avg_sleep_h': round(avg_sleep, 2),
        'avg_ortho_h': round(avg_ortho, 2),
        'adh_OOB':     round(adh_oob, 4) if adh_oob is not None else None,
        'adh_WB':      round(adh_wb,  4) if adh_wb  is not None else None,
        'hoog_OOB':    (adh_oob >= CUTOFF) if adh_oob is not None else None,
        'hoog_WB':     (adh_wb  >= CUTOFF) if adh_wb  is not None else None,
        'doel_h':      doel_h,
        'bestand_doel_h': round(tef['goal_h'], 1),
        'valid_days':  valid,
    })
    return out


# ─────────────────────────────────────────────────────────
# RAPPORTAGE
# ─────────────────────────────────────────────────────────
def _vlag(val, cutoff=CUTOFF):
    if val is None:
        return '—'
    sym = '✔ HOOG' if val >= cutoff else '✖ LAAG'
    return f'{val*100:.1f}%  [{sym}]'


def print_report(r: dict):
    print(f"\n{'═'*62}")
    print(f"  Deelnemer : {r['pid']}  (subject={r['subject']}, bezoek={r['visit']})")
    print(f"  Geldige dagen : {r['n_valid']}  |  Overgeslagen : {r['n_skipped']}")

    if not r['voldoende']:
        print(f"\n  ⚠  Onvoldoende geldige dagen (min. {MIN_VALID_DAYS}) — niet meegenomen.")
        for d, reason in r['skipped']:
            print(f"     {d}  –  {reason}")
        return

    print(f"\n  Gemiddelden per geldige dag:")
    print(f"    Gewichtsdragende tijd (WB)  : {r['avg_wb_h']:.2f} u")
    print(f"    Slaapperiode (schatting)     : {r['avg_sleep_h']:.2f} u")
    print(f"    Out-of-bed-tijd (OOB)        : {r['avg_oob_h']:.2f} u")
    print(f"    Orthotimer gedragen          : {r['avg_ortho_h']:.2f} u")

    print(f"\n  Adherentie:")
    print(f"    adh_OOB (primair)  = {_vlag(r['adh_OOB'])}")
    print(f"    adh_WB  (benaderd) = {_vlag(r['adh_WB'])}")
    print(f"    ⚑  adh_WB is een benadering (uniform-verdeling); epoch-data")
    print(f"       vereist voor exacte waarde per Jarl et al.")

    print(f"\n  {'─'*42}")
    print(f"  ▶▶  ORTHOTIMER-DOEL  :  {r['doel_h']} u/dag")
    print(f"      (= 80 % van gem. OOB-tijd {r['avg_oob_h']:.1f} u/dag)")
    print(f"      Huidig apparaatdoel : {r['bestand_doel_h']} u/dag")
    print(f"  {'─'*42}")

    if r['n_skipped']:
        print(f"\n  Overgeslagen dagen:")
        for d, reason in r['skipped']:
            print(f"    {d}  –  {reason}")


def print_group_summary(results: list):
    valid = [r for r in results if r['voldoende']]
    if not valid:
        print("\nGeen deelnemers met voldoende geldige dagen.")
        return

    print(f"\n{'═'*62}")
    print(f"  GROEPSOVERZICHT  –  {len(valid)} deelnemer(s)")

    oob_vals  = [r['adh_OOB']  for r in valid if r['adh_OOB']  is not None]
    wb_vals   = [r['adh_WB']   for r in valid if r['adh_WB']   is not None]
    doel_vals = [r['doel_h']   for r in valid]

    if oob_vals:
        print(f"    Gem. adh_OOB  : {statistics.mean(oob_vals)*100:.1f}%"
              f"  (SD {statistics.stdev(oob_vals)*100:.1f}%)" if len(oob_vals) > 1 else
              f"    Gem. adh_OOB  : {statistics.mean(oob_vals)*100:.1f}%")
    if wb_vals:
        print(f"    Gem. adh_WB   : {statistics.mean(wb_vals)*100:.1f}%  (benadering)")
    if doel_vals:
        print(f"    Gem. Orthotimer-doel : {statistics.mean(doel_vals):.1f} u/dag")
        print(f"    Bereik doel          : {min(doel_vals):.1f} – {max(doel_vals):.1f} u/dag")

    hoog_oob = sum(1 for r in valid if r['hoog_OOB'])
    print(f"    Hoog adherent (adh_OOB ≥ 80 %) : {hoog_oob}/{len(valid)}")


# ─────────────────────────────────────────────────────────
# BESTANDEN KOPPELEN
# ─────────────────────────────────────────────────────────
def find_pairs(folder: Path):
    """
    Zoekt PDF+TEF-paren in een map.
    Koppelstrategie (in volgorde):
      1. Zelfde deelmap
      2. Zelfde naamprefix (tot eerste '_' of spatie)
    """
    pdfs = list(folder.glob('**/*.pdf'))
    tefs = list(folder.glob('**/*.tef'))

    pairs = []
    for pdf in pdfs:
        match = None
        # 1. Zelfde map
        for tef in tefs:
            if tef.parent == pdf.parent:
                match = tef
                break
        # 2. Naamprefix
        if match is None:
            prefix = re.split(r'[_ ]', pdf.stem)[0].lower()
            for tef in tefs:
                if tef.stem.lower().startswith(prefix):
                    match = tef
                    break
        if match:
            pairs.append((pdf, match))
        else:
            print(f"[OVERGESLAGEN] Geen .tef gevonden voor: {pdf.name}")
    return pairs


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='PARADISE adherentieanalyse')
    parser.add_argument('--pdf', type=Path, help='McRoberts PDF')
    parser.add_argument('--tef', type=Path, help='Orthotimer .tef')
    parser.add_argument('--map', type=Path, default=Path('.'),
                        help='Map met PDF+TEF-paren (default: huidige map)')
    args = parser.parse_args()

    if args.pdf and args.tef:
        pairs = [(args.pdf, args.tef)]
    else:
        pairs = find_pairs(args.map)

    if not pairs:
        print("Geen PDF+TEF-paren gevonden.")
        return

    results = []
    for pdf_path, tef_path in pairs:
        print(f"\nVerwerken: {pdf_path.name}  +  {tef_path.name}")
        try:
            mcr = parse_mcroberts_pdf(pdf_path)
            tef = parse_tef(tef_path)
        except Exception as e:
            print(f"  ✖ Fout: {e}")
            continue

        pid    = mcr['subject'] or pdf_path.stem
        result = analyse(mcr, tef, pid)
        print_report(result)
        results.append(result)

    if len(results) > 1:
        print_group_summary(results)


if __name__ == '__main__':
    main()
