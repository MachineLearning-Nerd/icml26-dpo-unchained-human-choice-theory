"""Type-check the published Claim 4 reduction to classical measurement theory."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class AtomicAlternative:
    name: str


@dataclass(frozen=True)
class BinaryLottery:
    left: AtomicAlternative
    right: AtomicAlternative
    alpha: Fraction


def claim_4_reduction_audit() -> dict[str, object]:
    y = AtomicAlternative("y")
    y1 = AtomicAlternative("y1")
    y2 = AtomicAlternative("y2")
    p1 = Fraction(1, 4)
    p2 = Fraction(3, 4)
    target = Fraction(2, 5)
    alpha = (target - p1) / (p2 - p1)
    witness = BinaryLottery(y2, y1, alpha)
    expanded_probability = alpha * p2 + (1 - alpha) * p1

    external_domain = (AtomicAlternative,)
    witness_is_atomic = isinstance(witness, external_domain)
    witness_is_mixed = witness.left != witness.right
    degenerate_embedding_is_atomic = BinaryLottery(y, y, alpha).left == BinaryLottery(
        y, y, alpha
    ).right

    expanded_domain = (AtomicAlternative, BinaryLottery)
    closure_mutation_accepts_witness = isinstance(witness, expanded_domain)

    checks = {
        "alpha_strictly_between_zero_and_one": 0 < alpha < 1,
        "expandability_hits_target_exactly": expanded_probability == target,
        "published_witness_is_mixed_lottery": witness_is_mixed,
        "published_witness_not_in_atomic_domain": not witness_is_atomic,
        "paper_only_identifies_degenerate_lotteries_with_atoms": degenerate_embedding_is_atomic,
        "explicit_closure_axiom_would_accept_witness": closure_mutation_accepts_witness,
    }
    if not all(checks.values()):
        raise AssertionError("Claim 4 representation reduction audit failed")

    return {
        "verdict": "BLOCKED",
        "route": "formal premise and domain audit of the classical representation reduction",
        "checks": checks,
        "exact_example": {
            "p1": str(p1),
            "p2": str(p2),
            "target_q": str(target),
            "alpha": str(alpha),
            "expanded_probability": str(expanded_probability),
            "witness_type": type(witness).__name__,
            "external_theorem_domain_type": AtomicAlternative.__name__,
        },
        "finding": "Expandability constructs a mixed lottery in Y^alpha, while the cited solvability premise is asserted for the atomic domain Y. The paper states equivalence only for degenerate (yy)_alpha lotteries. No axiom closes Y under mixed lotteries or transfers all fixed-alpha axioms to their union.",
        "negative_control": {
            "mutation": "add an explicit domain-closure axiom identifying all mixed lotteries as alternatives",
            "witness_then_type_checks": closure_mutation_accepts_witness,
            "why_not_accepted": "that closure axiom is absent and would change the theorem's antecedent",
        },
        "honest_consequence": "This is a proof-premise gap, not an assumption-satisfying counterexample to the representation conclusion.",
    }
