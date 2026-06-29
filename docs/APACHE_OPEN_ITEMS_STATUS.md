# Apache Connector Open Items Status

**Language:** English | [Deutsch](APACHE_OPEN_ITEMS_STATUS.de.md)




Status: Historical analysis snapshot for Issues/PRs.

As of: 2026-05-24. This analysis is based on the then-open GitHub issues and pull requests in `owasp-modsecurity/ModSecurity-apache`, the local sources in `ModSecurity-conector`, and the then-existing Test-/Runtime-Artefakten in `ModSecurity-test-Framework`. No production code changes were made and no new smoke runs were started.

Current merge readiness status, full matrix numbers and the canonical next
Fix plan is in [reports/testing/README.md](../reports/testing/README.md)
and
[final-consistency-audit.generated.md](../reports/testing/generated/canonical/final-consistency-audit.generated.md).
This file remains as a historical Apache Open Items reconcile.

## Source

- Open Issues: https://github.com/owasp-modsecurity/ModSecurity-apache/issues
- Open pull requests: https://github.com/owasp-modsecurity/ModSecurity-apache/pulls

## Summary

- Number of checked issues: 26
- Number of verified PRs: 4
- Number implemented: 6
- Number partially implemented: 12
- Number not implemented: 8
- Number not relevant: 3
- Number unclear: 1

Most important technical gaps:

- Phase-4/`RESPONSE_BODY` blocking is still not proven as a stable Apache connector capability. The runtime snapshots show expected `403` but actually `200` for several response body and outbound audit cases.
- V2 compatible Apache directives such as `SecDataDir` or `SecDefaultAction` are not registered as native Apache directives; they can only get into the libmodsecurity ruleset via the v3 connector directives and `modsecurity_rules`.
- Build-/Installationspfade are only partly documented more robustly. `DESTDIR` at `make install` and flexible `--with-libmodsecurity=/usr/lib` detection are not solved.
- Lacks regression testing for graceful restart memory behavior, full CRS v2/v3 parity, vhost/UID dependent audit logs, SecRequestBodyAccess off behavior, and full Phase 5 coverage.
- RemoteIPHeader is implemented locally and occupied by a connector's own runtime gate.

## Status table

