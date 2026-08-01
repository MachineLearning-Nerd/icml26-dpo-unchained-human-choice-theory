# Evaluator-visible evidence matrix

Starting only from [the canonical entrypoint](../index.md), every cell below is directly reachable. “Complete” means the page contains the exact source scope, assumptions, code link, fixed command, inline result, raw link, checker, negative control, limitation, SHA, seeds, CPU/runtime data, and a fail-closed verdict.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](../claim-1/page.md) | [`falsification.py`](../../reproduction/falsification.py) | Complete | [`results.json`](../../artifacts/results.json) | Z3 + Decimal | reversed inequality + Brier | Yes, all `psi,F,z`; endpoint codomain audited | **FALSIFIED / HIGH** |
| 2 | [Claim 2](../claim-2/page.md) | [`proof_certificates.py`](../../reproduction/proof_certificates.py) | Complete | [`results.json`](../../artifacts/results.json) | symbolic + 200 exact fractions | wrong subgradient sign | Yes, arbitrary proper loss/dimension | **VERIFIED / HIGH** |
| 3 | [Claim 3](../claim-3/page.md) | [`falsification.py`](../../reproduction/falsification.py) | Complete | [`results.json`](../../artifacts/results.json) | SymPy + Z3 | remove mixed bearability | Yes, all atomic pairs and nontrivial `alpha` | **FALSIFIED / HIGH** |
| 4 | [Claim 4](../claim-4/page.md) | [four source modules](../../reproduction/adversarial_search.py) | Complete | [`results.json`](../../artifacts/results.json) | exhaustive loop + vectorized integers + SMT | linear pass + cyclic rejection | Yes; universal limitation explicit | **BLOCKED / LOW** |
| 5 | [Claim 5](../claim-5/page.md) | [`proof_certificates.py`](../../reproduction/proof_certificates.py) | Complete | [`results.json`](../../artifacts/results.json) | symbolic + exact asymmetric family | sign mutation + symmetry rejection | Yes, general identity and all real `z` specialization | **VERIFIED / HIGH** |

Environment and exact command: [methodology](../methodology/page.md). Run IDs/SHAs/core estimates/actual allocation/runtime: [`runs.json`](../../artifacts/runs.json). Fail-closed current verifier: [`run.py`](../../reproduction/run.py) and [`release_audit.py`](../../reproduction/release_audit.py). Historical preservation: [historical page](../historical/page.md).
