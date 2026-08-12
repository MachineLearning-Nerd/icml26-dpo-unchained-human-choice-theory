# Status — DPO Unchained

## Identification

- Paper: DPO Unchained: Your Training Algorithm is Secretly Disentangled in Human Choice Theory (and its Loss' Convexity is Dispensable)
- Authors: Wenxuan Zhou, Shujian Zhang, Brice Magdalou, John Lambert, Ehsan Amid, Richard Nock, Andrew Hard
- Source: arXiv:2507.07855v4
- OpenReview: j4c3i3a5kH
- Venue marker: ICML 2026
- Source archive SHA-256: f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc
- Former repository: icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi
- Current repository: icml26-dpo-unchained-human-choice-theory
- Canonical branch: main

## Scientific checkpoint

| Claim | Verdict | Evidence checkpoint |
| --- | --- | --- |
| 1 | FALSIFIED | Endpoint contradiction for psi(z)=z and F(z)=sigmoid(z); SMT and positive/mutation controls. |
| 2 | VERIFIED | Symbolic Bregman/regret identity and 200 exact rational trials in dimensions 2–9. |
| 3 | FALSIFIED | KLST* algebra forces atomic choice sum to one; abstention model only appears after dropping bearability. |
| 4 | BLOCKED | Four routes complete; no valid counterexample and no proof closing the mixed-lottery domain gap. |
| 5 | VERIFIED | Proper-loss triptych, Fenchel identity, and exact log-loss/sigmoid/logistic DPO specialization. |

Overall: 2 verified, 2 falsified, 1 blocked.

## Reproduction checkpoint

- Fixed command: uv sync --frozen && uv run --frozen python -m reproduction.run
- Environment: Python 3.12 with uv.lock
- Compute recorded: Hugging Face cpu-upgrade, no GPU, 64 allocated CPUs
- Historical live score: 5/10
- Forecast in research notes: 8–9/10, not a judge result
- Scientific evidence commit before documentation cleanup: be9e71d16855a80ab75cf19b6aedd0f009ac97d5

## Publication checkpoint

- Main is the canonical documentation and evaluator-visible surface.
- Claim contracts and per-claim evidence are committed under .openresearch/artifacts.
- Historical branches are preserved under descriptive audit/release names.
- The paper source hash and theorem anchors are recorded in .openresearch/artifacts/source_audit.md.
- The audit is independent; no separate author implementation was identified for code-level comparison.
- Reachable commit attribution is normalized to MachineLearning-Nerd.
- The GitHub repository is renamed to icml26-dpo-unchained-human-choice-theory.
- The old ORX branch names are deleted; ten descriptive audit/release branches remain beside main.
