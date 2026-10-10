# Change Record: CR-20261009-native-python-quality-sink

**Language:** English | [Deutsch](CR-20261009-native-python-quality-sink.de.md)



## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-native-python-quality-sink |
| Date (UTC) | 2026-10-09 |
| Base revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation and problem statement

Fresh PR396 findings concern Python source authority, complexity, duplicate literals and exception-test clarity. Direct request guarding is defense in depth; the admitted CLI already restricts the two cases and no command-injection exploit is demonstrated.

## Acceptance criteria

Preserve authority, exact typed identities, error order, original seals and nonzero driver exits; characterize quality behavior before refactoring and prove the direct sink guards with failing then passing controlled tests.

## Implementation decision and rationale

Derive the identical fixed policy storage root through the existing environment-independent helper, without changing ancestry predicates. Extract source and collector checks in their original order; keep duplicate JSON rejection. Validate exact request paths and integer ports locally and place -- before the URL.

## Changed files

Four assigned lifecycle modules and their four existing dedicated test files. Source adapter tests remain in tests/test_nginx_native_operation_dispatch.py; shared dispatcher source, runtime utilities, Framework and MRTS are unchanged. The separate inherited-FD change is documented in its own record.

## Commands executed

RTK-proxied existing Parent Python with external TMPDIR and explicit current Framework roots: python -m unittest tests.test_nginx_native_authority tests.test_nginx_native_operation_dispatch tests.test_nginx_common_input_fault_driver tests.test_nginx_native_operation_collection -v. Baseline33 tests exit0; intermediate40 tests exit0. Corrected real baseline request controls fail12 assertions; guarded controls pass. Evidence: python-sonar-slice-baseline.log, python-sonar-quality-green.log, python-sonar-request-baseline-red-r2.log and python-sonar-request-green.log.

## Security impact

No public-directory grant, environment-selected authority, validation relaxation or suppression. Literal policy-root routing is not an exploit remediation claim. Source directory ancestor policy remains unchanged.

## Runtime evidence

No native runtime or E2E evidence was produced; controlled subprocess results test argv and retention only.

## Known limitations

Remote Sonar resolution requires a scan of the integrated revision; current81 findings cannot be called resolved by local unit results.

## Remaining risks

Coordinator must independently review integrated source, full lint and a new exact-revision scan. Native admission and transport evidence remain separate.

## Checks not run and rationale

No native build/runtime, package installation, authentication changes, publication or Git writes; coordinator owns these steps.

Final current-source focused six-module run:58 tests,48.211s, exit0 without skips (python-sonar-slice-final-focus-r2.log), including duplicate-keyword preservation and pointer-driver controls with explicit FRAMEWORK_ROOT. Earlier refinement9 tests exited0 with one Framework-dependent skip because that command omitted FRAMEWORK_ROOT (python-sonar-slice-final-refinement.log). Record archive and all four new-record local path checks exited0; full repository path check exited2 solely on absent isolated Framework submodule files. Ruff exited1 because the existing Parent environment lacks the module; no installation was attempted.

## Final diff and review status

Scoped diff reviewed for predicates, exact diagnostic order, unchanged raw retention and actual exits. Uncommitted isolated delivery only; no integration or remote closure claimed.
