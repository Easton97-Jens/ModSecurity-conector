# Change Record: validated Framework maintainability gitlink

**Language:** English | [Deutsch](CR-20261003-framework-sonar-gitlink.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20261003-framework-sonar-gitlink` |
| Date (UTC) | `2026-10-03` |
| Base revision | `209e6f003282695e62876332a4b916eb3e170969` |

Delivery: Draft PR #396.
Framework: `b9b9534b7e0b15edad31393699ebd0617748148d` →
`dd4af7d24b0ae90f8fa81513e5c9c290d40847f3`, separately delivered in Framework PR #135.
MRTS remains `615b13bacbd008562c17408246c41ab27dca3104`.

## Motivation and problem statement

The user additionally selected the 28 actual Framework Sonar findings and a
separate Parent pointer update. This is not a repair of historical Parent
PR #135: its current report-helper lineage has no observed Sonar defect.

## Acceptance criteria

Use the published, clean, exact Framework commit after all six SHA-bound
workflows succeeded. Its new Sonar analysis must pass without suppression;
all 28 original issue IDs must be CLOSED/FIXED. Preserve Parent source,
required selection/evidence contracts, protocol separation and MRTS.

## Implementation decision and rationale

Change only the gitlink and paired integration traceability/index. No Parent
dispatch/API change is required by the helper-only Framework contract.
Frame source and tests belong to separate commits; see its
`20261003-02-no-crs-sonar-maintainability` record. Keep the existing unrelated
With-CRS static profile pins unchanged; their pre-existing mismatch is not
a new maintenance-induced wiring defect. Do not relabel retained runtime data.

## Security impact

No validator, containment, receipt identity, descriptor authority, event
requirement or status precedence is weakened. No new runtime claim is made.
Protected dispatcher/builder/launcher/collector source remains unchanged.

## Changed files

`modules/ModSecurity-test-Framework`, this EN/DE record pair and its EN/DE index.
No connector/Common C, Parent runtime script, protocol test or MRTS change.

## Commands executed

Artifact references prefixed `analysis/` below resolve under the approved
external run root `/var/tmp/codex/ModSecurity-conector`, never under the checkout.

Parent baseline focus: 31 tests PASS, no skips, exit 0, including two trusted
Framework API calls. Exact command and log are retained in external
`analysis/framework-pr135-sonar-plan.md` and
`analysis/framework-pr135-parent-pointer-baseline-focus.log` / `.exit`.
The same focus must run against the new committed Parent gitlink before push.
Native `rtk proxy make check-bilingual-docs check-doc-links` and
`rtk proxy git diff --check` are precommit documentation/diff gates.

Separately, Framework native lint passed; postcommit No-CRS/API passed 166 + 23
tests; finite baseline parity passed 2,081 comparisons. Remote Framework
workflows passed 6/6. Sonar analysis `2026-10-03T14:09:15+0000` at exact dd4
reports Quality Gate OK, 0 open issues, 0 hotspots, duplication 0.0%, and
28/28 original issue IDs CLOSED/FIXED. These are not Parent runtime proofs.

## Runtime evidence

No manual lifecycle, requests, new canonical runtime evidence or Full E2E.
Collector source commit remains `209e6f003282695e62876332a4b916eb3e170969`.

## Checks not run and rationale

New Parent-head CI/Sonar and coverage remeasurement remain pending until
publication. No full connector build or E2E is authorized in this step.

## Known limitations

Maintained source parity does not fulfill missing required runtime cases.
Old counts are not fresh coverage.

## Remaining risks

Current Parent CI/Sonar must pass before
remeasurement and MIME work. Both PRs remain Draft; no merge is authorized.

## Final diff and review status

Review the scoped five-path diff, exact gitlink, unchanged producer/dispatch
bytes and separate protocol worktree. Postcommit Parent compatibility and
new-head remote verification are still required. No secrets or raw logs here.
