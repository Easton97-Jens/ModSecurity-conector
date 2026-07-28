# Change Record: Parent HTTP authorization CLI loop control for SonarQube Cloud c:S5955 and c:S886

**Language:** English | [Deutsch](CR-20260728-sonar-http-authorization-cli-scope.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-http-authorization-cli-scope |
| Date (UTC) | 2026-07-28 |
| Base revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Boundary | Parent `common/runtime/http_authorization_service.c`, this English/German Change Record pair, and the Change Record indexes. Framework, MRTS, both gitlinks, workflows, scanner policy, generated reports, and connector behavior remain unchanged. |
| Finding linkage | SonarQube Cloud code smell `AZ9MwjL6-bUaKQ_zSGBL`, rule `c:S5955`, at `parse_cli` line 110, followed by exact-PR-head code smell `AZ-orCBNFp8FN2qblodn`, rule `c:S886`, at line 109. |

## Motivation and problem statement

The shared HTTP authorization-service CLI parser declared its loop counter
outside the only loop that uses it. SonarQube Cloud reports this as `c:S5955`.
The initial loop-local correction then exposed `c:S886` on the same touched
parser because direct `argv[++index]` expressions also changed the `for`
counter inside its body. The parser is shared by Parent authorization-service
wrappers, so the follow-up must retain argument consumption, timeout-bound
enforcement, and invalid-input rejection exactly while leaving counter updates
in the `for` header.

## Acceptance criteria

- The counter is declared only in the C17 `for` initializer and is modified
  only by that header's update expression.
- The CLI grammar, parsing order, return paths, value consumption, and
  `AUTH_CONNECTION_TIMEOUT_*` bounds remain unchanged.
- Missing values after `--config`, `--listen`, `--max-requests`, and
  `--connection-timeout-ms` are rejected with the existing CLI failure status.
- The timeout/invalid-input smoke passes with both available C17 compilers
  under `-std=c17 -Wall -Wextra -Werror` using task-owned external outputs.
- Focused Parent source-contract validation and whitespace validation pass.
- No hosted closure, Ready-for-review transition, merge, master update,
  Framework/MRTS change, Gitlink update, or scanner-policy change is claimed.

## Implementation decision and rationale

The loop-local C17 declaration remains. An explicit `skip_option_value` flag
preserves the existing two-token option behavior: the option iteration reads
`argv[index + 1]`, validates it where required, and marks the following
iteration as the consumed value. The next iteration clears that flag and
continues, while `++index` remains solely in the `for` header.

This replaces no parser grammar, command-line option, timeout default, timeout
maximum, allocation, socket operation, or authorization decision. It makes
the pre-existing skip explicit rather than mutating the loop counter from an
expression in the branch body.

## Security impact

This is a behavior-preserving maintainability correction adjacent to an
authorization-service parser, not a validated security finding. The unchanged
legitimate controls are ordered option-value consumption, invalid numeric
rejection, missing-value rejection, zero-timeout rejection, and the configured
maximum timeout bound. Focused review found no changed authentication,
authorization, request, network, filesystem, or command-execution path.

## Changed files

- `common/runtime/http_authorization_service.c`
- `ci/checks/common/http_authorization_service_timeout_smoke.c`
- `reports/audits/change-records/README.md` and `README.de.md`
- this English/German Change Record pair

## Commands executed

| Command or control | Actual result |
| --- | --- |
| `make check-http-authorization-service-timeout` with GCC, explicit task-owned `TMPDIR`, `VERIFIED_RUN_ROOT`, `VERIFIED_BUILD_ROOT`, and `BUILD_ROOT` | passed; the smoke compiled the changed translation unit with `-std=c17 -Wall -Wextra -Werror` and exercised stalled requests, drip headers, zero-timeout rejection, and all four missing-option-value rejections. |
| `make check-http-authorization-service-timeout` with `CC=clang` and the same explicit C17 flags and isolated roots | passed with the same valid and invalid CLI controls. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_sonar_reliability_contract` | passed, 10 tests. |
| Task-owned external overlay of the exact Parent candidate plus the read-only Parent-pinned Framework archive `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`: `check-bilingual-docs.py`, `check-repository-path-references.py`, and Framework `check-doc-links.py` | passed: `bilingual docs ok`, `repository path references: PASS`, and `doc links ok`. |
| `git diff --check` | passed; no output. |

## Runtime evidence

The timeout smoke is a focused local service-control test. It is not host
connector runtime evidence, does not start Traefik or Envoy, and does not make
a claim about a full deployment.

## Checks not run and rationale

- Fresh exact-PR-head GitHub checks and SonarQube Cloud analysis are pending
  the normal task-owned Draft PR follow-up cycle.
- Full connector matrices and host-runtime suites are not applicable to this
  lexical parser-scope change and were not used as a substitute for the
  focused authorization-service control.

## Known limitations

SonarQube Cloud is the authority for removing `AZ9MwjL6-bUaKQ_zSGBL` and
`AZ-orCBNFp8FN2qblodn`; local C17 compilation cannot prove the hosted rule
disposition. The project-wide 652-issue and duplicate-line backlog remains
outside this one parser-focused remediation.

## Remaining risks

The correction deliberately leaves the public CLI design unchanged. Any future
functional CLI change must separately re-evaluate argument ordering, timeout
policy, and authorization-service wrapper behavior.

## Final diff and review status

The initial scope correction was committed as
`8fa2f2cf8e8c6130ee1530f97008284c63bf298b` and the initial bilingual Change
Record/index commits were pushed to the task branch. Its exact hosted head
reported `c:S886`, so this follow-up adds only the explicit skip and its
missing-value regression control. The reviewed candidate remains a Draft PR;
fresh exact-head hosted evidence is required after the normal follow-up push.
No Ready-for-review transition or merge is claimed.
