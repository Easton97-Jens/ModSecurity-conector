# FND-PARENT-0038 — Apache Phase-4 response bypass

## Classification

| Field | Value |
| --- | --- |
| Category | security_validated |
| Repository / ownership | Parent / parent |
| Priority / severity | P0 / high |
| Confidence / status | validated / fixed |
| Release blocker | yes |
| Security relevant | yes |
| Feasibility | feasible_now |
| Current local candidate | `93c5f30c181710f5c2cecf207fb92aaecb215035` plus focused unpushed Parent remediation |

## Summary, impact, and invariant

Before remediation, Apache could pass a response brigade downstream before
libModSecurity processed `RESPONSE_BODY` at EOS. A disruptive Phase-4 deny
could consequently follow protected bytes across the response-commit boundary.
Normal internal redirects could also retain the original transaction while
resetting the target request's filter and handler path.

A remote requester able to cause a response body matching a deployed Phase-4
deny rule could receive content policy intended to suppress. No byte that Phase
4 can consider may reach downstream before `msc_process_response_body` and its
intervention resolve. An unsafe redirect must also neither release protected
content nor invoke a target quick handler or normal handler.

## Affected scope, preconditions, and reproduction

- `connectors/apache/src/msc_filters.c` — held-response lifecycle and terminal
  filter helpers.
- `connectors/apache/src/mod_security3.c` —
  `apache_phase4_redirect_is_terminal_error_emission`,
  `hook_phase4_redirect_quick_handler`, `hook_phase4_redirect_handler`, and
  `apache_phase4_terminal_error_redirect_note`.
- Parent harness and regression scope:
  `connectors/apache/harness/{mod_phase4_terminal_rogue.c,run_apache_smoke.sh}`,
  `ci/runtime/lifecycle/run-apache-phase4-response-regression.sh`, and
  `tests/test_apache_phase4_response_regression_wiring.py`.

The precondition is a native Apache/libModSecurity Phase-4 response-body rule
and a direct or internal-redirect response route. The requester needs no local
privilege. The historical URI-target control recorded an internal-redirect
response containing the deny marker; its central artifacts remain missing or
unsealed and are retained only in `finding.json`.

Fresh exact-dependency testing first ran `redirect-target-handler-abort-h1`
before the focused repair. It exited `1` and logged both the connector refusal
and `ModSecurity Phase4 redirect target handler executed`, proving that
aborting in the insert-filter path did not stop the target handler.

## Current retained evidence

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| Pre-fix target-handler H1 log | `ada09ca5545220b3c2e9afee4b54d069eae66257f2b615ba1678350f3dd7c040` | exit `1`, refusal and marker present |
| Post-fix target-handler H1 log | `c02afef668fc16a98ed026d3b5e0587975ed4fedd7f29184e5059021afafe021` | exit `0`, refusal present and marker absent |
| Post-fix target-handler H2 log | `264f67f18b99979f60b6a6ecec2c40d808937aca6c0e293aa8ce94f606c7de22` | exit `0`, refusal present and marker absent |
| Exact native matrix report | `2218e7d5545f6b09dcb43d1b0779889fc778a16d3f3f65e2246598c3b54e4627` | serial 30-control matrix exit `0` |
| Sealed native manifest | `1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548` | current evidence inventory |

All current artifacts are under retained task run
`20260719T162259Z-pr60-exact-head-revalidation-dfba422e`; complete paths,
commands, working directory, timestamps, and retention state are in the
canonical JSON record.

## Root cause and remediation

`hook_insert_filter` is `void`, so sealing or aborting there does not stop
`ap_run_handler`. Apache runs a normal internal redirect quick handler before
`ap_process_request_internal` and `ap_invoke_handler`; the former guard could
therefore not prevent target-handler side effects.

The repair adds `APR_HOOK_REALLY_FIRST` quick-handler and normal-handler guards
that return `DONE` for an unsafe `r->prev` redirect. It keeps the bounded
core-shaped local `ErrorDocument` exception only after its proof succeeds and
records that one-time allowance in the new request's notes table, preventing a
nested redirect from inheriting it. Held-response, terminal-guard, and
single-release behavior remains in place.

## Acceptance, regression, and legitimate controls

- A marker deny releases no protected marker before EOS.
- Allow, log-only, empty, body-limit, ProcessPartial, client-abort,
  `ErrorDocument`, redirect, H1/H2, late-producer, and multi-brigade controls
  retain their documented behavior.
- `redirect-target-handler-abort-h1` and
  `redirect-target-handler-abort-h2` preserve the refusal and execute no target
  handler.
- The focused static suite
  `tests.test_apache_phase4_content_type_synchronized_upstream` plus
  `tests.test_apache_phase4_response_regression_wiring` passed 16/16; shell
  syntax, `git diff --check`, and a focused exact-header C17 frontend check also
  passed.
- Local ErrorDocument controls remain the legitimate control. CRS is blocked by
  its Framework provenance guard and MRTS has no current read-only
  materialization result; neither was bypassed or claimed as passing.

## Dependencies, blockers, and residual risk

The current matrix used a task-owned read-only copy of the Parent-gitlink
Framework revision `cdc91a398d6c156eaff927d742b23018a3817fb6` and left the
Framework, MRTS, and both gitlinks unchanged. The relevant MRTS revision is
`13aa91291adea12d5c607fdd165d010fcfb1da78`.

This finding is **fixed**, not verified. Remaining blockers are a fresh local
Codex Security diff scan, then exact pushed-head CI, CodeQL, SonarCloud,
review/thread evidence, protected merge, resulting-master validation, and a
master rerun of the original reproduction plus legitimate controls. The local
ErrorDocument proof still relies on Apache-core `no_local_copy` and
`REDIRECT_STATUS` correlation rather than an unforgeable provenance primitive;
no risk is accepted.

Related finding: `FND-PARENT-0008` is an unrelated Clang baseline warning and
not a duplicate.

## History

- `2026-07-18T14:57:02Z` — historical native evidence recorded the response bypass.
- `2026-07-19T16:50:12Z` — canonical record created as blocked after the
  historical-evidence audit.
- `2026-07-19T18:20:42Z` — exact native target-handler reproduction identified
  the remaining handler side effect; focused Parent remediation passed H1/H2 and
  the sealed 30-control matrix, moving this finding to `fixed` locally.
