# Architecture

ShipVitals is split for progressive disclosure:

- `SKILL.md` gives the core workflow and routing.
- `references/` contains domain-specific gates.
- `scripts/` provides deterministic local checks.
- `templates/` standardizes reports and audit prompts.
- `agents/` defines specialist reviewer roles.
- `schemas/` keeps evidence/report output machine-readable.
- `benchmarks/` and `evals/` support regression testing.

This follows the professional skill pattern: short entrypoint, specialized references, executable helpers, and reproducible evidence.
