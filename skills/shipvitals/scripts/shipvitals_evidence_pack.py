#!/usr/bin/env python3
import json, subprocess, sys, time, argparse
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('root', nargs='?', default='.')
parser.add_argument('--self-check', action='store_true')
args=parser.parse_args()
root=Path(args.root)
out=root/'.shipvitals-evidence'
out.mkdir(exist_ok=True)
manifest={'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'commands':[]}
commands=[
 ('probe','python3 skills/shipvitals/scripts/shipvitals_probe.py .'),
 ('gate','python3 skills/shipvitals/scripts/shipvitals_gate.py .'),
 ('secret_scan','python3 skills/shipvitals/scripts/shipvitals_secret_scan.py .'),
 ('link_check','python3 skills/shipvitals/scripts/shipvitals_link_check.py .')
]
if not args.self_check:
 commands.append(('falsification_scan','python3 skills/shipvitals/scripts/shipvitals_falsification_scan.py .'))
for name,cmd in commands:
 p=subprocess.run(cmd,cwd=root,shell=True,text=True,capture_output=True)
 (out/f'{name}.stdout.txt').write_text(p.stdout)
 (out/f'{name}.stderr.txt').write_text(p.stderr)
 manifest['commands'].append({'name':name,'cmd':cmd,'exit_code':p.returncode})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(out)
