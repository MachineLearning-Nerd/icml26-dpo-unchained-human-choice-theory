"""Fixed entrypoint for every experiment node."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path

from reproduction.falsification import (
    claim_1_counterexample,
    claim_3_counterexample,
    claim_4_proof_dependency_check,
)
from reproduction.proof_certificates import claim_2_certificate, claim_5_certificate
from reproduction.representation_search import claim_4_exhaustive_search


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / ".openresearch" / "artifacts"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def baseline_audit() -> dict[str, object]:
    judge_record = ARTIFACTS / "protected" / "historical_judge_record.json"
    manifest = ARTIFACTS / "protected" / "judged_space_file_manifest.txt"
    contracts = ARTIFACTS / "contracts" / "claim_contract.json"

    record = json.loads(judge_record.read_text())
    contract_data = json.loads(contracts.read_text())
    manifest_lines = [line for line in manifest.read_text().splitlines() if line]

    checks = {
        "space_id_exact": record["space_id"] == "DineshAI/j4c3i3a5kH",
        "judged_revision_exact": record["sha"]
        == "091825f20ce3d96b380ae87e43acb6633d73e568",
        "five_claims_present": len(record["claims"]) == len(contract_data["claims"]) == 5,
        "all_historical_verdicts_toy": all(
            claim["verdict"] == "toy" for claim in record["claims"]
        ),
        "protected_manifest_has_17_files": len(manifest_lines) == 17,
        "historical_core_missing": not any(
            line.endswith(" ./core.py") or line.endswith("\tcore.py")
            for line in manifest_lines
        ),
        "historical_controls_missing": not any(
            "negative" in line.lower() or "control" in line.lower()
            for line in manifest_lines
        ),
    }

    negative_control = dict(checks)
    negative_control["historical_core_missing"] = False
    negative_control_detected = not all(negative_control.values())

    if not all(checks.values()) or not negative_control_detected:
        raise AssertionError({"checks": checks, "negative_control": negative_control_detected})

    return {
        "stage": "historical_baseline",
        "scientific_verdicts": {f"claim_{index}": "BLOCKED" for index in range(1, 6)},
        "reviewer_points_at_judged_revision": 5,
        "checks": checks,
        "negative_control_detected": negative_control_detected,
        "manifest_sha256": sha256(manifest),
        "contract_sha256": sha256(contracts),
        "limitation": "This run audits the judged evidence; it does not verify a universal theorem.",
    }


def cumulative_route() -> dict[str, object]:
    baseline = baseline_audit()
    claim_1 = claim_1_counterexample()
    claim_2 = claim_2_certificate()
    claim_3 = claim_3_counterexample()
    claim_4_dependency = claim_4_proof_dependency_check()
    claim_4 = claim_4_exhaustive_search()
    claim_4["prior_proof_dependency_route"] = claim_4_dependency
    claim_5 = claim_5_certificate()
    return {
        "stage": "claim_4_exhaustive_finite_search",
        "baseline_regression": baseline,
        "scientific_verdicts": {
            "claim_1": claim_1["verdict"],
            "claim_2": claim_2["verdict"],
            "claim_3": claim_3["verdict"],
            "claim_4": claim_4["verdict"],
            "claim_5": claim_5["verdict"],
        },
        "claims": {
            "claim_1": claim_1,
            "claim_2": claim_2,
            "claim_3": claim_3,
            "claim_4": claim_4,
            "claim_5": claim_5,
        },
        "limitations": "Claims 1 and 3 are exact falsifications; Claims 2 and 5 have proof-level certificates. Claim 4 combines a proof-dependency audit with complete finite-domain search, but remains BLOCKED unless an assumption-satisfying counterexample is found.",
    }


def main() -> int:
    started = time.perf_counter()
    result = cumulative_route()
    result["compute"] = {
        "required_core_estimate": 4,
        "selected_flavor": "cpu-upgrade",
        "container_image": "ghcr.io/astral-sh/uv:python3.12-bookworm-slim",
        "actual_cpu_allocation": os.cpu_count(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "gpu_requested": False,
        "runtime_seconds": round(time.perf_counter() - started, 6),
    }
    print("DPO_UNCHAINED_EVIDENCE_BEGIN")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("DPO_UNCHAINED_EVIDENCE_END")
    return 0


if __name__ == "__main__":
    sys.exit(main())
