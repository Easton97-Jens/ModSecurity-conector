# Change Record: submodule updater Draft contract

**Language:** English | [Deutsch](CR-20260809-update-submodules-draft-contract.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260809-update-submodules-draft-contract |
| Date (UTC) | 2026-08-09 |
| Base revision | aa640d5a6d6a41a6ba8d87a0300f995c7392b5df |

## Motivation and problem statement

Update-submodules Run [31317377866](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317377866), publisher job
[93254814385](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317377866/job/93254814385), validated the candidate and Parent master, recognized state C, verified the updater branch, staged only the Framework gitlink, validated the full-SHA raw diff, created a maintenance commit, and advanced the branch with an explicitly bound lease from `fd7e63d7994fd9322c5bbb7862ef283d436c88d5` to `51db35ddf74da9053553da3c6250685d812a8e00`.

The publisher then created [PR #261](https://github.com/Easton97-Jens/ModSecurity-conector/pull/261). Its base, head, head SHA, title, bot author, marker, one-file scope, and absent auto-merge matched the updater contract, but GitHub returned `draft=false`. The final verifier correctly rejected that Ready state.

Run [31317356208](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317356208), actionlint job
[93254643817](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/31317356208/job/93254643817), passed actionlint and workflow YAML validation before `tests.test_ci_security_workflows` failed: its assertion required a one-line `git update-index` spelling although the secure command only used shell continuations.

## Acceptance criteria

Only an exactly identified updater-owned PR may be converted; Ready is never a valid final state; conversion and readback failures remain fatal. Shell layout normalization must retain every exact gitlink-staging argument and reject broad staging.

## Implementation decision and rationale

Open-PR verification is split into mutation-free identity verification and a final verifier that still requires `draft=true`. Draft enforcement first verifies state, repositories, base, head, exact remote head SHA, title, bot author, exactly one marker, and absent auto-merge. A Ready PR is changed only after a second remote-head and full-identity readback, using only `gh pr ready --undo`; the final full readback must observe Draft. Any ambiguity, mismatch, conversion failure, or Ready readback fails closed before `published=true`.

This also recovers a PR-261-like state B before branch-history verification and the SHA-bound branch update. It never makes Ready a valid final state and does not weaken candidate validation, quick-check, path scope, commit provenance, lease binding, token policy, or the fail-closed result job.

The CI contract test now removes backslash-newline continuations and collapses whitespace without executing shell or expanding variables. It still requires `git update-index --add --cacheinfo "160000,$CANDIDATE_SHA,$SUBMODULE_PATH"` and rejects missing flags, another mode/path, and broad `git add` staging.

No Framework/MRTS source, gitlink, secret, permission, auto-merge setting, Quality Gate, or result-job behavior changes. Neither PR #261 nor this source fix is merged or auto-merged by this work; the separately authorized post-merge master E2E remains pending.

## Changed files

`.github/workflows/update-submodules.yml`, `tests/test_ci_security_workflows.py`, and this paired Change Record. No gitlink changed.

## Commands executed

The focused unittest suite, CI-security contract, YAML parser, Python compiler, documentation checks, security tools, and diff checks are run locally. Exact results are reported on the source-fix PR; Framework-dependent checks require an initialized Framework checkout.

## Security impact

Only a twice-identified PR at the exact remote head can reach the single `gh pr ready --undo` mutation. Final Draft readback is mandatory, auto-merge stays forbidden, and `published=true` remains after verification.

## Runtime evidence

The linked Runs and jobs are authoritative. PR #261 remains the unmodified post-merge recovery fixture during this source fix.

## Known limitations

Local static simulation cannot mutate GitHub or reproduce API timing. The post-merge master dispatch is intentionally outside this task.

## Remaining risks

GitHub state can race between reads; repeated identity checks, remote-head comparison, and the existing exact lease make every observed mismatch fail closed.

## Checks not run and rationale

Hosted exact-head checks and the master E2E cannot exist before the source-fix push/PR and are checked afterward without merging or dispatching master.

## Final diff and review status

The source diff adds no permission, fallback credential, auto-merge, general force push, result-job relaxation, Framework/MRTS change, or gitlink change.
