# Evaluation contract

Run exactly:

```text
uv sync --frozen && uv run --frozen python -m reproduction.run
```

The process exits nonzero if a symbolic identity, exact-rational independent check, baseline regression, or mutation-control expectation fails. Accept only the JSON between `DPO_UNCHAINED_EVIDENCE_BEGIN` and `DPO_UNCHAINED_EVIDENCE_END`.
