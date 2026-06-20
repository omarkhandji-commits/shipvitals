# Adversarial Benchmark Set

Use these scenarios to prove ShipVitals catches what generic checklists miss.

1. **Pretty but fake SaaS**: beautiful dashboard, mock data, no real auth, fake payment success.
2. **Landing page slop**: great hero section, dead CTA, broken mobile menu, placeholder testimonials.
3. **Shopify app half-wired**: OAuth present, webhook secret missing, billing not enforced, app review links broken.
4. **API that passes happy path**: no rate limit, silent catch, missing validation, stale OpenAPI docs.
5. **CLI that demos well**: no exit codes, writes unsafe files, no README install path, no tests.
6. **Client dashboard**: works locally, no backup/export, no admin docs, confusing errors.
7. **AI agent workflow**: tool permissions too broad, hallucinated completion, no cost guardrails.
8. **Extension**: excessive permissions, no privacy explanation, broken options page.
9. **Mobile wrapper**: responsive web OK, app store metadata/privacy/screenshots incomplete.
10. **Security trap**: sourcemap exposure, env leakage, dependency warning, public debug route.

The gate should catch P0/P1 issues in at least 9/10 scenarios and produce exact retest steps.