| type | number | title | status | Relevance to ModSecurity connector | Relevance to testing framework | Evidence in Code/Test | Next Steps |
|---|---:|---|---|---|---|---|---|
| Issue | 12 | Having the exactly same results for apache version 2 and version 3 while running the OWASP CRS | Partially implemented | V2/v3 parity and CRS behavior | High, but only present as a subset | `docs/testing/generated/runtime/apache-runtime-results.generated.md`, `docs/testing/generated/coverage/connector-gap-summary.generated.md`, `docs/testing/v2-vs-v3-compatibility.md` | Add complete CRS run with log parser and v2/v3-Diff |
| Issue | 15 | Have all the phases correctly attached to Apache | Partially implemented | Apache hooks, filters, phases 1 to 5 | High | `connectors/apache/src/mod_security3.c`: `hook_request_late`, `hook_insert_filter`, `hook_log_transaction`; PR-70 tests phase 1 to 3 PASS, phase 4 former expected-failure | Stabilize phase 4 and supplement phase 5 testing |
| Issue | 17 | Implement the logging callback | Implemented | libmodsecurity log callback in Apache | Medium, dedicated logcallback test is missing | `modsecurity_log_cb`, `msc_set_log_cb`, `modsecurity_use_error_log` into `connectors/apache/src/mod_security3.c` and `connectors/apache/src/msc_config.c` | Add regression for error-log forwarding to `log,deny` |
| Issue | 23 | Configuration merge is not working as expected | Partially implemented | Directory/Location-Merge, ruleset merge, Enable/Disable | High | `msc_hook_merge_config_directory`; `ci/check-apache-directive-config.sh` tests `modsecurity off` in `Location` | Test merge order and directory vs location rule inheritance |
| Issue | 24 | Module name should be investigated | Not implemented | Module name and LoadModule compatibility | Low | Module remains `mod_security3.so` and `security3_module` in `connectors/apache/Makefile.am`, `COMPILE_APACHE.md` | Document decision or draft Alias-/Installationsstrategie |
| Issue | 25 | Make sure that the performance numbers are at least equally to the ones on version 2 | Not implemented | Performance/Regression | Medium | No benchmarks or performance suites found | Add Apache-v2/v3-Benchmark-Suite and baselines |
| Issue | 26 | Having all the configurations set in the Apache fashion | Partially implemented | Directives API and v2 compatibility | High | Only `modsecurity`, `modsecurity_rules`, `modsecurity_rules_file`, `modsecurity_rules_remote`, `modsecurity_use_error_log`, `modsecurity_transaction_id`, `modsecurity_transaction_id_expr` are registered | Create V2 directive matrix and define native compatibility strategy |
| Issue | 27 | Version banner at startup | Partially implemented | Startup logging | Low | `msc_hook_post_config` logs `ModSecurity-Apache v0.1.1-beta configured.` | Add libmodsecurity version, build source and test for banners |
| Issue | 30 | modsec audit log repeats section F | Not implemented | Response-Header/Audit-Log-Serialisierung | High | `output_filter` adds `err_headers_out` and `headers_out` per filter call; no guard flag against replay | Implement one-time header processing per transaction and add Section F testing |
| Issue | 47 | fail to compile on standard archlinux install | Not implemented | Autotools/APXS, installation target | High | `find_libmodsec.m4` expects prefix with `include/` and `lib/`; `Makefile.am` uses `@APXS@ -i` without `DESTDIR` | Implement libdir/pkg-config-Erkennung and DESTDIR-respecting installation |
| Issue | 55 | ./configure fails... configure: error: ModSecurity libraries not found! | Partially implemented | Build documentation and libmodsecurity detection | Medium | `COMPILE_APACHE.md` documents `--with-libmodsecurity`; `find_libmodsec.m4` remains prefix-oriented | Add `pkg-config`, explicit Lib/Header-Pfade and better error messages |
| Issue | 57 | General Apache Startup Error | Partially implemented | Directives and v2 vs v3 configuration | Medium | Docs mention v3 connector directives; `SecDataDir` is not an Apache directive of the connector | Add migration documentation for v2 directives and, if necessary, warning compatibility directives |
| Issue | 67 | Apache error log does not work for blocking actions | Unclear | Blocking log path and callback | High | Callback exists, but no test occupies `log,deny` in Apache error log | Include reproduction case as regression test |
| Issue | 72 | ModSecurity SecRequestBodyAccess Off still process the POST request | Not implemented | Request body filter and phase 2 | High | `hook_request_late` and `input_filter` call `msc_process_request_body` with no visible SecRequestBodyAccess off-gate logic | Test off-fall and link body processing to engine status |
| Issue | 77 | What does "ModSecurity-apache is unstable" mean, exactly? | Partially implemented | Documentation and v2 configuration differences | Medium | `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md` document current status and gaps | Add user-oriented "v2 to v3 Apache config" documentation |
| Issue | 78 | The modsecurity-apache v2.9 rule chain always appears #conforms | Not relevant | Affects v2.9, not the v3 Apache connector in the workspace | Low | No v3 relevance found | No connector code required; If necessary, refer to upstream v2 |
| Issue | 79 | Under mod_ruid2 ot mod_mpm_itk SecAuditLog is only being logged to when request is to an IP (or localhost) | Not implemented | Audit log under vhost/UID-Kontext | Medium | No mod_ruid2/mod_mpm_itk-spezifische logic or tests | Add vhost/UID-Audit-Szenario to Apache harness |
| Issue | 80 | Future plans? | Not relevant | Project planning, no specific code requirement | Low | Roadmap-/Statusdokumente exist locally | No technical implementation except roadmap maintenance |
| Issue | 81 | Apache connector 3.0 not factoring in RemoteIPHeader like mod_security2 | Implemented | REMOTE_ADDR/RemoteIPHeader | High | `msc_apache_client_ip` uses `r->useragent_ip`; `ci/check-apache-directive-config.sh` tests `RemoteIPHeader X-Forwarded-For` with status `406` | Make testing more visible in the framework or CI pipeline |
| Issue | 82 | apache graceful restart + Apache connector + rules = memory leak | Not implemented | Lifetime/Cleanup on graceful restart | High | No memory test; `rules_set`-Cleanup and `name_for_debug`-Lifetime are not proven by tests | Add graceful restart leak test and cleanup audit |
| Issue | 83 | modsec3 module not loaded for Linux 7.2 os version | Partially implemented | ABI/API compatibility with libmodsecurity | Medium | `msc_new_transaction_with_id` is used; `COMPILE_APACHE.md` documents Load-/ldd-Mismatch | Add Version-/Symbol-Check or clear minimum version in configure |
| Issue | 84 | Unable to disable module once loaded | Implemented | `modsecurity off` in Apache contexts | High | `msc_config_modsec_state`, `create_tx_context`; `ci/check-apache-directive-config.sh` expects `Location` bypass with HTTP `200` | Add framework test for vhost/location-disable |
| Issue | 85 | Segmentation Fault in modsecurity_log_cb (Security) | Implemented | Security-related format string fix | High | `modsecurity_log_cb` uses `"%s", msg` for `ap_log_rerror` and `ap_log_error` | Add security regression case with `%` in the log text |
| Issue | 87 | v3.0.5 of ModSecurity breaks apache connector | Partially implemented | API types `Rules`/`RuleSet` | High | `mod_security3.h` uses `rules_set.h` conditionally and `void *rules_set`; no v3.0.5 matrix | Add build matrix against 3.0.5 and current v3 |
| Issue | 89 | Plans for production readiness? | Not relevant | Projekt-/Supportfrage | Low | Local documentation highlights known gaps | Keep roadmap current, no direct code fix |
| Issue | 90 | Is it possible to change the SecAuditLogStorageDir variable so that the logs are sorted by vhost? | Not implemented | Audit log configuration per vhost | Low to medium | No vhost-based `SecAuditLogStorageDir` extension found | Check whether libmodsecurity-Variable/Apache-Ausdruck can be integrated sensibly |
| PR | 56 | Small fixes | Partially implemented | Request body processing, format string, filter removal | High | Format string done by PR #86; `ap_remove_input_filter` completed by PR #65; `hook_request_late` continues to process Body | Divide PR into partial changes; Test body duplication and empty body case |
| PR | 65 | Removing the input filter using the corresponding API | Implemented | Input filter error path | Medium | `connectors/apache/src/msc_filters.c` uses `ap_remove_input_filter` in `input_filter` | Add regression for intervention in the input filter |
| PR | 70 | Enable audit log and add 00-phases tests | Partially implemented | Audit log phase testing | High | `pr70_phase1_audit_request_header`, `pr70_phase2_audit_urlencoded_body`, `pr70_phase3_audit_response_header` PASS; `pr70_phase4_response_body_audit_xfail` former expected failure | Stabilize Phase 4 and import Phase 5 test |
| PR | 86 | Fix logging format string | Implemented | Security fix in log callback | High | `modsecurity_log_cb` uses fixed format string `"%s"` | Add dedicated `%` payload test |

