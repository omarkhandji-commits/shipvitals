import json
import subprocess
import sys
from pathlib import Path


def test_full_audit_can_return_ready_with_required_proof(tmp_path):
    repo = Path(__file__).parents[2]
    root = Path(__file__).parents[1] / 'fixtures' / 'mock-nextjs'
    runtime_proof = tmp_path / 'runtime.txt'
    visual_proof = tmp_path / 'visual.png'
    runtime_proof.write_text('dashboard observed', encoding='utf-8')
    visual_proof.write_bytes(b'visual-proof')
    result = subprocess.run(
        [
            sys.executable,
            'skills/shipvitals/scripts/shipvitals_runner.py',
            str(root),
            '--ci',
            '--runtime-proof',
            str(runtime_proof),
            '--visual-proof',
            str(visual_proof),
        ],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data['verdict'] == 'READY'
    assert data['score'] == 100
    assert data['not_verified'] == ['independent review']
