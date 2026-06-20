# ShipVitals Independent Review

Status: `PENDING`

Round 1 was completed on 2026-06-20 and rejected the beta. See `review-2026-06-20-round-1.md`. L6 remains ungranted until the reproduced findings are fixed and independently retested.

This folder stores the independent L6 review required before the release scorecard can mark independent review complete.

## Required Reviewer

Use a reviewer who did not write the current implementation. Acceptable options:

- another senior engineer;
- another agent thread with no access to the intended answer;
- a maintainer or user who runs ShipVitals on a fresh checkout.

## Required Inputs

- `.shipvitals-evidence/report.json`
- `.shipvitals-evidence/summary.md`
- `benchmarks/real-world/results/SUMMARY.md`
- `docs/DEPLOYMENT_READINESS.md`
- `docs/RELEASE_MATURITY.md`

## Required Output

Before this case study is marked complete, add:

- reviewer identity or review method;
- date;
- commands run;
- findings;
- false positives;
- missed risks;
- final independent verdict;
- whether the 89 cap can be lifted.

## Current Decision

Do not lift the ShipVitals self-audit cap yet.

Reason: the project is public-release oriented, and a tool should not certify itself as fully `READY` without an independent evidence review.
