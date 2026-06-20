#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
findings = []
ignore = {'.git', 'node_modules', 'dist', 'build', '.next', '.shipvitals-evidence'}

for p in list(root.rglob('*.md')) + list(root.rglob('*.html')):
    if any(part in ignore for part in p.parts):
        continue
    txt = p.read_text(errors='ignore')
    for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)|(?:href|src)=["\']([^"\']+)', txt):
        url = (m.group(1) or m.group(2) or '').split('#')[0]
        if not url or re.match(r'https?://|mailto:|tel:|#|javascript:', url):
            continue
        target = (p.parent / url).resolve()
        if not target.exists():
            findings.append({'file': str(p.relative_to(root)), 'line': txt[:m.start()].count('\n') + 1, 'missing': url})

print(json.dumps({'count': len(findings), 'findings': findings}, indent=2))
sys.exit(1 if findings else 0)
