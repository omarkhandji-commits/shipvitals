# jonschlinkert/is-number

Real open-source audit evidence.

## Source

- Repository: https://github.com/jonschlinkert/is-number.git
- Local benchmark clone: `<system temporary directory>/shipvitals-real-world/jonschlinkert-is-number`
- Report: `benchmarks/real-world/results/jonschlinkert-is-number/report.json`
- Run log: `benchmarks/real-world/results/jonschlinkert-is-number/run.json`

## Result

- Verdict: `ALMOST READY`
- Score: `89`
- Commands executed: `1`
- P0/P1: `0/0`
- Cap: public open-source release missing independent review

## Runtime Proof

- `node -e "const isNumber = require('./'); if (!isNumber('42') || isNumber('x')) process.exit(1);"`

This project shows the library smoke-test path: ShipVitals can verify package entrypoint behavior without installing dev dependencies.
