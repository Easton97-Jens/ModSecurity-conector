# Change Record: CR-20261008-nginx-merge-c17-unused-context

**Language:** English | [Deutsch](CR-20261008-nginx-merge-c17-unused-context.de.md)

Bounded Parent compile fix; compilation is not Exact-Head runtime or coverage proof.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-merge-c17-unused-context |
| Date (UTC) | 2026-10-08 |
| Base revision | `fe43865c03e89c0e8b0e1ae7dfbd5a9e11a7b602` |

## Motivation and problem statement

With `MODSECURITY_DDEBUG=0`, `ngx_http_modsecurity_merge_conf` intentionally does not use `cf`. The real NGINX 1.31.6 / ModSecurity v3.0.17 headers and GCC 15.2.0 reproduced `unused parameter 'cf'` at line 1203 under `-std=c17 -Wall -Wextra -Werror`; native `make check-nginx-c17` exited 2 before the fix.

## Acceptance criteria

The full module must compile with debug disabled and enabled using real configured headers and unchanged strict warnings. Removing the local unused-parameter treatment must restore the compiler failure. Supported debug traces, callback ABI, merge logic, and existing ownership/default contracts must remain intact.

## Implementation decision and rationale

Add a local explanatory comment and `(void) cf;` in the merge callback. This documents the intentionally unused non-debug parameter without changing its type, callback registration, merge operations, or debug macro implementation. No warning suppression, Framework/MRTS/Common source change, selection reduction, or validator change is included.

## Changed files


- `connectors/nginx/src/ngx_http_modsecurity_module.c`: local unused-context treatment.
- `tests/test_nginx_merge_conf_c17.py`: actual full-module compilation, preprocessor debug-trace checks, and removal mutation control.
- `reports/audits/change-records/CR-20261008-nginx-merge-c17-unused-context.md` and `reports/audits/change-records/CR-20261008-nginx-merge-c17-unused-context.de.md`: this complete EN/DE pair, initialized by the native generator.

## Commands executed

Native commands were RTK-wrapped in the Parent task worktree. `make check-nginx-c17` changed from exit 2 to exit 0; the same native check with a fixed external `CC` pass-through adding `-DMODSECURITY_DDEBUG=1` to `/usr/bin/cc` exited 0. `python -m unittest -v tests.test_nginx_merge_conf_c17` ran three tests with explicitly supplied real headers and external `TMPDIR`, exit 0. The mutation compilation returned 1 with the original unused-`cf` diagnosis. Preprocessing confirms merge traces and rule dumps remain present only in supported debug mode.

Compiler: `cc (Ubuntu 15.2.0-16ubuntu1) 15.2.0`. Configured NGINX headers: cache entry `2cd54e97b4f729370661e4fa745420b60e70b3ae4cd4a5790b1fd1d5c1bb351b`, `build/nginx-src`. ModSecurity headers: prefix `bfc407eed25c7a3df0b55a7dadafa832ba0c401f77461ea6371778acb29a0e2e/include`. NGINX release archive SHA256: `974ed5298a5e398e008704ed5db284e655fc270c596493dbccada452448fc9f1`. Exact compiler arguments, header hashes, diagnostics and direct exit records are retained under `/var/tmp/codex/ModSecurity-conector/analysis/nginx-c17-config-header-20261008T041648Z/c17`.

The Parent merge/security/lifecycle focus suite passed 64 tests, exit 0, after an unchanged-test rerun with short external `TMPDIR=/var/tmp/codex/ModSecurity-conector/t-c1708`. The first attempt exited 1 because three assertions encountered Unix socket path-length limits with a longer external temporary path; that initial result is retained. RTK-wrapped `make check-nginx-common-adoption` also exited 0. These results establish their own test layers, not complete lint or runtime coverage.

## Security impact

Strict C17 warnings remain enabled. The change evaluates no pointer contents and alters no configuration validation, projection freshness, containment, trust gate, runtime evidence, or canonical status policy. Required records still require genuine evidence.

## Runtime evidence

No new runtime build, request, lifecycle, or canonical coverage result is claimed by this compile fix. Existing cache headers are compile inputs, not proof that an old module represents the changed source. A later runtime check must rebuild the module with a new native identity.

## Known limitations

Compile regressions are optional when explicit native prerequisites are absent: a SKIP is not verification. Explicitly supplied missing headers fail instead of silently skipping. This host ran the tests with actual configured headers. The independent six configuration targets and duplicate-header target are outside this atomic change; their reusable contract gaps need separately authorized work.

## Remaining risks

Successful compilation does not close missing required runtime records or establish an overall E2E PASS. Full lint remains incomplete, with HAProxy preparation under separate diagnosis. Protected Exact-Head remains blocked on independent trusted-base and administrative prerequisites.

## Checks not run and rationale

No new complete runtime lifecycle, protected workflow, or current-commit remote CI/Sonar result is available for this atomic fix. Full native lint completion is not established. These checks cannot be replaced by the compiler results or historical evidence.

## Final diff and review status

The atomic diff is the local callback treatment, its compiler regressions, and this documentation pair. Native bilingual, repository-path and documentation-link checks passed with exit 0. An independent bounded read-only review found no actionable ABI, debug or regression-test issue. Commit/push and later run outcomes remain separate; no resulting SHA or delivery success is invented here. PR #396 stays Draft.
