# Publishing

ShipVitals is published on npm. PyPI publishing remains manual until credentials are configured.

## Current Status

- npm package target: `shipvitals`
- PyPI package target: `shipvitals-cli`
- npm registry check: `shipvitals@1.0.0-beta.1` is public
- PyPI registry check: package not found before first publish

## Required Secrets

Configure these GitHub repository secrets before running `.github/workflows/publish.yml`:

- `NPM_TOKEN`: optional for future npm releases; current beta was published locally.
- `PYPI_API_TOKEN`: PyPI API token for `shipvitals-cli`.

## Manual GitHub Publish

1. Open GitHub Actions.
2. Run `Publish Packages`.
3. Select `publish_pypi` for the remaining registry publish, or `publish_npm` for future npm releases.
4. Verify clean installs after publication:

```bash
npx shipvitals audit .
pipx install shipvitals-cli
shipvitals audit .
```

## Local Publish

```bash
npm whoami
npm run test:node
npm run test:package
npm pack --dry-run
npm publish --tag beta --access public --otp <code>
```

```bash
python -m pip install --upgrade build twine
python -m build --sdist --wheel
python -m twine check dist/*
python -m twine upload dist/*
```

Do not publish stable `latest` until independent L6 review, registry clean installs, and external feedback are complete.
