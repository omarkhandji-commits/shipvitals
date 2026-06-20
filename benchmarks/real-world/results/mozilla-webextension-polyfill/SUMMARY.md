# mozilla/webextension-polyfill

Real open-source benchmark audit.

- Repository: https://github.com/mozilla/webextension-polyfill.git
- Revision: `ff0f24b2e3d816c76330ff931f7cc042c622c123`
- Category: Marketplace/extension
- Verdict: `ALMOST READY`
- Score: `74`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, visual proof, independent review

## Commands

- `node -e "const fs=require('fs'); const pkg=JSON.parse(fs.readFileSync('package.json','utf8')); if(!pkg.name || !fs.existsSync('src/browser-polyfill.js') || !fs.existsSync('api-metadata.json')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
