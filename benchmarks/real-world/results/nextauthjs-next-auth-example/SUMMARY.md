# nextauthjs/next-auth-example

Real open-source benchmark audit.

- Repository: https://github.com/nextauthjs/next-auth-example.git
- Revision: `39ff2b7a375c240a4741866b3818d80fc8edaa5c`
- Category: SaaS/Next.js/web app
- Verdict: `ALMOST READY`
- Score: `74`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, visual proof, independent review

## Commands

- `node -e "const fs=require('fs'); const pkg=JSON.parse(fs.readFileSync('package.json','utf8')); if(!pkg.scripts || !pkg.scripts.build || !fs.existsSync('app') || !fs.existsSync('auth.ts')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
