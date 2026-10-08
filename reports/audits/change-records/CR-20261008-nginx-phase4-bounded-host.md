# Change Record: CR-20261008-nginx-phase4-bounded-host

**Language:** English | [Deutsch](CR-20261008-nginx-phase4-bounded-host.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-phase4-bounded-host |
| Date (UTC) | 2026-10-08 |
| Base revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation and problem statement

Selected Phase-4 split, EOS, Engine-limit and bounded-metadata operations lack actual dedicated invocations. A declared fixture or HTTP status alone cannot establish these contracts.

## Acceptance criteria

Bounded loopback chunks and EOS must be actually sent; missing release must fail. Dedicated host invocations retain exact configtest/client exits, artifacts, native records, observed Root/nobody and PIDFD-bound cleanup. No driver-generated native event or premature canonical PASS is allowed.

## Implementation decision and rationale

The new `ci/runtime/common/nginx_phase4_upstream.py` sends at most eight chunks and 8192 bytes, on an allocated IPv4-loopback listener. The explicit barrier bounds split timing; its observations concern only successful sends and EOS, not native inspection. The dedicated `ci/runtime/lifecycle/run-nginx-phase4-cases.py` imports the existing secure snapshot/projection and role/PIDFD cleanup helpers rather than duplicating authority. It loads closed Framework inputs, uses `proxy_buffering off`, and retains exact stdout/stderr/config/rules/native events with digests. It keeps `canonical_status=NOT_EXECUTED` until independent strict canonical validation. The latest explicit user decision migrates the legacy Required identity to existing `safe`; no `minimal` mode is restored and off legacy behavior is unchanged. Earlier off focus artifacts remain historical diagnostic data, not safe evidence.

## Changed files

Continuation on 2026-10-08: the dedicated curl invocation now retains
`response.headers` using its actual `--dump-header` output and includes those
bytes in `raw_sha256`. This lets the independent Framework operation validator
check the wire status, MIME and framing alongside the decoded body and curl
result. Native observations and canonical status remain unchanged by capture.
Two existing driver-boundary tests pass after this focused capture change;
the new native producer still requires coordinator integration and rebuild.

The two new helpers, `tests/test_nginx_phase4_upstream.py`, `tests/test_nginx_phase4_driver.py`, and this EN/DE pair. Central dispatcher/collector/schema/native producer are coordinator-owned integration dependencies.

## Commands executed

RTK-wrapped Parent Python unittest: three real loopback wire tests and two driver-boundary tests pass, exit 0. The initial upstream test failed because its implementation was absent. A broad existing phase4 pattern run passed 25 tests with three existing SKIPs; those SKIPs are not host evidence. Syntax/help and `git diff --check` pass. Native NGINX focus, documentation validation and final integration remain pending at record preparation.

## Security impact

No foreign process, listener, network or global rights mutation. Root/nobody operations require isolated task attempts; signals target observed owned processes and bound children. Output roots remain fresh private external children; docroot projections remain fresh direct authorized children. Raw fixture response is bounded; no body is put into events or upstream metadata.

## Runtime evidence

The socket tests prove actual local HTTP chunk frames and timeout behavior, not NGINX coverage. External development focus `stream-c-r1` performed eight real isolated operations with read-only sources and baseline artifacts: all configtests exit 0, Root 0/nobody 65534 observed, cleanup verified. Split/EOS and ProcessPartial requests returned client 0/HTTP 200 with actual native rule 1100301. Reject produced client 18 with native invalid-Engine-response abort; off-after-commit produced client 18 with native connector-error abort. Neither is claimed PASS. Existing counters still report bytes handed to append, not Engine retained length. Borrowed proc observer captured master/child maps before privilege drop, not nobody-UID maps; later ready worker identity is independently bound by the role/PIDFD receipt. Real host observations are deliberately not assigned PASS by this input/driver layer. Operations-specific strict interpretation and final integrated execution remain required.

## Known limitations

Actual upstream chunk boundaries alone do not prove multiple ModSecurity append calls. The existing append-byte counter does not prove Engine-retained inspection length after ProcessPartial. Native producer and explicit deterministic source mapping remain integration work. Shared Required selection stays unchanged; no final Exact-Head or Protected acceptance is claimed.

## Remaining risks

Successful helper execution does not imply a validated native limit or EOS contract. Final integrated strict canonical validation and negative artifact controls remain required.

## Checks not run and rationale

Privileged focus waits for the coordinator's serialized runtime slot. Final native lint, combined regression suite and fresh-head CI/Sonar are coordinator-owned.

## Final diff and review status

Exclusive Parent task worktree; no Parent Gitlink, MRTS, publication or protected-infrastructure modification.
