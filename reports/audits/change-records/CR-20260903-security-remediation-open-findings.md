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

The implementation ports only the current-base-required security controls. Historical broad PRs are reference evidence, not merge sources. The Authorization port excludes unrelated duplicate-host validation and SIGPIPE strategy changes. The NGINX configuration reference is generated from a NGINX-only metadata override, so its English/German files and canonical configuration inventory remain source-backed rather than manually divergent. Hosted Lighttpd feedback then showed that, although the host harness already expects the safe serialized URI and `redacted=true`, the later Parent normalizer still compared it with the raw query-bearing wire URI. Both correlation stages now require the safe JSONL representation while raw curl-wire and correlated CRS-log evidence remain intact.

## Changed files

- Common runtime and event serialization: common/include/msconnector/event.h, common/src/event.c, common/src/integrity_event.c, and common/runtime/http_authorization_service.c.
- Connector implementation: connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c, connectors/nginx/src/ngx_http_modsecurity_log.c, and connectors/traefik/src/traefik_engine_service.c.
- Focused regressions: tests/event_json_query_redaction_test.c, tests/haproxy_spop_request_target_test.c, tests/test_haproxy_spop_request_target.py, tests/http_authorization_service_detached_worker_smoke.c, tests/test_http_authorization_service_worker_contract.py, tests/test_nginx_error_log_callback_contract.py, and tests/test_traefik_engine_service_contract.py.
- Lighttpd runtime-redaction regression: connectors/lighttpd/harness/run_patched_full_lifecycle.sh, ci/runtime/lifecycle/normalize-with-crs-no-mrts.py, connectors/lighttpd/tests/test_patched_host_contract.py, and tests/test_with_crs_no_mrts_runtime.py.
- Source-backed documentation/inventory: ci/checks/documentation/connector_config_reference.py, examples/nginx/configuration-reference.md, examples/nginx/configuration-reference.de.md, and reports/connector-configuration-inventory.json.
- Parent NGINX provenance alignment: ci/provisioning/components/prepare-runtime-components.py, ci/checks/evidence/check-runtime-producer-readiness.py, ci/runtime/broker/nginx_root_broker.py, ci/runtime/broker/protected_nginx_broker_caller.py, the NGINX hosted/full-smoke/broker workflows, and the paired compiler guide.
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
| Authorization timeout, detached-worker smoke, dynamic response-companion lifecycle fixture, ASan/UBSan, and TSan | Passed. The dynamic fixture proves the configured companion's pre-quiescence hold, failed-shutdown quarantine, one post-drain release, concurrent owner/worker single-winner release, and the no-companion deferred case. |
| Envoy module graph, Go test, and Go vet | Passed; module graph reports google.golang.org/grpc v1.83.1. |
| Traefik contracts/native-plugin/Authorization worker contracts | Passed: 47 tests. |
| Traefik C17 syntax and engine-service build/self-test/runtime/negative test | Passed with GCC and Clang syntax checks; normal, ASan/UBSan, and TSan engine-service runs passed. |
| Lighttpd JSONL-redaction host/normalizer contract | Passed: 62 focused tests and `bash -n`. The host harness requires `/?<redacted>` with `redacted=true`; the Parent normalizer now applies that same representation while binding the allow guard to its server-generated transaction ID. |
| Directive parity | Passed. |
| Full bilingual/link checks | Blocked solely by pre-existing missing Framework-submodule link targets; the task neither initializes nor modifies the Framework. |

## Security impact

The changes reduce request-target ambiguity, query-value disclosure, logging-configuration bypasses, local UDS resource exhaustion, and asynchronous use-after-free/double-release risk. Event JSONL redaction applies to newly emitted records; operators must treat historical JSONL and audit logs as potentially sensitive and restrict, rotate, or retain them according to local policy. No production service was contacted and no real credential, cookie, token, password, or personal data was used in tests or evidence.

## Runtime evidence

