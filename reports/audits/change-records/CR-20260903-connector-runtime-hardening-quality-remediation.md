# Change Record CR-20260903-connector-runtime-hardening-quality-remediation

**Language:** English | [Deutsch](CR-20260903-connector-runtime-hardening-quality-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260903-connector-runtime-hardening-quality-remediation |
| Date (UTC) | 2026-09-03 |
| Base revision | 95bc04203455bc74a9cd18fafc6fb5848af2bbb2 (`origin/master`) |
| Delivery status | Remediation commit `d4f5674e8438d398696b1e92965d6e246618306f` is pushed on `codex/connector-runtime-hardening-20260824`; Draft PR [#346](https://github.com/Easton97-Jens/ModSecurity-conector/pull/346) remains open. The exact-head GitHub Actions checks succeeded except SonarQube Cloud; the current authority-boundary follow-up is locally validated but not yet committed or pushed. No merge is asserted. |

## Motivation and problem statement

This Parent-only remediation addresses the current PR's Codex review findings,
SonarQube Cloud Quality-Gate errors, and red connector workflow evidence for
runtime error, timeout, cancellation, protocol, and cleanup paths. The initial
hosted state contained an Apache runtime failure, a bilingual-documentation
heading failure, and a SonarQube Cloud gate error (`new_security_rating=3` and
`new_duplicated_lines_density=4.5`).

## Acceptance criteria

- Correct the identified connector runtime and cleanup defects without
  weakening fail-closed controls or changing CI/governance inputs.
- Preserve legitimate allow/block behavior and add trigger and control
  regression coverage at each changed boundary.
- Remove the identified Sonar new-code security and duplication causes without
  suppressions, exclusions, or Quality-Gate changes.
- Keep English/German reader-facing documentation and the Change Record pair
  materially equivalent.
- Obtain fresh exact-head GitHub Actions and SonarQube Cloud evidence after a
  normal push; delivery remains pending until those results exist.

## Implementation decision and rationale

The remediation corrects Apache listener-inode parsing and private artifact
handling; Common event protocol-value double escaping plus lossless JSONL and
integrity-chain handling; Traefik stable worker-slot cleanup; Lighttpd helper
artifact, endpoint, executable, and zombie-session handling; Envoy ext_proc
absolute stream lifetime, cancellation, and bounded post-send evidence after a
confirmed response at the lifetime boundary; and the two bilingual heading
hierarchies.

For HAProxy SPOE/SPOP, the remediation uses checked `MSG_NOSIGNAL` full-write
paths, terminal peer-local failure handling and rate-limited error evidence,
detached bounded peer workers, immediate close on exhausted peer admission,
strict worker/transaction limits, and fail-closed protocol outcomes. A
response NOTIFY sent while response processing is disabled produces the
documented 503 outcome before transaction processing; malformed NOTIFY and
missing response correlation remain disruptive even in `mode=detect-only`.
Valid engine Allow/Block decisions retain their configured mode semantics.
The source-backed configuration renderer now documents that
`response-body-timeout` must be zero only with `response-companion=none`.

The scope is limited to Parent source, tests, connector documentation, example
configuration, and this record. It includes no CI workflow, permission,
branch-protection, ruleset, required-check, Framework, MRTS, Gitlink, direct
`master`, or merge change. Current `master` remains the authoritative base.

## Security impact

The affected security boundaries include untrusted network peers,
request/response streams, subprocess and artifact paths, Unix/TCP endpoints,
protocol parsers, and concurrent transaction state. The implementation adds
bounded path and endpoint checks, stable cleanup ownership, cancellation
propagation, absolute stream lifetime, and single-pass event encoding while
retaining existing authorization decisions. An independent post-fix review
found an Apache `/proc/net/tcp` token-index defect; the parser and its
actual-layout regression fixture were corrected, and focused verification
passed. The final independent review then found three active Envoy service
configurations missing the new mandatory stream lifetime; all were corrected.
A later independent HAProxy boundary review found the response-phase,
detect-only protocol-error, and saturated-admission gaps addressed above. The
earlier combined-diff review is retained as historical evidence. A later
two-stage Apache/lighttpd boundary review found, then verified the correction
of, FIFO-before-type-check, directory-creation and artifact-parent TOCTOU,
bounded cleanup-tree, and JSON-receipt resource-limit defects. Its final
re-review found no concrete remaining bypass in the corrected boundary.

## Changed files

- `connectors/apache/harness/apache_process_guard.py`,
  `connectors/apache/harness/run_apache_smoke.sh`, and their focused tests
- Common event headers, runtime, JSON/JSONL/integrity implementation, and
  `tests/event_json_utf8_smoke.c` plus
  `tests/transaction_phase_runtime_companion_test.c`
- `connectors/traefik/src/traefik_engine_service.c` and
  `tests/test_traefik_engine_service_shutdown_contract.py`
- Lighttpd backend-close and Stock lifecycle harness source, tests, and
  English documentation
- `ci/checks/common/check-common-helpers.sh`
- Envoy ext_proc processor/configuration source, tests, English/German
  READMEs, active service configurations, and example service configurations
- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`, HAProxy example
  configurations and English/German configuration references, and
  `reports/connector-configuration-inventory.json`
- HAProxy response-timeout, transaction-cache, peer-isolation, resource-limit,
  SIGPIPE/peer-isolation, and Sonar reliability contracts
- `ci/checks/documentation/connector_config_reference.py` and
  `tests/test_connector_config_reference.py`
- `connectors/traefik/native_middleware/README.de.md`
- this English/German Change Record pair and both archive indexes

## Commands executed

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest
  tests.test_apache_process_guard
  connectors.lighttpd.tests.test_backend_close_harness_contract
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract
  tests.test_traefik_engine_service_shutdown_contract` — passed, 81 tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_haproxy_spop_response_timeout_contract
  tests.test_haproxy_spop_transaction_cache_contract
  tests.test_haproxy_spop_peer_isolation_contract
  tests.test_haproxy_spop_resource_limits_contract
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
  tests.test_sonar_reliability_contract` — passed, 34 tests.
- `rtk proxy make -C connectors/haproxy self-test-spoa-runtime` — passed;
  the selected libModSecurity headers lack the optional rule-ID API and the
  supported baseline probe was selected as designed.
- In `connectors/envoy/ext_proc`, `rtk proxy go test -count=5
  ./internal/processor`, `rtk proxy go test -race -count=1
  ./internal/processor`, `rtk proxy go test -count=1 ./...`, and `rtk proxy go
  vet ./...` — passed; deterministic controls cover successful response-CONTINUE
  and immediate-response sends at the actual stream deadline, evidence failure,
  terminal cleanup, and rejected follow-up admission.
- `rtk proxy cc -std=c17 -Wall -Wextra -Werror -Icommon/include
  tests/event_json_utf8_smoke.c common/src/*.c` followed by the smoke binary
  and `jq` decoded-value assertion — passed. Strict C17 and ASAN/UBSAN builds
  of that smoke and the real Common-runtime/libmodsecurity companion test —
  including rejection of malformed UTF-8 without an event/chain advance and a
  valid follow-up event — also passed; task-owned binaries are removed before
  delivery.
- `rtk proxy jq -e .` for the three active and four example Envoy service JSON
  files — passed.
- `rtk proxy cc -std=c17 -Wall -Wextra -Werror -fsyntax-only
  -Icommon/include -Iconnectors/haproxy/src
  connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` — passed.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_connector_config_reference` and
  `rtk proxy python3 ci/checks/documentation/check-connector-config-reference.py
  --repo-root .` — passed, 4 tests and current generated references.
- `rtk proxy git diff --check` — passed at the final local validation point.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
  tests.test_bilingual_docs tests.test_connector_config_reference` — passed,
  26 tests. At that historical validation point, the combined focused connector
  set passed 119 tests.

## Runtime evidence

No complete local real-host matrix run is asserted. The Apache hosted runtime
failure was traced to listener-inode parsing and corrected locally; exact-head
hosted workflow evidence is still required. The real Common runtime regression
proves a lossy event is neither written nor chained and that a legitimate
follow-up succeeds. The HAProxy native self-test proves the connector's framed
protocol controls but not a full HAProxy host integration or operating-system
FD-leak audit.

## Checks not run and rationale

No complete local real-host matrix was run. The full bilingual documentation
check was run but is `blocked_environment` solely because this task checkout
lacks required Framework Gitlink targets; no Framework initialization or
modification is authorized. PR-scoped SonarQube Cloud analysis and GitHub
Actions have not yet run for the remediation head. No merge or direct `master`
update is authorized.

## Known limitations

The ten connector solutions still need full runtime-layer failure-vector,
parallelism, shutdown, and cleanup evidence where their real host dependencies
are available.

## Remaining risks

Any remaining Sonar or hosted failure must be addressed from its exact-head
evidence without weakening controls.

## Final diff and review status

An earlier local combined review is retained as historical evidence. The fresh
independent Apache/lighttpd bypass review completed in two correction rounds:
it first found the FIFO and creation race, then pathname-after-validation
paths, and finally an unbounded `write-json --field` sink. The final narrow
re-review found no concrete remaining bypass after the descriptor-relative and
size-bound corrections. A normal remediation commit and push, then exact-head
Codex, GitHub Actions, and SonarQube Cloud results, remain pending. This
record deliberately does not claim a final commit, push, Quality Gate pass,
workflow pass, or merge; those facts are reconciled only after they occur.

## Follow-up trust-boundary correction

The Apache smoke runner now prepares generated runtime, log, audit, module,
configuration, document-root, and case-output directories through a
descriptor-relative `mkdirat`/`O_DIRECTORY|O_NOFOLLOW` walk. It rejects a
symlinked nested path without creating the target outside the runtime area,
requires trusted ancestor ownership, and preserves both private `0700` and
non-private-output-root legitimate controls. Apache evidence is opened
descriptor-relatively below the private artifact root, accepts only a regular
file, and is bounded to `1048576` bytes; FIFO and oversized evidence fail
closed without blocking.

The lighttpd Linux guard now opens the trusted root, artifact parent, and
cleanup-tree descendants through verified directory descriptors. It opens
candidate artifacts with `O_NONBLOCK|O_NOFOLLOW`, requires a private regular
file before parsing, preserves retryable absent-log polling, and bounds the
cleanup tree by entry count and depth. JSON receipts accept at most 32 fields,
4096 bytes per field, and 65536 serialized bytes; an oversized receipt creates
no artifact, while the fixed-provenance control remains accepted.

The narrow Common helper test correction retains the lossless event contract:
when serialization cannot produce a lossless event, the output buffer is empty
rather than a synthetic `"truncated":true` record. This changes neither a
workflow nor a ruleset, required check, Quality Gate, or production fail mode.

The newest focused aggregate was:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_apache_process_guard tests.test_apache_smoke_case_output_root \
  connectors.lighttpd.tests.test_backend_close_harness_contract \
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract \
  tests.test_haproxy_spop_peer_isolation_contract \
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
```

It passed `114` tests. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m
py_compile` for the affected Apache/lighttpd Python guards and probes,
`rtk proxy sh -n` for the affected Apache/lighttpd runners,
`rtk proxy make check-common-helpers-c17`, and `rtk proxy git diff --check`
also passed. `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
tests.test_bilingual_docs tests.test_connector_config_reference` also passed
with `26` tests. The HAProxy revalidation confirms that a saturated gate closes the
new peer and continues the accept loop; all slots can still be occupied until
their bounded peer deadlines, a documented deployment-dependent residual that
requires a real-agent saturation run before it can be classified further.

## Exact-head Sonar authority-boundary follow-up — 2026-09-04

This section supersedes the earlier pending-hosted-status statements above;
those earlier statements remain historical snapshots rather than current
delivery status.
For exact PR head `d4f5674e8438d398696b1e92965d6e246618306f`, all returned
GitHub Actions checks, including `bounded-c-cpp` and the five connector runtime
matrix cells, succeeded. SonarQube Cloud alone failed the Quality Gate with
`new_security_rating=3` (required `<=1`) and five open vulnerabilities: four
`pythonsecurity:S8707` findings in the Apache process guard and one
`pythonsecurity:S8705` finding in the lighttpd session guard. The duplication
measure was `2.3`, within its configured threshold. No CI workflow, ruleset,
branch rule, or required check was modified.

The Apache guard no longer accepts generic `--directory` or `--artifact-root`
flags from a direct invocation. The smoke runner supplies those capabilities
through required trusted runner-scoped configuration; the existing
descriptor-relative, ownership, mode, size-bound, and cleanup controls remain
in force. The lighttpd guard no longer accepts an `argparse.REMAINDER` command.
It constructs only four typed runner profiles: `lighttpd-config-check`,
`lighttpd-server`, `stock-lifecycle-hold`, and bounded `sleep-duration`.
Missing, unknown, additional, or conflicting profile values fail before
`execv`; the Stock profile uses the fixed lifecycle probe and its fixed
argument shape.

The final local candidate passed the focused Apache/lighttpd/HAProxy aggregate
below with `116` tests and the bilingual/config-reference suite with `26`
tests:

```text
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  tests.test_apache_process_guard tests.test_apache_smoke_case_output_root \
  connectors.lighttpd.tests.test_backend_close_harness_contract \
  connectors.lighttpd.tests.test_stock_lifecycle_harness_contract \
  tests.test_haproxy_spop_peer_isolation_contract \
  tests.test_haproxy_spop_sigpipe_peer_isolation_contract
```

Python compilation for the affected guards/probes, `sh -n` for all affected
runners, `make check-common-helpers-c17`, and `git diff --check` also passed.
Two independent post-patch authority-boundary reviews found no direct CLI
bypass or runner-contract regression. The residual trust boundary is the
runner process configuration and selected host executables: this is trusted
orchestration input, not an authentication mechanism against a same-identity
local principal. Such a principal is outside this local harness boundary.
`FND-SONAR-0074` remains `in_progress` until a normal follow-up push produces
a passing SonarQube Cloud result for its exact PR head.

### lighttpd zombie-cleanup follow-up

An original Codex review finding remained reproducible after the earlier
zombie-state correction: `terminate_registered_session()` preserved raw initial
session membership for audit, then incorrectly derived `unexpected_members`
from that raw list. A pre-existing zombie therefore made
`cleanup-session --reject-unexpected-members` fail after successful active
containment. The guard now retains raw `initial_members` as evidence, but
derives unexpected members from active initial non-leaders and verified
non-leader TERM/KILL signals only. Uninspectable state remains fail-closed;
live initial and late-forked members remain unexpected and keep the reject
control effective.

The regression launches a task session with a pre-existing zombie child,
requires `cleanup-session --reject-unexpected-members` to return success, and
proves that the zombie remains in `initial_members` but not in
`unexpected_members`. The test waits for a complete child-PID record and gives
the leader a TERM reaping path before any escalation. A process that disappears
between membership scan and `/proc` state read is benign only for `ENOENT` or
`ESRCH`; all other inspection failures remain fail-closed. The existing
live-child and late-fork controls also passed. The two lighttpd harness contract
suites passed with `65` tests; Python compilation and `git diff --check`
passed. No CI workflow, ruleset, branch rule, or required check was changed.
