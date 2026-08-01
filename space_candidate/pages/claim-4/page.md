# Claim 4 — BLOCKED after four routes

![Four Claim 4 routes](../../images/claim4-routes.svg)

## Exact contract and assumptions

Theorem 4.2, v4 anchors `content/generalization.tex:35–44` and `content/appendix-proofs.tex:20–124`: **every** KLST* choice probability admits functions `u,F` such that `p(y>y'|x)=F(u(x,y)−u(x,y'))` for every context and pair, with strictly increasing `F`, image in `[0,1]`, and `F(−z)+F(z)≤1`. [Contract](../../artifacts/claim_contract.json); [source audit](../../artifacts/source_audit.md).

Finite corroboration cannot verify this universal theorem, and a proof defect alone cannot falsify its conclusion. Confidence therefore remained LOW and triggered exactly three verification routes plus the mandatory fourth falsification route.

## Four materially different routes

1. **Published-lemma audit.** [`falsification.py`](../../reproduction/falsification.py) gives exact probabilities `p13=p24=2/5`, `p14=p23=1`, `alpha=1/2`: the expanded lottery probability is `7/10≥1/2` while both claimed diagonal consequences are false. This breaks a proof step, not the theorem antecedent.
2. **Complete finite-domain search.** [`representation_search.py`](../../reproduction/representation_search.py) exhausts all 125 reciprocal three-alternative models on `{0,1/4,1/2,3/4,1}`. It checks all `9^6=531,441` monotonicity sextuples per candidate. Nineteen models satisfy the finite KLST* obligations; independent SMT finds all 19 representable. A cyclic control is rejected.
3. **Independent representation-reduction audit.** [`reduction_audit.py`](../../reproduction/reduction_audit.py) reconstructs the solvability witness exactly: `p1=1/4`, `p2=3/4`, target `2/5`, `alpha=3/10`. The witness is a mixed lottery in `Y^alpha`, while the cited premise is asserted on atomic `Y`. Adding a closure axiom type-checks the witness, but that axiom is absent and changes the antecedent.
4. **Mandatory adversarial falsification.** [`adversarial_search.py`](../../reproduction/adversarial_search.py) uses seeds `4401,4402,4403` and 2,000 denominator-20 four-alternative candidates each. SMT identifies 5,987 nonrepresentable targets; exact monotonicity rejects all 5,987. Zero valid counterexamples remain. A linear model passes vectorized and independent brute-force checkers; a cyclic target fails with a concrete witness.

[Raw route outputs](../../artifacts/results.json). Fixed command: `uv sync --frozen && uv run --frozen python -m reproduction.run`.

## Provenance, verdict, and limitation

Final scientific SHA `be9e71d16855a80ab75cf19b6aedd0f009ac97d5`; seeds `4401–4403`; estimated 8 cores, actual 64 CPUs; HF job 42 s, verifier 20.912088 s; no GPU. **Reviewer verdict: BLOCKED, confidence LOW.** All four required routes are complete. No valid falsification was found, and neither finite enumeration nor a proof-gap diagnosis establishes the universal theorem. A formal proof closing the atomic/mixed-lottery domain step or an assumption-satisfying counterexample would unblock it.
