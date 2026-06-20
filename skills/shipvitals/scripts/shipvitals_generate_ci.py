#!/usr/bin/env python3
"""Generate a drop-in GitHub Actions workflow for a target project.
The workflow runs the ShipVitals baseline gate plus common project commands when available.
"""
from pathlib import Path
import sys, textwrap
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
out=root/'.github'/'workflows'
out.mkdir(parents=True, exist_ok=True)
workflow=out/'shipvitals-gate.yml'
workflow.write_text(textwrap.dedent('''
name: ShipVitals Gate

on:
 pull_request:
 push:
 branches: [ main, master ]

jobs:
 shipvitals:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v4
 - uses: actions/setup-node@v4
 with:
 node-version: '20'
 - uses: actions/setup-python@v5
 with:
 python-version: '3.11'
 - name: Install JS dependencies when present
 run: |
 if [ -f package-lock.json ]; then npm ci; elif [ -f package.json ]; then npm install; fi
 - name: Run common project checks when present
 run: |
 if [ -f package.json ]; then npm run lint --if-present; npm run typecheck --if-present; npm test --if-present; npm run build --if-present; fi
 - name: ShipVitals baseline scans
 run: |
 python3 skills/shipvitals/scripts/shipvitals_secret_scan.py . || true
 python3 skills/shipvitals/scripts/shipvitals_falsification_scan.py . || true
 python3 skills/shipvitals/scripts/shipvitals_link_check.py . || true
 - name: Upload evidence
 uses: actions/upload-artifact@v4
 if: always()
 with:
 name: shipvitals-evidence
 path: .shipvitals-evidence/
''').strip()+"\n")
print(f'Generated {workflow}')
