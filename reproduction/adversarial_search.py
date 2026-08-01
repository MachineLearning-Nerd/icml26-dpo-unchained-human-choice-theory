"""Mandatory fourth route: adversarial Claim 4 counterexample synthesis."""

from __future__ import annotations

import itertools
import random
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from z3 import Real, Solver, sat

ALTERNATIVES = range(4)
LOTTERIES = list(itertools.product(ALTERNATIVES, repeat=2))
UNORDERED_PAIRS = list(itertools.combinations(ALTERNATIVES, 2))
DENOMINATOR = 20


def _atomic_matrix(parameters: tuple[int, ...]) -> list[list[int]]:
    matrix = [[DENOMINATOR // 2 for _ in ALTERNATIVES] for _ in ALTERNATIVES]
    for value, (left, right) in zip(parameters, UNORDERED_PAIRS):
        matrix[left][right] = value
        matrix[right][left] = DENOMINATOR - value
    return matrix


def _lottery_matrix(atomic: list[list[int]]) -> np.ndarray:
    return np.array(
        [
            [
                atomic[a][c] + atomic[a][d] + atomic[b][c] + atomic[b][d]
                for c, d in LOTTERIES
            ]
            for a, b in LOTTERIES
        ],
        dtype=np.int16,
    )


def _representation_model(
    atomic: list[list[int]],
) -> tuple[bool, list[str] | None]:
    utilities = [Real(f"route4_u_{index}") for index in ALTERNATIVES]
    solver = Solver()
    solver.add(utilities[0] == 0)
    ordered_pairs = list(itertools.product(ALTERNATIVES, repeat=2))
    for left in ordered_pairs:
        for right in ordered_pairs:
            probability_left = atomic[left[0]][left[1]]
            probability_right = atomic[right[0]][right[1]]
            difference_left = utilities[left[0]] - utilities[left[1]]
            difference_right = utilities[right[0]] - utilities[right[1]]
            if probability_left < probability_right:
                solver.add(difference_left < difference_right)
            elif probability_left == probability_right:
                solver.add(difference_left == difference_right)
    if solver.check() != sat:
        return False, None
    model = solver.model()
    return True, [str(model.eval(utility)) for utility in utilities]


def _vectorized_monotonicity_witness(
    lottery: np.ndarray,
) -> tuple[int, int, int, int, int, int] | None:
    size = len(LOTTERIES)
    conclusion_fails = lottery[:, :, None, None] < lottery[None, None, :, :]
    for second in range(size):
        for fifth in range(size):
            first_condition = lottery[:, second, None] >= lottery[None, :, fifth]
            second_condition = lottery[second, :, None] >= lottery[fifth, None, :]
            violations = (
                first_condition[:, None, :, None]
                & second_condition[None, :, None, :]
                & conclusion_fails
            )
            indices = np.argwhere(violations)
            if len(indices):
                first, third, fourth, sixth = map(int, indices[0])
                return first, second, third, fourth, fifth, sixth
    return None


def _brute_monotonicity_witness(
    lottery: np.ndarray,
) -> tuple[int, int, int, int, int, int] | None:
    size = len(LOTTERIES)
    for second in range(size):
        for fifth in range(size):
            first_pairs = [
                (first, fourth)
                for first in range(size)
                for fourth in range(size)
                if lottery[first, second] >= lottery[fourth, fifth]
            ]
            second_pairs = [
                (third, sixth)
                for third in range(size)
                for sixth in range(size)
                if lottery[second, third] >= lottery[fifth, sixth]
            ]
            for first, fourth in first_pairs:
                for third, sixth in second_pairs:
                    if lottery[first, third] < lottery[fourth, sixth]:
                        return first, second, third, fourth, fifth, sixth
    return None


def _search_seed(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    trials = 2000
    evaluated = 0
    nonrepresentable = 0
    axiom_satisfying = 0
    counterexample = None
    for _ in range(trials):
        evaluated += 1
        parameters = tuple(rng.randint(0, DENOMINATOR) for _ in UNORDERED_PAIRS)
        atomic = _atomic_matrix(parameters)
        represented, _ = _representation_model(atomic)
        if represented:
            continue
        nonrepresentable += 1
        lottery = _lottery_matrix(atomic)
        if _vectorized_monotonicity_witness(lottery) is not None:
            continue
        axiom_satisfying += 1
        if _brute_monotonicity_witness(lottery) is None:
            counterexample = {
                "seed": seed,
                "parameters": parameters,
                "atomic_probability_numerators_over_20": atomic,
            }
            break
    return {
        "seed": seed,
        "candidate_budget": trials,
        "candidates_evaluated": evaluated,
        "nonrepresentable_candidates": nonrepresentable,
        "axiom_satisfying_nonrepresentable_candidates": axiom_satisfying,
        "counterexample": counterexample,
    }


def claim_4_adversarial_falsification() -> dict[str, object]:
    seeds = [4401, 4402, 4403]
    with ProcessPoolExecutor(max_workers=3) as executor:
        searches = list(executor.map(_search_seed, seeds))

    counterexample = next(
        (search["counterexample"] for search in searches if search["counterexample"]),
        None,
    )

    linear_utilities = [-3, -1, 1, 3]
    linear_atomic = [
        [DENOMINATOR // 2 + linear_utilities[i] - linear_utilities[j] for j in ALTERNATIVES]
        for i in ALTERNATIVES
    ]
    linear_lottery = _lottery_matrix(linear_atomic)
    linear_vectorized = _vectorized_monotonicity_witness(linear_lottery)
    linear_brute = _brute_monotonicity_witness(linear_lottery)
    linear_represented, linear_model = _representation_model(linear_atomic)

    cyclic_atomic = _atomic_matrix((15, 10, 5, 15, 10, 15))
    cyclic_witness = _vectorized_monotonicity_witness(_lottery_matrix(cyclic_atomic))

    controls_pass = all(
        [
            linear_vectorized is None,
            linear_brute is None,
            linear_represented,
            cyclic_witness is not None,
            all(int(search["candidates_evaluated"]) > 0 for search in searches),
            counterexample is not None
            or sum(int(search["candidates_evaluated"]) for search in searches) == 6000,
        ]
    )
    if not controls_pass:
        raise AssertionError("adversarial falsification controls failed")

    if counterexample:
        verdict = "FALSIFIED"
        conclusion = "A synthesized non-representable model passed every finite KLST* obligation with an independent checker."
    else:
        verdict = "BLOCKED"
        conclusion = "No assumption-satisfying counterexample was found. Three searches generated non-representable targets, but every one violated KLST* monotonicity."

    return {
        "verdict": verdict,
        "route": "mandatory fourth route dedicated to falsification",
        "exact_claim": "Every KLST* choice probability has a strictly increasing utility-difference link representation.",
        "assumptions": {
            "expandability": "exact bilinear lottery construction",
            "lcs_all_alpha": "exact from reciprocal probabilities and the complete zero-abstention graph",
            "monotonicity_exists_alpha": "checked at alpha=1/2 over all 16^6 lottery sextuples",
            "representation_negation": "linear SMT infeasibility of every strictly order-preserving utility difference",
        },
        "searches": searches,
        "total_candidates": sum(
            int(search["candidates_evaluated"]) for search in searches
        ),
        "total_nonrepresentable_targets": sum(
            int(search["nonrepresentable_candidates"]) for search in searches
        ),
        "counterexample": counterexample,
        "independent_checker": "vectorized exact-integer monotonicity followed by a separate exhaustive loop before accepting a witness",
        "controls": {
            "linear_representable_model": {
                "vectorized_pass": linear_vectorized is None,
                "independent_brute_pass": linear_brute is None,
                "smt_represented": linear_represented,
                "utility_model": linear_model,
            },
            "cyclic_nonrepresentable_model": {
                "rejected_by_monotonicity": cyclic_witness is not None,
                "witness_indices": list(cyclic_witness) if cyclic_witness else None,
            },
        },
        "conclusion": conclusion,
        "limitation": "A failed counterexample search is not a proof. If no valid witness is found, Claim 4 remains BLOCKED after all four required routes.",
    }
