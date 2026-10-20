# Change Record: CR-20261020-i12-apache-sonar-remediation

**Language:** English | [Deutsch](CR-20261020-i12-apache-sonar-remediation.de.md)

Apache-only acceptance-harness remediation in Draft PR #414. This record describes source changes and local validation; it does not approve an Apache runtime case.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261020-i12-apache-sonar-remediation |
| Date (UTC) | 2026-10-20 |
| Base revision | `fe2c30f710a26e3ea7ef0dcc2b847e3fb093deb6` |

## Motivation and problem statement

The full SonarQube Cloud readback for PR #414 at the base revision contains 179 distinct unresolved issues: 11 vulnerabilities and 168 code smells, with 495 secondary flow locations. GitHub exposed only 50 annotations. The authoritative analysis is `eb509cd6-12be-445f-b81b-c966be977bc3`, CE task `AaFOsW5SEA5tm64SJa9s`, dated `2026-10-18T11:04:17Z`. Annotation counts therefore cannot establish the complete issue inventory.

The change addresses Apache test-harness input handling, resource cleanup and maintainability while preserving the actual SDK/APR calls and original acceptance contracts. A new Cloud analysis is required to determine which findings are resolved.

## Acceptance criteria

Preserve the 155 original Apache IDs, their original oracles and historical failures; preserve genuine SDK/APR results and physical fault behavior. Keep filesystem inputs bounded and identity checked, restrict private HTTP endpoints to the admitted loopback/high-port boundary, and release owned descriptors on exceptional paths. Relevant local regressions must pass; a later analysis must be bound to the actual published commit before reporting Sonar closure. Host acceptance remains subject to fresh, fully qualified execution evidence.

## Implementation decision and rationale

The observed-module builder checks canonical roots and ancestry, rejects symlinks and invalid file types, reads through bounded `O_NOFOLLOW`/`O_CLOEXEC` descriptors, and parses/hashes the same checked bytes. It preserves the exact 28-wrapper contract, defined ELF-symbol checks and SDK binding.

Python request framing, response parsing, case selection, backend handling and batch collection are split into focused helpers. Constants replace repeated literals. Port admission is checked at both CLI and socket boundaries. Direct child cancellation preserves arbitrary `BaseException` termination and reaping. Native helper refactors preserve real returns, `errno`, forwarding and cleanup order. The multipart observer uses RAII descriptor cleanup and fixed diagnostics for allocation failures; C++17 `steady_clock` timestamps are checked against the actual Linux monotonic epoch by a native-process test.

No scanner suppression, reduced test contract, TLS substitution or language-standard upgrade is used to obtain a pass. Private plain HTTP remains part of the Apache test contract; related findings require fresh server-side adjudication or explicit open status.

## Changed files

All implementation paths below are under `ci/runtime/lifecycle/apache-i12/`:

