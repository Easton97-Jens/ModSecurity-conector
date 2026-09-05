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
| Delivery status | Draft PR [#354](https://github.com/Easton97-Jens/ModSecurity-conector/pull/354) is open and unmerged. Exact-head `f38f239a8d0e73408a049583f5fcdb01d8b7be9b` completed the full hosted runtime workflow and SonarCloud Quality Gate; its NGINX provision/compile passed, while its on/off runtime cells remain deliberately blocked by the required worker-identity control. This documentation successor requires its own fresh exact-head rerun. |

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
