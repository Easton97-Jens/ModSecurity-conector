# Change Record: Remove redundant native-oracle JSON fallback

**Language:** English | [Deutsch](CR-20260720-sonar-native-oracle-null-fallback.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260720-sonar-native-oracle-null-fallback |
| Date (UTC) | 2026-07-20 |
| Base revision | cbd8385ce1b34318c84cf8f4a5a92ef98c83f82a |
| Tracking | SonarQube Cloud issue AZ7b3dgOcO69wzd-_jHv, c:S3519, native JSON result serialization |
| Boundary | Parent ci/tools native oracle and its focused Parent source contract only; no Framework, MRTS, gitlink, scanner, or Quality-Gate change. |

## Motivation and problem statement

Fresh Parent-master analysis 6cc3a8ba-3926-4240-b6ec-f2c1f99509ff reports
AZ7b3dgOcO69wzd-_jHv as an open Blocker c:S3519 in
ci/tools/native_modsecurity_oracle.c. Its recorded interprocedural flow enters
json_string from the redundant caller expression whoami ? whoami : "".

The existing callee already has an explicit NULL branch that serializes an
empty JSON string and returns before a byte cursor is initialized. Passing a
manufactured empty literal from the caller therefore duplicates that behavior
and permits the analyzer to model an impossible one-byte-literal loop path.

## Acceptance criteria

- A NULL whoami value serializes as the same empty JSON string as before.
- A non-NULL whoami value continues through the existing JSON escaping path.
- The caller contains no redundant whoami ? whoami : "" fallback.
- The focused source contract covers the direct nullable call and the callee
  NULL guard.
- No Sonar suppression, issue dismissal, scanner exclusion, Quality-Gate
  change, Framework/MRTS change, or gitlink update is used.

## Implementation decision and rationale

write_result now passes whoami directly to json_string. json_string remains the
single owner of the nullable-string contract: it writes "" and returns when
value is NULL, otherwise it initializes the unsigned-byte cursor and preserves
the existing escape switch.

This is the smallest behavior-preserving correction for the exact recorded
Sonar flow. It removes the only remaining caller-level empty-string literal
source for json_string rather than classifying a real source change as a false
positive.

## Changed files

- ci/tools/native_modsecurity_oracle.c
- tests/test_sonar_reliability_contract.py
- this English/German Change Record pair

## Commands executed

| Command | Result |
| --- | --- |
| Focused unittest for tests.test_sonar_reliability_contract | passed: 6 tests |
| git diff --check before staging | passed |
| Git staged-diff check for the two source/test files | passed |
| Direct Sonar issue-flow readback for AZ7b3dgOcO69wzd-_jHv | confirmed the caller-level empty-literal data flow |

## Security impact

The affected program is a short-lived connector-free CI/native oracle, not a
connector request sink. The issue is a reliability/static-analysis result, not
a proven remote memory-safety exploit. The correction preserves safe NULL
serialization and removes a misleading interprocedural literal path without
weakening any control.

## Runtime evidence

The focused source contract proves the intended NULL/non-NULL boundary at
source level. A complete native-oracle runtime was not executed in this
worktree. The parent-source change is intentionally limited to the existing
JSON-result serialization boundary.

## Known limitations

A fresh exact PR-head SonarQube Cloud analysis is required before claiming
that the issue is fixed or resolved. The parent master Quality Gate also has
independent vulnerabilities and three unreviewed security hotspots; this small
record does not claim to resolve them.

## Remaining risks

Until exact-head and resulting-master Sonar evidence is observed, the
c:S3519 alert remains open. The independent current-master backlog consists of
220 open vulnerabilities and three TO_REVIEW python:S5332 hotspots. No risk is
accepted and no external issue is closed by this local commit.

## Checks not run and rationale

- Native C17 compilation and an actual native-oracle run are blocked because
  gcc and clang are present but libmodsecurity headers, pkg-config metadata,
  and a linkable runtime are absent.
- Full connector/runtime matrices are outside this two-file Parent scope and
  require the unavailable native prerequisites.
- PR, CodeQL, OSV, secret-scanning, Scorecard, and SonarQube Cloud checks have
  not yet run for this exact source commit.

## Final diff and review status

The source/test correction is commit
941551080c9c9bc764b2db140288570f7c147499 on the isolated Parent branch
codex/sonar-json-string-null-guard-20260720. This record preserves only
source-level pre-delivery evidence; it neither claims nor substitutes for a
normal push, pull request, merge, or external-alert resolution. The delivery
gate is normal push, Draft PR creation, exact-head checks, review/thread
readback, and protected merge only if those gates pass.