## Details per Issue/PR

### Issue #12: Having the exactly same results for apache version 2 and version 3 while running the OWASP CRS

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/12
- Type: Issue
- Status assessment: Partially implemented
- Short description: A complete comparison of Apache v2 and Apache v3 when running the OWASP CRS with log parser evaluation is desired.
- Relevant files in the ModSecurity connector: `reports/testing/real-world-connector-validation.md`, `reports/testing/generated/runtime/runtime-matrix.generated.md`, `README.md`.
- Relevant tests in the ModSecurity test framework: `docs/testing/generated/runtime/apache-runtime-results.generated.md`, `docs/testing/generated/runtime/runtime-matrix.generated.md`, `docs/testing/v2-vs-v3-compatibility.md`.
- Evaluation: The framework covers many portable rule, body, audit and phase cases, but not a complete CRS-v2/v3-Gleichlauf.
- Missing implementation: Full CRS run, ModSecurity log utilities integration, reproducible v2 vs v3 diff and accepted deviation list.
- Recommended next steps: Include CRS fixtures in `ModSecurity-test-Framework`, add CRS profile to `ci/run-apache-smoke.sh`, persist log parser output as an artifact. Assumed effort: high.

### Issue #15: Have all the phases correctly attached to Apache

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/15
- Type: Issue
- Status assessment: Partially implemented
- Short description: All libmodsecurity phases should be correctly connected to Apache hooks and filters.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `hook_request_late`, `hook_insert_filter`, `hook_log_transaction`, `process_request_headers`; `connectors/apache/src/msc_filters.c` with `input_filter` and `output_filter`.
- Relevant tests in the ModSecurity test framework: `tests/cases/audit-log/pr70-phases/pr70_phase1_audit_request_header.yaml`, `pr70_phase2_audit_urlencoded_body.yaml`, `pr70_phase3_audit_response_header.yaml`, `pr70_phase4_response_body_audit_xfail.yaml`, `docs/testing/generated/runtime/apache-runtime-results.generated.md`.
- Assessment: Phases 1 to 3 are occupied by PR-70 derivatives; Phase 4 remains a former expected failure and Phase 5 does not have a comparable PR-70 test.
- Lack of implementation: Robust response body blocking, full audit assertions for phase 4 and dedicated phase 5 logging test.
- Recommended next steps: Add Guard/State to `output_filter`, verify `msc_process_response_body` only once per transaction, derive phase 5 YAML from PR #70. Assumed effort: high.

### Issue #17: Implement the logging callback

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/17
- Type: Issue
- Status assessment: Implemented
- Short description: libmodsecurity should be able to write log messages to the Apache error log.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `modsecurity_log_cb` and `msc_set_log_cb`; `connectors/apache/src/msc_config.c` with `modsecurity_use_error_log`.
- Relevant tests in the ModSecurity-test framework: No dedicated callback test found.
- Evaluation: The callback is implemented and uses fixed format strings.
- Missing implementation: Test coverage for actual error log entries for `log`, `deny` and `modsecurity_use_error_log off`.
- Recommended next steps: Add error log assertion to Apache harness. Assumed effort: medium.

