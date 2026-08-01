# Finding FND-SONAR-0026: PR #198 test bootstrap uses an optimization-sensitive composite assert

**Language:** English | [Deutsch](finding.de.md)

## Classification

| Field | Value |
| --- | --- |
| Category | `maintainability` |
| Repository / ownership | `parent` / `parent` |
| Priority / severity / confidence | `P2` / `not_applicable` / `confirmed` |
| Status / feasibility | `verified` / `feasible_now` |
| Release blocker / candidate integration blocker / security relevant | no / no / no |
| Sonar inventory | `python:S9073`, `AZ-zgsKSuhGCH8wggCxz` |

## Summary, behavior, and impact

Initial SonarQube Cloud analysis for PR #198 head
`6a9f1d21a927405833aa0f07ae6e09e5aa3fd07d` reports one open MAJOR code
smell, `python:S9073`, at `tests/test_prepare_runtime_components.py:22`.
The module-level compound assert guards the dynamically created module
specification and its loader before `module_from_spec()` and `exec_module()`.

This is a task-owned non-security maintainability finding. Python removes
assertions under `-O`, so the guard is not suitable for import/bootstrap
failure handling. The exact-head Quality Gate is `OK`, but the open issue must
be remediated and reverified before this controlled integration can progress.
No user risk acceptance covers this PR-local issue.

## Scope, remediation, and controls

- Scope is limited to the Parent test bootstrap
  `tests/test_prepare_runtime_components.py` and its bilingual Change Record.
- Replace the compound assert with a single explicit guard that raises
  `ImportError` if `SPEC` or `SPEC.loader` is unavailable. Preserve the
  existing dynamic module creation and exactly-once execution sequence.
- Verify the valid bootstrap and focused runtime-component suite normally and
  under `Python -O`, plus a controlled invalid-spec import rejection.
- Do not use `NOSONAR`, an assertion split, suppression, cast/type-ignore,
  Sonar policy or Quality Gate changes, exclusions, Framework/MRTS changes, or
  Gitlink changes.

## Retained evidence

Run ID: `fnd-sonar-0026-20260730T145943Z`.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| `evidence/sonar-pr198-initial.json` | `6cd1dafc4d62b5d17a2e94196afc36007b43f2a4a4b8c776447b6282df059e3a` | Exact-head Sonar check and analysis `dfe0aaad-3fc8-428c-aa03-a1eb3cc684f1` are successful and Quality Gate is `OK`, but issue `AZ-zgsKSuhGCH8wggCxz` remains `OPEN`. |

The artifact is retained under
`/var/tmp/codex/ModSecurity-conector/pr-integration-186-199-20260730T072658Z/fnd-sonar-0026-20260730T145943Z/`.
It binds the issue to PR #198's recorded head and base; no credentials or raw
environments are retained.

## Exact-head remediation verification

The narrow test-only ImportError guard is present on exact PR head
b55eedd470df4e3395a6833f7814363c8beb1974. Its retained final evidence records
Sonar Quality Gate OK, zero open/confirmed task-owned PR issues, zero new
hotspots, and original issue AZ-zgsKSuhGCH8wggCxz / python:S9073 as
CLOSED/FIXED by analysis 5ef72438-492c-43d3-8ca5-4572826a993f. Required
GitHub checks, no-bypass Ruleset contexts, code and secret scanning,
mergeability, reviews, and threads were independently read back for that same
head. No rule, Quality Gate, exclusion, suppression, NOSONAR, Gitlink,
Framework, or MRTS change was used.

| Artifact | SHA-256 | Result |
| --- | --- | --- |
| fnd-sonar-0026-20260730T164415Z/evidence/sonar-pr198-remediated.json | 9b59e06506d7d513f9939a77bfaaa6ad316971ee9a8164a6363e82d95abc7c07 | Exact PR-head remediation verification; original issue CLOSED/FIXED and no task-owned replacement issue. |

## Resulting-master verification

Protected SHA-bound squash merge of PR #198 created Parent master
`4e5d45072bf32ff822f4b1039517026416259493` at `2026-07-30T16:58:50Z`.
The result has the reviewed head's identical tree, exactly the six approved
paths, clean whitespace, and the unchanged Parent-Framework Gitlink
`6400ee882afa0527e5c0763fa6efb850ffa403f2`. Required protected contexts,
CodeQL, and the available Secret Scanning service/alert evidence passed.

Sonar analysis `32425f2d-a1e8-47bb-b22a-276b1f93cd6b` is bound to that master
SHA. It reports zero open `python:S9073` issues at the affected test path;
the original key is absent from the accessible current index and its detail
endpoint is no longer retrievable. The sole failed Sonar master check is
precisely the separately documented FND-SONAR-0001 signature: its three known
`python:S5332` hotspots and two known failed conditions only. This is not a
green Sonar claim and does not waive any other PR, scanner, review, or master
control. The queued zero-run Cloudflare suite is not applicable: it is not a
Ruleset requirement, no deployment path/configuration changed or exists, and
the exact-SHA deployment inventory is empty.

## Acceptance and disposition

Acceptance requires an explicit invalid-spec `ImportError` in normal and
optimized Python; preservation of valid module loading and all focused
runtime-component controls; a final exact-head security-diff review; terminal
required hosted checks with no unresolved review thread; and Sonar readback
showing the original key and any task-owned replacement issue absent. The
finding is `verified` on resulting master; it is deliberately not closed from
an index absence alone.

`FND-SONAR-0016` is related aggregate new-code follow-up and
`FND-SONAR-0024` is a different C complexity issue; neither is a duplicate.
`FND-SONAR-0001` is separate master-level risk context. The current user's
risk acceptance is deliberately restricted to that unchanged master signature,
not this PR-local issue.

## History

- `2026-07-30T14:59:43Z`: exact PR #198 evidence confirmed open
  `AZ-zgsKSuhGCH8wggCxz` / `python:S9073`; the distinct Parent P2 finding was
  triaged as `in_progress` and narrow remediation was planned. No merge,
  suppression, or Sonar configuration change occurred.
- `2026-07-30T16:41:38Z`: the exact remediation PR head
  `b55eedd470df4e3395a6833f7814363c8beb1974` passed local controls, sealed
  security-diff review, terminal hosted/governance checks, and PR-bound Sonar
  analysis `5ef72438-492c-43d3-8ca5-4572826a993f`. Original issue
  `AZ-zgsKSuhGCH8wggCxz` is `CLOSED/FIXED`; status moved to `fixed`,
  pending resulting-master verification.
- `2026-07-30T17:06:29Z`: protected squash of #198 created master
  `4e5d45072bf32ff822f4b1039517026416259493` with the reviewed head's tree.
  SHA-bound analysis `32425f2d-a1e8-47bb-b22a-276b1f93cd6b` has zero open
  `python:S9073` issues at the affected path; the original key is absent from
  the accessible master index. Status moved to `verified`, not `closed`.
