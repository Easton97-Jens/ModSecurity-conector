# Change Record: Parent HAProxy runtime maintainability remediation

**Language:** English | [Deutsch](CR-20260730-sonar-haproxy-runtime-maintenance.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260730-sonar-haproxy-runtime-maintenance |
| Date (UTC) | 2026-07-30 |
| Base revision | `4e5d45072bf32ff822f4b1039517026416259493` |
| Tracking | Current HAProxy SonarQube Cloud maintenance remediation and initial Draft-PR delivery. |
| Boundary | Parent `connectors/haproxy/`, its direct contract check, and this bilingual Change Record/index pair. Framework, MRTS, Gitlinks, workflows, Sonar configuration, suppressions, and `master` are unchanged. |

## Motivation and problem statement

The current master inventory contains 55 HAProxy maintainability rows plus one
`python:S5332` loopback-helper signal. This focused increment extracts repeated
SPOP argument parsing, separates HTX request/response end-of-stream handling,
centralizes build-artifact hashing, and isolates CRS configuration loading. It
does not claim that the Draft PR closes every historical baseline finding.

## Acceptance criteria

- Preserve exact bounded SPOP key matching, typed-value consumption, owned
  header/body handling, and request/response lifecycle state.
- Preserve HTX Phase-2 pre-commit and Phase-4 late-intervention behavior with
  exactly one binding finalization callsite for each phase.
- Keep the builder's SHA-256 evidence deterministic and POSIX-shell clean.
- Keep CRS setup-file precedence, example fallback, rules-directory loading,
  and cleanup behavior unchanged.
- Keep all changes Parent-only and C17-compatible where C is changed.

## Implementation decision and rationale

The SPOP runtime uses tables and a length-aware C-string comparator for its
known string, integer, and response-header arguments; the literal-only macro
is retained only for actual literals. It removes custom variadic file writers
and retries interrupted I/O without nested `continue` paths. HTX lifecycle
work is split into request and response helpers; the direct contract checker
follows those helpers. The builder owns one `sha256_of` pipeline. Binding CRS
loading now has one allocation-cleanup path.

## Security impact

The changed code processes peer-controlled SPOP fields and native HTTP
lifecycle state. The security invariant is unchanged: only bounded, recognized
typed inputs may alter the parsed request, unknown input uses the existing
skip path, and Phase-2/Phase-4 controls cannot be bypassed by callback
reordering. The current `python:S5332` signal is an `already_safe` local test
server: it binds literal `127.0.0.1`, and probe URLs are checked as credential-
free `https://127.0.0.1` before use. No suppression, scanner exclusion, or
control weakening was used.

## Changed files

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/htx-overlay/build-overlay.sh`
- `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`
- This English/German Change Record pair and both indexes.

## Commands executed

| Control | Result |
| --- | --- |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | passed |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | passed: 26 contracts |
| `shellcheck --severity=warning connectors/haproxy/htx-overlay/build-overlay.sh` | passed |
| `PYTHONDONTWRITEBYTECODE=1 python3 connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` in the authoritative Parent checkout | passed: 9 tests |
| `git diff --check` | passed |

## Runtime evidence

The focused Python helper suite confirms its local-loopback controls. The HTX
checker verifies source-level lifecycle invariants. Neither result claims a
live HAProxy plus libmodsecurity enforcement run.

## Checks not run and rationale

`make -C connectors/haproxy test-htx-overlay` completed its 26 static checks
then could not import the deliberately uninitialized Framework helper in this
isolated task worktree. `make -C connectors/haproxy build-modsecurity-binding`
exited 77 because libmodsecurity headers and library are absent from `/src`
and the registered temporary build root. No full runtime, connector matrix,
complete Codex Security diff scan, or hosted exact-head check has run yet.

## Known limitations

The Draft PR deliberately retains unaddressed historical HAProxy SonarQube
Cloud baseline rows. The missing libmodsecurity development artifacts prevent
native binding/link/runtime evidence locally.

## Remaining risks

A fresh exact-head SonarQube Cloud result may identify remaining baseline or
newly introduced issues; it is required before the PR can be considered
verified or merged.

## Final diff and review status

The local diff is Parent-only, has passed its available focused checks, and is
prepared for a Draft PR. Push, PR number, exact head, hosted checks, review,
and SonarQube Cloud results are intentionally recorded only after they occur.
