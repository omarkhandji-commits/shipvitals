# Contributing

ShipVitals accepts changes that make release decisions clearer, stricter, or easier to verify.

Good contributions usually do one of three things:

- add better evidence;
- reduce false confidence;
- make the output easier for a builder or client to act on.

Before opening a pull request, run:

```bash
npm run validate
npm run scorecard
npm run schema:check
npm run tone:check
```

Writing rules:

- use plain English;
- avoid hype and inflated scores;
- name the tradeoff when a check is limited;
- mark untested areas as `NOT VERIFIED`;
- give the smallest useful fix, not a vague recommendation.
