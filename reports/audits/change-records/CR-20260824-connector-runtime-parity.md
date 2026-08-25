# Change Record CR-20260824: Connector runtime-parity baseline

**Language:** English | [Deutsch](CR-20260824-connector-runtime-parity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260824-connector-runtime-parity` |
| Date (UTC) | `2026-08-24` |
| Base revision | `a6b4ced4876a19666f7c7203ed9e719674c69ec1` |
| Scope | Parent follow-up only: five connector-source/test files and this paired Change Record. No task-owned Framework/MRTS/Gitlink, workflow, branch-rule, required-check, CI, dependency, or global-toolchain change. A later external merge of `master` into the existing PR branch is not part of this Change Record. |

## Motivation and problem statement

The connector matrix required one evidenced local baseline for Apache, NGINX,
HAProxy HTX, HAProxy SPOE/SPOP, Envoy ext_authz, Envoy ext_proc, Traefik
forwardAuth, Traefik Native UDS, Stock lighttpd, and Patched lighttpd. The
Stock-lighttpd source incorrectly hid a shared response helper behind the
patched stream-hook ABI guard, while Stock invokes that helper from its normal
response-start path. The NGINX harness also required a real local
master/worker lifecycle proof rather than treating sandbox single-process mode
as production-equivalent. HAProxy cleanup needed to remove its task-owned
runtime markers after verified child termination.

## Acceptance criteria

- Keep Stock-lighttpd references limited to APIs declared by its Stock ABI;
  retain Patched-only stream functions behind the compile-time ABI guard.
- Build Stock and Patched lighttpd separately with the locked `1.4.85` host;
  retain their distinct Allow and Block connector paths.
- Require a normal NGINX master/worker lifecycle with a non-root worker,
  readiness, connector Allow and Block traffic, reload replacement, orderly
  shutdown, and artifact cleanup. Sandbox special mode is not normal-worker
  evidence.
- Keep each of the ten connector paths independently evidenced for source
  identity, build, configuration validation, start, readiness, Allow, Block,
  shutdown, and cleanup.
- Preserve CI and its configuration unchanged.

## Implementation decision and rationale

- Shared Lighttpd response-header helpers, including
  `mod_msconnector_emit_host_transaction_id`, are compiled outside
  `LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION`; only patched stream-body
  hooks remain inside that guard. This is an ABI-correct scope change, not a
  warning suppression or a Stock stub.
- A focused static contract test asserts the split between shared and
  patched-only Lighttpd helpers.
- The HAProxy smoke harness deletes only its explicit PID and readiness files,
  and only after its child-process shutdown checks.
- The NGINX lifecycle harness treats disabled lifecycle mode as invalid in a
  normal run, records expected initial and replacement workers, and fails
  closed when tracked processes, listeners, UDS paths, or runtime artifacts
  remain after shutdown.
- The static NGINX lifecycle contract is a repository-owned `tests/` contract,
  not a connector-local executable test. Moving it preserves all seven
  master/worker assertions while leaving the intentionally prohibited
  `connectors/nginx/tests/` directory absent.

## Security impact

This work affects untrusted HTTP request paths and local process boundaries.
The changes preserve real policy decisions: a legitimate request reaches the
connector and is allowed, while a rule-triggering request reaches the same
connector path and is blocked. No mock replaces a host or agent. The changes
do not weaken authorization, request validation, compiler diagnostics,
isolation, cleanup checks, or CI controls. Remaining P1--P4 feature work is
not claimed complete by this baseline.

## Changed files

- `connectors/lighttpd/module/mod_msconnector.c`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_master_worker_lifecycle_contract.py`
- `reports/audits/change-records/CR-20260824-connector-runtime-parity.md`
- `reports/audits/change-records/CR-20260824-connector-runtime-parity.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| Separate Stock-lighttpd strict C17 module build against locked `lighttpd-1.4.85` | Passed; module produced in the isolated Stock build root. |
| Separate Patched-lighttpd strict C17 module build against locked `lighttpd-1.4.85` | Passed; module produced in the isolated Patched build root. |
| `python3 -m unittest connectors.lighttpd.tests.test_patched_host_contract` | Passed: 36 tests, 2 skipped. |
| `sh -n connectors/haproxy/harness/run_haproxy_smoke.sh` | Passed. |
| Final Stock-lighttpd host run | Passed: config validation, Allow `200`, Block `403` / rule `1000001`, connector event, orderly foreground-host shutdown, and cleanup. An opt-in Allow response carried `X-Msconnector-Host-Transaction-Id`. |
| Final Patched-lighttpd host run | Passed: config validation, Allow `200`, Block `403` / rule `1000001`, connector event, orderly foreground-host shutdown, and cleanup. The patched host still exports both entity-body hook symbols; this run makes no P4 claim. |
| Final HAProxy HTX run | Passed: real overlay host config/readiness, Allow `200`, Block `403`, and `processes_stopped=yes`. |
| Final HAProxy SPOE/SPOP runs | Passed separately: real HAProxy `-db` + SPOA agent + Python backend Allow `200` and Block `403`; all four task-owned PID/readiness markers were absent after each run. |
| `python3 -m unittest tests.test_nginx_master_worker_lifecycle_contract` | Passed: 7 tests. |
| `sh -n connectors/nginx/harness/run_nginx_smoke.sh` | Passed. |
| Final NGINX transient-service runs | Passed: separate Allow `200`, Block `403`, and forced-quit/`TERM` fallback Allow `200`; each config-tested, reached readiness, used root master plus `nobody:nogroup` worker, reloaded to a distinct worker, and completed cleanup with exit `0`. |
| Lifecycle-disabled NGINX negative control | Passed: normal run exited `1` before host start. |
| `git diff --check` on the final delivery diff | Passed. |
| Follow-up exact `Check common scaffold` command in initialized Base and corrected PR worktrees | Base and corrected PR passed; the original PR location stopped at `test ! -d connectors/nginx/tests`. |
| Follow-up exact `Check NGINX scaffold` command in initialized Base and corrected PR worktrees | Base and corrected PR passed; the original PR location stopped at the same prohibited-directory predicate. |
| Follow-up exact pinned-revision command in initialized Base and PR worktrees | Reproduced inherited failure in both: Parent comparison passed, then Framework `7bf8b7cb...` differed from fixed workflow pin `c40e924e...`; no host stage was reached. |
| Follow-up focused Lighttpd and NGINX static contracts | Passed: 43 tests total; 2 namespace-gated Lighttpd skips. |
| Follow-up separate Stock-lighttpd strict C17 module build and config validation | Passed with `-Wall -Wextra -Werror` against locked `1.4.85`; real Stock `lighttpd -tt` loaded the newly built module. |
| Follow-up separate Patched-lighttpd strict C17 host/module build and config validation | Passed with locked `1.4.85` and patch SHA-256 `e00d3892...fa8b5`; the patched host retained both required hook exports and completed real `lighttpd -tt` validation. |

## Runtime evidence

The sealed main matrix is retained at
`/var/tmp/codex/ModSecurity-conector/task-connector-runtime-parity-20260824/runs/20260824T103505Z-connector-runtime-parity-61be62e2`.
Its manifest SHA-256 is
`cdfaaab244fd580f97f876de190c4a6d4c809ef56a839f96808a54e42fe9e2e4`.
The separately retained Traefik Native UDS evidence is at
`/var/tmp/codex/ModSecurity-conector/t.aeQFSv/runs/20260824T122139Z-traefik-native-uds-41fdda3c`.

The final exact-source NGINX receipt is retained at
`/var/tmp/codex/ModSecurity-conector/connector-runtime-parity-delivery-20260824/evidence/final-nginx-master-worker-verification.md`
with SHA-256
`64dfe67c16c6b6b6b49fb9c921b2a689fa43ca0b5319148ee8d092d0376703f4`.
Its harness SHA-256 is
`301323aa66255ae04e7be1d2e2620c285371a8039f2c9d18039c984cab7d8af9`
and lifecycle-test SHA-256 is
`df3dfe851459258897389b4df442afbc8c33331f99d51c1897c67f2137bee561`.
The current changed-connector rerun receipt is retained beside it at
`final-changed-connector-reruns.md` with SHA-256
`d0e291b695ca605a8670e36493bb1472deca91227d5839d6d0b985297ffcde2c`.

The locked host versions are Apache HTTP Server `2.4.68`, NGINX `1.31.4`,
HAProxy `3.2.22`, Envoy `1.39`, Traefik `3.7.11`, and lighttpd `1.4.85`.
The runtime receipts show distinct real-host Allow (`200`, rule `2103`) and
Block (`403`, rule `2101`) requests, readiness, shutdown, and cleanup for all
ten named paths; NGINX additionally shows master/root, worker/non-root,
reload replacement, lifecycle-disabled rejection, and fallback cleanup
behavior.

## Checks not run and rationale

- No CI or workflow configuration was changed by this follow-up, and no hosted
  check was triggered manually. Opening or updating the pull request automatically
  triggered the repository’s existing pull-request workflows. Their actual
  status is recorded separately from the local runtime evidence.
- At the original Draft PR head, the automatic common and NGINX scaffold
  checks failed because this static Parent contract was placed in the
  prohibited `connectors/nginx/tests/` path. The automatic with-CRS/no-MRTS
  runtime jobs failed before host execution at the inherited Framework-pin
  comparison; that Base/PR Gitlink mismatch is separate from this local
  runtime evidence. The later external `master` merge updated that inherited
  pin/Gitlink tuple; its automatic hosted outcomes remain separate evidence.
- No global dependency installation or mutable host-source fallback was used.
- `make check-bilingual-docs` and `make check-doc-links` were executed after
  the Change Record headings were corrected. Both remain blocked in this fresh
  Parent worktree because its pinned Framework Gitlink is intentionally
  uninitialized and existing repository links therefore have no local target.
  No Framework checkout, source change, Gitlink update, or link workaround was
  authorized. The checks reported no remaining Change-Record-heading failure.

## Known limitations

The evidence roots are retained local evidence, not versioned source files.
The final NGINX receipt names the exact final harness and test hashes; older
POSIX receipts remain historical evidence only. This record also does not
claim completion of future P1--P4 connector work.

## Remaining risks

The isolated test hosts do not prove deployment-specific production policies,
namespace restrictions, or operator configuration. The task deliberately
retains fail-closed lifecycle and cleanup checks so an unavailable normal NGINX
worker environment cannot be misreported as a successful production model.
The two repository-wide documentation checks require a populated pinned
Framework Gitlink and therefore remain environment-blocked, not waived.

## Final diff and review status

The user authorized an isolated follow-up commit and normal push only on the
existing Draft PR #339 branch. No merge, direct `master` push, Framework/MRTS
modification, Gitlink update, CI or workflow configuration change by this
follow-up, manual hosted-check trigger, or protected-check outcome is
authorized or asserted.
