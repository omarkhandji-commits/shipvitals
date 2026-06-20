# CI gate requirements

ShipVitals should be repeatable in CI when used seriously.

Minimum CI layers:

1. install dependencies;
2. lint/typecheck when present;
3. tests when present;
4. secret scan;
5. falsification scan;
6. link check for docs/static pages;
7. generated evidence pack;
8. fail on P0/P1 unless explicitly waived with reason.

A local-only manual audit can be useful, but cannot receive premium-grade.
