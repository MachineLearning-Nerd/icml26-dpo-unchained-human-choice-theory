# DPO Unchained — independent claim-by-claim reproduction

> This repository is an independent mathematical reproduction and audit of the paper, not the authors' implementation.

## Current status

The audit covers the five theorem/definition statements used by the paper's evaluation. The current evidence record contains two verified claims, two falsified claims, and one unresolved claim:

| Claim | Status | Short result |
| --- | --- | --- |
| 1 | FALSIFIED | The stated real-valued endpoint construction fails for psi(z)=z and F(z)=sigmoid(z). |
| 2 | VERIFIED | Proper-loss regret equals the stated Bayes-risk Bregman divergence. |
| 3 | FALSIFIED | The published KLST* axioms force zero abstention on the stated atomic domain. |
| 4 | BLOCKED | Four routes found a proof-domain gap and no valid counterexample, but no proof is complete. |
| 5 | VERIFIED | The proper-loss triptych and the log-loss/sigmoid/logistic DPO specialization hold exactly. |

The historical live evaluation score was 5/10. The projected 8–9/10 range in the research notes is a forecast, not a judge result.

Publication boundary: publication_allowed=false, score_claim=false, and official_author_endorsement=false. This repository publishes a scoped mathematical audit only; it does not claim a full-paper reproduction, a new evaluation score, or author endorsement.

## Paper and provenance

