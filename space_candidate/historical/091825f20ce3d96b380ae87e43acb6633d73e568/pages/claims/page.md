# Claims


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_2d3d0dfb4966", "created_at": "2026-07-31T07:01:14+00:00", "title": "Claims to reproduce"}
-->
## Claims to reproduce

1. Theorem 4.3 proves that for any strictly increasing function ψ, there exists a strictly proper loss pair (ℓ0, ℓ1) such that ψ decomposes as a composition of that loss with a strictly increasing function, generalizing DPO's link beyond the fixed logistic loss (Theorem 4.3, Section 4.3).
2. Theorem 4.1 shows that when the RLHF regularizer R is the regret of a proper loss, R equals a Bregman divergence, generalizing DPO's KL-based regularization to arbitrary Bregman divergences (Theorem 4.1, Section 4.1).
3. The paper introduces a 'KLST*' choice-theoretic structure built on expandability, local choice structure, and monotonicity axioms (Definitions 3.2-3.4) to generalize Bradley-Terry-Luce while allowing abstention (Section 3, Definition 3.4).
4. Theorem 4.2 shows any choice probability with a KLST* structure can be represented as a strictly increasing link function F applied to a difference of latent utility functions, generalizing DPO's BTL-derived link r_theta = f(pi_theta) (Theorem 4.2, Section 4.2).
5. Theorem 4.4 and Corollary 4.5 show that DPO's standard logistic loss and symmetric link are recovered as one special case within the general (proper loss, link function, proper loss) triptych the paper constructs (Theorem 4.4, Corollary 4.5, Section 4.4).
