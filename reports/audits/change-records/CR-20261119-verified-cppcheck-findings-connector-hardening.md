# Change Record: CR-20261119-verified-cppcheck-findings-connector-hardening

**Language:** English | [Deutsch](CR-20261119-verified-cppcheck-findings-connector-hardening.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261119-verified-cppcheck-findings-connector-hardening |
| Date (UTC) | 2026-11-19 |
| Base revision | `b79c3d93efbb8330f121caf8fb7c1a7874195e57` |

## Motivation and problem statement

A Cppcheck 2.22.0 scan of the whole checkout reported about 1,800 diagnostics. Every
priority diagnostic in Parent product code was verified against the real control flow and
the real compiler configuration. Most were analysis artefacts: the scan did not define
`__linux__`, parsed no system or host headers, and mixed Framework test stubs into the
cross-translation-unit analysis of `common/runtime/`. Two Parent defects were confirmed:

1. `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`,
   `phase4_common_event_write()`: the signed `int` field `decision->rule_id` was formatted
   with `%u`. A negative value is undefined behaviour for that conversion and rendered as a
   large unsigned number (`-7` became `4294967289`), and "no rule" (`0`) was rendered as
   `"0"`. The canonical HAProxy binding (`haproxy_modsecurity_binding.c`) renders only
   positive IDs and leaves "no rule" empty.
2. `connectors/nginx/src/ngx_http_modsecurity_module.c`: analysis without the NGINX
   headers reported syntax errors at three `ngx_http_set_ctx(...)` calls. NGINX 1.31.8
   supplies the terminating semicolon in the macro definition. The initially added
   semicolons produced three SonarCloud `c:S1116` empty-statement findings and were
   removed during review. Static analysis requires the configured NGINX headers.

## Acceptance criteria

- SPOP phase-4 Common events render positive rule IDs unchanged and render `0` and negative
  values as an empty `rule_id`.
- The NGINX calls use the terminator supplied by the configured NGINX macro and compile
  with the captured C17 configuration.
- The native C17 checks for HAProxy, Apache, NGINX and the remaining connectors pass.
- A realistic Cppcheck run of all Parent product translation units reports no remaining
  confirmed defect; remaining diagnostics are dispositioned.

## Implementation decision and rationale

- `haproxy_spop_diagnostic_runtime.c`: format with `%d` only when `rule_id > 0`, otherwise
  write an empty string. This reuses the existing canonical binding rule instead of adding a
  new convention. The change is identical to the uncommitted change already present in the
  maintainer's working tree, so later integration does not conflict.
- `ngx_http_modsecurity_module.c`: preserve the three original macro calls. The NGINX
  1.31.8 definition supplies the terminator, so an extra semicolon creates an empty
  statement. Header-free parser diagnostics require corrected preprocessing inputs.
- No other Parent source was changed. Fail-open/fail-closed policy, API, ABI and wire
  protocol are unchanged.
- The Framework gitlink is not changed by this record. The regression tests for both fixes
  and the NDEBUG test-hygiene fix live in the separate Framework repository and are
  delivered through their own Framework pull request.

## Changed files

- `reports/audits/change-records/CR-20261119-verified-cppcheck-findings-connector-hardening.md`
- `reports/audits/change-records/CR-20261119-verified-cppcheck-findings-connector-hardening.de.md`

## Commands executed

All commands ran through RTK in a task worktree, with build, temporary and log output in the
task-owned external run root `cppcheck-audit-20261119T095825Z`.

| Command | Result |
| --- | --- |
| `rtk bypass make check-haproxy-c17` (Bear-captured) | exit 0, `PASS: haproxy_c_standards c17 compile completed` |
| `rtk bypass make check-apache-c17` (Bear-captured) | exit 0, `PASS: apache_c_standards c17 compile` |
| `rtk bypass make check-nginx-c17` (Bear-captured, NGINX 1.31.8 configured headers) | exit 0, `PASS: nginx_c_standards c17 compile completed` |
| `rtk bypass make check-remaining-connectors-c17` (Bear-captured) | exit 0, `PASS: remaining connectors C standard check (c17)` |
| `rtk bypass cppcheck --project=<Bear compile database> --enable=all --inconclusive --std=c17 --library=posix -D__linux__ ...` over 105 Parent product translation units | exit 0; every Parent diagnostic dispositioned (see Known limitations) |
| Framework on-demand test `test_haproxy_spop_event_sink_failures...test_phase4_event_renders_only_positive_signed_rule_ids` | base revision: 2 failures (`'0' != ''`, `'4294967289' != ''`); this change: OK |
| Framework on-demand module `test_nginx_upstream_security_contract` at initial PR publication | only status change: `test_context_creation_returns_only_context_or_null` ERROR on base, ok with the subsequently removed redundant semicolons; its other 7 non-passing cases are identical on base and change |
| Framework on-demand module `test_haproxy_spop_event_sink_failures`, also with `CC="gcc -fsanitize=address,undefined"` | all cases OK, no sanitizer report |
| `rtk make check-active-inventory` | exit 0, `active_case_count` 100 of `hard_limit` 100 |

## Security impact

The SPOP fix removes undefined behaviour in event formatting and keeps audit events
consistent with the canonical rule-ID contract, so a missing or invalid rule ID can no
longer appear as a fabricated large rule number in phase-4 evidence. No enforcement
decision, status code, fail mode or transport behaviour changes. The NGINX review preserves
the original macro calls and records the configured headers needed for static analysis.

## Runtime evidence

None. No HAProxy or NGINX host was started. Evidence is limited to compilation, the
extracted-function SPOP harness, source-contract tests and static analysis.

## Known limitations

- Remaining Parent Cppcheck diagnostics were reviewed and are not defects: `__linux__`
  and missing-header artefacts, cross-unit contamination by Framework test stubs (separate
  scans avoid it), `snprintf(NULL, 0, ...)` length queries, `fdopen()` failure paths that
  correctly close the descriptor, `NULL` attributes for `pthread_*_init`, `apr_pstrcat(...,
  NULL)` in C with glibc, and redundant defensive conditions.
- The lighttpd module was analysed without lighttpd headers (not available locally).

## Remaining risks

Low. Consumers that relied on the previous `"0"` rule ID in SPOP phase-4 events now receive
an empty value, matching the HAProxy binding events.

## Checks not run and rationale

- Host runtime and lifecycle tests for HAProxy SPOE/SPOP and NGINX: not part of this
  bug-fix scope; no host binaries are installed locally.
- `make test` and `make quick-check`: not run in full; targeted native checks and the
  affected Framework on-demand tests were selected instead.
- Cloud Quality Gate: CI-owned; results belong to the pull-request head.

## Final diff and review status

Parent PR #454 landed the HAProxy rule-ID correction. This PR adds the two audit records.
The NGINX source matches the original macro calls. On 2026-11-22 the actual NGINX module
translation unit compiled successfully using the captured GCC 15 C17 configuration with
NGINX 1.31.8 headers and `-Wall -Wextra -Werror`. The task-owned adapter
`nginx455-compile.py` redirects only checkout paths and object/dependency output paths
from the existing compilation database. `git diff --check` passed.

The focused Framework test `test_context_creation_returns_only_context_or_null` still
requires a caller-written semicolon at line 49 and failed with `ValueError: substring not
found` after the macro correction. Its source-text assertion needs a Framework follow-up
that accepts the terminator supplied by the pinned macro.
