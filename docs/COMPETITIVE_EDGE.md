# Product Boundary

ShipVitals combines release evidence from project commands, runtime checks, visual checks, security scans, delivery requirements, and independent review. It converts those signals into a release verdict.

## Specialist Inputs

| Tool category | Evidence supplied to ShipVitals |
|---|---|
| Production-readiness checks | Build, test, type, lint, performance, and stack signals |
| Independent audit | Second-review findings and sign-off |
| CI quality gate | Repeatable command results and exit codes |
| Browser automation | Screenshots, responsive states, forms, and critical flows |
| Security review | Secret, dependency, auth, privacy, and vulnerability findings |
| Launch checklist | Support, legal, marketplace, and operational requirements |

## Decision Contract

ShipVitals answers one release question:

> Does the available evidence support publishing, selling, submitting, deploying, or delivering this project?

The report records the verdict, score caps, blockers, evidence, unverified areas, fixes, and retest commands.