### Issue #23: Configuration merge is not working as expected

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/23
- Type: Issue
- Status assessment: Partially implemented
- Short description: Directory and location configurations should be merged like in v2.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_config.c` with `msc_hook_create_config_directory` and `msc_hook_merge_config_directory`; `connectors/apache/src/mod_security3.c` with `create_tx_context`.
- Relevant tests in the ModSecurity test framework: No comprehensive Directory-/Location-Merge-Matrix. Connector's own gate: `ci/check-apache-directive-config.sh`.
- Evaluation: Enable/Disable and transaction ID overrides are merged, rulesets too, but the order and v2 parity are not fully occupied.
- Missing implementation: Tests for Parent/Child-Regelreihenfolge, Directory-vs-Location-Precedence, `modsecurity_rules_file` and `modsecurity_rules_remote` in nested contexts.
- Recommended next steps: Add connector-specific Apache YAML or CI cases for merge semantics; If there is a deviation, check the `msc_rules_merge` sequence. Assumed effort: medium to high.

### Issue #24: Module name should be investigated

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/24
- Type: Issue
- Status assessment: Not implemented
- Short description: It should be checked whether the module should be called `mod_security` instead of `mod_security3`.
- Relevant files in the ModSecurity connector: `connectors/apache/Makefile.am`, `connectors/apache/build/apxs-wrapper.in`, `COMPILE_APACHE.md`.
- Relevant tests in the ModSecurity test framework: None.
- Assessment: The current workspace continues to use `mod_security3.so` and `security3_module`.
- Missing implementation: naming decision, possible Alias-/Symlink-Strategie and migration documentation.
- Recommended next steps: Record decision in `docs/connectors/directive-parity.md` or build documentation, test installation path. Assumed effort: low to medium.

### Issue #25: Make sure that the performance numbers are at very least equally to the ones on version 2

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/25
- Type: Issue
- Status assessment: Not implemented
- Short description: Apache v3 performance should at least reach v2 level or be similarly documented.
- Relevant files in ModSecurity connector: No performance suite found.
- Relevant tests in the ModSecurity test framework: No benchmarks found.
- Assessment: The workspace contains functional smoke and runtime matrix artifacts, but no performance baselines.
- Missing implementation: load test scenarios, Latenz-/Durchsatzmessungen, v2/v3-Vergleich with CRS.
- Recommended next steps: Create a separate benchmark profile in `ModSecurity-test-Framework/ci` and store results in `reports/testing/`. Assumed effort: high.

### Issue #26: Having all the configurations set in the Apache fashion

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/26
- Type: Issue
- Status assessment: Partially implemented
- Short description: v2-like Apache configuration directives should be available in v3 or migrated cleanly.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_config.c`, `common/include/msconnector/directives.h`, `docs/connectors/directive-parity.md`, `README.md`.
- Relevant tests in the ModSecurity test framework: `ci/check-apache-directive-config.sh` in the connector; Framework only has indirect rule tests.
- Evaluation: The v3 connector directives are registered. Broad native v2 directive compatibility is not available.
- Missing implementation: Directive matrix for v2 Apache configuration names, Warn-/Fallback-Verhalten for no longer supported directives, tests for startup vs runtime errors.
- Recommended next steps: Map V2 directives from `ModSecurity_V2/apache2/apache2_config.c` against current v3 connector directives. Assumed effort: high.

### Issue #27: Version banner at startup

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/27
- Type: Issue
- Status assessment: Partially implemented
- Short description: A helpful version banner should appear when starting.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.h` with `MSC_APACHE_CONNECTOR`; `connectors/apache/src/mod_security3.c` with `msc_hook_post_config`.
- Relevant tests in the ModSecurity test framework: No banner assertion.
- Evaluation: The connector logs the connector name and version, but not libmodsecurity version or build details.
- Missing implementation: Extended diagnostic information and test that the banner appears in the error log.
- Recommended next steps: Add libmodsecurity version to `msc_hook_post_config` and add log assertion. Assumed effort: low.

### Issue #30: modsec audit log repeats section F

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/30
- Type: Issue
- Status assessment: Not implemented
- Short description: Section F of the audit log contains repeated response headers.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_filters.c` with `output_filter`.
- Relevant tests in the ModSecurity test framework: `tests/cases/response/headers/phase3_response_headers_multi_value_connector_gap.yaml`, `phase3_response_headers_duplicate_value_runtime_difference.yaml`, `docs/testing/generated/runtime/apache-runtime-results.generated.md`.
- Evaluation: The output filter adds response headers per filter pass; an “already processed” flag is not visible.
- Missing implementation: Transaction state for one-time `msc_process_response_headers` execution and Section F deduplication regression.
- Recommended next steps: Add state to `msc_t`, pass headers only once to libmodsecurity, check audit log fixture with duplicate headers. Assumed effort: medium.

