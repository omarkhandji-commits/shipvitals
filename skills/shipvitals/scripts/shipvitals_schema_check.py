#!/usr/bin/env python3
from pathlib import Path
import json, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
for rel in ['schemas/evidence.schema.json','schemas/report.schema.json','evals/rubric.json','package.json']:
 json.loads((root/rel).read_text())
print('ShipVitals schema check: PASS')
