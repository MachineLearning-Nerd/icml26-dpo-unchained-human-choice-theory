# Evaluation contract

Run exactly:

```text
uv sync --frozen && uv run --frozen python -m reproduction.run
```

The verifier exits nonzero unless both falsification certificates, their independent checks, mutation controls, and the historical baseline regression pass. `FALSIFIED` is used only where the witness satisfies the exact stated assumptions.
