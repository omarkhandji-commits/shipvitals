import json, subprocess, sys
from pathlib import Path

def test_falsification_scan_finds_demo_signal():
    repo=Path(__file__).parents[1]
    root=Path(__file__).parent/'fixtures'/'mock-fake'
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_falsification_scan.py',str(root)], cwd=repo, text=True, capture_output=True)
    assert r.returncode==0
    assert json.loads(r.stdout)['count'] >= 1
