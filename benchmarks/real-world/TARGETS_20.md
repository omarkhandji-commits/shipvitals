# 20 Real-World Benchmark Target

Status: `20/20 executed`

This file tracks real benchmark coverage. Every executed project has:

- `report.json`
- `run.json`
- `SUMMARY.md`
- verdict, score, P0/P1, commands, and not-verified areas

Results live in `benchmarks/real-world/results/`.

## Current Status

| Metric | Count |
|---|---:|
| Executed real audits | 20 |
| Target total | 20 |
| Remaining for raw 20-audit target | 0 |
| P0/P1 across latest run | 0/0 |

## Mix Target

The raw 20-audit target is complete. The ideal category mix is not perfect yet; it is intentionally documented instead of hidden.

| Category | Ideal target | Executed | Gap |
|---|---:|---:|---:|
| CLI/API/library | 5 | 11 | +6 |
| SaaS/Next.js/web app | 5 | 2 | -3 |
| Landing/content site | 4 | 2 | -2 |
| Agent/automation | 3 | 2 | -1 |
| Marketplace/extension | 3 | 3 | 0 |

Next proof expansion should add 6 more projects:

- 3 SaaS/Next.js/web app audits
- 2 landing/content site audits
- 1 agent/automation audit

## Executed

| Slot | Project | Category | Evidence |
|---:|---|---|---|
| 1 | `pypa/sampleproject` | CLI/API/library | `benchmarks/real-world/results/pypa-sampleproject/` |
| 2 | `tj/commander.js` | CLI/API/library | `benchmarks/real-world/results/tj-commander-js/` |
| 3 | `jonschlinkert/is-number` | CLI/API/library | `benchmarks/real-world/results/jonschlinkert-is-number/` |
| 4 | `pallets/click` | CLI/API/library | `benchmarks/real-world/results/pallets-click/` |
| 5 | `pallets/itsdangerous` | CLI/API/library | `benchmarks/real-world/results/pallets-itsdangerous/` |
| 6 | `pypa/packaging` | CLI/API/library | `benchmarks/real-world/results/pypa-packaging/` |
| 7 | `nodeca/js-yaml` | CLI/API/library | `benchmarks/real-world/results/nodeca-js-yaml/` |
| 8 | `expressjs/cors` | CLI/API/library | `benchmarks/real-world/results/expressjs-cors/` |
| 9 | `mozilla/readability` | CLI/API/library | `benchmarks/real-world/results/mozilla-readability/` |
| 10 | `sindresorhus/query-string` | CLI/API/library | `benchmarks/real-world/results/sindresorhus-query-string/` |
| 11 | `date-fns/date-fns` | CLI/API/library | `benchmarks/real-world/results/date-fns-date-fns/` |
| 12 | `h5bp/html5-boilerplate` | Landing/content site | `benchmarks/real-world/results/h5bp-html5-boilerplate/` |
| 13 | `11ty/eleventy-base-blog` | Landing/content site | `benchmarks/real-world/results/11ty-eleventy-base-blog/` |
| 14 | `vercel/nextgram` | SaaS/Next.js/web app | `benchmarks/real-world/results/vercel-nextgram/` |
| 15 | `nextauthjs/next-auth-example` | SaaS/Next.js/web app | `benchmarks/real-world/results/nextauthjs-next-auth-example/` |
| 16 | `mdn/webextensions-examples` | Marketplace/extension | `benchmarks/real-world/results/mdn-webextensions-examples/` |
| 17 | `mozilla/webextension-polyfill` | Marketplace/extension | `benchmarks/real-world/results/mozilla-webextension-polyfill/` |
| 18 | `GoogleChrome/chrome-extensions-samples` | Marketplace/extension | `benchmarks/real-world/results/googlechrome-chrome-extensions-samples/` |
| 19 | `actions/github-script` | Agent/automation | `benchmarks/real-world/results/actions-github-script/` |
| 20 | `actions/starter-workflows` | Agent/automation | `benchmarks/real-world/results/actions-starter-workflows/` |

## Acceptance Rule

An audit counts only when:

- the repository or project source is identified;
- command output is captured in `run.json`;
- ShipVitals generated `report.json`;
- the markdown summary includes verdict, score, P0/P1 count, not-verified areas, and commands executed;
- any before/after claim links to both states or explains exactly what changed.
