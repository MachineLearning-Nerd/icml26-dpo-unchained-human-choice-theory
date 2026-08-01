# Release forecast and claim summary

- Previous live judged score: `5/10`
- Conservative projected score range after the proposed change: **8–9/10**
- Best-supported possible new score: **9/10 (forecast, not a judge result)**

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 1 | 2 | HIGH | FALSIFIED | Assumption-satisfying identity/sigmoid witness gives an exact endpoint contradiction. Risk: evaluator could interpret losses as extended-real despite the paper's real-valued codomain. |
| 2 | 1 | 2 | HIGH | VERIFIED | Dimension-free derivation plus independent exact rational checks and sign control. Minimal interpretation risk. |
| 3 | 1 | 2 | HIGH | FALSIFIED | Expandability and bearability force zero abstention for arbitrary atomic pairs. Risk is limited to the paper separating mixed-lottery bearability from its stated structure. |
| 4 | 1 | 1 | LOW | BLOCKED | Four routes completed; proof-domain gap found, but no valid counterexample and no repaired proof. It remains unresolved. |
| 5 | 1 | 2 | HIGH | VERIFIED | General canonical identities and full-domain logistic specialization are exact; asymmetric controls isolate symmetry. Minimal risk. |

Current total score: **5/10**, unchanged until a live judge evaluates a new revision. Claims 1–3 and 5 change from historical toy evidence to exact falsification/verification. Claim 4 changes from toy evidence to a rigorously documented `BLOCKED` result after four routes.

No claims are silently skipped. Claim 4 remains `BLOCKED` because neither the cited proof nor the finite searches provide a proof certificate, and no candidate satisfies all KLST* assumptions while contradicting representation. An explicit domain-closure derivation or valid counterexample would unblock it.

Publication action, once every executable gate passes: upload only the paths in [`upload_allowlist.txt`](../../upload_allowlist.txt), verified by the [`SHA-256 manifest`](../../upload_manifest.sha256), through the text-only Hugging Face API to the existing Space `DineshAI/j4c3i3a5kH`; retain the three existing PNGs and every judged file; then download the exact revision, verify hashes and traversal, mirror the published text on GitHub `main`, and mark the paper awaiting judge.
