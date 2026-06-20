# Release checklist

Before publishing a new ShipVitals release:

- [ ] `npm run validate` passes.
- [ ] `npm run test` passes.
- [ ] `npm run test:compile` passes.
- [ ] `npm run test:package` installs and audits from the packed tarball.
- [ ] `npm run site:check` passes.
- [ ] `npm run scorecard` passes.
- [ ] `npm run schema:check` passes.
- [ ] `npm run tone:check` passes.
- [ ] `npm run benchmark:real` passes or documented why skipped.
- [ ] ShipVitals self-audit has 0 P0/P1.
- [ ] GitHub Action output `verdict` is verified.
- [ ] README commands are correct.
- [ ] GitHub Pages canonical URLs, sitemap, and social image are reachable.
- [ ] `skills/shipvitals/SKILL.md` stays short and uses reference files for detail.
- [ ] No score-based branding, hype language, or stale project names remain.
- [ ] Sample reports still match the current report template.
- [ ] The changelog explains what changed in human language.

Release description:

> ShipVitals checks product promise, project commands, runtime proof, visual proof, security baseline, fake-completion risks, and delivery requirements before returning a release verdict.
