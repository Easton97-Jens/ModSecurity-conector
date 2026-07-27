# Change Record: Parent compiler-guide metadata literals for SonarQube Cloud S1192

**Language:** English | [Deutsch](CR-20260727-sonar-compiler-guide-metadata-literals.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-compiler-guide-metadata-literals |
| Date (UTC) | 2026-07-27 |
| Base revision | 7c782b0089880c02deb2b4ee32d2f3f6d7b8f59d |
| Tracking | Parent Sonar Code Smells AZ9cRzBeHhV2CayPTP5m, AZ9cRzBeHhV2CayPTP54, AZ9cRzBeHhV2CayPTP5S, and AZ9cRzBeHhV2CayPTP5n (python:S1192). |
| Boundary | Parent compiler-guide metadata and guide tests, this English/German pair, and indexes. Commands, URLs, package names, source-map paths, German labels, source/provenance behavior, guide semantics, scanner configuration, external Sonar/GitHub state, Framework/MRTS content, and delivery are unchanged. |

## Motivation and problem statement

Four current Sonar findings identify duplicated closed-set documentation
metadata: two package statuses, the patched Lighttpd host-source value, and
the English Source mapping heading. Module-local constants give each value one
owner while preserving all generated guide text and link targets.

## Acceptance criteria

- Add constants only for the four selected metadata values.
- Replace only their exact value/key/heading uses.
- Preserve rendered English and German guides byte-for-byte.
- Preserve source-map paths, commands, URLs, package names, and host/provenance
  descriptions.
- Maintain this English/German pair and indexes, then validate the pair and
  diff hygiene.

## Implementation decision and rationale

Two package-status constants remain in the existing status set, the patched
host-source constant remains in the Lighttpd model and both translation maps,
and the English heading constant replaces six presentation labels only. The
German heading remains explicit and unchanged. A focused metadata test proves
the exact constant values and placements; existing idempotent, bilingual, and
repository-link tests prove generated output remains current.

## Changed files

- scripts/generate_compiler_guides.py
- tests/test_compiler_guides.py
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- this English/German Change Record pair

## Commands executed

- The focused metadata, idempotent generated-file, bilingual-structure, and
  repository-link controls passed: 4 tests in 0.039s.
- The AST ownership predicate passed with four exact values and respectively
  seven, five, three, and six constant loads.
- The guide test used a task-owned temporary compiler-guides directory below
  the evidence root and left no retained matching directory.
- Pair validation and diff hygiene are run after this pair is added; no
  unobserved CI, runtime, review, or delivery result is asserted.

## Security impact

Not applicable to the product security boundary: this patch centralizes static
documentation metadata only. It changes no command, URL, checksum, source-map
path, host selection, provenance validation, filesystem behavior, network
behavior, or security-control wording.

## Runtime evidence

No real host build, package operation, connector runtime, Framework, MRTS, or
host runtime was run. The tests render guides in memory and into a private
test temporary directory only.

## Known limitations

The local interpreter is Python 3.14.4 while CI requires Python 3.14.6, so
the result is same-minor local evidence. This batch covers four current Code
Smells; the public endpoint still reports 1,125 OPEN issues and this
uncommitted candidate changes no external Sonar state.

## Remaining risks

Guide labels can feed status comparisons and rendered content. The constants
retain the exact old bytes, the status set and translation maps remain covered,
and the idempotent guide test compares generated files to the committed
documents. Exact delivered-head Sonar analysis remains required before the
keys are externally resolved.

## Checks not run and rationale

- Real compiler, package, connector, and Framework operations are outside this
  metadata-only batch.
- Full documentation/link checks remain outside this batch; prior full runs
  are blocked by the intentionally uninitialized Framework Gitlink.
- No GitHub CI, Sonar PR analysis, review, pull request, merge, or
  default-branch update occurred.

## Final diff and review status

The B21 candidate is local, uncommitted, and unpushed. It has no delivery,
Framework, or MRTS action.
