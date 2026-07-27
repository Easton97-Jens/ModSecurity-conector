# Change Record: Parent prepare-runtime-components provenance-guard assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-tests-prepare-runtime-components-assert-order.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-tests-prepare-runtime-components-assert-order |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smell AZ-KYVRDfYmbqbBXVNDp (324). |
| Boundary | Parent test source, this English/German Change Record pair, and their indexes. Runtime-component provisioning behavior, Framework, MRTS, Gitlinks, scanner configuration, Quality Gates, suppressions, external Sonar issue state, GitHub state, and delivery remain unchanged. |

## Motivation and problem statement

The selected provenance-guard test already verifies the correct blocked result
when Framework-approved ModSecurity v3 provenance fails. Its assertion passes
the expected literal before the observed record field, contrary to SonarQube
Cloud rule `python:S3415`'s `actual, expected` diagnostic order.

## Acceptance criteria

- Correct only `AZ-KYVRDfYmbqbBXVNDp` to `actual, expected` order.
- Preserve the blocked provenance fixture and every assertion that prevents
  copy, subprocess, output-copy, or publish behavior.
- Pass the focused Parent-only test before and after the edit.
- Pass an exact AST map for the retained Sonar line anchor.
- Maintain this complete English/German Change Record pair and indexes, then
  run applicable documentation and diff-hygiene checks.

## Implementation decision and rationale

The test now passes the already-materialized `record["status"]` value before
the unchanged inert literal `"blocked"`. `prepare_shared_modsecurity(...)`
finishes before the assertion is evaluated, so the swap neither changes the
guard invocation nor moves a filesystem, subprocess, copy, or publish sink.
The exact equality domain remains `str`; no fixture, mock, expected value, or
assertion of blocked build behavior changed.

## Changed files

- `tests/test_prepare_runtime_components.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair

## Commands executed

- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_prepare_runtime_components.PrepareRuntimeComponentsTest.test_shared_modsecurity_blocks_before_build_sinks_when_framework_guard_rejects` before the edit.
- The same focused unittest command after the edit.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <AST exact-map predicate>` after the edit.
- `rtk proxy env TMPDIR=<task-owned TMPDIR> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_bilingual_docs`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -c <direct Change Record-pair validator>`.
- `rtk proxy git diff --check` and `rtk proxy rg --files -g '*.pyc' .`.

## Security impact

`not_applicable` to production behavior: only test diagnostic order changed.
The rerun control still requires rejected Framework provenance to yield
`"blocked"`, leave the build and prefix directories absent, and forbid
`copytree`, `run_env`, `copy_modsecurity_outputs`, and `atomic_publish_dir`.
No implementation-level provenance, host-executable, path, subprocess, or
publication control changed.

## Runtime evidence

No runtime-component preparation, Framework checkout, connector build, or
publication was performed. The focused method uses a temporary fake framework
path and mocks every build/output sink; it is test-contract evidence only.

## Known limitations

This local batch addresses one current Sonar Code Smell. Three other S3415
inventory rows in the same module remain untouched: two have non-inert
expected command-list construction, and one is already actual-first in current
source. The public project endpoint still reports 1,125 `OPEN` issues; this
uncommitted candidate does not change external Sonar state.

## Remaining risks

An unintended assertion-value change could weaken the provenance failure
contract. The one-call diff, before/after focused test, exact AST map, and
preserved mocked sink prohibitions reduce that risk. An exact delivered-head
Sonar analysis remains necessary before the listed key can be treated as
resolved externally.

## Checks not run and rationale

- `tests.test_bilingual_docs` passed: 13 tests in 0.035s. The direct Change
  Record-pair validator passed, and `git diff --check` passed. The scoped
  bytecode scan found no `*.pyc` files (the no-match `rg` status is expected).
- The broader test module, runtime-component build, connector builds, host
  runtime smoke tests, Framework, and MRTS checks are not run because the
  scoped test mocks its sinks and no implementation behavior changed.

## Final diff and review status

The B11 candidate is local, uncommitted, and unpushed. No GitHub CI,
SonarQube Cloud PR analysis, review, pull request, merge, default-branch
update, Framework action, or MRTS action has occurred.
