# Falsification Gate

Look for signs that a project only appears finished.

## Search targets

- TODO, FIXME, placeholder, lorem ipsum, coming soon, replace me.
- mock/demo/fake/sample/dummy/stub data in production paths.
- skipped tests: `.skip`, `xit`, `test.todo`, pending tests.
- silent failures: empty catch blocks, swallowed errors, console-only error handling.
- hardcoded users, prices, tokens, API responses, or success states.
- fake integrations: payment/auth/email/API flows that display success without real calls.
- disabled validation, disabled rate limits, permissive CORS, debug routes.

## Rule

A falsification finding is not automatically fatal. It becomes P0/P1 when it affects the core product promise, user trust, payment, auth, data integrity, privacy, or client delivery.
