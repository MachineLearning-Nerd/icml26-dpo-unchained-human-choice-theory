# Source audit

## Paper identity

| Source | Record |
| --- | --- |
| Primary paper | [arXiv:2507.07855](https://arxiv.org/abs/2507.07855) |
| Version used by the evidence | arXiv v4 |
| Paper title | DPO Unchained: Your Training Algorithm is Secretly Disentangled in Human Choice Theory (and its Loss' Convexity is Dispensable) |
| Authors | Wenxuan Zhou; Shujian Zhang; Brice Magdalou; John Lambert; Ehsan Amid; Richard Nock; Andrew Hard |
| OpenReview record | [j4c3i3a5kH](https://openreview.net/forum?id=j4c3i3a5kH) |
| Venue note | The current arXiv record carries the ICML 2026 marker |
| Versioned source archive | https://export.arxiv.org/src/2507.07855v4 |
| Source retrieval | 2026-08-02, Asia/Kolkata |
| Source SHA-256 | f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc |
| HTML audit URL | https://ar5iv.labs.arxiv.org/html/2507.07855 |
| HTML SHA-256 | 57d8b089b1cf01d982df693976bf09362cb01b4cd0c5c41a731ccf9f38885d19 |

The versioned arXiv source archive is authoritative for theorem numbering.
The ar5iv service returned the same current HTML for explicit v1–v4 requests,
so the audit records both hashes and does not silently treat an unversioned
HTML rendering as the source of truth.

## Exact anchors and quantifiers

| Claim | v4 source anchor | Exact scope |
| --- | --- | --- |
| C1 | content/generalization.tex:66-71; proof content/appendix-proofs.tex:125-170 | For any strictly increasing psi and F_tilde, there exists a strictly proper binary loss satisfying the equality for every real z. |
| C2 | content/generalization.tex:23-29; proof content/appendix-proofs.tex:4-18 | Proper-loss regret equals the stated Bregman divergence on the simplex. |
| C3 | content/normative-framework.tex:48-83 | Expandability, all nontrivial alpha for local choice, one nontrivial alpha for monotonicity, and every context x. |
| C4 | content/generalization.tex:35-44; proof content/appendix-proofs.tex:20-124 | Every KLST* probability admits the stated increasing utility-difference representation. |
| C5 | content/generalization.tex:96-117; proof content/appendix-proofs.tex:173-212 | General canonical identities for strictly proper binary losses, plus the symmetric log-loss DPO specialization. |

The historical judge aliases Theorems 4.1–4.4 and Corollary 4.5; the v4
source labels above are retained for exact provenance.

## Author implementation

No separate author implementation is identified in the pinned source audit or
the public GitHub search recorded for this repository. This repository is an
independent reproduction and theorem audit; it does not claim code-level
agreement with an official implementation.

## Evidence boundary

- .openresearch/artifacts/source_audit.md preserves the original source
  retrieval record and hashes.
- .openresearch/artifacts/claim_1/ through claim_5/ preserve the claim
  contracts, raw results, checkers, controls, and run metadata.
- space_candidate/artifacts/results.json and runs.json are the released
  machine-readable evidence and historical runtime record.
- The source archive and HTML were pinned externally by hash; the archive is
  not silently replaced by a newer unpinned copy during documentation work.
