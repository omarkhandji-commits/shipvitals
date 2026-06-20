#!/usr/bin/env python3
import json, sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
skill=root/'skills'/'shipvitals'
required=[
 'SKILL.md','references/evidence-standard.md','references/verdict-scoring.md','references/falsification-gate.md','references/finding-quality.md',
 'references/web-saas-motionvitals.md','references/api-cli-backend.md','references/shopify-marketplace.md','references/specialist-chaining.md',
 'scripts/shipvitals_probe.py','scripts/shipvitals_gate.py','scripts/shipvitals_secret_scan.py','scripts/shipvitals_link_check.py',
 'scripts/shipvitals_falsification_scan.py','scripts/shipvitals_evidence_pack.py','templates/final-report.md','templates/product-promise.md'
]
root_required=['README.md','LICENSE','CHANGELOG.md','CONTRIBUTING.md','RELEASE.md','VALIDATION.md','package.json','.github/workflows/validate.yml','assets/shipvitals-hero.svg']
missing=[x for x in required if not (skill/x).exists()]+[x for x in root_required if not (root/x).exists()]
skill_text=(skill/'SKILL.md').read_text(errors='ignore') if (skill/'SKILL.md').exists() else ''
checks={
 'has_frontmatter': skill_text.startswith('---'),
 'progressive_disclosure': len(skill_text.splitlines()) < 180 and 'references/' in skill_text,
 'truth_rule': 'Never say `READY` without evidence' in skill_text,
 'evidence_levels': 'L6' in (skill/'references'/'evidence-standard.md').read_text(errors='ignore') if (skill/'references'/'evidence-standard.md').exists() else False,
 'anti_generic': 'Every finding must include' in skill_text,
 'examples': len(list((skill/'examples'/'reports').glob('*.md'))) >= 3,
 'case_studies': len(list((root/'case-studies').glob('*'))) >= 3,
 'missing_files': missing
}
score=100 - len(missing)*7 - sum(0 if v else 6 for k,v in checks.items() if isinstance(v,bool))
print(json.dumps({'score':max(score,0),'checks':checks},indent=2))
sys.exit(1 if missing or score<90 else 0)
