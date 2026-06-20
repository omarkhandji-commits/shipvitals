#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
if not (p/'.git').exists():
    print(json.dumps({'git':False})); raise SystemExit(0)
r=subprocess.run('git log --oneline -n 20', cwd=p, shell=True, text=True, capture_output=True)
print(json.dumps({'git':True,'recent_commits':r.stdout.splitlines()[:20]}, indent=2))
