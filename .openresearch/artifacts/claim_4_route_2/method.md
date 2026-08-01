# Claim 4 route 2: complete finite-domain search

The search exhausts all 125 reciprocal three-alternative probability matrices on the grid `{0, 1/4, 1/2, 3/4, 1}`. For each model it constructs all nine binary lotteries at `alpha=1/2`, checks the complete monotonicity sextuple domain, and uses an independent linear SMT system to decide whether a strictly order-preserving utility-difference representation exists.

Reciprocity makes the zero-abstention graph complete for every `alpha`, so all LCS obligations hold analytically. Monotonicity needs to hold for only one nontrivial `alpha`; the search checks `1/2` exactly.