The local Traefik engine service was built and exercised over a private Unix
socket for normal, malformed-frame, and socket-ownership-negative controls.
It is not a Traefik host-runtime test. No production service was contacted.
The hosted Lighttpd CRS/no-MRTS runtime is the authoritative host validation
for the updated JSONL correlation contract. The diagnostic `fe518101` run
completed the lower host harness but the later Parent normalizer still compared
against the raw URI; its rerun is pending on the next immutable Draft-PR head.

## Checks not run and rationale

NGINX C17 host compilation/runtime is blocked by missing local NGINX
headers/source. Full bilingual and link checks are blocked only by existing
missing Framework-submodule targets; no Framework initialization or change is
authorized. Full HTTP/1.1, HTTP/2, and HTTP/3 host matrices require local host
fixtures that are not present.

## Known limitations

A configured Authorization companion has static lifecycle-contract coverage
and a dynamic late-quiescence fixture; the local fixture passed the complete
release/worker-drain matrix, but fresh exact-head hosted evidence is still
pending. The local Traefik service test does not exercise a Traefik host
process. These are evidence limits, not a claim that the safety controls are
disabled.

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
- The diagnostic Lighttpd hosted run showed a stale raw-URI comparison in the
  Parent normalizer after the host harness had already accepted the safe JSONL
  event. The scoped correction uses the same redacted representation at both
  stages, binds the allow guard to its server-generated transaction ID, and
  preserves raw wire and CRS evidence.
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

### Exact-head successor Sonar follow-up

SonarCloud check `100738129438` analysed successor
`fe518101c7c19ee29dba8be165f9356f5acfe78f` and failed solely because its
New-Code security rating was `D`. The twelve newly attributed reports below
were individually reviewed. The eight `c:S5443` reports are not reachable
public-directory operations: this parser-only fixture opens, binds, creates,
and writes no supplied path. Its inert `/tmp` literals are nevertheless
replaced with non-filesystem sentinel names so that the test cannot model an
unsafe directory use. The `c:S108` retry is clarified. The three `c:S995`
reports remain the only documented non-problems: their test stubs implement
public runtime ABI declarations whose mutable pointer types cannot be made
const without changing that ABI.

| # | Sonar key / rule | Location/issue | Disposition |
|---:|---|---|---|
| 1 | `AaBoE29gD03N4v8H0Ojv` / c:S5443 | Traefik CLI valid config literal, line 214 | Replaced inert `/tmp` spelling with `engine.conf`; parser coverage is unchanged. |
| 2 | `AaBoE29gD03N4v8H0Ojw` / c:S5443 | Traefik CLI valid socket literal, line 215 | Replaced inert `/tmp` spelling with `engine.sock`; no filesystem operation exists in this test. |
| 3 | `AaBoE29gD03N4v8H0Ojx` / c:S5443 | Traefik CLI missing-value config literal, line 218 | Replaced with the non-filesystem config sentinel. |
| 4 | `AaBoE29gD03N4v8H0Ojy` / c:S5443 | Traefik CLI missing-value socket literal, line 219 | Replaced with the non-filesystem socket sentinel. |
| 5 | `AaBoE29gD03N4v8H0Ojz` / c:S5443 | Traefik CLI zero-worker config literal, line 222 | Replaced with the non-filesystem config sentinel. |
| 6 | `AaBoE29gD03N4v8H0Oj0` / c:S5443 | Traefik CLI zero-worker socket literal, line 223 | Replaced with the non-filesystem socket sentinel. |
| 7 | `AaBoE29gD03N4v8H0Oj1` / c:S5443 | Traefik CLI overflow config literal, line 226 | Replaced with the non-filesystem config sentinel. |
| 8 | `AaBoE29gD03N4v8H0Oj2` / c:S5443 | Traefik CLI overflow socket literal, line 227 | Replaced with the non-filesystem socket sentinel. |
| 9 | `AaBoE29gD03N4v8H0Oju` / c:S108 | Traefik EINTR sleep retry, line 41 | Added the nested retry-purpose comment; behavior is unchanged. |
| 10 | `AaBnPLYKQISHK43ZVdja` / c:S995 | Authorization fixture runtime setter, line 99 | Non-problem: signature must match the public mutable-pointer ABI. |
| 11 | `AaBnPLYKQISHK43ZVdjb` / c:S995 | Authorization fixture profile setter, line 112 | Non-problem: signature must match the public mutable-pointer ABI. |
| 12 | `AaBnPLYKQISHK43ZVdjc` / c:S995 | Authorization fixture transaction begin, line 194 | Non-problem: signature must match the public mutable-pointer ABI. |

