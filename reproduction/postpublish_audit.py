"""Download and fail-closed audit the exact published Space revision."""

from __future__ import annotations

import hashlib
import json
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

from reproduction.release_audit import _markdown_targets, _reachable_from_entrypoint


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "space_candidate"
SPACE_ID = "DineshAI/j4c3i3a5kH"
PUBLISHED_REVISION = "c2ec63147309eb77ff5e352dcfbf7c2ea8f9575b"
JUDGED_REVISION = "091825f20ce3d96b380ae87e43acb6633d73e568"
USER_AGENT = "Mozilla/5.0 OpenResearch-PostPublication-Audit/1.0"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def _remote(path: str) -> bytes:
    quoted = "/".join(urllib.parse.quote(part, safe="") for part in path.split("/"))
    return _get(
        f"https://huggingface.co/spaces/{SPACE_ID}/resolve/{PUBLISHED_REVISION}/{quoted}"
    )


def _old_manifest() -> dict[str, str]:
    result = {}
    manifest = CANDIDATE / ".openresearch" / "artifacts" / "protected" / "judged_space_file_manifest.txt"
    for line in manifest.read_text().splitlines():
        digest, path = line.split("  ./", 1)
        result[path] = digest
    return result


def postpublish_audit() -> dict[str, object]:
    info = json.loads(_get(f"https://huggingface.co/api/spaces/{SPACE_ID}"))
    allowlist = [
        line
        for line in (CANDIDATE / "upload_allowlist.txt").read_text().splitlines()
        if line
    ]
    local_hashes = {
        path: _sha256((CANDIDATE / path).read_bytes()) for path in allowlist
    }

    with tempfile.TemporaryDirectory() as directory:
        downloaded = Path(directory) / "published"
        published_hashes = {}
        for path in allowlist:
            content = _remote(path)
            target = downloaded / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            published_hashes[path] = _sha256(content)

        reachable = _reachable_from_entrypoint(downloaded)
        required_pages = {
            (downloaded / "README.md").resolve(),
            *((downloaded / "pages" / f"claim-{index}" / "page.md").resolve() for index in range(1, 6)),
            (downloaded / "pages" / "visibility" / "page.md").resolve(),
        }
        links_exist = all(
            target.exists()
            for page in reachable
            for target in _markdown_targets(page, downloaded)
        )
        current_verifier_obvious = "Current cumulative verifier" in (
            downloaded / "pages" / "index.md"
        ).read_text()
        raw = json.loads((downloaded / "artifacts" / "results.json").read_text())

    old_hashes = _old_manifest()
    moved_paths = {"README.md", "logbook.json", "pages/index.md"}
    historical_subset = {}
    for path, expected_hash in old_hashes.items():
        if path in moved_paths:
            location = f"historical/{JUDGED_REVISION}/{path}"
        else:
            location = path
        historical_subset[path] = _sha256(_remote(location)) == expected_hash

    checks = {
        "space_head_is_exact_published_revision": info["sha"] == PUBLISHED_REVISION,
        "all_54_uploaded_paths_match_local_bytes": published_hashes == local_hashes,
        "canonical_pages_reachable": required_pages <= reachable,
        "all_reachable_links_exist": links_exist,
        "current_verifier_is_obvious": current_verifier_obvious,
        "displayed_raw_verdicts_match": raw["verdicts"]
        == {
            "claim_1": "FALSIFIED",
            "claim_2": "VERIFIED",
            "claim_3": "FALSIFIED",
            "claim_4": "BLOCKED",
            "claim_5": "VERIFIED",
        },
        "all_17_judged_files_preserved_by_hash": all(historical_subset.values()),
    }
    if not all(checks.values()):
        raise AssertionError({"checks": checks, "historical_subset": historical_subset})
    return {
        "status": "PASS",
        "published_revision": PUBLISHED_REVISION,
        "checks": checks,
        "uploaded_paths_verified": len(allowlist),
        "reachable_markdown_files": len(reachable),
        "historical_files_verified": len(historical_subset),
        "historical_subset": historical_subset,
    }
