# ShipVitals

**Know what blocks release before users do.**

ShipVitals is a release-readiness audit for AI-built apps. It runs the project checks it can prove, scans for release blockers, records missing evidence, and returns a go/no-go verdict: `READY`, `ALMOST READY`, `NOT READY`, or `DEMO ONLY`.

[![CI](https://github.com/omarkhandji-commits/shipvitals/actions/workflows/ci.yml/badge.svg)](https://github.com/omarkhandji-commits/shipvitals/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/omarkhandji-commits/shipvitals?include_prereleases)](https://github.com/omarkhandji-commits/shipvitals/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-1f6f5f.svg)](./LICENSE)

```bash
npx github:omarkhandji-commits/shipvitals audit .
```

The Node CLI runs without Python. npm and PyPI registry releases will be documented here only after clean installs from both registries pass.

## The Release Question

Tests answer whether known code paths behave as expected. ShipVitals asks a different question: **is there enough evidence to publish, sell, submit, deploy, or deliver this project?**

```text
Verdict: NOT READY
Score: 59

P0 blockers
- API key candidate found in committed source.
- Product promise and critical flows are not defined.

Not verified
- checkout runtime proof
- mobile visual proof
- independent review
```

Every finding names the affected file or command, release impact, evidence level, and retest path. Missing proof stays `NOT VERIFIED`; it is never converted into a pass.

## What It Checks

- declared lint, typecheck, test, and build commands;
- secret candidates in release-relevant source;
- TODO, skipped-test, mock-data, and demo-only signals;
- product promise and critical-flow definition;
- runtime, visual, CI, and independent-review evidence;
- score caps that prevent unsupported `READY` verdicts.

ShipVitals does not replace tests, Lighthouse, Playwright, security scanners, or code review. It uses their outputs as release evidence.

## Install

### Node CLI

Run directly from GitHub before the npm registry release:

```bash
npx github:omarkhandji-commits/shipvitals audit .
```

Initialize repeatable project context:

```bash
npx github:omarkhandji-commits/shipvitals init .
```

### Python CLI

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install "git+https://github.com/omarkhandji-commits/shipvitals.git"
shipvitals audit .
```

### Agent Skill

Copy [`skills/shipvitals`](./skills/shipvitals) into the skills directory used by Codex, Claude Code, or another compatible agent, then ask it to audit the current project as a release gate.

## Add Proof

Static analysis cannot prove a browser flow, payment, authentication boundary, or client acceptance. Attach observed evidence explicitly:

```bash
shipvitals audit . \
  --runtime-proof "artifacts/runtime.shipvitals-evidence.json" \
  --visual-proof "artifacts/visual.shipvitals-evidence.json" \
  --ci-proof "artifacts/ci.shipvitals-evidence.json" \
  --independent-review "artifacts/independent_review.shipvitals-evidence.json"
```

Reports are written to:

```text
.shipvitals-evidence/report.json
.shipvitals-evidence/summary.md
```

Proof flags accept typed .shipvitals-evidence.json manifests. Local artifacts require a matching SHA-256; CI and independent-review manifests must match the audited commit. See docs/EVIDENCE.md.

## GitHub Action

```yaml
steps:
  - uses: actions/checkout@v4
  - id: shipvitals
    uses: omarkhandji-commits/shipvitals@v1
    with:
      path: .
      mode: deep
      ci-proof: "GitHub Actions run"
```

The Action exposes a `verdict` output and preserves the JSON report as the source of detail.

## Evidence From Open Source

The calibration suite runs ShipVitals against 20 public repositories at pinned commits. These projects are used to measure command execution, evidence caps, and false-positive behavior; inclusion is not an endorsement by their maintainers.

| Category | Projects | Current limiting evidence |
|---|---:|---|
| CLI, API, library | 11 | independent review |
| Landing or content site | 2 | visual proof, independent review |
| SaaS or Next.js app | 2 | visual proof, independent review |
| Marketplace or extension | 3 | visual proof, independent review |
| Agent or automation | 2 | independent review |

Latest run: 20 repositories, 0 P0 findings, 0 P1 findings. UI projects remain capped at 74 when visual proof is absent; non-UI projects remain capped at 89 when independent review is absent.

- [Full benchmark table](./benchmarks/real-world/results/SUMMARY.md)
- [Benchmark method](./docs/EVALUATION_METHOD.md)
- [Measured before/after](./case-studies/real-before-after/README.md)
- [Release maturity](./docs/RELEASE_MATURITY.md)

## Where It Fits

| Tool | Primary signal | ShipVitals adds |
|---|---|---|
| Unit and integration tests | Known behavior | Product promise, missing proof, release verdict |
| Lighthouse | Browser quality | Auth, payment, handoff, and launch evidence |
| Playwright | Browser flows | Evidence levels and score caps |
| Security scanner | Vulnerability signals | UX, onboarding, support, and delivery context |
| Code review | Implementation quality | A documented release decision |

See the [comparison and boundaries](./docs/COMPARISON.md).

## Verify This Repository

```bash
npm run validate
npm run test
npm run test:package
npm run test:compile
npm run scorecard
npm run schema:check
npm run tone:check
npm run benchmark:real
npm pack --dry-run
python -m build --sdist --wheel
```

## Limits

- A static scan cannot prove production behavior.
- Pattern matching can produce false positives; reports separate candidates from blockers.
- A self-audit is not an independent review.
- Scores compare evidence against ShipVitals rules, not product-market fit or business value.

Report an incorrect verdict with a sanitized report using the [issue templates](https://github.com/omarkhandji-commits/shipvitals/issues/new/choose). Do not publish credentials, customer data, or private source.
