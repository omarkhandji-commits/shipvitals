# Release Proof Protocol

A release-grade audit must produce a release proof bundle.

## Required artifacts

- `shipvitals-report.json`
- `shipvitals-summary.md`
- `shipvitals-findings.csv`
- `shipvitals-html-report.html` when requested
- command transcript or summarized command outputs
- screenshot paths or visual evidence references when relevant
- final verdict and score caps

## Evidence integrity

Each evidence item should include:

- check id;
- check name;
- status;
- evidence level;
- source command or file;
- timestamp if available;
- blocking impact;
- retest command.

## Why this beats generic skills

A generic skill gives advice. ShipVitals leaves a repeatable release artifact that can be reviewed by the builder, client, future agent, or CI system.
