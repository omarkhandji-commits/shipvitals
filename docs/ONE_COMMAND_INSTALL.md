# Source Usage

## CLI

From the repository root:

```bash
npm link
shipvitals audit /path/to/project
```

## As a Claude Skill

Copy this folder into Claude's skills directory:

```text
skills/shipvitals/
```

Then ask:

```text
Use ShipVitals. Audit this project as a release gate.
```

## As a repo quality gate

From this repository root:

```bash
npm run validate
npm run scorecard
```

For a target project:

```bash
python3 skills/shipvitals/scripts/shipvitals_runner.py /path/to/project
```

Output:

```text
.shipvitals-evidence/report.json
.shipvitals-evidence/summary.md
.shipvitals-evidence/shipvitals-report.json
.shipvitals-evidence/shipvitals-summary.md
```

## Generate CI for a target project

```bash
python3 skills/shipvitals/scripts/shipvitals_generate_ci.py /path/to/project
```
