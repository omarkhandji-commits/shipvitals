from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills' / 'shipvitals' / 'scripts'
COMMANDS = {
    'audit': 'shipvitals_runner.py',
    'init': 'shipvitals_interview.py',
    'interview': 'shipvitals_interview.py',
    'diagnostics': 'shipvitals_diagnostics.py',
    'validate': 'shipvitals_validate.py',
    'scorecard': 'shipvitals_scorecard.py',
}

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else 'audit'
    if cmd in {'-h', '--help', 'help'} or cmd not in COMMANDS:
        print('Usage: shipvitals audit [project] [--ci] [--verbose] [--runtime-proof TEXT] [--visual-proof TEXT] | shipvitals init [project] | shipvitals diagnostics [project]')
        return 0 if cmd in {'-h', '--help', 'help'} else 1
    rest = argv[1:]
    target = next((a for a in rest if not a.startswith('--')), '.')
    flags = [a for a in rest if a != target]
    if cmd in {'init', 'interview'} and '--write-config' not in flags:
        flags.append('--write-config')
    script = SCRIPTS / COMMANDS[cmd]
    return subprocess.call([sys.executable, str(script), target, *flags])

if __name__ == '__main__':
    raise SystemExit(main())
