# NGINX synchronized First-Byte Safe policy

**Language:** English | [Deutsch](CR-20260927-nginx-first-byte-safe.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260927-nginx-first-byte-safe |
| Date (UTC) | 2026-09-27 |
| Base revision | `1bf1dcd46d25ba5b22f8a7d5915b5f72b4daa4da` |

## Motivation and problem statement

The portable First-Byte fixture materializes an empty host mode. The Parent
expects complete Safe streaming but previously executed default Off, receiving
all 44 payload bytes with incomplete chunked framing and curl exit 18.

## Acceptance criteria

Explicit synchronized Safe policy survives case loading; omitted/invalid/Off/
Strict synchronized selection is rejected before startup. Direct default Off
and ordinary fixture modes remain unchanged. Real native proof requires HTTP
200, 44 bytes, complete chunked termination, curl 0, causal first byte before
EOS, native rule 1100301 and a non-aborted Safe late observation.

## Implementation decision and rationale

Caller selects `NGINX_SYNCHRONIZED_PHASE4_MODE=safe` only for NGINX. Harness
captures it readonly and applies the validated literal after case loading.
Existing `server_with_location_override` logging scope supplies the native
Phase4 sink consumed by the First-Byte producer. No connector C, Common,
Framework, MRTS, rule, serializer, canonical or early/allow-event changes.

## Security impact

No eval of policy input; exact Safe enum only. An override outside its route
fails closed. Existing root/nobody separation, path authority, projection
freshness, private-network runtime and curl/error guards remain unchanged.
Technical errors retain existing terminal behavior; Rule 1100301 remains deny.

## Changed files

- `ci/runtime/lifecycle/run-native-first-byte.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_synchronized_phase4_policy.py`
- `connectors/nginx/README.md` / `README.de.md`
- This Change Record pair.

## Commands executed

Red regression ran on unmodified production before the fix and exposed missing
caller/post-load binding. Focused `python3 -m unittest
tests.test_nginx_synchronized_phase4_policy -v`: 11 PASS, including readonly
tamper rejection, malicious/missing/Strict values and full44/HTTP200/curl18 FAIL.
Framework `tests/security_regression/test_synchronized_upstream_security_boundaries.py`:
8 PASS, Framework unchanged. All commands RTK-wrapped, external TMPDIR.
Broader 17-module Parent suite: 248 PASS, no skips. Final focused + runner-
wiring rerun: 17 PASS. Syntax PASS; ShellCheck has the same 20 existing
diagnostics as the base, with no additions. Bilingual documentation,
repository path references and documentation links passed.

```sh
rtk run -c 'python3 -m unittest tests.test_nginx_synchronized_phase4_policy tests.test_nginx_phase4_runner_wiring -v'
rtk run -c 'sh -n ci/runtime/lifecycle/run-native-first-byte.sh connectors/nginx/harness/run_nginx_smoke.sh'
rtk run -c 'make check-bilingual-docs check-doc-links'
rtk run -c 'git diff --check'
```

The actual test invocations bind external TMPDIR, disable bytecode writes and
select the exact pinned Framework; detailed logs are external run evidence.

## Runtime evidence

Isolated pre-commit native proof under
`/var/tmp/codex/nginx-first-byte-safe-20260927T165747Z`: Safe rendered after empty
case.env; HTTP200, 44/44 bytes, 23+33+5 chunked framing bytes (terminal zero
chunk), curl0 and native wrapper0. Rule1100301 requested deny, actual log_only,
visible200, not aborted. Client transport is `http_status`; existing native
event transport enum is `log_only`, deliberately unchanged. Real-host barrier
and no-full-buffering evidence PASS; root/nobody, 16 preflights, clean shutdown.

## Checks not run and rationale

New exact-head full E2E is deferred until after the separate commit and all
prerequisite checks. No new CRS/MRTS/H2/H3 matrix, Sonar, remote CI, push or merge.

## Known limitations

Allow/early event emission/collection defects remain separate. Isolated PASS
does not establish whole canonical E2E PASS. Framework remains pinned to
`cc36b37d0f6a0fbc3512f3878a691751e91c5fbb`, MRTS to
`615b13bacbd008562c17408246c41ab27dca3104`.

## Remaining risks

Only this synchronized proof changes policy selection. Real errors must not
be reclassified as successful Safe handling. Existing transport and event
assertions are not loosened; native and client transport fields stay distinct.

## Final diff and review status

Focused regression, broader tests, isolated proof, documentation and final
diff checks verified before commit. Final run/delivery status belongs to
external run-scoped evidence, not an invented pre-commit E2E claim.
