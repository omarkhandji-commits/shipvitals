# real-before-after

Real improvement evidence from local ShipVitals validation on 2026-06-12.

## Before

- No repeatable real-world OSS benchmark harness.
- Real case-study folders were placeholders.
- `node cli/bin/shipvitals.js --help` printed help but exited with code `1`.
- The runner could not return `READY` even when required proof was supplied.
- `npm run test` failed on Windows because `python3` pointed to an interpreter without `pytest`.
- `npm run test:compile` failed on Windows because `py_compile` did not expand `*.py`.
- First real `tj/commander.js` audit produced a false P0 secret candidate from README password examples: score `59`, verdict `NOT READY`.

## After

- Added `npm run benchmark:real`.
- Added `benchmarks/real-world/manifest.json` with 3 real repositories.
- Generated real reports under `benchmarks/real-world/results/`.
- Added real case studies for pypa/sampleproject, tj/commander.js, and jonschlinkert/is-number.
- Expanded the real-world benchmark suite to 20 executed open-source repositories.
- Added per-project `SUMMARY.md` files beside `report.json` and `run.json`.
- Fixed CLI help exit code and Python fallback for Windows.
- Added explicit runtime/visual/CI/independent-review proof flags.
- Added score caps, proof fields, and report aliases.
- Fixed the secret scanner false positive while preserving real secret detection.
- Fixed additional false P0s from README example keys, SPDX license identifiers, archived examples, and vendored files.

## Measured Result

| Check | Before | After |
|---|---:|---:|
| Real OSS benchmark projects | 0 | 20 |
| Placeholder real case studies | 4 | 0 |
| `--help` exit code | 1 | 0 |
| Windows `npm run test` | fail | pass |
| Windows `npm run test:compile` | fail | pass |
| `tj/commander.js` false P0 | yes | no |
| Full test suite | not passing through npm | 18 Python + 7 Node tests passed |
| Packed npm install | not tested | clean temporary install passed |
| Node CLI Python dependency | required | removed for audit/init/diagnostics |
| Indexable project site | one thin HTML page | 5 validated public pages |

## Current Real Benchmark Summary

Latest run:

- 20 real repositories audited.
- P0/P1: `0/0`.
- CLI/API/library projects: score `89`, capped by missing independent review.
- UI, landing, and extension projects: score `74`, capped by missing visual proof and independent review.

Full table: `benchmarks/real-world/results/SUMMARY.md`.
