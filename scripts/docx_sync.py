#!/usr/bin/env python3
"""
DOCX -> TXT auto-sync watcher for 'Report Summary' folder.

- Scans for all .docx files and generates/updates matching .txt files
- Watches for changes and re-syncs automatically
- Also maintains canonical "latest" TXT per vessel in: Report Summary/latest/<vessel-slug>.txt
  so the website can always load the most recent summary by vessel name.
- No external dependencies required (uses only Python standard library)

Usage:
  python scripts/docx_sync.py

Notes:
- Ignores temporary Word lock files that start with '~$'
- Writes .txt next to the .docx with the same base name
- Only rewrites .txt if extracted text actually changed (to avoid churn)
- File naming expected like: "Monthly Vessel Operational Summary_ Genie Lab - December 2025.docx"
"""
import time
import zipfile
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

# WordprocessingML namespace
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

MONTHS = {m: i for i, m in enumerate([
    '', 'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])}

NAME_PATTERN = re.compile(
    r'^Monthly Vessel Operational Summary_\s*(?P<vessel>.+?)\s*-\s*(?P<month>[A-Za-z]+)\s+(?P<year>\d{4})\.docx$',
    re.IGNORECASE
)


def extract_text_from_docx(docx_path: Path) -> str:
    """Extract plain text from a .docx file preserving paragraph breaks.
    This reads word/document.xml and collects text from w:t, inserting tabs for w:tab
    and line breaks for w:br. Paragraphs are separated by a blank line.
    """
    with zipfile.ZipFile(docx_path) as z:
        with z.open('word/document.xml') as f:
            tree = ET.parse(f)
    root = tree.getroot()

    # Collect paragraphs
    paragraphs = []
    for p in root.findall('.//%sbody/%sp' % (W, W)):
        parts = []
        for node in p.iter():
            tag = node.tag
            if tag == f'{W}t':
                parts.append(node.text or '')
            elif tag == f'{W}tab':
                parts.append('\t')
            elif tag == f'{W}br':
                parts.append('\n')
        paragraph_text = ''.join(parts).strip()
        paragraphs.append(paragraph_text)

    text = '\n\n'.join(paragraphs).rstrip() + '\n'
    return text


def slugify(name: str) -> str:
    return re.sub(r'-{2,}', '-', re.sub(r'[^a-z0-9]+', '-', name.lower())).strip('-')


def parse_vessel_and_date(docx_path: Path) -> Tuple[str, int]:
    """Return (vessel_slug, yyyymm) parsed from the filename.
    Raises ValueError if filename doesn't match expected pattern.
    """
    m = NAME_PATTERN.match(docx_path.name)
    if not m:
        raise ValueError('Unrecognized filename format')
    vessel = m.group('vessel').strip()
    month_name = m.group('month').capitalize()
    year = int(m.group('year'))
    month_num = MONTHS.get(month_name)
    if not month_num:
        raise ValueError('Unknown month')
    return slugify(vessel), year * 100 + month_num


def compute_latest_map(report_dir: Path) -> Dict[str, Path]:
    """Build a map of vessel_slug -> Path to latest .docx (by Year/Month)."""
    latest: Dict[str, Tuple[int, Path]] = {}
    for docx in report_dir.glob('*.docx'):
        if docx.name.startswith('~$'):
            continue
        try:
            vessel_slug, yyyymm = parse_vessel_and_date(docx)
        except Exception:
            continue
        cur = latest.get(vessel_slug)
        if cur is None or yyyymm > cur[0]:
            latest[vessel_slug] = (yyyymm, docx)
    return {slug: path for slug, (_, path) in latest.items()}


def update_latest_outputs(report_dir: Path) -> None:
    """Write/refresh canonical latest text files under Report Summary/latest/"""
    latest_dir = report_dir / 'latest'
    latest_dir.mkdir(parents=True, exist_ok=True)

    latest_map = compute_latest_map(report_dir)
    for slug, docx_path in latest_map.items():
        txt_out = latest_dir / f'{slug}.txt'
        try:
            text = extract_text_from_docx(docx_path)
        except Exception as e:
            print(f"[ERROR] Latest extraction failed for {docx_path.name}: {e}")
            continue

        # Only write if changed
        old_text = None
        if txt_out.exists():
            try:
                old_text = txt_out.read_text(encoding='utf-8')
            except Exception:
                old_text = None
        if text != old_text:
            try:
                txt_out.write_text(text, encoding='utf-8')
                print(f"[LATEST] Updated: latest/{slug}.txt -> {docx_path.name}")
            except Exception as e:
                print(f"[ERROR] Failed writing latest/{slug}.txt: {e}")


def sync_docx(docx_path: Path) -> None:
    txt_path = docx_path.with_suffix('.txt')
    try:
        new_text = extract_text_from_docx(docx_path)
    except Exception as e:
        print(f"[ERROR] Failed to extract text from {docx_path.name}: {e}")
        return

    old_text = None
    if txt_path.exists():
        try:
            old_text = txt_path.read_text(encoding='utf-8')
        except Exception:
            old_text = None

    if new_text != old_text:
        try:
            txt_path.write_text(new_text, encoding='utf-8')
            print(f"[SYNC] Wrote: {txt_path.name}")
        except Exception as e:
            print(f"[ERROR] Failed to write {txt_path.name}: {e}")
    else:
        print(f"[OK] No changes: {txt_path.name}")


def initial_scan(report_dir: Path) -> Dict[Path, float]:
    mtimes: Dict[Path, float] = {}
    for docx in sorted(report_dir.glob('*.docx')):
        if docx.name.startswith('~$'):
            continue  # ignore Word temp files
        sync_docx(docx)
        try:
            mtimes[docx] = docx.stat().st_mtime
        except FileNotFoundError:
            pass
    # After basic syncs, refresh latest outputs
    update_latest_outputs(report_dir)
    return mtimes


def watch(report_dir: Path, interval: float = 2.0) -> None:
    print(f"Watching: {report_dir}")
    mtimes = initial_scan(report_dir)
    print("Ready. Monitoring for changes... (Ctrl+C to stop)")

    while True:
        time.sleep(interval)
        changed = False
        # Track current files
        current = set()
        for docx in report_dir.glob('*.docx'):
            if docx.name.startswith('~$'):
                continue
            current.add(docx)
            try:
                m = docx.stat().st_mtime
            except FileNotFoundError:
                continue
            last = mtimes.get(docx)
            if last is None or m > last:
                sync_docx(docx)
                mtimes[docx] = m
                changed = True
        # Handle deletions
        removed = set(mtimes.keys()) - current
        for path in removed:
            print(f"[INFO] .docx removed: {path.name}")
            mtimes.pop(path, None)
            changed = True
        if changed:
            update_latest_outputs(report_dir)


if __name__ == '__main__':
    # Resolve 'Report Summary' directory relative to repo root
    repo_root = Path(__file__).resolve().parents[1]
    report_dir = repo_root / 'Report Summary'
    report_dir.mkdir(parents=True, exist_ok=True)

    try:
        watch(report_dir)
    except KeyboardInterrupt:
        print('\nStopped watcher.')
