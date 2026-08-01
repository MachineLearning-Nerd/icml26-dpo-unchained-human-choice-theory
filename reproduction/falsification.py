"""Exact counterexamples and proof-dependency checks."""

from __future__ import annotations

from decimal import Decimal, getcontext

import sympy as sp
from z3 import Real, Solver, sat, unsat


def claim_1_counterexample() -> dict[str, object]:
    """Refute the real-valued endpoint formulation with identity and sigmoid."""
    c = Real("ell0_at_zero")
    proper_solver = Solver()
    proper_solver.add(c <= c - 1)
    contradiction_certified = proper_solver.check() == unsat

    mutated_solver = Solver()
    mutated_solver.add(c >= c - 1)
    reversed_properness_survives = mutated_solver.check() == sat

    t = sp.symbols("t", positive=True)
    q = t / (1 + t)
    sigmoid_lower = sp.simplify(q > 0)
    sigmoid_upper = sp.simplify(q < 1)

    getcontext().prec = 60
    independent_trials = []
    for c_value in [Decimal(-100), Decimal(-3), Decimal(0), Decimal(7), Decimal(100)]:
        z = c_value - 1
        exp_z = z.exp()
        q_value = exp_z / (1 + exp_z)
        independent_trials.append(
            {
                "ell0_at_zero": str(c_value),
                "chosen_z": str(z),
                "q_in_open_unit_interval": 0 < q_value < 1,
                "forced_ell0_q_below_ell0_0": z < c_value,
            }
        )

    p, report = sp.symbols("p report", real=True)
    brier_regret = sp.expand(
        (1 - p) * report**2
        + p * (1 - report) ** 2
        - ((1 - p) * p**2 + p * (1 - p) ** 2)
    )
    brier_control_residual = sp.expand(brier_regret - (report - p) ** 2)

    passed = all(
        [
            contradiction_certified,
            reversed_properness_survives,
            sigmoid_lower is sp.true,
            sigmoid_upper is sp.true,
            all(
                trial["q_in_open_unit_interval"]
                and trial["forced_ell0_q_below_ell0_0"]
                for trial in independent_trials
            ),
            brier_control_residual == 0,
        ]
    )
    if not passed:
        raise AssertionError("Claim 1 counterexample certificate failed")

    return {
        "verdict": "FALSIFIED",
        "exact_statement_scope": "losses are real-valued on the closed probability simplex, as in Definition 3.1 and Section 4.3",
        "witness": {
            "psi": "psi(z)=z",
            "F_tilde": "sigmoid(z)",
            "assumptions": {
                "psi_strictly_increasing_R_to_R": True,
                "F_strictly_increasing_R_to_closed_unit_interval": True,
            },
        },
        "certificate": [
            "decomposition forces ell0(sigmoid(z))=z for every real z",
            "write c=ell0(0), which is finite because the loss is R-valued",
            "properness at true p=0 requires ell0(q)>=c for every q in [0,1]",
            "choose z=c-1 and q=sigmoid(z) in (0,1)",
            "decomposition gives ell0(q)=c-1<c, a contradiction",
        ],
        "smt_properness_and_decomposition": "UNSAT" if contradiction_certified else "SAT",
        "independent_decimal_trials": independent_trials,
        "negative_control": {
            "mutation": "reverse the defining properness inequality",
            "mutant_is_satisfiable": reversed_properness_survives,
        },
        "non_vacuous_instance_control": {
            "psi": "sigmoid(z)^2",
            "ell0(q)": "q^2",
            "ell1(q)": "(1-q)^2",
            "strict_properness_regret": "(q-p)^2",
            "symbolic_residual": str(brier_control_residual),
        },
    }