### Issue #47: fail to compile on standard archlinux install

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/47
- Type: Issue
- Status assessment: Not implemented
- Short description: `./configure --with-libmodsecurity=/usr/lib` cannot find the library; `make install` does not respect `DESTDIR`.
- Relevant files in the ModSecurity connector: `connectors/apache/build/find_libmodsec.m4`, `connectors/apache/Makefile.am`, `connectors/apache/build/apxs-wrapper.in`.
- Relevant tests in the ModSecurity test framework: `ci/prepare-apache-build.sh` uses a staging prefix, but does not test Arch-Layout or `DESTDIR`.
- Assessment: The local build path is usable for the framework staging prefix, but the reported distribution packaging issue remains.
- Missing implementation: libdir/include-dir/pkg-config-Erkennung and installation target without root write access.
- Recommended next steps: Add `PKG_CHECK_MODULES` or explicit `--with-libmodsecurity-libdir`/`--with-libmodsecurity-includedir`, add `DESTDIR` installation test. Assumed effort: medium.

### Issue #55: ./configure fails... configure: error: ModSecurity libraries not found!

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/55
- Type: Issue
- Status assessment: Partially implemented
- Short description: Users cannot reliably pass an installed libmodsecurity to `configure`.
- Relevant files in the ModSecurity connector: `COMPILE_APACHE.md`, `connectors/apache/build/find_libmodsec.m4`, `connectors/apache/docs/build.md`.
- Relevant tests in the ModSecurity test framework: `ci/prepare-apache-build.sh` with `./configure --with-libmodsecurity=$MODSECURITY_STAGE`.
- Review: Documentation and framework path help, but autoconf detection remains restrictive.
- Missing implementation: Better error message for incorrect prefix, support for library file or pkg-config.
- Recommended next steps: Make Configure macros more robust and add negative/positive Configure tests. Assumed effort: medium.

### Issue #57: General Apache Startup Error

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/57
- Type: Issue
- Status assessment: Partially implemented
- Short description: Apache does not recognize v2 directives like `SecDataDir` as Apache directives of the v3 connector.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_config.c`, `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md`.
- Relevant tests in the ModSecurity-test framework: No direct `SecDataDir` startup regression.
- Assessment: The workspace documents the v3 directives, but not full v2 migration compatibility.
- Missing implementation: migration instructions, example configurations and possibly warning compatibility directives.
- Recommended next steps: Extend `COMPILE_APACHE.md` with v2-to-v3 configuration examples; Add startup error test for direct v2 directives. Assumed effort: medium.

### Issue #67: Apache error log does not work for blocking actions

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/67
- Type: Issue
- Status rating: Unclear
- Short description: `log,deny` is supposed to write to the Apache error log during blocking actions, but according to the issue it doesn't.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `modsecurity_log_cb` and `process_intervention`.
- Relevant tests in the ModSecurity test framework: No dedicated error log test; Audit log tests are in place.
- Evaluation: The callback exists, but existing artifacts do not occupy the specific `log,deny` path in the Apache error log.
- Missing implementation: Reproduction and regression testing with `SecRuleEngine On` and `log,deny`.
- Recommended next steps: Include an error log assert for blocking rules in `ci/check-apache-directive-config.sh` or framework. Assumed effort: medium.

### Issue #72: ModSecurity SecRequestBodyAccess Off still process the POST request

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/72
- Type: Issue
- Status assessment: Not implemented
- Short description: With `SecRequestBodyAccess Off`, phase 2 or request body processing continues to be triggered.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `hook_request_late`; `connectors/apache/src/msc_filters.c` with `input_filter`.
- Relevant tests in the ModSecurity test framework: `tests/cases/phases/phase1/phase1_vs_phase2_request_body_gap.yaml`, `tests/cases/negative-pass-through/phase2_header_only_pass_through.yaml`, `docs/testing/generated/runtime/apache-runtime-results.generated.md`.
- Evaluation: No explicit off-gate logic is visible; the runtime case `phase1_vs_phase2_request_body_gap` fails.
- Lack of implementation: Body processing must respect Engine-/Ruleset-Status; Debug log double start should be regression tested.
- Recommended next steps: Add `SecRequestBodyAccess Off` and POST body to the YAML case, then correct Filter-/Hook-Pfad. Assumed effort: medium to high.

### Issue #77: What does "ModSecurity-apache is unstable" mean, exactly?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/77
- Type: Issue
- Status assessment: Partially implemented
- Short description: Documentation question about production readiness and v2/v3-Konfigurationsunterschieden, including `SecDefaultAction` startup error.
- Relevant files in the ModSecurity connector: `README.md`, `COMPILE_APACHE.md`, `docs/connectors/directive-parity.md`, `reports/testing/test-coverage-overview.md`.
- Relevant tests in the ModSecurity test framework: `docs/testing/generated/runtime/apache-runtime-results.generated.md`, `docs/testing/generated/coverage/connector-gap-summary.generated.md`.
- Assessment: Local documentation describes supported directives and loopholes, but no clear end-user migration page.
- Missing implementation: Explicit declaration "unstable/not production ready", examples of CRS integration via `modsecurity_rules_file`, handling of v2 directives.
- Recommended next steps: Add user-oriented migration document. Assumed effort: low to medium.

### Issue #78: The modsecurity-apache v2.9 rule chain always appears #conforms

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/78
- Type: Issue
- Status rating: Not relevant
- Short description: The issue relates to ModSecurity Apache v2.9.
- Relevant files in the ModSecurity connector: None.
- Relevant tests in the ModSecurity test framework: None.
- Assessment: The current workspace assesses the v3 Apache connector and common v3/v2 compatibility cases, not a v2.9 database logging bug.
- Missing implementation: None for this connector.
- Recommended next steps: Check upstream v2 context separately if desired. Assumed effort: not applicable.

### Issue #79: Under mod_ruid2 ot mod_mpm_itk SecAuditLog is only being logged to when request is to an IP (or localhost)

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/79
- Type: Issue
- Status assessment: Not implemented
- Short description: Audit logging behaves differently under mod_ruid2 or mod_mpm_itk for name-based vhosts.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`; no specific UID/vhost-Logik.
- Relevant tests in the ModSecurity-test framework: General audit log tests, but no mod_ruid2/mod_mpm_itk- or vhost UID cases.
- Assessment: The reported scenario is not covered.
- Missing implementation: Apache harness with named vhost, changing Runtime-User/Group-Kontext and audit log rights.
- Recommended next steps: Reproduce first, then check whether libmodsecurity file opening or Apache process model is responsible. Assumed effort: high.

