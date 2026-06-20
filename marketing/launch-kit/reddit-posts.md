# Reddit Drafts

Publish after the npm package and public repository are live. Adapt each post to the community rules.

## r/SideProject

Title:

```text
I built a release gate for AI-built apps
```

Body:

```text
ShipVitals audits a project before launch or client delivery:

npx shipvitals audit .

It runs project commands and records runtime proof, visual proof, secrets, fake integrations, skipped tests, handoff requirements, and unverified areas.

The report returns READY, ALMOST READY, NOT READY, or DEMO ONLY with blockers and retest commands.

The repository contains 20 repeatable open-source audits. I am looking for false-positive reports and missed release blockers.
```

## r/webdev

Title:

```text
Release evidence checks for projects built with coding assistants
```

Body:

```text
Generated applications can pass tests while auth, payment, mobile layouts, environment setup, or support requirements remain unverified.

ShipVitals records those gaps and returns a release verdict:

npx shipvitals audit .

It writes JSON and Markdown reports with evidence, score caps, fixes, and retest commands. The repository includes 20 repeatable audits.

I would value examples of release blockers that normal project commands miss.
```

## r/ClaudeAI or r/ChatGPTCoding

Title:

```text
Release gate for projects built with coding agents
```

Body:

```text
ShipVitals checks a generated project before publication, deployment, or client delivery.

npx shipvitals audit .

It records project commands, runtime and visual proof, secret candidates, fake integrations, skipped tests, handoff requirements, and independent-review evidence.

Missing proof caps the verdict. A public project cannot receive READY from its own self-audit alone.

I am looking for sanitized reports from real agent-built projects.
```
