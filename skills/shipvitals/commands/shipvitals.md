# /shipvitals

Run the release gate on the current project.

Required behavior:

1. Extract or ask for the product promise.
2. Run deterministic checks where possible.
3. Require runtime/visual proof before READY for web/UI projects.
4. Apply the falsification gate.
5. Produce verdict first.
6. Never mark READY if checks were not executed or evidence is missing.

Output:

- Verdict
- Score
- Evidence level
- P0/P1 blockers
- Exact fixes
- Retest commands
- Final release decision

To allow `READY`, provide required proof explicitly, for example:

```bash
shipvitals audit . --runtime-proof "artifacts/runtime-trace.zip" --visual-proof "artifacts/mobile.png"
```
