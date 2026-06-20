# actions/starter-workflows

Real open-source benchmark audit.

- Repository: https://github.com/actions/starter-workflows.git
- Revision: `1035244887e26fbbd4f1017d919fb5995cc521c4`
- Category: Agent/automation
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `node -e "const fs=require('fs'); if(!fs.existsSync('ci') || !fs.existsSync('automation') || !fs.existsSync('pages')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
