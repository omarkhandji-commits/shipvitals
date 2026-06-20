# 11ty/eleventy-base-blog

Real open-source benchmark audit.

- Repository: https://github.com/11ty/eleventy-base-blog.git
- Revision: `e37a55c4c4705d7881929de5242ec50448b5eb0b`
- Category: Landing/content site
- Verdict: `ALMOST READY`
- Score: `74`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, visual proof, independent review

## Commands

- `node -e "const fs=require('fs'); const pkg=JSON.parse(fs.readFileSync('package.json','utf8')); if(!pkg.scripts || !fs.existsSync('eleventy.config.js') || !fs.existsSync('content')) process.exit(1)"` -> `0`

## Evidence

- `report.json`
- `run.json`
