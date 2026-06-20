# Awesome List PR Copy

Use this draft after the repository has a public URL.

## PR Title

```text
Add ShipVitals release-readiness gate
```

## Entry Fields

- Name: `ShipVitals`
- URL: use the public repository URL
- Description: `Audits release evidence for AI-built apps and returns READY, ALMOST READY, NOT READY, or DEMO ONLY.`

## PR Body

```markdown
ShipVitals audits projects built with coding assistants before publication, deployment, sale, submission, or client delivery.

- command: `npx shipvitals audit .`
- outputs: JSON and Markdown evidence reports
- checks: project commands, runtime and visual proof, secrets, fake integrations, skipped tests, handoff requirements, marketplace requirements, and CI evidence
- benchmark: 20 repeatable open-source audits

The repository uses tests, security review, browser automation, and code review as evidence sources for the release verdict.
```

Confirm that the target list accepts developer tools or agent skills before opening the PR.
