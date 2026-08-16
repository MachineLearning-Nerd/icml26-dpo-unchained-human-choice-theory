# Branch audit

The published branch names describe the mathematical or release role. Former
orx/ names are retained only as migration provenance; no final remote branch
uses that prefix.

## Pre-dossier snapshot

- Repository: MachineLearning-Nerd/icml26-dpo-unchained-human-choice-theory
- Former repository: MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi
- Default branch: main
- Main tip before this dossier: 7c6e24001085332492ef842083f9efd5ad75479c
- Reachable commits before this dossier: 16 unique commits
- Remote branches before this dossier: 11 (main plus 10 descriptive audit/release branches)
- Recovery bundle: /tmp/icml-dpo-unchained-before-dossier.IAtKIs/dpo-unchained-before-dossier.bundle
- Recovery bundle SHA-256: 938a2df5d71300daf402cd2717d3425b12a67a26a9946caaf3c11ad84539899c
- The bundle was verified complete and contains 24 local/remote refs.

## Final branch map

| Final branch | Former branch | Evidence role | Pre-dossier tip |
| --- | --- | --- | --- |
| main | main | Canonical README, claim dossier, reports, contracts, and evaluator surface | 7c6e24001085332492ef842083f9efd5ad75479c |
| audit/baseline-judged-5-10 | orx/judged-5-10-baseline-audit | Preserves the historical 5/10 judged baseline | 4b1077f36b576d0faa739d65c0aae309161f90f6 |
| audit/constructive-certificates | orx/constructive-proof-certificates | Exact certificates for Claims 2 and 5 | 0f38c345b4b4bcda141fe4eb26e0fd34dd20eb02 |
| audit/claims-1-3-falsification | orx/assumption-satisfying-falsification-search | Exact endpoint and abstention falsifications | 6e1dc0713dd644512e9af40ea0818212761d30d0 |
| audit/claim-4-finite-klst-search | orx/claim-4-exhaustive-finite-klst-search | Exhaustive finite Claim 4 search | ea4620a04a9f136221257e2af234bd6f440219a9 |
| audit/claim-4-representation-reduction | orx/claim-4-representation-reduction-audit | Typed/domain audit of the Claim 4 reduction | f4bbb50835104541744f0de03442eb45584bde89 |
| audit/claim-4-adversarial-falsification | orx/claim-4-adversarial-falsification | Adversarial assumption-satisfying counterexample search | 7a70428af669df1e3adb8ad42bfba661ae72a796 |
| audit/cumulative-four-claim-certificates | orx/cumulative-four-claim-certificates | Cumulative accepted certificates and falsifications | d1d0f66ca0b9b2f50c77ef06b7aecde4b984e2e9 |
| release/evaluator-visible-candidate | orx/evaluator-visible-release-candidate | Evaluator-facing claim pages and result record | 49efaca036052f27fae64775b91072f8d67d2156 |
| release/hugging-face-metadata | orx/hugging-face-metadata-publication-repair | Publication metadata repair only | 5ff0c1e589b4c2cc063d3a3201362ec5723a6cc2 |
| release/post-publication-verification | orx/post-publication-exact-revision-audit | Post-publication source/revision verification | 882597b4f8876af7c326742d83a6f665bb6644bf |

The branch tips are preserved. Documentation additions are intended for main
only and do not rewrite or erase the evidence branches.

## Attribution and safety record

Every reachable pre-dossier commit has both author and committer set to:

    MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>

The dossier commit uses the same identity. Co-author trailers are not used.
The final verifier checks that no refs/original/*, legacy orx/*, or unexpected
branch remains after a fresh clone.
