# Environment and artifact record

## Fixed reproduction command

From a clean checkout, the repository's cumulative evidence entrypoint is:

    uv sync --frozen && uv run --frozen python -m reproduction.run

The project requires Python 3.12 and is pinned by pyproject.toml and uv.lock.
The same producer and lockfile are mirrored in space_candidate/.

## Recorded scientific campaign

The historical campaign used the image
ghcr.io/astral-sh/uv:python3.12-bookworm-slim on Hugging Face cpu-upgrade
hardware. No GPU was requested; run metadata reports 64 allocated CPUs. The
campaign's cumulative evidence-producing revision is
be9e71d16855a80ab75cf19b6aedd0f009ac97d5.

| Purpose | Run ID | Git SHA | Estimated cores | Runtime |
| --- | --- | --- | ---: | ---: |
| baseline audit | 3b68e966-b552-484a-a6c9-d869f7036b81 | 2e05e92b65dcf103e70e2c6114402729ff2ae026 | 2 | 16 s |
| constructive certificates | 0a0568bc-3e72-416a-b7c2-4c4c23b253be | eb77763fe9669bf02fcece1b6fb93b8cab4b8b67 | 4 | 21 s |
| exact falsifications | 735b9f6c-8dad-4cdd-ae12-78b48b44f682 | 3ada4e95a82907b7f350bc66088d6394c1e4cdef | 2 | 21 s |
| cumulative certificates | a1fa0c4a-78d7-452d-a2b7-7b60c5fca330 | ec5a15ae88d3aba81fc7e952f37ad2497f8eb096 | 4 | 21 s |
| Claim 4 exhaustive finite route | e586390e-3bd8-475d-a5d0-442543c67831 | c472c55239f41981fb76e91ee9a07f18e5536f9f | 4 | 21 s |
| Claim 4 reduction audit | f78238ff-1d63-45f9-994a-b2cea1eab6c3 | eea82d5ca7dac2393f67494026f132fbc077a665 | 4 | 21 s |
| Claim 4 adversarial route | 1a793bde-e523-469d-8f44-91ad934761dc | be9e71d16855a80ab75cf19b6aedd0f009ac97d5 | 8 | 42 s |

Verifier runtimes and the no-GPU policy are preserved in
space_candidate/artifacts/runs.json. The run log exposed no billing amount;
this dossier does not invent a monetary cost. Documentation changes were not
presented as a new scientific rerun.

## Evidence inputs

- reproduction/run.py — cumulative producer.
- reproduction/falsification.py — Claims 1 and 3 plus the first Claim 4 route.
- reproduction/proof_certificates.py — Claims 2 and 5.
- reproduction/representation_search.py — finite Claim 4 route.
- reproduction/reduction_audit.py — typed Claim 4 route.
- reproduction/adversarial_search.py — mandatory adversarial Claim 4 route.
- .openresearch/artifacts/ — contracts, raw outputs, controls, and metadata.
- space_candidate/artifacts/results.json — released result record.
- space_candidate/artifacts/runs.json — run and resource record.

The content-addressed files used by the release are listed in
EVIDENCE_MANIFEST.json and checked by verify_final.py.
