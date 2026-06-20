# pypa/sampleproject

Real open-source benchmark audit.

- Repository: https://github.com/pypa/sampleproject.git
- Revision: `621e4974ca25ce531773def586ba3ed8e736b3fc`
- Category: CLI/API/library
- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `2`
- Not verified: runtime proof, independent review

## Commands

- `python -m py_compile src/sample/__init__.py src/sample/simple.py` -> `0`
- `python -c "import sys; sys.path.insert(0, 'src'); from sample.simple import add_one; assert add_one(5) == 6"` -> `0`

## Evidence

- `report.json`
- `run.json`
