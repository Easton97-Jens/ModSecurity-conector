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
| Delivery status | Draft PR [#354](https://github.com/Easton97-Jens/ModSecurity-conector/pull/354) is open and unmerged, and remains Draft. This Change Record is part of its own documentation successor and does not promote any predecessor result. After the successor push, its exact SHA and fresh result readback are recorded in PR metadata and retained delivery evidence. The Parent exact-five workflow implementation now exists, but no fresh exact-successor five-cell aggregate artifact or result has been observed and read back. FND-CROSS-0004 therefore remains an independent, unaccepted `P1` release blocker pending its existing Framework acceptance and hosted-evidence criteria; no Draft transition or merge is authorized. |

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
- Parent With-CRS/no-MRTS exact-five evidence contract: ci/runtime/lifecycle/with-crs-no-mrts-profile.py, ci/runtime/lifecycle/aggregate-five-connector-with-crs-no-mrts.py, ci/runtime/lifecycle/normalize-with-crs-no-mrts.py, ci/runtime/lifecycle/prepare-with-crs-no-mrts-upload.py, ci/runtime/lifecycle/project-haproxy-runtime-evidence.py, and .github/workflows/test-connectors-with-crs-no-mrts.yml.
- Apache profile evidence and focused regressions: connectors/apache/harness/run_apache_smoke.sh, tests/test_with_crs_no_mrts_profile.py, tests/test_apache_with_crs_profile_evidence_contract.py, tests/test_haproxy_evidence_projection.py, tests/test_haproxy_evidence_workflow_contract.py, tests/test_with_crs_no_mrts_runtime.py, and tests/test_ci_security_workflows.py.
- Profile documentation: docs/reference/with-crs-no-mrts-profile-contract.md and docs/reference/with-crs-no-mrts-profile-contract.de.md.
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
| Exact f38 NGINX supported-source provision/compile | Passed: the pinned `nginx-1.31.4` archive was SHA-256 verified and produced the managed `ngx_http_modsecurity_module.so`; the task-local `--no-same-owner` setting only avoids unsupported archive-owner restoration. It is not an on/off runtime result. |
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

### Exact-head NGINX make-log evidence handoff

Exact-head hosted run `33807403800` for
`810b0df3c1a83af2cedc6a2b3a84a4fe60df2c5b` passed exact-head and pinned
provenance checks and reached the real `make -j4` step. The build failed, but
the prior bounded outer diagnostic retained only the command-level failure and
not the compiler/linker line needed to classify it. That run does not claim a
successful compile or `modsecurity_use_error_log` on/off runtime evidence.

The scoped Parent-only follow-up keeps the failed build authoritative and,
before transactional staging cleanup, derives only the fixed managed path
`build/logs/nginx/nginx-make.log`. It requires the current `connector:nginx`
marker, cache key, cache root, and exact `staging_root/build` identity; it does
not consume a report-selected path or mutable environment root. The fixed
descendant is opened through no-follow descriptors with directory/file
identity checks. Path escape, symlink, hardlink, and replacement-race inputs
are rejected; oversized content is bounded to a 64-KiB tail; and the retained
representation is terminal- and Actions-command-sanitized before it is
appended to the existing fixed outer log. The longer staged line prefix is
included in the 512-character line budget. A staging-root resolution error is
fail-soft and cannot replace the primary failed-build result. Framework, MRTS,
Gitlink, provenance, test, and workflow controls are unchanged.

Focused local validation covers managed-identity mismatch, a missing inner log,
path escape, symlink/hardlink rejection, a replacement race, bounded tails,
the complete staged-line limit, terminal/Actions-command sanitization, and
symlink-loop resolution.
It also proves that the append leaves the primary failed-build exit code,
failed status, and blocker mapping authoritative. Python compilation, 81 Parent component tests with five pre-existing
Framework-head skips, 11 NGINX-diagnostic tests, `git diff --check`, and an
independent post-patch security review pass. A fresh normal successor head and
exact-head hosted rerun remain required before supported-header compilation or
isolated `modsecurity_use_error_log` on/off runtime evidence is claimed.

### NGINX profile-registry materialization repair

Exact-head NGINX run `33813265768` on
`896a7dd94421bd47d1078cf4360c463be3fa1a14` verified the bounded make-log
handoff by retaining the earliest compiler error. It also exposed a distinct,
fail-closed Parent build defect: the materialized NGINX tree omitted the
canonical `connectors/profile_registry.h` input and both dynamic/static source
lists omitted `connectors/profile_registry.c`. That separate issue is tracked
as `FND-PARENT-1030`; `FND-PARENT-1028` is verified only for its diagnostic
handoff, not as NGINX host-build proof.

The local repair binds both registry files into the NGINX cache-source hash,
stages them beneath the managed build root, supplies only that staged root to
the child environment, and declares the source, header, and include root in
both NGINX configuration branches. Staging uses descriptor-relative
`O_NOFOLLOW` directory/file opens, regular single-link source checks before
and after open, exact-size copying, descriptor-relative temporary files, and
atomic replacement. This prevents an arbitrary inherited registry root,
source replacement, hardlink input, and destination symlink/replacement from
silently affecting the managed build. The direct-checkout fallback remains
explicitly documented and does not apply to a copied adapter tree.

Fresh local validation passed 88 preparation cases with five pre-existing
Framework-head skips, 45 cache-contract cases, 7 cache-identity cases, and 51
diagnostics/compiler-guide/bilingual cases. It includes deterministic
source-replacement, source-hardlink, destination-directory symlink/replacement
and destination-file-symlink-canary controls. The NGINX source/C17 wiring
contract, shell syntax checks, Python compilation, and diff check passed. A
capped local `make check-nginx-c17` attempt correctly returned the native
blocked status because supported NGINX headers/source are unavailable here;
that is not host-compile evidence. The next normal immutable head must be read
back from GitHub and run fresh Sonar, exact-head NGINX build plus both
`modsecurity_use_error_log` cells, and the complete CRS/no-MRTS runtime
workflow. No earlier run is reused, and no merge, force-push,
Framework/MRTS/Gitlink, workflow, test, or quality-gate change is made.

### NGINX registry Sonar follow-up and hosted runtime limitation

The exact-head SonarCloud result for
`ac78937ace73fbc27a7c8a9b9ab0297c1d94de16` kept the Quality Gate `OK`, but
the PR inventory contained two genuine new issues in the registry staging
repair: `python:S3776` on descriptor-copy cognitive complexity and
`python:S107` on the fourteen-argument NGINX build-environment helper. The
three remaining `c:S995` Authorization fixture rows remain the documented
public-ABI non-problems. No issue transition, `NOSONAR`, rule exclusion, or
Quality-Gate change is used.

The follow-up splits the descriptor copy into bounded allocation, read/write,
sync/identity, publication, and cleanup helpers while retaining no-follow
opens, single-link source checks, exact-size copying, atomic replacement, and
descriptor-relative cleanup. It replaces the large internal argument list with
one immutable typed input boundary and preserves the hostile inherited
`MSCONNECTOR_PROFILE_REGISTRY_ROOT` override. Independent review found one
close-failure ownership path during that split; the descriptor is now retained
until a successful close, and a negative regression verifies temporary-file
cleanup on that failure. The focused preparation suite passes 89 cases with
five pre-existing Framework-head skips; the broader cache/diagnostics suite,
Python compilation, and diff check pass. A local single-file Sonar analyzer is
blocked by the host CPU's incompatibility with its signed analyzer binary, so
the next fresh SonarCloud result is the authoritative verification.

Hosted NGINX run `33818517134` on `ac78937` successfully provisioned pinned
NGINX and completed the connector build step, but the isolated on/off harness
correctly stopped with its intentional status `77`: an unprivileged GitHub
runner cannot establish the required distinct verified worker identity. The
harness has no safe same-identity bypass, and the protected root broker does
not execute these cells. Therefore this result is compile evidence only, not
`modsecurity_use_error_log` runtime evidence. A task-owned root-capable local
provision/run is the remaining authorized alternative to investigate after the
next normal successor head; no workflow change, merge, force-push,
Framework/MRTS/Gitlink change, or test/control weakening is made.

### Exact-head f38 validation follow-up

Successor head `f38f239a8d0e73408a049583f5fcdb01d8b7be9b` was pushed
normally and read back from GitHub. The complete runtime workflow `33820766693`
passed all five connector jobs at this exact head. NGINX workflow `33820766701`
also passed exact checkout, pinned provenance, and runtime-component
provisioning.

Its isolated `modsecurity_use_error_log` on/off cells stopped with the
intentional status `77` because the unprivileged hosted runner cannot establish
the required distinct verified worker identity. No same-identity bypass or
workflow weakening was used, so this workflow is not on/off runtime evidence.
A separate local pinned-source retry first confirmed that the release archive
is valid but cannot restore uid `502`/gid `50` in this capability-restricted
root namespace. With only the safe `--no-same-owner` host-compatibility setting,
the real provisioner produced the managed NGINX connector module. The local
runtime still cannot supply the required evidence: `runuser` cannot set groups,
and the existing Framework containment control correctly rejects its
non-contained materialization geometry before worker startup. Neither outcome
justifies relaxing the identity or containment controls.

The exact-head SonarCloud result passed the Quality Gate. The two newly
surfaced registry-staging issues (`python:S3776` and `python:S107`) were fixed
in f38. The three remaining `c:S995` Authorization fixture findings are
individually documented public-ABI non-problems. No `NOSONAR`, exclusion, issue
transition, or Quality-Gate weakening was used.

### 2026-09-05 current-base reconciliation

This PR was reconciled against the exact current `origin/master` comparison
revision `b779167ff979aa73cdd9321a829f9c693d943760` by a normal merge into the
existing PR branch. PR #355 remains unmerged: its requested exact-head
integration is blocked by the independent, still-open FND-PARENT-1038. The
external codex-security dependency blocker FND-PARENT-1036 remains unchanged
and is not reported as fixed.

The five requested boundary areas were retained or minimally reconciled with
the current base: HAProxy lossless path/uri boundary handling, Common JSONL
query redaction with explicit truncation and integrity flags, NGINX effective
`modsecurity_use_error_log` callback handling, Traefik deadline/cap/FD
ownership controls, and Authorization companion quiescence with exactly-once
release. Focused local evidence currently passes for the linked JSONL test,
the executable HAProxy parser test and C17 check, the Authorization native
companion smoke test and seven worker-contract tests, and the targeted Traefik
worker/FD and service-contract tests. The complete 37-test Traefik native
local-plugin suite also passed when run with a private short AF_UNIX temporary
root. These are fresh working-tree results, not claims about a future pushed
head.

The local NGINX native check remains blocked because supported NGINX
headers/source are unavailable. The named
`NGINX-Use-Error-Log-Exact-Head-Hosted-Gate` is still required for
supported-source compilation and isolated
`modsecurity_use_error_log` on/off runtime evidence; no exit-77 result is
treated as success and no host runtime evidence is claimed here.

The additional `check-nginx-common-adoption` control is currently red on this
head only because it is already red on the exact comparison base, with the two
known FND-PARENT-1010 assertions. The relevant current-base NGINX paths are
unchanged here except for the native log callback; the separate checker-only
successor is Draft PR #357. This PR neither absorbs that independent repair
nor weakens the check, and its fresh hosted result must report the baseline
failure as such.

`check-haproxy-common-adoption` likewise reproduces a pre-existing
current-base assertion (`request mapper prefers Host header and keeps server_ip
fallback`) on both revisions. It conflicts with the current mapper's validated
Host assignment and separate server-endpoint field, not with this PR's target
parser change. FND-PARENT-1041 tracks the checker-only discrepancy for a
separate narrow remediation; no fallback, runtime source, or check was changed
here.

### 2026-09-05 mutable-runtime fixture remediation (pre-push)

At the starting PR head `1208ca9b5bfbf8851ec4d9fe0772cfa3313092d8`, the two
active SonarCloud `c:S995` records were
`AaBnPLYKQISHK43ZVdja` (event-integration setter) and
`AaBnPLYKQISHK43ZVdjb` (transaction-profile setter). Production declarations
and definitions intentionally use mutable `msconnector_runtime *`: the former
copies the integration mode into runtime storage and the latter stores the
selected profile. Changing that ABI to `const` would be incorrect.

The detached-worker fixture now models those two effects in its own valid
runtime object under its existing lock: it copies the accepted integration
mode into bounded fixture storage and records the accepted profile pointer.
The fixture asserts the state is unconfigured before service startup and
configured through the service's real setter calls. The response-companion
fixture resets this same test runtime object, rather than obsolete global
flags. This is a behavioral fixture correction, not a cast, dummy write,
suppression, or production-ABI change; all Companion quiescence, failed-shutdown
quarantine, exactly-once release, concurrent claim, and no-companion deferred
release controls remain intact.

The C17 timeout/companion lifecycle script passed both normally and with
AddressSanitizer plus UndefinedBehaviorSanitizer. The worker and security
contract suites passed 14 tests with 14 passes, zero failures/errors/skips.
A fresh SonarCloud analysis of the normally pushed successor is still required
to demonstrate that both active keys are absent; no local result is presented
as SonarCloud evidence.

The requested equal-environment adoption comparison was rerun in clean
worktrees with `rtk 0.47.0` and `Python 3.14.7`:

| Finding | Command in each clean worktree | Base `b779167…` | PR start `1208ca9…` | Cause | PR regression? |
| --- | --- | --- | --- | --- | --- |
| FND-PARENT-1010 | `python3 -B ci/checks/connectors/nginx/check-nginx-common-adoption.py` | exit 1; same two assertions | exit 1; same two assertions | stale non-fatal-mapper and explicit-length sink assumptions | No |
| FND-PARENT-1041 | `python3 -B ci/checks/connectors/haproxy/check-haproxy-common-adoption.py` | exit 1; same Host/server-IP assertion | exit 1; same Host/server-IP assertion | stale Host-preference/server-endpoint checker assumption | No |

Both worktrees were clean before and after. These shared base/checker failures
remain separate remediation work; this PR neither changes their checker nor
claims a green result for them.

### 2026-09-05 native NGINX Phase-4 event-sink remediation (pre-push)

Starting from Draft PR #354 head
`bf4666883463e066aad82db6ea27716b5e9d13e7`, the native
`modsecurity_phase4_log` setter rejected every configured target before it
could transfer a descriptor to the JSONL callbacks.  A valid secure target
could therefore never produce native NGINX JSONL evidence.

The scoped fix opens the configured target only through
`msconnector_open_private_event_file`, installs one NGINX pool cleanup before
descriptor ownership transfers, and writes through that connector-owned file
descriptor.  The descriptor is deliberately not registered in
`cycle->open_files`: generic NGINX `USR1` reopening would otherwise reopen the
pathname outside Common's no-follow, regular-file, trusted-parent/owner, and
`0600` contract.  `USR1` therefore retains the validated descriptor; a secure
configuration reload parses and opens a new descriptor while old workers
drain.  Inherited locations borrow the parent descriptor without a second
cleanup, explicitly configured children own their own descriptor, and cleanup
invalidates the descriptor before closing it.

The accompanying Functional-A gate creates separate `on` and `off` cells from
the same hashed binary/module/rule set.  It requires a real root master and a
distinct non-root worker, tests valid targets, unconfigured logging, existing
mode repair, inheritance/override, five unsafe target forms, redacted JSONL,
raw-URI/WAF continuity, callback separation, `USR1` retention, failed unsafe
reload preservation, secure reload overlap/drain, and shutdown FD/process
cleanup.  The gate is a GitHub-hosted native integration test, not an
independent hostile-candidate attestation. It deliberately exercises
candidate-controlled code only for Functional A on a disposable GitHub-hosted
VM; it is neither source-independent nor an adversarial trust boundary and
cannot validate Protected B or FND-PARENT-1038.

Local verification on this candidate passed the 43 focused NGINX/Common/
launcher/reference Python tests, shell syntax checks, Python compilation,
`actionlint`, generated-reference checks, `git diff --check`, and supported
source C17/C23/C2y compilation.  `check-nginx-common-adoption` still reports
only the two documented current-base FND-PARENT-1010 assertions; no checker,
test, workflow, or Quality-Gate control was weakened.  A local Functional-A
run is not valid in this container: it is already root, cannot establish the
required sudo/non-root-worker chain, has no initialized task-worktree
Framework, and has no fresh current-head artifacts.  Exact-head GitHub-hosted
build/runtime evidence, SonarCloud analysis, and the required PR checks remain
`not_run` until the normal successor commit is pushed and read back.  Draft PR
#354 remains open and unmerged; FND-PARENT-1036 remains
`blocked_external_dependency`.

### 2026-09-05 hosted Functional-A and Sonar follow-up (successor pending)

The normal push of `dcb499b04239f55c6faf7a3abf709b6cc9622fb6` was read back
as the Draft PR #354 head.  Its five fresh CRS/no-MRTS runtime cells passed,
but those predecessor results are not evidence for a successor.  The fresh
hosted NGINX workflow completed the sudo/root-versus-worker preflight and
unprivileged provisioning, then failed closed with exit `77`: its launcher
correctly rejected the generic Libtool `libmodsecurity.so` alias because that
alias is a symbolic link.  This is a failed Functional-A runtime result, not a
passing on/off result.

The approved component provisioner intentionally preserves that generic alias
for ordinary consumers and separately publishes
`libmodsecurity.so.3` as the protected regular runtime artifact.  The narrow
successor repair binds Functional A only to that existing regular file: the
root launcher validates it without symlink traversal, passes its exact bounded
path, and the exact-head gate hashes that file before/after both on/off cells.
The generic smoke harness retains its existing `libmodsecurity.so` default
outside Functional A.  A Functional-A invocation rejects a missing, substituted
or symlinked runtime artifact rather than falling back to the generic alias.
No provisioner, Framework, MRTS, dependency, policy, workflow permission, or
attestation boundary is changed.

SonarCloud readback for the predecessor reported Quality Gate `ERROR` and six
active PR issues: reader complexity and file-open hardening, two missing shell
`case` defaults, and two assertion-expression checks.  The successor splits
the bounded parser, opens only the fixed
`runtime_root/conf/case.env` by descriptor-relative no-follow operations, and
rejects unsafe directories, substitutions, special files, hard links,
oversized content, and changed file identity.  The shell cases now fail
closed, and the tests use one evaluated expression per exception assertion.
No issue is ignored, suppressed, or risk-accepted.  Focused reader,
launcher, exact-gate, and phase-runner tests passed locally; the three
phase-runner skips are the existing absent/mismatched Framework-pin condition.

The successor still requires a normal push, GitHub readback, fresh hosted
on/off runtime, fresh CRS/no-MRTS checks, and a fresh SonarCloud zero-active-
issue/Quality-Gate result.  Functional A remains a GitHub-hosted native
integration test only, not Protected B or a resolution of FND-PARENT-1038;
FND-PARENT-1036 remains `blocked_external_dependency`.

### 2026-09-05 second hosted follow-up (successor candidate pending)

For exact Draft PR #354 head `d2abf5dc9fc287d5e8d233ec725c23ab1f14a97a`,
the fresh hosted NGINX run `33989150637` passed exact-head checkout, the
sudo/root-versus-worker preflight, isolated-path initialization, and
unprivileged component provisioning. It then failed closed with exit `77`
before either native on/off cell: the deliberately scrubbed `/usr/bin/env -i`
allowlist omitted both already preflighted
`NGINX_FUNCTIONAL_WORKER_USER` and `NGINX_FUNCTIONAL_WORKER_GROUP`, so the
root launcher received an empty worker identity and rejected it. This is a
workflow allowlist omission, not a relaxation of the worker check and not a
successful Functional-A result.

The same exact-head SonarCloud analysis cleared the preceding six issues but
reported two new active `pythonsecurity:S8707` flows from the reader's
path-valued `--runtime-root` CLI option into `os.open`; the Quality Gate
therefore remained `ERROR` (`new_security_rating=3`, threshold `1`). The
candidate remediation removes all path-valued reader CLI/environment input.
The Functional-A harness opens its already path-authorized, freshly private
runtime root only as inherited descriptor `3`; the reader duplicates and
validates that capability, then opens only fixed `conf/case.env` components
with no-follow checks. Owner/mode/type/link-count/size and mutation checks
remain enforced. Header, body, and audit paths from the generated record are
also compared against the already constructed trusted paths before later
root-side consumers use them; they cannot replace those paths.

The candidate also forwards both bounded worker names explicitly through the
existing clean environment. The root launcher continues to validate and map
them to the NGINX worker identity; no ambient environment, broad sudo chain,
or identity bypass is introduced. Local candidate validation passed 46
focused NGINX/Common/event/lifecycle/reader/launcher/reference tests, the
Phase-4 runner's three applicable tests (three Framework-pin-dependent tests
remain skipped), Python compilation, shell syntax, `actionlint`, C-standard
wiring, and whitespace checks. The local Sonar Vortex precheck is unavailable
for this organization and is not treated as a SonarCloud result. The existing
two FND-PARENT-1010 baseline assertions still make
`check-nginx-common-adoption` fail; they were neither changed nor masked.

