# tj/commander.js

Real open-source audit evidence.

## Source

- Repository: https://github.com/tj/commander.js.git
- Local benchmark clone: `<system temporary directory>/shipvitals-real-world/tj-commander-js`
- Report: `benchmarks/real-world/results/tj-commander-js/report.json`
- Run log: `benchmarks/real-world/results/tj-commander-js/run.json`

## Result

- Verdict: `ALMOST READY`
- Score: `89`
- Commands executed: `1`
- P0/P1: `0/0`
- Cap: public open-source release missing independent review

## Runtime Proof

- `node -e "import('./index.js').then(m => { if (!m.Command || !m.program) process.exit(1); })"`

## Before/After From Real Benchmark

Initial benchmark run flagged README password examples as secret candidates and returned `NOT READY` with score `59`.

After tightening secret detection to require assignment-like secret values, the same real project returns `ALMOST READY` with score `89` and no P0/P1 findings.