### Issue #80: Future plans?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/80
- Type: Issue
- Status rating: Not relevant
- Short description: Project planning question without specific technical requirements.
- Relevant files in the ModSecurity connector: `docs/roadmap/roadmap.md`, `README.md`.
- Relevant tests in the ModSecurity test framework: Not relevant.
- Assessment: No direct implementation can be derived.
- Lack of implementation: None.
- Recommended next steps: Keep roadmap current. Assumed effort: low.

### Issue #81: Apache connector 3.0 not factoring in RemoteIPHeader like mod_security2

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/81
- Type: Issue
- Status assessment: Implemented
- Short description: `REMOTE_ADDR` should use the client value set by mod_remoteip after `RemoteIPHeader X-Forwarded-For`.
- Relevant files in ModSecurity connector: `connectors/apache/src/mod_security3.c` with `msc_apache_client_ip`, `msc_apache_client_port` and hook order with `mod_remoteip.c`.
- Relevant tests in the ModSecurity test framework: Connector's own test `ci/check-apache-directive-config.sh`.
- Evaluation: Code uses `r->useragent_ip` and the CI gate blocks with `X-Forwarded-For: 1.2.3.4` with `REMOTE_ADDR @ipMatch 1.2.3.4`.
- Missing implementation: The test is in the Connector CI, not as a general framework YAML case.
- Recommended next steps: Include the RemoteIP case in the runtime matrix or reference the CI gate more visibly in the documentation. Assumed effort: low.

### Issue #82: apache graceful restart + Apache connector + rules = memory leak

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/82
- Type: Issue
- Status assessment: Not implemented
- Short description: Repeated graceful restarts with loaded rules increase memory consumption.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `msc_apache_init`/`msc_apache_cleanup`; `connectors/apache/src/msc_config.c` with `msc_create_rules_set` and `name_for_debug`.
- Relevant tests in the ModSecurity test framework: No memory or graceful restart suite.
- Rating: Cleanup is only roughly registered; Regeln-/Config-Lifetimes are not proven by leak tests.
- Missing implementation: Repeated `apachectl graceful` test with rules and memory metrics.
- Recommended next steps: Add leak repro in `ci/run-apache-smoke.sh` or separate long test; Audit ruleset cleanup. Assumed effort: high.

### Issue #83: modsec3 module not loaded for Linux 7.2 os version

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/83
- Type: Issue
- Status assessment: Partially implemented
- Short description: Apache cannot load the module due to missing symbol `msc_new_transaction_with_id`.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` uses `msc_new_transaction_with_id`; `COMPILE_APACHE.md` contains Load-/ldd-Troubleshooting.
- Relevant tests in the ModSecurity-test framework: `src/v3-api-smoke/v3_api_smoke.c` checks API base paths, but not module ABI against old libmodsecurity versions.
- Evaluation: Documentation helps with the diagnostic path, but there is no configure coercion or fallback for missing symbols.
- Missing implementation: Mindestversion/Symbolcheck during build or load diagnostics.
- Recommended next steps: Add Autoconf test for `msc_new_transaction_with_id` and document clear minimum version. Assumed effort: medium.

### Issue #84: Unable to disable module once loaded

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/84
- Type: Issue
- Status assessment: Implemented
- Short description: ModSecurity should be deactivable in individual contexts.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_config.c` with `msc_config_modsec_state`; `connectors/apache/src/mod_security3.c` with `create_tx_context`.
- Relevant tests in the ModSecurity test framework: Connector's own `ci/check-apache-directive-config.sh` with `Location "/__modsec_directive_off"`.
- Evaluation: `modsecurity off` prevents transaction creation locally and the runtime gate expects HTTP `200`.
- Missing implementation: General framework case for vhost/location-disable is missing.
- Recommended next steps: Add Apache-specific framework test or CI documentation reference. Assumed effort: low.

