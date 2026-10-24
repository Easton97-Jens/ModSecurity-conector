# NGINX redirect Location replacement

**Language:** English | [Deutsch](CR-20260930-nginx-redirect-location.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-nginx-redirect-location |
| Date (UTC) | 2026-09-30 |
| Base revision | `0fe4c7b8cf4b021663985d895064e56cd2c63410` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation and problem statement

The pinned NGINX Phase-3 redirect case returned two active `Location` fields,
so its no-follow curl request exited 8 with `Multiple Location headers`. The
Parent response-header fixture supplied `/encoded%2Ftarget`; the ModSecurity
rule supplied `https://no-crs.invalid/phase3-redirect`. NGINX retained the
relative upstream field in its output list without indexing it at
`headers_out.location`; the connector cleared only that pointer before adding
its redirect. This is separate from two historical port-cleanup failures.

## Acceptance criteria

An accepted connector-owned redirect replaces every older active `Location`
field and emits exactly its validated target once. Preserve ordinary upstream
responses, status-only interventions, unrelated headers, repeated redirects,
and rejection of malformed or already-committed redirects. Prove the change
with a RED/GREEN executable regression and a real Root-master/`nobody`-worker
request. A full Exact-Head PASS requires a later canonical result and exit 0.

## Implementation decision and rationale

Only the Parent connector redirect helper changes. After successful allocation
of its new header, it retains `ngx_http_clear_location` and deactivates prior
active, case-insensitive `Location` entries across all NGINX output-list
parts. It does not touch other headers, status-only interventions, the
Framework, MRTS, Common, event contracts, or the separate cleanup probe.
The connector's existing EN/DE README redirect contract remains accurate.

## Security impact

Removing conflicting prior `Location` fields prevents ambiguous redirect
targets at the HTTP client boundary. Existing URL validation, CR/LF rejection,
header-sent guard and NGINX path/ownership checks remain unchanged. The
isolated runtime used `PrivateNetwork=yes`, a fresh root-owned direct docroot
projection child, and a Root master with a `nobody` worker.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `tests/test_nginx_redirect_location.py`
- This English/German Change Record pair.

## Commands executed

The actual C redirect and status helpers were compiled with `-std=c17 -Wall
-Wextra -Werror` in a bounded NGINX header-list fixture. Before the source
fix, four subcases exposed two or three active `Location` fields; after the
fix, all eight tests passed. Focused Parent suites passed 98/98 with host
rights and 96/96 for First-Byte, Phase-4, collector, and worker contracts.
The initial sandbox-only 98-test run had one `chown: Invalid argument` failure;
the exact suite passed on repetition with host rights. Relevant shell syntax
and task-local ShellCheck passed; unchanged Parent shell files retain existing
ShellCheck diagnostics. `make build-nginx` completed with exit 0 against the
pinned source and produced a cache-v2 manifest whose independently checked
source hash matched the worktree.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_redirect_location'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/build-nginx-redirect-fix.sh'
rtk run -c 'make FRAMEWORK_ROOT=/var/tmp/codex/worktrees/nginx-p3-redirect-location-20260930/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links check-no-crs-doc-consistency'
rtk run -c 'git diff --check'
```

## Runtime evidence

The preserved RED replay at
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-redirect-red-20260930T124227Z-50Zvn9`
captured HTTP 302 with both `Location` fields, curl exit 8, and collector
exit 0. Two fresh GREEN replays used the rebuilt module and returned HTTP
302 with exactly one `Location`:
`https://no-crs.invalid/phase3-redirect`. Raw client, original no-follow curl,
case assertion, and native collector exited 0. The second replay is at
`/var/tmp/codex/ModSecurity-conector/runs/diagnosis/nginx-redirect-green-20260930T140030Z-t9x93A`.
Its harness still exited 1 on separate `port=19889 result=still_bound` cleanup:
after graceful quit and process exit, there was no listener, but the private
namespace showed `TIME-WAIT`; the probe's bind without `SO_REUSEADDR` failed
with `EADDRINUSE` (errno 98), while the same bind with `SO_REUSEADDR` passed.
No cleanup failure was reclassified as a pass.

## Checks not run and rationale

The fresh Exact-Head full E2E follows this separate commit. Remote CI, push,
PR, merge, Framework/MRTS changes, and a cleanup source fix are outside this
change. No full canonical PASS is claimed from the isolated redirect case.

## Known limitations

The historical cleanup namespaces no longer exist, so their exact socket
states and errno cannot be reconstructed. The current reproduction proves a
cleanup false-positive mechanism, not the precise state of both old incidents.
The full selected profile may still stop on cleanup before all requests run.

## Remaining risks

Canonical counts, event completeness, and lifecycle exit must be checked on
the new exact Parent head. The cleanup probe needs its own separately scoped
fix and regression if the failure persists; no containment, validator, or
port check is weakened in this change.

## Final diff and review status

The intended commit contains only the Parent redirect helper, its executable
regression, and this paired record. Final documentation, diff, commit and
Exact-Head evidence must be checked before any overall E2E status is reported.
