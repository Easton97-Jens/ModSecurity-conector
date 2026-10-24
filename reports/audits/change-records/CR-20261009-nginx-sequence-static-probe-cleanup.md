# Change Record: CR-20261009-nginx-sequence-static-probe-cleanup

**Language:** English | [Deutsch](CR-20261009-nginx-sequence-static-probe-cleanup.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-sequence-static-probe-cleanup |
| Date (UTC) | 2026-10-09 |
| Base revision | `b884c6653a72dc490c4ae472dd3cbf5a1ee646b8` |

## Motivation and problem statement

The genuine R10 Root-master/nobody-worker Full97 run reached a real HTTP 200
`clean_shutdown` request, then Framework retention correctly rejected two
`transaction_cleanup` source events for the same configured transaction ID.
The Parent sequence fixture used `try_files $uri /index.html;`: the synthetic
sequence URI was absent, so NGINX internally redirected to `index.html`,
created a second location transaction context, and cleaned up one complete and
one premature context. This is a Parent fixture-routing defect, not a reason to
weaken the Framework exact-one cleanup contract.

## Acceptance criteria

- Every static, non-upstream sequence serves the fixed projected `index.html`
  without an internal redirect.
- Actual upstream cases retain their real `proxy_pass` path.
- Product redirect-context isolation, strict Framework validation, the 97
  Required selections, Framework and MRTS remain unchanged.
- A fresh real sequence request must emit exactly one truthful cleanup event
  per admitted transaction before this change can support Canonical PASS.

## Implementation decision and rationale

Replace the redirecting location inherited from the generic startup template
with the existing `try_files /index.html =404;` probe location before applying
case-specific configuration. The fixed projected file is present, so NGINX
serves it in the original request context. Upstream cases replace that probe
location directly with their existing unbuffered proxy configuration. The
connector module and its deliberate new-context behavior after genuine
internal redirects are not changed.

## Changed files

- `ci/runtime/lifecycle/run-nginx-lifecycle-sequences.py`
- `tests/test_nginx_sequence_driver.py`
- `reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.md`
- `reports/audits/change-records/CR-20261009-nginx-sequence-static-probe-cleanup.de.md`

## Commands executed

Commands used RTK in the isolated Parent or Framework worktree; temporary data
remained under `/var/tmp/codex/ModSecurity-conector`.

- RED: Parent unittest
  `tests.test_nginx_sequence_driver.DriverTests.test_static_sequence_probes_do_not_create_internal_redirect_contexts`;
  exit 1 with ten failing non-upstream configurations that still contained
  `try_files $uri /index.html;`.
- GREEN: the same focused unittest; exit 0, one test.
- Parent `tests.test_nginx_sequence_driver tests.test_nginx_sequence_driver_phases`;
  exit 0, 28 tests.
- Parent driver-table contract with the exact Framework root; exit 0, seven
  tests. Expanded sequence, transport, dispatcher, H1 protocol and selected
  runner/authority wiring matrix; exit 0, 90 tests.
- Framework `tests.no_crs.test_nginx_native_operation_bundle`; exit 0, 26
  tests. Its exact-one cleanup rejection remains unchanged.
- Parent cleanup/redirect neighbor command ran 21 tests but exited 1 because
  the unchanged `NginxErrorPageInterventionTests` C fixture lacks a stub for
  the previously introduced `ngx_http_modsecurity_request_completion_log_event`;
  the source-only redirect-context assertion and the other 20 tests passed.
- Native `ci/tools/new-change-record.py create` generated this pair from the
  exact base; exit 0.
- Change Record check, 30 Change Record/sequence tests, bilingual-doc check and
  repository link check; all exit 0.
- Full Parent `make lint` in a fresh external build root; exit 0, no
  `SKIPPED`, failure, error or traceback marker. Retained log SHA256 is
  `6eac50fee96f663af17c336c4d9f81a94030904c6f788abcdee3e0053b969906`.
- `rtk proxy git diff --check`; exit 0 after the implementation slice.

## Security impact

The change removes an unintended internal redirect from controlled runtime
fixtures and therefore prevents an abandoned extra transaction context from
being mistaken for one logical probe transaction. It does not relax event,
cleanup, path, projection, privilege, source, or evidence validation. The
Root-master/nobody-worker boundary and product handling of genuine redirects
remain intact.

## Runtime evidence

R10 is retained as failure evidence: one real HTTP 200 request had master UID
0, worker UID 65534, verified process/listener cleanup, then emitted a normal
cleanup followed by `common_return=-8` / `cleanup_incomplete` under the same
transaction ID. No post-fix runtime has run yet, so no local or Canonical PASS
is claimed.

## Known limitations

The unit test proves generated configuration, not live NGINX redirect behavior.
Only H1 is in scope. R10 did not produce a Canonical `result.json` because
native artifact retention failed first.

## Remaining risks

A fresh exact-head build and isolated Root-master/nobody-worker request must
prove one cleanup per transaction. Further independent Required-record defects
may appear after the first R10 retention failure is removed. The neighboring
pre-existing C fixture compilation failure remains separately visible.

## Checks not run and rationale

Fresh NGINX build, post-fix runtime, Canonical finalization, current-head CI,
Sonar and delivery have not yet run because this record captures the
pre-commit implementation slice. Ruff is not installed as a separate local
tool; repository-native `make lint` passed. Protected Exact-Head remains
blocked by its independently missing trusted-base, runner, environment and
administrative Host-Gate prerequisites.

## Final diff and review status

The current four-file diff is Parent-only and preserves Framework/MRTS
gitlinks. The focused regression is RED on the base and GREEN after the driver
change; focused, expanded, documentation and full Parent lint gates pass.
Commit, clean-head validation, fresh runtime and delivery review remain in
progress. R10 remains FAIL and is not reused or relabelled.
