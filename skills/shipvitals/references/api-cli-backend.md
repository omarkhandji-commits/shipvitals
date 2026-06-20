# API / CLI / Backend Gate

## API

- clear input validation;
- auth/rate limit when public;
- structured errors;
- no stack traces to users;
- docs/examples for core endpoint;
- happy path and failure path tested;
- environment variables documented;
- secrets not committed.

## CLI

- install command works;
- help command works;
- invalid input returns helpful error;
- exit codes are meaningful;
- README includes examples;
- no destructive action without confirmation.
