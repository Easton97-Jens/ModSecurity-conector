# Change Record: PR #369 SonarQube Cloud S1820 sidecar state remediation

**Language:** English | [Deutsch](CR-20260919-pr369-sonarqubecloud-s1820.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260919-pr369-sonarqubecloud-s1820 |
| Date (UTC) | 2026-09-19 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Predecessor PR #369 head | `c8b5faf2491ed2e4489ad8298a1083557bfba349` |
| Finding | `FND-SONAR-0089`; Sonar issue `AaCrebhgrY5Yi_GLZMw7` / `c:S1820` |
| User authorization | “das muss null sein und gib mir eine übersicht welche findings damit behoben sind” |
| Delivery status | The scoped normal implementation follow-up was pushed to the existing Parent Draft PR #369. Its exact SHA `623546bb3bfb8231d92f566aa9704c1928d7ed29` passed SonarQube Cloud with zero open PR issues. No merge, auto-merge, direct `master` write, Framework/MRTS/Gitlink change, control weakening, or branch deletion is authorized. |

## Motivation and problem statement

Authenticated SonarQube Cloud PR #369 readback reported one open MAJOR
`CODE_SMELL`: `sidecar_exchange_state` had 24 direct fields where `c:S1820`
allows at most 20. Although the Quality Gate was `OK`, the requested PR-scoped
zero-open-issue state was not achieved.

## Acceptance criteria

- `sidecar_exchange_state` has at most 20 direct fields without changing its
  endpoint, transaction, error, commit, or phase-order behavior.
- The C17/Werror source-contract and legitimate loopback endpoint/allow
  controls pass.
- The exact successor PR #369 analysis has zero `OPEN`/`CONFIRMED` issues and
  no `AaCrebhgrY5Yi_GLZMw7` record.
- No `NOSONAR`, exclusion, acceptance, scanner, workflow, rule, or
  Quality-Gate change is made.

## Implementation decision and rationale

The repair introduces `sidecar_request_endpoints` for the four kernel-derived
endpoint values and `sidecar_exchange_dependencies` for immutable `options`
and `runtime` references. `sidecar_exchange_state` now has exactly 20 direct
fields. Only member access paths change; initialization and all parser,
decision, error, response-commit, late-intervention, and fail-closed branches
remain in the prior order.

## Security impact

This is a maintainability repair, not a security vulnerability. The relevant
preservation invariant is that `getpeername()` and `getsockname()` produce
validated IPv4 endpoint data before Common Runtime transaction begin. The
change neither adds a request-controlled fallback nor alters socket,
configuration, parser, or authorization behavior.

## Changed files

- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `reports/audits/change-records/CR-20260919-pr369-sonarqubecloud-s1820.md`
- `reports/audits/change-records/CR-20260919-pr369-sonarqubecloud-s1820.de.md`

The existing Change-Record index pair was already modified by unrelated work
and was deliberately not edited or staged by this follow-up.

## Commands executed

| Command or check | Result | Observed result |
| --- | --- | --- |
| RTK-proxied `/usr/local/bin/sonar-with-env` PR #369 issue and Quality Gate readback | passed | One `OPEN`/`CONFIRMED` issue, `AaCrebhgrY5Yi_GLZMw7` / `c:S1820`, was identified; Quality Gate `OK` did not make the issue zero. |
| Exact implementation-head SonarQube Cloud readback | passed | GitHub-App check `SonarCloud Code Analysis` completed successfully for `623546bb3bfb8231d92f566aa9704c1928d7ed29` at `2026-09-19T10:28:59Z`; the approved wrapper returned zero `OPEN`/`CONFIRMED` PR #369 issues and Quality Gate `OK`. |
| Direct `sidecar_exchange_state` field-count check | passed | Exactly `20` direct fields after the refactor. |
| `StockSidecarSourceContractTest` | passed | 17 tests, including C17/Werror source harnesses. |
| C17/Werror Sidecar build with `CC=cc` | passed | External-root build completed. |
| C17/Werror Sidecar build with `CC=clang` | passed | Independent external-root build completed. |
| Full `self-test-lighttpd-stock-sidecar` | failed | 33/34 tests passed; immediate client-reset event case did not observe its event. |
| Same immediate-reset case compiled from unmodified `HEAD` source | failed | Identical empty-event result, so this is not attributed to this refactor. |
| `git diff --check` for the Sidecar candidate | passed | No whitespace errors. |

## Runtime evidence

The full loopback suite's allow path and
`test_loopback_endpoint_metadata_reaches_common_runtime` passed with the
candidate binary. This is bounded loopback evidence for preservation of the
kernel-derived endpoint invariant; it is not real stock-lighttpd backend or
hosted PR evidence.

## Checks not run and rationale

The real stock-lighttpd backend, full connector matrix, and broader hosted
reviews were not run as part of this focused remediation. The exact
implementation-head SonarQube Cloud analysis did run and passed; no result is
claimed for unrelated PR checks.

## Known limitations

The complete Sidecar module remains at 33/34 because its immediate-client-reset
event case fails identically on unmodified `HEAD`. This known separate runtime
limitation remains `FND-PARENT-1091`; it is not weakened, accepted, or treated
as solved by `FND-SONAR-0089`.

## Remaining risks

`FND-SONAR-0089` is verified for implementation SHA
`623546bb3bfb8231d92f566aa9704c1928d7ed29`: SonarQube Cloud reported zero
open PR issues without altered Sonar controls. The documentation-only
follow-up does not change source behavior; broader PR verification remains a
separate exact-head decision.

## Final diff and review status

The reviewed product delta is data-only and scoped to the private Sidecar
state. The implementation commit passed its exact-head SonarQube Cloud check
with zero `OPEN`/`CONFIRMED` issues. The local `.codex` finding and its
payload-safe evidence record are intentionally unversioned and do not replace
this Change Record.
