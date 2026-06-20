# date-fns/date-fns

Real open-source benchmark audit.

- Repository: https://github.com/date-fns/date-fns.git
- Revision: `4098115cf705e3af7f663d8e5b0686e39a9f478a`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `node -e "const fs=require('fs'); const pkg=JSON.parse(fs.readFileSync('package.json','utf8')); if(!pkg.name || !fs.existsSync('pkgs/core')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
