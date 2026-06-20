# Real-world Benchmark

This benchmark runs ShipVitals against real open-source repositories, not synthetic fixtures.

## Run

Use existing clones:

```bash
python skills/shipvitals/scripts/shipvitals_real_world_benchmark.py
```

Clone or refresh the repositories first:

```bash
python skills/shipvitals/scripts/shipvitals_real_world_benchmark.py --clone
```

Results are copied to:

```text
benchmarks/real-world/results/
```

## Rule

Do not claim `READY` for public projects without independent review evidence. Runtime smoke proof is enough to show the tool works on real repositories, but public release readiness remains capped until L6 evidence exists.
