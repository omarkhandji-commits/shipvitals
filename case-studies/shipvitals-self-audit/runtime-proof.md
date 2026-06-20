# Runtime Proof

Observed on 2026-06-19 before the first public push.

- `npm run test:package` packed `shipvitals-1.0.0-beta.1.tgz`.
- The tarball was installed into a new temporary Node project.
- `npx --no-install shipvitals audit .` executed from that project.
- The generated report returned `READY`, P0/P1 `0/0`.
- The fixture command `npm run test` exited `0`.

The repeatable harness is `scripts/npm-smoke.mjs`.
