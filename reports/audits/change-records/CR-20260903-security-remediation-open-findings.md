# Change Record CR-20260903-security-remediation-open-findings

**Language:** English | [Deutsch](CR-20260903-security-remediation-open-findings.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260903-security-remediation-open-findings |
| Date (UTC) | 2026-09-03 |
| Base revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 |
| Branch | codex/security-remediation-open-findings-20260903 |
| Final HEAD_SHA | This record is part of the delivery head and therefore cannot truthfully self-reference its own final Git object. The exact immutable final SHA is recorded in the Draft PR metadata and task delivery evidence after this record is committed. |
| Delivery status | Draft PR [#354](https://github.com/Easton97-Jens/ModSecurity-conector/pull/354) is open and unmerged. Local remediation and focused validation are complete; the post-correction hosted runtime rerun remains pending. |

## Motivation and problem statement

The current origin/master base still had five Parent-owned connector/runtime security gaps and an incomplete Authorization response-companion lifecycle. The related Envoy grpc-go finding was already fixed on the base and is only verified here. The remediation is Parent-only: Framework, MRTS, Gitlinks, CI permissions, dependencies, and master are not changed.

| Finding | Root cause on the base | Security invariant and remediation |
| --- | --- | --- |
| A — HAProxy SPOP request target | A generic 1024-byte copy could silently truncate length-delimited path/uri values before WAF inspection. | A request target is either copied losslessly up to the explicit 4096-byte limit or rejected, including embedded-NUL and over-limit inputs. |
| B — Event JSONL query privacy | Serializers and integrity metadata represented the raw URI, allowing query values into JSONL. | The WAF retains the raw URI; serialization and its integrity representation use a query-redacted URI and record redaction. |
| C — NGINX callback logging | The native libModSecurity callback wrote to the NGINX error-log sink without checking the effective use_error_log value. | modsecurity_use_error_log off suppresses that host sink without disabling WAF processing or the independent event JSONL path. |
| D/E — Traefik UDS transport and workers | Blocking socket I/O, unbounded admission, and unsafe bounded-wait teardown could hang, exhaust workers, or release service state too early. | One monotonic per-frame deadline, nonblocking I/O, bounded admission (64 default; 256 hard maximum), active-socket shutdown, and deferred one-time cleanup keep the service bounded. |
| F — FND-PARENT-1013 Authorization companion | The base used an unbounded worker wait and destructive cleanup/abort on a non-quiescent companion failure. | Heap-owned deferred cleanup permits exactly one release only after workers and companion quiescence; configured companions remain quarantined on failed shutdown. |
| Envoy grpc-go floor | Already remediated on the base. | No dependency change is made; module-graph verification preserves google.golang.org/grpc v1.83.1. |

## Acceptance criteria

- The affected request, event, host-log, UDS, and Authorization lifecycle paths
  enforce the invariants in the baseline table without changing Framework/MRTS
  or the already-fixed Envoy dependency.
- Focused positive, boundary, and negative regression checks pass where the
  necessary local host/toolchain is available.
- Generated documentation remains current, English/German records remain
  paired, and all unavailable host or Framework checks are explicitly recorded.
- The resulting review branch is delivered only as a Draft PR; no merge or
  default-branch write is performed.

## Implementation decision and rationale

The implementation ports only the current-base-required security controls. Historical broad PRs are reference evidence, not merge sources. The Authorization port excludes unrelated duplicate-host validation and SIGPIPE strategy changes. The NGINX configuration reference is generated from a NGINX-only metadata override, so its English/German files and canonical configuration inventory remain source-backed rather than manually divergent. Hosted Lighttpd feedback then showed that its runtime harness still expected a raw query-bearing JSONL URI; the harness now expects the safe serialized URI and `redacted=true` while retaining raw curl-wire and correlated CRS-log evidence.

## Changed files

- Common runtime and event serialization: common/include/msconnector/event.h, common/src/event.c, common/src/integrity_event.c, and common/runtime/http_authorization_service.c.
- Connector implementation: connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c, connectors/nginx/src/ngx_http_modsecurity_log.c, and connectors/traefik/src/traefik_engine_service.c.
- Focused regressions: tests/event_json_query_redaction_test.c, tests/haproxy_spop_request_target_test.c, tests/test_haproxy_spop_request_target.py, tests/http_authorization_service_detached_worker_smoke.c, tests/test_http_authorization_service_worker_contract.py, tests/test_nginx_error_log_callback_contract.py, and tests/test_traefik_engine_service_contract.py.
- Lighttpd runtime-redaction regression: connectors/lighttpd/harness/run_patched_full_lifecycle.sh and connectors/lighttpd/tests/test_patched_host_contract.py.
- Source-backed documentation/inventory: ci/checks/documentation/connector_config_reference.py, examples/nginx/configuration-reference.md, examples/nginx/configuration-reference.de.md, and reports/connector-configuration-inventory.json.
- Operator documentation: common/docs/transaction-phase-contract.md and .de.md; connectors/haproxy, nginx, and traefik README pairs; and examples/traefik README pairs.
- Traceability: this paired Change Record and the paired archive indexes.

## Commands executed

| Check | Result |
| --- | --- |
| HAProxy executable parser regression | Passed: 1024/4096-byte path and uri controls, over-limit rejection, and embedded-NUL rejection. |
| HAProxy C17 and ASan/UBSan | Passed. |
| Common JSONL redaction linked test and ASan/UBSan | Passed; raw WAF URI remains distinct from redacted JSONL/integrity output. |
| Common security contract | Passed. |
| NGINX callback, phase-runner, and upstream-security contracts | Passed: 23 tests (3 skipped). |
| NGINX generated-reference and focused contract tests | Passed: 5 tests; make check-connector-config-reference passed. |
| NGINX C17 host compilation | Blocked: this environment lacks NGINX headers/source; no header installation or host emulation was performed. |
| Authorization timeout, detached-worker smoke, ASan/UBSan, and TSan | Passed. The configured-companion late-quiescence branch has static contract coverage; no dynamic host-companion fixture exists. |
| Envoy module graph, Go test, and Go vet | Passed; module graph reports google.golang.org/grpc v1.83.1. |
| Traefik contracts/native-plugin/Authorization worker contracts | Passed: 47 tests. |
| Traefik C17 syntax and engine-service build/self-test/runtime/negative test | Passed with GCC and Clang syntax checks; normal, ASan/UBSan, and TSan engine-service runs passed. |
| Lighttpd JSONL-redaction harness contract | Passed: 37 tests (2 skipped) and `bash -n`. A first hosted Lighttpd runtime run exposed its stale raw-URI JSONL expectation; the scoped harness correction preserves the raw wire/CRS correlation and requires `/?<redacted>` with `redacted=true`. |
| Directive parity | Passed. |
| Full bilingual/link checks | Blocked solely by pre-existing missing Framework-submodule link targets; the task neither initializes nor modifies the Framework. |

## Security impact

The changes reduce request-target ambiguity, query-value disclosure, logging-configuration bypasses, local UDS resource exhaustion, and asynchronous use-after-free/double-release risk. Event JSONL redaction applies to newly emitted records; operators must treat historical JSONL and audit logs as potentially sensitive and restrict, rotate, or retain them according to local policy. No production service was contacted and no real credential, cookie, token, password, or personal data was used in tests or evidence.

## Runtime evidence

The local Traefik engine service was built and exercised over a private Unix
socket for normal, malformed-frame, and socket-ownership-negative controls.
It is not a Traefik host-runtime test. No production service was contacted.
The hosted Lighttpd CRS/no-MRTS runtime is the authoritative host validation
for the updated JSONL harness contract; its rerun is pending on the current
Draft-PR head.

## Checks not run and rationale

NGINX C17 host compilation/runtime is blocked by missing local NGINX
headers/source. Full bilingual and link checks are blocked only by existing
missing Framework-submodule targets; no Framework initialization or change is
authorized. Full HTTP/1.1, HTTP/2, and HTTP/3 host matrices require local host
fixtures that are not present.

## Known limitations

A configured Authorization companion has static lifecycle-contract coverage but
no dynamic late-quiescence fixture. The local Traefik service test does not
exercise a Traefik host process. These are evidence limits, not a claim that
the safety controls are disabled.

## Remaining risks

Historical JSONL and audit records can still contain data emitted before this
redaction change. The corrected exact-head Lighttpd runtime rerun, other
hosted CI, review, and any merge decision remain separate future evidence. No
merge is requested or performed.

## Final diff and review status

In progress until the post-correction final diff is committed and read back
from the task branch and Draft PR. The current user authorizes a normal
task-branch push and Draft PR only; merge, force-push, rebase of published
work, and default-branch writes remain unauthorized.

## 2026-09-03 review-remediation follow-up for Draft PR #354

This follow-up records the requested review pass against starting head
`c44dd04a16cb698584c023e2f81521e07f5c3fb2`. It is intentionally not a claim
that the successor head has been pushed or that hosted checks have completed.

The scoped remediation and evidence work is as follows:

- RR1 extends the Common JSONL URI-redaction helper with explicit truncation
  output. The serializer now combines redaction and safe-buffer truncation,
  including partial `<redacted>` markers, in both JSON and JSONL; tests cover
  long paths with and without queries, canary absence, `redacted=true`,
  `truncated=true`, unchanged raw WAF URIs, and consistent integrity output.
- RR2/RR4 make Traefik slot invalidation and descriptor close one locked
  ownership operation, guard shutdown with `socket_fd >= 0`, and add a
  controlled descriptor-reuse/shutdown race plus dynamic `max_workers=2`
  admission, slot-reuse, create-failure rollback, and slow/non-reading-peer
  coverage.
- RR3 adds executable HAProxy parser/mapper cases at exactly 1023 bytes and
  places a harmless marker only after byte 1023, proving full boundary reach
  or explicit rejection rather than relying on a static Python length loop.
- RR5 adds a dynamic live response-companion fixture for quiescence, failed
  shutdown, exactly-once release after worker drain, competing owner/worker
  release, and the no-companion deferred path. FND-PARENT-1013 remains
  `fixed, verification pending` until fresh exact-head evidence proves these
  cases.
- The first Lighttpd hosted run exposed a stale harness expectation for raw
  query-bearing JSONL. The scoped correction correlates the safe redacted
  event by response transaction ID while preserving raw wire and CRS evidence.
- Local NGINX headers/source are unavailable. A clearly named
  `Exact-Head-Hosted` NGINX gate is therefore required for supported-header
  compilation and isolated `modsecurity_use_error_log` on/off runtime proof;
  no local host result is claimed.

### SonarQube Cloud: twelve PR-new issues triaged individually

The twelve issues reported for PR #354 were triaged at the starting head as
follows. Nine are addressed by maintainability refactors or const-correctness
fixes; three public test-stub findings are documented non-problems because
their signatures must match the production header ABI. No `NOSONAR`, rule
exclusion, threshold change, or Quality-Gate weakening was used.

| # | Sonar key / rule | Location/issue | Disposition |
|---:|---|---|---|
| 1 | `AaBnPLiUQISHK43ZVdjk` / c:S134 | `common/runtime/http_authorization_service.c` — nested deferred-worker control flow | Refactored into a focused helper. |
| 2 | `AaBnPLYKQISHK43ZVdjZ` / c:S995 | `tests/http_authorization_service_detached_worker_smoke.c` — flag parameter | Fixed by making the wait flag pointer const. |
| 3 | `AaBnPLYKQISHK43ZVdja` / c:S995 | Authorization test public runtime stub — parameter constness | Non-problem: production header ABI requires the non-const signature. |
| 4 | `AaBnPLYKQISHK43ZVdjb` / c:S995 | Authorization test public runtime stub — parameter constness | Non-problem: production header ABI requires the non-const signature. |
| 5 | `AaBnPLYKQISHK43ZVdjc` / c:S995 | Authorization test public runtime stub — parameter constness | Non-problem: production header ABI requires the non-const signature. |
| 6 | `AaBnPLhlQISHK43ZVdjd` / c:S3776 | Traefik send deadline | Refactored deadline/poll logic into bounded helpers. |
| 7 | `AaBnPLhlQISHK43ZVdje` / c:S134 | Traefik send path — nested control flow | Removed through the focused send/wait helper refactor. |
| 8 | `AaBnPLhlQISHK43ZVdjf` / c:S134 | Traefik send path — nested control flow | Removed through the same focused send/wait helper refactor. |
| 9 | `AaBnPLhlQISHK43ZVdjg` / c:S3776 | Traefik receive loop | Refactored to shared bounded wait/deadline helpers. |
| 10 | `AaBnPLhlQISHK43ZVdjh` / c:S995 | Traefik shutdown helper service parameter | Fixed by making the service parameter const. |
| 11 | `AaBnPLhlQISHK43ZVdji` / c:S3776 | Traefik serve orchestration | Split lifecycle setup, runtime configuration, handlers, and completion. |
| 12 | `AaBnPLhlQISHK43ZVdjj` / c:S3776 | Traefik CLI parsing | Split switch/value parsing and retained fail-closed validation. |

The successor commit, GitHub read-back, fresh Sonar analysis, complete
exact-head runtime workflow (including the hosted NGINX gate), and final PR
description/Change Record read-back remain pending at the time of this
entry. No merge, force-push, Framework/MRTS/Gitlink change, or test/workflow
weakening is authorized or claimed.
