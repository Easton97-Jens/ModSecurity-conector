# Change Record CR-20260903-no-crs-doc-consistency-repair

**Language:** English | [Deutsch](CR-20260903-no-crs-doc-consistency-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260903-no-crs-doc-consistency-repair |
| Date (UTC) | 2026-09-03 |
| Base revision | d50fad793a8af1fa4cf0dc83a951c041dcd940e9 |
| Delivery status | In progress on a dedicated Parent worktree. The original user request authorizes a normal PR, but no commit, push, PR, hosted result, SonarCloud result, or merge is asserted. |

## Motivation and problem statement

Five `master` workflows at base revision
`d50fad793a8af1fa4cf0dc83a951c041dcd940e9` stopped in
`ci/checks/documentation/check-no-crs-doc-consistency.py`. The canonical
Traefik manifest already described the bounded `forwardAuth` Phase-2 path as
`configured_not_exercised`, but the checked-in generated catalog was stale and
the paired TODOs lacked the legacy `request_body_mode=none` boundary required
by that consistency control.

## Acceptance criteria

- Both Traefik TODO files retain the exact `request_body_mode=none` legacy
  compatibility boundary and state that the selected path is buffered.
- The supported generator refreshes all three versioned capability-catalog
  outputs and reports Traefik `request_body_buffered` and `phase2` as
  `configured_not_exercised`.
- `make check-no-crs-doc-consistency` and focused Traefik/bilingual controls
  pass without runtime promotion or request-body streaming enablement.
- A sealed Codex Security review is completed before delivery.

## Implementation decision and rationale

This Parent-only repair changes the English/German TODO pair and reruns the
supported `make capabilities-all-connectors` generator. It does not hand-edit
generated output, change runtime source, alter CI permissions, weaken the
consistency control, modify `modules/ModSecurity-test-Framework`, or update a
Gitlink. The complete catalog refresh is intentional: its prior version was
generated from older capability-manifest inputs, so the generator updates all
current connector entries as one source-of-truth artifact.

Independent source review found that the former capability text was too broad
about an operator omitting the response observer. The checked-in dynamic
profile and its source-contract test require the `forwardAuth` to
response-observer order. The canonical manifest is therefore narrowed to that
checked-in profile and truthfully marks an omitted or reordered observer as an
out-of-profile deployment change that needs separate P3/P4 validation. This
changes metadata wording only; it does not change the runtime chain.

## Security impact

The affected boundary is repository and CI metadata integrity. The repair
keeps `request_body_mode=buffered`, retains `request_body_mode=none` only for
the legacy request-body-disabled compatibility path, leaves request-body
streaming `unsupported_by_host_model`, and does not claim real-host Phase-2
evidence. It changes no request parser, listener, authorization rule, secret,
dependency, or workflow permission.

## Changed files

- `connectors/traefik/TODO.md`
- `connectors/traefik/TODO.de.md`
- `connectors/traefik/capabilities.json`
- `reports/testing/generated/canonical/connector-capabilities.generated.json`
- `reports/testing/generated/canonical/connector-capabilities.generated.md`
- `reports/testing/generated/canonical/connector-capabilities.generated.de.md`
- `reports/audits/change-records/CR-20260903-no-crs-doc-consistency-repair.md`
- `reports/audits/change-records/CR-20260903-no-crs-doc-consistency-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

- `rtk proxy make capabilities-all-connectors` — passed;
  `connector_capabilities: ok connectors=6 capabilities=60`.
- `rtk proxy make check-no-crs-doc-consistency` — passed.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_connector_capabilities tests.test_traefik_forwardauth_p2_contract tests.test_traefik_runtime_smoke_security tests.test_bilingual_docs` — passed, 62 tests.
- After the response-observer wording clarification,
  `rtk proxy make capabilities-all-connectors` and
  `rtk proxy make check-no-crs-doc-consistency` — passed.
- The same focused 62-test command — passed after the clarification, including
  `test_forwardauth_runtime_chain_requires_the_private_response_observer`.
- `rtk proxy make check-bilingual-docs` — blocked only by 20 pre-existing
  missing Framework Gitlink targets; it reports no task-owned Change Record
  error.
- `rtk proxy make check-doc-links` — blocked only by the same absent Framework
  targets.
- `rtk proxy git diff --check` — passed.

## Runtime evidence

No connector runtime was started. This repair restores static documentation and
generator consistency only; it is not real-host Phase-2, over-limit, response,
or CRS evidence and does not promote any capability.

## Checks not run and rationale

The full bilingual and link checks cannot complete because the selected
worktree does not contain the Framework Gitlink targets named by their output.
No Framework initialization or modification is authorized. A sealed Codex
Security diff scan covers this product snapshot. Commit, pull-request, hosted
workflow, and PR-scoped SonarCloud evidence are distinct delivery evidence and
are not asserted by the local controls above.

## Known limitations

The catalog refresh correctly includes current manifest changes outside
Traefik because it is one generated repository-wide artifact. The task does
not repair the five historical open SonarCloud issues on `master`, including a
Framework-owned path outside this Parent-only authority.

## Remaining risks

The buffered Phase-2 route remains `configured_not_exercised` until fresh
real-host allow, deny, and over-limit evidence exists. Request-body streaming
remains `unsupported_by_host_model`. The repair still requires exact-head CI
and SonarCloud evidence before any integration decision. An operator who
omits or reorders the response observer changes the selected profile and must
separately validate P3/P4; this record does not claim that out-of-profile
deployment is fail-closed.

## Final diff and review status

In progress. The current user authorized a Parent-only repair in a dedicated
worktree and a normal PR under the original failed-workflow request. This
record documents local remediation decisions; it does not itself establish a
commit, push, pull request, hosted result, SonarCloud result, or merge.
