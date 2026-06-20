# pypa/sampleproject

Real open-source audit evidence.

## Source

- Repository: https://github.com/pypa/sampleproject.git
- Local benchmark clone: `<system temporary directory>/shipvitals-real-world/pypa-sampleproject`
- Report: `benchmarks/real-world/results/pypa-sampleproject/report.json`
- Run log: `benchmarks/real-world/results/pypa-sampleproject/run.json`

## Result

- Verdict: `ALMOST READY`
- Score: `89`
- Commands executed: `2`
- P0/P1: `0/0`
- Cap: public open-source release missing independent review

## Runtime Proof

- `python -m py_compile src/sample/__init__.py src/sample/simple.py`
- `python -c "import sys; sys.path.insert(0, 'src'); from sample.simple import add_one; assert add_one(5) == 6"`

This is intentionally not marked `READY`: public release projects require independent review evidence for that verdict.
