# /shipvitals

Run ShipVitals as a release gate.

Instructions:

1. Extract product promise and mandatory flows.
2. Run deterministic checks if tools are available.
3. Require runtime/visual evidence for web/UI projects.
4. Scan for secrets, placeholders, fake integrations, skipped tests, and silent failures.
5. Apply score caps.
6. Return READY / ALMOST READY / NOT READY / DEMO ONLY with proof and retest commands.
