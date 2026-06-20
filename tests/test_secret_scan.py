import json, subprocess, sys
from pathlib import Path

def test_secret_scan_finds_candidate():
    repo=Path(__file__).parents[1]
    root=Path(__file__).parent/'fixtures'/'mock-secret'
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_secret_scan.py',str(root)], cwd=repo, text=True, capture_output=True)
    assert r.returncode==0
    assert json.loads(r.stdout)['count'] >= 1

def test_secret_scan_ignores_password_label_example(tmp_path):
    repo=Path(__file__).parents[1]
    (tmp_path/'README.md').write_text("console.log('password:', password);\n")
    r=subprocess.run([sys.executable,'skills/shipvitals/scripts/shipvitals_secret_scan.py',str(tmp_path)], cwd=repo, text=True, capture_output=True)
    assert r.returncode==0
    assert json.loads(r.stdout)['count'] == 0
