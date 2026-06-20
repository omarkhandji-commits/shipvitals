import json, subprocess, sys
from pathlib import Path

def test_probe_detects_node_project():
    root=Path(__file__).parent/'fixtures'/'mock-nextjs'
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_probe.py',str(root)], cwd=Path(__file__).parents[1], text=True, capture_output=True)
    assert r.returncode==0
    data=json.loads(r.stdout)
    assert 'javascript/typescript' in data['stack']
