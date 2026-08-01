# Constructive proof-certificate route

This route translates the arbitrary-loss identities into symbolic algebra rather than sampling a few named losses. Claim 2 is reduced to the properness inequality and a dimension-free identity. Claim 5 is reduced to the same properness inequality, Fenchel equality at a subgradient, and exact positive-variable algebra for log-loss and sigmoid.

An independent exact-rational checker evaluates multiclass quadratic proper losses in dimensions 2 through 9. Mutating the sign of the subgradient must be detected. An asymmetric strictly proper family checks that the symmetry-only conclusion is not applied to general losses.

Claims 1, 3, and 4 remain `BLOCKED` on this route because their full quantifiers are not discharged.
