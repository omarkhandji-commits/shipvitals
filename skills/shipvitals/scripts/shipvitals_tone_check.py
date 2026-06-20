#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
# Terms that made earlier drafts sound like a launch thread instead of a tool.
def join(*parts):
    return ''.join(parts)

banned = [
    join('Publish', 'Vitals'), join('9', '9.9'), join('9', '9+'), join('9', '9-grade'),
    join('Su', 'preme'), join('Ulti', 'mate'), join('Ap', 'ex'),
    join('world', '-class'), join('best in ', 'the world'), join('10', 'x better'),
    join('guarantees ', 'a perfect release'), join('vi', 'be', '-coded'),
    join('vi', 'be ', 'coding'), join('vi', 'be ', 'coders'),
]
allowed_parts = {'LICENSE'}
findings = []
for p in root.rglob('*'):
    if not p.is_file() or p.name in allowed_parts or p.name == 'shipvitals_tone_check.py':
        continue
    if p.suffix.lower() not in {'.md', '.json', '.yml', '.yaml', '.py', '.txt', '.svg'}:
        continue
    if any(part in {'.git', 'node_modules', 'dist', 'build', '.next'} for part in p.parts):
        continue
    text = p.read_text(errors='ignore')
    for term in banned:
        if term in text:
            line = text[:text.find(term)].count('\n') + 1
            findings.append({'file': str(p.relative_to(root)), 'line': line, 'term': term})

if findings:
    print('ShipVitals tone check: FAIL')
    for f in findings[:80]:
        print(f"{f['file']}:{f['line']} contains {f['term']}")
    sys.exit(1)
print('ShipVitals tone check: PASS')
