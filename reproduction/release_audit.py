"""Fail-closed audit for the evaluator-visible release candidate."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate" if (ROOT / "space_candidate").exists() else ROOT
EXPECTED = {
    "claim_1": "FALSIFIED",
    "claim_2": "VERIFIED",
    "claim_3": "FALSIFIED",
    "claim_4": "BLOCKED",
    "claim_5": "VERIFIED",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _markdown_targets(path: Path, root: Path) -> list[Path]:
    targets = []
    for target in re.findall(r"\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)", path.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        resolved = (path.parent / target).resolve()
        if root.resolve() in resolved.parents or resolved == root.resolve():
            targets.append(resolved)
    return targets


def _reachable_from_entrypoint(root: Path) -> set[Path]:
    pending = [(root / "README.md").resolve()]
    seen: set[Path] = set()
    while pending:
        path = pending.pop()
        if path in seen or not path.exists() or path.suffix != ".md":
            continue
        seen.add(path)
        pending.extend(_markdown_targets(path, root))
    return seen


def release_audit(cumulative: dict[str, object]) -> dict[str, object]:
    evidence = json.loads((CANDIDATE / "artifacts" / "results.json").read_text())
    contracts = json.loads((CANDIDATE / "artifacts" / "claim_contract.json").read_text())
    logbook = json.loads((CANDIDATE / "logbook.json").read_text())
    allowlist = [line for line in (CANDIDATE / "upload_allowlist.txt").read_text().splitlines() if line]
    actual_files = {
        path.relative_to(CANDIDATE).as_posix()
        for path in CANDIDATE.rglob("*")
        if path.is_file()
    }
    manifest_entries = {}
    for line in (CANDIDATE / "upload_manifest.sha256").read_text().splitlines():
        digest, relative = line.split("  ", 1)
        manifest_entries[relative] = digest
    manifest_valid = all(
        relative != "upload_manifest.sha256"
        and relative in actual_files
        and _sha256(CANDIDATE / relative) == digest
        for relative, digest in manifest_entries.items()
    ) and set(manifest_entries) == actual_files - {"upload_manifest.sha256"}
    with tempfile.TemporaryDirectory() as directory:
        downloaded = Path(directory) / "candidate"
        for relative in allowlist:
            source = CANDIDATE / relative
            target = downloaded / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        reachable = _reachable_from_entrypoint(downloaded)
        required_pages = {
            (downloaded / "README.md").resolve(),
            (downloaded / "pages" / "index.md").resolve(),
            (downloaded / "pages" / "visibility" / "page.md").resolve(),
            (downloaded / "pages" / "release-report" / "page.md").resolve(),
            *((downloaded / "pages" / f"claim-{index}" / "page.md").resolve() for index in range(1, 6)),
        }
        reachable_complete = required_pages <= reachable
        all_reachable_links_exist = all(
            target.exists()
            for page in reachable
            for target in _markdown_targets(page, downloaded)
        )

    historical_manifest = json.loads(
        (CANDIDATE / "historical" / "091825f20ce3d96b380ae87e43acb6633d73e568" / "manifest.json").read_text()
    )
    historical_root = CANDIDATE / "historical" / historical_manifest["revision"]
    historical_text_matches = all(
        (historical_root / item["path"]).exists()
        and _sha256(historical_root / item["path"]) == item["sha256"]
        for item in historical_manifest["text_files"]
    )

    text_files = sorted(path for path in CANDIDATE.rglob("*") if path.is_file())
    forbidden = re.compile(r"(?i)(hf_[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]|password\s*[:=])")
    no_secrets = not any(forbidden.search(path.read_text(errors="replace")) for path in text_files)

    svg_files = sorted(CANDIDATE.rglob("*.svg"))
    evidence_svgs = sorted((CANDIDATE / "images").glob("*.svg"))
    for svg in svg_files:
        ET.parse(svg)

    notebook = CANDIDATE / "notebooks" / "dpo_unchained_reproduction.py"
    marimo = subprocess.run(
        [sys.executable, "-m", "marimo", "check", str(notebook)],
        text=True,
        capture_output=True,
        check=False,
    )

    claims = cumulative["claims"]
    claim_4 = claims["claim_4"]
    raw_numbers_match = all(
        [
            claims["claim_1"]["smt_properness_and_decomposition"] == evidence["claim_1"]["smt"],
            claims["claim_2"]["symbolic_residual"] == evidence["claim_2"]["symbolic_residual"],
            claims["claim_2"]["independent_exact_trials"] == evidence["claim_2"]["exact_trials"],
            claims["claim_3"]["smt_abstention_under_axioms"] == evidence["claim_3"]["smt_abstention_under_axioms"],
            claim_4["domain"]["models_exhausted"] == evidence["claim_4"]["route_2"]["models_exhausted"],
            claim_4["klst_models"] == evidence["claim_4"]["route_2"]["klst_models"],
            claim_4["represented_models"] == evidence["claim_4"]["route_2"]["represented_models"],
            claim_4["mandatory_falsification_route"]["total_nonrepresentable_targets"] == evidence["claim_4"]["route_4"]["total_nonrepresentable"],
            claims["claim_5"]["general_certificate"]["subgradient_residual"] == evidence["claim_5"]["subgradient_residual"],
        ]
    )
    published_modules = [
        "adversarial_search.py",
        "falsification.py",
        "proof_certificates.py",
        "reduction_audit.py",
        "representation_search.py",
    ]
    source_mirrors_match = all(
        _sha256(ROOT / "reproduction" / name)
        == _sha256(CANDIDATE / "reproduction" / name)
        for name in published_modules
    )

    checks = {
        "cumulative_verdicts_match": cumulative["scientific_verdicts"] == EXPECTED,
        "raw_verdicts_match": evidence["verdicts"] == EXPECTED,
        "five_exact_contracts": len(contracts["claims"]) == 5,
        "space_id_exact": logbook["space_id"] == "DineshAI/j4c3i3a5kH",
        "allowlist_is_exact_candidate_tree": set(allowlist) == actual_files,
        "sha256_manifest_covers_every_other_upload": manifest_valid,
        "raw_numbers_regenerate": raw_numbers_match,
        "canonical_pages_reachable_from_fresh_copy": reachable_complete,
        "all_reachable_local_links_exist": all_reachable_links_exist,
        "all_visibility_rows_complete": all(row["complete"] for row in evidence["visibility_matrix"]),
        "historical_text_hashes_match": historical_text_matches,
        "historical_binary_files_retained_in_place": len(historical_manifest["binary_files_retained"]) == 3,
        "candidate_is_text_only": all(path.suffix != ".png" for path in CANDIDATE.rglob("*")),
        "no_secret_patterns": no_secrets,
        "five_evidence_figures_parse": len(evidence_svgs) == 5,
        "marimo_check_passes": marimo.returncode == 0,
        "visible_source_mirrors_match_executed_source": source_mirrors_match,
        "current_verifier_is_prominent": "Current cumulative verifier" in (CANDIDATE / "pages" / "index.md").read_text(),
        "historical_baseline_labeled": "Historical rejected baseline" in (CANDIDATE / "pages" / "historical" / "page.md").read_text(),
    }
    if not all(checks.values()):
        raise AssertionError({"release_checks": checks, "marimo": marimo.stdout + marimo.stderr})
    return {
        "status": "PASS",
        "checks": checks,
        "reachable_markdown_files": len(reachable),
        "text_files_scanned": len(text_files),
        "svg_files_parsed": len(svg_files),
        "marimo_output": (marimo.stdout + marimo.stderr).strip(),
        "upload_allowlist_sha256": _sha256(CANDIDATE / "upload_allowlist.txt"),
        "upload_manifest_sha256": _sha256(CANDIDATE / "upload_manifest.sha256"),
    }
