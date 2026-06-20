# Permissions

ShipVitals should be run with the least permissions possible.

## Default

- local file read;
- local command execution for deterministic checks;
- no network upload;
- no destructive changes.

## Optional

- browser automation for visual proof;
- CI workflow generation;
- hook installation;
- second-model audit using a separate tool chosen by the user.

All optional actions must be explicit.
