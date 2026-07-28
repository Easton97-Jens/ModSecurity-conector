# Change Record: Parent repository inventory complexity remediation for SonarQube Cloud S3776

**Language:** English | [Deutsch](CR-20260727-sonar-s3776-repository-inventory.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260727-sonar-s3776-repository-inventory |
| Date (UTC) | 2026-07-27 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent SonarQube Cloud `python:S3776` receipt keys `AZ9cRzA4HhV2CayPTP5A` (`category`) and `AZ9cRzA4HhV2CayPTP5B` (`proposed_destination`). |
| Boundary | Parent inventory generator, its direct Parent test, and this English/German Change Record pair. Product connectors, workflows, generated inventory output, Framework source, MRTS source, Gitlinks, SonarQube Cloud configuration, suppressions, external issue state, and master integration remain unchanged. |

## Motivation and problem statement

The current SonarQube Cloud inventory reports two cognitive-complexity findings
in `scripts/generate_repository_organization_inventory.py`. The previous
helpers encoded category and destination precedence as long conditional chains,
which made exact routing and fallback behavior hard to review.

## Acceptance criteria

- Both receipt-linked public helpers remain available and are structurally
  simpler.
- Category precedence, destination strings, inventory row schema, sorting,
  fallback behavior, CLI behavior, and file-write behavior remain unchanged.
- Table-driven tests cover Parent and Framework destination routes plus
  fallbacks without modifying the Framework.
- The generator's current-corpus JSON output matches after normalizing only
  `generated_at_utc`; both generated Markdown plans remain byte-identical.
- No source outside the scoped Parent generator/test or this traceability pair
  changes, and no Sonar issue is claimed closed before an exact-head analysis.

## Implementation decision and rationale

The refactor replaces the two high-complexity chains with ordered immutable
category/routing tables and small private resolver helpers. The public
`category` and `proposed_destination` signatures and output values remain
unchanged. Ordering is explicit in the tables so generated, historical,
security, evidence, testing, build-guide, architecture, roadmap, connector,
entry-point, and fallback precedence remain reviewable.

## Changed files

- scripts/generate_repository_organization_inventory.py
- tests/test_repository_organization_inventory.py
- reports/audits/change-records/CR-20260727-sonar-s3776-repository-inventory.md
- reports/audits/change-records/CR-20260727-sonar-s3776-repository-inventory.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Commands executed

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest discover -v -s tests -p test_repository_organization_inventory.py
rtk proxy git diff --check
```

The isolated implementation comparison also executed the base and refactored
generator against the same current corpus, comparing all three temporary
outputs after normalizing only `generated_at_utc` in JSON.

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused repository-inventory test module | passed: 5 tests. |
| Category/destination regression coverage | passed: precedence, Parent routes, Framework routes, and fallbacks are table-driven. |
| Same-corpus generator output comparison | passed: JSON differs only by normalized `generated_at_utc`; English and German Markdown plans are byte-identical. |
| Receipt/symbol structural review | passed locally: `category` and `proposed_destination` remain present with small branch-like AST counts. This is not an external SonarQube Cloud result. |
| `git diff --check` | passed: no whitespace errors. |

## Security impact

The focused assessment is `not_applicable` to a new security boundary. The
generator's tracked-file reads, private temporary-root allocation, subprocess
use, error fallback, and output writes are unchanged. The same-corpus output
comparison and route/fallback controls provide the relevant regression
evidence; no new security finding was identified.

## Documentation status

This complete English/German Change Record pair records the exact scope,
validation, limits, and delivery state. The record indexes are updated in both
languages. No generated inventory output was edited.

## Runtime evidence

No connector, host, protocol, report-runtime, or production behavior changed
or is claimed. Generator/output-equivalence and focused unit tests are not
connector runtime evidence.

## Known limitations

SonarQube Cloud has not yet analyzed the uncommitted candidate. The two
receipt-backed findings can only be considered remediated after an exact-head
analysis; the broader 1,022-item remediation remains in progress.

## Remaining risks

Table ordering is the behavior contract for the refactor. A future table edit
could change a routing precedence; the table-driven route/precedence tests and
same-corpus comparison reduce that risk. No conclusion follows for unrelated
complexity, security, or duplication findings.

## Checks not run and rationale

- Connector builds, runtime smokes, protocol matrices, Framework tests, and
  MRTS tests are not applicable because no connector/runtime or
  cross-repository source changed.
- GitHub Actions, hosted SonarQube Cloud analysis, commit, push, pull request,
  and merge have not yet occurred. This record does not provide master-merge
  authority.

## Final diff and review status

The isolated task-worktree candidate contains only the scoped generator,
direct test, and required bilingual traceability material. A root-agent source
and diff review confirmed the ordered tables preserve the prior route families
and fallback paths. Framework and MRTS source, both Gitlinks, scanner controls,
external issue disposition, and `master` remain unchanged. Delivery facts will
be added only after they are observed.
