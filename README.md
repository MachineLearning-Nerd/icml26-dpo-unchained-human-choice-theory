# DPO Unchained reproduction campaign

This branch freezes the evaluator-visible `5/10` baseline before stronger claim verification.

| Item | Baseline |
| --- | --- |
| Paper | arXiv `2507.07855v4` |
| Judged Space | `DineshAI/j4c3i3a5kH@091825f20ce3d96b380ae87e43acb6633d73e568` |
| Assessment | Five historical checks are real numerical spot-checks, but all five exact theorem contracts remain `BLOCKED` at this baseline. |
| Compute | Hugging Face `cpu-upgrade`; estimated 2 cores; actual allocation and runtime are printed by the run. |
| Fixed command | `uv sync --frozen && uv run --frozen python -m reproduction.run` |

The baseline audit is intentionally not presented as theorem verification. Its purpose is to preserve the judged evidence, pin the paper source, and make the missing evaluator-visible requirements executable.

See `.openresearch/artifacts/baseline/EVAL.md` for the gate result and `.openresearch/artifacts/contracts/claim_contract.json` for the exact claim contracts.

## Experiment log

| Branch/experiment | Purpose | Exact run command | Assessment/outcome | Compute |
| --- | --- | --- | --- | --- |
| `orx/judged-5-10-baseline-audit` | Freeze and audit the judged 5/10 Space revision. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | Pending baseline run. | Hugging Face `cpu-upgrade`; 2-core estimate. |
| `main` | Initial workspace SHA `9db8e7a2cfd33fc000a40571cb89226201f56d1a`. | Not run as an experiment (publication surface). | Presentation-only initial state. | None. |

## Original workspace note

ICML 2026 agent reproduction workspace for j4c3i3a5kH.
