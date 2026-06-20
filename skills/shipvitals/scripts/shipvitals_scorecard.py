#!/usr/bin/env python3
from pathlib import Path
import sys, json
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
groups={
 'core_skill':['skills/shipvitals/SKILL.md','skills/shipvitals/references/evidence-standard.md'],
 'zero_friction_cli':['package.json','cli/package.json','cli/bin/shipvitals.js','pyproject.toml','shipvitals_cli/cli.py'],
 'config_memory':['schemas/config.schema.json','skills/shipvitals/scripts/shipvitals_config.py','skills/shipvitals/templates/project-config.example.json'],
 'interview_modes':['skills/shipvitals/scripts/shipvitals_interview.py','skills/shipvitals/templates/interview-questions.md','skills/shipvitals/templates/quick-audit.md','skills/shipvitals/templates/deep-audit.md'],
 'rules_json':['skills/shipvitals/references/verdict-scoring.json','skills/shipvitals/references/evidence-levels.json','skills/shipvitals/references/severity-rules.json','skills/shipvitals/references/verdict-decision-tree.json'],
 'scripts':['skills/shipvitals/scripts/shipvitals_runner.py','skills/shipvitals/scripts/shipvitals_secret_scan.py','skills/shipvitals/scripts/shipvitals_falsification_scan.py','skills/shipvitals/scripts/shipvitals_diagnostics.py'],
 'framework_adapters':['skills/shipvitals/references/adapters/nextjs.md','skills/shipvitals/references/adapters/shopify.md','skills/shipvitals/references/adapters/fastapi.md','skills/shipvitals/scripts/shipvitals_detect_adapter.py'],
 'docs':['README.md','docs/INSTALLATION.md','docs/ARCHITECTURE.md','docs/SCORING_RUBRIC.md','docs/EDITORIAL_STANDARD.md'],
 'trust':['SECURITY.md','docs/TRUST_AND_SAFETY.md','docs/PERMISSIONS.md'],
 'agents':['agents/product-promise-auditor.md','agents/visual-qa-auditor.md','agents/release-manager.md'],
 'proof':['schemas/evidence.schema.json','schemas/report.schema.json','benchmarks/BENCHMARK_PLAN.md','evals/rubric.json'],
 'distribution':['registry/skill-card.md','registry/listing.md','LICENSE','CONTRIBUTING.md','SUPPORT.md','README_ACTION.md','action.yml','skills/shipvitals/agents/openai.yaml'],
 'automation':['.github/workflows/ci.yml','.claude/commands/shipvitals.md','.claude/settings/shipvitals.hooks.example.json','.pre-commit-hooks.yaml'],
 'sessions':['skills/shipvitals/examples/session-ready.md','skills/shipvitals/examples/session-almost-ready.md','skills/shipvitals/examples/session-not-ready.md','skills/shipvitals/examples/session-demo-only.md'],
 'tests':['tests/test_probe.py','tests/test_gate.py','tests/test_secret_scan.py','tests/test_falsification_scan.py','tests/test_release_metadata.py','tests/integration/test_full_audit.py'],
 'client_reports':['skills/shipvitals/templates/client-report.md','skills/shipvitals/templates/client-report.html','skills/shipvitals/templates/client-email.md'],
 'tone':['skills/shipvitals/scripts/shipvitals_tone_check.py','docs/EDITORIAL_STANDARD.md']
}
score=0; detail={}
for k,items in groups.items():
    ok=all((root/i).exists() for i in items); detail[k]=ok; score+=ok
pct=round(score/len(groups)*100,2)
print(json.dumps({'tool':'ShipVitals','score_percent':pct,'groups':detail}, indent=2))
sys.exit(0 if pct==100 else 1)
