import subprocess
import sys
from pathlib import Path


def test_node_cli_help_exits_zero():
    repo = Path(__file__).parents[1]
    result = subprocess.run(
        ['node', 'cli/bin/shipvitals.js', '--help'],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert 'shipvitals audit' in result.stdout


def test_python_cli_help_exits_zero():
    repo = Path(__file__).parents[1]
    result = subprocess.run(
        [sys.executable, '-m', 'shipvitals_cli.cli', '--help'],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert '--runtime-proof' in result.stdout


def test_python_cli_accepts_flags_before_project():
    repo = Path(__file__).parents[1]
    project = repo / 'tests' / 'fixtures' / 'mock-nextjs'
    result = subprocess.run(
        [sys.executable, '-m', 'shipvitals_cli.cli', 'audit', '--no-fail', '--ci', str(project)],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert '"verdict"' in result.stdout