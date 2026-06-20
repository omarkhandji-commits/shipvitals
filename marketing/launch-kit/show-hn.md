# Show HN Draft

Publish this draft after the npm package and public repository are live.

## Title

Show HN: ShipVitals, a release gate for AI-built apps

## Post

ShipVitals checks whether a project has enough evidence to publish, sell, submit, deploy, or deliver.

```bash
npx shipvitals audit .
```

The audit runs project commands and checks runtime proof, visual proof, secrets, fake integrations, skipped tests, handoff requirements, marketplace requirements, and CI repeatability. It writes JSON and Markdown reports with one verdict: `READY`, `ALMOST READY`, `NOT READY`, or `DEMO ONLY`.

The repository contains 20 repeatable open-source audits. UI projects remain capped when visual proof is absent. Public projects remain capped when independent review is absent.

I am looking for reports of:

- false positives;
- missed release blockers;
- install failures;
- verdicts that lack enough evidence.
