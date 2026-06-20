---
name: shipvitals
description: Audit whether a web app, SaaS, API, CLI, Shopify app, browser extension, mobile app, automation, landing page, or client project is ready to publish, submit, deploy, sell, or deliver. Use ShipVitals to collect command, runtime, visual, security, delivery, and independent-review evidence before returning READY, ALMOST READY, NOT READY, or DEMO ONLY.
---

# ShipVitals - Release Gate

## Mission

Decide whether a project is ready to ship.

Do not add features. Do not create a long roadmap. Find what blocks release, prove what was checked, and give a clear decision.

## Truth rule

Never say `READY` without evidence. If a check was not run, label it `NOT VERIFIED`.

A confident claim without proof is a failure of the audit.

## Scope

Use ShipVitals for:

- web apps, SaaS, dashboards, and landing pages;
- APIs, CLIs, and backend tools;
- Shopify and marketplace apps;
- browser extensions;
- mobile apps and store submissions;
- agents, automations, and workflows;
- client projects and handoffs.

## Token rule

Load the smallest useful context. Start with this file and the runner output. Read references only when a verdict, finding, or release type needs that detail.

## Workflow

1. Identify the product promise. Use `templates/product-promise.md` if the promise is unclear.
2. Detect stack and available commands with `scripts/shipvitals_probe.py`.
3. Load references only as needed:
   - Scoring or evidence: `references/evidence-standard.md`, `references/verdict-scoring.md`.
   - Findings: `references/finding-quality.md`.
   - Fake-completion risk: `references/falsification-gate.md`.
   - CI/release repeatability: `references/ci-gate.md`.
   - Web/SaaS/Landing: `references/web-saas-motionvitals.md`.
   - API/CLI/backend: `references/api-cli-backend.md`.
   - Shopify/marketplace: `references/shopify-marketplace.md`.
   - Extension: `references/browser-extension.md`.
   - Mobile/store: `references/mobile-appstore.md`.
   - Agent/automation: `references/ai-agent-workflow.md`.
   - Client delivery: `references/client-delivery.md`.
   - High-risk, paid, public, or client release: `references/specialist-chaining.md`, `references/cross-model-audit.md`.
4. Prefer the runner when commands are available:

```bash
python3 skills/shipvitals/scripts/shipvitals_runner.py .
```

5. If the runner cannot be used, run checks separately:

```bash
python3 skills/shipvitals/scripts/shipvitals_probe.py .
python3 skills/shipvitals/scripts/shipvitals_gate.py .
python3 skills/shipvitals/scripts/shipvitals_falsification_scan.py .
python3 skills/shipvitals/scripts/shipvitals_secret_scan.py .
python3 skills/shipvitals/scripts/shipvitals_link_check.py .
```

6. For UI projects, require runtime and visual evidence before `READY`: desktop screenshot, mobile screenshot, console/page-error check, and at least one key flow.
7. Apply score caps from `references/verdict-scoring.md` and `docs/RELEASE_STANDARD.md`.
8. For paid, public, client, security-sensitive, or marketplace releases, prepare an independent review using `templates/independent-audit-prompt.md`.
9. Produce the final report using `templates/final-report.md` or `templates/release-report.md`.

## READY path

`READY` requires all of these:

- product promise and critical flows;
- deterministic commands executed and passing;
- no P0/P1 findings, secret candidates, or fake core-flow signals;
- runtime proof for any project with critical flows;
- visual proof for UI, web, mobile, extension, landing, Shopify, or marketplace projects.
- independent review for client, paid, public, marketplace, security, auth, payment, or privacy-sensitive releases.

With the runner, pass proof explicitly:

```bash
python3 skills/shipvitals/scripts/shipvitals_runner.py . --runtime-proof "artifacts/runtime-trace.zip" --visual-proof "artifacts/mobile.png"
```

## Verdicts

- `READY`: no P0/P1 issues and enough evidence for the release type.
- `ALMOST READY`: close, but important fixes remain.
- `NOT READY`: blocked by critical issues, serious risk, or missing required proof.
- `DEMO ONLY`: acceptable for demonstration, not for paying users, reviewers, or client delivery.

## Severity

- `P0`: release blocker.
- `P1`: serious user, client, security, or credibility risk.
- `P2`: should be fixed before a serious launch.
- `P3`: optional improvement.

## Finding standard

Every finding must include:

- severity;
- area;
- location;
- evidence;
- why it matters;
- smallest useful fix;
- owner or tool;
- retest command.

Avoid vague findings like "improve UI", "add tests", or "make it cleaner".

## Release proof

For serious releases, produce or request:

1. product promise;
2. command evidence;
3. falsification scan;
4. secret/privacy baseline;
5. runtime/visual proof when relevant;
6. CI or hook repeatability;
7. machine-readable evidence pack;
8. independent review prompt when stakes are high;
9. final go/no-go report;
10. retest commands for blockers.

If any item cannot be executed, mark it `NOT VERIFIED` and apply the correct score cap.

## Final answer style

Give the verdict first. Then give the score, cap, blockers, evidence, required fixes, and retest plan.

Be specific. Be calm. No hype. No long roadmap unless the user asks for one.