The resulting successor commit, GitHub read-back, fresh Sonar analysis,
complete exact-head runtime workflow (including the hosted NGINX gate), and
final PR-description/Change Record read-back remain pending at the time of
this entry. No merge, force-push, Framework/MRTS/Gitlink change, or
test/workflow weakening is authorized or claimed.

### Exact-head NGINX gate retry

The first successor-head hosted NGINX gate reached the real provisioning step
but exited with its framework-required status `77` before a host build. Its
workflow had invoked the aggregate runtime-component default, which requires
unrelated aggregate inputs. The scoped retry explicitly selects
`RUNTIME_COMPONENT_TARGET=nginx` and grants the existing runtime preparation
its required build/download capability flags; it neither broadens the target
nor weakens a control. The updated static gate contracts and `actionlint` pass.
A new immutable PR head and new hosted run are still required before claiming
NGINX compile or on/off runtime evidence.

### Exact-head NGINX provenance alignment

The scoped retry then reached the current Framework provenance guard and
correctly stopped with status `77` before any download or build: the immutable
Framework Gitlink `86451b45ae7bb7953baf9f81f2c2dad07395a808` canonically
selects `release-1.31.4`, `nginx-1.31.4.tar.gz`, and
`e6f20b644a17a643f059ae6467a1971fe2811587d025e071068753a1f1e3b3c3`, while
the Parent consumers still required the superseded `1.31.3` tuple. This
successor aligns only Parent provenance consumers, exact-head/full-smoke and
broker declarations, paired operator documentation, and their direct tests
to that already pinned Framework tuple. The strict tag/ref/asset/digest and
runtime-readback checks remain fail-closed; no Framework, MRTS, or Gitlink is
changed. Fresh hosted compile and on/off evidence remains required for the
new immutable head.

### Exact-head NGINX native-override isolation

The `fe518101` hosted retry passed its exact-head and pinned-provenance checks
but stopped before the host build with `missing_nginx_modsecurity_module`.
The provisioner had received an inherited native NGINX module-directory
override, which is forbidden when pinned provenance is required and did not
contain the managed module. The gate now clears only inherited native NGINX
artifact overrides for both provisioning and the subsequent runtime wrapper,
so the existing managed cache plan builds and validates the Parent NGINX
module. This neither accepts an absent module nor changes MRTS, Framework,
Gitlink, release tuple, or runtime provenance checks. The static gate contract
asserts every cleared override at both process boundaries; fresh exact-head
hosted compilation and on/off runtime evidence remains required.

### Exact-head NGINX failure-diagnostic boundary correction

The diagnostic-only successor `c5073a9ef3466c879cb5e352fe256ddeb8e88e75`
introduced a separate CI trust-boundary defect: after PR-controlled
provisioning code ran, its `if: failure()` helper trusted mutable
`GITHUB_ENV` roots and report-selected paths. It could disclose a
runner-readable file, load an unbounded report/log, or emit terminal/workflow
command text. Its NGINX and complete-runtime hosted runs were cancelled and
are not evidence for a later head.

