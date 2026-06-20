# Release Maturity

This scorecard separates local verification from public distribution and external validation.

## Current Evidence

| Area | Status | Evidence |
|---|---|---|
| Tests | 25 passing | 18 Python and 7 Node tests via `npm run test` |
| Repository validation | Passing | `npm run validate` |
| Schema validation | Passing | `npm run schema:check` |
| Tone check | Passing | `npm run tone:check` |
| npm package | Packed install passes | `npm run test:package` |
| Python package | Wheel and sdist pass | `shipvitals_cli-1.0.0b1` artifacts |
| GitHub Pages site | Local validation passes | `npm run site:check`, desktop/mobile renders |
| Real-project benchmark | 20 projects executed | `benchmarks/real-world/results/` |
| Self-audit | `ALMOST READY`, P0/P1 `0/0` | `case-studies/shipvitals-self-audit/report.public.json` |
| Independent review | Pending | `case-studies/shipvitals-independent-review/` |
| npm publication | Pending | Registry returns 404 until publication |
| PyPI publication | Pending | Registry returns 404 until publication |
| Remote GitHub Action | Pending | Requires public repository and release tag |
| External feedback | Pending | Requires public users |

## Beta Release Requirements

- initialize the Git repository;
- publish the repository under its final owner;
- confirm GitHub source installation after the first push;
- run the GitHub Action in the public repository;
- publish the beta release notes.

## Stable Release Requirements

- publish npm and PyPI packages;
- verify registry installation in clean environments;
- publish and test the `v1` Action reference;
- complete the independent L6 review;
- add 3 SaaS/Next.js, 2 landing/content, and 1 automation benchmark to balance coverage;
- resolve external false-positive and install reports;
- record accepted directory or marketplace submissions.

## Evidence Policy

Do not convert pending items into passed items without a public URL, command output, report artifact, or reviewer record.
