#!/usr/bin/env python3
"""Create commit-bound local runtime or visual evidence."""
import argparse
import datetime
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path


def head(root):
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True, capture_output=True, check=True)
    return result.stdout.strip().lower()


def write_manifest(root, kind, artifact, source, summary):
    output = root / '.shipvitals-evidence'
    output.mkdir(exist_ok=True)
    manifest = {
        'shipvitals_evidence': 1,
        'kind': kind,
        'observed_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'source': source,
        'summary': summary,
        'commit': head(root),
        'artifacts': [{
            'path': os.path.relpath(artifact, output).replace('\\', '/'),
            'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
        }],
    }
    destination = output / f'{kind}.shipvitals-evidence.json'
    destination.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    print(destination)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project', nargs='?', default='.')
    parser.add_argument('--runtime-command')
    parser.add_argument('--visual-file')
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if bool(args.runtime_command) == bool(args.visual_file):
        parser.error('provide exactly one of --runtime-command or --visual-file')
    if args.runtime_command:
        started = time.time()
        result = subprocess.run(args.runtime_command, cwd=root, shell=True, text=True, capture_output=True)
        artifact = root / '.shipvitals-evidence' / 'runtime-record.json'
        artifact.parent.mkdir(exist_ok=True)
        record = {
            'shipvitals_runtime': 1,
            'commit': head(root),
            'command': args.runtime_command,
            'exit_code': result.returncode,
            'seconds': round(time.time() - started, 2),
            'stdout_tail': result.stdout[-2000:],
            'stderr_tail': result.stderr[-2000:],
        }
        artifact.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
        write_manifest(root, 'runtime', artifact, 'shipvitals-runtime-recorder', 'A local release command completed and produced a commit-bound execution record.')
        raise SystemExit(result.returncode)
    artifact = Path(args.visual_file).resolve()
    if not artifact.is_file():
        parser.error('visual file not found')
    write_manifest(root, 'visual', artifact, 'shipvitals-visual-recorder', 'A visual release artifact was captured for the audited commit.')


if __name__ == '__main__':
    main()