This candidate is not yet pushed. A normal successor push, GitHub head
readback, fresh hosted on/off runtime, all five CRS/no-MRTS runs, and a fresh
SonarCloud zero-active-issue/Quality-Gate result remain required. Functional
A remains an integration test only, FND-PARENT-1038 is unchanged and open,
and FND-PARENT-1036 remains `blocked_external_dependency`.

### 2026-09-05 third hosted follow-up (runuser-capability successor pending)

For exact Draft PR #354 head
`1f267564b35086eda8fed80895eb0cb7f6fb35ab`, fresh SonarCloud readback reports
Quality Gate `OK`, zero active `OPEN`/`CONFIRMED` PR issues, and zero
`TO_REVIEW` hotspots.  The fresh local exact-head C17 compilation also passed.
These results do not turn the native runtime into a passing result by
themselves.

Hosted workflow `33990967266` checked out that exact head, completed the
sudo/root-versus-worker preflight, initialized the isolated root, and completed
the unprivileged pinned provisioning.  Its first `on` cell then correctly
failed closed with exit `77`: the clean root environment intentionally has
`PATH=/usr/bin:/bin`, the preflight already uses the verified absolute
`/usr/sbin/runuser`, but the harness later looked up and invoked `runuser`
through `PATH`.  This deterministic mismatch is neither a runner flake nor a
successful on/off result.

