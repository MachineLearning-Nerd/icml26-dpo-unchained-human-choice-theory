"""Fixed entrypoint for every experiment node."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from pathlib import Path


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


def main() -> int:
    started = time.perf_counter()
    result = baseline_audit()
    result["compute"] = {
        "required_core_estimate": 2,
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
