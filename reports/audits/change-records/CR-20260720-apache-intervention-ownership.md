# Change Record: Apache intervention ownership cleanup

**Language:** English | [Deutsch](CR-20260720-apache-intervention-ownership.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260720-apache-intervention-ownership` |
| Date (UTC) | `2026-07-20` |
| Base revision | `929fe60dfca30787947027e5bd49003581a5b080` |
| Boundary | Parent Apache connector source, Parent source-contract/wiring tests, Parent Change Record/index pair only; Framework, MRTS, dependencies, and both gitlinks remain unchanged. |
| Finding linkage | `FND-PARENT-0043`; `CAND-PARENT-APACHE-INTERVENTION-LEAK-0001`. |

## Motivation and problem statement

`process_intervention()` receives `ModSecurityIntervention` values from
libmodsecurity. The pre-change helper did not release nonzero intervention
results. Its redirect branch also passed `intervention.url` to Apache's
non-copying `apr_table_setn()`, so any cleanup correction must first copy that
value into request-owned storage. Replacing a null intervention log with a
static literal by writing the intervention field would likewise be unsafe when
the native cleanup releases that field.

## Acceptance criteria

- Every nonzero `msc_intervention()` result reaches exactly one
  `msc_intervention_cleanup()` call after Apache has copied values it retains.
- The no-intervention (`z == 0`) path preserves the existing direct allow
  return and does not call native cleanup.
- The cached intervention log and redirect URL are copied into `r->pool` before
  Apache retains them; `Location` never retains the native-owned URL pointer.
- A null log uses a local fallback pointer without overwriting the native-owned
  intervention field.
- A focused source-contract regression covers cleanup, no-intervention,
  fallback-log, redirect-ownership, and C17-source-list invariants.
- No Framework/MRTS source, gitlink, dependency, scanner configuration, or
  external alert disposition changes in this patch.

## Implementation decision and rationale

The correction uses local `log`, `location`, `result`, and `z` variables in
`process_intervention()`. It copies the log into `r->pool`, copies a redirect
URL into `r->pool` before `apr_table_setn()`, and uses one `cleanup:` path for
every nonzero result. The `z == 0` branch keeps the existing direct allow
return before any Apache value is retained, while nonzero paths return
`result` after native cleanup.

The new source-contract test prevents a later nonzero return path from
bypassing cleanup, requires the direct zero-result return, prevents direct
retention of `intervention.url`, prevents mutation of `intervention.log` to the
fallback literal, and requires the changed translation unit in the Apache C17
compilation list. The test is wired into a dedicated Make target and the
`lint` aggregate.

## Changed files

- `connectors/apache/src/mod_security3.c`
- `tests/test_apache_intervention_cleanup.py`
- `Makefile`
- `ci/checks/connectors/apache/check-apache-c-standards.sh`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Result |
| --- | --- |
| `rtk make check-apache-intervention-cleanup` | passed: 5 focused source-contract tests. |
| `rtk make check-apache-c-standard-wiring` | passed: Apache C-standard script and Makefile wiring checks. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_apache_request_transaction_cleanup` | passed: 5 existing Apache transaction-ownership contract tests. |
| `rtk make check-apache-request-transaction-cleanup` | static Python portion passed (5 tests); native helper then reported missing `apxs`/usable Apache headers and Make returned `2`. |
| `rtk run 'APACHE_C_STANDARDS_OUT=/var/tmp/codex/ModSecurity-conector/runs/20260720T225753Z-apache-intervention-cleanup-40c97373/apache-c17 make check-apache-c17'` | blocked environment: runtime-component preparation failed closed before compilation because required local Apache/libmodsecurity prerequisites were unavailable; the wrapper returned `2`. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs` | passed: 11 bilingual-checker unit tests. |
| `rtk make check-bilingual-docs` | blocked by existing links into the absent Framework gitlink and returned `2`; it reported no error for this Change Record pair. |
| `rtk make check-doc-links` | blocked by the same existing absent-Framework targets and returned `2`; no changed Apache Change Record link was reported. |
| `rtk git diff --check` | passed: no whitespace errors in the task worktree. |

## Security impact

This is a native lifecycle and availability remediation. A remote request that
matches a normal disruptive ModSecurity rule can cause Apache to process an
intervention. The original nonzero path leaked native intervention-owned
buffers. The correction releases that native ownership and preserves Apache
behavior by copying retained values first, so the cleanup cannot create a
redirect dangling-pointer path. The patch does not assert a measured leak rate,
production exposure, or a completed native sanitizer run.

## Runtime evidence

Not available in the current isolated Parent worktree. The host lacks the
Apache development and libmodsecurity prerequisites needed to compile and run
the affected translation unit, and no ASan/LSan Apache repetition was run.
The successful tests establish source-level ownership and control-flow
invariants only.

## Protocol assessment

`process_intervention()` is transport-agnostic host lifecycle code, but the
affected Apache boundary remains transport-adjacent. No wire-protocol behavior
is claimed from the source tests:

- HTTP/1.1: `not_run`; no native Apache runtime was available.
- HTTP/2: `not_run`; no native Apache runtime or HTTP/2 configuration was
  available.
- HTTP/3: `not_run`; no native Apache runtime or HTTP/3 configuration was
  available.

The patch makes no H1/H2/H3 compatibility claim beyond preserving the source
level intervention ownership behavior.

## Checks not run and rationale

- Native Apache/APR/libmodsecurity C17 compilation and ASan/LSan repetition are
  blocked by missing `apxs`, usable Apache/APR headers, and libmodsecurity
  runtime/build prerequisites. Failed-closed runtime preparation was retained
  as environment evidence; it was not bypassed.
- At the `2026-07-20T23:43:04Z` readback, exact PR #72 head
  `c761a13cb5b4dd3717018960aa03d928758fd21d` had six required GitHub checks
  passed, a passing SonarQube Cloud Quality Gate, zero new issues, zero new
  hotspots, and `0.0%` duplication. The PR was Draft/open with no submitted
  review. These facts do not transfer to a subsequent SHA; that SHA requires
  its own CI, Sonar, review, and resulting-master evidence.
- The full `lint` aggregate was not run because its existing Framework and
  native Apache prerequisites are absent in this isolated worktree; the newly
  wired targeted control was run directly and passed.
- No Framework or MRTS test was run because neither boundary is part of this
  Parent-only correction.

## Known limitations

The regression is structural rather than a native Apache process test. It
cannot measure allocation behavior or prove an absence of leaks under repeated
requests. The canonical finding remains open until an exact PR head with all
required review and the resulting master are revalidated; native sanitizer
evidence remains an environment-dependent follow-up requirement.

## Remaining risks

The current host does not prove the full host/connector/libmodsecurity ABI path
or sanitizer behavior. Other independently tracked Apache, NGINX, Sonar,
Scorecard, Dependabot, OSV, and secret-scanning items remain outside this
narrow patch. No risk is accepted, alert is dismissed, or scanner control is
weakened.

## Final diff and review status

The source correction is committed and pushed as
`23b84324e1db8fe13af48ddcc8bf04caae26e30c` on
`agent/apache-intervention-ownership-20260720`; its test-only Sonar follow-up
is `c761a13cb5b4dd3717018960aa03d928758fd21d`. The latter is Draft PR #72's
observed head and preserves the direct zero-result return. Completion requires
a security diff review, protected pull-request validation, normal merge, and
exact resulting-master revalidation. The absent native prerequisites are
recorded as a blocker, not a passing test result.
