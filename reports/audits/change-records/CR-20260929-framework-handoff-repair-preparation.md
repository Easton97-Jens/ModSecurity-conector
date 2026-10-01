# Change Record: Framework handoff repair preparation

**Language:** English | [Deutsch](CR-20260929-framework-handoff-repair-preparation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260929-framework-handoff-repair-preparation |
| Date (UTC) | 2026-09-29 |
| Base revision | `d56af0856507eb048987974d3960e301e7c24371` |
| Delivery state | Preparation only; the production correction is not applied. |

## Motivation and problem statement

The user requested diagnosis, repair, and a separate pull request for
[run 36608694822, job 109544329844](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36608694822/job/109544329844).

The first material failure is
`Framework common.sh differs from approved reviewed structure`, from
`ci/tools/verify-framework-candidate-contract.py`, exit code 2. The final
sandbox-success check fails because preparation and candidate execution were
skipped; it is not the primary cause.

The updater proposes Framework
`0290a979ba4bc63a7abed175a53471367b385553` instead of
`f9e48b0774b5bdf7aaa8e38ce98eb6c50bf293c8`. The candidate's `common.sh`
changes 12 literal pins: NGINX release/checksum, AWS-LC tag/commit, go-ftw
tag/commit, Node.js version, CodeQL version/commit, and Ruff
version/commit/checksum. These bytes intentionally remain covered by the
Parent structural review boundary.

## Acceptance criteria

The requested repair is complete only after the generated patch is reviewed
and applied, the real candidate passes the unchanged contract checks, and
current-head CI is verified. Creating this preparation-only PR does not meet
that criterion. Do not merge it as a completed production fix.

## Implementation decision and rationale

The new one-time generator reads the two exact Framework Git objects as data.
It checks that the baseline reproduces the currently approved structural hash
`7ad268af3baa17d2c2e9b5857ced2138684fab70e5066ddddd6f3656e8baa6af`
and that the candidate differs by exactly the 12 reviewed assignments.
It then computes the replacement digest rather than guessing a hash.

The planned patch aligns 19 closed Parent text paths and one Framework
gitlink. It updates the explicit approval digest, unprotected NGINX handoff
and fixtures, and all registered CRS/no-MRTS Framework SHA consumers. It
adds a real-`common.sh` regression and keeps the unreviewed-next-release
negative control distinct at `release-1.31.7`.

The reviewed NGINX tuple is `release-1.31.6`, asset
`nginx-1.31.6.tar.gz`, SHA-256
`974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1`.
Its digest was read from the
[official release metadata](https://github.com/nginx/nginx/releases/tag/release-1.31.6).
This source-provenance check is not a runtime test.

The generator refuses target files differing from the reviewed Parent base,
checks changed Python syntax, and calls `git apply --check --index`.
It writes only a new patch file and never overwrites an existing output.
It does not apply, stage, fetch, checkout, commit, push, or create a workflow.
The real full-file patch has not yet been generated or applied in this session.

## Security impact

No production guard, parser grammar, mutable-field registry, provenance flag,
sandbox, publisher permission, or protected NGINX root-broker pin is changed
by this preparation. The planned patch also leaves those boundaries intact.
No Framework or MRTS source modification is proposed. NGINX is not added to
the generic synchronizer. Candidate shell is never sourced by the generator.

## Changed files

- `ci/tools/prepare-reviewed-framework-handoff.py`
- `tests/test_prepare_reviewed_framework_handoff.py`
- `reports/audits/change-records/CR-20260929-framework-handoff-repair-preparation.md`
- `reports/audits/change-records/CR-20260929-framework-handoff-repair-preparation.de.md`

## Commands executed

The unmodified generator and test file were loaded from an isolated fixture
tree using Python 3.13.5: **19 unit tests passed**. Both new Python files
passed AST parsing and a trailing-whitespace check. The unit tests cover
unexpected candidate changes, baseline drift, missing/duplicate assignments,
closed target scope, non-no-op negative controls, Python syntax, gitlink
patch content, missing final newlines, symlinks, and output preservation.

This was not a repository-native test run and did not use the pinned
Python 3.14.7 CI environment. The exact real-repository patch check has not run.

## Runtime evidence

None. No native connector build, NGINX execution, or successor runtime
matrix is asserted.

## Checks not run and rationale

The real candidate verifier after patch application, the full repository
CI-security suite, the NGINX/evidence suite, bilingual/link checks, and
current-head hosted CI/Sonar verification remain required. Local checkout
was unavailable because GitHub DNS resolution failed. The required local
RTK wrapper was also unavailable. An attempted writable preparation workflow
was rejected and was not created; it is not part of this change.

## Known limitations

The generator requires an existing Parent checkout and a Framework clone
containing both exact commits. Its real-source integration remains
unverified. It deliberately refuses already-modified target files rather
than merging into unrelated work. The current production workflow will
still reject the candidate until the real patch is applied.

## Application and validation

Use the task branch, preserve unrelated work, and use the installed RTK
wrapper's supported invocation. The following are native command payloads,
not permission to omit the repository's required wrapper. The patch output
directory must already exist under the project's approved external storage.

```sh
git submodule update --init -- modules/ModSecurity-test-Framework
git -C modules/ModSecurity-test-Framework fetch origin 0290a979ba4bc63a7abed175a53471367b385553
python3 ci/tools/prepare-reviewed-framework-handoff.py --repo-root "$PWD" --output /var/tmp/codex/ModSecurity-conector/reviewed-framework-handoff.patch
```

Review the generated diff before these explicit write operations:

```sh
git apply --index /var/tmp/codex/ModSecurity-conector/reviewed-framework-handoff.patch
git submodule update --init --checkout -- modules/ModSecurity-test-Framework
python3 ci/tools/verify-framework-candidate-contract.py --repo-root "$PWD" --candidate-sha 0290a979ba4bc63a7abed175a53471367b385553 --framework-common "$PWD/modules/ModSecurity-test-Framework/ci/lib/common.sh"
python3 -m unittest -v tests.test_prepare_reviewed_framework_handoff
make check-ci-security-contract
python3 -m unittest -v tests.test_nginx_exact_head_gate_contract tests.test_nginx_body_buffer_fixture tests.test_prepare_runtime_components tests.test_runtime_component_cache_identity tests.test_runtime_component_cache_contract tests.test_runtime_env_snapshot_contract tests.test_report_presentation_literals tests.test_evidence_output_security tests.test_nginx_functional_evidence
make check-bilingual-docs
make check-doc-links
git diff --cached --check
```

Review the staged diff, commit only the task changes on the task branch,
update this record with actual results, and verify the exact successor PR
head before considering the repair complete. No merge is authorized.

## Remaining risks

The repair recipe may expose further integration failures when exercised
against the real checkout. No passing unit result removes that uncertainty.
The preparation must not be mistaken for an applied or fully verified fix.

## Final diff and review status

Diagnosis and the offline generator tests are supported by observed evidence.
Production application, full validation, and resolution of the original
CI failure remain pending.
