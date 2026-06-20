# Benchmark Plan

To prove ShipVitals is not "one more skill," benchmark it against at least five project types:

1. assistant-built SaaS dashboard
2. Landing page with pricing/contact/legal flow
3. API/CLI developer tool
4. Shopify or marketplace app
5. Browser extension or automation/agent project

## Method

For each project:

1. Seed realistic issues:
 - broken mobile layout
 - placeholder copy
 - fake integration
 - skipped tests
 - missing legal/privacy page
 - exposed secret pattern
 - broken link
 - unclear product promise
2. Run ShipVitals.
3. Run a technical production readiness tool if available.
4. Run a code review skill/tool if available.
5. Run a visual QA tool if available.
6. Compare findings by:
 - true blockers found
 - false positives
 - specificity of fixes
 - evidence quality
 - ability to make a final release decision

## Success condition

ShipVitals wins when it finds not only code/runtime issues, but also product, delivery, marketplace, falsification, and credibility blockers that specialist tools miss.

## Real-world track

Synthetic cases are not enough. The package also includes `benchmarks/real-world/manifest.json` and `npm run benchmark:real`.

Current real repositories:

1. `pypa/sampleproject`
2. `tj/commander.js`
3. `jonschlinkert/is-number`

The real-world track measures:

1. whether the project can be configured without manual prompt rewriting;
2. whether deterministic smoke commands execute;
3. whether false positives are caught and reduced;
4. whether public release verdicts remain capped without independent review.

Latest generated results live in `benchmarks/real-world/results/`.
