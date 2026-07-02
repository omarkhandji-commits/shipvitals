#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def is_type(value, expected):
    if isinstance(expected, list):
        return any(is_type(value, item) for item in expected)
    return {
        'object': lambda item: isinstance(item, dict),
        'array': lambda item: isinstance(item, list),
        'string': lambda item: isinstance(item, str),
        'number': lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        'integer': lambda item: isinstance(item, int) and not isinstance(item, bool),
        'boolean': lambda item: isinstance(item, bool),
        'null': lambda item: item is None,
    }.get(expected, lambda _item: True)(value)


def validate(schema, value, path='$'):
    errors = []
    if 'const' in schema and value != schema['const']:
        errors.append(f'{path}: expected const {schema["const"]!r}')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(f'{path}: expected one of {schema["enum"]!r}')
    if 'type' in schema and not is_type(value, schema['type']):
        errors.append(f'{path}: expected type {schema["type"]!r}')
        return errors
    if isinstance(value, str):
        if len(value) < schema.get('minLength', 0):
            errors.append(f'{path}: shorter than minLength {schema["minLength"]}')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            errors.append(f'{path}: does not match pattern {schema["pattern"]}')
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in schema and value < schema['minimum']:
            errors.append(f'{path}: below minimum {schema["minimum"]}')
        if 'maximum' in schema and value > schema['maximum']:
            errors.append(f'{path}: above maximum {schema["maximum"]}')
    if isinstance(value, list):
        if len(value) < schema.get('minItems', 0):
            errors.append(f'{path}: fewer than minItems {schema["minItems"]}')
        if 'items' in schema:
            for index, item in enumerate(value):
                errors.extend(validate(schema['items'], item, f'{path}[{index}]'))
    if isinstance(value, dict):
        for required in schema.get('required', []):
            if required not in value:
                errors.append(f'{path}: missing required property {required!r}')
        for key, subschema in schema.get('properties', {}).items():
            if key in value:
                errors.extend(validate(subschema, value[key], f'{path}.{key}'))
    for index, subschema in enumerate(schema.get('allOf', [])):
        if 'if' in subschema and 'then' in subschema:
            if not validate(subschema['if'], value, path):
                errors.extend(validate(subschema['then'], value, path))
        else:
            errors.extend(validate(subschema, value, f'{path}.allOf[{index}]'))
    if 'oneOf' in schema:
        matches = [option for option in schema['oneOf'] if not validate(option, value, path)]
        if len(matches) != 1:
            errors.append(f'{path}: expected exactly one oneOf match, got {len(matches)}')
    return errors


def require_valid(label, schema, value):
    errors = validate(schema, value)
    if errors:
        print(f'ShipVitals schema check: FAIL in {label}', file=sys.stderr)
        for error in errors[:30]:
            print(f'- {error}', file=sys.stderr)
        raise SystemExit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    schema_paths = [
        'schemas/evidence.schema.json',
        'schemas/evidence-manifest.schema.json',
        'schemas/report.schema.json',
        'evals/rubric.json',
        'package.json',
    ]
    loaded = {rel: load_json(root / rel) for rel in schema_paths}
    report_schema = loaded['schemas/report.schema.json']
    manifest_schema = loaded['schemas/evidence-manifest.schema.json']

    report_sample = {
        'tool': 'ShipVitals',
        'version': '1.0.0-beta.1',
        'generated_at': '2026-07-02T00:00:00Z',
        'project': '/tmp/project',
        'mode': 'deep',
        'config_exists': True,
        'product_type': 'cli',
        'product_promise_present': True,
        'commands_detected': ['npm test'],
        'command_results': [{'cmd': 'npm test', 'exit_code': 0, 'seconds': 1.0}],
        'secret_candidates': [],
        'blocking_secret_candidates': [],
        'fake_completion_candidates': [],
        'blocking_fake_completion_candidates': [],
        'proof': {'runtime': [], 'visual': [], 'ci': [], 'independent_review': []},
        'rejected_proof': {'runtime': [], 'visual': [], 'ci': [], 'independent_review': []},
        'rejected_proof_details': {'runtime': [], 'visual': [], 'ci': [], 'independent_review': []},
        'scan_stats': {'secret_priority_count': 0, 'fake_priority_count': 0},
        'evidence_levels': ['L1_STATIC', 'L2_DETERMINISTIC'],
        'score': 89,
        'score_caps': [{'max_score': 89, 'reason': 'High-stakes release missing independent review.'}],
        'p0': [],
        'p1': [],
        'verdict': 'ALMOST READY',
        'not_verified': ['independent review'],
    }
    require_valid('report sample', report_schema, report_sample)

    digest = 'a' * 64
    commit = 'b' * 40
    manifests = [
        {
            'shipvitals_evidence': 1,
            'kind': 'runtime',
            'observed_at': '2026-07-02T00:00:00Z',
            'source': 'local',
            'summary': 'Commit-bound runtime command evidence.',
            'commit': commit,
            'artifacts': [{'path': 'runtime.json', 'sha256': digest}],
        },
        {
            'shipvitals_evidence': 1,
            'kind': 'visual',
            'observed_at': '2026-07-02T00:00:00Z',
            'source': 'local',
            'summary': 'Commit-bound visual flow evidence.',
            'commit': commit,
            'artifacts': [{'path': 'flow.trace', 'sha256': digest}],
        },
        {
            'shipvitals_evidence': 1,
            'kind': 'ci',
            'observed_at': '2026-07-02T00:00:00Z',
            'source': 'github-actions',
            'summary': 'Verified GitHub Actions run evidence.',
            'commit': commit,
            'run_url': 'https://github.com/acme/repo/actions/runs/1',
            'artifacts': [{'url': 'https://github.com/acme/repo/actions/runs/1'}],
        },
        {
            'shipvitals_evidence': 1,
            'kind': 'independent_review',
            'observed_at': '2026-07-02T00:00:00Z',
            'source': 'github-review',
            'summary': 'Verified independent GitHub review evidence.',
            'reviewed_commit': commit,
            'reviewer': 'reviewer',
            'review_url': 'https://github.com/acme/repo/issues/1#issuecomment-1',
            'decision': 'accept',
            'artifacts': [{'path': 'review.md', 'sha256': digest}],
        },
    ]
    for manifest in manifests:
        require_valid(f'{manifest["kind"]} evidence manifest sample', manifest_schema, manifest)

    report_path = root / '.shipvitals-evidence' / 'report.json'
    if report_path.exists():
        require_valid('.shipvitals-evidence/report.json', report_schema, load_json(report_path))

    print('ShipVitals schema check: PASS')


if __name__ == '__main__':
    main()