#!/usr/bin/env python3
import json, sys, shutil
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
out=root/'.shipvitals-golden-benchmark'
if out.exists(): shutil.rmtree(out)
out.mkdir()
cases={
 'ai-saas-dashboard':['TODO fix billing','const API_KEY="sk-demo-fake"','test.skip("payment works")','placeholder pricing'],
 'shopify-app':['missing privacy URL','fake billing integration','demo merchant data','mobile overflow'],
 'api-cli':['catch(e){}','sample token committed','no rate limit','README missing install'],
 'landing-page':['href="#"','generic generated copy','no support email','broken mobile CTA'],
 'browser-extension':['permissions: ["<all_urls>"]','no privacy disclosure','fake onboarding complete','console errors']
}
manifest=[]
for name, defects in cases.items():
 d=out/name; d.mkdir()
 (d/'README.md').write_text('# '+name+'\n\nThis is a synthetic flawed benchmark project.\n')
 (d/'defects.txt').write_text('\n'.join(defects)+'\n')
 manifest.append({'case':name,'expected_blockers':defects})
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'benchmark_dir':str(out),'cases':len(cases)},indent=2))
