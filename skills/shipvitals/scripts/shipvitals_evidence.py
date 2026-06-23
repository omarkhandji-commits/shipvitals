"""Strict, provenance-aware validation for ShipVitals evidence manifests."""
import datetime
import hashlib
import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path


def git_head(root):
    result = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True, capture_output=True)
    return result.stdout.strip().lower() if result.returncode == 0 else ''


def git_repository(root):
    result = subprocess.run(['git', '-C', str(root), 'remote', 'get-url', 'origin'], text=True, capture_output=True)
    if result.returncode != 0:
        return ''
    match = re.search(r'github\.com[/:]([^/]+)/([^/\s]+?)(?:\.git)?$', result.stdout.strip(), re.I)
    return f'{match.group(1)}/{match.group(2)}'.lower() if match else ''


def inside(root, candidate):
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def valid_visual_file(path):
    data = path.read_bytes()
    signatures = (b'\x89PNG', b'\xff\xd8\xff', b'GIF8', b'RIFF', b'PK\x03\x04')
    return any(data.startswith(item) for item in signatures) or (len(data) > 12 and data[4:8] == b'ftyp')


def github_json(api_path):
    try:
        request = urllib.request.Request(
            'https://api.github.com' + api_path,
            headers={
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'shipvitals-1.0.0-beta.1',
                **({'Authorization': 'Bearer ' + os.environ['SHIPVITALS_GITHUB_TOKEN']} if os.getenv('SHIPVITALS_GITHUB_TOKEN') else {}),
            },
        )
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.load(response)
    except Exception:
        return None


def verify_ci_provenance(root, manifest):
    match = re.fullmatch(r'https://github\.com/([^/]+)/([^/]+)/actions/runs/(\d+)', str(manifest.get('run_url', '')))
    if not match:
        return 'CI evidence requires a GitHub Actions run URL.'
    repository = f'{match.group(1)}/{match.group(2)}'.lower()
    expected = git_repository(root)
    if expected and repository != expected:
        return 'CI run belongs to a different repository.'
    run = github_json(f'/repos/{match.group(1)}/{match.group(2)}/actions/runs/{match.group(3)}')
    if not run or str(run.get('html_url')) != str(manifest.get('run_url')):
        return 'GitHub could not verify the CI run.'
    head = git_head(root)
    if not head or str(run.get('head_sha', '')).lower() != head or str(manifest.get('commit', '')).lower() != head:
        return 'CI evidence commit does not match the audited HEAD.'
    current = (
        os.getenv('GITHUB_ACTIONS') == 'true'
        and os.getenv('GITHUB_RUN_ID', '') == match.group(3)
        and os.getenv('GITHUB_SHA', '').lower() == head
    )
    if run.get('conclusion') != 'success' and not (current and run.get('status') in {'queued', 'in_progress'}):
        return 'The verified CI run did not complete successfully.'
    return ''


def verify_independent_provenance(root, manifest):
    match = re.fullmatch(
        r'https://github\.com/([^/]+)/([^/]+)/(?:issues|pull)/\d+#issuecomment-(\d+)',
        str(manifest.get('review_url', '')),
    )
    if not match:
        return 'Independent review requires a GitHub issue or pull-request comment URL.'
    repository = f'{match.group(1)}/{match.group(2)}'.lower()
    expected = git_repository(root)
    if not expected or repository != expected:
        return 'Independent review must be published on the audited repository.'
    comment = github_json(f'/repos/{match.group(1)}/{match.group(2)}/issues/comments/{match.group(3)}')
    if not comment or str(comment.get('html_url')) != str(manifest.get('review_url')):
        return 'GitHub could not verify the review comment.'
    reviewer = str(comment.get('user', {}).get('login', ''))
    if (
        not reviewer
        or reviewer.lower() != str(manifest.get('reviewer', '')).lower()
        or reviewer.lower() == match.group(1).lower()
    ):
        return 'Reviewer identity is not independent of the repository owner.'
    if comment.get('author_association') not in {'NONE', 'CONTRIBUTOR', 'FIRST_TIMER', 'FIRST_TIME_CONTRIBUTOR'}:
        return 'Reviewer is an owner, member, or collaborator.'
    head = git_head(root)
    if not head or str(manifest.get('reviewed_commit', '')).lower() != head:
        return 'Independent review does not cover the audited HEAD.'
    if f'SHIPVITALS-L6 ACCEPT {head}' not in str(comment.get('body', '')):
        return 'Review comment does not contain the required acceptance statement.'
    user = github_json('/users/' + reviewer)
    if not user or not user.get('created_at'):
        return 'GitHub could not verify reviewer account age.'
    created = datetime.datetime.fromisoformat(str(user['created_at']).replace('Z', '+00:00'))
    if datetime.datetime.now(datetime.timezone.utc) - created < datetime.timedelta(days=90):
        return 'Reviewer account must be at least 90 days old.'
    return ''


