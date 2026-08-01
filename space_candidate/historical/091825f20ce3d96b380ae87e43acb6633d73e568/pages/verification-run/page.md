# Verification run


---
<!-- trackio-cell
{"type": "code", "id": "cell_0e8fcba56931", "created_at": "2026-07-31T07:01:16+00:00", "title": "verify all claims", "command": [".venv/bin/python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 0.105}
-->
````bash
$ .venv/bin/python repro/src/verify.py
````

exit 0 · 0.1s


````python title=verify.py
"""verify.py - 5 anchored claims for j4c3i3a5kH (arXiv 2507.07855)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import core as C
OUT = os.path.join(os.path.dirname(__file__), "..", "outputs"); os.makedirs(OUT, exist_ok=True)
v = {"paper": "j4c3i3a5kH", "arxiv": "2507.07855", "checks": {}}
r = C.thm43_composite_loss()
v["checks"]["C0_thm43_composite_loss"] = {"status":"PASS" if r["passed"] else "FAIL",
  "anchor":"Theorem 4.3 / [0]: for any increasing psi, F~ exists strictly proper loss with psi=l0 o F~",
  "precision":f"decomp err {r['decomposition_err_psi_eq_l0_o_Ftilde']:.2e}; log-loss strictly proper {r['log_loss_strictly_proper']}, Brier {r['brier_strictly_proper']}"}
r = C.thm41_regret_bregman()
v["checks"]["C1_thm41_regret_bregman"] = {"status":"PASS" if r["passed"] else "FAIL",
  "anchor":"Theorem 4.1 / [1]: proper-loss regret = Bregman divergence of Bayes risk",
  "precision":f"max |regret - Bregman| by loss: {[(n,round(e,8)) for n,e in r['max_abs_err_by_loss']]}"}
r = C.thm44_dpo_special_case()
v["checks"]["C2_thm44_dpo_special"] = {"status":"PASS" if r["passed"] else "FAIL",
  "anchor":"Theorem 4.4 / [4]: DPO logistic loss is the canonical special case",
  "precision":f"|DPO loss - logistic psi| = {r['dpo_equals_logistic_err']:.2e}"}
r = C.thm42_choice_link()
v["checks"]["C3_thm42_choice_link"] = {"status":"PASS" if r["passed"] else "FAIL",
  "anchor":"Theorem 4.2 / [3]: KLST* choice probability = F(u_i-u_j) (BTL: F=sigmoid)",
  "precision":f"link cond F(-z)+F(z)={r['link_condition_F_neg_z_plus_F_z']:.6f}; symmetry err {r['choice_matrix_symmetry_err']:.2e}"}
r = C.claim4_klstar_axioms()
v["checks"]["C4_klstar_axioms"] = {"status":"PASS" if r["passed"] else "FAIL",
  "anchor":"[2] KLST* axioms (monotonicity, no-abstention boundary, lottery linearity) for BTL",
  "precision":f"monotone {r['monotonicity']}, boundary {r['boundary_no_abstention']}, lottery-lin err {r['lottery_linearity_err']:.3f}"}
v["n_claims_passed"]=sum(1 for c in v["checks"].values() if c["status"]=="PASS"); v["n_claims_total"]=5
v["all_passed"]=all(c["status"]=="PASS" for c in v["checks"].values())
json.dump(v, open(os.path.join(OUT,"verdict.json"),"w"), indent=2)
print(json.dumps(v, indent=2)); print(f"\nSUMMARY: {v['n_claims_passed']}/{v['n_claims_total']} passed, all_passed={v['all_passed']}")

````


````output
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

````
