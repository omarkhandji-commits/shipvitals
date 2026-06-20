# jonschlinkert/is-number

Real open-source benchmark audit.

- Repository: https://github.com/jonschlinkert/is-number.git
- Revision: `98e8ff1da1a89f93d1397a24d7413ed15421c139`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `node -e "const isNumber = require('./'); if (!isNumber('42') || isNumber('x')) process.exit(1);"` -> `0`

## Evidence

- `report.json`
- `run.json`
