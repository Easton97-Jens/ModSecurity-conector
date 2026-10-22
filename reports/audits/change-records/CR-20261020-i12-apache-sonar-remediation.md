# Change Record: CR-20261020-i12-apache-sonar-remediation

**Language:** English | [Deutsch](CR-20261020-i12-apache-sonar-remediation.de.md)

Apache-only acceptance-harness remediation in Draft PR #414. This record describes source changes and local validation; it does not approve an Apache runtime case.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-i12-apache-sonar-remediation |
| Date (UTC) | 2026-10-20 |
| Base revision | `fe2c30f710a26e3ea7ef0dcc2b847e3fb093deb6` |
| Apache remediation commit | `ee68b78f4f802149ed6d864a32ff5198e8c0596b` |
| Follow-up Sonar remediation commit | `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1` |
| Executed product-source head | `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38` |
| Published final-review hardening head | `de23f2fa4b490c66f15ac97f2646434351f05c5e` |
| PR #410 target head at final review | `76672071c3f7665dfde3340bef9e64271d6f6e70` |

## Motivation and problem statement

The full SonarQube Cloud readback for PR #414 at the base revision contains 179 distinct unresolved issues: 11 vulnerabilities and 168 code smells, with 495 secondary flow locations. GitHub exposed only 50 annotations. The authoritative analysis is `eb509cd6-12be-445f-b81b-c966be977bc3`, CE task `AaFOsW5SEA5tm64SJa9s`, dated `2026-10-18T11:04:17Z`. Annotation counts therefore cannot establish the complete issue inventory.

The change addresses Apache test-harness input handling, resource cleanup and maintainability while preserving the actual SDK/APR calls and original acceptance contracts. A new Cloud analysis is required to determine which findings are resolved.

The subsequent exact-revision Cloud analysis for `a36f9831cb34532d388d2da9a787b25268721b74` still reported 22 unresolved issues. This is a separate analysis from the historical 179-issue inventory, not proof that every difference is an independently verified closure. Commit `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1` addresses those source findings. Later commits and the current runtime campaign do not by themselves prove a green Cloud gate; exact-head CI and server analysis remain separate delivery evidence.

## Acceptance criteria

Preserve the 155 original Apache IDs, their original oracles and historical failures; preserve genuine SDK/APR results and physical fault behavior. Keep filesystem inputs bounded and identity checked, restrict private HTTP endpoints to the admitted loopback/high-port boundary, and release owned descriptors on exceptional paths. Relevant local regressions must pass; a later analysis must be bound to the actual published commit before reporting Sonar closure. Host acceptance remains subject to fresh, fully qualified execution evidence.

## Implementation decision and rationale

The observed-module builder checks canonical roots and ancestry, rejects symlinks and invalid file types, reads through bounded `O_NOFOLLOW`/`O_CLOEXEC` descriptors, and parses/hashes the same checked bytes. It preserves the exact 28-wrapper contract, defined ELF-symbol checks and SDK binding.

Python request framing, response parsing, case selection, backend handling and batch collection are split into focused helpers. Constants replace repeated literals. Port admission is checked at both CLI and socket boundaries. Direct child cancellation preserves arbitrary `BaseException` termination and reaping. Native helper refactors preserve real returns, `errno`, forwarding and cleanup order. The multipart observer uses RAII descriptor cleanup and fixed diagnostics for allocation failures; C++17 `steady_clock` timestamps are checked against the actual Linux monotonic epoch by a native-process test.

No scanner suppression, reduced test contract, TLS substitution or language-standard upgrade is used to obtain a pass. Private plain HTTP remains part of the Apache test contract; related findings require fresh server-side adjudication or explicit open status.

The follow-up preserves native function addresses for identity checks while using ordinary function-pointer calls, and simplifies the C++17 multipart observer without changing its observation contract. The Python builder uses bounded, named validation steps; the backend retains the admitted loopback HTTP contract and tests keep actual/expected assertion order explicit.

The Apache ledger and package now dispatch configuration controls, host pre-native rejections and lifecycle packets to their respective existing shared validators. Additive fields `fresh_qualification_scope`, `fresh_case_qualified`, `fresh_case_outcome` and `fresh_case_qualified_pass`, with separate configuration/pre-native/case counters, retain the qualification scope. A control PASS never becomes a lifecycle PASS: lifecycle fields remain false or `null` where lifecycle qualification is absent. This dispatch does not supply missing semantic predicates or approve unsigned review candidates.

## Changed files

All implementation paths below are under `ci/runtime/lifecycle/apache-i12/`:

