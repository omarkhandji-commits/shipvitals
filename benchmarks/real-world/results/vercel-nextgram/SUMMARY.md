# vercel/nextgram

Real open-source benchmark audit.

- Repository: https://github.com/vercel/nextgram.git
- Revision: `e74b34625b9da1d3c8edf3c33dca39986a95f038`
- Category: SaaS/Next.js/web app
- Verdict: `ALMOST READY`
- Score: `74`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, visual proof, independent review

## Commands

- `node -e "const fs=require('fs'); const pkg=JSON.parse(fs.readFileSync('package.json','utf8')); if(!pkg.scripts || !pkg.scripts.build || !fs.existsSync('app')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
