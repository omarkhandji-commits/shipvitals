# Evidence Standard

ShipVitals uses evidence levels to prevent fake confidence.

| Level | Name | Acceptable proof |
|---|---|---|
| L0 | CLAIMED | User/agent says it works, no proof. Never enough for READY. |
| L1 | STATIC | File inspection, config inspection, code reading. |
| L2 | DETERMINISTIC | Command output: build, lint, test, typecheck, audit, scan. |
| L3 | RUNTIME | App/API/CLI executed locally or in a test environment. |
| L4 | VISUAL_FLOW | Screenshots, console inspection, responsive check, key flow executed. |
| L5 | CI_REPRODUCIBLE | Same checks run in CI/hook with artifacts. |
| L6 | INDEPENDENT | Second model/agent/human verifies the evidence independently. |

Rules:

- Web UI cannot be READY below L4.
- Client delivery cannot be READY without at least L2 plus handoff evidence.
- Marketplace/mobile submissions should target L5 before public submission.
- High-risk security/payment/auth/data projects should seek L6 before serious launch.
