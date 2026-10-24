# Change Record

**Language:** English | [Deutsch](CR-20260919-framework-candidate-review-digest.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-framework-candidate-review-digest |
| Date (UTC) | 2026-09-19 |
| Base revision | 6bb07fee268aa013268f9b0566176d6f94c4abf9 |

## Motivation and problem statement

GitHub Actions [run 35449797036](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35449797036), job `105914883572`, failed in `Validate Framework component-pin data contract`. The current Parent Framework gitlink was `d4f7b69dc264852eac74e1439c0887fcb9fbe372`; the resolved, descended Framework candidate was `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`. The candidate's reviewed OpenSSL, OSV Scanner, and Ruff maintenance pins changed the intentionally covered `common.sh` structure, while Parent still expected `609315092e5f5cdd793a33636f7d620445f2e4e802a383c23bc26a70d1bc7c75`.

The requested Parent-only repair admits only the separately reviewed candidate structure. It does not modify Framework/MRTS source, any Gitlink, NGINX, generic component synchronization, workflow permissions, Quality Gates, or delivery controls.

## Acceptance criteria

- The exact `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` candidate passes the verifier while the current Parent static projection remains `d4f7b69dc264852eac74e1439c0887fcb9fbe372`.
- The production review constant equals `7ad268af3baa17d2c2e9b5857ced2138684fab70e5066ddddd6f3656e8baa6af`.
- Covered OpenSSL, OSV Scanner, and Ruff pin mutations still fail before Parent projection; the existing registered generic source-data control remains accepted.
- All existing bounded file-read, closed mutable-field, NGINX handoff, and shell-mutation controls remain unchanged.

## Implementation decision and rationale

The change replaces one single review digest, not an old/new allowlist. A persistent allowlist would continue to admit the older covered maintenance-pin structure and weaken the one-reviewed-structure invariant. The test fixture records the exact new review literal and exercises representative covered OpenSSL, OSV Scanner, and Ruff pin modifications, which must fail at the structure boundary. The already-merged static SHA-projection flow remains unchanged: it checks the current static Parent SHA, projects the trusted resolver SHA in its closed five-slot registry, and verifies again.

## Security impact

This is a CI/supply-chain integrity boundary. Candidate content is extracted from an exact Framework Git object and read as bounded regular-file data before it reaches any later sourcing or publication path. The verifier continues to hash every non-generic line, reject unsafe shell forms, and validate NGINX separately against Parent projections. The observed failure is a fail-closed stale-review reliability defect, not a demonstrated security bypass or external vulnerability. No scanner suppression, exclusion, Quality-Gate change, permission expansion, or relaxed validation is introduced.

## Changed files

- `ci/tools/verify-framework-candidate-contract.py`
- `tests/test_verify_framework_candidate_contract.py`
- `reports/audits/change-records/CR-20260919-framework-candidate-review-digest.md`
- `reports/audits/change-records/CR-20260919-framework-candidate-review-digest.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

No Framework/MRTS source, Gitlink, `.gitmodules`, dependency manifest, credential, generated artifact, runtime source, workflow permission, or Quality Gate changed.

## Tests and actual results

- Before the patch, `python3 ci/tools/verify-framework-candidate-contract.py --repo-root . --candidate-sha cc36b37d0f6a0fbc3512f3878a691751e91c5fbb --framework-common /root/git/ModSecurity-conector/modules/ModSecurity-test-Framework/ci/lib/common.sh --expected-parent-framework-sha d4f7b69dc264852eac74e1439c0887fcb9fbe372` exited `2` with `Framework common.sh differs from approved reviewed structure`.
- After the patch, the same command exited `0` with JSON status `verified`, `nginx_release_tag` `release-1.31.5`, and the same candidate/current SHA values.
- `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/runtime python3 -m unittest -v tests.test_verify_framework_candidate_contract` passed `27` tests.
- The selected Parent virtual-environment interpreter repeated the exact-candidate verifier with exit `0` and the focused verifier module with `27` passing tests.

## Commands executed

- `env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/runtime make check-ci-security-contract` passed `155` tests with `5` expected environment-dependent skips.
- `PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/fix-actions-run-35449797036/bytecode python3 -m py_compile ci/tools/verify-framework-candidate-contract.py tests/test_verify_framework_candidate_contract.py` passed.
- `/root/git/ModSecurity-conector/.venv/bin/python` was verified as a virtual-environment interpreter (`sys.prefix != sys.base_prefix`) and was used with `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and `PYTHONDONTWRITEBYTECODE=1` for final focused verifier checks.

## Runtime evidence

The authoritative observed failure is GitHub Actions run `35449797036`, job `105914883572`. The local exact-candidate verifier is the strongest available deterministic contract proof. No runtime connector, NGINX, Framework, or MRTS service was started or changed.

## Checks not run and rationale

`make check-bilingual-docs` and `make check-doc-links` are not clean because this isolated worktree deliberately has no initialized Framework submodule; the remaining reported targets are all beneath `modules/ModSecurity-test-Framework`. The new record's required headings were corrected after the first checker output and its paired documentation review found no content or link issue. Ruff and Pyright are not configured in this Parent worktree and their executables are absent from the selected Parent environment; no external-tool installation is authorized. GitHub exact-head checks, SonarQube Cloud Quality Gate, review state, and hosted updater run remain pending. No workflow dispatch or merge is authorized by this record.

## Known limitations

The local test environment cannot prove GitHub-hosted tokens, scheduler behavior, branch protection, concurrent remote changes, or later candidate publication. Framework upstream release provenance remains Framework-owned; Parent acceptance is bound to the immutable candidate commit and the reviewed structure digest.

## Remaining risks

Any future covered `common.sh` pin or executable-structure change requires a new explicit Parent review digest. A malformed candidate, unsafe shell form, NGINX drift, invalid Parent projection, or changed resolver state continues to fail closed.

## Final diff and review status

The implementation is Parent-only and the local evidence is recorded above. Independent documentation and post-patch bypass/regression reviews found no actionable or reportable item. Normal task-branch delivery, exact PR-head checks, and SonarQube Cloud evidence remain pending; no commit, push, PR, hosted rerun, or merge is claimed in this record.
