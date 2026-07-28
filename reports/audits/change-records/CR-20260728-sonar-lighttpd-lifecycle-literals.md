# Change Record: Parent Lighttpd lifecycle literal deduplication for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260728-sonar-lighttpd-lifecycle-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-lighttpd-lifecycle-literals |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent Lighttpd full-lifecycle runner and its direct contract test, this English/German Change Record pair, and both indexes only. Framework, MRTS, Gitlinks, workflows, scanner policies, generated reports, and `master` remain unchanged. |
| Tracking | Live baseline Parent SonarQube Cloud items `AZ9cRynjHhV2CayPTPzV` (`shelldre:S1192`, `%{http_code}`, 8 uses) and `AZ9cRynjHhV2CayPTPzW` (`shelldre:S1192`, `1,200p`, 6 uses). Neither item is claimed externally closed before a fresh exact-head pull-request analysis. |

## Motivation and problem statement

The Parent Lighttpd full-lifecycle runner repeated two fixed command literals:
the HTTP status formatter used by its existing `curl --write-out` probes and
the bounded `sed -n` diagnostic program used by existing failure paths. The
repetition is the live baseline for the two selected `shelldre:S1192` items.

This is a literal-only maintenance refactor. It must retain every request,
expected status comparison, error branch, trap, cleanup action, and
fail-closed exit while giving each fixed string one file-local owner.

## Acceptance criteria

- The runner has exactly one unconditional, non-exported declaration of each
  fixed literal, and all selected uses expand the value only as one quoted
  command argument.
- The direct source contract proves one declaration each, eight
  `--write-out "$HTTP_STATUS_FORMAT"` uses, six
  `sed -n "$DIAGNOSTIC_LINES"` uses, no legacy selected literal invocation,
  no export, and the existing lifecycle controls and status expectations.
- Shell syntax, the focused no-host contract suite, and scoped source/test
  whitespace validation report only their observed successful results.
- This complete English/German Change Record pair and both indexes describe
  the same facts, technical literals, limitations, and delivery state.
- No external issue closure, hosted check, Ready-for-review transition,
  Framework/MRTS/Gitlink/workflow/scanner-policy/generated-report change,
  merge, or `master` update is claimed.

## Implementation decision and rationale

The runner unconditionally initializes these non-exported values before its
helper functions:

```sh
HTTP_STATUS_FORMAT='%{http_code}'
DIAGNOSTIC_LINES='1,200p'
```

Each selected status probe now uses `--write-out "$HTTP_STATUS_FORMAT"`, and
each selected bounded failure diagnostic now uses
`sed -n "$DIAGNOSTIC_LINES"`. The values remain fixed internal shell data;
they are neither caller-environment inputs nor request/status-derived values.
The refactor changes no request construction, status expectation, control
flow, redirection, trap, cleanup, or failure behavior.

The direct contract test pins the declarations before their uses, the exact
eight/six use counts, quoted-only use form, lack of export, absence of the
legacy selected literal invocations, existing traps, and all existing status
comparisons.

## Changed files

- `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`
- `connectors/lighttpd/tests/test_patched_host_contract.py`
- `reports/audits/change-records/CR-20260728-sonar-lighttpd-lifecycle-literals.md`
- `reports/audits/change-records/CR-20260728-sonar-lighttpd-lifecycle-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or control | Result |
| --- | --- |
| `sh -n connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | passed. |
| `env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 python3 -B -m unittest -v connectors.lighttpd.tests.test_patched_host_contract` | passed: 17 tests; root rerun completed in 0.244 seconds and the worker run completed in 0.251 seconds. |
| Scoped source/test `git diff --check` | passed. |
| Direct source readback | passed: one declaration of each value, eight `--write-out "$HTTP_STATUS_FORMAT"` uses, and six `sed -n "$DIAGNOSTIC_LINES"` uses. |
| Independent focused shell/HTTP review | `already_safe` for the fixed-literal refactor. |
| Exact-candidate documentation overlay | passed: Parent bilingual documentation and repository-path checks, plus Framework documentation-link checks, against a disposable Parent copy and read-only archive of the Parent-pinned Framework revision. |

## Tests and actual results

The 17-test focused suite is no-host source-contract evidence. Its added
contract checks that both declarations are unconditional and non-exported,
precede all selected uses, and remain the only occurrence of their respective
literal after the declarations are removed. It also preserves the existing
`set -eu`, cleanup traps, synchronized-client error path, result failure
check, and all eight expected status comparisons.

The syntax and scoped whitespace results are local static evidence only. They
do not exercise a patched Lighttpd host or replace a future exact-head
SonarQube Cloud analysis.

## Security impact

The selected runner contains shell commands, HTTP requests, diagnostics, and
lifecycle cleanup, but this record does not change that security boundary. The
fixed-literal refactor preserves the invariant that `%{http_code}` and
`1,200p` are unconditional, internal, non-exported values expanded only as
quoted command arguments. No caller environment, request, response status, or
control data can select either value.

The independent focused shell/HTTP review classified the refactor
`already_safe`. It found no new security finding and no change to requests,
status handling, control flow, cleanup, or fail-closed behavior.

## Runtime evidence

No real patched-Lighttpd host runtime was run. The local suite reads and
checks source contracts without starting Lighttpd, loading a module, or
exercising a host HTTP lifecycle. No generated report or runtime evidence was
created or changed.

## Known limitations

The static source-contract evidence cannot prove runtime behavior on a real
patched Lighttpd host. Exact-candidate bilingual, repository-path, and
Framework-link validation passed in a disposable overlay that used the
Parent-pinned Framework revision without changing a Framework checkout. No
task delivery branch, commit, push, pull request, Ready-for-review transition,
merge, or `master` evidence exists yet for this candidate.

## Remaining risks

An exact-head external analysis is still required before either live baseline
SonarQube Cloud item can be described as absent or externally closed. A future
real patched-Lighttpd host run is still needed to add runtime evidence; the
present local checks deliberately do not make that claim.

## Checks not run and rationale

- The real patched-Lighttpd host runtime was not run. It requires the separate
  patched host/module prerequisites and is outside this literal-only
  no-host validation scope.
- `make check-doc-links` remains `not_run`: it depends on `check-framework`
  and would materialize the Framework, which is outside the assigned
  Parent-documentation scope. Its underlying Parent bilingual/path and
  Framework-link checks instead passed in the exact-candidate disposable
  overlay using the read-only Parent-pinned Framework archive.
- No exact-head hosted check or SonarQube Cloud analysis was run because no
  task delivery branch, commit, push, or pull request evidence exists yet.

## Final diff and review status

This record is written before any task delivery evidence. The observed local
runner/test validation and the focused shell/HTTP review passed as recorded
above. The record does not state that `AZ9cRynjHhV2CayPTPzV` or
`AZ9cRynjHhV2CayPTPzW` is externally closed, and it does not claim a branch,
commit, push, pull request, Ready-for-review transition, merge, or `master`
state. Only the scoped Parent runner/test and this bilingual traceability/index
set are in scope.
