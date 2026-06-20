# ShipVitals Self-Audit

Real audit of ShipVitals against its own release gate.

## Source

- Project: `ShipVitals`
- Config: `.shipvitals-config.json`
- Public report: `case-studies/shipvitals-self-audit/report.public.json`
- Local raw report: `.shipvitals-evidence/report.json` (gitignored because it contains machine paths and raw output)

## Result

- Verdict: `ALMOST READY`
- Score: `89`
- P0/P1: `0/0`
- Commands executed: `10`
- Real benchmark projects: `20`
- Evidence levels: `L1_STATIC`, `L2_DETERMINISTIC`, `L3_RUNTIME`, `L4_VISUAL_FLOW`
- Missing: `independent review`

## Commands Executed

- `npm run validate`
- `npm run test`
- `npm run test:compile`
- `npm run scorecard`
- `npm run schema:check`
- `npm run tone:check`
- `npm run benchmark:real` (20 real repositories)
- `npm pack --dry-run`
- `npm run test:package`
- `npm run site:check`

## Why 89

ShipVitals is configured for public release. The policy caps its self-audit at 89 until an independent reviewer validates the evidence.

## Current Interpretation

ShipVitals is suitable for beta review. A stable release still requires accepted independent review. The current report was generated on 2026-06-20 with P0/P1 `0/0`; remote CI evidence remains pending until the first public workflow run.

The latest benchmark expansion reached 20 executed real open-source audits with 0 P0/P1 across the generated results. The remaining score cap is independent review, not local test failure.
