import json, subprocess, sys
from pathlib import Path

def test_full_audit_writes_report():
    repo=Path(__file__).parents[2]
    root=Path(__file__).parents[1]/'fixtures'/'mock-nextjs'
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_runner.py',str(root),'--ci','--no-fail'], cwd=repo, text=True, capture_output=True)
    assert r.returncode==0
    data=json.loads(r.stdout)
    assert data['verdict'] in ['ALMOST READY','READY']
    assert (root/'.shipvitals-evidence'/'report.json').exists()