- `acceptance/backend.py`, `acceptance/batch.py`, `acceptance/build_fault_boundary.py`, `acceptance/build_host_io.py`, `acceptance/build_observed_module.py`, `acceptance/cancellation.py`, `acceptance/cases.py`, `acceptance/keepalive.py`, `acceptance/review_batch.py`, `observed_curl.py`.
- `acceptance/common_sink_boundary.c`, `acceptance/fault_boundary.c`, `acceptance/host_bucket.c`, `acceptance/host_io.c`, `acceptance/multipart_observer.cpp`.
- `ledger.py`, `package.py`, with `tests/test_apache_i12_ledger.py` and `tests/test_apache_i12_package.py`.
- Tests under `tests/`: `test_apache_i12_acceptance_driver.py`, `test_apache_i12_acceptance_oracles.py`, `test_apache_i12_backend.py`, `test_apache_i12_boundaries.py`, `test_apache_i12_cancellation.py`, `test_apache_i12_keepalive.py`, `test_apache_i12_multipart_observer.py`, `test_apache_i12_observed_module_builder.py`.
- This English record and `CR-20261020-i12-apache-sonar-remediation.de.md`.

Central matrices, report generators, capture manifests, shared observers, production connector source, workflows and Framework/MRTS gitlinks are outside this change.

## Commands executed

Commands use RTK and the existing Python environment. Working directory: `/var/tmp/codex/ModSecurity-conector/worktrees/i12-apache-410-20261015`.

| Procedure | Observed result and scope |
| --- | --- |
| `rtk proxy /usr/local/bin/sonar-with-env api get '/api/issues/search?componentKeys=Easton97-Jens_ModSecurity-conector&pullRequest=414&ps=500&p=1&resolved=false'` | Full base-analysis inventory: 179 issues; this is not a new analysis of the remediation. |
| Apache-I12 unittest discovery before the final expanded refactor | 255 tests, exit 0, 3 explicit opt-in/DAC skips. |
| Focused acceptance cases/driver, keepalive, cancellation, backend and observed-builder unittests after Python refactoring | 118 tests, exit 0. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_apache_i12_common_sink_boundary tests.test_apache_i12_fault_boundary tests.test_apache_i12_host_bucket tests.test_apache_i12_host_io tests.test_apache_i12_multipart_observer` | 67 tests, exit 0, 1 root-DAC skip; final native-helper rerun. |
| Actual-capture batch-review opt-ins | 8 tests, exit 0, no skips; preceding validation stage. |
| Sonar strict-gate contract tests | 44 tests, exit 0; preceding validation stage. |
| Apache native/header/Common regressions | 67 tests, exit 0, 1 expected skip; preceding validation stage. Initial setup lacked the external `RUNNER_TEMP` directory; the directory-created rerun is authoritative. |
| Earlier Apache-I12 unittest discovery | 269 tests, exit 0, 3 explicit opt-in/root-DAC skips; superseded as the combined local run by the 287-test validation below. |
| Actual-capture batch-review opt-ins after the final source fixes | 8 tests, exit 0, no skips. Two preceding invocations selected the wrong retained spec path and failed before extraction; the exact attempt-owned `2-smoke-spec-v2.json` rerun is authoritative. |
| Separate Common sink boundary run under UID/GID `65534` after the C changes | 9/9 tests passed, exit 0, including genuine read-only-parent `EACCES`/`errno 13`; evidence is under `/var/tmp/codex/ModSecurity-conector/nonroot-common-boundary-414-20261020-v2/evidence`. |
| Broad Sonar gate/reliability/helper selection | Initial integrated run: 60 passed and one stale HAProxy fixture failed to link, exit 1. The fixture-only correction was independently tested and published centrally on #410 as `92cd1133ceb3de1afee0e935be167dac39673a8c`, then normally merged. Exact integrated rerun: 61 tests passed, exit 0. |
| Incoming target regressions | Lighttpd response-splice/empty-EOS: 2 tests passed, exit 0. Shared configuration/lifecycle/pre-native ledger: 40 tests passed, exit 0. |
| Combined Apache-I12 discovery after the follow-up Sonar fixes and typed dispatch | 287 tests total: 284 PASS, 3 explicit opt-in/root-DAC skips, exit 0. |
| Apache ledger/package tests after typed dispatch | 34 tests passed, exit 0; control/lifecycle separation and mutation rejection included. |
| Shared configuration/lifecycle/pre-native ledger regression rerun | 40 tests passed, exit 0. |
| Native-helper regression rerun | 67 tests total, exit 0, including 1 root-DAC skip; separate UID/GID `65534` execution passed 9/9. |
| Retained-capture opt-ins after the follow-up | 8/8 passed, exit 0. One invocation selected the `all-v2` spec and failed setup because `15 != 3`; the corrected, spec-hash-bound `smoke-v2` rerun is authoritative. This setup failure is preserved and is not a host-case failure or PASS. |
| Fresh private 155-case campaign at product source `57e94983...` | Controller and candidate exit 0, no timeout, 155 captured principal/control executions, complete controller cleanup. This count does not imply 155 completed case contracts or PASS results. |
| Final Apache-I12 discovery after reviewer hardening | 387 tests total, exit 0, with 5 explicit opt-in/root-DAC skips. |
| Focused batch/final-review suite | 52 tests total, exit 0, with 2 explicit opt-in skips. |
| Current native-helper regression | 67 tests total, exit 0, with 1 root-DAC skip. |
| Current shared lifecycle-ledger regression | 40 tests passed, exit 0. |
| Approved final per-case review | 155 decisions, 4 full lifecycle PASS, 151 null/open, `i12_complete=false`; unchanged shared ledger validation exited 0. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | Exit 0; Change Record structure only, not evidence validation. |
| `rtk proxy make check-bilingual-docs` with Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` mounted read-only at the gitlink | Exit 0, `bilingual docs ok`. The first direct checkout attempt only exposed the intentionally unpopulated worktree gitlink; the exact-pin read-only rerun is authoritative. |
| `rtk proxy make check-doc-links` in the same exact-pin read-only namespace | Exit 0, repository path references and document links passed. |
| `rtk proxy git diff --check` | Exit 0 after filling this record pair. |

