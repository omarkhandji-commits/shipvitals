#!/usr/bin/env python3
import json, subprocess, sys
from pathlib import Path
try:
    from shipvitals_config import load_config
except Exception:
    sys.path.append(str(Path(__file__).resolve().parent)); from shipvitals_config import load_config
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
cfg=load_config(p) or {}
commands=list((cfg.get('commands') or {}).values())
if not commands:
    pkg=p/'package.json'
    if pkg.exists():
        scripts=json.loads(pkg.read_text()).get('scripts',{})
        pm='pnpm' if (p/'pnpm-lock.yaml').exists() else 'yarn' if (p/'yarn.lock').exists() else 'bun' if (p/'bun.lockb').exists() else 'npm'
        commands=[f'{pm} run {s}' for s in ['typecheck','lint','test','build'] if s in scripts]
    if (p/'pyproject.toml').exists(): commands.append('python -m pytest')
results=[]
for c in commands:
    r=subprocess.run(c, cwd=p, shell=True, text=True, capture_output=True, timeout=120)
    results.append({'cmd':c,'exit_code':r.returncode,'stdout':r.stdout[-1000:],'stderr':r.stderr[-1000:]})
print(json.dumps({'commands':commands,'results':results,'monorepo':any((p/x).exists() for x in ['pnpm-workspace.yaml','turbo.json','lerna.json','nx.json'])}, indent=2))
sys.exit(1 if any(r['exit_code'] for r in results) else 0)
