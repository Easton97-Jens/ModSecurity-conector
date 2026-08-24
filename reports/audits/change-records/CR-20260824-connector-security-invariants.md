# Change Record

**Language:** English | [Deutsch](CR-20260824-connector-security-invariants.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260824-connector-security-invariants |
| Date (UTC) | 2026-08-24 |
| Base revision | a6b4ced4876a19666f7c7203ed9e719674c69ec1 |
| Repository boundary | Parent only; Framework, MRTS, Gitlink, CI, and governance unchanged |
| Delivery authority | Local Parent commit only; remote push and Draft PR pending explicit current-user authorization; no merge |

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
repository. The current user limited implementation to Parent fixes, so that
path is reported as an out-of-scope remediation dependency rather than patched
or represented as safely extracted here.

## Acceptance criteria

- Every reviewed Parent remote-rule entry point rejects both complete and
  incomplete remote-rule configuration before a network-capable sink.
- Apache, NGINX, and Common Runtime do not retain a productive
  `msc_rules_add_remote` path; all connector capability records describe the
  same policy.
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
  cleanup and a bounded fully owned profile for an uninterruptible detached
  worker.
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
- `examples/common/common-connector-configuration.{md,de.md}` and the Apache/
  NGINX README pairs — documented finite limits and phase-4 configuration cap.
- This English/German Change Record pair and the paired archive index entries.

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
rtk proxy env BUILD_ROOT=<external-task-root>/docs make check-doc-links
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
check, listed Common contracts, and repository-path/document-link checks passed.

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
~~~

`check-common-helpers` compiled then failed its existing assertion that a
complete remote-rule pair validates. Its test implementation is under `ci/`,
which the current request explicitly excludes; no policy or test weakening was
made. The TSan binary built and exercised loopback cases but the command
wrapper returned no terminal exit status or completion marker in two attempts.
It is inconclusive, not a pass. The bilingual checker likewise produced no
terminal exit status or completion marker through the command wrapper within
30 seconds; required Change-Record headings and English/German parity were
reviewed manually, but its automated result is inconclusive rather than passed.

## Security impact

The delivered Parent controls close configuration-to-sink remote-rule loading,
block unauthenticated public HTTP authorization binds, remove ambiguous
duplicate security-header and Content-Length paths, reject silent authorization
Host fallback, and protect the final event-file and JSONL boundaries. Existing
request/header/body limits, phase validation, payload-free event JSONL, local
rules, and deterministic cleanup controls are not relaxed.

This is hardening based on source-to-sink evidence. It is not a claim that a
remote deployment was reachable or that every HAProxy, HTTP/2, HTTP/3, UDS, or
host-specific runtime behavior has been dynamically proven safe.

## Runtime evidence

The HTTP smoke uses local loopback listeners and a focused fake Runtime. It
demonstrates bounded admission, cancellation, timeout, recovery, and shutdown
paths for the shared HTTP helper. The bounded fuzzer covers the Common HTTP
header parser. No native Apache, NGINX, HAProxy, Envoy, Traefik, or lighttpd
host process was started, and no external network or dependency download was
performed.

## Known limitations

- The direct NGINX `tar` invocation and the transitive shared archive helper
  are Framework-owned. Their lack of proof for all requested member-count,
  byte-size, link, device, and traversal controls remains out of scope for the
  Parent-only change.
- A concurrently modified Envoy ext_proc idle-timeout/admission implementation
  remains unstaged. Its focused Go race run fails
  `TestStreamIdleTimeoutCleansUpAndAllowsFollowUpStream`; it is neither
  attributed to nor delivered by this change.
- Full native-host, HTTP/2/HTTP/3, reload, cross-connector parallel, leak,
  and ThreadSanitizer matrices have no safe available target in this checkout.
- The controlled deferred-worker test uses a fake Runtime and does not prove a
  true libmodsecurity hang or host-supervisor reload behavior.
- The UTF-8 smoke covers invalid and valid UTF-8, embedded NUL in the bounded
  escaper, and representative URI/protocol fields. It is not an exhaustive
  native-host field matrix or maximum-escape-expansion proof.

## Remaining risks

Operators using remote rules must migrate to inline or local file rules; a
configuration with either remote-rule field fails deterministically rather
than falling back. A future secure remote-loading feature requires a separately
reviewed HTTPS/origin/integrity/timeout/size/atomic-activation design.

HAProxy HTX late response inspection, SPOP framing/cache/timeout behavior,
Traefik Native UDS peer identity, and host-specific lifecycle behavior remain
plausible candidates pending native, isolated runtime evidence. No confirmed
high- or critical-impact finding is silently treated as resolved: the separate
`FND-PARENT-0222` NGINX P0/high P2/P3 finding remains a release blocker with
source-level correction but no real NGINX/libmodsecurity host proof. It is not
part of this Common follow-up's staged delivery.

## Checks not run and rationale

No Framework archive test or Framework source change was run because the user
explicitly limited implementation to Parent. No native host matrix, external
remote fetch, dependency installation, or hosted CI/governance operation was
run. Focused local targets reuse repository scripts stored under `ci/`, but
none of those files was changed. The legacy `ci/` helper assertion is reported
as failed rather than changed.

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
Runtime entry. Remote publication and Draft-PR creation await a new explicit
current-user authorization. The active checkout also contains unrelated and
mixed concurrent edits; they are excluded from staging. No merge is authorized
or asserted.