The native-helper receipt is retained at `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/native-sonar-remediation-20261020.json`. It records 48 actual allocation-failure budgets, zero descriptor leaks, preserved `errno` and the fixed failure diagnostic. Independent final review reproduced two candidate regressions in CLI port conversion and child-exit handling; both were fixed and rechecked. The reviewer found no remaining concrete blocking issue in the bounded final-review diff. Exact-head Cloud analysis remains separate from this host-evidence result.

## Security impact

This is defensive test/build/evidence work within the explicitly authorized private environment. The fresh TAC query reported `granted`, level `tac1`, source `user`, at `2026-10-22T20:59:23.107554+00:00`; the task treats this as the user-described DrayTek-Blue ceiling, without inferring additional authorization. Private controller isolation, identity checks, permissions, redaction and quality gates remain required.

Filesystem admission and exception cleanup reduce harness misuse and evidence substitution risks. These source changes do not establish a production vulnerability or its remediation. Independently confirmed production Apache defects require a separately authorized fix on #382.

## Runtime evidence

The fresh `57e94983...` campaign captured all 155 principal/control executions: 141 host HTTP cases, 10 configuration tests and 4 host pre-native candidates. The unchanged shared validator and explicit Root review qualify exactly four full request lifecycles: `NEED-request-empty`, `NEED-request-single-chunk`, `NEED-request-csv` and `NEED-request-eos-once`. They resolve 4 of the 54 originally open oracle members for this current campaign; 50 remain open. The other 151 outcomes remain `null`. The exact current result and immutable references are in the [2026-10-22 report](../apache-i12-20261022/README.md). The [2026-10-15 report](../../../docs/i12-apache-native-evidence-20261015.md) remains historical and is not aggregated into current-source qualification.

All ten configuration executions and four pre-native executions remain unqualified because their physical receipts do not satisfy the unchanged typed validators. This is missing or contradictory evidence, not a permission refusal. Missing observations remain `null`; `I12_COMPLETE` is false.

## Known limitations

The 179-issue inventory belongs to the old base analysis; the later `a36f9831cb34532d388d2da9a787b25268721b74` analysis contains 22 unresolved issues. Local source remediation and host evidence cannot establish a green Cloud gate, zero new findings or closure of intentional loopback HTTP/C++17 recommendations. Subset test counts must not be added to claim a complete combined run. The root-DAC skip requires the separate nonroot test and a fresh rerun if its implementation changes.

## Remaining risks

Refactoring framing, exception and observer paths may still affect behavior outside the locally exercised paths. Apache acceptance lacks full current-run qualification for all mandatory cases and independent approval of the original oracle proposals. The Apache-specific dispatch is implemented; semantic predicates and fully reviewed packets remain open. Shared validators and the central generator are unchanged.

## Checks not run and rationale

The fresh 155-case campaign and explicit review are complete, but exact-head CI/Cloud disposition after the final evidence-only commit remains delivery evidence outside the runtime qualification. The 151 open case decisions need new producer fields, family predicates or independent mapping evidence. There is no permission-based blocker to the defensive work performed; the remaining case blockers are missing or contradictory evidence and the documented shared-producer integration needs.

## Final diff and review status

The first remediation is committed as `ee68b78f4f802149ed6d864a32ff5198e8c0596b`; the Sonar follow-up is `33e89e8ad636787a5c9a19eafbbe9bc8eaadabd1`, the executed product source is `57e94983e808bcc4c1ca4f5fcf9745f6dc9d4a38`, and final reviewer hardening is published at `de23f2fa4b490c66f15ac97f2646434351f05c5e`. Independent review found no remaining concrete finding in that bounded reviewer diff. Exact final evidence-commit CI/Sonar success and PR merge are not claimed here. No force-push, automatic merge, release or `I12_COMPLETE` claim follows.
