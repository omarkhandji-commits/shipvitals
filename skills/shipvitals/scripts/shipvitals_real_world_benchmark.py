#!/usr/bin/env python3
import argparse, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / 'benchmarks' / 'real-world' / 'manifest.json'
RESULTS = ROOT / 'benchmarks' / 'real-world' / 'results'
RUNNER = ROOT / 'skills' / 'shipvitals' / 'scripts' / 'shipvitals_runner.py'


def sanitize_public_artifact(value, workspace):
    replacements = ((str(workspace), '<benchmark-workspace>'), (str(ROOT), '<shipvitals-root>'))
    if isinstance(value, dict):
        return {key: sanitize_public_artifact(item, workspace) for key, item in value.items()}
    if isinstance(value, list):
        return [sanitize_public_artifact(item, workspace) for item in value]
    if isinstance(value, str):
        for source, target in replacements:
            value = value.replace(source, target).replace(source.replace('\\', '/'), target)
    return value


def run(cmd, cwd=None, timeout=180):
    started = time.time()
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    return {
        'cmd': cmd,
        'exit_code': proc.returncode,
        'seconds': round(time.time() - started, 2),
        'stdout': proc.stdout[-8000:],
        'stderr': proc.stderr[-8000:],
    }


def write_config(project_dir, item):
    config = {
        'version': 1,
        'project': {
            'name': item['name'],
            'type': item['type'],
            'audience': item['audience'],
            'destination': item['destination'],
            'promise': item['promise'],
            'critical_flows': item['critical_flows'],
        },
        'commands': item['commands'],
        'exclude': ['.git', 'node_modules'],
    }
    (project_dir / '.shipvitals-config.json').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')


def clone_project(workspace, item):
    target = workspace / item['slug']
    if target.exists():
        result = {'status': 'exists', 'path': str(target)}
    else:
        result = run(['git', 'clone', '--depth', '1', item['repo'], str(target)], timeout=300)
    revision = item.get('revision')
    if target.exists() and revision:
        checkout = run(['git', 'checkout', '--detach', revision], cwd=target)
        if checkout['exit_code'] != 0:
            run(['git', 'fetch', '--depth', '1', 'origin', revision], cwd=target, timeout=300)
            checkout = run(['git', 'checkout', '--detach', revision], cwd=target)
        result['checkout'] = checkout
    result['path'] = str(target)
    return result


def audit_project(workspace, item):
    project_dir = workspace / item['slug']
    if not project_dir.exists():
        return {
            'slug': item['slug'],
            'name': item['name'],
            'repo': item['repo'],
            'category': item.get('category', item['type']),
            'verdict': 'NO REPORT',
            'score': 0,
            'p0': 0,
            'p1': 1,
            'commands': 0,
            'not_verified': ['project clone'],
            'error': 'missing clone',
        }
    write_config(project_dir, item)
    (project_dir / '.shipvitals-evidence').mkdir(exist_ok=True)
    cmd = [
        sys.executable,
        str(RUNNER),
        str(project_dir),
        '--ci',
    ]
    result = run(cmd, cwd=ROOT, timeout=240)
    report_path = project_dir / '.shipvitals-evidence' / 'report.json'
    report = json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {}
    revision_result = run(['git', 'rev-parse', 'HEAD'], cwd=project_dir)
    revision = revision_result.get('stdout', '').strip()
    out_dir = RESULTS / item['slug']
    out_dir.mkdir(parents=True, exist_ok=True)
    public_result = sanitize_public_artifact(result, workspace)
    public_report = sanitize_public_artifact(report, workspace)
    (out_dir / 'run.json').write_text(json.dumps(public_result, indent=2), encoding='utf-8')
    if report:
        (out_dir / 'report.json').write_text(json.dumps(public_report, indent=2), encoding='utf-8')
    p0 = len(report.get('p0', []))
    p1 = len(report.get('p1', []))
    commands = len(report.get('command_results', []))
    project_summary = [
        f"# {item['name']}",
        '',
        'Real open-source benchmark audit.',
        '',
        f"- Repository: {item['repo']}",
        f"- Revision: `{revision}`",
        f"- Category: {item.get('category', item['type'])}",
        f"- Verdict: `{report.get('verdict', 'NO REPORT')}`",
        f"- Score: `{report.get('score', 0)}`",
        f"- P0/P1: `{p0}/{p1}`",
        f"- Commands executed: `{commands}`",
        f"- Not verified: {', '.join(report.get('not_verified', [])) or 'none'}",
        '',
        '## Commands',
        '',
    ]
    for command in report.get('command_results', []):
        project_summary.append(f"- `{command.get('cmd')}` -> `{command.get('exit_code')}`")
    project_summary.extend([
        '',
        '## Evidence',
        '',
        '- `report.json`',
        '- `run.json`',
    ])
    (out_dir / 'SUMMARY.md').write_text('\n'.join(project_summary) + '\n', encoding='utf-8')
    return {
        'slug': item['slug'],
        'name': item['name'],
        'repo': item['repo'],
        'category': item.get('category', item['type']),
        'verdict': report.get('verdict', 'NO REPORT'),
        'score': report.get('score', 0),
        'p0': p0,
        'p1': p1,
        'commands': commands,
        'command_names': [command.get('cmd', '') for command in report.get('command_results', [])],
        'revision': revision,
        'not_verified': report.get('not_verified', []),
        'result_dir': str(out_dir.relative_to(ROOT)),
    }


def write_summary(rows):
    RESULTS.mkdir(parents=True, exist_ok=True)
    summary = {
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'projects': rows,
    }
    (RESULTS / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    lines = ['# Real-world Benchmark Results', '']
    lines.append('| Project | Revision | Category | Verdict | Score | P0/P1 | Commands | Not verified |')
    lines.append('|---|---|---|---:|---:|---:|---|---|')
    for row in rows:
        command_names = '<br>'.join(f"`{command}`" for command in row.get('command_names', [])) or 'none'
        lines.append(f"| {row['name']} | `{row.get('revision', '')[:12]}` | {row['category']} | {row['verdict']} | {row['score']} | {row['p0']}/{row['p1']} | {command_names} | {', '.join(row['not_verified']) or 'none'} |")
    lines.append('')
    lines.append('These are real repositories. Public release verdicts stay capped without independent review evidence.')
    (RESULTS / 'SUMMARY.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--workspace', default=str(Path(tempfile.gettempdir()) / 'shipvitals-real-world'))
    parser.add_argument('--manifest', default=str(MANIFEST))
    parser.add_argument('--clone', action='store_true')
    args = parser.parse_args()
    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(Path(args.manifest).read_text(encoding='utf-8-sig'))
    if RESULTS.exists():
        shutil.rmtree(RESULTS)
    RESULTS.mkdir(parents=True)
    clone_results = [clone_project(workspace, item) for item in manifest['projects']]
    public_clone_results = sanitize_public_artifact(clone_results, workspace)
    (RESULTS / 'clone-results.json').write_text(json.dumps(public_clone_results, indent=2), encoding='utf-8')
    rows = [audit_project(workspace, item) for item in manifest['projects']]
    write_summary(rows)
    print(json.dumps({'results': str(RESULTS), 'projects': rows, 'clone_results': clone_results}, indent=2))


if __name__ == '__main__':
    main()