The narrow successor candidate removes that path lookup.  Its worker identity
and access checks select only executable fixed system capabilities
`/usr/sbin/runuser` or `/usr/bin/runuser`; they do not widen `PATH`, accept a
caller-selected helper path, or relax the distinct-worker requirement.  The
direct path-authority suite passed 11 tests, the relevant NGINX security,
launcher, exact-gate, and lifecycle suites passed 26 tests, shell syntax and
whitespace checks passed.  The successor is not yet pushed, so these local
results are not a hosted success claim.

The first five-cell CRS/no-MRTS matrix for `1f267...` passed Apache, Envoy,
Traefik, and Lighttpd.  HAProxy stopped before product execution because the
GitHub-hosted component provisioner received `HTTP Error 403: rate limit
exceeded` while obtaining expat; exact-head checkout, runtime preflight, CRS
preparation, and cleanup passed.  A normal failed-job-only retry on the same
head is in progress.  Regardless of its result, all final runtime evidence
must be rerun on the next normal successor head.

Functional A remains a GitHub-hosted native integration test only, not
Protected B and not a resolution of FND-PARENT-1038.  FND-PARENT-1036 remains
`blocked_external_dependency`; PR #354 remains Draft, open, and unmerged.

### 2026-09-05 fourth hosted follow-up (contained-materialization successor pending)

