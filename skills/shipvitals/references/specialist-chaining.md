# Specialist Chaining

ShipVitals is a release gate. It should call for specialists when risk exceeds baseline.

Escalate to a security specialist when:

- auth/payment/PII/health/legal/financial data is involved;
- secrets were found;
- public API has write/destructive operations;
- user-generated content is stored or rendered.

Escalate to deep code review when:

- core logic is complex;
- migrations/data loss risk exists;
- concurrency, billing, permissions, or role logic is non-trivial.

Escalate to Playwright/Lighthouse specialist when:

- web app is public;
- conversion depends on UX;
- mobile/responsive is important;
- visual proof is missing.
