# X / LinkedIn Draft

Publish after the npm package and public repository are live.

1. Generated projects can pass basic checks while critical flows, integrations, and delivery requirements remain unverified.

2. ShipVitals runs a release audit before publication or client delivery.

```bash
npx shipvitals audit .
```

3. It returns `READY`, `ALMOST READY`, `NOT READY`, or `DEMO ONLY` with evidence and retest commands.

4. The repository contains 20 repeatable audits across libraries, web apps, sites, browser extensions, and automation projects.

5. Missing runtime, visual, CI, or independent-review evidence caps the verdict.

6. Open an issue with a sanitized report if ShipVitals misses a blocker or flags a false positive.