For exact Draft PR #354 head
`f29fe20fd556b75b96a5fbdcef140bbeb66f5a61`, fresh SonarCloud readback reports
Quality Gate `OK`, zero active `OPEN`/`CONFIRMED` PR issues, zero `TO_REVIEW`
hotspots, and a successful exact-commit SonarCloud check.  The fresh five-cell
CRS/no-MRTS workflow `33992317099` also passed Apache, Envoy, HAProxy,
Lighttpd, and Traefik.  These results do not make the separate native NGINX
runtime successful by themselves.

Hosted workflow `33992317013` checked out that exact head, completed the
sudo/root-versus-worker preflight, isolated-path initialization, and pinned
unprivileged provisioning.  Its first `on` cell then failed closed with exit
`78` before NGINX configuration parsing or worker startup: the exact gate set
`BUILD_ROOT` to a `case_root/build` child while its generated runtime, log,
and audit paths were sibling children of the fresh private `case_root`.
Framework `case_cli materialize` correctly rejected those out-of-root targets
through its unchanged containment guard.  No out-of-root write occurred, the
`off` cell did not run, and there is no f29 native callback, JSONL, WAF, or
allow-control success claim.

The narrow Parent successor candidate binds both `VERIFIED_BUILD_ROOT` and
`BUILD_ROOT` to the already fresh private per-case root, so all generated
runtime, log, audit, harness, and result paths remain descendants of the same
trusted root.  It neither changes Framework code nor weakens path containment,
the outer path validator, the scrubbed root environment, or the distinct
worker requirement.  A dynamic regression proves that the Framework
materializer accepts the common-root layout and continues to reject the former
sibling layout; it also checks generated header/body/audit references.  The
full focused NGINX/Common/event/lifecycle/reader/launcher/path-authority/
reference set passed 60 tests, together with shell syntax, Python compilation,
`actionlint`, C-standard wiring, and whitespace checks.  These are local
candidate results, not a hosted success claim.

The candidate still requires a normal successor commit and push, GitHub head
readback, fresh C17 and available-sanitizer assessment, fresh SonarCloud,
required checks, all five CRS/no-MRTS runtimes, and a new GitHub-hosted native
on/off/JSONL/WAF/allow run on that new exact head.  Functional A remains a
GitHub-hosted native integration test only, not Protected B or a resolution of
FND-PARENT-1038; FND-PARENT-1036 remains `blocked_external_dependency`, and
PR #354 remains Draft, open, and unmerged.

### 2026-09-05 fifth hosted follow-up (worker-traversable successor pending)

Before committing the contained-materialization candidate, an independent
source review identified another deterministic pre-NGINX blocker. Keeping the
provisioning `RUN_ROOT` and each Functional-A ancestor private at `0700` would
correctly prevent the distinct NGINX worker from traversing the path to its
required docroot, worker-state, and server-log leaves. Making `RUN_ROOT`
traversable would be unsafe because it contains the unprivileged build,
provisioning, and evidence paths. This is additional current evidence for the
existing lifecycle finding `FND-PARENT-0078`, which remains `in_progress`; it
is neither a new finding nor a closure of any existing finding.

The narrow Parent successor keeps `RUN_ROOT` at `0700`. The workflow instead
creates one fresh, fixed-name Functional-A parent as a direct sibling under the
GitHub temporary root at exact mode `0711`. Before the scrubbed root handoff,
the launcher requires an absolute, symlink-free designated sibling owned by
the runner, exact non-enumerable `0711` mode, and a worker-traversable ancestor
chain. The root-only exact gate then creates only the Functional-A, mode, and
case ancestors as newly root-owned `0711` directories. Runtime configuration,
rules, logs, audit/evidence, and other private leaves keep their existing
private contract; the harness retains its existing narrow worker-readable
docroot/state/server-log controls. Framework materialization remains under the
common case root and its containment guard is unchanged.

The dedicated parent is a runner-owned bootstrap for the explicitly bounded
Functional-A GitHub-hosted integration test. It is not a hostile-runner or
hostile-VM-root attestation boundary and is not represented as Protected B.
`FND-PARENT-1038` remains fixed but unverified and not closed, unchanged by
this candidate; `FND-PARENT-1036` remains `blocked_external_dependency`. No
Framework, MRTS, Gitlink, dependency,
permission-policy, test, Sonar, or generic path-authority control is changed.

Local candidate validation passed 63 focused NGINX/Common/event/lifecycle/
reader/launcher/path-authority/reference tests, including a dynamic Framework
materialization control against the read-only exact Framework gitlink checkout,
the new mode/layout regression, shell syntax for both NGINX harness scripts,
Python compilation, `actionlint`, C-standard wiring, and whitespace checks.
The local container cannot execute the real distinct-worker `runuser` control
because group changes are denied, so no local worker-runtime success is
claimed. `check-nginx-common-adoption` remains red only for the two unchanged
tracked FND-PARENT-1010 baseline assertions. This candidate is not yet pushed;
a normal successor push and all fresh exact-head hosted, CRS/no-MRTS,
required-check, and Sonar evidence remain mandatory.

### 2026-09-05 sixth hosted follow-up (ShellCheck successor pending)

The worker-traversal commit
`25a3eea84185ebcb1d121e84d267e53610cf4118` was pushed normally to the
existing Draft PR #354 branch and read back from both Git and GitHub.  Its
exact-head Security workflow lint then failed with exit `1` at
`.github/workflows/test-nginx-exact-head.yml`: ShellCheck `SC2015` correctly
flagged the fresh-parent test written as an `&&`/`||` chain.  This is a real
workflow-quality defect, not a reason to disable ShellCheck, actionlint, or
the occupied-path rejection.  The exact-head hosted NGINX and CRS/no-MRTS runs
had started, but are not used as success evidence because the next normal
successor will supersede that head.  The initial exact-head Sonar success is
likewise predecessor-only after that successor push.

The narrow successor rewrites only that condition as an explicit `if`:
an existing or symlinked Functional-A parent still fails the step before any
privileged handoff, while a fresh parent continues unchanged.  Its contract
test now rejects reintroduction of the ambiguous chain.  Thirteen focused
launcher/layout/gate tests, local `actionlint`, and whitespace checks pass.
The full relevant regression set, C17 build, Sonar, required checks, all five
CRS/no-MRTS cells, and GitHub-hosted native On/Off/JSONL/WAF/allow proof must
be rerun on the new exact head.

This successor is not yet pushed.  Functional A remains a GitHub-hosted native
integration test only, not Protected B or hostile-runner/VM-root attestation.
FND-PARENT-1038 remains fixed but unverified and not closed, unchanged by this
candidate; FND-PARENT-1036 remains `blocked_external_dependency`; PR #354
remains Draft, open, and unmerged.

### 2026-09-05 seventh hosted follow-up (Phase-4 request metadata and `/tmp` traversal successor pending)

Exact Draft PR #354 predecessor
`a4666abf3b6585c80abc68f84ab9ebef10f054aa` reached successful provisioning in
GitHub-hosted Functional-A run `33996313979`, then failed closed with exit
`77`: `NGINX_FUNCTIONAL_A_PARENT_ROOT has a worker-non-traversable ancestor`.
The bounded log did not identify that ancestor. NGINX never started, so this
run proves neither native callback behavior nor Phase-4 JSONL, WAF, or allow
behavior and cannot be reused for the successor.

