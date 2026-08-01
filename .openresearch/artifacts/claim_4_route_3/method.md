# Claim 4 route 3: representation-reduction audit

This route independently type-checks the paper's reduction to the classical Chapter 17, Theorem 2 representation result. The paper claims expandability satisfies the classical solvability premise on the atomic domain `Y`, but its witness is the mixed lottery `(y2 y1)_alpha`, whose declared domain is `Y^alpha`.

The checker verifies exact interpolation and then verifies the domain mismatch. A mutation adding an explicit closure axiom makes the witness type-check; that control is not accepted because the axiom is absent from KLST* and changes the antecedent.