### Issue #85: Segmentation Fault in modsecurity_log_cb (Security)

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/85
- Type: Issue
- Status assessment: Implemented
- Short description: Insecure format string in `ap_log_rerror`/`ap_log_error` can trigger a crash or format-string attack.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c` with `modsecurity_log_cb`.
- Relevant tests in the ModSecurity test framework: No dedicated `%` payload test.
- Evaluation: Both Apache log calls use `"%s", msg` locally.
- Missing implementation: Regression test with `%` sequences in Regel-/Payload-Logtext.
- Recommended next steps: Add security smoke to Apache harness. Assumed effort: low.

### Issue #87: v3.0.5 of ModSecurity breaks apache connector

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/87
- Type: Issue
- Status assessment: Partially implemented
- Short description: Type change `Rules` to `RuleSet` breaks the build against certain libmodsecurity-v3 versions.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.h` with `MSC_USE_RULES_SET`, `rules_set.h` and `void *rules_set`; `connectors/apache/src/mod_security3.c` without old `(Rules *)` cast.
- Relevant tests in the ModSecurity test framework: `src/v3-api-smoke/v3_api_smoke.c`; no explicit v3.0.5 build matrix.
- Assessment: The old hard `Rules` cast is locally mitigated, but the version condition is not proven against v3.0.5.
- Missing implementation: Build test against v3.0.5 and current v3, including header paths in `msc_filters.h`/`msc_utils.h`.
- Recommended next steps: Add matrix in CI or local build script, check macros based on real headers. Assumed effort: medium.

### Issue #89: Plans for production readyness?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/89
- Type: Issue
- Status rating: Not relevant
- Short description: Projekt-/Supportfrage ready for production.
- Relevant files in the ModSecurity connector: `README.md`, `docs/roadmap/roadmap.md`, `reports/testing/real-world-connector-validation.md`.
- Relevant tests in the ModSecurity test framework: Runtime matrix and smoke artifacts as evidence, but no direct "production ready" test.
- Assessment: No single actionable code item.
- Lack of implementation: No technical implementation directly from the issue.
- Recommended next steps: Keep Status-/Roadmapdokumente up to date and clearly state known gaps. Assumed effort: low.

### Issue #90: Is it possible to change the SecAuditLogStorageDir variable so that the logs are sorted by vhost?

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/issues/90
- Type: Issue
- Status assessment: Not implemented
- Short description: Audit logs should be able to be written to different storage directories in vhost.
- Relevant files in ModSecurity-conector: No vhost-based extension found; Audit paths are configured via libmodsecurity rules.
- Relevant tests in the ModSecurity test framework: Audit log tests use `@@AUDIT_LOG@@` and `@@AUDIT_LOG_DIR@@`, but no vhost sorting.
- Rating: Currently not implemented.
- Missing implementation: concept for Apache-Ausdruck/vhost-Variable in audit log configuration or documentation why this is on the libmodsecurity side.
- Recommended next steps: Check feasibility with libmodsecurity configuration model; Add vhost harness test. Assumed effort: medium.

