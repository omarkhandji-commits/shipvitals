#!/usr/bin/env python3
import json, html, sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
evidence_dir=root/'.shipvitals-evidence'
evidence=evidence_dir/'report.json'
if not evidence.exists():
 evidence=evidence_dir/'shipvitals-report.json'
out=root/'.shipvitals-evidence'/'shipvitals-html-report.html'
out.parent.mkdir(exist_ok=True)
if evidence.exists():
 data=json.loads(evidence.read_text())
else:
 data={'verdict':'NOT VERIFIED','score':0,'findings':[],'evidence':[],'note':'No evidence JSON found.'}
findings=data.get('findings',[])
items=''.join(f"<li><strong>{html.escape(str(f.get('severity','')))}</strong> {html.escape(str(f.get('title',f)))}</li>" for f in findings)
page=f"""<!doctype html><html><head><meta charset='utf-8'><title>ShipVitals Report</title><style>body{{font-family:system-ui;max-width:900px;margin:40px auto;line-height:1.5}}.verdict{{font-size:32px;font-weight:800}}code{{background:#f3f3f3;padding:2px 4px}}</style></head><body><div class='verdict'>{html.escape(str(data.get('verdict')))}</div><p>Score: <strong>{html.escape(str(data.get('score')))}</strong></p><h2>Findings</h2><ul>{items}</ul><h2>Raw Evidence</h2><pre>{html.escape(json.dumps(data,indent=2))}</pre></body></html>"""
out.write_text(page)
print(str(out))
