#!/usr/bin/env python3
import base64, json, math, re, shutil, subprocess, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); deep='--deep' in sys.argv
if deep and shutil.which('trufflehog'):
    r=subprocess.run('trufflehog filesystem . --json', cwd=p, shell=True, text=True, capture_output=True, timeout=180)
    print(r.stdout if r.stdout.strip() else json.dumps({'tool':'trufflehog','exit_code':r.returncode,'stderr':r.stderr[-2000:]})); raise SystemExit(0)
if deep and shutil.which('gitleaks'):
    r=subprocess.run('gitleaks detect --no-git --report-format json', cwd=p, shell=True, text=True, capture_output=True, timeout=180)
    print(r.stdout if r.stdout.strip() else json.dumps({'tool':'gitleaks','exit_code':r.returncode,'stderr':r.stderr[-2000:]})); raise SystemExit(0)
patterns=[r'(?i)\b(api[_-]?key|secret|token|password)\b\s*[:=]\s*["\'][A-Za-z0-9_./+=-]{12,}["\']',r'sk-[A-Za-z0-9_-]{20,}',r'AIza[0-9A-Za-z\-_]{20,}']
skip={'.git','node_modules','dist','build','.next','.venv','venv'}; findings=[]
def entropy(s):
    if not s: return 0
    from collections import Counter
    c=Counter(s); n=len(s)
    return -sum((v/n)*math.log2(v/n) for v in c.values())
for f in p.rglob('*'):
    if any(part in skip for part in f.parts) or not f.is_file() or f.stat().st_size>600000: continue
    txt=f.read_text(errors='ignore')
    for pat in patterns:
        for m in re.finditer(pat,txt,re.I): findings.append({'file':str(f.relative_to(p)),'line':txt[:m.start()].count('\n')+1,'kind':'pattern'})
    for m in re.finditer(r'[A-Za-z0-9_\-+/=]{32,}', txt):
        s=m.group(0)
        if entropy(s)>4.5: findings.append({'file':str(f.relative_to(p)),'line':txt[:m.start()].count('\n')+1,'kind':'high_entropy','length':len(s)})
print(json.dumps({'deep_requested':deep,'findings':findings[:200],'count':len(findings)}, indent=2))