def claim_3_counterexample() -> dict[str, object]:
    """Show that expandability plus lottery bearability forbids abstention."""
    alpha, s = sp.symbols("alpha s", real=True)
    expanded_self = (
        alpha**2 / 2
        + alpha * (1 - alpha) * s
        + (1 - alpha) ** 2 / 2
    )
    factorized = sp.factor(expanded_self - sp.Rational(1, 2))
    solved_s = sp.solve(sp.Eq(expanded_self, sp.Rational(1, 2)), s)

    a = Real("alpha")
    abstention_sum = Real("choice_sum")
    solver = Solver()
    solver.add(a > 0, a < 1)
    solver.add(abstention_sum < 1)
    solver.add(a * (1 - a) * (abstention_sum - 1) == 0)
    abstention_with_axioms = solver.check()

    control = Solver()
    control.add(a > 0, a < 1, abstention_sum >= 0, abstention_sum < 1)
    abstention_without_mixed_bearability = control.check()

    passed = all(
        [
            factorized == alpha * (1 - alpha) * (s - 1),
            solved_s == [1],
            abstention_with_axioms == unsat,
            abstention_without_mixed_bearability == sat,
        ]
    )
    if not passed:
        raise AssertionError("Claim 3 counterexample certificate failed")

    return {
        "verdict": "FALSIFIED",
        "falsified_phrase": "KLST* permits abstention between alternatives through nonedges",
        "scope": "every pair of atomic alternatives and every alpha in (0,1)",
        "certificate": [
            "fix arbitrary alternatives a,b and L=(ab)_alpha",
            "atomic bearability gives p(a>a)=p(b>b)=1/2",
            "expandability gives p(L>L)=alpha^2/2+alpha(1-alpha)S+(1-alpha)^2/2",
            "lottery bearability gives p(L>L)=1/2",
            "because alpha(1-alpha)>0, S=p(a>b)+p(b>a)=1",
            "therefore every atomic pair is a zero-abstention edge",
        ],
        "symbolic_factor": str(factorized),
        "symbolic_solution_for_choice_sum": [str(value) for value in solved_s],
        "smt_abstention_under_axioms": str(abstention_with_axioms).upper(),
        "negative_control": {
            "mutation": "drop bearability for the mixed lottery L=(ab)_alpha",
            "abstention_then_satisfiable": abstention_without_mixed_bearability == sat,
        },
        "implication": "The formal definition is consistent but collapses to zero abstention on the original alternative domain; it does not provide the advertised abstention generalization.",
    }


def claim_4_proof_dependency_check() -> dict[str, object]:
    """Give a pointwise counterexample to Lemma I used in the published proof."""
    alpha = sp.Rational(1, 2)
    p13, p14, p23, p24 = map(sp.Rational, [2, 5, 5, 2], [5, 5, 5, 5])
    lottery_probability = sp.simplify(
        alpha**2 * p13
        + alpha * (1 - alpha) * p14
        + alpha * (1 - alpha) * p23
        + (1 - alpha) ** 2 * p24
    )
    pointwise_antecedent = lottery_probability >= sp.Rational(1, 2)
    claimed_consequent = p13 >= sp.Rational(1, 2) and p24 >= sp.Rational(1, 2)
    dependency_counterexample = bool(pointwise_antecedent and not claimed_consequent)
    if not dependency_counterexample:
        raise AssertionError("Claim 4 dependency check failed")

    return {
        "verdict": "BLOCKED",
        "published_lemma_counterexample": {
            "alpha": "1/2",
            "p13": str(p13),
            "p14": str(p14),
            "p23": str(p23),
            "p24": str(p24),
            "lottery_probability": str(lottery_probability),
            "antecedent_true": bool(pointwise_antecedent),
            "claimed_consequent_false": not claimed_consequent,
        },
        "reason": "The pointwise Lemma I implication in the supplied proof is false; its argument varies alpha after fixing it. This invalidates that proof route but is not by itself a counterexample satisfying every KLST* axiom, so Theorem 4.2 is not marked FALSIFIED.",
        "corrected_control": "If the lottery preference antecedent held for every alpha arbitrarily close to 0 and 1, endpoint limits would imply the two diagonal preferences.",
    }