| Field | Record |
| --- | --- |
| Full title | DPO Unchained: Your Training Algorithm is Secretly Disentangled in Human Choice Theory (and its Loss' Convexity is Dispensable) |
| Authors | Wenxuan Zhou, Shujian Zhang, Brice Magdalou, John Lambert, Ehsan Amid, Richard Nock, Andrew Hard |
| Primary source | [arXiv:2507.07855v4](https://arxiv.org/abs/2507.07855) |
| OpenReview record | [j4c3i3a5kH](https://openreview.net/forum?id=j4c3i3a5kH) |
| Venue marker | ICML 2026, as stated in the current arXiv record |
| Pinned source archive | https://export.arxiv.org/src/2507.07855v4 |
| Source SHA-256 | f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc |
| HTML audit SHA-256 | 57d8b089b1cf01d982df693976bf09362cb01b4cd0c5c41a731ccf9f38885d19 |
| Source audit | [.openresearch/artifacts/source_audit.md](.openresearch/artifacts/source_audit.md) |
| Repository lineage | Formerly icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi |
| Canonical repository | [MachineLearning-Nerd/icml26-dpo-unchained-human-choice-theory](https://github.com/MachineLearning-Nerd/icml26-dpo-unchained-human-choice-theory) |
| Canonical branch | main |
| Official implementation | No separate author implementation is pinned by the paper-source audit or the public GitHub search used here; this reproduction is independent. |

The versioned arXiv source archive is authoritative for theorem numbering. The HTML source returned the same current rendering for explicit v1–v4 requests, so versioned source hashes and source anchors are recorded locally rather than inferred from the HTML.

## Audit dossier

The standardized audit files make the repository inspectable without relying
on a single narrative page:

- CLAIM_EVIDENCE.md — paper anchors, claim contracts, producers, raw evidence,
  controls, statuses, and boundaries.
- SOURCE_AUDIT.md — pinned paper revision, source hashes, theorem anchors, and
  official-code search boundary.
- BRANCH_AUDIT.md — final branch roles, former ORX names, tips, and attribution
  checks.
- ENVIRONMENT.md — fixed command, historical hardware, run IDs, and inputs.
- REPORT.md — concise decision and evaluation boundary.
- CITATION.cff and AUTHOR_THANK_YOU.md — citation and author acknowledgement.
- claims.json and reproduction_verdicts.json — machine-readable claim statuses, production paths, and evidence boundaries.
- AUTONOMOUS_STATE.json — durable continuation and publication state.
- EVIDENCE_MANIFEST.json — content-addressed dossier and evidence hashes.
- verify_final.py — fail-closed final-state verifier.

The publication boundary remains explicit: publication_allowed=false for a
complete paper reproduction or score; score_claim=false and
official_author_endorsement=false. Claims 1 and 3 are literal-contract
falsifications, Claims 2 and 5 are scoped algebraic verifications, and Claim 4
remains blocked.

## What the paper is doing

The paper asks how much of Direct Preference Optimization is genuinely tied to the Bradley–Terry/logistic choice model. Its framework separates preference optimization into three mathematical pieces:

1. Proper losses determine a regret and a Bayes-risk/Bregman regularizer.
2. Human choice theory determines how pairwise preference probabilities depend on utility differences.
3. A canonical proper-loss link recovers the DPO objective as a special case, while allowing broader loss and choice-model families.

The paper's central message is that the training algorithm can be understood through human choice theory and proper-loss identities rather than through logistic-loss convexity alone. This repository tests the exact universal quantifiers, endpoints, domains, and algebraic assumptions. It does not replace theorem-level checks with model training or a nearby finite example.

## Claim-to-evidence ledger

The exact contracts are in [.openresearch/artifacts/contracts/claim_contract.json](.openresearch/artifacts/contracts/claim_contract.json). Each claim has a method, environment, raw output, independent checker output, negative control, and limitations file under [.openresearch/artifacts](.openresearch/artifacts).

### Claim 1 — universal proper composite construction

Paper scope: for every strictly increasing psi from R to R and strictly increasing F from R to [0,1], there exists a strictly proper binary loss satisfying psi(z)=l0(F(z)) for every real z.

Evidence path:

1. [claim_1/method.md](.openresearch/artifacts/claim_1/method.md) fixes the quantifiers and endpoint convention.
2. [reproduction/falsification.py](reproduction/falsification.py) constructs the witness psi(z)=z and F(z)=sigmoid(z).
3. The endpoint value required by properness conflicts with the interior values as z tends to negative infinity.
4. The independent SMT checker returns UNSAT for the required inequality, while reversing the inequality is SAT.
5. A Brier positive control has zero residual; the mutation control is satisfiable.

Verdict: FALSIFIED for the stated finite real-valued closed-simplex formulation. Extended-real endpoint losses would be a different claim and are outside this audit contract.

### Claim 2 — proper-loss regret and Bregman divergence

Paper scope: the regret of every proper loss on the simplex equals the Bregman divergence generated by phi(p)=-L(p,p), with G(q)=-ell(q) as a subgradient selection.

Evidence path:

1. [claim_2/method.md](.openresearch/artifacts/claim_2/method.md) reconstructs the symbolic derivation independently.
2. [reproduction/proof_certificates.py](reproduction/proof_certificates.py) expands the definitions and reduces the residual to zero.
3. Two hundred exact rational trials cover dimensions 2 through 9.
4. The wrong-sign subgradient control produces a nonzero residual of 4.

Verdict: VERIFIED within the stated proper-loss and simplex scope.

### Claim 3 — KLST* and abstention

Paper scope: the KLST* definitions combine expandability, local choice structure for every nontrivial alpha, and monotonicity for some nontrivial alpha, while allowing abstention through nonedges of the zero-abstention graph.

Evidence path:

1. [claim_3/method.md](.openresearch/artifacts/claim_3/method.md) expands the lottery and atomic axioms symbolically.
2. Expandability plus bearability yields alpha(alpha-1)(1-choice_sum)=0.
3. For nontrivial alpha, the axioms force choice_sum=1 on every atomic pair.
4. The SMT checker finds no abstaining model under all stated axioms.
5. Dropping mixed-lottery bearability makes an abstaining model SAT, isolating the responsible premise.

Verdict: FALSIFIED as an abstention-permitting definition on the stated atomic domain. The audit does not claim that every surrounding choice-theory result is false.

### Claim 4 — utility-difference representation

Paper scope: every KLST* choice probability admits p(y>y'|x)=F(u(x,y)-u(x,y')) for an increasing F with the stated range and symmetry condition.

Evidence path:

1. Route 1 finds a counterexample to a pointwise lemma used by the published proof, but not to the theorem's full antecedent.
2. Route 2 exhausts 125 finite reciprocal three-alternative models and all 9^6 monotonicity sextuples per model; 19 models satisfy KLST* and all 19 are represented.
3. Route 3 identifies a domain-typing gap: the reduction constructs mixed lotteries while the external representation premise is asserted on atomic alternatives.
4. Route 4 searches 6,000 deterministic four-alternative denominator-20 targets. It finds 5,987 nonrepresentable targets, but all violate monotonicity; zero valid KLST* counterexamples survive.

The route artifacts are [claim_4](.openresearch/artifacts/claim_4), [claim_4_route_2](.openresearch/artifacts/claim_4_route_2), [claim_4_route_3](.openresearch/artifacts/claim_4_route_3), and [claim_4_route_4](.openresearch/artifacts/claim_4_route_4).

Verdict: BLOCKED. Finite searches are useful falsification attempts, not a proof of a universal theorem. A complete proof must close the atomic/mixed-lottery domain step, or a valid assumption-satisfying counterexample must be found.

### Claim 5 — proper-loss triptych and DPO specialization

Paper scope: for a strictly proper binary loss, H=l0-l1 is a subgradient of phi, the Fenchel identity holds, symmetry supplies the reflected identity, and symmetric log-loss with the sigmoid link recovers logistic DPO.

Evidence path:

1. [claim_5/method.md](.openresearch/artifacts/claim_5/method.md) reconstructs the general identities symbolically.
2. The subgradient and Fenchel residuals are zero.
3. The log-loss/sigmoid/logistic DPO specialization has residuals [0, 0, 0].
4. Nineteen asymmetric strictly proper-loss trials preserve the general identities while rejecting the extra symmetry identity.
5. The wrong-sign control produces residual 2.

Verdict: VERIFIED for the canonical-link and DPO-specialization scopes stated in the contract.

## Branch map

The old ORX prefixes were workspace execution labels. They are retained below only for provenance; the published branch names describe the mathematical or release role.

| Published branch | Former branch | What it does | State |
| --- | --- | --- | --- |
| main | main | Canonical README, reports, notebook, contracts, evidence, and evaluator surface. | Current |
| audit/baseline-judged-5-10 | orx/judged-5-10-baseline-audit | Pins and preserves the historical 5/10 judged baseline. | Historical |
| audit/constructive-certificates | orx/constructive-proof-certificates | Builds exact symbolic certificates for Claims 2 and 5. | Verified evidence |
| audit/claims-1-3-falsification | orx/assumption-satisfying-falsification-search | Produces the exact endpoint and abstention falsifications. | Falsified evidence |
| audit/claim-4-finite-klst-search | orx/claim-4-exhaustive-finite-klst-search | Exhausts the finite Claim 4 grid and monotonicity sextuples. | Scoped blocked route |
| audit/claim-4-representation-reduction | orx/claim-4-representation-reduction-audit | Checks the type/domain assumptions in the representation reduction. | Blocked route |
| audit/claim-4-adversarial-falsification | orx/claim-4-adversarial-falsification | Searches adversarial four-alternative targets for an assumption-satisfying counterexample. | Blocked route |
| audit/cumulative-four-claim-certificates | orx/cumulative-four-claim-certificates | Combines the accepted Claim 1–3 and Claim 5 certificates. | Cumulative evidence |
| release/evaluator-visible-candidate | orx/evaluator-visible-release-candidate | Packages the claim contracts, results, pages, figures, and visible evaluator entrypoint. | Release surface |
| release/hugging-face-metadata | orx/hugging-face-metadata-publication-repair | Repairs evaluator-facing metadata without changing scientific evidence. | Release maintenance |
| release/post-publication-verification | orx/post-publication-exact-revision-audit | Verifies the post-publication source/revision and visible artifact alignment. | Release audit |

All renamed branches point to the same historical commits as their former names. Branch names do not change the claim verdicts.

## Reproduce and inspect

The repository uses Python 3.12 and the committed uv lockfile. From a clean checkout:

    uv sync --frozen
    uv run --frozen python -m reproduction.run

The main evidence surfaces are:

- [Claim contract](.openresearch/artifacts/contracts/claim_contract.json)
- [Pinned source audit](.openresearch/artifacts/source_audit.md)
- [Claim-specific artifacts](.openresearch/artifacts)
- [Independent reproduction entrypoint](reproduction/run.py)
- [Illustrated technical report](reports/dpo-unchained/report.md)
- [Self-contained marimo notebook](notebooks/dpo_unchained_reproduction.py)
- [Evaluator candidate README](space_candidate/README.md)
- [Published result record](space_candidate/artifacts/results.json)
- [Release audit](reproduction/release_audit.py)

The fixed command performs exact algebra, rational arithmetic, SMT checks, and finite searches. It does not train a neural model. Historical research runs used Hugging Face cpu-upgrade hardware, requested no GPU, and reported 64 allocated CPUs.

## Reproduction policy

- Keep the paper version, source hash, claim quantifiers, and acceptance criteria pinned.
- Treat a finite search as scoped evidence, never as a universal proof.
- Keep positive and mutated negative controls beside every claim result.
- Keep historical judge-facing artifacts labeled as historical.
- Record any new result on a descriptive audit or release branch before updating main.
- Do not silently broaden a theorem after a counterexample; state the changed domain explicitly.

## Citation

If this audit or its evidence artifacts are useful, please cite the paper:

    @article{zhou2025dpo,
      title = {DPO Unchained: Your Training Algorithm is Secretly Disentangled in Human Choice Theory (and its Loss' Convexity is Dispensable)},
      author = {Zhou, Wenxuan and Zhang, Shujian and Magdalou, Brice and Lambert, John and Amid, Ehsan and Nock, Richard and Hard, Andrew},
      journal = {arXiv preprint arXiv:2507.07855},
      year = {2025},
      doi = {10.48550/arXiv.2507.07855}
    }

The paper's current arXiv record includes later revisions and the ICML 2026 venue marker; the citation above identifies the arXiv work and should be updated by users if a final proceedings citation is preferred.

## Thank you

Thank you to Wenxuan Zhou, Shujian Zhang, Brice Magdalou, John Lambert, Ehsan Amid, Richard Nock, and Andrew Hard for developing a clear framework connecting DPO, proper losses, and human choice theory. The theorem-level structure made it possible to audit each claim separately, preserve counterexamples and controls, and document exactly where the current evidence is strong or still incomplete. This repository is intended as a respectful, reproducible companion to the paper.

## Limitations

- Claim 1 and Claim 3 are falsifications of the exact contracts recorded here; they do not automatically falsify every repaired or restricted version of the statements.
- Claim 4 remains unresolved. No finite search can substitute for the missing universal proof step.
- The historical 5/10 score is preserved for provenance and is not evidence that the forecasted score was awarded.
- No author implementation was identified for comparison, so code-level agreement with an official implementation cannot be claimed.
- Hardware and run metadata describe the recorded evidence; rerunning the command may produce different wall-clock times.