The narrow traversal successor does not widen `RUNNER_TEMP`. It verifies the
root-owned sticky `/tmp` contract, creates an atomic runner-owned job root
below it, keeps the provisioning `RUN_ROOT` private at `0700`, and exposes only
the fixed Functional-A sibling at `0711`. The launcher binds exact direct
topology, ownership, modes, and no-symlink components; the workflow uses the
real configured `runuser` identity to prove worker traversal of the job and
Functional-A ancestors while proving that `RUN_ROOT` remains non-traversable.
This is a GitHub-hosted Functional-A integration test only, not hostile-runner
or hostile-VM-root attestation and not Protected B.

Independent source-to-sink review also found a distinct Phase-4 defect:
`ngx_http_modsecurity_phase4_log_event` initialized its event but omitted
request method/URI, causing the Common serializer to receive an empty URI. The
narrow NGINX C repair uses the existing pool-owned
`ngx_http_modsecurity_event_request_metadata(r)` helper and assigns method/URI
before Common serialization. Common remains the sole owner of query redaction,
truncation signaling, and the matching integrity view; raw `r->unparsed_uri`
continues independently through the NGINX/WAF request path. No connector-
specific redactor or Common-runtime refactor was added.

The predecessor source contract was observed failing before the assignment and
passes for the current candidate. Current local evidence includes 28 focused
native/launcher/topology/exact-gate tests, a C17 compile with warnings as
errors, the direct Common long-URI/query-redaction/integrity control, shell
syntax, `actionlint`, C-standard wiring, and whitespace checks. These are
source/contract evidence only: the required fresh exact-successor hosted
ON/OFF/JSONL/WAF/allow proof, all five CRS/no-MRTS cells, required checks, and
SonarCloud must run after a normal successor push. Exit `77` remains failed
evidence.

`FND-PARENT-1046` records the separately remediable Phase-4 request-metadata
boundary and remains `in_progress`; `FND-PARENT-0078` retains the traversal
boundary and likewise remains `in_progress`. `FND-PARENT-1038` is unchanged
and not closed; `FND-PARENT-1036` remains `blocked_external_dependency`. PR
#354 remains Draft, open, and unmerged.

### 2026-09-05 eighth hosted follow-up (ShellCheck guard successor pending)

The normal successor `d88b47abb598eb410ebddca7d3016ca526d06447` was pushed
to the existing Draft PR #354 branch and read back from Git and GitHub. Its
exact-head Security workflow lint run `33999439753` then failed at the two new
Functional-A `/tmp` and fresh-job-root guards with ShellCheck `SC2015`. The
guards fail closed, but their `A && B || { ...; }` form is ambiguous and must
not remain in a passing workflow.

The bounded follow-up rewrites only those two conditions as explicit `if`
guards with the same truth table: a missing/non-directory or symbolic-link
`/tmp`/job root is rejected before any privileged handoff. The focused contract
test rejects reintroduction of either ambiguous form, and local
`actionlint -shellcheck=/usr/bin/shellcheck` passes. No ownership, mode,
traversal, Common serialization, descriptor-lifecycle, or root-command
boundary is weakened.

This successor is not yet pushed. The in-progress `d88b47ab...` Hosted
Functional-A and five-cell CRS/no-MRTS runs, plus its remaining checks and
Sonar analysis, are predecessor-only after the next normal push. The next
exact head still requires fresh native ON/OFF/JSONL/WAF/allow evidence,
worker/reload/shutdown lifecycle evidence, relevant checks, all five runtime
cells, and SonarCloud. `FND-PARENT-1046` and `FND-PARENT-0078` remain in
progress; `FND-PARENT-1038` is unchanged and not closed; `FND-PARENT-1036`
remains `blocked_external_dependency`. PR #354 remains Draft, open, and
unmerged.

### 2026-09-06 ninth hosted follow-up (root-owned Functional-A ancestry and fixed-temporary-root successor pending)

The normal successor `c98dbac165d1d2dcee81fafab4a670bd90a82f53` passed its
exact-head Security workflow lint, but its GitHub-hosted Functional-A workflow
`33999740011` then failed closed with exit `77` in the first runtime step. It
had completed checkout, exact-HEAD verification, the root/worker preflight,
isolated-path initialization, and unprivileged pinned provisioning. The
unchanged runtime path-authority validator correctly rejected the runner-owned
job-root ancestor while executing as root: `runtime directory has an untrusted
owner below shared temporary root /tmp`. No NGINX server, native on/off
callback, JSONL, WAF, allow, reload, or shutdown assertion ran. Exit `77` is
failed evidence, not a successful hosted result.

The same exact c98 SonarQube Cloud analysis reported one active task-owned
`python:S5443` issue at the Functional-A launcher public-temporary-root line
and Quality Gate `ERROR`. No `NOSONAR`, rule exclusion, false-positive state,
Quality-Gate change, or risk acceptance was used. The narrowly scoped
successor resolves the standard temporary-directory result only to fail closed
unless it is the exact fixed `/tmp` namespace, then retains the existing
no-symlink, root-owned sticky `01777`, owner, mode, and traversal checks before
the scrubbed `sudo` handoff. It does not accept a `TMPDIR`-redirected root.

Before unprivileged provisioning, the workflow now creates the fresh
Functional-A job root and its fixed functional-parent sibling as root-owned
directories, validates only the job root's initial `0700` state, and then sets
both ancestors to non-enumerable `0711`. It creates, chowns, and keeps only the separate
provisioning `RUN_ROOT` runner-owned at exact `0700`. The launcher therefore
requires root ownership for both visible ancestors and runner ownership only
for that private root. This preserves the existing runtime path-authority
validator, leaves unprivileged provisioning unprivileged, and does not add a
generic path reopen or broaden the privileged command surface.

The successor's non-root-fixture launcher, exact-gate, worker-traversal,
path-authority, and runtime-path security suite passed 49 focused tests;
`actionlint` with ShellCheck, shell syntax, Python compilation, and whitespace
checks also passed. These local source/contract results are not a Sonar or
GitHub-hosted runtime success claim. After its normal successor push, the new
exact head still requires fresh C17 and available-sanitizer assessment,
SonarQube Cloud Quality Gate plus active-issue/hotspot readback, relevant
checks, all five CRS/no-MRTS cells, and the native GitHub-hosted
on/off/JSONL/WAF/allow run.

`FND-PARENT-0078` remains `in_progress`; `FND-PARENT-1046` remains
`in_progress`; `FND-PARENT-1038` is unchanged and not closed; and
`FND-PARENT-1036` remains `blocked_external_dependency`. Functional A remains
a GitHub-hosted native integration test, not Protected B or an attestation
against malicious runner or VM-root code. PR #354 remains Draft, open, and
unmerged.

### 2026-09-06 tenth follow-up (narrow native Phase-4 and lifecycle candidate pending successor proof)

The predecessor `f5c16f210cd6435a7372ca8d4f8ed10aaa2d9174` is not evidence for
this candidate. Its dynamic transaction-ID path reached Common with an
evaluator-added terminal NUL because `ngx_conf_set_transaction_id()` used
`ccv.zero=1`; Common correctly rejected that non-canonical byte. The narrow
NGINX C change sets `ccv.zero=0`, retains strict Common byte validation, copies
only the exact evaluated bytes, and adds its own C terminator after the copy.
No Common validation, serializer, redaction, integrity, WAF-URI, dependency,
Framework, MRTS, or Gitlink behavior was changed.

The candidate also makes two native lifecycle assertions causal. For a
deliberately unsafe phase-4 target it preserves expected `nginx -t` rejection,
records the active master/worker identity, then delivers direct HUP to that
master rather than treating a separate `nginx -s reload` parse as signal
delivery. For the secure reload it reuses the pinned, read-only Framework
synchronized upstream through a dedicated `modsecurity off`, unbuffered
loopback route; paused state and a client first byte precede reload, an exact
old live non-zombie direct worker and distinct replacement are observed from
one PID/PPID/state snapshot, and release occurs only after overlap. The
full-lifecycle synchronized control root is now additionally authorized below
the verified run root before the helper opens control or evidence files; an
out-of-root negative control is rejected fail-closed.