The scoped Parent-only correction derives the sole diagnostic root from the
immutable `${{ runner.temp }}` context, invokes an empty-environment isolated
Python helper, and permits only fixed report and NGINX build-log descendants
opened by no-follow descriptor walks. It rejects symlinks, hardlinks,
replacement races, malformed/oversized inputs, and untrusted log selections;
it bounds and terminal-sanitizes emitted metadata/tail lines. The already
failed provisioning result remains authoritative. Forty-two focused dynamic
CI/workflow/helper tests, Python compilation, `actionlint`, and diff checks
pass locally. A new normal successor head, exact remote/PR read-back, and
fresh successor-only Sonar, NGINX on/off, and full CRS/no-MRTS workflow
evidence remain required; no earlier green run is reused.

### Exact-head NGINX diagnostic compatibility and Sonar correction

Exact-head hosted run `33800744562` for
`4350a8a77c61630025ba436cda12dfac6b3751e2` correctly kept the failed
provisioning result (`missing_nginx_modsecurity_module`) authoritative and
ran the bounded diagnostic step. That step reported `report_too_large`: the
normal complete generated component report is about 120,601 bytes and exceeds
the intentionally retained 64-KiB metadata cap, so the separately produced
fixed NGINX build-log tail was not reached.

The scoped successor candidate keeps that report cap and does not parse a
truncated report or trust its `build_log` value. Only for the explicit
`report_too_large` result it emits that status and then reads the independently
fixed `build/logs/runtime-components/nginx-build.log` path through the same
no-follow, identity-checked, bounded reader. The regression fixture places a
forged log path and canaries in the oversized report and proves that only the
fixed canonical tail is rendered. It retains symlink/hardlink/race rejection,
64-KiB tail bounds, line limits, and terminal/Actions-command sanitization.

The current SonarQube Cloud PR result has four open records: the new
`python:S3776` diagnostic-reader complexity report is a real maintainability
issue and the candidate splits the descriptor traversal, regular-file open,
and bounded-read responsibilities without changing their security invariants.
The three remaining `c:S995` Authorization fixture rows remain the
already-documented public-ABI non-problems above. No suppression, `NOSONAR`,
Quality-Gate change, or workflow/test weakening is used. Python compilation
and the 42 focused diagnostic/gate/CI-security tests pass locally; a new normal
head, exact remote read-back, and successor-only Sonar, NGINX on/off, and full
CRS/no-MRTS evidence remain required.

### Exact-head NGINX non-H3 QUIC TLS handoff

Exact-head hosted run `33803351249` for
`79156cb550eebf76c52add7a2059379ee2d8df90` reached the pinned NGINX build
boundary, but correctly stopped before configure with `BLOCKED:
NGINX_QUIC_TLS_VERSION override is not permitted`. The bounded diagnostic
fallback safely exposed that primary blocker; the later
`missing_nginx_modsecurity_module` mapping was secondary because no module
build had started. The complete CRS/no-MRTS run `33803351191` passed its five
non-NGINX connector jobs for the same head, but cannot validate a successor.

The Parent source correction does not relax the Framework provenance guard or
change its QUIC TLS tuple. For H1/H1-H2, profile-specific `not_used`/empty
facts are no longer forwarded as environment pin overrides, so the canonical
values loaded from Framework `common.sh` survive the next guarded source
boundary. H3 continues to replace those fields with its resolved reviewed
tuple. Thus an empty or noncanonical inherited pin remains fail-closed at the
unchanged Framework boundary.

Focused dynamic tests now prove canonical H1/H1-H2 child-environment
preservation, H3 replacement with the reviewed tuple, and the actual mocked
NGINX preparation path. Python compilation, 78 Parent component tests (five
pre-existing Framework-head skips), all 45 NGINX cache-contract tests, the 64
bilingual/NGINX-gate/CI-security/diagnostic tests, `actionlint`, and `git diff
--check` pass locally. An independent post-patch security review passed and
found no bypass or regression. A new normal exact-head successor remains
required before claiming supported-header compile or
`modsecurity_use_error_log` on/off runtime evidence; exact remote read-back
and successor-only Sonar, NGINX on/off, and full CRS/no-MRTS evidence also
remain required.
