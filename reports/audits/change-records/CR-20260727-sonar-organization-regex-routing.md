# Change Record: Parent repository-organization regex and routing for SonarQube Cloud

**Language:** English | [Deutsch](CR-20260727-sonar-organization-regex-routing.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-organization-regex-routing |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent Sonar Code Smells AZ9cRzA4HhV2CayPTP49 (python:S6035), AZ9cRzA4HhV2CayPTP4- and AZ9cRzA4HhV2CayPTP4_ (python:S5843), and AZ9cRzA4HhV2CayPTP5C (python:S8513). |
| Boundary | Parent metadata classifier and pure unit test, this English/German pair, and indexes. Tracked-file subprocesses, temporary-output allocation, file reads/writes, Framework discovery, scanner configuration, external Sonar/GitHub state, Framework/MRTS content, and delivery are unchanged. |

## Motivation and problem statement

The temporary repository-organization inventory used avoidable regular-
expression alternation complexity and equivalent chained prefix checks. The
four Sonar findings identify those pure classifier expressions. The change
must preserve current metadata matching, including accepted legacy
incomplete-brace forms, and Framework catalog routing.

## Acceptance criteria

- Factor the common dollar prefix and the common reference boundary/suffix.
- Replace only the three equivalent one-character assignment alternatives and
  the paired check-prefix chain.
- Preserve positive, negative, and legacy regex matches plus catalog routing.
- Preserve the existing private temporary-output symlink/permission control.
- Maintain this English/German pair and indexes, then validate the pair and
  diff hygiene.

## Implementation decision and rationale

VARIABLE_RE shares its dollar prefix and uses an equivalent character class
for the three assignment operators. REFERENCE_RE shares the word boundary and
directory suffix while retaining the same five prefixes. The routing branch
uses a tuple argument to startswith. The new pure test exercises legacy brace
matches, rejected near-misses, reference boundaries, and both check-prefix
spellings. No temporary-directory, subprocess, or Framework behavior changed.

## Changed files

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- this English/German Change Record pair

## Commands executed

- A baseline in-memory import retained representative old regex matches and
  catalog destinations before the edit.
- The focused repository-organization suite passed: 3 tests in 0.001s.
- The existing RuntimePathSecurity temporary-writer symlink test passed: 1
  test in 0.418s. It used and removed a task-owned temporary directory below
  the evidence root; the exact path was verified absent.
- The AST regex/tuple-routing ownership predicate passed.
- Pair validation and diff hygiene are run after this pair is added; no
  unobserved CI, runtime, review, or delivery result is asserted.

## Security impact

Low-risk metadata-classifier maintenance, not a security-control relaxation.
The ASCII identifier and reference character classes are retained. The patch
does not change the subprocess command, private mkdtemp allocation, path
behavior, or write permissions; the existing symlink/permission control passed.

## Runtime evidence

The new suite imports the module and calls only regex/routing functions in
memory. The established security control calls main with tracked files mocked,
uses only test-owned temporary reports, performs no real Git listing, and
leaves no output. No connector, Framework, MRTS, or host runtime was run.

## Known limitations

The local interpreter is Python 3.14.4 while CI requires Python 3.14.6, so
the result is same-minor local evidence. This batch covers four current Code
Smells; the public endpoint still reports 1,125 OPEN issues and this
uncommitted candidate changes no external Sonar state.

## Remaining risks

Regex refactoring can change edge matches. The test preserves current unusual
accepted brace behavior, rejects intended near-misses, and keeps no capturing
groups, so findall continues to return full matches. Exact delivered-head
Sonar analysis remains required before these keys are externally resolved.

## Checks not run and rationale

- The real inventory main was not run against tracked files because it queries
  Git and writes a planning snapshot outside this classifier-only batch.
- Full documentation/link checks remain outside this batch; prior full runs
  are blocked by the intentionally uninitialized Framework Gitlink.
- No GitHub CI, Sonar PR analysis, review, pull request, merge, or
  default-branch update occurred.

## Final diff and review status

The B20 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