Fresh local candidate checks passed: 208 executable NGINX contract tests,
53 native/collector contracts, shell syntax, whitespace validation, and a
supported-source C17 compile. The bounded local exact gate passed both
`modsecurity_use_error_log` On/Off cells with dynamic-ID HTTP 200, phase-4
JSONL, redaction/integrity, no query canary, failed-reload rollback, secure
FD reload, old/new worker overlap, drain, descriptor closure, and cleanup.
An independent postpatch review found no validated bypass; its sole unvalidated
control-root boundary was added to the candidate and its focused negative test
passes. The repository-supported live Valgrind path is not available for this
artifact: Valgrind is installed, but the harness requires verified NGINX
`1.31.2` plus its retained archive while the local candidate artifact is
`1.31.4`; `scan-build` is absent. No sanitizer success is claimed. A direct
full-lifecycle positive attempt is likewise not claimed: `/var/tmp` rejected
the required worker `chown` with `EINVAL`, while creation of a task root under
`/tmp` returned `EROFS`.

The candidate is unpushed. Therefore all earlier hosted runs, checks,
CRS/no-MRTS cells, and Sonar analyses remain predecessor-only. After a normal
push, the new exact head still requires fresh hosted NGINX On/Off/JSONL/WAF/
allow and lifecycle evidence, all five CRS/no-MRTS jobs, required checks,
SonarCloud Quality Gate with zero active PR issues and zero hotspots, and any
available supported sanitizer path. `FND-PARENT-1048`, `FND-PARENT-1049`, and
`FND-PARENT-1050` are `fixed` locally with verification pending; `FND-PARENT-
1038` is unchanged and not closed; `FND-PARENT-1036` remains
`blocked_external_dependency`. PR #354 remains Draft, open, and unmerged.

### 2026-09-06 eleventh follow-up (task-owned Sonar successor)

The normal successor push of
`63487793c62c3407114482f748d6e808cc303f12` correctly created fresh exact-head
checks. SonarQube Cloud evaluated its Quality Gate as `OK`, but reported one
active task-owned `shelldre:S7679` issue at
`connectors/nginx/harness/run_nginx_smoke.sh`: the small
`nginx_process_children()` wrapper forwarded positional `$1` directly. The
next narrow successor assigns that value to the named POSIX shell variable
`nginx_children_parent_pid` before passing it to the already validated
snapshot helper. It changes no process, FD, path, request, or logging
semantics and has a focused source-contract regression.

The new commit necessarily invalidates all in-progress `63487793` hosted
results as successor proof. After its normal push, only checks, Sonar analysis,
CRS/no-MRTS cells, and NGINX On/Off runtime evidence bound to its own exact
head may satisfy the remaining acceptance criteria. PR #354 remains Draft,
open, and unmerged; FND-PARENT-1036 remains
`blocked_external_dependency` and FND-PARENT-1038 remains unchanged.

### 2026-09-06 twelfth follow-up (targeted pre-merge gate candidate)

This candidate adds a separately built, statically linked, test-only NGINX fixture for
the existing P4 body-limit boundary. It emits actual memory, file-only, and
mixed `ngx_buf_t` states through the installed connector filter, covers the
within-limit and reject-before-forwarding controls, and exercises file
metadata, missing-source, read, short-read, and request-pool-allocation error
paths. The fixture is not linked into the product. No product C correction was
made: current source uses the Common reject plan before native forwarding and
returns before the downstream filter on each tested error path. The 64-bit
selected runtime cannot represent the separate `file_length > SIZE_MAX` branch;
the runner records that limitation rather than claiming an artificial overflow
execution.

For FND-PARENT-1047, successful Envoy, Lighttpd, and Traefik cells now validate
their own normalized evidence before uploading only that evidence. A
non-successful generic or Apache cell publishes only a bounded, no-follow,
one-shot failure receipt, so a stale or partial PASS bundle cannot be uploaded
as its failure artifact. Apache retains its real Apache result path; HAProxy's
separate projector path is unchanged. The current FND-PARENT-1046 audit keeps
the historical `ad193b...` candidate run as partial functional evidence only:
it retained no field-level JSONL artifact and is neither proof for this
successor nor the independent protected-host evidence required by
FND-GITHUB-0009.

The successor's NGINX Functional-A workflow now prepares one fresh,
runner-owned private staging directory before the bounded root handoff. Only
after both real On/Off cells and their JSONL, raw-WAF, callback, lifecycle,
artifact-identity, and allow-control assertions pass, a no-follow, one-shot
writer emits a bounded canonical `result.json`. It records the exact Parent
head, pinned NGINX archive digest/version, role-labelled build identities and
the required boolean/count facts, but excludes raw logs, request targets,
Canaries, payloads, transaction identifiers, timestamps, and absolute paths.
This remains candidate-owned integration evidence for FND-PARENT-1046, not an
independent protected-host attestation for FND-GITHUB-0009.

At this record's commit time, the focused local contracts, C fixture compile,
workflow lint, and whitespace checks are current candidate evidence only. The
new clean exact-head native run, normal push, GitHub-hosted successor checks,
Sonar readback, five-cell CRS/no-MRTS artifact readback, and the separate
protected-base/host owner decision remain required. No merge, Draft transition,
rebase, force-push, risk acceptance, Framework/MRTS/Gitlink/dependency change,
or test, Sonar, or quality-gate weakening is asserted.

### 2026-09-06 thirteenth follow-up (native fixture's isolated runner root)

The exact-head NGINX workflow `34037807569` for
`2dba14da707216652227709e79bf73d58a6c8ba6` passed checkout, head verification,
preflight, provisioning, and the real Functional-A On/Off controls. It then
failed closed in the native body-buffer fixture's private `nginx -t` test with
the bounded class `permission_denied` and configuration-output SHA-256
`cf980554148465c1143c6be9dc8043b7543c4093d49d5b6518bb30d8f54d3486`. Both
uploads were correctly skipped, so this run supplies neither a native-fixture
nor a Functional-A artifact. The concurrently exact-head CRS/no-MRTS run
`34037807658` passed all five cells, including the strictly read-back Lighttpd
artifact, but becomes predecessor evidence after this successor change.

A controlled non-root reproduction identified no product defect. Common's
secure event-file parent walk opens every component with
`O_RDONLY|O_DIRECTORY|O_NOFOLLOW`; it correctly cannot read-open the
root-owned, non-enumerable `0711` Functional-A ancestor even though ordinary
path traversal is possible. The same fixture configuration test succeeds with
an output root that is a direct runner-owned `0700` child of the verified,
root-owned sticky `/tmp`. Common's no-follow, owner, and private-leaf checks
are unchanged.

The narrowly scoped successor creates that native-fixture root with an
unprivileged `mktemp` directly below the already checked `/tmp`, validates its
fixed namespace, non-symlink type, runner UID:GID ownership, and `0700` mode,
and passes it only to the native fixture. It leaves `FUNCTIONAL_JOB_ROOT`, its
root-owned `0711` ancestry, `RUN_ROOT`, the Functional-A evidence root, Common,
and product C unchanged. The artifact upload still admits only the existing
bounded `result.json` and fails when it is absent. This adds no runner,
privilege, dependency, or permission-policy change.

The successor requires fresh local and GitHub-hosted exact-head evidence,
including SonarCloud readback, all required repository checks, both NGINX
artifacts, and all five CRS/no-MRTS cells. PR #354 remains Draft, open, and
unmerged; this candidate-owned evidence remains distinct from the protected
host/collector decision required for `FND-GITHUB-0009`.

### 2026-09-06 fourteenth follow-up (current-base refresh and bounded exception)

