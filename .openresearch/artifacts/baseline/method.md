# Historical baseline method

The baseline parses the protected judged record, exact Space manifest, and claim contracts. It verifies that the correct Space/revision was selected, all five historical verdicts are `toy`, and the missing `core.py` and controls are detectable. A deliberately corrupted visibility result is the negative control and must fail the gate.

This is an evaluator-evidence audit, not a theorem experiment.

The first launch with the backend's default `python:3.12` image answered nothing because `uv` was absent (exit 127). The fixed image for the repaired baseline and every descendant is `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`.
