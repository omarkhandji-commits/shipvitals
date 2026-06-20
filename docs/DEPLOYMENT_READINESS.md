# Deployment Readiness

Last local verification: 2026-06-20.

## Current Verdict

`ALMOST READY`, score `89`, P0/P1 `0/0`.

The only current score cap is independent L6 review. Remote CI, registry publication, and external feedback remain separate release requirements.

The public, path-sanitized report is stored at `case-studies/shipvitals-self-audit/report.public.json`.

## Fresh Self-Audit

Generated at `2026-06-20T16:28:47Z` with:

```bash
python skills/shipvitals/scripts/shipvitals_runner.py . --mode deep --ci --timeout 600 \
  --runtime-proof "case-studies/shipvitals-self-audit/runtime-proof.md" \
  --visual-proof "case-studies/shipvitals-self-audit/visual/mobile.png"
```

Ten deterministic commands passed:

- `npm run validate`
- `npm run test`
- `npm run test:compile`
- `npm run scorecard`
- `npm run schema:check`
- `npm run tone:check`
- `npm run benchmark:real`
- `npm pack --dry-run`
- `npm run test:package`
- `npm run site:check`

## Package Evidence

- Python: wheel and sdist built successfully as `shipvitals_cli-1.0.0b1`.
- npm: packed tarball installed into a temporary project and audited successfully.
- Node CLI: seven tests pass, including timeout, saturation, and invalid-proof regressions.
- Python suite: 18 tests pass, including matching adversarial coverage.
- GitHub Action: local metadata validates; remote execution and L5 evidence require the public repository.

## Website Evidence

- Five indexable pages with unique title, description, and canonical URL.
- Sitemap, robots policy, SoftwareApplication JSON-LD, social image, and `llms.txt` present.
- Internal links and sitemap coverage pass `npm run site:check`.
- Desktop render inspected at 1440 px.
- Playwright mobile viewport: `390 px` client width and `390 px` scroll width.

## Real-World Benchmark

The latest run contains 20 public repositories and 0 P0/P1 findings. CLI and library projects remain capped at 89 without independent review. UI, landing, and extension projects remain capped at 74 without observed visual proof.

See `benchmarks/real-world/results/SUMMARY.md` for repository revision, commands, score, and missing-evidence details.

## Release Boundary

Ready for a public source beta after the repository, release tag, Pages site, and remote Action run are live.

Not yet a stable registry release until:

- an independent L6 review is accepted;
- npm and PyPI publication credentials are configured;
- clean installs from the public registries pass;
- external users provide install or false-positive feedback.
