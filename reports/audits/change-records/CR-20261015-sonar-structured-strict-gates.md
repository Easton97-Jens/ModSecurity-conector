# Change Record: CR-20261015-sonar-structured-strict-gates

**Language:** English | [Deutsch](CR-20261015-sonar-structured-strict-gates.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261015-sonar-structured-strict-gates |
| Date (UTC) | 2026-10-15 |
| Base revision | `a311c725c44a7a4da95acb1a4818f66bd56c462a` |

## Motivation and problem statement

The provider summary can omit explicit finding counts even for a successful analysis. Presentation text cannot establish strict zero. The previous summary parser rejected this shape without consulting the official PR-scoped structured evidence.

## Acceptance criteria

Require the current GitHub PR head, a terminal successful Sonar provider check, and the Sonar PR analysis commit to agree before and after readback. Require Quality Gate OK with no ignored or failing conditions, overall and new-code Security Rating A, zero new active/accepted issues, an explicit zero PR hotspot measure, and all three exact new-duplication metrics zero. Missing, stale, partial, ambiguous or inconsistent evidence must fail.

## Implementation decision and rationale

Both gates use one strict structured verifier. Official project PR inventory supplies commit SHA and analysis date; PR-scoped Quality Gate, measures and complete paginated issue inventories supply independent counts. The supported issue filter is `sinceLeakPeriod=true`. The published hotspot-search contract lacks PR scope, so it is never used as a substitute: the explicit PR-component `new_security_hotspots` measure is mandatory and any positive value fails. Missing measures never become zero.

JSON fields, numeric values, pagination totals and record identities are validated. HTTP redirects are rejected; responses, timeouts, page counts and diagnostic output are bounded. Duplication diagnostics retain file/block evidence through the same client. A second provider readback also rejects a changed conclusion, even when check ID and output remain unchanged. Workflow invocation now passes PR number to both gates.

## Changed files

- `ci/checks/common/check-sonar-zero.py` and `check-sonar-duplication.py`.
- `tests/test_sonar_zero_gate.py` and `test_sonar_duplication_gate.py`.
- `.github/workflows/lint.yml`: explicit PR-number binding for the zero gate.
- This EN/DE Change Record pair.

## Commands executed

From the isolated shared-gates worktree, all shell commands used RTK. With the Parent virtual environment and `PYTHONNOUSERSITE=1`, `PIP_REQUIRE_VIRTUALENV=true`, `PIP_DISABLE_PIP_VERSION_CHECK=1`:

- `rtk proxy .../.venv/bin/python -m unittest tests.test_sonar_zero_gate tests.test_sonar_duplication_gate`: 38 tests PASS on 2026-10-18.
- The new provider-conclusion race regression failed before the final comparison was added, then passed in the complete focused suite.
- `tests.test_bilingual_docs tests.test_change_record`: 42 tests PASS. Change Record structure, AST syntax for four Python files and `git diff --check`: PASS. The combined Sonar/lint/workflow/CI-security suite passed 67 tests in 296.897 seconds, including the internally invoked repository target `make check-ci-security-contract`. The standalone lint/workflow-security control passed 16 tests.
- `rtk --version`, `rtk gain`, `rtk proxy which rtk`: PASS; RTK 1.0.1.

## Security impact

No Quality Gate, rule, exclusion, finding state or credential setting is relaxed. Only official fixed-origin read endpoints are admitted. Credential values, headers and response bodies are not emitted on client failure. Local credential-dependent Sonar access remains subject to the canonical `sonar-with-env` wrapper. This patch does not perform Sonar state mutations.

## Runtime evidence

Offline tests use explicit structured API shapes and independently controlled failures. They cover stale heads, changed analyses/checks/conclusions, absent and nonzero metrics, ambiguous periods, foreign identities, incomplete and duplicate pages, annotations, unsupported filters, redirects and response bounds. Retained official API contract receipts are under the task's external `shared-gates` evidence directory. These checks validate gate behavior; they do not establish a passing hosted product analysis.

## Known limitations

The public readback assumes the configured public SonarCloud project. Unsupported or missing evidence fails closed. Inventories above 2,000 records or responses above 1 MiB require deliberate review rather than partial acceptance. Hotspot proof is the explicit PR-scoped aggregate zero, because the published hotspot-search endpoint cannot independently list PR hotspots.

## Remaining risks

The exact final published PR head still requires fresh successful GitHub and Sonar readback. A historical successful summary or a local test result cannot satisfy that acceptance requirement.

## Checks not run and rationale

No scanner upload or live final-head acceptance is claimed by this source patch. Product host tests belong to the integrated Traefik evidence run and are outside these shared gate changes.

## Final diff and review status

The two gate implementations, workflow binding and focused tests were reviewed against the strict final-head contract. The same-ID provider-conclusion race was reproduced and fixed during final review. Publication and final hosted verification remain the parent task's responsibility.
