#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
p=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
skip={'.git','node_modules','dist','build','.next','.venv','venv'}
patterns=[('TODO','todo'),('FIXME','fixme'),('placeholder','placeholder'),('demo only','demo_only'),('mock data','mock_data'),('.skip(','skipped_test'),('catch_empty','silent_failure')]
findings=[]
for f in p.rglob('*'):
    if any(part in skip for part in f.parts) or not f.is_file() or f.stat().st_size>600000: continue
    txt=f.read_text(errors='ignore')
    for token,kind in patterns:
        if kind=='silent_failure': matches=list(re.finditer(r'catch\s*\([^)]*\)\s*\{\s*\}', txt, re.I|re.S))
        else: matches=list(re.finditer(re.escape(token), txt, re.I))
        for m in matches:
            rel=str(f.relative_to(p)); context='test' if any(x in rel.lower() for x in ['test','spec','fixture','mock']) else 'production'
            severity='P2' if context=='test' else 'P1'
            if kind in ['demo_only','mock_data'] and context=='production': severity='P0'
            findings.append({'file':rel,'line':txt[:m.start()].count('\n')+1,'kind':kind,'context':context,'severity':severity})
print(json.dumps({'findings':findings[:300],'count':len(findings)}, indent=2))
