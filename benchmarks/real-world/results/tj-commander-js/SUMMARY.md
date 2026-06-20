# tj/commander.js

Real open-source benchmark audit.

- Repository: https://github.com/tj/commander.js.git
- Revision: `ba6d13ddb4243e5913367734f8c159089ffe7834`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `node -e "import('./index.js').then(m => { if (!m.Command || !m.program) process.exit(1); })"` -> `0`

## Evidence

- `report.json`
- `run.json`
