# Evaluator-blind pre-publication red team

## Pass 1 — candidate-only traversal

The reviewer was given only the downloaded candidate tree and the evaluator rubric. Files opened, in order:

1. `README.md`
2. `pages/index.md`
3. `pages/claim-1/page.md` through `pages/claim-5/page.md`
4. `artifacts/claim_contract.json`, `artifacts/source_audit.md`, `artifacts/results.json`, `artifacts/runs.json`
5. `reproduction/run.py`, `reproduction/release_audit.py`, and the claim-specific source modules
6. `pyproject.toml`, `uv.lock`
7. `pages/visibility/page.md`, `pages/release-report/page.md`, `pages/historical/page.md`

Unverifiable conclusions found in pass 1: the initial draft did not put the current verifier phrase on the canonical page; it did not state the historical binary retention rule inline; and Claim 4's page did not clearly separate proof-gap evidence from theorem falsification. These were treated as missing.

## Fixes

The canonical page now names the current verifier and superseding SHA. The historical page enumerates all retained binaries and exact hashes. Claim 4 now labels each route's inference boundary and states why its final result is `BLOCKED`.

## Pass 2 — repeated blind traversal

The same entrypoint-only traversal was repeated. Files opened: `README.md`, `pages/index.md`, all five claim pages, `pages/visibility/page.md`, all linked raw/source/environment files, `pages/release-report/page.md`, and `pages/historical/page.md`. Every row exposed the exact contract, assumptions, code, fixed command, inline numbers, raw JSON, checker, control, limitation, SHA/seeds/CPU/runtime, and reviewer verdict. No conclusion required repository knowledge or an OpenResearch dashboard. Missing conclusions: **none**.

The executable [`release_audit.py`](../../reproduction/release_audit.py) repeats the discoverability and integrity checks on Hugging Face compute and exits nonzero on regression.
