# Product Hunt Copy

Publish this copy after npm, PyPI, and the public repository are live.

## Name

ShipVitals

## Tagline

Release evidence and a go/no-go verdict for AI-built apps.

## Description

ShipVitals audits a project before launch or client delivery.

```bash
npx shipvitals audit .
```

It records project commands, runtime and visual proof, secrets, fake integrations, skipped tests, handoff requirements, marketplace requirements, CI evidence, and unverified areas.

The report returns `READY`, `ALMOST READY`, `NOT READY`, or `DEMO ONLY`, with blockers, fixes, and retest commands.

## First Comment

I built ShipVitals after seeing generated projects pass basic checks while critical flows and integrations remained unverified.

The repository includes 20 repeatable open-source audits. I want early users to report false positives, missed blockers, and clean-install failures.
