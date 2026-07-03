# Installation

## Node CLI

Node 18 or newer is required. Python is not required for the Node CLI.

```bash
npx shipvitals audit .
```

To install from a checkout:

```bash
npm link
shipvitals audit /path/to/project
```

## Python CLI

Python 3.10 or newer is required.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install "git+https://github.com/omarkhandji-commits/shipvitals.git"
shipvitals audit .
```

## Agent Skill

Copy `skills/shipvitals/` into the skills directory used by the agent. The folder includes its operating instructions, references, templates, scripts, and OpenAI metadata.

## Verify A Source Checkout

```bash
npm run validate
npm run test
npm run test:package
npm run scorecard
```

Registry commands will replace the GitHub source commands after the npm and PyPI packages pass post-publication install tests.
