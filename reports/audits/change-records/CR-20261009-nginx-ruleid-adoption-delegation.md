# Change Record: CR-20261009-nginx-ruleid-adoption-delegation

**Language:** English | [Deutsch](CR-20261009-nginx-ruleid-adoption-delegation.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-ruleid-adoption-delegation |
| Date (UTC) | 2026-10-09 |
| Base revision | `c09480ff9b5b83b52883f5cf116266f1da5ca4d1` |

## Motivation and problem statement

The name-only duplicate-parser gate rejected the existing `ngx_http_modsecurity_extract_intervention_rule_id` wrapper although Common owns parsing. The unchanged checker returned 1 with only `FAIL: Duplicate NGINX rule-id helper is absent`.

## Acceptance criteria

Accept bounded delegation; reject altered input, output, size, null guard, local parsing, log configuration gates, inactive safe twins, missing or late extraction, missing or nonempty reset, duplicates, and macro overrides. Preserve the other adoption contracts and stay within the four assigned files.

Reject direct top-level `return` / `goto` before extraction while preserving
the existing conditional early guards.

## Implementation decision and rationale

Validate the complete active and unmasked wrapper body using the existing C lexical helpers: one null-log guard and one Common call with the intervention message, `ctx->last_intervention_rule_id`, and its `sizeof`. Require a direct caller immediately after the empty reset and before limit classification, terminal recording, redirect/status dispatch, and cleanup. Reject additional connector rule-ID helper names and additional Common extraction calls in the intervention module; preserve the logger's independent Common delegation. Extend critical macro controls over the helper, caller, input/output identifiers, `sizeof`, and `NULL`. The complete contract replaces the name-only gate; no parser-name whitelist substitutes for validation.

Independent review found that a direct `goto cleanup;` before the reset made
the otherwise ordered call unreachable. A second test-first slice rejects
direct `return` / `goto` in the caller prefix using `c_direct_matches`; nested
conditional guards remain accepted.

## Changed files

- `ci/checks/connectors/nginx/check-nginx-common-adoption.py`
- `tests/test_nginx_common_adoption.py`
- `reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.md`
- `reports/audits/change-records/CR-20261009-nginx-ruleid-adoption-delegation.de.md`

## Commands executed

Portable notation: `$PARENT_PYTHON` represents the already selected Parent
virtual-environment interpreter; `<temporary-work-root>` represents the
task-owned external work root. Actual absolute execution paths remain in
external execution evidence, not in this versioned record.

Working directory: `<temporary-work-root>/worktrees/parent-ruleid-adoption-20261009`. Commands ran through `rtk proxy bash -c` with `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and external `TMPDIR` / `PYTHONPYCACHEPREFIX`. Python: `$PARENT_PYTHON`.

- Unchanged native checker: exit 1; original RED retained in `native-red.log`.
- The positive baseline test against the unchanged checker: exit 1, one expected failure with the original name-ban diagnostic; `positive-red.log`.
- `make check-nginx-common-adoption PYTHON=$PARENT_PYTHON`: exit 0; `native-green.log`.
- Native scaffold creation with `ci/tools/new-change-record.py create --name nginx-ruleid-adoption-delegation --base-revision c09480ff9b5b83b52883f5cf116266f1da5ca4d1 --date 2026-10-09`: exit 0.
- `make check-doc-links PYTHON=$PARENT_PYTHON`: exit 2; missing pre-existing Framework-linked paths in this isolated worktree; `doc-links.log`.
- `make check-bilingual-docs PYTHON=$PARENT_PYTHON`: exit 2 for the same missing Framework paths; `bilingual.log`.
- `ci/tools/new-change-record.py check` with the selected interpreter: exit 0; archive structural contract only; `change-record-check.log`.
- Four focused `test_rule_id_delegation_*` methods: exit 0, 4 tests in 85.734s; `focused-tests.log`.
- `$PARENT_PYTHON -m unittest -v tests.test_nginx_common_adoption tests.test_nginx_upstream_security_contract tests.test_nginx_native_intervention_chain`: exit 0, 143 tests in 698.443s, no skips; `scoped-tests.log`. This previous run includes the independent ordered extraction contract and the native intervention unit harness using real Common code. It preceded the early-exit correction and started before the initial candidate freeze; final nine-symbol macro coverage ran separately. It is not a 143-test result for the final candidate.
- Final `test_rule_id_delegation_rejects_macro_overrides` rerun: exit 0, 1 test in 27.105s; nine critical symbols; `final-macro-tests.log`.
- `rtk proxy git diff --check`: exit 0.
- Optional `python -m ruff check ci/checks/connectors/nginx/check-nginx-common-adoption.py tests/test_nginx_common_adoption.py` with the selected interpreter: exit 1, `No module named ruff`; `ruff.log`. No installation was attempted.
- `rtk --version`: `0.51.0`; `rtk gain` was available.

Logs are retained under `<temporary-work-root>/analysis/nginx-all-required-20261008T124555Z/ruleid-adoption`.

Previous frozen candidate SHA256 values: checker
`9edc90aa7ccfb026cfe471e8bdc23352b2aca5ff5d9a6470a742770f33e01dfd`, tests
`8010273f47b86dce9894ac8d1785e05a65a02fa55691717ce49bc4593d1c5cc6`.
Final candidate SHA256 values: checker
`4046f208daf62c3e61c80b8b9e9bfe78265c66fd27f6d12e7ad6779de9b20399`, tests
`84f17120a5bdb67fe1e1372942bcc93006927dee4351b31a9cfe5bf0fbcab033`.

Second-slice RED: `test_rule_id_delegation_rejects_direct_early_exits_before_extraction`
against the previous checker, exit 1, three expected failures in 9.856s;
`early-exits-red.log`. Final native adoption checker: exit 0;
`final-native-green.log`.

Final candidate focused run: `$PARENT_PYTHON -m unittest -v` selecting
`test_current_helper_aware_contract_is_accepted` and all five
`test_rule_id_delegation_*` methods of
`tests.test_nginx_common_adoption.NginxCommonAdoptionCheckerTests`: exit 0,
6 tests in 113.614s, no skips; `final-six-focused-tests.log`. Source/test files
remained frozen throughout this run.

Direct `$PARENT_PYTHON ci/checks/documentation/check-repository-path-references.py`:
exit 2 for existing missing Framework-linked paths; `final-path-references.log`.
The paired records use portable path notation and contain no prohibited local
source-checkout absolute paths.

Independent Root integration validation at the final checker/test hashes:
`rtk proxy $PARENT_PYTHON -m unittest -v` selecting the same six checker
methods plus `tests.test_nginx_native_intervention_chain` and
`tests.test_nginx_upstream_security_contract`: exit 0, 40 tests in 113.853s,
no skips; `root-ruleid-focus-r2.log` / `.exit` in the external task analysis.
The actual Common-C unit seam ran; this is not hosted NGINX evidence.

In the populated Parent integration worktree at the same c09480ff base,
`rtk proxy make check-nginx-common-adoption check-bilingual-docs check-doc-links
check-variable-documentation` with explicit Parent/Framework interpreters and
roots exited 0 before the pause. These integrated results supersede the
isolated missing-Framework-path limitation for that checkout only. A fresh
full 144-test run and native full lint remain pending after the normal
correction commit; the earlier 143-test run is not reused as final evidence.

## Security impact

Strengthens source-contract validation without changing product source, parser, or host behavior. Synthetic mutations must not cause the checker to accept a broken bounded-delegation boundary.

## Runtime evidence

No hosted runtime execution. Native-intervention unit tests are separate evidence from a running NGINX host; no new host/runtime claim is made.

## Known limitations

This is a conservative lexical source-contract validator, not a C compiler or runtime proof. The isolated worktree lacks populated Framework paths needed by the full documentation-link target.

## Remaining risks

Equivalent future wrapper refactors may need an explicitly reviewed checker contract update. External headers and hosted runtime behavior remain outside this correction's evidence scope.

## Checks not run and rationale

Product builds, full repository suite, hosted runtime, scanner authentication, and administrative checks were excluded from this bounded task. Framework/MRTS changes and dependency/toolchain installation were not authorized.

The previous 143-test run was not repeated after the minimal early-exit slice;
focused regression and independent integration checks cover that final change.

## Final diff and review status

The four assigned files are retained for independent Parent integration review. No product source, Framework, MRTS, dependency, or configuration file was changed. No commit, push, PR, merge, or master integration was performed by this task.

Manual EN/DE content review confirmed equivalent technical facts and literals.
The isolated documentation-check limitation remains historical; populated
integration documentation validation and the independent 40-test run passed.
Full immutable post-commit gates and genuine hosted execution remain pending.

The bounded checker correction and all specified negative controls are verified.
The overall worktree validation outcome is partial because the full
documentation targets could not pass here.
