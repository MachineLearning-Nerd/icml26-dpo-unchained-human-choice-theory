# Branch audit — DPO Unchained

This ledger records the branch cleanup so that the public names describe the work and the old ORX workspace labels remain traceable.

## Initial remote snapshot

- Repository: MachineLearning-Nerd/icml26-repro-j4c3i3a5kH-dpo-unchained-your-training-algorithm-is-secretly-disentangled-in-human-choi
- Default branch: main
- Main before documentation: 3790b2ef53bb143fb39fddde721d77d38d3094cf
- Reachable commits before cleanup: 14
- Remote branches before cleanup: main plus 10 ORX branches
- Historical source and evidence tip: be9e71d16855a80ab75cf19b6aedd0f009ac97d5

## Identity policy

Every reachable commit will use this exact author and committer identity:

    MachineLearning-Nerd <37579156+MachineLearning-Nerd@users.noreply.github.com>

The pre-cleanup history contains Dinesh Jinjala author/committer records and one GitHub noreply commit. The rewrite changes identity metadata only; file content and branch topology are preserved before the documentation checkpoint is added.

## Branch rename map

| Old remote branch | New remote branch | Purpose |
| --- | --- | --- |
| main | main | Canonical landing page and current release surface |
| orx/judged-5-10-baseline-audit | audit/baseline-judged-5-10 | Historical judged baseline |
| orx/constructive-proof-certificates | audit/constructive-certificates | Claims 2 and 5 proof certificates |
| orx/assumption-satisfying-falsification-search | audit/claims-1-3-falsification | Claims 1 and 3 exact falsifications |
| orx/claim-4-exhaustive-finite-klst-search | audit/claim-4-finite-klst-search | Finite Claim 4 enumeration |
| orx/claim-4-representation-reduction-audit | audit/claim-4-representation-reduction | Domain/type audit of Claim 4 |
| orx/claim-4-adversarial-falsification | audit/claim-4-adversarial-falsification | Adversarial Claim 4 search |
| orx/cumulative-four-claim-certificates | audit/cumulative-four-claim-certificates | Cumulative accepted certificates |
| orx/evaluator-visible-release-candidate | release/evaluator-visible-candidate | Evaluator-visible artifact package |
| orx/hugging-face-metadata-publication-repair | release/hugging-face-metadata | Publication metadata repair |
| orx/post-publication-exact-revision-audit | release/post-publication-verification | Post-publication exact revision audit |

## Cleanup checks

Before publication:

- [x] README explains the paper, claims, evidence paths, branches, citation, and thank-you note.
- [x] STATUS.md records the scientific and publication checkpoints.
- [x] AUTONOMOUS_STATE.json records the next action and pinned source.
- [x] Target repository name is available.
- [ ] Rewrite reachable commit identities.
- [ ] Rename the GitHub repository.
- [ ] Push new branch names and remove old ORX branch names.
- [ ] Verify remote main, branch inventory, README blob, JSON parsing, and commit identities.

The final state will be appended below after the GitHub API and remote refs are verified.
