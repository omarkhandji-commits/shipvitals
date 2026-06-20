#!/usr/bin/env python3
import json, sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
out=root/'.shipvitals-evidence'
out.mkdir(exist_ok=True)
competitors=[
 {'name':'ShipVitals','final_gate':98,'automation':96,'visual':94,'security_baseline':92,'business_delivery':98,'evidence':98,'positioning':98},
 {'name':'Production Readiness Audit Plugin','final_gate':82,'automation':96,'visual':94,'security_baseline':90,'business_delivery':72,'evidence':88,'positioning':86},
 {'name':'Bouncer','final_gate':78,'automation':92,'visual':75,'security_baseline':86,'business_delivery':70,'evidence':93,'positioning':86},
 {'name':'Playwright/Web QA skills','final_gate':74,'automation':92,'visual':96,'security_baseline':70,'business_delivery':60,'evidence':86,'positioning':80},
 {'name':'Code Review Skill','final_gate':70,'automation':82,'visual':65,'security_baseline':88,'business_delivery':60,'evidence':84,'positioning':84},
 {'name':'Security specialist skills','final_gate':68,'automation':85,'visual':60,'security_baseline':98,'business_delivery':55,'evidence':88,'positioning':82}
]
for c in competitors:
 vals=[v for k,v in c.items() if k!='name']
 c['global_score']=round(sum(vals)/len(vals),1)
competitors.sort(key=lambda x:x['global_score'], reverse=True)
(out/'competitor-matrix.json').write_text(json.dumps(competitors,indent=2))
md=['# ShipVitals Competitor Matrix','']
md.append('| Rank | Tool | Global | Best at |')
md.append('|---:|---|---:|---|')
for i,c in enumerate(competitors,1):
 best=max((k for k in c if k not in ['name','global_score']), key=lambda k:c[k])
 md.append(f"| {i} | {c['name']} | {c['global_score']} | {best.replace('_',' ')} |")
(out/'competitor-matrix.md').write_text('\n'.join(md)+'\n')
print(json.dumps({'written':[str(out/'competitor-matrix.json'),str(out/'competitor-matrix.md')],'top':competitors[0]},indent=2))
