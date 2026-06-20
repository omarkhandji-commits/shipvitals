#!/usr/bin/env python3
import json, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); f=p/'Dockerfile'
findings=[]
if f.exists():
    txt=f.read_text(errors='ignore')
    if ':latest' in txt: findings.append('Avoid latest tags in production images.')
    if 'USER ' not in txt: findings.append('No non-root USER directive found.')
    if 'COPY . .' in txt: findings.append('COPY . . can include unnecessary files without .dockerignore.')
print(json.dumps({'dockerfile':f.exists(),'findings':findings}, indent=2))
