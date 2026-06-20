# ShipVitals GitHub Action

Run the release-readiness gate in CI:

```yaml
steps:
  - uses: actions/checkout@v4
  - id: shipvitals
    uses: omarkhandji-commits/shipvitals@v1
    with:
      path: .
      mode: deep
      ci-proof: "GitHub Actions run"
```

The Action writes `.shipvitals-evidence/report.json` and exposes the `verdict` output. Runtime, visual, and independent proof remain explicit inputs; the Action does not infer evidence it did not observe.
