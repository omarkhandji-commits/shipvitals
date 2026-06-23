import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def manifest(root, kind, artifact):
    artifact_path = root / artifact
    path = root / f'{kind}.shipvitals-evidence.json'
    path.write_text(json.dumps({
        'shipvitals_evidence': 1,
        'kind': kind,
        'observed_at': '2026-06-22T12:00:00Z',
        'source': 'pytest',
        'summary': 'The required release flow was observed in the integration fixture.',
        'artifacts': [{'path': artifact, 'sha256': hashlib.sha256(artifact_path.read_bytes()).hexdigest()}],
    }), encoding='utf-8')
    return path


def test_full_audit_can_return_ready_with_required_proof(tmp_path):
    repo = Path(__file__).parents[2]
    source = Path(__file__).parents[1] / 'fixtures' / 'mock-nextjs'
    root = tmp_path / 'mock-nextjs'
    shutil.copytree(source, root)
    (root / 'runtime.json').write_text(json.dumps({'shipvitals_runtime': 1, 'exit_code': 0, 'observations': ['dashboard observed']}), encoding='utf-8')
    (root / 'visual.png').write_bytes(b'\x89PNG\r\n\x1a\nfixture')
    runtime_proof = manifest(root, 'runtime', 'runtime.json')
    visual_proof = manifest(root, 'visual', 'visual.png')
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