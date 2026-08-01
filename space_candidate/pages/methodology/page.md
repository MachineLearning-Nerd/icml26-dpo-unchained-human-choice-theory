# Method, environment, and provenance

## Fixed reproducibility contract

Every experiment node inherited one command unchanged:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run
```

The environment uses Python 3.12, one repository-level `.venv`, [`pyproject.toml`](../../pyproject.toml), and the exact [`uv.lock`](../../uv.lock). The image is `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`. Research compute ran only on Hugging Face `cpu-upgrade`; no GPU was requested. [Machine-readable run provenance](../../artifacts/runs.json).

## Independent evidence layers

1. SymPy reconstructs the universal algebra without finite-domain sampling.
2. Z3 checks satisfiability or order-representation constraints independently.
3. Exact `Fraction`/integer implementations check concrete loss and finite choice domains without floating-point tolerance.
4. Every accepted route has a mutation or structural negative control that fails for the intended reason.
5. [`release_audit.py`](../../reproduction/release_audit.py) fails nonzero on verdict drift, missing pages, broken historical hashes, malformed JSON/SVG, secret patterns, notebook failure, or a missing visibility row.

The entrypoint prints actual CPU allocation and verifier runtime. Core requirements were estimated before each run; the estimate, selected flavor, actual allocation, and job runtime are in [`runs.json`](../../artifacts/runs.json). Hugging Face logs did not expose a monetary amount, so the report does not invent one.

## Source integrity

The authoritative v4 arXiv source archive was retrieved on 2026-08-02 with an explicit browser User-Agent. Archive SHA-256: `f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc`. ar5iv HTML SHA-256: `57d8b089b1cf01d982df693976bf09362cb01b4cd0c5c41a731ccf9f38885d19`. Exact anchors and quantifiers are in the [source audit](../../artifacts/source_audit.md).

## Non-circularity

Claims 1, 2, 3, and 5 are resolved algebraically over their full quantified domains. Sample counts are supporting independent checks, not theorem calibration. Claim 4 finite domains and search budgets were selected as falsification attempts, never as evidence that a universal statement is true. The absence of a witness is therefore reported only as `BLOCKED`.
