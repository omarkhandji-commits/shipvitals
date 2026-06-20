# Competitive Comparison

ShipVitals competes in one category:

> Final shipping gate for AI-built apps before publish, sale, submission, deployment, or client delivery.

ShipVitals turns technical, product, runtime, visual, trust, and delivery evidence into one release decision.

## Category Comparison

| Category | Usually stronger at | What it misses | ShipVitals advantage |
|---|---|---|---|
| Code review | language-specific bugs, maintainability | runtime proof, client readiness, final shipping verdict | converts findings into a release decision |
| Unit/integration tests | known behavior under coded assumptions | fake integrations, skipped flows, visual/mobile issues | treats missing proof as risk |
| Lighthouse | web performance, accessibility basics, SEO basics | product promise, payments, auth, handoff, marketplace readiness | includes Lighthouse-type signals inside broader gate |
| Playwright/Cypress | browser automation | business risk, score caps, client delivery, not-verified areas | requires browser proof without pretending it is complete proof |
| Security scanners | vulnerability patterns, dependency risk, secret patterns | UX, onboarding, launch support, false completion | adds security baseline to product readiness |
| Launch checklists | marketing and GTM tasks | test/build/runtime evidence | combines launch readiness with actual project evidence |
| Human audit | judgment and context | repeatability, machine-readable evidence, retest commands | standardizes evidence and retest paths |

## Practical Difference

| Question | Typical tool answer | ShipVitals answer |
|---|---|---|
| Do tests pass? | yes/no | yes/no plus evidence for critical user flows |
| Is Lighthouse green? | score | score plus whether the product can be delivered |
| Are there security issues? | findings | findings plus severity in release context |
| Can I ship? | not answered | `READY`, `ALMOST READY`, `NOT READY`, or `DEMO ONLY` |
| What must I fix first? | list of issues | P0/P1 blockers with smallest useful fix and retest command |

## Real Benchmark Policy

ShipVitals benchmarks must be reproducible:

- every real audit needs `report.json`;
- every run needs metadata and commands executed;
- every summary must include verdict, score, P0/P1 counts, and not-verified areas;
- public projects stay capped below `READY` without independent review evidence.

Current real benchmark reports live in `benchmarks/real-world/results/`.

## Boundary

ShipVitals owns the release verdict. Security teams, product teams, browser suites, CI, and code reviewers own their specialist findings.
