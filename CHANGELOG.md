# Changelog

## 1.0.0-beta.1

- Added a native Node audit engine so the npm CLI no longer requires Python.
- Added Node CLI tests for clean audits, secrets, UI evidence caps, and project initialization.
- Added a packed-package smoke test that installs the generated tarball and runs `npx --no-install shipvitals audit .`.
- Added Windows, macOS, Node 18, Node 20, and Node 22 CI coverage.
- Added an indexable GitHub Pages site with five public pages, canonical URLs, structured data, sitemap, robots policy, and `llms.txt`.
- Added automated validation for page metadata, JSON-LD, sitemap coverage, and internal links.
- Added repository metadata, dependency updates, code ownership, pull-request guidance, and community conduct policy.
- Added adversarial regressions for command timeouts, scan saturation, invalid proof, and blocking Action behavior after independent review.
- Pinned all 20 open-source benchmarks to Git revisions and added commands and revisions to the aggregate summary.
- Removed local path leakage from public benchmark and self-audit artifacts.
- Replaced the README with source-install, evidence, benchmark, and release-status documentation.
- Expanded real-world benchmarks from 3 to 20 executed open-source audits.
- Added per-project benchmark summaries with verdict, score, P0/P1, commands, and not-verified areas.
- Tuned secret blocking to avoid false P0s from README examples, archived samples, vendored files, and SPDX license identifiers.
- Added launch kit copy for Show HN, Reddit, X/LinkedIn, Product Hunt, awesome-list PRs, and short replies.
- Added GitHub issue templates for bugs, false positives, audit examples, and feature requests.
- Added public docs for product scope, launch execution, directory submissions, and release maturity.
- Added a 20-project benchmark tracker with generated evidence.
- Added a pending independent-review case study required before lifting the self-audit score cap.
- Expanded npm keywords for AI coding, release readiness, GitHub Action, and agent-skill discovery.

## 0.9.0

- Added CLI entry points for npm and Python.
- Added project config memory with `.shipvitals-config.json`.
- Added interview wizard, quick audit mode, and deep audit mode.
- Added JSON verdict rules, evidence levels, severity rules, and decision tree.
- Added framework adapters, diagnostics, client report templates, tests, CI, and benchmark scaffolding.
- Removed exaggerated version names and kept plain ShipVitals branding.
