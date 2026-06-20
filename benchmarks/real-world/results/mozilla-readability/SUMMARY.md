# mozilla/readability

Real open-source benchmark audit.

- Repository: https://github.com/mozilla/readability.git
- Revision: `08be6b4bdb204dd333c9b7a0cfbc0e730b257252`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `node -e "const Readability=require('./Readability.js'); if(typeof Readability !== 'function') process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
