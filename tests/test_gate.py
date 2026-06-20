import json, subprocess, sys
from pathlib import Path

def test_gate_runs_configured_commands():
    repo=Path(__file__).parents[1]
    root=Path(__file__).parent/'fixtures'/'mock-nextjs'
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_gate.py',str(root)], cwd=repo, text=True, capture_output=True)
    assert r.returncode==0
    assert 'echo build ok' in r.stdout
