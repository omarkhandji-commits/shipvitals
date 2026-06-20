#!/usr/bin/env python3
import json, shutil, subprocess, sys
from pathlib import Path
project=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
spec=project/'.shipvitals-evidence'/'shipvitals.spec.ts'
result={'available': bool(shutil.which('npx')), 'spec': str(spec), 'exit_code': None, 'note': ''}
if not spec.exists():
    result['note']='No generated Playwright spec found. Run shipvitals_generate_playwright_gate.py first.'
elif not result['available']:
    result['note']='npx not available.'
else:
    r=subprocess.run(f'npx playwright test {spec}', cwd=project, shell=True, text=True, capture_output=True, timeout=180)
    result.update({'exit_code':r.returncode,'stdout':r.stdout[-2000:],'stderr':r.stderr[-2000:]})
print(json.dumps(result, indent=2))
