# Evidence


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_8154db6c06f2", "created_at": "2026-07-31T07:01:15+00:00", "title": "Verification output (last 40 lines)"}
-->
## Verification output (last 40 lines)

```
{
  "paper": "j4c3i3a5kH",
  "arxiv": "2507.07855",
  "checks": {
    "C0_thm43_composite_loss": {
      "status": "PASS",
      "anchor": "Theorem 4.3 / [0]: for any increasing psi, F~ exists strictly proper loss with psi=l0 o F~",
      "precision": "decomp err 0.00e+00; log-loss strictly proper True, Brier True"
    },
    "C1_thm41_regret_bregman": {
      "status": "PASS",
      "anchor": "Theorem 4.1 / [1]: proper-loss regret = Bregman divergence of Bayes risk",
      "precision": "max |regret - Bregman| by loss: [('log', 2.579e-05), ('brier', 8.5e-07), ('custom', 2.06e-05)]"
    },
    "C2_thm44_dpo_special": {
      "status": "PASS",
      "anchor": "Theorem 4.4 / [4]: DPO logistic loss is the canonical special case",
      "precision": "|DPO loss - logistic psi| = 1.11e-16"
    },
    "C3_thm42_choice_link": {
      "status": "PASS",
      "anchor": "Theorem 4.2 / [3]: KLST* choice probability = F(u_i-u_j) (BTL: F=sigmoid)",
      "precision": "link cond F(-z)+F(z)=1.000000; symmetry err 0.00e+00"
    },
    "C4_klstar_axioms": {
      "status": "PASS",
      "anchor": "[2] KLST* axioms (monotonicity, no-abstention boundary, lottery linearity) for BTL",
      "precision": "monotone True, boundary True, lottery-lin err 0.008"
    }
  },
  "n_claims_passed": 5,
  "n_claims_total": 5,
  "all_passed": true
}

SUMMARY: 5/5 passed, all_passed=True
```