- `acceptance/backend.py`, `acceptance/batch.py`, `acceptance/build_fault_boundary.py`, `acceptance/build_host_io.py`, `acceptance/build_observed_module.py`, `acceptance/cancellation.py`, `acceptance/cases.py`, `acceptance/keepalive.py`, `acceptance/review_batch.py`, `observed_curl.py`.
- `acceptance/common_sink_boundary.c`, `acceptance/fault_boundary.c`, `acceptance/host_bucket.c`, `acceptance/host_io.c`, `acceptance/multipart_observer.cpp`.
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
| Final Apache-I12 unittest discovery after all source fixes | 269 tests, exit 0, 3 explicit opt-in/root-DAC skips. This is the authoritative combined local run. |
| Actual-capture batch-review opt-ins after the final source fixes | 8 tests, exit 0, no skips. Two preceding invocations selected the wrong retained spec path and failed before extraction; the exact attempt-owned `2-smoke-spec-v2.json` rerun is authoritative. |
| Separate Common sink boundary run under UID/GID `65534` after the C changes | 9/9 tests passed, exit 0, including genuine read-only-parent `EACCES`/`errno 13`; evidence is under `/var/tmp/codex/ModSecurity-conector/nonroot-common-boundary-414-20261020-v2/evidence`. |
| Broad Sonar gate/reliability/helper selection | 61 tests executed, exit 1: 60 passed and the pre-existing HAProxy append-string link fixture failed on unresolved Common/authorization symbols. That other-connector integration is outside this Apache-only change and was not hidden or modified. |
| `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check` | Exit 0; Change Record structure only, not evidence validation. |
| `rtk proxy make check-bilingual-docs` with Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf` mounted read-only at the gitlink | Exit 0, `bilingual docs ok`. The first direct checkout attempt only exposed the intentionally unpopulated worktree gitlink; the exact-pin read-only rerun is authoritative. |
| `rtk proxy make check-doc-links` in the same exact-pin read-only namespace | Exit 0, repository path references and document links passed. |
| `rtk proxy git diff --check` | Exit 0 after filling this record pair. |

The native-helper receipt is retained at `/var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/native-sonar-remediation-20261020.json`. It records 48 actual allocation-failure budgets, zero descriptor leaks, preserved `errno` and the fixed failure diagnostic. Independent final review reproduced two candidate regressions in CLI port conversion and child-exit handling; both were fixed and rechecked. The reviewer found no remaining concrete blocking issue in the final code diff. Exact published-head Cloud analysis remains to be recorded by the integrating task.

## Security impact

This is defensive test/build/evidence work within the explicitly authorized private environment. The TAC query reported `granted`, level `tac1`, source `user`, on `2026-10-18`; the task treats this as the user-described DrayTek-Blue ceiling, without inferring additional authorization. Private controller isolation, identity checks, permissions, redaction and quality gates remain required.

Filesystem admission and exception cleanup reduce harness misuse and evidence substitution risks. These source changes do not establish a production vulnerability or its remediation. Independently confirmed production Apache defects require a separately authorized fix on #382.

## Runtime evidence

No new fully qualified host PASS and no original-oracle resolution is claimed by this remediation. Helper/unit tests demonstrate their own layer only. The historical inventory remains 155 IDs: 10 configuration and 145 host cases; 28 executed, 8 fully qualified PASS, 20 partial and 127 unexecuted. There are 54 originally open Apache-oracle members. Independent source review yielded 41 conditional proposals, 13 gaps and zero newly approved resolutions.

Fresh final-source builds, loaded binary/configuration/SDK/run identities, private host execution and per-case semantic qualification are still required. Missing observations remain `null` or open. `I12_COMPLETE` is not claimed.

## Known limitations

The full 179-issue inventory belongs to the old base analysis. Local source remediation cannot establish a green Cloud gate, zero new findings or closure of intentional loopback HTTP/C++17 recommendations. The 118-test Python and 67-test native runs cover different subsets; their counts must not be added to claim a complete combined run. The root-DAC skip requires the separate nonroot test and a fresh rerun if its implementation changes.

## Remaining risks

Refactoring framing, exception and observer paths may still affect behavior outside the locally exercised paths. Apache acceptance lacks full current-run qualification for all mandatory cases and independent approval of the original oracle proposals. Shared ledger dispatch needed for configuration/pre-native/host qualification remains an integration need; this change does not alter the central generator. The unrelated HAProxy fixture link failure also remains a central/connector integration need outside the permitted Apache file scope.

## Checks not run and rationale

At this record's local-validation stage, a new commit-bound Cloud analysis and a fresh 155-case host campaign have not been established. The integrating task must execute and report them. There is no permission-based blocker to the authorized defensive local work; these are missing execution evidence, not a claimed security refusal.

## Final diff and review status

The remediation is an uncommitted candidate relative to the full base SHA above. An independent final review covered the expanded diff, found the two regressions recorded above, and verified their corrections; it found no remaining concrete blocking security or behavior issue. Normal commit/push and target-branch integration are authorized; no published remediation SHA, exact-commit CI/Sonar success or PR merge is claimed here. Final delivery and runtime qualification are tracked separately in the integrating task.
