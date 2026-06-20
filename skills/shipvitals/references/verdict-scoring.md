# Verdict Scoring

Start from 100 and apply blockers/caps.

## Hard caps

- No product promise/spec: max 74.
- No build/run proof: max 69.
- Web UI without runtime/visual proof: max 74.
- Broken core flow: max 49.
- Payment/auth/onboarding broken when promised: max 59.
- Secrets or private keys found: max 59.
- Critical privacy/legal gap for data collection: max 69.
- Placeholder/demo content in public core flow: max 69.
- Skipped or fake tests in critical areas: max 74.
- App cannot install/start: max 49.
- No README/client handoff for client project: max 79.

## Verdict mapping

- 90-100: READY only if no P0/P1 and required evidence level is met.
- 80-89: ALMOST READY unless only minor P2/P3 remain and evidence is strong.
- 60-79: NOT READY or DEMO ONLY depending on severity.
- Below 60: NOT READY.

## Important

A high score cannot override a hard cap. Missing proof is not a pass.
