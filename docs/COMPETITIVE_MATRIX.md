# Tool Integration Matrix

ShipVitals uses specialist results as inputs to a release decision.

| Tool category | Specialist output | ShipVitals responsibility |
|---|---|---|
| Production readiness | Stack, build, test, visual, and performance checks | Add product promise, delivery requirements, and verdict caps |
| CI quality gate | Deterministic checks and exit codes | Record repeatability and release impact |
| Independent audit | Second-review findings | Store L6 evidence and reviewer decision |
| Code review | Language and framework findings | Map findings to P0/P1/P2/P3 and retest steps |
| Security review | Vulnerability and data-risk findings | Block release when baseline or required specialist proof is missing |
| Visual QA | Screenshots, responsive states, and browser errors | Require visual proof for UI release verdicts |
| Launch checklist | Support, legal, marketplace, and operational items | Combine launch evidence with technical evidence |

## Release Question

ShipVitals reports whether the evidence supports publication, sale, submission, deployment, or delivery at the time of the audit.
