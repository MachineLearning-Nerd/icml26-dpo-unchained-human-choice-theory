"""Symbolic and exact-arithmetic certificates for the constructive route."""

from __future__ import annotations

import random
from fractions import Fraction

import sympy as sp


def _quadratic_loss(report: list[Fraction], outcome: int) -> Fraction:
    return sum(
        (value - Fraction(index == outcome)) ** 2
        for index, value in enumerate(report)
    )


def _simplex(rng: random.Random, size: int) -> list[Fraction]:
    weights = [rng.randint(1, 97) for _ in range(size)]
    total = sum(weights)
    return [Fraction(weight, total) for weight in weights]


def claim_2_certificate() -> dict[str, object]:
    """Check the dimension-free regret/Bregman algebra and an independent loss."""
    p0, p1, q0, q1 = sp.symbols("p0 p1 q0 q1")
    lp0, lp1, lq0, lq1 = sp.symbols("lp0 lp1 lq0 lq1")

    regret = p0 * lq0 + p1 * lq1 - p0 * lp0 - p1 * lp1
    phi_p = -(p0 * lp0 + p1 * lp1)
    phi_q = -(q0 * lq0 + q1 * lq1)
    bregman = phi_p - phi_q + (p0 - q0) * lq0 + (p1 - q1) * lq1
    symbolic_residual = sp.expand(regret - bregman)

    rng = random.Random(4201)
    exact_trials = 0
    for size in range(2, 10):
        for _ in range(25):
            truth = _simplex(rng, size)
            report = _simplex(rng, size)
            loss_truth = [_quadratic_loss(truth, i) for i in range(size)]
            loss_report = [_quadratic_loss(report, i) for i in range(size)]
            exact_regret = sum(
                truth[i] * (loss_report[i] - loss_truth[i]) for i in range(size)
            )
            expected = sum((truth[i] - report[i]) ** 2 for i in range(size))
            if exact_regret != expected or exact_regret < 0:
                raise AssertionError("independent quadratic-loss checker failed")
            exact_trials += 1

    mutated = phi_p - phi_q - (p0 - q0) * lq0 - (p1 - q1) * lq1
    mutation_witness = sp.expand(regret - mutated).subs(
        {p0: 1, p1: 0, q0: 0, q1: 1, lp0: 0, lp1: 3, lq0: 2, lq1: 0}
    )
    mutation_detected = mutation_witness != 0
    passed = symbolic_residual == 0 and exact_trials == 200 and mutation_detected
    if not passed:
        raise AssertionError("Claim 2 certificate failed")

    return {
        "verdict": "VERIFIED",
        "scope": "arbitrary proper loss and arbitrary simplex dimension",
        "proof_schema": [
            "properness gives p·ell(q)-p·ell(p) >= 0",
            "phi(p)=-p·ell(p) and G(q)=-ell(q)",
            "D_phi,G(p||q)=phi(p)-phi(q)-(p-q)·G(q)",
            "expansion equals p·ell(q)-p·ell(p) identically",
        ],
        "symbolic_residual": str(symbolic_residual),
        "independent_exact_trials": exact_trials,
        "independent_dimensions": list(range(2, 10)),
        "seed": 4201,
        "negative_control": {
            "mutation": "use G=+ell instead of G=-ell",
            "witness_residual": str(mutation_witness),
            "detected": mutation_detected,
        },
    }


def claim_5_certificate() -> dict[str, object]:
    """Check the general proper-loss algebra and the exact DPO specialization."""
    p, q = sp.symbols("p q", real=True)
    l0p, l1p, l0q, l1q = sp.symbols("l0p l1p l0q l1q", real=True)
    phi_p = -(p * l1p + (1 - p) * l0p)
    phi_q = -(q * l1q + (1 - q) * l0q)
    h_p = l0p - l1p
    subgradient_gap = sp.expand(phi_q - phi_p - (q - p) * h_p)
    properness_gap = sp.expand(
        q * l1p + (1 - q) * l0p - q * l1q - (1 - q) * l0q
    )
    subgradient_residual = sp.expand(subgradient_gap - properness_gap)
    fenchel_residual = sp.expand(p * h_p - phi_p - l0p)

    x = sp.symbols("x", positive=True)
    sigmoid = x / (1 + x)
    dpo_h_residual = sp.simplify(
        -sp.log(1 - sigmoid) + sp.log(sigmoid) - sp.log(x)
    )
    dpo_l0_residual = sp.simplify(-sp.log(1 - sigmoid) - sp.log(1 + x))
    dpo_l1_residual = sp.simplify(-sp.log(sigmoid) - sp.log(1 + 1 / x))

    # Outcome-specific constants preserve strict propriety but break symmetry.
    c0, c1 = Fraction(2, 7), Fraction(-3, 11)
    asymmetric_general_trials = 0
    asymmetric_symmetry_failures = 0
    for numerator in range(1, 20):
        report = Fraction(numerator, 20)
        h = 2 * report - 1 + c0 - c1
        phi = -(
            report * ((1 - report) ** 2 + c1)
            + (1 - report) * (report**2 + c0)
        )
        ell0 = report**2 + c0
        if report * h - phi != ell0:
            raise AssertionError("asymmetric general identity failed")
        asymmetric_general_trials += 1

        mirrored_l0 = (1 - report) ** 2 + c0
        ell1 = (1 - report) ** 2 + c1
        if mirrored_l0 != ell1:
            asymmetric_symmetry_failures += 1

    wrong_sign_residual = sp.expand(p * (-h_p) - phi_p - l0p)
    wrong_sign_witness = wrong_sign_residual.subs({p: sp.Rational(1, 3), l0p: 2, l1p: 5})
    mutation_detected = wrong_sign_witness != 0

    passed = all(
        [
            subgradient_residual == 0,
            fenchel_residual == 0,
            dpo_h_residual == 0,
            dpo_l0_residual == 0,
            dpo_l1_residual == 0,
            asymmetric_general_trials == 19,
            asymmetric_symmetry_failures == 19,
            mutation_detected,
        ]
    )
    if not passed:
        raise AssertionError("Claim 5 certificate failed")

    return {
        "verdict": "VERIFIED",
        "scope": "general canonical identities plus full-domain DPO specialization",
        "general_certificate": {
            "subgradient_residual": str(subgradient_residual),
            "fenchel_residual": str(fenchel_residual),
            "logic": "properness gap is nonnegative; Fenchel equality follows at z=H(p)",
        },
        "dpo_certificate": {
            "substitution": "x=exp(z)>0, p=x/(1+x)",
            "H_minus_log_x": str(dpo_h_residual),
            "ell0_minus_log1px": str(dpo_l0_residual),
            "ell1_minus_log1p1overx": str(dpo_l1_residual),
            "conclusion": "ell1(sigmoid(z))=log(1+exp(-z)) exactly",
        },
        "asymmetric_control": {
            "strictly_proper_family": "Brier loss plus outcome-specific constants",
            "general_identity_trials": asymmetric_general_trials,
            "symmetry_identity_failures": asymmetric_symmetry_failures,
        },
        "negative_control": {
            "mutation": "replace H=l0-l1 by H=l1-l0",
            "witness_residual": str(wrong_sign_witness),
            "detected": mutation_detected,
        },
    }
