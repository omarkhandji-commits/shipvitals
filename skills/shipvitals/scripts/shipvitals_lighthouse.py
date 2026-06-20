#!/usr/bin/env python3
import json, shutil, subprocess, sys
url=sys.argv[1] if len(sys.argv)>1 else 'http://localhost:3000'
if not shutil.which('npx'):
    print(json.dumps({'available':False,'note':'npx not available'})); raise SystemExit(0)
r=subprocess.run(f'npx lighthouse {url} --output=json --quiet --chrome-flags="--headless"', shell=True, text=True, capture_output=True, timeout=180)
print(r.stdout if r.stdout.strip() else json.dumps({'exit_code':r.returncode,'stderr':r.stderr[-2000:]}))
