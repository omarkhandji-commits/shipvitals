#!/usr/bin/env python3
"""Run the deterministic ShipVitals baseline and write an evidence pack."""
import json
import subprocess
import sys
import time
from pathlib import Path

skill_root = Path(__file__).resolve().parents[1]
target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
scripts = skill_root / 'scripts'
steps = [
    ('probe', ['python3', str(scripts / 'shipvitals_probe.py'), str(target)]),
    ('gate', ['python3', str(scripts / 'shipvitals_gate.py'), str(target)]),
    ('secret_scan', ['python3', str(scripts / 'shipvitals_secret_scan.py'), str(target)]),
    ('falsification_scan', ['python3', str(scripts / 'shipvitals_falsification_scan.py'), str(target)]),
    ('link_check', ['python3', str(scripts / 'shipvitals_link_check.py'), str(target)]),
]
results = []
for name, cmd in steps:
    p = subprocess.run(cmd, text=True, capture_output=True)
    results.append({'step': name, 'returncode': p.returncode, 'stdout': p.stdout[-4000:], 'stderr': p.stderr[-4000:]})
out = target / '.shipvitals-evidence'
out.mkdir(exist_ok=True)
report = out / 'baseline-run.json'
report.write_text(json.dumps({'target': str(target), 'timestamp': time.time(), 'results': results}, indent=2))
print(f'ShipVitals runner complete: {report}')
sys.exit(1 if any(r['returncode'] != 0 and r['step'] in ['gate', 'secret_scan'] for r in results) else 0)
