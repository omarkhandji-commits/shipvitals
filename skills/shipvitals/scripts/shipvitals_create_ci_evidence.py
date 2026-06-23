#!/usr/bin/env python3
"""Create the commit-bound evidence manifest used by the composite action."""
import datetime
import json
import os
import sys
from pathlib import Path

output = Path(sys.argv[1])
run_url = os.environ['SHIPVITALS_RUN_URL']
commit = os.environ['SHIPVITALS_COMMIT'].lower()
manifest = {
    'shipvitals_evidence': 1,
    'kind': 'ci',
    'observed_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'source': 'github-actions',
    'summary': 'ShipVitals executed in GitHub Actions for the audited commit.',
    'run_url': run_url,
    'commit': commit,
    'artifacts': [{'url': run_url}],
}
output.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')