def validate_manifest(root, value, kind):
    def fail(reason):
        return False, reason

    manifest_path = Path(value).expanduser()
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path
    if not str(value).endswith('.shipvitals-evidence.json'):
        return fail('Expected a .shipvitals-evidence.json manifest.')
    if not manifest_path.is_file():
        return fail('Manifest file not found.')
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    except Exception:
        return fail('Manifest is not valid JSON.')
    if manifest.get('shipvitals_evidence') != 1 or manifest.get('kind') != kind:
        return fail(f'Manifest kind must be {kind}.')

    timestamp = str(manifest.get('observed_at', ''))
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', timestamp):
        return fail('observed_at must be a valid UTC timestamp.')
    try:
        observed = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    except ValueError:
        return fail('observed_at must be a valid UTC timestamp.')
    now = datetime.datetime.now(datetime.timezone.utc)
    if observed > now + datetime.timedelta(minutes=5) or now - observed > datetime.timedelta(days=30):
        return fail('Evidence timestamp must be within the last 30 days.')

    if len(str(manifest.get('source', '')).strip()) < 3:
        return fail('source is required.')
    if len(str(manifest.get('summary', '')).strip()) < 20:
        return fail('summary must contain at least 20 characters.')
    artifacts = manifest.get('artifacts')
    if not isinstance(artifacts, list) or not artifacts:
        return fail('At least one artifact is required.')

    head = git_head(root)
    if kind in {'runtime', 'visual'} and head and str(manifest.get('commit', '')).lower() != head:
        return fail('Evidence commit does not match the audited HEAD.')
    runtime_ext = {'.json', '.xml', '.zip', '.har', '.trace', '.mp4', '.mov'}

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            return fail('Invalid artifact entry.')
        if artifact.get('path'):
            unresolved = manifest_path.parent / str(artifact['path'])
            if not inside(root, unresolved) or not unresolved.exists():
                return fail('Local artifacts must stay inside the audited project.')
            artifact_path = unresolved.resolve()
            if not inside(root, artifact_path) or not artifact_path.is_file() or artifact_path.stat().st_size == 0:
                return fail('Local artifact is missing, empty, or escapes through a symlink.')
            digest = hashlib.sha256(artifact_path.read_bytes()).hexdigest()
            if not re.fullmatch(r'[a-fA-F0-9]{64}', str(artifact.get('sha256', ''))) or digest != str(artifact['sha256']).lower():
                return fail('Local artifact SHA-256 mismatch.')
            if kind == 'visual' and not valid_visual_file(artifact_path):
                return fail('Visual artifact has no recognized image, video, trace, or archive signature.')
            if kind == 'runtime':
                if artifact_path.suffix.lower() not in runtime_ext:
                    return fail('Runtime evidence must be a structured test, trace, HAR, video, or JSON artifact.')
                if artifact_path.suffix.lower() == '.json':
                    try:
                        runtime = json.loads(artifact_path.read_text(encoding='utf-8-sig'))
                    except Exception:
                        return fail('Runtime JSON artifact is invalid.')
                    if (
                        runtime.get('shipvitals_runtime') != 1
                        or runtime.get('exit_code') != 0
                        or (head and str(runtime.get('commit', '')).lower() != head)
                    ):
                        return fail('Runtime JSON is not a passing commit-bound execution record.')
        elif artifact.get('url'):
            if kind != 'ci':
                return fail('Remote artifacts are not accepted without local digest verification.')
            if str(artifact['url']) != str(manifest.get('run_url')):
                return fail('CI artifact URL must equal run_url.')
        else:
            return fail('Each artifact requires path or url.')

    if kind == 'ci':
        reason = verify_ci_provenance(root, manifest)
        if reason:
            return fail(reason)
    if kind == 'independent_review':
        if manifest.get('decision') != 'accept' or len(str(manifest.get('reviewer', '')).strip()) < 3:
            return fail('Independent evidence requires an identified reviewer and accept decision.')
        reason = verify_independent_provenance(root, manifest)
        if reason:
            return fail(reason)
    return True, ''


def validate_evidence(root, values, kind, as_list):
    valid = []
    rejected = []
    details = []
    for value in as_list(values):
        accepted, reason = validate_manifest(root, value, kind)
        (valid if accepted else rejected).append(value)
        if not accepted:
            details.append({'value': value, 'reason': reason})
    return {'valid': valid, 'rejected': rejected, 'details': details}