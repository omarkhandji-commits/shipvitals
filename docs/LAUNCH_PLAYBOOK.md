# Launch Playbook

Goal: earn organic installs, stars, feedback, and trust without an existing audience.

## Positioning

One-line positioning:

```text
Final shipping gate for AI-built apps.
```

Core message:

```text
Run ShipVitals before you publish, sell, submit, deploy, or deliver an AI-built app.
```

Primary CTA:

```bash
npx shipvitals audit .
```

## Day 1: Public Repository

- Rename repository to `shipvitals`.
- Set the GitHub description and topics from `docs/DIRECTORY_SUBMISSIONS.md`.
- Enable Issues, Discussions, and Releases.
- Tag a beta release only after `npm pack --dry-run`, PyPI build, tests, and benchmark pass.
- Add a pinned issue asking users to share audit reports and false positives.

## Day 2: Package Surfaces

- Publish npm package `shipvitals`.
- Publish PyPI package `shipvitals-cli`.
- Verify clean install in a fresh folder:

```bash
npx shipvitals audit .
pipx install shipvitals-cli
shipvitals audit .
```

- Create a release note with install commands, benchmark links, and known limits.

## Day 3: Passive Discovery

- Submit to relevant awesome lists using `marketing/launch-kit/awesome-list-pr.md`.
- Post Show HN using `marketing/launch-kit/show-hn.md`.
- Post one honest Reddit post in two or three relevant communities.
- Avoid spam. If a community rejects self-promotion, do not repost.

## Weekly Trust Loop

- Add one real-world audit.
- Convert one user report into a case study.
- Fix false positives before adding features.
- Keep `docs/RELEASE_MATURITY.md` current.
- Ship small releases with changelog entries written for users, not only maintainers.

## What Not To Do

- Do not buy stars.
- Do not fake downloads, benchmarks, or independent reviews.
- Do not claim `READY` for projects without proof.
- Do not describe ShipVitals as a replacement for specialist tools.

## Success Metrics

Early signs:

- first 20 organic stars;
- first 100 package downloads;
- first 3 external issues or feedback reports;
- first directory PR accepted or under review;
- first independent audit completed.
