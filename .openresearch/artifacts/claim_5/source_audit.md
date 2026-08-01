# Paper source audit

- Retrieval date: 2026-08-02 (Asia/Kolkata).
- Versioned source URL: `https://export.arxiv.org/src/2507.07855v4`.
- Retrieval User-Agent: browser-compatible Mozilla/Chrome UA with `OpenResearch-Reproduction/1.0` suffix.
- Source archive SHA-256: `f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc`.
- HTML URL: `https://ar5iv.labs.arxiv.org/html/2507.07855`.
- HTML SHA-256: `57d8b089b1cf01d982df693976bf09362cb01b4cd0c5c41a731ccf9f38885d19`.
- Versioning caveat: ar5iv returned the same current HTML for explicit `v1` through `v4`; the versioned arXiv source archive is authoritative for theorem numbering and anchors.

## Exact anchors and quantifiers

| Claim | v4 source anchor | Exact scope |
| --- | --- | --- |
| 1 | `content/generalization.tex:66-71`, proof `content/appendix-proofs.tex:125-170` | For **any** strictly increasing `psi:R->R` and **any** strictly increasing `F_tilde:R->[0,1]`, there **exists** a strictly proper binary loss and the equality holds for all `z`. |
| 2 | `content/generalization.tex:23-29`, proof `content/appendix-proofs.tex:4-18` | If `R` is regret of a proper loss, equality with the stated Bregman divergence holds for policies in the simplex. |
| 3 | `content/normative-framework.tex:48-83` | Expandability; all nontrivial `alpha` for LCS; existence of one nontrivial `alpha` for monotonicity; every context `x`. |
| 4 | `content/generalization.tex:35-44`, proof `content/appendix-proofs.tex:20-124` | For every KLST* choice probability, there exist `F,u`; representation holds for all contexts and alternative pairs. |
| 5 | `content/generalization.tex:96-117`, proof `content/appendix-proofs.tex:173-212` | General canonical identities for every strictly proper binary loss; the DPO specialization additionally uses symmetric log-loss and sigmoid. |

The judge record uses the earlier aliases Theorems 4.1–4.4/Corollary 4.5. The v4 source labels above are used for the campaign; historical aliases remain visible for traceability.