The current user explicitly authorized one normal merge of current
`origin/master` into the existing PR #354 work branch, with no rebase,
force-push, direct default-branch write, Framework/MRTS/Gitlink/dependency
change, or test/quality-control weakening. The merge of current master
`9925ef647b5fb49d21aebd658a658d4fdb649c58` was clean. It preserves the
current-master NGINX Common-adoption checker, its regression suite, and its
paired Change Record while retaining the PR #354 remediation paths. The
resulting successor still requires a normal push, exact remote readback, and
fresh evidence; no predecessor result is promoted.

At `2026-09-06T19:30:15Z`, the current user also accepted only the residual
risk in `FND-GITHUB-0009`: functional GitHub CI selected by the PR is not an
independent protected-host attestation. The canonical finding is now
`accepted_risk` for one ordinary PR #354 integration only, not fixed,
verified, or closed; its technical Base/Environment/runner/host-gate work
remains open. The exception binds only after one final full successor SHA is
freshly validated and read back immediately before a regular GitHub squash
merge. It neither claims independent host proof, an external seal, or general
error-free behavior nor accepts another finding, defect, failed required check,
Sonar issue/hotspot, unresolved review, ruleset failure, bypass, release, or
later head.

The current integration policy also requires a 24-row connector-profile
assessment. The independently revalidated `FND-CROSS-0004` remains a separate,
not-risk-accepted release blocker: the Framework now has the five-connector
CRS fixture/catalog contract and the PR has five With-CRS/No-MRTS rows, but the
Parent workflow does not invoke the Framework aggregate command or retain an
exact-five Parent aggregate artifact. Therefore its criterion for a closed
Parent profile remains unmet. This task neither changes that infrastructure nor
treats a partial five-row result as an aggregate pass. The fresh successor will
retain the required five row-level results and a complete 24-row assessment;
until the independent blocker is resolved under separate authority, PR #354
remains Draft and must not be merged.

### 2026-09-06 fifteenth follow-up (HAProxy security-contract alignment)

Current-successor validation found five stale lexical assertions in two
repository-owned HAProxy static checkers, not a product regression. The source
had already been hardened in `2b3d7f7f`: a request requires one valid,
non-empty received `Host`, maps `hostname` only from that Host, and rejects and
cleans up an absent or invalid Host before transaction allocation. A legacy
checker still required an obsolete `server_ip` hostname fallback. Its updated
contract now forbids that fallback and requires the validated-Host rejection
and cleanup path. Its executable C17 mapper fixture now also rejects a
zero-header request and an empty `Host`, while retaining the valid-Host
control.

The HTX-overlay checker had likewise retained four pre-hardening field and
function-boundary spellings. It now follows the dispatcher into the real
request-header helper and the nested lifecycle fields, preserving the exact
invariants: P1 begins before request-payload registration, P2 and P4 mark EOS
before their sole binding finish calls, and a P2 native reply is possible only
before response headers. No production C, host behavior, workflow, gate,
Framework, MRTS, Gitlink, dependency, or test strictness was weakened. Two
independent security reviews found no surviving bypass or valid-Host
regression. The focused checker/HTX/C17 suite and 34 direct HAProxy contracts
passed; the final successor still requires a normal push, exact readback, and
fresh hosted evidence rather than promoting this predecessor result.

### 2026-09-06 sixteenth follow-up (final documentation-head disposition)

This paired documentation update is the next ordinary PR #354 successor. It
does not change product behavior, tests, workflows, Framework, MRTS, a
Gitlink, a dependency, a policy, or a required control. Its own exact SHA and
fresh GitHub/Sonar/runtime result readback must be recorded after its normal
push; no predecessor run is promoted to this documentation head.

The bounded FND-GITHUB-0009 exception remains `accepted_risk` only for one
future ordinary PR #354 integration after all non-excepted conditions pass. It
is not fixed, verified, closed, or consumed: the independent
FND-CROSS-0004 `P1` release blocker prevents any merge before that point. The
retained 24-row assessment has five passed cells, six blocked cells, and
thirteen unrun cells, and the required Parent exact-five aggregate artifact is
absent. Accordingly PR #354 remains open and Draft, no GitHub merge is
attempted, and there are no resulting-master checks or release actions to
report.

### 2026-09-07 seventeenth follow-up (Parent exact-five With-CRS/no-MRTS candidate)

This Parent-only candidate starts from PR #354 head
`3054e43ed9082a953e718ce2341bc7e9fc43b3a7` and checked base
`9925ef647b5fb49d21aebd658a658d4fdb649c58`. It adds a separate versioned
`with-crs-no-mrts` contract rather than changing or relabelling the existing
closed `no-crs` profile. The new producer binds each selected Apache, HAProxy,
Envoy, Lighttpd, and Traefik cell to schema version, exact Parent/base,
workflow-owned profile and cell run IDs, GitHub run/attempt, Framework/MRTS/CRS
provenance, actual case, original artifact paths, and their hashes. The strict
aggregator accepts exactly one descriptor-safe, canonical cell per expected
connector and rejects missing, duplicate, foreign, renamed, mixed-identity,
altered-hash, unsafe-path, and incomplete evidence.

`functional-facts.json` now carries `source_files_sha256`, the SHA-256 of the
canonical JSON representation of the ordered source-artifact list. The
aggregator recomputes this digest and rejects any receipt whose source paths or
hashes disagree, chaining source list → facts → receipt → manifest without
claiming external source authenticity.

Candidate review also found that canonical syntax alone did not require exact
JSON primitive types at the aggregate sink: Python equality admitted
value-equivalent `true`/`1`, `403.0`/`403`, and `0`/`false` substitutions in a
repacked cell. The aggregate now compares schema, manifest, receipt/facts,
block/allow, and no-MRTS structures recursively with exact types. This narrow
repair is tracked as FND-PARENT-1061 and rejects the reproduced mutations
without globally banning legitimate JSON booleans or floats.

The same final contract review found a distinct Apache producer-boundary gap:
summary/JSONL and cleanup-receipt scalars could accept `true`/`1` or
`403`/`403.0` before the producer rebuilt typed facts. The Apache-local exact
scalar comparison now rejects the six reproduced substitutions before facts or
a receipt are published, while the complete typed source control remains valid.
This is FND-PARENT-1062, a candidate-only source-contract/evidence-integrity
finding; its raw audit still independently binds the request, HTTP `403`, and
rule `942270`, so no connector runtime bypass is claimed. It remains
`in_progress` pending exact-successor hosted Apache/aggregate readback.

The candidate renders a complete, honest current 24-row disposition: five
selected With-CRS/no-MRTS cells can be `passed` only from the five validated
receipts; the six unavailable Envoy/Lighttpd/Traefik MRTS routes remain
`blocked`; the remaining thirteen cells remain `not_run`. The aggregate
separates technical validity, the five-cell functional result, disposition
completeness, and remaining integration conditions. That renderer and its
synthetic fixtures are not a hosted result, and they do not attribute the
historical `3054e43...` cell artifacts to the successor that will contain this
record.

For Apache, the new profile path verifies a raw serial transaction bound to the
selected request, HTTP `403`, and CRS rule `942270`. It writes a no-follow,
one-shot cleanup receipt only after bounded host/helper-process, selected
listener, and PID-file checks, and the workflow explicitly supplies
`RUN_ONE_CASE=1` with the current cell/run/GitHub identity. The producer also
verifies every required Apache summary/JSONL scalar and cleanup-receipt
identity with exact JSON primitive types before it can normalize facts.
For HAProxy, the profile reads the existing sealed stage through its strict
verifier using the distinct workflow evidence UID/GID; it neither copies nor
relabels that stage.
Its projected source receipt and sealed package now also carry the
Parent-issued `cell_run_id` as `cell_run_id_kind: workflow_cell`. The workflow
passes the same ID from `CRS_RUNTIME_RUN_ID` through projection and
verification; missing or mismatched IDs are rejected. This is workflow binding,
not a native HAProxy run-ID claim. Candidate review identified the Apache
false-complete cleanup boundary, the missing selected-case handoff, and the
source-list/HAProxy-cell binding gap before delivery. They are tracked locally
as FND-PARENT-1058, FND-PARENT-1059, and FND-PARENT-1060, all `fixed` pending
exact-successor hosted verification; the earlier raw-observation gap remains
FND-PARENT-0218 and is not silently closed.

