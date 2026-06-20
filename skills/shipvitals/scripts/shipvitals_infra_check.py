#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); findings=[]
for f in list(p.rglob('*.tf'))[:200]:
    txt=f.read_text(errors='ignore')
    if re.search(r'(?i)(secret|password|token)\s*=', txt): findings.append(str(f.relative_to(p)))
print(json.dumps({'terraform_files':len(list(p.rglob('*.tf'))),'secret_like_files':findings}, indent=2))
