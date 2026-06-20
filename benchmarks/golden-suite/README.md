# Golden Benchmark Suite

This benchmark suite is the public proof plan for ShipVitals.

It defines intentionally flawed AI-assisted projects and the defects a release-gate skill should catch.

## Benchmark cases

1. assistant-built SaaS dashboard with fake auth, placeholder pricing, mobile overflow, skipped tests.
2. Shopify app with missing privacy route, fake billing integration, weak app-store copy.
3. API/CLI with exposed sample token, silent error handling, no rate limit, incomplete README.
4. Landing page with dead links, generic generated copy, no support/contact, broken mobile CTA.
5. Browser extension with overbroad permissions, no privacy disclosure, incomplete onboarding.

## Pass condition

A competing tool should catch the release blockers and produce a clear go/no-go decision with retest steps. ShipVitals should produce one normalized verdict across all categories.
