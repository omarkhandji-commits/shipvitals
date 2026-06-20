#!/usr/bin/env python3
from pathlib import Path
import sys, subprocess
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
required=[
 'README.md','LICENSE','CHANGELOG.md','CONTRIBUTING.md','SECURITY.md','SUPPORT.md','ROADMAP.md','RELEASE.md','VALIDATION.md','package.json','pyproject.toml','action.yml','README_ACTION.md',
 'cli/bin/shipvitals.js','shipvitals_cli/cli.py','skills/shipvitals/SKILL.md','schemas/config.schema.json',
 'skills/shipvitals/scripts/shipvitals_runner.py','skills/shipvitals/scripts/shipvitals_interview.py','skills/shipvitals/scripts/shipvitals_config.py','skills/shipvitals/scripts/shipvitals_diagnostics.py',
 'skills/shipvitals/scripts/shipvitals_real_world_benchmark.py','benchmarks/real-world/manifest.json','benchmarks/real-world/README.md',
 'skills/shipvitals/references/verdict-scoring.json','skills/shipvitals/references/evidence-levels.json','skills/shipvitals/references/severity-rules.json','skills/shipvitals/references/verdict-decision-tree.json',
 'skills/shipvitals/templates/interview-questions.md','skills/shipvitals/templates/quick-audit.md','skills/shipvitals/templates/deep-audit.md',
 'tests/test_probe.py','tests/test_gate.py','tests/test_secret_scan.py','tests/test_falsification_scan.py','tests/test_release_metadata.py','tests/integration/test_full_audit.py',
 'skills/shipvitals/agents/openai.yaml','.github/workflows/ci.yml'
]
missing=[x for x in required if not (root/x).exists()]
py_files=[str(p) for p in (root/'skills/shipvitals/scripts').glob('*.py')]+[str(p) for p in (root/'shipvitals_cli').glob('*.py')]
compile_ok=True
if py_files:
    r=subprocess.run([sys.executable,'-m','py_compile',*py_files], text=True, capture_output=True)
    compile_ok=(r.returncode==0)
if missing or not compile_ok:
    print('ShipVitals validation: FAIL')
    if missing: print('missing:', missing)
    if not compile_ok: print('py_compile failed:', r.stderr)
    sys.exit(1)
print('ShipVitals validation: PASS')
