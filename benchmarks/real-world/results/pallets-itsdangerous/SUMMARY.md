# pallets/itsdangerous

Real open-source benchmark audit.

- Repository: https://github.com/pallets/itsdangerous.git
- Revision: `672971d66a2ef9f85151e53283113f33d642dabd`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `1`
- Not verified: runtime proof, independent review

## Commands

- `python -c "import sys; sys.path.insert(0, 'src'); import itsdangerous; assert itsdangerous.URLSafeSerializer"` -> `0`

## Evidence

- `report.json`
- `run.json`
