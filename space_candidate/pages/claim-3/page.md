# Claim 3 — FALSIFIED

![Abstention identity](../../images/claim3-abstention.svg)

## Exact contract and assumptions

Definitions 3.2–3.4, v4 anchor `content/normative-framework.tex:48–83`: KLST* combines expandability, local choice structure for every nontrivial `alpha`, and monotonicity for at least one nontrivial `alpha`, and is advertised as permitting abstention through missing zero-abstention edges. Quantifiers cover every context; the certificate fixes an arbitrary context and arbitrary atomic pair. [Contract](../../artifacts/claim_contract.json); [source audit](../../artifacts/source_audit.md).

## Executable verifier and raw result

Current source: [`falsification.py`](../../reproduction/falsification.py), called by [`run.py`](../../reproduction/run.py). Fixed command: `uv sync --frozen && uv run --frozen python -m reproduction.run`.

For arbitrary atoms `a,b` and `L=(ab)_alpha`, expandability plus atomic bearability gives

`p(L>L)−1/2 = alpha(1−alpha)(p(a>b)+p(b>a)−1)`.

Lottery bearability makes the left side zero. Since `alpha∈(0,1)`, the atomic choice sum must equal one for every pair. Z3 returns **UNSAT** for nonzero abstention under these obligations. [Raw JSON](../../artifacts/results.json).

## Independent checker and controls

- Independent checker: SymPy factorization and solution return exactly `choice_sum=1`; Z3 separately rules out `choice_sum<1`.
- Negative control: drop mixed-lottery bearability; an abstaining model becomes **SAT**.
- The proof does not use the monotonicity axiom, so adding it cannot restore abstention.

## Provenance, verdict, and limitation

Scientific SHA `3ada4e95a82907b7f350bc66088d6394c1e4cdef`; seed-free; estimated 2 cores, actual 64 CPUs; HF job 21 s, verifier 0.308565 s; no GPU. **Reviewer verdict: FALSIFIED, confidence HIGH.** The formal KLST* definition remains consistent, but its claimed abstention generalization collapses on the original atomic domain. Altering bearability or expandability could permit abstention, but that is a different structure.
