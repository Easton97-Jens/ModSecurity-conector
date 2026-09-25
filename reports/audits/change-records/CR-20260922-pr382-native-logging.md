# Change Record: native logging result and re-entry

**Language:** English | [Deutsch](CR-20260922-pr382-native-logging.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-native-logging` |
| Date (UTC) | `2026-09-22` |
| Base revision | `1ce569e1afce55e17c767e1e06b0266874fe8c3e` |

## Motivation and problem statement

The native NGINX audit epilogue ignored `msc_process_logging()` results and did
not claim its own one-attempt marker. Failed native completion could appear as
success, and repeated log-phase callbacks could invoke the engine again.
The upstream native logging API documents boolean operation success, not the
byte-append `ProcessPartial` contract.

## Acceptance criteria

Accept only native result one. Keep failed completion failed on re-entry, avoid
duplicate native calls, preserve the first canonical cause and restore the PCRE
allocator bracket. Missing native state must not reach the engine. A failed
canonical finish must not become success merely because audit processing works.

## Implementation decision and rationale

The existing `logged` field claims the attempt before native entry; a separate
`native_logging_failed` bit retains pending/failed outcome. Static native
operator diagnostics report failure without recursive JSONL or native logging.
The audit epilogue still runs once after a canonical sequence failure to permit
native audit capture; its success does not repair the sequence. No response is
rewritten or aborted from the log phase, and no earlier delivery is claimed.
Existing early-log callers keep their HTTP policy; the retained flag ensures a
later logging callback does not turn a failed audit into success.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `connectors/nginx/src/ngx_http_modsecurity_log.c`
- `tests/test_nginx_native_logging.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

The new module is in the existing request/native CI step:

```sh
python -m unittest -v tests.test_nginx_native_logging
```

Execution is pending at preparation. Eight compiled-function tests cover valid,
zero, negative and undocumented results, missing state, failed canonical finish,
first-cause retention, recursive entry and repeated callbacks. Compilation uses
C17 with `-Wall -Wextra -Werror`, without replacing the changed function.

## Security impact

Native audit failure is an explicit failure, not an allow or successful audit.
No raw payload, credentials or unbounded diagnostic values are added. HTTP
policy and existing rule-match event semantics are unchanged.

## Runtime evidence

Controlled engine, canonical-operation and final host boundaries are used around
the actual changed functions. These tests do not prove audit-file persistence or
NGINX core handling of log callback return values in a running server.

## Known limitations

This closes one I09 native-call gap and duplicate audit attempts, not all I11
physical sink routes. A log phase cannot retract already delivered bytes. Other
adapters and the complete direct/companion route matrix remain separate work.

## Remaining risks

The audit failure flag is private NGINX request state, not a public wire field.
A successful API result is only native API success, not an independent fsync or
client-delivery receipt. Earlier error classes must remain authoritative.

## Checks not run and rationale

Local project commands were not run because the required RTK wrapper is absent.
Fresh GitHub CI and exact-head Sonar zero remain required. Live-host logging and
cross-route comparisons have not been executed by this change.

## Final diff and review status

Source, regression tests and paired documentation stay in Draft PR #382. No
merge, master push, force push, scanner exclusion or dependency change.
