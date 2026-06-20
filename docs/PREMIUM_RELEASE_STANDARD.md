# Release Qualification Standard

ShipVitals must operate as a reproducible release gate rather than a static checklist.

## Requirements

1. Start each audit from a product promise and required user flows.
2. Attach command, file, screenshot, runtime, CI, or review evidence to each release claim.
3. Search for mocks, skipped tests, placeholder content, fake integrations, silent failures, exposed secrets, and package leaks.
4. Require browser or device evidence for visual products.
5. Export machine-readable JSON for CI and hooks.
6. Export a short report for builders, clients, and reviewers.
7. Route deep security, code review, and browser work to specialist tools.
8. Keep source installation under five minutes.
9. Maintain repeatable adversarial and real-project benchmarks.
10. Run ShipVitals against its own repository before release.

## Score Caps

- Missing product promise: maximum `84`.
- Missing deterministic command output: maximum `87`.
- Missing runtime evidence for a UI product: maximum `89`.
- Missing visual/mobile evidence for a public web app: maximum `91`.
- Missing security or secret scan: maximum `90`.
- Missing falsification scan: maximum `88`.
- Missing CI or hook path: maximum `92`.
- Missing independent review for paid or client delivery: maximum `94`.
- Exposed secret, broken auth/payment, or fake core integration: `NOT READY`.

## READY Evidence

- product promise;
- passing project commands;
- runtime proof;
- visual proof where applicable;
- security and dependency baseline;
- falsification scan;
- P0/P1/P2 findings;
- retest commands;
- CI or hook evidence;
- independent review for high-stakes releases.
