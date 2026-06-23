# Evidence Manifests

ShipVitals does not treat a filename, note, or arbitrary URL as proof. Each proof flag accepts a JSON manifest ending in .shipvitals-evidence.json.

## Required fields

    {
      "shipvitals_evidence": 1,
      "kind": "runtime",
      "observed_at": "2026-06-22T12:00:00Z",
      "source": "playwright-checkout",
      "summary": "Checkout completed against the release candidate.",
      "artifacts": [{"path": "checkout-trace.zip", "sha256": "64 lowercase hex characters"}]
    }

Supported kinds are runtime, visual, ci, and independent_review.

Local artifacts must remain inside the audited project, be non-empty, and match their SHA-256. Visual artifacts must be an image, video, trace, HAR, or archive.

CI manifests also require a GitHub Actions run_url and a commit equal to the audited Git HEAD. Independent-review manifests require reviewer, decision set to accept, and reviewed_commit equal to the audited Git HEAD.

The machine-readable schema is schemas/evidence-manifest.schema.json.