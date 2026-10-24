# Change Record: CR-20261009-nginx-cleanup-pool-lifetime

**Language:** English | [Deutsch](CR-20261009-nginx-cleanup-pool-lifetime.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261009-nginx-cleanup-pool-lifetime |
| Date (UTC) | 2026-10-09 |
| Base revision | `240d1b32c9d1ea6e5fcbf23a5e1371090f92a8ee` |

## Motivation and problem statement

NGINX clears `r->pool` before request-pool cleanup callbacks. Cleanup previously allocated method/URI strings through `ngx_http_modsecurity_event_request_metadata` using this cleared pointer. The motivating real run reported worker `SIGSEGV 11` and zero cleanup events. A deterministic C fixture independently proves the invalid allocation.

## Acceptance criteria

Preserve genuine request identity and exactly one truthful cleanup observation without allocation from a cleared pool. Preserve Common/native ordering, errors, strict serialization, URI bounds and query redaction. Reject snapshot failure before transaction admission.

## Implementation decision and rationale

Snapshot exact length-delimited method and original URI during context creation while the pool is live; retain two C-string pointers in the context. Pool storage remains alive throughout cleanup callbacks. Cleanup uses retained identity without consulting `r->pool`. Empty input stays empty; NULL data, overflow and allocation failure reject context creation. Identity belongs to the admitted transaction, even if later internal redirects alter live method data. Existing Common projection and validators stay unchanged. No new source file or SOURCE_MAP entry.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_module.c`
- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_nginx_native_cleanup_bridge.py`
- `reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.md`
- `reports/audits/change-records/CR-20261009-nginx-cleanup-pool-lifetime.de.md`

## Commands executed

Commands used `rtk proxy` in the isolated Parent worktree; `$PARENT_PYTHON` denotes its existing virtual-environment interpreter. Logs and temporary files are external in the task analysis directory `cleanup-pool-lifetime`.

- RED: `$PARENT_PYTHON -m unittest -v tests.test_nginx_native_cleanup_bridge.NativeCleanupBridgeTests.test_destroyed_pool_cleanup_retains_exact_request_metadata_without_allocation`; exit 1, one expected failure: unchanged source attempted NULL-pool allocation; safe fixture returned 19. `red.log`.
- GREEN: `$PARENT_PYTHON -m unittest -v tests.test_nginx_native_cleanup_bridge tests.test_nginx_native_technical_events tests.test_nginx_bounded_event_uri tests.test_nginx_native_intervention_chain tests.test_nginx_request_error_events`; exit 0, 48 tests in 5.098s, no skips. `affected.log`. Actual snapshot/cleanup/phase writer and Common state/serializer run; only host allocation/file-write and native cleanup seams are controlled. Tests cover non-NUL-terminated slices, identity retention after original-byte changes, empty input, allocation/NULL/overflow rejection, pool-cleared reentry, query redaction, long URI projection, native absence and terminal errors.
- `NGINX_C_STD_PROFILE=c17 bash ci/checks/connectors/nginx/check-nginx-c-standards.sh`; exit 0, `PASS: nginx_c_standards c17 compile completed`, all listed sources with `-Wall -Wextra -Werror`. Existing NGINX 1.31.6 generated headers and ModSecurity headers prove compilation only.
- `$PARENT_PYTHON ci/checks/connectors/nginx/check-nginx-common-adoption.py`; exit 0. `adoption.log`.
- `rtk proxy git diff --check`; exit 0.
- Native `ci/tools/new-change-record.py create` generated this pair from the exact base; exit 0.

## Security impact

Removes a request-reachable cleanup allocation from an invalid pool. Metadata remains request-derived; no fabricated events or weakened checks. Snapshot failure prevents admission; retained storage belongs to the existing request pool.

## Runtime evidence

The reported crash motivates the fix. This worker ran no hosted NGINX lifecycle and claims no runtime PASS. Fresh integrated build and Root-master/nobody-worker execution remain required.

## Known limitations

The fixture models pool allocation/clearing rather than executing the full NGINX destructor. Header compilation proves source compatibility, not fresh binaries or hosted cleanup.

## Remaining risks

Independent integration and actual cleanup verification remain required. Two additional strings remain in the request pool until destruction. Framework, MRTS, Required97 selection and canonical validators stay unchanged.

## Checks not run and rationale

No full build, hosted runtime, cache mutation, full repository suite, CI, Sonar, Git delivery or protected-host action by this worker; integration coordinator owns these. Full documentation links require populated Framework paths absent here. Archive structure and bilingual content are checked separately.

## Final diff and review status

Five listed files are handed off for independent integration review with RED/GREEN and C17 evidence. No worker commit or push. Full E2E and delivery remain unverified.