Fresh local controls passed: 104 profile, Apache, HAProxy, and workflow tests
(11 environment skips); 17 protected no-CRS contract tests; 67 current
runtime-observation contract tests; Apache/HAProxy shell syntax; selected
Python compilation; 22 bilingual documentation tests; and `git diff --check`.
The earlier broader 141-test runtime/observation run predates the narrow
Apache-scalar change and is not represented as its direct control. Expected
negative fixtures print their internal `FAIL:` diagnostics while their test
processes exit successfully. Full bilingual/link Make targets remain
environment-blocked only by the existing unavailable Framework-submodule
targets and are not reported as passed. No Framework, MRTS, Gitlink,
dependency, policy, ruleset, test, Sonar, or Quality-Gate change is part of
this candidate.

No new head has been pushed at this record revision. A normal commit/push to
the existing PR #354 branch, exact remote/PR head readback, a fresh GitHub-
hosted five-cell profile run, child-receipt and aggregate-artifact readback,
current required checks, SonarCloud Quality Gate/issue/hotspot readback, and
review disposition remain required. FND-CROSS-0004 remains `blocked` until its
existing acceptance criteria are actually met; PR #354 remains Draft and
unmerged.

### 2026-09-07 eighteenth follow-up (first exact-five failure repair)

The first delivered exact-five head
`8f91f70ce8f1bdf6167aa5e1aa386fe18df0fa50` was exercised only by the fresh
GitHub-hosted workflow `34140286420`, bound to the checked base
`9925ef647b5fb49d21aebd658a658d4fdb649c58`. It failed closed and is negative
evidence only: the four non-Apache producers rejected the pinned CRS source
because its valid JSON-like rule form uses the quoted key `"id":942270`;
Apache lacked the raw serial audit file demanded by its evidence validator; and
the aggregate correctly rejected unavailable upstream cells. This does not
establish a CRS HTTP-block failure or promote any failure receipt to a passing
cell.

FND-PARENT-1063 narrows the CRS identity matcher to the actual pinned quoted
form and its established unquoted form, while retaining exact descriptor,
digest, and commit verification and rejecting tested near misses. FND-PARENT-
1064 appends profile-only Apache serial/native audit directives with parts
`ABFHZ` after case materialization and before startup, only for a complete
selected With-CRS profile. It leaves No-CRS and incomplete/non-profile paths
outside that append. No Framework, MRTS, Gitlink, dependency, workflow policy,
or existing control was changed.

A mandatory independent review then found that the new generated
`SecAuditLog` sink must treat its derived path as Apache configuration data.
FND-PARENT-1065 records the payload-safe quote/newline directive-split
reproduction and the distinct Apache configuration-variable expansion case.
The profile-only guard now rejects quote, backslash, dollar characters, and
POSIX control characters before append or server startup. Its real extracted-
shell regression accepts a normal absolute path with spaces/ordinary
punctuation and rejects quote/newline, backslash, and expansion inputs
fail-closed. This is a narrow new-sink repair; no local Apache configtest or
runtime acceptance is claimed.

The candidate also contains narrow source refactors addressing
FND-SONAR-0079 without a suppression, quality-gate change, or semantic
relaxation. The prior SonarCloud result on `8f91f70...` remains failed
(Quality Gate `ERROR`, 44 active open issues, no reviewable hotspots), so a
fresh SonarCloud result for the successor is required and no green result is
claimed here.

After the final path-guard change, the combined affected Parent suite passed
`265` tests with `11` existing environment skips. It covers CI security,
the Apache profile guard, HAProxy projection/workflow/harness contracts,
With-CRS producer/aggregate/runtime contracts, runtime observations, and the
protected No-CRS profile/workflow contracts. Expected negative-fixture
diagnostics are emitted inside tests that exit successfully. A fresh normal
commit/push, exact remote/PR-head readback, hosted five-cell/aggregate artifact
validation, current required checks, and exact-successor SonarCloud readback
remain mandatory. PR #354 remains Draft and unmerged; FND-CROSS-0004 remains
`blocked` pending its existing acceptance criteria.

### 2026-09-07 nineteenth follow-up (native Apache audit parser and Sonar successor)

The fresh exact-five run `34149333852`, bound only to delivered head
`0ffb03bb72a6c0a2ecf8aa12581175bffe0b6b41` and base
`9925ef647b5fb49d21aebd658a658d4fdb649c58`, reached the Apache raw-audit
validator but failed closed before receipt publication. Its Apache job reported
`Apache audit has data outside a transaction`. The retained failure receipt is
negative evidence only; it is not a profile cell or a proof of a failed CRS
HTTP block.

The failure was a distinct Parent parser/fixture defect: real ModSecurity
Native serial boundaries are `---<transaction>---<part>--`, whereas the newly
introduced parser and synthetic fixture expected `--<transaction>-<part>--`.
The parser now accepts only the actual Native shape, and the regression covers
the valid Native control plus rejection of the former non-Native shape and an
arbitrary preamble. FND-PARENT-1066 records this evidence-integrity defect as
in progress pending a new exact-successor hosted Apache receipt and aggregate
readback; no production connector vulnerability, protected-host attestation,
external seal, or merge authority is claimed.

The same successor retains the narrow behavior-preserving refactors for the
eight active SonarCloud items on `0ffb03...`: shared manifest/diagnostic
literals and analyzer-visible container narrowing preserve the strict
exact-builtin-type comparison. No `NOSONAR`, issue exclusion, Quality-Gate,
workflow, or test weakening is used. A normal successor push, fresh exact
SonarCloud Quality Gate/issue/hotspot readback, and a new hosted exact-five
run remain mandatory. The later user authorization to merge current
`origin/master` into the existing PR branch is a normal branch update only;
PR #354 remains Draft and unmerged.

### 2026-09-07 twentieth follow-up (master merge and final Sonar contract cleanup)

The authorized normal branch update merged current `origin/master`
`08fab232d77e300be15cb010e2adbcd590955727` into the existing PR #354 branch
as `775060fffb835f871e3abe3a49f302ad27a705b6`; it did not merge PR #354 into
`master`, change its Draft state, rebase, or force-push. The two HAProxy
conflicts retained current-master Common-header validation and SPOP byte-bound
controls while preserving the PR's NULL-header regression. The merge exposed
two stale test assumptions, not a product rollback: the Traefik contract now
checks the current shared monotonic-deadline send path, and the HAProxy target
control accepts exactly 4096 lossless bytes and rejects 4097 bytes.

SonarCloud analyzed exactly `775060ff...` with Quality Gate `OK`, zero
reviewable hotspots, but two active `python:S5778` test-code issues remained
at the two Apache audit negative controls. They are real maintainability
findings: each `assertRaisesRegex` body contained both an encoding expression
and the parser call. The narrow successor candidate precomputes the immutable
UTF-8 bytes outside each exception context, leaving exactly the parser call
inside it. Both malformed-Native-boundary and untrusted-preamble controls
still require the same `ValueError`; the valid Native control is unchanged.
No parser, workflow, test outcome, `NOSONAR`, issue disposition, or quality
control is weakened.

The in-progress five-cell run `34154897241` is bound only to transitional head
`775060ff...` and base `08fab232...`; it cannot be used as evidence for this
new successor. After its ordinary non-forcing push, only fresh exact-head
SonarCloud Quality-Gate/zero-issue/zero-hotspot readback, required GitHub
checks, and a new five-cell aggregate/artifact readback may advance this PR.
FND-CROSS-0004 remains independently blocked, and PR #354 remains Draft,
open, and unmerged.
