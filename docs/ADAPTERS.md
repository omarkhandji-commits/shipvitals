# Adapters

ShipVitals is written as a Claude Skill, but the workflow can be used in Cursor, Codex, Gemini CLI, Windsurf, Lovable, Bolt, Replit, and manual terminal workflows.

## Claude Code

Use `skills/shipvitals/SKILL.md`, `/shipvitals`, and the hook example.

## Codex / Cursor / other agents

Use:

```text
Use the ShipVitals workflow. Start with product promise, run deterministic checks, generate evidence, apply score caps, and give a READY/ALMOST READY/NOT READY/DEMO ONLY verdict.
```

Then run the local scripts manually.
