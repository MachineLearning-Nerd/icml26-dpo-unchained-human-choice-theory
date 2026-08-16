# Audit report

## Decision

**FALSIFIED_CLAIMS_1_AND_3_VERIFIED_CLAIMS_2_AND_5_BLOCKED_CLAIM_4**

This is a scoped audit of the five paper targets. Claims 1 and 3 fail the
explicit contracts recorded in the repository. Claims 2 and 5 have
proof-level algebraic certificates at their stated scope. Claim 4 remains
unresolved after four independent routes; the absence of a finite
counterexample is not a universal proof.

## Evidence decision

- C1: the psi(z)=z, F(z)=sigmoid(z) endpoint witness produces an exact
  contradiction under the finite real-valued contract.
- C2: the proper-loss regret/Bregman identity has symbolic residual 0 and
  survives 200 exact rational trials in dimensions 2–9.
- C3: the stated KLST* axioms force atomic choice sums to one, while the
  abstention control appears only after dropping mixed-lottery bearability.
- C4: the proof dependency has a domain gap; finite and adversarial searches
  found no valid assumption-satisfying counterexample.
- C5: the proper-loss triptych and log-loss/sigmoid/logistic DPO specialization
  reproduce exactly, with asymmetric and sign-error controls.

## Evaluation boundary

The historical live judge score is **5/10**. It is preserved for provenance,
not treated as scientific evidence. The projected 8–9/10 range in the
research notes is a forecast, not an awarded score. This repository does not
claim a new evaluation score, full neural training, or author endorsement.

## Publication state

The former long ORX-named repository is now
MachineLearning-Nerd/icml26-dpo-unchained-human-choice-theory. Its ten
historical ORX branches are represented by descriptive audit/release branches,
and the canonical main branch contains the claim ledger, source and branch
audits, citation, author thanks, environment record, content hashes, and
verify_final.py.
