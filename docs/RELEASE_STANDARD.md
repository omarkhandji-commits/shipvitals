# ShipVitals Release Standard

ShipVitals defines the evidence required for a release verdict on projects built with coding assistants.

## The Release bar

A project can only be called release-ready when the gate has evidence across all release-critical dimensions:

1. Product promise and mandatory flows are explicit.
2. Deterministic checks have run, not merely been suggested.
3. Runtime behavior is observed where runtime matters.
4. Visual/mobile proof exists for visual products.
5. Security/privacy baseline is checked.
6. Fake completion is actively falsified.
7. CI/hook repeatability exists or the lack of it caps the verdict.
8. A second-auditor path exists for client, paid, public, or risky releases.
9. Findings are specific enough to fix and retest.
10. Evidence is exported in machine-readable and human-readable form.

## Non-negotiable score caps

- No product promise: max `DEMO ONLY`.
- No deterministic command output: max `ALMOST READY`.
- Web/UI project without runtime/visual evidence: max `ALMOST READY`.
- Payment/auth/data flow not verified when present: max `NOT READY`.
- Public/client release without secret scan: max `NOT READY`.
- Any P0: max `NOT READY`.
- Any untested critical claim: max `ALMOST READY`.
- Same-agent-only audit on paid/client/high-risk release: max `ALMOST READY` unless the user explicitly accepts risk.

## Specialist Integration

ShipVitals integrates specialist outputs into the release report:

- use specialized QA, security, browser, and code-review tools;
- convert their outputs into one final release verdict;
- refuse to overclaim when evidence is missing;
- create a reproducible release artifact.

The report preserves the specialist evidence and applies the release policy defined above.
