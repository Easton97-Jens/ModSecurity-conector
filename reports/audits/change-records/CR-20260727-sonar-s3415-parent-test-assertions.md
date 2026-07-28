# Change Record: Parent test assertion-order remediation for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260727-sonar-s3415-parent-test-assertions.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-s3415-parent-test-assertions |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud `python:S3415` Code Smells: 112 current OPEN receipt keys across nine test-only modules. |
| Boundary | Parent test sources and this English/German Change Record pair. Product source, workflows, Framework, MRTS, Gitlinks, SonarQube Cloud configuration, Quality Gates, suppressions, external issue state, push, pull request, and merge remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud inventory contains 112 open `python:S3415`
findings in nine Parent test-only modules. The affected `assertEqual` calls
show the expected value before the observed value, which makes failure output
less useful and violates the repository's assertion-order convention.

## Acceptance criteria

- All 112 receipt-backed `python:S3415` calls use `actual, expected` order.
- No production source, workflow, Framework source, MRTS source, or Gitlink
  changes are included.
- Every changed focused test module passes, the receipt-level static ordering
  audit passes, and the patch has no whitespace errors.
- Maintain an equivalent English/German Change Record pair; do not claim any
  Sonar issue closed before an exact candidate-head analysis observes it.

## Implementation decision and rationale

Each assertion was reordered in place only. The assertion type, operands,
messages, fixtures, test names, and control flow were retained. This avoids
changing the tested behavior while making the observed runtime value appear
first in a failure diagnostic.

## Changed files

- connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py
- tests/test_collect_no_crs_source.py
- tests/test_connector_capabilities.py
- tests/test_nginx_phase4_runner_wiring.py
- tests/test_prepare_runtime_components.py
- tests/test_response_header_backend.py
- tests/test_runtime_path_policy.py
- tests/test_traefik_transport_hardening_contract.py
- tests/test_transport_lifecycle_artifacts.py
- reports/audits/change-records/CR-20260727-sonar-s3415-parent-test-assertions.md
- reports/audits/change-records/CR-20260727-sonar-s3415-parent-test-assertions.de.md

## Commands executed

The task worktree initialized the Parent-recorded Framework Gitlink at
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0` without changing Framework source
or the Parent Gitlink. The following command prefix was used for each module:

```sh
rtk proxy env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/sonar-s3415-test-assertions-20260727/tmp /root/git/ModSecurity-conector/.venv/bin/python3 -B -m unittest -v
```

- `connectors.haproxy.harness.test_haproxy_htx_smoke_helper`
- `tests.test_collect_no_crs_source`
- `tests.test_connector_capabilities`
- `tests.test_nginx_phase4_runner_wiring`
- `tests.test_prepare_runtime_components`
- `tests.test_response_header_backend`
- `tests.test_runtime_path_policy`
- `tests.test_traefik_transport_hardening_contract`
- `tests.test_transport_lifecycle_artifacts`
- `rtk proxy git diff --check`
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs`

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused test modules | passed: nine commands exited 0; 8 + 34 + 13 + 6 + 28 + 5 + 6 + 7 + 5 = 112 tests. |
| Receipt-level assertion audit | passed: `receipt_open_python_S3415=112`, `static_ordering_failures=0`. |
| `git diff --check` | passed: no whitespace error. |
| Direct source-diff review | passed: 112 in-place assertion argument swaps across the nine scoped test modules only. |
| `make check-bilingual-docs` before the record-layout correction | failed: this record's first draft did not match the repository Change Record schema; the failure is retained and the record is corrected in this candidate. |
| `make check-bilingual-docs` after correction | passed: `bilingual docs ok`. |
| `make check-doc-links` | passed: `repository path references: PASS` and `doc links ok`. |

## Security impact

The focused security assessment is `not_applicable`: no production security
boundary changes. The affected tests continue to cover their existing security
and lifecycle controls; only assertion-diagnostic argument order changed.

## Documentation status

This English/German Change Record pair records the test-only refactor. Both
files contain the same source scope, test results, validation limitations, and
delivery status. `make check-bilingual-docs` and `make check-doc-links` pass
after the corrected pair and its indexes were prepared.

## Runtime evidence

No connector, host, protocol, report-generation, or production runtime
behavior changed or is claimed. The focused unit tests are not runtime
evidence.

## Known limitations

SonarQube Cloud has not yet analyzed this uncommitted candidate; the 112
current findings are expected to disappear only after an exact-head analysis.

## Remaining risks

An accidental operand swap can weaken a test. Every changed module was rerun
and the receipt-level static ordering audit was retained as focused evidence.
No conclusion about unrelated Sonar rows or security findings follows from
this test-only cleanup.

## Checks not run and rationale

- Connector builds, host configuration checks, runtime smokes, protocol
  matrices, Framework checks, and MRTS checks are not applicable because no
  connector/runtime implementation or cross-repository content changed.
- No hosted SonarQube Cloud analysis, GitHub CI, commit, push, pull request,
  or merge has been performed. This task has no master-integration
  authorization.

## Final diff and review status

The local task-worktree candidate is uncommitted and contains the assertion
order cleanup plus required traceability material. No source changed in the
authoritative Parent checkout. No Framework or MRTS source action, Gitlink
update, scanner-control change, external issue disposition, push, pull
request, or master merge has occurred. Later documentation validation and
delivery evidence will be recorded only from observed results.
