# Positioning

## One-Line Description

ShipVitals checks release evidence and returns a go/no-go verdict for projects built with coding assistants.

## Scope

ShipVitals covers:

- product promise and required user flows;
- build, test, lint, type, and package commands;
- runtime and visual proof;
- secret, privacy, and fake-completion signals;
- client handoff and marketplace requirements;
- CI repeatability and independent review.

Specialist tools remain responsible for deep code review, penetration testing, browser automation, and performance analysis. ShipVitals records their output as release evidence.

## Users

- Codex, Claude Code, Cursor, OpenCode, Lovable, Bolt, Replit, and Windsurf users;
- solo product builders;
- freelancers delivering client applications;
- small agencies and marketplace developers.

## User Problem

A generated project can pass superficial checks while critical flows, integrations, mobile states, or delivery requirements remain unverified.

## Output

- `READY`
- `ALMOST READY`
- `NOT READY`
- `DEMO ONLY`
