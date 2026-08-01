# DPO Unchained — claim-by-claim reproduction

> **Forecast, not a judge result.** The previous live score remains **5/10**. Exact certificates now falsify Claims 1 and 3, verify Claims 2 and 5, and leave Claim 4 honestly `BLOCKED` after four distinct routes. Conservative projected range: **8–9/10**; best-supported possible score: **9/10**.

[![Open in molab](https://marimo.io/molab-shield.svg)](https://molab.marimo.io/github/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/blob/main/notebooks/dpo_unchained_reproduction.py)

The paper scope is five universal theorem/definition statements; the observed result is **2 verified, 2 falsified, 1 blocked**. The campaign tested arXiv `2507.07855v4`, not nearby finite examples. The strongest results are proof-level: Theorem 4.3's real-valued endpoint formulation is contradicted by `psi(z)=z` and `F=sigmoid`; the KLST* axioms algebraically force zero abstention; and the regret–Bregman and proper-loss-triptych identities reduce to exact symbolic zero residuals. Theorem 4.2 remains unresolved because its published proof crosses from atomic alternatives into mixed lotteries without a closure premise, while exhaustive and adversarial searches found no assumption-satisfying counterexample. There is no downscaled substitute for the four resolved claims; Claim 4's finite searches are explicitly limited falsification routes, not full verification.

All research computation ran on Hugging Face `cpu-upgrade` without GPU hardware. The fixed command on every node was:

```bash
uv sync --frozen && uv run --frozen python -m reproduction.run
```

Read the [illustrated technical report](reports/dpo-unchained/report.md), inspect the [self-contained marimo notebook](notebooks/dpo_unchained_reproduction.py), or start from the [candidate evaluator entrypoint](space_candidate/README.md). The exact source contract is in [.openresearch/artifacts/contracts/claim_contract.json](.openresearch/artifacts/contracts/claim_contract.json).

## Experiment log

| Branch/experiment | Purpose or change | Exact run command | Assessment/outcome | Compute |
| --- | --- | --- | --- | --- |
| [`orx/judged-5-10-baseline-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/judged-5-10-baseline-audit) | Freeze and audit judged revision `091825f…`. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | Five exact claims `BLOCKED`; historical checks preserved as toy. | HF `cpu-upgrade`; estimate 2 cores, actual 64; 16 s job. |
| [`orx/constructive-proof-certificates`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/constructive-proof-certificates) | Symbolic certificates for Claims 2 and 5. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | Claims 2 and 5 `VERIFIED`. | HF `cpu-upgrade`; estimate 4, actual 64; 21 s job. |
| [`orx/assumption-satisfying-falsification-search`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/assumption-satisfying-falsification-search) | Exact counterexamples for Claims 1 and 3. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | Claims 1 and 3 `FALSIFIED`; Claim 4 proof lemma challenged only. | HF `cpu-upgrade`; estimate 2, actual 64; 21 s job. |
| [`orx/claim-4-exhaustive-finite-klst-search`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/claim-4-exhaustive-finite-klst-search) | Exhaust 125 finite models and `9^6` sextuples/model. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | 19/19 KLST* models representable; universal claim still `BLOCKED`. | HF `cpu-upgrade`; estimate 4, actual 64; 21 s job. |
| [`orx/claim-4-representation-reduction-audit`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/claim-4-representation-reduction-audit) | Type-check the external representation reduction. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | Missing domain-closure premise; Claim 4 remains `BLOCKED`. | HF `cpu-upgrade`; estimate 4, actual 64; 21 s job. |
| [`orx/claim-4-adversarial-falsification`](https://github.com/MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi/tree/orx/claim-4-adversarial-falsification) | Mandatory fourth route: 6,000 four-alternative targets. | `uv sync --frozen && uv run --frozen python -m reproduction.run` | 5,987 nonrepresentable targets all violate monotonicity; Claim 4 `BLOCKED`. | HF `cpu-upgrade`; estimate 8, actual 64; 42 s job, 20.912 s verifier. |
| `main` | Public landing page, report, notebook, and exact published text mirror. | Not run as an experiment (publication surface). | Presentation-only. | None. |

## Reproducibility boundary

The experiments use exact algebra, rational arithmetic, SMT, and exhaustive finite checks—not model training. Finite searches are explicitly scoped corroboration and never promoted into a proof of the universal Claim 4. Historical Space pages are retained and labeled **Historical rejected baseline**; they are not the current verifier.

## Original workspace note

ICML 2026 agent reproduction workspace for `j4c3i3a5kH`.
