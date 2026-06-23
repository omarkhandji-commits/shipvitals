import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
RUNNER = ROOT / 'skills/shipvitals/scripts/shipvitals_runner.py'


def write_evidence(project, kind, artifact='runtime.txt'):
    artifact_path = project / artifact
    manifest = {
        'shipvitals_evidence': 1,
        'kind': kind,
        'observed_at': '2026-06-22T12:00:00Z',
        'source': 'pytest',
        'summary': 'Deterministic fixture evidence observed by the Python integration test.',
        'artifacts': [{'path': artifact, 'sha256': hashlib.sha256(artifact_path.read_bytes()).hexdigest()}],
    }
    path = project / f'{kind}.shipvitals-evidence.json'
    path.write_text(json.dumps(manifest), encoding='utf-8')
    return path


def write_project(project, destination='internal use', command=None):
    (project / 'src').mkdir(parents=True)
    (project / 'src/index.py').write_text('value = True\n', encoding='utf-8')
    config = {
        'project': {
            'name': 'fixture',
            'type': 'cli',
            'audience': 'developers',
            'destination': destination,
            'promise': 'Exercise the release gate.',
            'critical_flows': ['command'],
        },
        'commands': {'check': command or f'"{sys.executable}" -c "print(1)"'},
        'evidence': {},
        'exclude': [],
    }
    (project / '.shipvitals-config.json').write_text(json.dumps(config), encoding='utf-8')
    (project / 'runtime.txt').write_text('runtime artifact', encoding='utf-8')
    (project / 'package.json').write_text('{}', encoding='utf-8')
    write_evidence(project, 'runtime')


def run(project, *args):
    result = subprocess.run(
        [sys.executable, str(RUNNER), str(project), '--ci', '--no-fail', *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_python_runner_treats_timeout_as_failure(tmp_path):
    write_project(tmp_path, command=f'"{sys.executable}" -c "import time; time.sleep(2)"')
    report = run(tmp_path, '--timeout', '1', '--runtime-proof', str(tmp_path / 'runtime.shipvitals-evidence.json'))
    assert report['verdict'] == 'ALMOST READY'
    assert report['p1'] == ['One or more project commands failed.']
    assert 'L2_DETERMINISTIC' not in report['evidence_levels']


def test_python_runner_retains_distinct_blocker_after_core_saturation(tmp_path):
    write_project(tmp_path)
    (tmp_path / 'src/a-noise.py').write_text('# TODO\n' * 350, encoding='utf-8')
    (tmp_path / 'src/z-blocker.py').write_text('value = "mock data"\n', encoding='utf-8')
    report = run(tmp_path, '--runtime-proof', str(tmp_path / 'runtime.shipvitals-evidence.json'))
    assert report['verdict'] == 'DEMO ONLY'
    assert report['scan_stats']['fake_priority_count'] > 300
    assert any(item['file'].replace('\\', '/') == 'src/z-blocker.py' for item in report['blocking_fake_completion_candidates'])


def test_python_runner_rejects_existing_arbitrary_files_as_proof(tmp_path):
    write_project(tmp_path, destination='public release')
    report = run(
        tmp_path,
        '--runtime-proof', str(tmp_path / 'package.json'),
        '--visual-proof', str(tmp_path / 'package.json'),
        '--ci-proof', str(tmp_path / 'package.json'),
        '--independent-review', str(tmp_path / 'package.json'),
    )
    assert report['verdict'] == 'ALMOST READY'
    assert report['rejected_proof']['runtime'] == [str(tmp_path / 'package.json')]
    for level in ('L3_RUNTIME', 'L4_VISUAL_FLOW', 'L5_CI_REPRODUCIBLE', 'L6_INDEPENDENT'):
        assert level not in report['evidence_levels']


def test_python_runner_exits_nonzero_on_blocking_verdict(tmp_path):
    write_project(tmp_path)
    (tmp_path / 'src/index.py').write_text('token = "sk-abcdefghijklmnopqrstuvwxyz"\n', encoding='utf-8')
    result = subprocess.run(
        [sys.executable, str(RUNNER), str(tmp_path), '--ci', '--runtime-proof', str(tmp_path / 'runtime.shipvitals-evidence.json')],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)['verdict'] == 'NOT READY'