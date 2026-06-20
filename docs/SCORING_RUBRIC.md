# Scoring Rubric

ShipVitals scores projects by release risk, not by how impressive the code looks.

## Hard caps

- Any exposed secret candidate: cannot be READY.
- Missing product promise: cannot exceed ALMOST READY.
- Web app without runtime/visual evidence: cannot be READY.
- Payment/client/marketplace flow not verified: cannot be READY for paid release.
- Critical P0 issue: NOT READY.
- Fake integration or demo-only dependency in required flow: DEMO ONLY or NOT READY.

## Dimensions

1. Product promise and mandatory flows
2. Functional correctness
3. Runtime evidence
4. Visual/mobile quality
5. Security/privacy baseline
6. Falsification and fake-completion scan
7. Business/client/marketplace readiness
8. CI/hook repeatability
9. Independent audit when required
10. Report quality and retestability
