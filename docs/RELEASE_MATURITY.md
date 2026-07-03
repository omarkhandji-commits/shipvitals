# Release Maturity

This scorecard separates local verification from public distribution and external validation.

## Current Evidence

| Area | Status | Evidence |
|---|---|---|
| Tests | 39 passing | 25 Python and 14 Node tests via `npm run test` |
| Repository validation | Passing | `npm run validate` |
| Schema validation | Passing | `npm run schema:check` |
| Tone check | Passing | `npm run tone:check` |
| npm package | Packed install passes | `npm run test:package` |
| Python package | Wheel and sdist pass | `shipvitals_cli-1.0.0b1` artifacts |
| GitHub Pages site | Passing | `npm run site:check`, `https://omarkhandji-commits.github.io/shipvitals/` |
| Real-project benchmark | 20 projects executed | `benchmarks/real-world/results/` |
| Self-audit | `ALMOST READY`, P0/P1 `0/0` | `case-studies/shipvitals-self-audit/report.public.json` |
| Independent review | Pending | [Issue #6](https://github.com/omarkhandji-commits/shipvitals/issues/6) requests external L6 review |
| npm publication | Pending | [Issue #8](https://github.com/omarkhandji-commits/shipvitals/issues/8); registry returns 404 until publication |
| PyPI publication | Pending | [Issue #8](https://github.com/omarkhandji-commits/shipvitals/issues/8); registry returns 404 until publication |
| Remote GitHub Action | Passing | Public CI runs `uses: ./` on `main` |
| External feedback | Pending | [Issue #7](https://github.com/omarkhandji-commits/shipvitals/issues/7) invites real-world audit examples |

## Beta Release Requirements

- initialize the Git repository;
- publish the repository under its final owner;
- confirm GitHub source installation after the first push;
- run the GitHub Action in the public repository;
- publish the beta release notes.

Status: complete for the public beta baseline.

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

Registry publishing instructions live in [docs/PUBLISHING.md](./PUBLISHING.md).
