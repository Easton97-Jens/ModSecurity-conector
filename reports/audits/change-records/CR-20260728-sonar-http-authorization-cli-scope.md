# Change Record: Parent HTTP authorization CLI counter scope for SonarQube Cloud c:S5955

**Language:** English | [Deutsch](CR-20260728-sonar-http-authorization-cli-scope.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-http-authorization-cli-scope |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent `common/runtime/http_authorization_service.c`, this English/German Change Record pair, and the Change Record indexes. Framework, MRTS, both gitlinks, workflows, scanner policy, generated reports, and connector behavior remain unchanged. |
| Finding linkage | SonarQube Cloud code smell `AZ9MwjL6-bUaKQ_zSGBL`, rule `c:S5955`, at `parse_cli` line 110. |

## Motivation and problem statement

The shared HTTP authorization-service CLI parser declared its loop counter
outside the only loop that uses it. SonarQube Cloud reports this as `c:S5955`.
The parser is shared by Parent authorization-service wrappers, so the change
must retain all argument consumption, timeout-bound enforcement, and
invalid-input rejection exactly.

## Acceptance criteria

- The counter is declared only in the C17 `for` initializer.
- The CLI grammar, `argv[++index]` consumption, parsing order, return paths,
  and `AUTH_CONNECTION_TIMEOUT_*` bounds remain unchanged.
- The timeout/invalid-input smoke passes with both available C17 compilers
  under `-std=c17 -Wall -Wextra -Werror` using task-owned external outputs.
- Focused Parent source-contract validation and whitespace validation pass.
- No hosted closure, Ready-for-review transition, merge, master update,
  Framework/MRTS change, Gitlink update, or scanner-policy change is claimed.

## Implementation decision and rationale

The only source change removes the standalone `int index;` declaration and
uses `for (int index = 1; index < argc; ++index)`. C17 supports the loop-local
declaration. The counter is not used after the loop, so its initialization,
condition, increments, and all indexed accesses remain identical.

No helper, parser rewrite, command-line option, timeout default, timeout
maximum, allocation, socket operation, or authorization decision changes.

## Security impact

This is a behavior-preserving maintainability correction adjacent to an
authorization-service parser, not a validated security finding. The unchanged
legitimate controls are ordered `argv[++index]` value consumption, invalid
numeric rejection, zero-timeout rejection, and the configured maximum timeout
bound. Focused review found no changed authentication, authorization, request,
network, filesystem, or command-execution path.

## Changed files

- `common/runtime/http_authorization_service.c`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `make check-http-authorization-service-timeout` with GCC, explicit task-owned `TMPDIR`, `VERIFIED_RUN_ROOT`, `VERIFIED_BUILD_ROOT`, and `BUILD_ROOT` | passed; the smoke compiled the changed translation unit with `-std=c17 -Wall -Wextra -Werror` and exercised stalled requests, drip headers, and zero-timeout rejection. |
| `make check-http-authorization-service-timeout` with `CC=clang` and the same explicit C17 flags and isolated roots | passed. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | passed, 10 tests. |
| `git diff --check` | passed; no output. |

## Runtime evidence

The timeout smoke is a focused local service-control test. It is not host
connector runtime evidence, does not start Traefik or Envoy, and does not make
a claim about a full deployment.

## Checks not run and rationale

- Exact-PR-head GitHub checks and SonarQube Cloud analysis are pending the
  normal task-owned Draft PR cycle.
- Full connector matrices and host-runtime suites are not applicable to this
  lexical parser-scope change and were not used as a substitute for the
  focused authorization-service control.

## Known limitations

SonarQube Cloud is the authority for removing `AZ9MwjL6-bUaKQ_zSGBL`; local
C17 compilation cannot prove the hosted rule disposition. The project-wide
652-issue and duplicate-line backlog remains outside this one issue.

## Remaining risks

The correction deliberately leaves the existing parser design unchanged. Any
future functional CLI change must separately re-evaluate argument ordering,
timeout policy, and authorization-service wrapper behavior.

## Final diff and review status

The source correction was committed as `8fa2f2cf8e8c6130ee1530f97008284c63bf298b`
and pushed to its task branch before this required documentation amendment.
The reviewed source diff is limited to the loop-counter scope correction.
This record and its index entries are the pending documentation amendment;
no pull request, hosted result, review, Ready-for-review transition, or merge
is claimed yet.
