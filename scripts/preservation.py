#!/usr/bin/env python3
"""Inventory baseline rules/examples and reconcile them with the shipped corpus."""

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('plugins/shopware-knowledge/skills/shopware-development')
BASELINE = ROOT / 'docs/maintenance/preservation-baseline.json'
DECISIONS = ROOT / 'docs/maintenance/preservation-decisions.json'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True)


def units(content):
    lines = content.splitlines()
    heading = 'Frontmatter'
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.startswith('#'):
            heading = line.lstrip('# ').strip()
            index += 1
            continue
        start = index
        if line.startswith('```'):
            index += 1
            while index < len(lines) and not lines[index].startswith('```'):
                index += 1
            index = min(index + 1, len(lines))
            kind = 'example'
        elif start == 0 and line == '---':
            index += 1
            while index < len(lines) and lines[index] != '---':
                index += 1
            index = min(index + 1, len(lines))
            kind = 'metadata'
        else:
            index += 1
            while index < len(lines) and lines[index].strip() and not re.match(r'^(#|```|\s*[-*] |\s*\d+\. )', lines[index]):
                index += 1
            kind = 'rule'
        yield start + 1, heading, kind, '\n'.join(lines[start:index])


def normalize(value):
    return ' '.join(value.split())


def capture(ref):
    paths = git('ls-tree', '-r', '--name-only', ref).splitlines()
    paths = [p for p in paths if p.startswith('shopware-development/') and p.endswith('.md') or p == 'integrations/coderabbit/shopware-review.md']
    records = []
    for path in paths:
        for number, (line, heading, kind, body) in enumerate(units(git('show', f'{ref}:{path}')), 1):
            records.append(dict(id=f'{Path(path).stem}:{number:03d}', source=path, line=line,
                                heading=heading, kind=kind, sha256=hashlib.sha256(body.encode()).hexdigest()))
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(json.dumps(dict(commit=ref, records=records), indent=2) + '\n')
    print(f'Captured {len(records)} rules, paragraphs, metadata blocks, and examples from {len(paths)} files')


def reconcile():
    baseline = json.loads(BASELINE.read_text())
    decisions = json.loads(DECISIONS.read_text())
    paths = sorted((ROOT / SKILL).rglob('*.md')) + [ROOT / 'integrations/coderabbit/shopware-review.md']
    corpus = {str(p.relative_to(ROOT)): normalize(p.read_text()) for p in paths}
    old = {}
    rows = []
    pending = []
    totals = {}
    for record in baseline['records']:
        source = record['source']
        if source not in old:
            old[source] = {line: text for line, _, _, text in units(git('show', f'{baseline["commit"]}:{source}'))}
        body = normalize(old[source][record['line']])
        matches = [p for p, text in corpus.items() if body in text]
        natural = str(SKILL / Path(source).relative_to('shopware-development')) if source.startswith('shopware-development/') else source
        if matches:
            destination = natural if natural in matches else matches[0]
            status = 'retained' if destination == natural else 'moved'
            reason = 'Normalized content preserved.'
        else:
            found = [d for d in decisions if d.get('source') == source and
                     ('heading' not in d or d['heading'] == record['heading']) and
                     ('ids' not in d or record['id'] in d['ids'])]
            if len(found) != 1:
                pending.append({**record, 'text': old[source][record['line']], 'decision_matches': len(found)})
                continue
            choice = found[0]
            status, destination, reason = choice['status'], choice['destination'], choice['reason']
            if status not in ('corrected', 'retired', 'moved') or not (ROOT / destination).is_file():
                raise ValueError(f'Invalid disposition: {record["id"]}')
        totals[status] = totals.get(status, 0) + 1
        rows.append(f'| `{record["id"]}` | `{source}:{record["line"]}` | {record["kind"]} | {status} | `{destination}` | {reason} |')
    if pending:
        print(json.dumps(pending, indent=2))
        raise SystemExit(f'{len(pending)} baseline units need an explicit disposition')
    report = '# Preservation Ledger\n\nMaintainer audit; excluded from the installable skill.\n\n'
    report += f'Baseline after integrating PRs #2, #3, and #4: `{baseline["commit"]}`.\n\n'
    report += ', '.join(f'{k}: {v}' for k, v in sorted(totals.items())) + f'. Total: {len(rows)}.\n\n'
    report += '| ID | Baseline location | Kind | Disposition | Destination | Reason |\n| --- | --- | --- | --- | --- | --- |\n'
    (ROOT / 'docs/maintenance/preservation-ledger.md').write_text(report + '\n'.join(rows) + '\n')
    print(json.dumps(totals, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--capture')
    args = parser.parse_args()
    capture(args.capture) if args.capture else reconcile()
