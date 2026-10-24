# Change Record: CR-20260930-pr399-component-pin-test-fixtures

**Language:** English | [Deutsch](CR-20260930-pr399-component-pin-test-fixtures.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-pr399-component-pin-test-fixtures |
| Date (UTC) | 2026-09-30 |
| Base revision | `58345e70eee3753ae67964f6878c8193df8d353e` |

## Motivation and problem statement

PR #399 updated HAProxy to 3.2.25 and ModSecurity to v3.0.17. Synchronizer tests copied those live pins but supplied a historical offline candidate with 3.2.23/v3.0.16. The actionlint job in run 36768743096 failed three assertions; all three were reproduced locally before this change.

## Acceptance criteria

Pass the three original regressions and the 24-test synchronizer module while preserving the exact changed-file lists, byte comparisons, historical grammar fixture, and production pins. Obtain fresh hosted CI evidence for the updated PR head.

## Implementation decision and rationale

Initialize only the temporary copied repositories with explicit independent component-pin fixtures. Cover the ten existing generic target files, validate all assignment/JSON slots before writes, and reject the source checkout. Do not use the production registry, parser, or synchronizer to construct its own test inputs.

## Changed files

- `tests/framework_component_fixture.py`
- `tests/test_update_framework_versions.py`
- `reports/audits/change-records/CR-20260930-pr399-component-pin-test-fixtures.md`
- `reports/audits/change-records/CR-20260930-pr399-component-pin-test-fixtures.de.md`

## Commands executed

```sh
python3 -m unittest -v tests.test_update_framework_versions
python3 -m unittest -v tests.test_ci_security_workflows tests.test_validate_submodule_candidate_state tests.test_update_submodules_local_git tests.test_update_framework_versions tests.test_verify_framework_candidate_contract
make check-ci-security-contract
python3 ci/tools/fetch_security_tool.py --tool actionlint --validate-only
python3 ci/tools/fetch_security_tool.py --tool zizmor --validate-only
python3 ci/tools/fetch_security_tool.py --tool gitleaks --validate-only
python3 ci/tools/new-change-record.py check
python3 ci/checks/documentation/check-bilingual-docs.py
git diff --check
```

Local Python 3.12.14 and PyYAML 6.0.3: the 24-test module passed; the five-module contract suite passed (109 tests, one skip); all three tool-lock validations passed. The complete 170-test command encountered two failures and 18 errors in the unchanged sandbox/namespace suites because this execution environment lacks `/proc` facilities (five skips). A focused fixture probe passed source-checkout rejection, byte idempotence, and validation-before-write checks. Test commands used `PYTHONNOUSERSITE=1`, `PYTHONDONTWRITEBYTECODE=1`, and external task directories for `RUNNER_TEMP`/`TMPDIR`. The bilingual documentation, Change Record structure, and staged diff checks listed above passed before delivery.

## Security impact

Test preparation only; production validation, workflow permissions, dependency pins, and security assertions are unchanged. Independent literal fixtures keep the production synchronization behavior under test.

## Runtime evidence

No connector runtime claim. This change affects offline contract-test preparation only.

## Known limitations

Local Python differs from the repository CI pin 3.14.7. Missing `/proc` prevents complete local sandbox/namespace evidence; hosted CI must provide that evidence.

## Remaining risks

Future changes to the registered target schema must update the explicit test fixture mappings. Fixture release values intentionally remain historical.

## Checks not run and rationale

Connector builds, runtime matrices, and local actionlint/zizmor scanning were not repeated: production/workflow files are unchanged. Hosted CI reruns the configured checks. Kernel sandbox checks could not pass in this local environment.

## Final diff and review status

The scoped test changes received independent read-only review with no blocking findings. This record describes pre-delivery local evidence; it does not claim a hosted result, merge, or master change.
