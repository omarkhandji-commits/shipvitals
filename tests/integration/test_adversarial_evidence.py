import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[2]
RUNNER = ROOT / 'skills/shipvitals/scripts/shipvitals_runner.py'


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


def run(project, *args):
    result = subprocess.run(
        [sys.executable, str(RUNNER), str(project), '--ci', *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_python_runner_treats_timeout_as_failure(tmp_path):
    write_project(tmp_path, command=f'"{sys.executable}" -c "import time; time.sleep(2)"')
    report = run(tmp_path, '--timeout', '1', '--runtime-proof', str(tmp_path / 'runtime.txt'))
    assert report['verdict'] == 'ALMOST READY'
    assert report['p1'] == ['One or more project commands failed.']
    assert 'L2_DETERMINISTIC' not in report['evidence_levels']


def test_python_runner_retains_blocker_after_scan_saturation(tmp_path):
    write_project(tmp_path)
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs/notes.md').write_text('TODO\n' * 350, encoding='utf-8')
    (tmp_path / 'src/index.py').write_text('value = "mock data"\n', encoding='utf-8')
    report = run(tmp_path, '--runtime-proof', str(tmp_path / 'runtime.txt'))
    assert report['verdict'] == 'DEMO ONLY'
    assert any(item['file'].replace('\\', '/') == 'src/index.py' for item in report['blocking_fake_completion_candidates'])


def test_python_runner_rejects_free_form_proof(tmp_path):
    write_project(tmp_path, destination='public release')
    report = run(tmp_path, '--runtime-proof', 'x', '--ci-proof', 'x', '--independent-review', 'x')
    assert report['verdict'] == 'ALMOST READY'
    assert report['rejected_proof']['runtime'] == ['x']
    assert 'L3_RUNTIME' not in report['evidence_levels']
    assert 'L5_CI_REPRODUCIBLE' not in report['evidence_levels']
    assert 'L6_INDEPENDENT' not in report['evidence_levels']