### PR #56: Smallfixes

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/56
- Type: PR
- Status assessment: Partially implemented
- Short description: PR bundles format string workaround, request body processing and test configuration changes.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c`, `connectors/apache/src/msc_filters.c`.
- Relevant tests in the ModSecurity test framework: `tests/cases/phases/phase1/phase1_vs_phase2_request_body_gap.yaml`, `tests/cases/audit-log/pr70-phases/*`.
- Evaluation: Format string fix is ​​implemented more cleanly by PR #86; Input filter removal by PR #65. The body processing part is not fully adopted and the local code continues to call `msc_process_request_body` in `hook_request_late`.
- Missing implementation: Unique request body state machine, empty body case, off case, CRS regression proof.
- Recommended next steps: Break PR into atomic fixes and apply with tests only. Assumed effort: medium to high.

### PR #65: Removing the input filter using the corresponding API

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/65
- Type: PR
- Status assessment: Implemented
- Short description: `ap_remove_input_filter` should be used instead of `ap_remove_output_filter` in the input filter.
- Relevant files in the ModSecurity connector: `connectors/apache/src/msc_filters.c`.
- Relevant tests in the ModSecurity test framework: No dedicated input filter error path test.
- Evaluation: Local code uses `ap_remove_input_filter` in null context and intervention path.
- Lack of implementation: regression test for input filter intervention.
- Recommended next steps: Add early intervention to POST body blocking case. Assumed effort: low.

### PR #70: Enable audit log and add 00-phases tests

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/70
- Type: PR
- Status assessment: Partially implemented
- Short description: PR activates audit log evaluation in Apache::Test and adds phase tests.
- Relevant files in the ModSecurity connector: No direct code change necessary; `connectors/apache/src/mod_security3.c` and `connectors/apache/src/msc_filters.c` are relevant.
- Relevant tests in the ModSecurity test framework: `tests/cases/audit-log/pr70-phases/pr70_phase1_audit_request_header.yaml`, `pr70_phase2_audit_urlencoded_body.yaml`, `pr70_phase3_audit_response_header.yaml`, `pr70_phase4_response_body_audit_xfail.yaml`, `docs/testing/pr70-audit-phase-coverage-plan.md`.
- Assessment: Phases 1 to 3 were imported as portable YAML cases and run according to the runtime snapshot PASS. Phase 4 remains former expected failure; Phase 5 is not imported.
- Missing implementation: Stable phase 4 response body assertions and Phase-5-Audit-/Logging-Test.
- Recommended next steps: Derive phase 5 case from PR #70, repair response body path first. Assumed effort: medium to high.

### PR #86: Fix logging format string

- Link: https://github.com/owasp-modsecurity/ModSecurity-apache/pull/86
- Type: PR
- Status assessment: Implemented
- Short description: Fix for Issue #85 with fixed format string.
- Relevant files in the ModSecurity connector: `connectors/apache/src/mod_security3.c`.
- Relevant tests in the ModSecurity test framework: No dedicated `%` payload test.
- Assessment: The patch content is present locally: `ap_log_rerror(..., "%s", msg)` and `ap_log_error(..., "%s", msg)`.
- Missing implementation: Automatic regression test.
- Recommended next steps: Add test case with `%5C`, `%n`-like sequences in the logged text. Assumed effort: low.

## Missing tests

- Complete OWASP-CRS-v2/v3-Vergleich with log parser for Issue #12.
- Phase 4 response body blocking as a stable PASS, including audit log section and intervention, for Issue #15, PR #70 and related response body gaps.
- Phase-5-Logging/Audit-Test from PR #70.
- Error log callback test for `log,deny`, `DetectionOnly`, `success` and `modsecurity_use_error_log off` for issues #17 and #67.
- Directory-/Location-/vhost-Merge-Matrix for Issue #23 and Issue #84.
- `SecRequestBodyAccess Off` with POST body and Debug-/Audit-Negativassertion for Issue #72.
- Audit Log Section F deduplication for Issue #30.
- mod_ruid2/mod_mpm_itk or equivalent vhost/UID-Audit-Log-Repro for Issue #79.
- Graceful restart memory leak test for issue #82.
- Build matrix for Arch-/Alpine-artige layouts, `DESTDIR`, `pkg-config` and libmodsecurity-v3.0.5 for issues #47, #55, #83 and #87.
- Startup banner assertion with connector and libmodsecurity version for issue #27.
- Performance benchmark against ModSecurity v2 for Issue #25.
- Vhost based `SecAuditLogStorageDir` or audit trail testing for Issue #90.

## Prioritization

### High

- Issue #85 / PR #86: Format string security is implemented, but regression testing is missing.
- Issue #15 / PR #70: Phase 4 and Phase 5 coverage missing; `RESPONSE_BODY` remains unverified.
- Issue #72: `SecRequestBodyAccess Off` is not sufficiently respected or tested.
- Issue #30: Audit Log Section F duplicates can break forensics and parity.
- Issue #47, #55, #83, #87: Build/ABI compatibility may block installation or module load.
- Issue #82: Graceful restart leak with rules can endanger production operations.
- Issue #23: Config merge parity is central to vhost/Location-Sicherheit.
- Issue #67: Blocking error log behavior is relevant to security operations, but unclear.

### Medium

- Issue #12: CRS v2/v3 parity is important, but a longer validation distance.
- Issue #26, #57, #77: V2 to v3 configuration migration gaps.
- Issue #79: Audit log behavior under vhost/UID-Modulen.
- Issue #81: RemoteIPHeader is implemented; Framework promotion of the test would make sense.
- Issue #84: Deactivation is implemented; wider Merge-/vhost-Regression is missing.
- PR #56, PR #65: Partially adopted fixes should be atomically secured with tests.
- Issue #90: Vhost sorted audit logs are functionally useful, but not core-blocking.

### Low

- Issue #24: Modulname/Installationsalias is, above all, migration convenience.
- Issue #27: Startup banner is partially present, extension and test are missing.
- Issue #78: Affects v2.9 and is not relevant to this v3 connector.
- Issue #80 and Issue #89: Project planning questions without a direct code fix.
- Documentation cleanup for known Apache vs NGINX deviations, particularly Apache without NGINX Phase 4 directives.
