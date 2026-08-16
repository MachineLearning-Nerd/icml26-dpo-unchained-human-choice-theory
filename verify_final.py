#!/usr/bin/env python3
"""Fail-closed structural checks for the published DPO Unchained audit."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = "MachineLearning-Nerd/icml26-dpo-unchained-human-choice-theory"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "37579156+MachineLearning-Nerd@users.noreply.github.com"
EXPECTED_SOURCE_SHA = "f30cb463d9867221b8fa9c49306b83cd21ec528c59c6e9e115d11436a3220bdc"
EXPECTED_BRANCHES = {
    "main",
    "audit/baseline-judged-5-10",
    "audit/claim-4-adversarial-falsification",
    "audit/claim-4-finite-klst-search",
    "audit/claim-4-representation-reduction",
    "audit/claims-1-3-falsification",
    "audit/constructive-certificates",
    "audit/cumulative-four-claim-certificates",
    "release/evaluator-visible-candidate",
    "release/hugging-face-metadata",
    "release/post-publication-verification",
}
EXPECTED_CLAIMS = {
    "C1": "FALSIFIED",
    "C2": "VERIFIED",
    "C3": "FALSIFIED",
    "C4": "BLOCKED",
    "C5": "VERIFIED",
}
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "REPORT.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "BRANCH_AUDIT.md",
    "ENVIRONMENT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "AUTONOMOUS_STATE.json",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args, cwd=ROOT, check=True, capture_output=True, text=True
    )
    return result.stdout


def read_json(relative_path: str) -> object:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(relative_path: str) -> str:
    digest = hashlib.sha256()
    with (ROOT / relative_path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_branches() -> set[str]:
    refs = run(
        "git",
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:strip=2)",
    )
    return {ref.strip() for ref in refs.splitlines() if ref.strip()}


def remote_branches() -> set[str]:
    prefix = "refs/remotes/origin/"
    refs = run(
        "git",
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname)",
    )
    return {
        ref.strip()[len(prefix):]
        for ref in refs.splitlines()
        if ref.strip().startswith(prefix) and ref.strip() != prefix + "HEAD"
    }


def verify_history() -> None:
    records = run(
        "git", "log", "--all", "--format=%an%x00%ae%x00%cn%x00%ce"
    ).splitlines()
    if not records:
        fail("no reachable commits")
    expected = (
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}\x00"
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}"
    )
    unexpected = sorted({record for record in records if record != expected})
    if unexpected:
        fail(f"non-canonical reachable identities: {unexpected}")
    if "Co-authored-by:" in run("git", "log", "--all", "--format=%B"):
        fail("co-author trailer found")
    if int(run("git", "rev-list", "--count", "--all").strip()) < 16:
        fail("historical evidence commits are missing")
    if run("git", "for-each-ref", "refs/original", "--format=%(refname)").strip():
        fail("temporary refs/original remain")
    all_refs = run("git", "for-each-ref", "--format=%(refname)")
    if any("/orx/" in ref or ref.endswith("/orx") for ref in all_refs.splitlines()):
        fail("legacy orx ref remains")


def verify_remote() -> None:
    remote = run("git", "config", "--get", "remote.origin.url").strip()
    normalized = remote.removesuffix(".git").rstrip("/")
    if not normalized.endswith(EXPECTED_REPOSITORY):
        fail(f"origin is {remote!r}, expected {EXPECTED_REPOSITORY!r}")


def verify_branch_tips() -> None:
    remote = remote_branches()
    if remote != EXPECTED_BRANCHES:
        fail(f"remote branch set is {sorted(remote)!r}")
    local = local_branches()
    if "main" not in local:
        fail("local main branch is missing")
    for branch in EXPECTED_BRANCHES:
        remote_tip = run("git", "rev-parse", f"refs/remotes/origin/{branch}").strip()
        if branch in local:
            local_tip = run("git", "rev-parse", f"refs/heads/{branch}").strip()
            if local_tip != remote_tip:
                fail(f"local and origin tips differ for {branch}")
    head = run("git", "symbolic-ref", "refs/remotes/origin/HEAD").strip()
    if head != "refs/remotes/origin/main":
        fail(f"origin HEAD is {head!r}, expected origin/main")


def verify_manifest() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    if not isinstance(manifest, dict):
        fail("manifest must be a JSON object")
    if manifest.get("repository") != EXPECTED_REPOSITORY:
        fail("manifest repository marker is wrong")
    if manifest.get("claim_statuses") != EXPECTED_CLAIMS:
        fail("manifest claim statuses are wrong")
    expected_audit_files = {
        relative_path
        for relative_path in REQUIRED_FILES
        if relative_path != "AUTONOMOUS_STATE.json"
    }
    if set(manifest.get("required_audit_files", [])) != expected_audit_files:
        fail("manifest audit-file list is wrong")
    if set(manifest.get("branches", {}).get("expected_final", [])) != EXPECTED_BRANCHES:
        fail("manifest branch set is wrong")
    if manifest.get("attribution", {}).get("email") != CANONICAL_EMAIL:
        fail("manifest attribution is wrong")
    artifacts = manifest.get("content_addressed_artifacts", [])
    if not artifacts:
        fail("manifest has no content-addressed artifacts")
    for item in artifacts:
        relative_path = item.get("path")
        expected_hash = item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_hash, str):
            fail("malformed content-addressed artifact")
        if not (ROOT / relative_path).is_file():
            fail(f"missing content-addressed artifact: {relative_path}")
        if sha256(relative_path) != expected_hash:
            fail(f"artifact hash mismatch: {relative_path}")


def verify_evidence() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    for relative_path in manifest["required_evidence_paths"]:
        if not (ROOT / relative_path).is_file():
            fail(f"missing required evidence path: {relative_path}")
    evidence = read_json("space_candidate/artifacts/results.json")
    if evidence.get("paper") != "2507.07855v4":
        fail("evidence paper identifier is wrong")
    if evidence.get("paper_source_sha256") != EXPECTED_SOURCE_SHA:
        fail("evidence source hash is wrong")
    if evidence.get("verdicts") != {
        "claim_1": "FALSIFIED",
        "claim_2": "VERIFIED",
        "claim_3": "FALSIFIED",
        "claim_4": "BLOCKED",
        "claim_5": "VERIFIED",
    }:
        fail("raw evidence statuses are wrong")
    claim_1 = evidence["claim_1"]
    if claim_1["witness"] != {"psi": "z", "F": "sigmoid(z)"}:
        fail("Claim 1 witness is missing")
    if claim_1["smt"] != "UNSAT" or claim_1["positive_control_residual"] != "0":
        fail("Claim 1 certificate is missing")
    if evidence["claim_2"]["symbolic_residual"] != "0":
        fail("Claim 2 symbolic certificate is missing")
    if evidence["claim_2"]["exact_trials"] != 200:
        fail("Claim 2 exact-trial certificate is missing")
    if evidence["claim_3"]["smt_abstention_under_axioms"] != "UNSAT":
        fail("Claim 3 abstention certificate is missing")
    route_2 = evidence["claim_4"]["route_2"]
    if (
        route_2["models_exhausted"] != 125
        or route_2["klst_models"] != 19
        or route_2["represented_models"] != 19
    ):
        fail("Claim 4 finite route is missing")
    route_4 = evidence["claim_4"]["route_4"]
    if (
        route_4["total_nonrepresentable"] != 5987
        or route_4["axiom_satisfying_nonrepresentable"] != 0
        or route_4["counterexample"] is not None
    ):
        fail("Claim 4 adversarial boundary is missing")
    if evidence["claim_5"]["subgradient_residual"] != "0":
        fail("Claim 5 certificate is missing")


def verify_ledgers_and_state() -> None:
    claims = read_json("claims.json")
    state = read_json("AUTONOMOUS_STATE.json")
    if {row.get("id"): row.get("status") for row in claims["claims"]} != EXPECTED_CLAIMS:
        fail("claims.json statuses are wrong")
    if state.get("target_github_repository") != (
        "https://github.com/" + EXPECTED_REPOSITORY
    ):
        fail("state repository marker is wrong")
    if state.get("canonical_branch") != "main":
        fail("state canonical branch is wrong")
    if state.get("canonical_identity", {}).get("name") != CANONICAL_NAME:
        fail("state canonical identity is wrong")
    if state.get("source_archive_sha256") != EXPECTED_SOURCE_SHA:
        fail("state source hash is wrong")
    if state.get("historical_branch_count") != 10:
        fail("state branch count is wrong")


def verify_documentation() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "CLAIM_EVIDENCE.md",
        "SOURCE_AUDIT.md",
        "BRANCH_AUDIT.md",
        "ENVIRONMENT.md",
        "CITATION.cff",
        "AUTHOR_THANK_YOU.md",
        "FALSIFIED",
        "VERIFIED",
        "BLOCKED",
        "verify_final.py",
    ):
        if marker not in readme:
            fail(f"README is missing marker {marker!r}")
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
    if branch_audit.count("| orx/") != 10:
        fail("branch migration table is incomplete")
    if "5/10" not in (ROOT / "REPORT.md").read_text(encoding="utf-8"):
        fail("historical score boundary is missing")


def main() -> int:
    missing = sorted(
        relative_path
        for relative_path in REQUIRED_FILES
        if not (ROOT / relative_path).exists()
    )
    if missing:
        fail(f"required files missing: {missing}")
    verify_remote()
    verify_branch_tips()
    verify_history()
    verify_manifest()
    verify_evidence()
    verify_ledgers_and_state()
    verify_documentation()
    print("PASS: published DPO Unchained audit state is structurally verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
