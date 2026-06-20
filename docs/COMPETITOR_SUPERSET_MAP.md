# Competitor Superset Map

This file defines how ShipVitals intentionally covers the strongest public competitors in the release-gate category.

| Competitor strength | ShipVitals response |
|---|---|
| Production readiness checks | Runner + CI gate + evidence pack + score caps. |
| Visual QA / Playwright | Playwright gate generator + required visual evidence for UI projects. |
| Hooks quality gate | Stop-hook example + CI generator + repeatability requirement. |
| Bouncer / cross-model audit | Independent audit prompt + L6 evidence level + second-auditor protocol. |
| Code review skills | Specialist chaining; code review is a sub-signal, not the final verdict. |
| Security skills | Baseline secret/privacy/supply-chain check + escalation to specialists. |
| Launch checklist | Business/client/marketplace readiness included in final verdict. |
| App store / marketplace review | Marketplace-specific reference files and score caps. |
| QA skill packs | Evidence normalization and release decision across QA outputs. |

## Why this matters

A builder does not need ten disconnected reports. A builder needs one hard answer:

> Can I ship this project now?

ShipVitals is the superset decision layer.
