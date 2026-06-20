#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
cmd=None
if (p/'package-lock.json').exists() or (p/'package.json').exists(): cmd='npm audit --json'
elif (p/'pyproject.toml').exists(): cmd='python -m pip-audit --format json'
if not cmd:
    print(json.dumps({'available':False,'note':'No supported dependency manifest found'})); raise SystemExit(0)
r=subprocess.run(cmd, cwd=p, shell=True, text=True, capture_output=True, timeout=120)
print(r.stdout if r.stdout.strip() else json.dumps({'exit_code':r.returncode,'stderr':r.stderr[-2000:]}))
