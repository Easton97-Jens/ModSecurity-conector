# Change Record

**Language:** English | [Deutsch](CR-20260824-connector-security-invariants.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260824-connector-security-invariants |
| Date (UTC) | 2026-08-24 |
| Base revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Current uncommitted extension baseline | 8d8907f605a36ed8139d891f03f028cafb06bc99 |
| Repository boundary | Parent only; Framework, MRTS, Gitlink, CI, and governance unchanged |
| Delivery authority | Current user explicitly authorized Parent commit, push, and Draft PR creation; no merge |

## Motivation and problem statement

The requested assessment covers ten connector variants and their shared
Common, Engine, Provisioning, and Runtime boundaries. The source review found
three Parent-owned hardening opportunities with a concrete control gap:
remote-rule configuration could reach libmodsecurity remote loading without a
uniform trust policy; the unauthenticated HTTP authorization helper accepted a
wildcard listener, duplicate security-sensitive headers, and a silent
listener-address substitute for an absent or oversized `Host`; and Common
event output could serialize unescaped protocol metadata and open an unsafe
final event path.

A focused second Common re-audit found three additional independently
remediable boundaries: positive-only resource configuration could exceed the
header/event/body hard caps before allocation paths; malformed UTF-8 bytes could
produce invalid event JSONL; and a detached authorization worker could outlive
the stack-owned service object after both bounded shutdown waits expired.

The executable NGINX direct-archive path is in the separate Framework
repository. Current authorization permits Parent-only changes; Framework
write/test work requires an explicit repository selection by the user. The
path is therefore reported as a blocked remediation dependency rather than
patched or represented as safely extracted here.

## Acceptance criteria

- Every reviewed Parent remote-rule entry point rejects both complete and
  incomplete remote-rule configuration before a network-capable sink.
- Apache, NGINX, and Common Runtime do not retain a productive
  `msc_rules_add_remote` path; all connector capability records describe the
  same policy.
- Native Apache, HAProxy SPOE/SPOP, and NGINX fail closed on a rejected engine
  operation, missing authority/Host, or request-body budget breach; none
  selects a listener, virtual-server, server-endpoint, or `localhost` value as
  a silent substitute for client authority.
- HAProxy HTX fails closed after setup, sequence, header, or body-append
  failure; the SPOP diagnostic parser has finite reads, overflow-safe varints,
  bounded strings, and header-byte validation.
- Envoy ext_proc accepts only numeric loopback listeners, has finite
  connection/stream admission, and rejects a request with neither `:authority`
  nor `Host` before engine mapping.
- The Traefik Native UDS service has no unbounded worker queue or default
  lifetime shutdown: it admits at most 64 active workers with a backlog of 32,
  while an explicit positive `--max-connections` remains a controlled one-shot
  test boundary.
- The unauthenticated Common HTTP authorization endpoint remains loopback-only
  and rejects duplicate, absent, empty, or oversized `Host` values and
  configured original-URI headers before transaction mapping; it never
  substitutes the listener address as hostname.
- Event metadata remains payload-free JSONL, is escaped and NULL-safe, and the
  POSIX final event file is no-follow, regular, and private (`0600`).
- The FNV-derived event chain is documented only as process-local,
  non-cryptographic correlation; it is not described as tamper evidence.
- Common header/event resource settings reject values above their fixed caps;
  request, response, and phase-4 body configuration rejects values above
  10485760 bytes (10 MiB).
- Event JSONL preserves valid UTF-8, encodes malformed bytes as `\\u00XX`, and
  caps each event-field scan; it never emits request or response body payloads.
- A detached authorization worker never references a destroyed service/runtime;
  deferred shutdown transfers final cleanup to the last worker safely.
- No workflow, branch-protection, ruleset, required-check, or other governance
  path is changed.

## Implementation decision and rationale

Policy A was selected for remote rules: remote loading is uniformly disabled.
The existing Common, Apache, and NGINX source paths did not jointly enforce
HTTPS, origin allowlisting, integrity verification, size and time bounds,
atomic activation, or credential isolation required for a secure remote-loading
policy. Configuration validation, the Common loader, Common Runtime, and both
host directive handlers now fail closed before a fetch or native remote API
call. Inline and local rules files remain supported.

The Common HTTP authorization service has no authenticated transport mode.
Its listener parser therefore normalizes `localhost` to `127.0.0.1` and rejects
wildcards and other addresses. It also rejects duplicate `Host` and
profile-designated original-URI headers before a selected value can influence
mapping. An absent, empty, or oversized `Host` now receives a 400 response
before mapping rather than silently becoming the listener address. The existing
bounded worker admission and shutdown ownership model is preserved; shutdown
returns a defined failure rather than destroying Runtime objects still held by
an uninterruptible worker.

Event protocol text is escaped with the shared JSON escaper. The POSIX event
sink is opened with `O_NOFOLLOW`, verified as a regular file, restricted with
`fchmod(0600)`, and then converted to a stream. Windows has no equivalent
reparse-point control in this implementation and therefore fails closed instead
of opening a configured event path. The change intentionally does not claim
cross-process tamper resistance.

The Common Content-Length parser now rejects every duplicate value, including
identical duplicates. This avoids relying on different host normalization rules
at a request-smuggling-sensitive translation boundary.

Resource limits are now constrained in both Common resource validation and
runtime configuration validation. Existing checked-in profiles selecting a
10 MiB body limit remain valid, while larger request, response, or phase-4
budgets fail before Common buffering/allocation paths consume them.

Event serialization now uses a length-aware JSON escaper at the event boundary.
Valid UTF-8 is retained; each malformed byte becomes a `\\u00XX` JSON escape.
This is a JSON-safety transformation, not a byte-for-byte preservation claim.

For bounded shutdown, the authorization service is heap-owned and contains a
bounded, fully owned copy of the profile structure, its text fields, and its
original-URI header list. If both waits expire, the last detached worker
unlinks itself and releases the service/runtime; if mutex ownership cannot be
proven, the process-local state is intentionally leaked rather than freed while
potentially live. Mapping callbacks are retained only as code pointers.

## Current native connector-boundary extension

The follow-up review found validated Parent-owned gaps at native connector
boundaries and made narrow fail-closed changes. Apache now propagates native
engine failures as request errors, accepts only exact libmodsecurity phase
success (`== 1`), applies the shared request-body budget before append, and
opens native event files through a no-follow, regular-file,
private-descriptor contract. NGINX requires an actual nonempty client `Host`,
propagates transaction/header/body errors, bounds in-memory and temporary-file
request bodies, and rejects the native phase-4 event directive rather than
opening a path without an equivalent safe descriptor contract.

The Apache request mapper now also rejects absent or empty received `Host`
metadata rather than substituting `r->hostname`. HAProxy's native mapper
rejects missing or empty `Host`, and the binding treats that mapper failure as
terminal before allocating a libmodsecurity transaction. The legacy CRS helper
requires an explicit Host and the SPOP notify handler disconnects a request
with missing host metadata before either legacy or production processing.

HAProxy binding also accepts only exact libmodsecurity phase success (`== 1`),
while keeping the separate rule-loading return contract unchanged. HAProxy HTX
now records header setup and response-header engine failure in a distinct
`fail_closed` state and returns `-1` from later header or payload callbacks;
it no longer treats a missing transaction after a non-disabled abort, missing
response headers, or append failure as pass-through. The SPOP diagnostic runtime
uses a monotonic bounded receive deadline, rejects malformed or overflowing
varints and unrepresentable typed strings, validates header bytes before
transaction input, and limits worker/configuration choices that would otherwise
create unsupported concurrent or response-body paths.

Envoy ext_proc now rejects non-numeric, non-loopback listener configuration,
enforces 128 concurrent connections and 128 concurrent RPC streams, and
rejects a request that lacks both `:authority` and `Host`. The Traefik Go
middleware selects `uds` when `engineMode` is omitted and rejects every other
mode, including `passthrough`, before it can select an allow-all engine. The native C UDS engine limits live detached
workers to 64 before allocation and closes excess sockets instead of queueing
them. Its historical zero value remains the persistent-service sentinel;
positive `--max-connections` is retained only for controlled one-shot runs.
When a nonstandard Header-map `Host` is present, it must be singleton,
control-free, and exactly equal to `request.Host`; a mismatch or header-
splitting value is rejected before the engine sees either representation.

An independent final review caught an intermediate implementation that changed
the default zero sentinel to a 256-connection lifetime quota. Because the Go
middleware opens one UDS connection per request, that was a confirmed local
availability/DoS regression. The final code removes that default quota while
retaining the active-worker and backlog bounds. Local 258-connection and
64-active-worker saturation/recovery tests exercise the repaired behavior.

## Final 2026-08-25 boundary reconciliation

The last boundary pass adds four evidence-backed records. `FND-PARENT-0912`
makes the HAProxy mapper outcome an engine-entry prerequisite: invalid syntax,
header budgets, authority cardinality, duplicate Content-Length, and
Content-Length/Transfer-Encoding ambiguity now fail before raw request or
response header sinks. `FND-PARENT-0913` makes SPOP notification consumption
exact, validates bounded header/varint input, and gives the legacy state-null
receive path a 2,000 ms deadline. `FND-PARENT-0914` bounds
`max-transactions` to `1..65536`, defaults it to 4096, and proves the cache
allocation size before `calloc`.

`FND-PARENT-0915` is a confirmed Common concurrency defect, not merely a
static candidate: pre-fix ThreadSanitizer observed the SIGTERM/SIGINT handler
write `authorization_stop` while a detached worker read it through its I/O
helpers. Workers now inherit a blocked SIGTERM/SIGINT mask during creation and
have no reachable read of that flag; deadline and socket-shutdown cancellation
remain. The repaired normal timeout/admission smoke, Common memory-safety
target, six-test authorization contract, and same TSan smoke all passed with
exit code 0 and no TSan warning. This supersedes the earlier full-timeout TSan
classification as inconclusive.

The task's external payload-safe evidence manifest is
`/var/tmp/codex/ModSecurity-conector/runs/20260825T005347Z-connector-security-final-validation/manifest.json`.
Its current focused Python suite recorded 103 passing tests; the later amended
Common authorization contract passed 6/6. The standalone SPOP ASan/UBSan/leak
harness, HAProxy C17/overlay controls, Apache C17 lint, and Traefik Go race,
vet, and format checks passed as separately retained focused evidence.

`FND-CROSS-0011` remains blocked rather than misrepresented as fixed: the
separately governed Framework NGINX provisioner directly calls `tar -xf` and
bypasses the shared helper. The direct path has not received the required
bounded member/path/link/type/count/size/target-root/overwrite preflight or
isolated positive/negative archive controls. No archive was constructed or
extracted because the user has not explicitly selected the Framework repository
for write/test work.

## Post-reconciliation update — 2026-08-25

The last Parent-only source-to-sink pass added seven fixed, not host-runtime
verified, records. `FND-PARENT-0916` gives the public HAProxy binding and HTX
borrowed-payload path cumulative request/response byte budgets with
subtraction-form overflow checks before the libmodsecurity body sink.
`FND-PARENT-0917` rejects invalid header names, control characters, malformed
UTF-8, and oversized total header input in Envoy ext_proc before the raw CGo
header sink; it also preserves the no-authority fail-closed rule.
`FND-PARENT-0918` rejects response-bearing SPOP arguments in a `check-request`
notification so a peer cannot reclassify request processing as response
processing.

`FND-PARENT-0919` makes Envoy's optional JSONL observer walk every absolute
ancestor with no-follow descriptors and reject unsafe final type, ownership, or
mode before mutation. `FND-PARENT-0920` applies the equivalent
descriptor-backed ancestor, ownership, type, and private-mode contract to the
Common Runtime event file. `FND-PARENT-0921` makes both Apache compiled
connection-phase hooks treat every return other than `1` as an internal error
before normal request processing. `FND-PARENT-0922` applies the same secure
ancestor contract to Apache's native event file. These records do not assert a
remote exploit where the evidence only proves a local parser or descriptor
boundary.

The current task worktree passed the 118-test focused contract suite, Apache
C17, Common memory safety, the Common authorization timeout/admission smoke,
Envoy ext_proc and Traefik Native package race tests plus Vet/format checks,
and the HAProxy HTX overlay contract. The validation receipt is
`/var/tmp/codex/ModSecurity-conector/runs/20260825T014358Z-final-focused-contract-rerun/evidence/validation-summary.md`
(SHA-256 `52ac0fecea6bf7e5e5657ba6cb8cf00bce34995e918c3c271cf76b0c887bc2c3`).
The exact HAProxy C17 target remains blocked before compilation by
`nginx_pinned_provenance_ref_mismatch`; the legacy Common helper and SDK
contracts remain failed on pre-existing CI-owned expectations and were not
changed. This evidence does not replace the unavailable native ten-host,
HTTP/2/HTTP/3, reload, leak, or full sanitizer matrix.

## Final focused validation postscript — 2026-08-25

The final focused review records `FND-PARENT-0923` through
`FND-PARENT-0925` as fixed in the Parent source and test boundaries, but not
as host-runtime verified. Envoy ext_proc now revalidates the final redirect
`location` value at the response-header sink, rejecting invalid UTF-8,
controls, whitespace, CR/LF, NUL, and overlong values before emitting the
header. HAProxy SPOP preserves an active transaction when a duplicate request
ID arrives; the duplicate is rejected and cannot replace or finish the
original transaction. The Envoy Phase-4 harness now tracks accepted handler
threads through completion before temporary-root teardown, and retains the
standard HTTPS server type rather than changing the TLS fixture semantics.

The final observed validations were: Envoy transport `19/19`; Envoy Go
`-race`, `vet`, and `gofmt`; SPOP reliability `14/14`; the focused Parent
suite `104/104`; the HAProxy HTX overlay contract; and `git diff --check`.
These are local source, harness, and package checks. The complete ten-host
matrix, HTTP/2/HTTP/3, reload, leak, and full sanitizer coverage remain
unrun; the Framework NGINX archive path remains blocked under
`FND-CROSS-0011`. No commit, push, pull request, or other delivery action is
authorized by this record.

## Changed files

- `common/src/config.c`, `common/src/rule_loader.c`, `common/src/rule_merge.c`,
  `common/src/directive_spec.c`, and `common/runtime/msconnector_runtime.c` —
  shared remote-rule denial, Runtime enforcement, and secure event opening.
- `common/src/headers.c` and `fuzz/common_http_headers_fuzz.c` — fail-closed
  duplicate Content-Length parsing and its bounded fuzzer control.
- `connectors/apache/src/msc_config.c` and
  `connectors/nginx/src/ngx_http_modsecurity_module.c` — direct host directive
  denial before native remote conversion.
- `common/runtime/http_authorization_service.c` — loopback-only listener,
  fail-closed duplicate/missing/empty/oversized `Host` validation before
  mapping, signal-safe send, and bounded shutdown behavior; heap-owned deferred
  cleanup, a bounded fully owned profile for an uninterruptible detached
  worker, and serving-thread-only shutdown-flag ownership with worker signal
  masking.
- `common/src/event.c`, `common/include/msconnector/event.h`, and
  `common/include/msconnector/integrity_event.h` — escaped/null-safe event
  metadata, safe correlation semantics, and event-sink invariant.
- `common/src/json_escape.c` and `common/include/msconnector/json_escape.h` —
  length-aware valid-UTF-8 preservation and malformed-byte JSON encoding.
- `common/include/msconnector/limits.h`, `common/src/resource_limits.c`, and
  `common/src/config.c` — finite header/event limits plus a 10 MiB hard
  configuration cap for request, response, and phase-4 bodies.
- `connectors/{apache,nginx}/README.md` and `.de.md` — remote-rule behavior.
- `connectors/{apache,nginx,envoy,haproxy,lighttpd,traefik}/capabilities.json`
  — one consistent remote-rule capability statement.
- `tests/test_remote_rules_disabled.py`,
  `tests/test_http_authorization_service_security_contract.py`, and
  `tests/test_event_runtime_security_contract.py` — focused regression
  contracts.
- `tests/event_json_utf8_smoke.c`, `tests/test_resource_limits_hard_caps.c`,
  and `tests/http_authorization_service_detached_worker_smoke.c` — focused
  malformed-UTF-8, cap, missing-Host rejection before mapper entry, and
  deferred-worker lifecycle controls.
- `examples/common/common-connector-configuration.{md,de.md}`,
  `docs/{configuration,architecture}.{md,de.md}`, and the Apache/NGINX README
  pairs — documented finite limits, phase-4 configuration cap, and the
  technically enforced remote-rule rejection policy.
- `connectors/apache/src/mod_security3.c`, `msc_filters.c`, and
  `msc_apache_mapper.c` — fail-closed engine-return propagation including
  exact connection and request-phase success, bounded native request-body
  intake, descriptor-backed ancestor-safe native event opening, and mandatory
  received Host mapping.
- `connectors/nginx/src/ngx_http_modsecurity_{access,common,mapper,module}.c`
  and the NGINX README/capability records — mandatory client Host,
  error/body-limit propagation, and fail-closed native phase-4 event logging.
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`,
  `connectors/haproxy/src/haproxy_modsecurity_mapper.c`,
  `connectors/haproxy/src/haproxy_modsecurity_binding.c`, and
  `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — fail-closed HTX
  setup/error/sequence handling including unmappable disruptive decisions and
  request-EOS failures, cumulative bounded borrowed payload accounting, exact
  native phase success, mandatory authority before
  transaction allocation, fail-closed request/response mapper outcomes with
  bounded/validated header framing, and bounded SPOP frame/header/liveness and
  transaction-cache parsing/allocation plus notification-phase consistency.
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-ext-proc/main.go` and
  `internal/processor/{config,jsonl,processor}.go` — numeric-loopback
  configuration, finite gRPC admission, authority/header validation, and
  descriptor-backed private JSONL output.
- `connectors/envoy/ext_proc/internal/processor/{processor.go,processor_test.go}`
  — final redirect `location` validation at the response-header sink and its
  invalid-UTF-8/control/whitespace/size regression cases.
- `connectors/envoy/harness/envoy_smoke_helper.py` and
  `tests/test_envoy_transport_hardening_contract.py` — accepted-handler
  lifecycle tracking through deterministic Phase-4 cleanup while preserving
  the HTTPS fixture type and TLS behavior.
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` and
  `tests/test_sonar_reliability_contract.py` — duplicate SPOP request-ID
  rejection while preserving the active transaction and its regression
  contract.
- `connectors/traefik/native_middleware/`,
  `connectors/traefik/src/traefik_engine_service.c`, and matching Traefik
  configuration/README/ORIGIN files — secure UDS default, finite active admission,
  no default lifetime shutdown, authority validation and Header-map agreement
  before engine creation,
  and portable peer-identity limitation.
- `common/src/generic_mapper.c` — preserves a missing client hostname instead
  of silently substituting a server endpoint as request authority.
- `tests/test_{apache_connection_phase_contract,apache_native_security_contract,haproxy_binding_phase_contract,haproxy_header_validation_contract,haproxy_htx_filter_security_contract,native_host_fallback_contract,nginx_native_security_contract}.py`,
  Envoy ext_proc Go tests, Traefik Go/native tests, and the existing focused
  Common/Apache/SPOP contracts — task-owned regressions for these boundaries,
  including missing-host, header-framing, worker signal-ownership, and HTX
  fail-closed cases.
- This English/German Change Record pair.

No Framework source, MRTS source, Gitlink, dependency, generated runtime
artifact, or CI/governance file is part of this change.

## Commands executed

The placeholder `<external-task-root>` denotes the task-owned directory under
`/var/tmp/codex/ModSecurity-conector/`; it is outside the checkout.

### PASS

~~~text
rtk proxy python3 -B -m unittest -v tests.test_remote_rules_disabled tests.test_http_authorization_service_security_contract tests.test_event_runtime_security_contract
rtk proxy env BUILD_ROOT=<external-task-root>/http-timeout make check-http-authorization-service-timeout
rtk proxy env CC=clang ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=address -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-asan make check-http-authorization-service-timeout
rtk proxy env CC=clang UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=undefined -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-ubsan make check-http-authorization-service-timeout
rtk proxy env BUILD_ROOT=<external-task-root>/memory make check-common-memory-safety
rtk proxy env BUILD_ROOT=<external-task-root>/fuzz make check-common-http-header-fuzz
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -Icommon/runtime -fsyntax-only common/src/headers.c common/src/rule_merge.c common/src/event.c common/runtime/msconnector_runtime.c
rtk proxy make check-common-security-contract check-common-flow-integrity check-directive-parity
rtk proxy sh -c 'cc -std=c17 -Wall -Wextra -Werror -I. -Icommon/include tests/test_resource_limits_hard_caps.c common/src/resource_limits.c common/src/limits.c common/src/config.c common/src/body_policy.c common/src/block_statuses.c common/src/http_status.c -o <external-task-root>/resource-limits-hard-caps && <external-task-root>/resource-limits-hard-caps'
rtk proxy sh -c 'clang -std=c17 -Wall -Wextra -Werror -fsanitize=address,undefined -fno-omit-frame-pointer -I. -Icommon/include tests/test_resource_limits_hard_caps.c common/src/resource_limits.c common/src/limits.c common/src/config.c common/src/body_policy.c common/src/block_statuses.c common/src/http_status.c -o <external-task-root>/resource-limits-hard-caps-asan-ubsan && ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 <external-task-root>/resource-limits-hard-caps-asan-ubsan'
rtk proxy sh -c 'cc -std=c17 -Wall -Wextra -Werror -I. -Icommon/include tests/event_json_utf8_smoke.c common/src/*.c -o <external-task-root>/event-json-utf8-smoke && <external-task-root>/event-json-utf8-smoke | python3 -c "import json,sys; [json.loads(line) for line in sys.stdin if line.strip()]"'
rtk proxy sh -c 'clang -std=c17 -Wall -Wextra -Werror -pthread -fsanitize=thread -fno-omit-frame-pointer -I. -Icommon/include -Icommon/runtime tests/http_authorization_service_detached_worker_smoke.c common/runtime/http_authorization_service.c common/src/*.c -o <external-task-root>/http-auth-detached-worker-tsan && TSAN_OPTIONS=halt_on_error=1 <external-task-root>/http-auth-detached-worker-tsan'
~~~

The focused Python suite passed 11 tests. The loopback timeout/admission smoke
passed in normal, ASan-with-leak-detection, and UBSan configurations. The
memory-safety target passed its normal and optional ASan/UBSan smoke. The
bounded libFuzzer run completed 533086 executions in 16 seconds, with no
AddressSanitizer or UndefinedBehaviorSanitizer diagnostic. The C17 syntax
check and listed Common contracts passed. The current documentation-link check
is blocked by the unavailable/uninitialized Framework submodule (17 Framework
targets); manual inspection found no missing target in the changed Parent
documents.

The second re-audit added a normal and ASan/UBSan hard-cap smoke, a normal and
ASan/UBSan malformed-UTF-8 JSONL smoke with strict Python JSON parsing, and a
controlled detached-worker smoke. The detached-worker control passed normally,
with ASan/UBSan plus leak detection, and with TSan without a diagnostic. Its
TSan result is separate from the existing full HTTP timeout-smoke TSan run,
which remains inconclusive. A subsequent header-fuzzer run completed 516409
executions in 16 seconds without a sanitizer/crash diagnostic; both fuzzer
counts are retained as separate historical local runs. The detached-worker
smoke also frees caller-owned profile text and the original-header list after
the service entry point returns, before releasing the blocked worker.

The follow-up Host control passed the five-test Python authorization contract,
a strict C17 syntax check, and a real local loopback smoke. Both a missing
`Host` and a 1024-byte Host value (the fixed hostname-buffer boundary) received
HTTP 400 before the smoke's mapper flag or fake Runtime transaction flag was
set; a subsequent valid `Host` still reached the intentionally held worker.
That same smoke passed with ASan/UBSan plus leak detection and with TSan
without a diagnostic. The existing timeout/admission/cancel/parallel smoke
passed again after the implementation change.

### Current native-boundary PASS

~~~text
rtk proxy python3 -B -m unittest -v tests.test_remote_rules_disabled tests.test_http_authorization_service_security_contract tests.test_event_runtime_security_contract tests.test_haproxy_htx_filter_security_contract tests.test_haproxy_binding_phase_contract tests.test_sonar_reliability_contract tests.test_nginx_native_security_contract tests.test_nginx_upstream_security_contract tests.test_traefik_native_local_plugin tests.test_apache_native_security_contract tests.test_generic_mapper_host_fallback_contract tests.test_native_host_fallback_contract
rtk proxy make -C connectors/haproxy check-htx-overlay
rtk proxy env APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/apache-c17-native-host-final make check-apache-c17-lint
rtk proxy make check-common-security-contract check-common-flow-integrity check-directive-parity
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -fsyntax-only common/src/generic_mapper.c
rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include -Iconnectors/haproxy/src -fsyntax-only connectors/haproxy/src/haproxy_modsecurity_mapper.c
rtk proxy env GOTOOLCHAIN=local go test -mod=readonly -run 'TestMiddlewareRejects(Invalid|Missing)AuthorityBeforeEngine' -count=1  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go test -mod=readonly -run 'TestMiddleware(RejectsConflictingHostHeaderBeforeEngine|RejectsInvalidHostHeaderBeforeEngine|AcceptsMatchingHostHeaderWithoutAuthorityDuplicate)' -count=1  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go test -race -mod=readonly ./...  # Traefik middleware
rtk proxy env GOTOOLCHAIN=local go vet ./...  # Traefik middleware
~~~

The current focused Python command passed 96 tests. Apache C17, the HAProxy
exact-success binding contract, and the HAProxy HTX overlay contract passed.
The Traefik middleware's targeted authority regression, `go test -race`, and
`go vet` passed. The Common security/flow/directive contracts and the strict
Common mapper syntax check passed. Earlier 107-test, Envoy, memory, timeout,
and fuzzer runs remain separately retained historical evidence for their
then-scoped sets.

The current HTX source contracts show that an unsupported disruptive action or
status and a request-body finalization failure now latch `fail_closed`, abort
the transaction, and return an error instead of entering disabled pass-through.
The Traefik middleware rejects missing or malformed `request.Host` before
`engine.Open`; its normal valid-authority control remains accepted. The Common
mapper no longer turns a missing client hostname into a server endpoint. These
are source-contract and local-package results, not host fault-injection proof.

The Traefik header adapter now also rejects a singleton `Header["Host"]` that
conflicts with `request.Host` or contains control characters before engine
open; a matching singleton host remains a one-entry normal control. The
focused three-case Go test, package race test, vet, and formatting check
passed. This is local adapter proof, not a real Traefik-host reachability test.

The additional native-authority contract proves that Apache rejects missing or
empty received Host metadata; HAProxy rejects it and aborts before transaction
allocation; the CRS helper requires an explicit host; and SPOP disconnects the
missing-host message before request processing. The positive CRS self-test
still uses explicit synthetic `localhost`; it is no longer a runtime fallback.

The isolated Traefik engine-service build and protocol/cleanup runtime check
passed normally, under ASan/UBSan with leak detection, and under TSan without a
diagnostic. Independent local clients verified 258 sequential connections
without a default lifetime shutdown and verified that the 65th simultaneous
connection is closed at the 64-worker cap, followed by successful recovery.

### Expected source absence

~~~text
rtk proxy rg -n 'msc_rules_add_remote|rule_backend\.add_remote' common connectors/apache connectors/nginx
~~~

This command exited `1`, which is the expected `rg` no-match result: no
productive source sink remained in the scoped paths.

### Failed / inconclusive

~~~text
rtk proxy env BUILD_ROOT=<external-task-root>/helpers make check-common-helpers
rtk proxy env CC=clang TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 MSCONNECTOR_CFLAGS='-std=c17 -Wall -Wextra -Werror -fsanitize=thread -fno-omit-frame-pointer' BUILD_ROOT=<external-task-root>/http-tsan make check-http-authorization-service-timeout
rtk proxy timeout 30s .venv/bin/python ci/checks/documentation/check-bilingual-docs.py
rtk proxy make -C connectors/traefik test-engine-service
rtk proxy <HAProxy full binding self-test>
rtk proxy make check-haproxy-c17-lint
~~~

`check-common-helpers` compiled then failed its existing assertion that a
complete remote-rule pair validates. Its test implementation is under `ci/`,
which the current request explicitly excludes; no policy or test weakening was
made. The older TSan wrapper attempts in this historical subsection had no
terminal status and remain inconclusive. They are superseded for the actual
signal/worker boundary by the later controlled pre-fix race confirmation and
post-fix clean TSan smoke documented in the final reconciliation. The bilingual
checker likewise produced no terminal exit status or completion marker through
the command wrapper within 30 seconds; required Change-Record headings and
English/German parity were reviewed manually, but its automated result is
inconclusive rather than passed.

The combined Traefik `test-engine-service` target builds successfully but its
unchanged socket-ownership self-test exits nonzero after the protocol self-test
passes. Direct runtime protocol/cleanup checks pass in normal, ASan/UBSan, and
TSan builds. `strace` is unavailable in this environment, so the unchanged
self-test failure is an open validation gap rather than evidence that the
socket-ownership control is unsafe.

The optional HAProxy full binding self-test is blocked before binding
compilation: its probe references unavailable symbol
`msc_get_rules_messages_rule_ids`. The focused source-contract and HTX overlay
controls are passing, but this blocker is not represented as host-runtime
validation.

The HAProxy C17 lint target also remains blocked before HAProxy compilation:
`prepare-runtime-components` reports `nginx_pinned_provenance_ref_mismatch`
and does not provide the required host headers/source. This is an external
provisioning prerequisite, not a passing result or evidence of a source
failure.

## Security impact

The delivered Parent controls close configuration-to-sink remote-rule loading,
block unauthenticated public HTTP authorization binds, remove ambiguous
duplicate security-header and Content-Length paths, reject silent authorization
Host fallback, and protect the final event-file and JSONL boundaries. Existing
request/header/body limits, phase validation, payload-free event JSONL, local
rules, and deterministic cleanup controls are not relaxed.

The current extension also makes HTX reject unenactable disruptive outcomes and
request-body finalization failures instead of treating them as observer-only,
requires Traefik Native authority before engine allocation, and prevents the
shared generic mapper from using a server endpoint as an absent client host.

This is hardening based on source-to-sink evidence. It is not a claim that a
remote deployment was reachable or that every HAProxy, HTTP/2, HTTP/3, UDS, or
host-specific runtime behavior has been dynamically proven safe.

## Runtime evidence

The HTTP smoke uses local loopback listeners and a focused fake Runtime. It
demonstrates bounded admission, cancellation, timeout, recovery, and shutdown
paths for the shared HTTP helper. The bounded fuzzer covers the Common HTTP
header parser. The current extension also starts only an isolated native
Traefik UDS engine service with local cached libmodsecurity artifacts; it is
not a Traefik host-runtime test. No native Apache, NGINX, HAProxy, Envoy,
Traefik-host, or lighttpd host process was started, and no external network or
dependency download was performed.

## Known limitations

- The direct NGINX `tar` invocation and the transitive shared archive helper
  are Framework-owned. Their lack of proof for all requested member-count,
  byte-size, link, device, and traversal controls remains out of scope for the
  Parent-only change.
- Envoy ext_proc admission is now finite and race-tested, but a single admitted
  `Recv` still has no independent application-level idle deadline; the limits
  cap resource admission but do not prove every stalled-client recovery path.
- Full native-host, HTTP/2/HTTP/3, reload, cross-connector parallel, leak,
  and ThreadSanitizer matrices have no safe available target in this checkout.
- No running HAProxy host fixture is available to inject an unsupported
  disruptive decision or request-EOS error and prove that its backend is not
  reached; the retained HTX proof is therefore source-contract plus overlay
  validation.
- HAProxy native C17 compilation is blocked before compilation by the pinned
  provisioning provenance mismatch; the changed standalone mapper compiles,
  but a complete host build and missing-Host request remain unrun.
- No live Traefik UDS or lighttpd/Envoy generic-mapper host matrix was run for
  a deliberately missing authority. The Traefik package test proves rejection
  before engine opening; other generic consumers retain their explicit local
  contracts.
- The controlled deferred-worker test uses a fake Runtime and does not prove a
  true libmodsecurity hang or host-supervisor reload behavior.
- The UTF-8 smoke covers invalid and valid UTF-8, embedded NUL in the bounded
  escaper, and representative URI/protocol fields. It is not an exhaustive
  native-host field matrix or maximum-escape-expansion proof.
- Traefik's operator-facing and connector documentation now state that only
  UDS is accepted in production; the prior source-only `passthrough` wording
  was removed without changing CI-owned generators or workflow files.

## Remaining risks

Operators using remote rules must migrate to inline or local file rules; a
configuration with either remote-rule field fails deterministically rather
than falling back. A future secure remote-loading feature requires a separately
reviewed HTTPS/origin/integrity/timeout/size/atomic-activation design.

NGINX temporary-body-file type/no-follow enforcement under a hostile
NGINX-controlled temporary path, Envoy ext_proc stalled admitted streams,
Traefik Native UDS peer identity, and host-specific lifecycle behavior remain
plausible candidates pending native, isolated runtime evidence. No confirmed
high- or critical-impact finding is silently treated as resolved: the separate
`FND-PARENT-0222` (P0/high) remains a release blocker with source-level
correction but no real NGINX/libmodsecurity host proof. It is not part of this
Common follow-up's staged delivery.

## Checks not run and rationale

No Framework archive test or Framework source change was run because current
authorization permits Parent-only changes and Framework write/test work still
requires explicit repository selection. No native host matrix, external remote
fetch, dependency installation, or hosted CI/governance operation was run.
Focused local targets reuse repository scripts stored under `ci/`, but none of
those files was changed. The legacy `ci/` helper assertion is reported as
failed rather than changed. `check-doc-links` is blocked by the unavailable
Framework submodule and is not counted as a passing check.

## Final diff and review status

The initial scoped Parent commit is
`4fa010412bfc7510da4ca787d9d923b9e8cad018` and the delivery-status
documentation commit is `7367187de072a86cfb5314740f8e47870c530e39`. The
Common re-audit follow-up is committed locally as
`16a4a06fbf1e1ed20171bc29d31ce3e8476aa3db`, followed by the narrow Host-
fallback fix `1de8071aa92cc72cadcc90a0e49f39e27e9ceba6`. Its independent,
sealed security diff review reports zero reportable findings in
`6c75b136..1de8071aa92cc72cadcc90a0e49f39e27e9ceba6`, with partial coverage
explicitly limited to the unavailable native host matrix. `CAND-AUTH-HOST-001`
is resolved as local record `FND-PARENT-0900`: missing, empty, or oversized
Host values no longer select the listener address, and the strengthened local
smoke observes missing and boundary-sized Host rejection before mapper or fake
Runtime entry. The current native-boundary extension, including
`FND-PARENT-0912` through `FND-PARENT-0922`, remains uncommitted pending a
fresh final scoped security-diff review; no older zero-finding conclusion is
carried forward to it. `FND-CROSS-0011` records the separately governed,
blocked Framework NGINX archive path. The generated Traefik default-document
drift is tracked separately because its generator is in the excluded CI scope.
Remote publication, commit, and PR creation await a current explicit user
authorization. Only exact task-owned Parent files would be staged. No merge is
authorized or asserted.

## Endpoint and NGINX post-fix reconciliation — 2026-08-25

`FND-PARENT-0926` and `FND-PARENT-0927` are local Parent findings with the
status `fixed`, not host-runtime verified or closed. The first removes the
Common/HAProxy practice of fabricating absent endpoint metadata before the
ModSecurity connection phase. Common now requires bounded client and server
endpoints; the HAProxy HTX filter derives them from the active frontend stream
or fails closed, preserving a valid UNIX endpoint rather than replacing it
with an invented IP or nominal port. The second makes an NGINX Common mapper
failure return `NGX_HTTP_BAD_REQUEST` before hostname, connection, URI, or raw
request-header processing.

The focused post-fix command covering the HTX, endpoint, HAProxy header, and
NGINX contracts passed 31 tests. `make -C connectors/haproxy
check-htx-overlay` and `git diff --check` also passed. An isolated HAProxy
3.2.22 overlay build compiled and linked the final endpoint-capture source.
`make check-nginx-c17` was blocked before compilation because the required
NGINX headers/source are unavailable; it is not recorded as a native NGINX
build pass.

The shared remote-rule policy remains deterministic policy A: nonempty
`rules_remote_key` or `rules_remote_url` is rejected before fetch. Event
correlation remains documented as process-local, non-cryptographic
correlation rather than a tamper-evident audit mechanism. The Framework-owned
direct NGINX archive extraction remains out of scope, so no archive was
created or extracted and no member-validation claim is made here.

A fresh post-fix local security-diff review of the resulting content snapshot
reported zero surviving reportable findings with partial coverage. The
canonical local scan artifacts are task-completion evidence rather than a
versioned record dependency, so this Change Record does not create a
self-referential snapshot loop. The incomplete current host/protocol/reload/
sanitizer/leak matrix, Stock-lighttpd build, and deferred source candidates
remain limitations. No workflow, governance, Framework, MRTS, commit, push,
pull request, or merge action was performed by this reconciliation.

## Final boundary reconciliation — 2026-08-25

The final Parent-only pass added four narrow, evidence-backed repairs. HAProxy
SPOP now rejects unterminated/overwide varints and typed `uint32` narrowing
(`FND-PARENT-0932`). Traefik Native UDS rejects malformed HTTP field names and
control-byte values before Common mapping (`FND-PARENT-0934`). Envoy ext_proc
serializes JSONL `Record`/`Close` file state and rejects millisecond timeouts
that cannot fit a `time.Duration` (`FND-PARENT-0935` and `FND-PARENT-0936`).
NGINX native request and response header sinks now consume the existing shared
count, name, value, and aggregate-byte limits before libmodsecurity
(`FND-PARENT-0937`). These are local `fixed` findings, not delivery-head or
native-host verification claims.

Focused validation passed: the full ext_proc Go race suite and `go vet`; the
Native Traefik package race suite and `go vet`; C17 `-Wall -Wextra -Werror`
syntax validation for the UDS service; NGINX header contracts (10 tests); the
combined 137-test local security regression suite; the Common security/flow/
adapter/directive contracts; and `make -C connectors/haproxy
check-htx-overlay`. `git diff --check` passed. Native NGINX compilation is
still blocked by unavailable headers/source, and the fully linked Traefik UDS
self-test is blocked by unresolved local `libxml2` symbols; neither is counted
as a passing native-host result.

The final source review also records `FND-PARENT-0938` as a `deferred`
candidate, not a confirmed vulnerability: if a HAProxy upstream emits final
response headers before request EOS, the source contains a possible path that
later disables normal response Phase 3/4 inspection. Payload-before-header and
disruptive request-body branches are fail-closed. A pinned HAProxy 3.2.22
partial-request/early-response fixture must establish callback and forwarding
order before any remediation or bypass claim.

Remote rules remain uniform Policy A: nonempty remote fields are rejected
before a fetch, so no origin, secret-forwarding, partial-download, or atomic
activation claim is made. The event hash remains documented only as local,
non-cryptographic correlation. Framework-owned direct NGINX archive extraction
remains outside this Parent-only authority; no archive was created or extracted
and no member-validation control is claimed. CI/governance files remain
unchanged. Full current H1/H2/H3, reload, leak, sanitizer, stock-lighttpd, and
ten-host runtime evidence remains incomplete.

## Current native Traefik UDS deadline revalidation — 2026-08-25

`FND-PARENT-0242` is fixed in this task worktree rather than only in historical
unmerged evidence. The native Traefik UDS response-frame sink uses a single
monotonic deadline, bounded `poll(POLLOUT)`, and nonblocking writes; expiry
ends only the non-reading peer and releases its worker slot. The versioned,
bounded regression holds 64 UDS peers that do not read, then proves that a
subsequent readable peer completes after the deadline. The C17 syntax check,
shell check, 133-test Parent contract suite, native service target, and the
same native service target under Clang ASan/UBSan with leak detection passed.
These are local connector/service controls, not a Traefik host-runtime,
ThreadSanitizer, or independent file-descriptor-leak proof.

Documentation was reconciled to source policy: native NGINX
`modsecurity_phase4_log` is registered but fails closed because it cannot meet
the Common event-file descriptor contract; active examples and the smoke
template no longer present it as usable. Apache/NGINX/lighttpd references now
state uniform remote-rule Policy A, where nonempty remote fields are rejected
before any loader or network action. Traefik Native documentation now states
that `uds` is the only accepted default/mode. `git diff --check` and the
focused NGINX/Traefik contracts passed after this reconciliation.

The full ten-connector host/protocol/reload/concurrency matrix remains blocked
by the absent Framework runtime and host prerequisites. In particular, the
Framework-owned direct NGINX archive extraction path (`FND-CROSS-0011`) was
not changed or exercised, and the deferred HTX early-response candidate
(`FND-PARENT-0938`) remains neither confirmed nor fixed. No delivery authority
or delivery action is changed by this local revalidation.

## Current local verification result — 2026-08-25

The Envoy ext_proc and Traefik Native Go packages passed `go test -race` and
`go vet` with module resolution disabled from the network. The Common memory
safety smoke passed, and the Common HTTP authorization timeout/admission smoke
passed under both Clang ASan/UBSan with leak detection and Clang TSan. Its
intentional malformed, timeout, overload, abrupt-disconnect, and stalled-peer
controls emitted expected fail-closed messages without a sanitizer diagnostic.

`check-common-security-contract`, `check-common-flow-integrity`,
`check-adapter-contracts`, and `check-directive-parity` passed. The separate
`check-common-sdk-contract` remains failed because its existing static policy
rejects the server-specific token `envoy` in `common/include/msconnector/limits.h`
for lacking non-integration context. That checker/policy is not changed in this
Parent connector-hardening scope; the failure is recorded rather than masked.

## NGINX Phase-4 content-type configuration boundary — 2026-08-25

`FND-PARENT-0940` is a local `fixed` security-hardening record. The native
`modsecurity_phase4_content_types_file` loader formerly trusted a pathname
`stat()` size before allocation and opened the path only later. It now opens
with `NGX_FILE_NONBLOCK`, inspects the opened descriptor with `ngx_fd_info`,
requires a regular file, enforces a 64 KiB cap before pool allocation, and
rejects a short read. This closes the source-level unbounded allocation and
non-regular-file read path; it does not claim a remote request vulnerability.

The focused NGINX contract/configuration suite passed 9 tests, and the changed
module compiled with the configured NGINX 1.31.4 host headers and `-Werror`.
This supersedes only the earlier “headers/source unavailable” statement for
this isolated C compile. An exact-worktree `nginx -t` fixture for bounded
regular-file, FIFO, directory, oversized-file, and concurrent-replacement
controls was not available, so the finding remains `fixed`, not `verified` or
closed. No CI/governance, Framework, MRTS, commit, push, pull-request, or merge
action was performed.

A cross-platform source review added an explicit Win32 fail-closed branch:
Win32 NGINX exposes neither the POSIX regular-file distinction needed here nor
a nonblocking file-open flag, so this optional local-file directive is rejected
there rather than presenting a weaker special-file contract. The POSIX compile
and static contract remain the actual executed evidence; no Win32 build/runtime
claim is made.
## Envoy ext_proc process-wide active-stream containment — 2026-08-25

`FND-PARENT-0943` records a local `fixed`, not `verified`, Envoy ext_proc
remediation. The retained historical four-stream idle observation proved
resource retention beyond `engine_timeout_ms=150`; source review confirmed that
`grpc.MaxConcurrentStreams(128)` is per transport. The service now takes one
non-blocking process-wide slot before `streamState` construction or
`TransactionOpener.Open`, returns gRPC `ResourceExhausted` on saturation, and
defers one release for every accepted normal, EOF, cancellation, or processor-
error exit. The gRPC transport setting uses the same
`DefaultMaxActiveStreams` constant.

The current task worktree passed `go test -count=1 ./...`, `go test -count=1
-race ./...`, `go vet ./...`, and the 19-test
`tests.test_envoy_transport_hardening_contract` selection; the retained
payload-free receipt is
`.codex/runs/20260825T122012Z-envoy-active-stream-capacity/evidence/validation.md`
with SHA-256
`b246d933156ce602f928b5f81fc0078ffe2c28e586db72aafaaac72951197bd2`.
The capacity-one regression proves that an excess stream is rejected before a
second transaction opens and that a post-EOF legitimate stream is admitted.

The aggregate cap is deliberately not documented as an idle deadline: one
admitted valid stream may still wait for an Envoy message, EOF, or context
cancellation. No linked Common/libmodsecurity and real-Envoy multi-transport
saturation, reload-under-load, leak/descriptor, exact delivery-head, commit,
push, pull-request, or merge result is claimed.

## Common and Apache private event-file descriptor parity — 2026-08-25

`FND-PARENT-0223` remains locally `fixed`. Its former equivalent Common Runtime
and Apache path walks are now one Common API:
`msconnector_open_private_event_file`. On supported POSIX targets it walks each
configured component with `openat` and `O_DIRECTORY|O_NOFOLLOW`, opens the
final sink with `O_NOFOLLOW|O_APPEND|O_CREAT|O_NONBLOCK`, rejects a nonregular
or differently owned final object and a group/world-writable final parent,
repairs an accepted existing file to `0600`, and preserves close-on-exec even
when `O_CLOEXEC` is absent. Common Runtime converts the checked descriptor to
its `FILE *`; Apache transfers it to APR only after the Common check.

The bounded synthetic regression passed a private regular file, existing-file
mode repair, close-on-exec, final and ancestor symlinks, FIFO, directory,
traversal, and group-writable-parent controls in normal mode and under Clang
ASan/UBSan with leak detection. Focused Common/Apache/NGINX source contracts
(16 tests), C17 Common Runtime/Apache syntax checks, the UTF-8 JSONL smoke,
and `git diff --check` passed. The NGINX native phase-4 file directive remains
disabled before descriptor creation: a proposal to re-enable it was not applied
because its inherited-descriptor/reload lifecycle is a separately authorization-
requiring behavior change. No NGINX host runtime, Apache host runtime, Windows
build, CI/governance file, Framework/MRTS file, or delivery action is claimed.

## Delivery preparation — 2026-08-25

The current user explicitly authorized one Parent commit, push, and Draft PR
for this existing task-owned branch. The task does not authorize a merge,
default-branch push, history rewrite, Framework/MRTS change, Gitlink update,
or CI/governance modification. The branch and every PR head remain subject to
the verified `origin` destination, exact-SHA readback, and ordinary GitHub
checks. Actual PR number, URL, branch SHA, check states, and review status are
recorded only after observation in the PR and the task delivery evidence; this
Change Record does not preclaim them.

## PR #345 Sonar and workflow remediation — 2026-09-03

The task branch was forward-merged with the then-current `origin/master`
before this remediation; it retains that master integration and does not
rewrite history. This extension remediates current task-owned Sonar and
workflow feedback through source, test, and documentation changes only. It
does not modify `.github/workflows/`, branch protection, rulesets, required
checks, Sonar rules, Quality Gate configuration, exclusions, suppressions, or
coverage thresholds.

Two independently reproduced HAProxy SPOE/SPOP paths are corrected. First,
legitimate typed IPv4/IPv6 `src`/`dst` metadata is bounded, type-checked, and
canonically formatted before Common mapping; unsupported, truncated, and
trailing forms remain rejected. Second, missing required endpoints are now a
synchronous admission failure before owner-task allocation or queueing. It
therefore returns a disruptive `deny`/503 and `blocked=true` ACK for both
`fail-mode=open` and `closed`; the equivalent worker-side check remains as
defense in depth. No loopback, Host, or endpoint fallback was added. These are
tracked separately as FND-PARENT-1020 and FND-PARENT-1021 rather than as
duplicate findings.

The Common remote-rule helper now tests the existing uniform Policy A
correctly: any nonempty remote configuration is rejected before mutation or a
network-capable sink. Common event JSONL/event-file code, Apache, NGINX,
HAProxy binding/mapper/HTX, Envoy ext_proc, and Traefik Native changes reduce
Sonar complexity or duplication without changing their security contracts.
Refactor-sensitive HAProxy and HTTP-worker contract tests were moved to the
new helper boundaries only after source-to-sink review confirmed that mapper,
FIN, Host, allocation, body, and fail-closed ordering controls remained in
place. The German Traefik Native README duplicate was removed; its content
remains aligned with the English README.

Local validation passed: Common C17 helper, security/flow/adapter, and HTTP
timeout/admission/cancel checks; the detached-worker C17, ASan/UBSan with leak
detection, and TSan smoke; private-event C17, ASan/UBSan, GCC analyzer, and
Valgrind checks; Apache C17; Apache/NGINX/HTX and HAProxy contracts; HAProxy
SPOP protocol self-test; and Envoy ext_proc plus Traefik Native formatting,
vet, tests, and Go race checks. The exact hosted HAProxy CRS/no-MRTS control,
native NGINX host build/runtime, and full H1/H2/H3/reload matrix remain
blocked by unavailable Framework/host artifacts and are not represented as
passing. The PR's exact-SHA GitHub Actions and SonarQube Cloud result are
verified separately after delivery; this record does not preclaim them.
