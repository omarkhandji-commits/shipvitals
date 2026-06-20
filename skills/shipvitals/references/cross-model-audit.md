# Cross-model / independent audit protocol

Use this when the project is paid, public, client-facing, or handles user data.

## Why

An AI agent should not be the only judge of its own work. A premium-grade gate requires an independent critique path when stakes are high.

## Protocol

1. Run deterministic ShipVitals runner.
2. Generate evidence pack.
3. Ask a second model or second agent to audit only the evidence and final report.
4. The second auditor must answer:
 - What did the first auditor miss?
 - Which READY claims are unsupported?
 - Which issues are under-severity?
 - Is the verdict too generous?
5. Merge findings. The stricter verdict wins.

## Cap rule

Without independent audit, public paid/client projects are capped at 94 unless risk is very low.
