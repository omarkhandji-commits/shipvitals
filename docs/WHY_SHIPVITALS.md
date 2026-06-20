# Why ShipVitals

Coding assistants can produce a convincing interface before the project has release evidence.

Common gaps include:

- a promised user flow that nobody ran;
- a desktop layout with a broken mobile checkout;
- mocked payment, auth, email, or storage integrations;
- skipped tests on the critical path;
- setup instructions that fail on a clean machine;
- missing support, privacy, or handoff requirements.

ShipVitals checks those gaps and records a release verdict.

## Scope

ShipVitals consumes results from tests, Lighthouse, Playwright, security scanners, CI, and human review. It adds product promise, evidence levels, score caps, delivery requirements, and a go/no-go decision.

## Users

- builders using Codex, Claude Code, Cursor, OpenCode, Lovable, Bolt, Replit, or Windsurf;
- freelancers delivering client projects;
- solo builders preparing a launch or submission;
- agencies that require repeatable delivery evidence.

## Evidence Rules

| Missing evidence | ShipVitals response |
|---|---|
| Runtime proof | Cap the score and verdict |
| Real integration | Flag mock or fake core flows |
| Critical test | Surface skipped or absent coverage |
| Mobile proof | Cap UI release verdicts |
| Client handoff | Record missing setup, support, or delivery files |
| Independent review | Cap public and high-stakes releases |

## Boundary

ShipVitals reports the checks it ran and the areas it could not verify. A `READY` verdict describes the evidence available at audit time; it does not certify defect-free software.
