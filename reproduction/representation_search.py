"""Complete finite-domain search for a Claim 4 counterexample."""

from __future__ import annotations

import itertools

from z3 import Real, Solver, sat


GRID = range(5)
ALTERNATIVES = range(3)
LOTTERIES = list(itertools.product(ALTERNATIVES, repeat=2))


def _atomic_matrix(parameters: tuple[int, int, int]) -> list[list[int]]:
    matrix = [[2 for _ in ALTERNATIVES] for _ in ALTERNATIVES]
    for value, (left, right) in zip(parameters, [(0, 1), (0, 2), (1, 2)]):
        matrix[left][right] = value
        matrix[right][left] = 4 - value
    return matrix


def _lottery_matrix(atomic: list[list[int]]) -> list[list[int]]:
    return [
        [
            atomic[a][c] + atomic[a][d] + atomic[b][c] + atomic[b][d]
            for c, d in LOTTERIES
        ]
        for a, b in LOTTERIES
    ]


def _monotonicity_witness(
    lottery: list[list[int]],
) -> tuple[int, int, int, int, int, int] | None:
    size = len(LOTTERIES)
    for second in range(size):
        for fifth in range(size):
            first_pairs = [
                (first, fourth)
                for first in range(size)
                for fourth in range(size)
                if lottery[first][second] >= lottery[fourth][fifth]
            ]
            second_pairs = [
                (third, sixth)
                for third in range(size)
                for sixth in range(size)
                if lottery[second][third] >= lottery[fifth][sixth]
            ]
            for first, fourth in first_pairs:
                for third, sixth in second_pairs:
                    if lottery[first][third] < lottery[fourth][sixth]:
                        return first, second, third, fourth, fifth, sixth
    return None


def _representation_model(
    atomic: list[list[int]],
) -> tuple[bool, list[str] | None]:
    utilities = [Real(f"u_{index}") for index in ALTERNATIVES]
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


def claim_4_exhaustive_search() -> dict[str, object]:
    total_models = 0
    klst_models = 0
    represented_models = 0
    counterexample = None

    for parameters in itertools.product(GRID, repeat=3):
        total_models += 1
        atomic = _atomic_matrix(parameters)
        lottery = _lottery_matrix(atomic)
        if _monotonicity_witness(lottery) is not None:
            continue
        klst_models += 1
        represented, utilities = _representation_model(atomic)
        if represented:
            represented_models += 1
            continue
        if counterexample is None:
            counterexample = {
                "grid_parameters": parameters,
                "atomic_probability_numerators_over_4": atomic,
            }

    cyclic = _atomic_matrix((3, 1, 3))
    cyclic_witness = _monotonicity_witness(_lottery_matrix(cyclic))
    negative_control_detected = cyclic_witness is not None

    if total_models != 125 or not negative_control_detected:
        raise AssertionError("finite search coverage or negative control failed")
    if counterexample is None and klst_models != represented_models:
        raise AssertionError("model accounting failed")

    if counterexample is not None:
        verdict = "FALSIFIED"
        conclusion = "A complete finite-domain KLST* counterexample lacks a difference-utility representation."
    else:
        verdict = "BLOCKED"
        conclusion = "Every KLST* model on this complete grid was representable; finite corroboration does not prove the universal theorem."

    return {
        "verdict": verdict,
        "route": "complete finite rational-domain falsification search",
        "domain": {
            "alternatives": 3,
            "directed_pair_probability_grid": ["0", "1/4", "1/2", "3/4", "1"],
            "models_exhausted": total_models,
            "lotteries_at_alpha_half": len(LOTTERIES),
            "monotonicity_sextuples_per_model": len(LOTTERIES) ** 6,
            "lcs_scope": "all alpha in (0,1), exact from reciprocity and complete zero-abstention graph",
        },
        "klst_models": klst_models,
        "represented_models": represented_models,
        "counterexample": counterexample,
        "negative_control": {
            "cyclic_parameters": [3, 1, 3],
            "monotonicity_violation_detected": negative_control_detected,
            "violating_lottery_indices": list(cyclic_witness) if cyclic_witness else None,
        },
        "conclusion": conclusion,
        "limitation": "Exhaustion is complete only for the stated finite rational domain; absence of a witness cannot establish a universal theorem.",
    }
