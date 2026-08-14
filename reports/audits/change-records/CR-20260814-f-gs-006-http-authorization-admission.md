# Change Record

**Language:** English | [Deutsch](CR-20260814-f-gs-006-http-authorization-admission.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260814-f-gs-006-http-authorization-admission |
| Date (UTC) | 2026-08-14 |
| Base revision | ea3b48abab7940de49997a371f9117b409c05a2a |
| Related finding | F-GS-006 (<code>partially_fixed</code>) |
| HTTP sub-status | <code>hardening_applied_locally_verified</code> |
| Repository boundary | Parent only; Framework and MRTS unchanged |
| Delivery authority | Scoped commit, push, and Draft PR only; no merge or ready-for-review action |

## Motivation and problem statement

The shared HTTP/1.1 authorization service accepted a connection and then read,
mapped, evaluated, responded to, and closed it in the listener loop. An
incomplete client could therefore delay a later valid client until the first
client's absolute read deadline. The service also had no explicit bounded
connection-admission policy.

F-GS-006 also records candidate Event/Rule/remote-origin and Traefik UDS
identity concerns. Repository evidence does not establish a compatible
configuration/path/origin contract for the former or a live peer-identity and
restart contract for the latter. Neither receives a speculative code change in
this record.

## Acceptance criteria

- <code>--max-connections</code> defaults to <code>8</code> and accepts only <code>1</code> through <code>64</code>.
- Empty, negative, zero, overflow, trailing-character, and over-limit capacity
  values are rejected by the existing numeric parser contract.
- One incomplete loopback client does not serially delay a concurrent valid
  client, and a full admission bound closes a later accepted connection.
- Default-eight saturation is bounded and a valid client is served after a slot
  is released.
- Detached-worker metadata and active-worker accounting remain bounded for the
  process lifetime; workers drain before Runtime destruction.
- Worker shutdown interrupts blocked socket I/O without taking final close
  ownership away from the worker.
- The shared Runtime is serialized only during request mapping and Runtime
  transaction work, not during socket reads or response writes.
- Direct Smoke, Envoy, Envoy ext_proc, and Traefik C build paths carry pthread
  compile/link support where they compile or link this code.

## Implementation decision and rationale

### Technical decisions

<code>common/runtime/http_authorization_service.c</code> snapshots request limits during
startup and admits at most the configured number of detached workers. A worker
is placed on the service-owned list before it starts and removes itself exactly
once while decrementing the active-worker count under the worker mutex.
Consequently, completed joinable-thread handles and worker metadata do not
accumulate. A condition variable waits for active workers to reach zero before
the Runtime is destroyed.

The listener immediately closes an accepted socket when no admission slot is
available; it does not create a user-space queue. If worker allocation,
attribute setup, or thread creation fails, the same release path removes the
worker metadata and closes the accepted FD. Shutdown holds the worker-list
mutex only while calling <code>shutdown(fd, SHUT_RDWR)</code>. The worker remains the
unique owner of final <code>close(fd)</code>, which avoids a shutdown-side FD-reuse or
double-close race.

Socket reads occur before the Runtime mutex, and responses are written after it
is released. Request mapping, transaction begin, finish, destruction, and the
copy of the transaction identifier are serialized by a service-local Runtime
mutex because the Common Runtime holds mutable shared engine, event, and
transaction state. No path holds the worker-list mutex while it acquires the
Runtime mutex.

The <code>--listen</code> option remains explicit: there is no implicit bind default.
<code>127.0.0.1</code> and <code>localhost</code> resolve to the loopback use case; <code>0.0.0.0</code>
remains an explicitly selected, compatible binding. The
<code>--max-connections</code> default is <code>8</code>, the maximum is <code>64</code>, and the existing
maximum connection timeout remains 600000 ms.

The focused smoke adds deterministic default-eight saturation and recovery,
bounded sequential and complete-parallel requests, abrupt disconnect, blocked
read shutdown, and capacity-parser boundary cases. A pthread-creation fault was
not injected: the current repository-native design has no proportional fault
injection seam, and adding one solely for this case would be a wider test
abstraction change. The source error path is instead reviewed and covered by
the bounded release design.

## Changed files

- <code>common/runtime/http_authorization_service.c</code> — bounded admission, detached
  worker lifecycle, FD ownership, shutdown drain, and narrow Runtime locking.
- <code>ci/checks/common/http_authorization_service_timeout_smoke.c</code> —
  deterministic admission, parser, lifecycle, recovery, disconnect, and
  shutdown coverage.
- <code>ci/checks/common/check-http-authorization-service-timeout.sh</code> —
  pthread compile/link support for the focused helper.
- <code>connectors/envoy/build/build_connector.sh</code> — pthread compile and link
  support for the Envoy ext_authz build path.
- <code>connectors/envoy/build/build_ext_proc.sh</code> — pthread compile support for
  the Common archive used by Envoy ext_proc; its cgo link flags already include it.
- <code>connectors/traefik/build/build-connector.sh</code> — pthread compile support;
  its existing link path already includes it.
- <code>docs/operations-and-security.md</code> and
  <code>docs/operations-and-security.de.md</code> — operator-facing admission, bound,
  and external-bind limitations.
- This English/German Change Record pair and paired archive-index entries —
  scoped traceability, actual validation state, and sanitised follow-ups.

No Event/Rule/remote-origin source, Traefik UDS client source, Go module or
toolchain file, Framework, MRTS, Gitlink, dependency, or workflow is changed.
Local task plans, external build output, and cleanup metadata are not versioned
product artifacts.

## Commands executed

The portable <code>&lt;external-task-build-root&gt;</code> placeholder denotes the external,
task-owned build root used for the observed commands. Repository paths remain
relative.

### PASS

~~~text
rtk proxy env CC=gcc 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror' BUILD_ROOT=<external-task-build-root>/gcc-c17 make check-http-authorization-service-timeout
rtk proxy env CC=clang 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror' BUILD_ROOT=<external-task-build-root>/clang-c17 make check-http-authorization-service-timeout
rtk proxy env CC=clang ASAN_OPTIONS=detect_leaks=1:halt_on_error 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=address -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/asan make check-http-authorization-service-timeout
rtk proxy env CC=clang UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=undefined -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/ubsan make check-http-authorization-service-timeout
rtk proxy env CC=clang TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1 'MSCONNECTOR_CFLAGS=-std=c17 -Wall -Wextra -Werror -fsanitize=thread -fno-omit-frame-pointer' BUILD_ROOT=<external-task-build-root>/tsan make check-http-authorization-service-timeout
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/parent-checks make check-common-sdk-contract check-common-security-contract check-common-helpers check-common-flow-integrity check-adapter-contracts check-remaining-connectors-common-adoption check-remaining-connectors-build-wiring check-remaining-connectors-c-standard-wiring
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/c17-checks make check-remaining-connectors-c17-lint check-remaining-connectors-c17
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/common-memory make check-common-memory-safety
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/docs make check-connector-guides
rtk proxy jq -e 'type == "object"' connectors/envoy/SOURCE_MAP.json
rtk proxy jq -e 'type == "object"' connectors/traefik/SOURCE_MAP.json
rtk proxy git diff --check
~~~

Each focused smoke completed the added parser, admission, recovery, sequential,
parallel, abrupt-disconnect, and blocked-read-shutdown cases. AddressSanitizer,
UndefinedBehaviorSanitizer, and ThreadSanitizer produced no diagnostic. The
Common/connector contracts and C17 wiring checks passed. No versioned JSON file
changed; the relevant connector JSON objects parsed successfully.

### Historical pre-fix evidence

~~~text
rtk proxy env BUILD_ROOT=<external-pre-fix-build-root> make check-http-authorization-service-timeout
~~~

This isolated earlier run failed as expected with
<code>parallel_request: valid peer waited for the stalled peer deadline</code>. It is not
recompiled with the expanded current smoke against the base revision because
that smoke now exercises <code>--max-connections</code>, which does not exist in the
pre-fix source.

### UNKNOWN / blocked

~~~text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 BUILD_ROOT=<external-task-build-root>/docs make check-bilingual-docs
rtk proxy env PYTHONDONTWRITEBYTECODE=1 <repository-python> ci/checks/documentation/check-repository-path-references.py
rtk proxy env GOTOOLCHAIN=local GOPROXY=off GOWORK=off GOCACHE=<external-task-build-root>/go-cache make -C connectors/traefik test-native-middleware
~~~

The two documentation commands report only pre-existing missing links under
<code>modules/ModSecurity-test-Framework/</code>; the clean task worktree has the
uninitialized Framework gitlink and this task neither initializes nor changes
that separate repository. They are therefore <code>UNKNOWN</code>, not evidence against
the changed HTTP documentation.

The Traefik command is <code>UNKNOWN (blocked_environment)</code> with the exact error:
<code>go: go.mod requires go &gt;= 1.26.5 (running go 1.26.0; GOTOOLCHAIN=local)</code>.
The installed Go toolchain is 1.26.0 while the module requires Go 1.26.5. With
<code>GOTOOLCHAIN=local</code>, validation cannot proceed; enabling automatic toolchain
download is prohibited for this task.

## Security impact

The closed invariant is deliberately narrow: **one slow or incomplete client
no longer serially blocks every subsequent client, and concurrent connection
handling is bounded.** It is an availability hardening for the HTTP
authorization boundary, not a claim that every denial-of-service condition is
eliminated.

F-GS-006 remains <code>partially_fixed</code>. Event/rule/remote inputs remain
<code>unproven</code>, and the Traefik UDS client remains
<code>blocked_missing_evidence</code>.

## Runtime evidence

All executed HTTP evidence uses a local loopback listener and a fake Common
Runtime. It demonstrates the narrow admission and lifecycle invariants, not a
real Envoy or Traefik host integration, libmodsecurity production behavior,
external-network behavior, or delivery status. The repository has no installed
Envoy or Traefik host binary, and <code>pkg-config</code> has no <code>libmodsecurity</code>
package entry; no host runtime or dependency download was attempted.

## Known limitations

The Runtime evaluation itself remains serialized for Common Runtime thread
safety. A slow Runtime transaction can therefore limit throughput even though
socket reads and writes overlap. The test is intentionally bounded and local;
it is not a production stress test. No pthread-creation fault injection was
added for the stated repository-native testability reason.

## Remaining risks

Eight slow clients can exhaust the default eight admission slots, and up to 64
slow clients can exhaust a configured maximum until their absolute deadline;
the maximum permitted timeout is 600000 ms. The service provides no built-in
fairness, rate limiting, TLS, or client authentication. Explicit <code>0.0.0.0</code>
binding remains a host-level exposure decision that needs appropriate network
controls and an authenticated protective layer. No risk is accepted.

## Checks not run and rationale

Real Envoy and Traefik host-runtime tests were not run because the required
host binaries and complete configured prerequisites are not present; downloading
or provisioning them is outside this task. No production, external-network,
Framework, MRTS, merge, ready-for-review, resulting-master, or hosted-CI
validation is asserted.

## Sanitised follow-up drafts

The repository is public and its security policy does not permit public issues
for suspected security concerns. No issue was created. The following
issue-ready design/hardening drafts are retained for the Draft PR without
unnecessary attack-path detail.

### Define the security contract for event/rule paths and remote rule origins

**Product decisions needed:** identify who may set <code>event_path</code>, local rule
paths, and remote rule URLs; define supported absolute and relative paths,
authoritative base roots, parent-directory ownership, and symlink/replacement
semantics; define permitted URL schemes, redirect, TLS, DNS/internal-target,
origin-allowlist, pinning/checksum, and failure behavior; state the operator
status and provenance requirements for remote rules.

**Acceptance criteria:** publish one explicit code and bilingual documentation
contract; add positive and negative containment, object-type, ownership,
replacement, and remote-provenance tests; do not promote the path or remote
input boundary before those focused tests demonstrate the contract.

### Define and verify Traefik UDS peer identity

**Product decisions needed:** define the expected server UID/GID and whether a
same-UID adversary is in scope; choose supported Linux <code>SO_PEERCRED</code> behavior
or an equivalent identity mechanism, with secure fail-closed behavior on other
platforms; define restart/rebind, container, mount, and namespace semantics;
evaluate descriptor handoff or a long-lived verified connection; require an
actual Traefik-host integration fixture.

**Acceptance criteria:** bind identity to every accepted client-to-engine
session; make identity mismatch, restart replacement, and unsupported-platform
handling deterministic and fail closed where applicable; add focused tests and
bilingual documentation. This design follow-up is separate from the internal
UDS evidence record and has no source patch here.

## Final diff and review status

The scoped patch contains only the HTTP authorization admission hardening, its
tests, direct build wiring, paired operations documentation, and paired Change
Record/index. F-GS-006 remains an intentionally partial remediation; no
whole-finding completion is claimed. A narrow commit, push, and Draft PR are
authorized after final staged-diff review; the exact commit, PR, and one-time
hosted-check snapshot are recorded in delivery metadata rather than creating a
self-referential commit loop in this record.
