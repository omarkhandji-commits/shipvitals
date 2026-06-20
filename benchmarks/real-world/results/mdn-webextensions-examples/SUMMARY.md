# mdn/webextensions-examples

Real open-source benchmark audit.

- Repository: https://github.com/mdn/webextensions-examples.git
- Revision: `ef4192ffa7f74f8bfd12b2808668e0fcc808a7d7`
- Category: Marketplace/extension
- Verdict: `ALMOST READY`
- Score: `74`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, visual proof, independent review

## Commands

- `node -e "const fs=require('fs'); const examples=JSON.parse(fs.readFileSync('examples.json','utf8')); if(!Array.isArray(examples) || examples.length < 10) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
