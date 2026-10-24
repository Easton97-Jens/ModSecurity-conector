# NGINX cleanup port probe after graceful shutdown

**Language:** English | [Deutsch](CR-20260930-nginx-port-cleanup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-nginx-port-cleanup |
| Date (UTC) | 2026-09-30 |
| Base revision | `91fce858acea9273d649e0bca1a5c2faadd28f9a` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation and problem statement

The Parent NGINX harness could classify a successful graceful shutdown as
`port=... result=still_bound`. Its cleanup probe attempted a bare IPv4 TCP
bind after the NGINX master and workers had exited. A recently closed local
connection in `TIME_WAIT` can reject that bind with `EADDRINUSE` even when no
listener remains. A separate diagnostic replay demonstrated this mechanism;
the exact socket state of the two earlier full-E2E failures cannot be
reconstructed because their private network namespaces no longer exist.

## Acceptance criteria

The post-shutdown check must accept `TIME_WAIT` only when the TCP listener is
gone and an NGINX-compatible loopback bind succeeds. It must still reject an
active local or foreign listener, an occupied HTTP/3 UDP port, an unusable TCP
port, and inspection errors. Keep master, worker, PID, Unix-socket, and other
cleanup checks intact. Prove the behavior with executable socket tests and
repeated real Root-master/`nobody`-worker cases. A full Exact-Head PASS still
requires a fresh canonical result and exit 0.

## Implementation decision and rationale

Only the Parent harness's **post-shutdown** port check uses the new probe;
pre-start port selection remains unchanged. The probe inspects
`/proc/net/tcp` in its current network namespace for IPv4 loopback and
wildcard listeners, rejects `LISTEN` before binding, and then tests
`127.0.0.1` with TCP `SO_REUSEADDR`, matching NGINX's listening socket
behavior without using `SO_REUSEPORT`. HTTP/3 retains its separate UDP bind
check. Inspection and bind failures remain fail-closed. A bounded structured
diagnostic records namespace, family, address, port, listener and `TIME_WAIT`
counts, bind outcomes, and errno where applicable in the harness output and
lifecycle log.

## Security impact

The change distinguishes harmless `TIME_WAIT` from a live listener; it does
not turn a failed cleanup into success merely because NGINX processes exited.
Foreign-process listeners remain rejected and are not killed. The probe uses
the harness's inherited namespace; it adds no global `/tmp` or `/var/tmp`
write exception and does not relax path authority, ownership, event, or
canonical validation. Framework, MRTS, Common, and connector C source remain
unchanged.

## Changed files

- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_port_cleanup_probe.py`
- This English/German Change Record pair.

## Commands executed

The executable socket regression was RED on the base harness: the real
cleanup call rejected a `TIME_WAIT`-only port even though a control TCP bind
with `SO_REUSEADDR` succeeded; its old bare bind returned `EADDRINUSE`. After
the fix, all 9 socket tests passed. They cover a free port and current
namespace, `TIME_WAIT`, loopback and wildcard listeners, a foreign-process
listener left alive, HTTP/3 UDP occupancy, IPv6-only and dual-stack listeners,
and invalid input. A 90-test focused Parent suite had 89 passes and one
sandbox-only `chown: Invalid argument` failure in the real ownership test;
that exact test passed with host rights. `sh -n` and `git diff --check` passed.
ShellCheck reported the same 13 pre-existing findings as the base revision,
with none introduced by this change. The complete `test_nginx_*.py` discovery
suite then passed 446/446 with host rights and external `TMPDIR`.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_port_cleanup_probe'
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p "test_nginx_*.py" -q'
rtk run -c 'sh -n connectors/nginx/harness/run_nginx_smoke.sh'
rtk run -c 'git diff --check'
```

## Runtime evidence

Two six-invocation focused host runs exited 0. The latest, noncanonical run
is at
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-port-cleanup-focused-20260930T153915Z-1YDTDy`.
It ran Phase-3 deny, Phase-4 after-commit abort, and Phase-3 redirect twice
each under `PrivateNetwork=yes`, with Root NGINX master (UID 0) and `nobody`
worker (UID 65534). All six real case assertions passed: HTTP 403 for the
two Phase-3 denies, the expected transport abort for the two Phase-4 cases,
and HTTP 302 for the two redirects. Each invocation ended with successful
graceful cleanup; the diagnostic recorded zero TCP listeners, one `TIME_WAIT`
entry, and a successful reusable TCP bind on ports 19880–19885. Both
redirects also had raw client and no-follow curl exit 0 with exactly one
`Location` field. These are focused diagnostics, not a canonical full-E2E
result.

## Checks not run and rationale

A fresh full Exact-Head E2E, canonical result/evidence review, and SHA256SUMS
verification remain pending at this record's current review point. Remote CI,
PR checks, and merge have not been observed. This record does not claim an
overall `NGINX EXACT-HEAD E2E PASS`.

## Known limitations

The historical private namespaces and their exact TCP state/errno are gone;
the present RED socket reproduction and focused live runs establish the
failure mechanism and corrected behavior, not a retrospective state of those
specific incidents. The focused suite's sandbox `chown` failure is an
execution-environment limitation, not counted as a pass for that run.

## Remaining risks

The full selected profile may expose a separate failure after the corrected
cleanup path. Canonical case counts, requests, native records, events, result,
exit code, and evidence integrity must be checked on the eventual new Parent
head before any Exact-Head status is declared.

## Final diff and review status

The intended change is confined to the Parent cleanup probe, its dynamic
regression, and this paired record. Focused validation is green subject to
the stated sandbox limitation; final documentation, diff, commit, full E2E,
and delivery review are still pending.
