#!/usr/bin/env sh
set -eu
printf 'ShipVitals installer\n'
if command -v npm >/dev/null 2>&1; then
  npm install -g shipvitals
  printf 'Run: shipvitals audit .\n'
elif command -v pipx >/dev/null 2>&1; then
  pipx install shipvitals-cli
  printf 'Run: shipvitals audit .\n'
else
  printf 'Install Node.js/npm or pipx, then run one of:\n  npm install -g shipvitals\n  pipx install shipvitals-cli\n' >&2
  exit 1
fi
