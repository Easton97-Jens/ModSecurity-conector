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
wildcard listener and duplicate security-sensitive headers; and Common event
output could serialize unescaped protocol metadata and open an unsafe final
event path.

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
  and rejects duplicate `Host` and configured original-URI headers before
  transaction mapping.
- Event metadata remains payload-free JSONL, is escaped and NULL-safe, and the
  POSIX final event file is no-follow, regular, and private (`0600`).
- The FNV-derived event chain is documented only as process-local,
  non-cryptographic correlation; it is not described as tamper evidence.
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
mapping. The existing bounded worker admission and shutdown ownership model is
preserved; shutdown returns a defined failure rather than destroying Runtime
objects still held by an uninterruptible worker.

Event protocol text is escaped with the shared JSON escaper. The POSIX event
sink is opened with `O_NOFOLLOW`, verified as a regular file, restricted with
`fchmod(0600)`, and then converted to a stream. Windows has no equivalent
reparse-point control in this implementation and therefore fails closed instead
of opening a configured event path. The change intentionally does not claim
cross-process tamper resistance.

The Common Content-Length parser now rejects every duplicate value, including
identical duplicates. This avoids relying on different host normalization rules
at a request-smuggling-sensitive translation boundary.

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
  duplicate security-header rejection, signal-safe send, and bounded shutdown
  behavior.
- `common/src/event.c`, `common/include/msconnector/event.h`, and
  `common/include/msconnector/integrity_event.h` — escaped/null-safe event
  metadata, safe correlation semantics, and event-sink invariant.
- `connectors/{apache,nginx}/README.md` and `.de.md` — remote-rule behavior.
- `connectors/{apache,nginx,envoy,haproxy,lighttpd,traefik}/capabilities.json`
  — one consistent remote-rule capability statement.
- `tests/test_remote_rules_disabled.py`,
  `tests/test_http_authorization_service_security_contract.py`, and
  `tests/test_event_runtime_security_contract.py` — focused regression
  contracts.
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
~~~

The focused Python suite passed 11 tests. The loopback timeout/admission smoke
passed in normal, ASan-with-leak-detection, and UBSan configurations. The
memory-safety target passed its normal and optional ASan/UBSan smoke. The
bounded libFuzzer run completed 533086 executions in 16 seconds, with no
AddressSanitizer or UndefinedBehaviorSanitizer diagnostic. The C17 syntax
check, listed Common contracts, and repository-path/document-link checks passed.

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
duplicate security-header and Content-Length paths, and protect the final
event-file and JSONL boundaries. Existing request/header/body limits, phase validation,
payload-free event JSONL, local rules, and deterministic cleanup controls are
not relaxed.

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

## Remaining risks

Operators using remote rules must migrate to inline or local file rules; a
configuration with either remote-rule field fails deterministically rather
than falling back. A future secure remote-loading feature requires a separately
reviewed HTTPS/origin/integrity/timeout/size/atomic-activation design.

HAProxy HTX late response inspection, SPOP framing/cache/timeout behavior,
Traefik Native UDS peer identity, and host-specific lifecycle behavior remain
plausible candidates pending native, isolated runtime evidence. No confirmed
high- or critical-impact finding is left silently unresolved by this record.

## Checks not run and rationale

No Framework archive test or Framework source change was run because the user
explicitly limited implementation to Parent. No native host matrix, external
remote fetch, dependency installation, or hosted CI/governance operation was
run. Focused local targets reuse repository scripts stored under `ci/`, but
none of those files was changed. The legacy `ci/` helper assertion is reported
as failed rather than changed.

## Final diff and review status

After local commit `4fa010412bfc7510da4ca787d9d923b9e8cad018`, this remains a
Parent-only, task-owned change. Remote publication and Draft-PR creation await
a new explicit current-user authorization. The active checkout also contains
unrelated and mixed concurrent edits; they are excluded from staging. Final
scoped diff, documentation checks, exact branch/commit/remote/PR head
relationship, and hosted-check status will be reconciled only after an
authorized delivery. No merge is authorized or asserted.
