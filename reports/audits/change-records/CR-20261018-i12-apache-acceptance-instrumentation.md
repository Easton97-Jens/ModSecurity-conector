# Change Record: CR-20261018-i12-apache-acceptance-instrumentation

**Language:** English | [Deutsch](CR-20261018-i12-apache-acceptance-instrumentation.de.md)

Apache-only acceptance instrumentation; runtime qualification remains pending.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261018-i12-apache-acceptance-instrumentation |
| Date (UTC) | 2026-10-18 |
| Base revision | `f1fb6f8e2d2ed59f00da1b82fe788d934c3f743d` |

## Motivation and problem statement

The 155 original Apache I12 contracts require independent host, SDK, physical sink, client, backend and cleanup observations. Existing captures leave gaps around real bucket reads, multipart files, native fault seams and abnormal termination. This change extends the existing Apache lifecycle package with bounded helpers and explicit provenance.

## Acceptance criteria

Preserve all 155 original identities and expectations. Bind source, configuration, binaries, SDK, helper objects and run inputs by hashes. Observe actual boundaries; missing observations remain null. A fresh current-source build and complete case-specific host evidence are required before any new full PASS. Original-oracle reconciliation, all runtime groups, five physical sink failures and final CI/Sonar remain separate completion requirements.

## Implementation decision and rationale

Case-private configurations, markers, upload directories and hash bindings extend the batch driver; review extracts existing capture roles. Keepalive/cancellation clients and Common-sink, host-I/O, bucket, multipart and fault helpers are opt-in test artifacts. Multipart callbacks observe public SDK state after real body processing and cleanup, preserving return/errno. The fault helper records the real msc_add_request_header SDK return; no additional GNU wrapper for that API is claimed.

The observed-module builder requires a disposable source export, complete capture receipt, all 33 freshly built Product objects, exact SDK/header identity and hash-bound canonical compiler transcript. In an external overlay it applies versioned fault seams and hooks immediately before selected real APR bucket reads, recompiles two translation units, retains 31 fresh objects and links four observer translation units plus three helper objects. It preserves strict flags, checks ELF hardening/SDK resolution and rechecks source/object hashes. runtime_qualification remains null.

## Changed files

ci/runtime/lifecycle/apache-i12/acceptance/: cases.py, batch.py, backend.py, review_batch.py, oracles.py, keepalive.py, cancellation.py, common_sink_boundary.c, host_io.c, host_bucket.c, multipart_observer.cpp, fault_boundary.c, build_host_io.py, build_host_bucket.py, build_multipart_observer.py, build_fault_boundary.py, build_observed_module.py.

New tests: tests/test_apache_i12_acceptance_cases.py, test_apache_i12_acceptance_driver.py, test_apache_i12_acceptance_oracles.py, test_apache_i12_batch_review.py, test_apache_i12_cancellation.py, test_apache_i12_common_sink_boundary.py, test_apache_i12_fault_boundary.py, test_apache_i12_host_bucket.py, test_apache_i12_host_io.py, test_apache_i12_keepalive.py, test_apache_i12_multipart_observer.py, test_apache_i12_observed_module_builder.py.

Existing Apache files: ci/runtime/lifecycle/apache-i12/launch.py, observed_curl.py, prepare.py; reports/audits/apache-i12-20261015/rule-equivalence-probe.py; tests/test_apache_i12_boundaries.py, tests/test_apache_i12_launch.py. These address bounded matching, serialization and repeated literals with regressions. This EN/DE pair records the scope. No product source, shared capture manifest/observer, other connector, workflow or Framework/MRTS Gitlink is changed by this instrumentation.

## Commands executed

The coordinator ran rtk proxy env with PYTHONDONTWRITEBYTECODE=1 and external RUNNER_TEMP/CODEX_TEST_TMP_ROOT using the Parent virtual environment: python -m unittest discover -v -s tests -p 'test_apache_i12_*.py' — 235 tests, OK, skipped3, exit0, including added builder-hardening regressions. An earlier attempt with a nonexistent RUNNER_TEMP failed four setup operations and remains an invalid attempt. Separate opt-in batch-review execution against actual smoke capture and source metadata passed 8 tests, exit0. The nonroot Common-sink suite passed 9/9 tests, no skips, exit0 under UID/GID65534; both control and wrapped paths returned actual EACCES errno13. Durable evidence: /var/tmp/codex/ModSecurity-conector/runs/i12-apache-414-acceptance-20261015/analysis/resume-20261018/nonroot-common-boundary-v1/evidence. Other validation evidence is retained under the same resume-20261018 root.

## Security impact

Fault activation requires explicit test configuration in private authorized hosts. Helpers do not establish production behavior or justify expectation changes. The builder rejects ambiguous commands, stale inputs, historical objects, unsafe compiler auxiliary outputs and mismatched wrappers/SDK. Authentication, isolation, compiler warnings and CI/Sonar controls remain mandatory.

## Runtime evidence

Passive multipart/host-I/O integration exercises the real SDK with and without opt-in preload, compares return/errno and observes temporary files and actual cleanup. This supports helper transparency only. Historical host captures retain their own identities. No new full host PASS, approved original oracle, product defect, release approval or I12_COMPLETE is claimed.

## Known limitations

The 41 conditional reconciliation proposals still require source approval and runtime confirmation; 13 original-oracle gaps remain. The completed nonroot helper suite establishes its permission boundary only; it does not replace the Apache host sink retest. Native transaction cleanup, physical JSONL, descriptor/process cleanup and follow-up recovery require complete current-build captures for every applicable case.

## Remaining risks

Injected paths may differ from naturally occurring failures. Activation, actual SDK/APR return and host action must be independently observed. Overlay linkage requires review against the canonical build before host use. Missing evidence stays null and prevents qualification.

## Checks not run and rationale

Fresh final-source full build, final observed-module linkage, all 155 current-build host executions, five sink retests and final exact-head CI/Sonar are pending coordinator work. Full bilingual/document-link checks for this pair are pending; structure validation does not replace them. This documentation worker performs no commit or push.

## Final diff and review status

The base revision was rechecked before creating this pair with ci/tools/new-change-record.py. Both languages were manually aligned for technical facts and limitations. rtk proxy python3 ci/tools/new-change-record.py check passed, exit0 (structure only); rtk proxy git diff --check passed, exit0. RTK verification confirmed version1.0.1, the installed path and available gain reporting. All shell validation used RTK. Final integrated diff review and delivery remain with the coordinator.
