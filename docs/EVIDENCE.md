# Evidence Manifests

ShipVitals rejects notes, arbitrary files, unverified remote hashes, stale evidence, and evidence from another commit.

## Local runtime and visual evidence

Generate commit-bound evidence after checkout:

    python skills/shipvitals/scripts/shipvitals_create_local_evidence.py . --runtime-command "npm run test:package"
    python skills/shipvitals/scripts/shipvitals_create_local_evidence.py . --visual-file case-studies/shipvitals-self-audit/visual/mobile.png

The files are written under .shipvitals-evidence and expire after 30 days. Runtime proof must be a ShipVitals JSON execution record for the current HEAD. Visual proof must be a real image/video signature or a Playwright trace with trace entries; arbitrary ZIP/HAR/files are rejected. Local paths are resolved through symlinks and cannot leave the project.

## CI provenance

A CI manifest needs run_url and commit. ShipVitals resolves the run through the GitHub API and checks repository, head SHA, URL, and successful conclusion. During the same GitHub Actions run, queued or in-progress status is accepted only when GITHUB_RUN_ID and GITHUB_SHA match the process environment.

## Independent review provenance

L6 requires a GitHub issue or pull-request comment on the audited repository. The comment must contain:

    SHIPVITALS-L6 ACCEPT <full-commit-sha>

The manifest supplies review_url, reviewer, reviewed_commit, and decision set to accept. ShipVitals verifies the comment and account through GitHub. The reviewer must differ from the repository owner, must not be an owner, member, or collaborator, and the account must be at least 90 days old.

Use SHIPVITALS_GITHUB_TOKEN for private repositories or higher GitHub API limits. The GitHub Action passes its scoped token automatically.

The machine-readable format is schemas/evidence-manifest.schema.json.