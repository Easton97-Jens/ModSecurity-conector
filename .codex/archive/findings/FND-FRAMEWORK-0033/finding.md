# FND-FRAMEWORK-0033 — Framework Python-maintenance contract permits future token and secret exposure outside its reviewed publisher input

## Identity

| Field | Value |
| --- | --- |
| ID | FND-FRAMEWORK-0033 |
| Category | security_hardening |
| Repository / ownership | framework / framework |
| Priority / severity | P2 / low |
| Confidence / status | validated / fixed |
| Feasibility | feasible_now |
| Release blocker | no |
| Security relevant | yes |

## Summary, affected path, and impact

Before remediation, the uncommitted CPython 3.13 maintenance workflow was
exempt as a whole from the generic GitHub-token reference rule. Its
maintenance-specific check looked only for the literal `github.token` in
`resolve` and `candidate-validate`, and did not inspect `publish`. A future
workflow edit could therefore use `${{ github['token'] }}`,
`${{ secrets.GITHUB_TOKEN }}`, another `${{ secrets.* }}` expression, or a
publisher shell/action token reference without the local CI-security contract
rejecting it.

The source is a proposed edit to `.github/workflows/check-python-version.yml`;
the potential sinks are an action or Bash context in a reader job or the
write-capable publisher. Current source has none of these unsafe references:
the sole explicit token is the reviewed
`create-pull-request.with.token: ${{ github.token }}` input. Publication is
schedule/manual-only and default-branch/repository gated. This is a P2/low
future-regression hardening finding, not a current disclosure, untrusted-PR
execution, or broader repository-write finding.

`actions/checkout` may use GitHub's automatic read-scoped job token internally.
That hosted default is distinct from an explicit YAML secret declaration; the
workflow retains `contents: read` for readers and `persist-credentials: false`
to avoid credential persistence for subsequent Git commands.

## Evidence and reproduction

Retained evidence is:

- Run ID: `20260720T180337Z-framework-python-313-updater-f3349a7e`
- Artifact: `/var/tmp/codex/ModSecurity-conector/runs/20260720T180337Z-framework-python-313-updater-f3349a7e/analysis/codex-security-scans/ModSecurity-test-Framework/9dab40c2_20260720T185431Z/05_findings/FND-FRAMEWORK-0033-pre-fix-validation.md`
- SHA-256: `8a0a0cb5ac7fa15a76de01c5210d596bc2ceac1933e40380eb6d49869bb71495`
- Command: RTK-wrapped focused Python-version and CI-security contract test modules
- Working directory: `/var/tmp/codex/ModSecurity-test-Framework/worktrees/framework-python-updater`
- Exit code: `1` (intentional pre-fix regression)
- Observed at: `2026-07-20T19:12:21Z`
- Retention: `retained_task_evidence`

The test copied the parsed workflow, put the literal non-secret test expression
`${{ secrets.GITHUB_TOKEN }}` in `resolve.env`, and expected
`python_version_maintenance_errors` to reject it. Before remediation the
checker returned no error. The retained run also proved the independent
basename-only candidate-workflow exception; that nested configuration is not
executable by GitHub Actions, but is repaired in the same narrow change.

No real secret was created, exposed, or retained. A malicious change would
still need to be accepted onto the trusted branch; the evidence does not claim
a current exploit.

## Root cause, remediation, and acceptance criteria

A file-wide allow-list was used where a parsed, location-specific exception
was required. The special matcher omitted indexed `github['token']`,
`secrets.*`, and shell `${GITHUB_TOKEN}` forms, and did not inspect publisher
fields outside the create-pull-request token option.

The repair recursively detects `github.token`, `github['token']`,
`secrets.<name>`, bracketed `secrets[...]`, and shell `${GITHUB_TOKEN}` forms.
It rejects every explicit reference in `resolve` and `candidate-validate`. In
`publish`, it permits only the unique reviewed
`peter-evans/create-pull-request` action's `with.token` scalar
`${{ github.token }}`. Focused mutations reject reader env/with/uses/run
references, publisher shell/env/non-approved-action references, and a second
PR-creation action while preserving the current legitimate workflow.

## Validation evidence, dependencies, blockers, and residual risk

The focused mutation suite, Python-version and CI-security contract suites,
full Framework lint, documentation/Change-Record checks, `git diff --check`,
and a sealed complete security-diff review all passed. The scan report is
retained at the evidence path in the JSON record with SHA-256
`f4c1ec2c78aeb33745fada8f1a9795cc5eba576e11be1f1cc24130ee9e4de56a` and
zero reportable findings. The bypass review covers dotted and indexed GitHub
token syntax, generic and bracketed secrets, shell `${GITHUB_TOKEN}`, publisher
locations, and duplicate PR actions. No external dependency, blocker, or
duplicate is known.

The local repair is fixed, but exact-head GitHub Actions, reviewer, and
SonarQube evidence remains pending on the authorized Draft PR. Current source
remains limited by reader `contents: read`, nonpersistent checkout credentials,
publisher-only write permissions, exact candidate gates, and Draft-only
publication. No Parent gitlink or MRTS change is authorized or performed.

## History

- 2026-07-20T19:12:21Z — a task-owned pre-fix mutation test validated that
  the resolver accepted an explicit `${{ secrets.GITHUB_TOKEN }}` expression;
  this P2/low Framework hardening finding was allocated before delivery.
- 2026-07-20T19:55:25Z — the location-specific recursive parser repair,
  including `${{ github['token'] }}`, passed focused mutation regressions,
  native full lint, and the sealed security-diff scan. The finding is `fixed`;
  exact-head Draft-PR validation remains pending.

## Serialized-context follow-up

The earlier direct-reference repair did not classify bare context objects
inside GitHub expression functions. A safe literal mutation with
`${{ toJSON(secrets) }}` in a reader shell step failed the focused test because
the maintenance contract returned no error; a publisher
`${{ toJSON(github) }}` mutation was likewise accepted. No secret was
resolved, printed, transmitted, or retained, and a malicious source edit would
still need acceptance on the trusted branch.

The active narrow repair parses `${{ ... }}` expression bodies. It rejects
`secrets` anywhere in an expression, `github.token`, every `github[...]` form,
bare GitHub-context serialization, and shell `${GITHUB_TOKEN}` outside the one
reviewed `create-pull-request.with.token: ${{ github.token }}` input. It keeps
the legitimate `github.sha` and `github.repository` controls valid. The
retained safe evidence is
`evidence/fnd-framework-0033-serialized-context.md` in task run
`20260720T180337Z-framework-python-313-updater-f3349a7e`; the post-fix focused
suite passed 12 tests. The renewed 36-test focused suite, 85 CI-security tests,
native workflow/documentation/full-lint gates, and the sealed 11-file follow-up
security-diff scan all passed with zero reportable findings. Its report SHA-256
is `be92a7e65c3c81e72140b5441494eb4461df4417ee361c344bd3d0cf56775a5c`.

- 2026-07-20T20:54:02Z — reopened as `in_progress` after the serialized-context
  bypass was reproduced with literal test expressions.
- 2026-07-20T21:12:33Z — returned to `fixed` after expression-aware regression
  coverage, the complete local validation set, and the sealed follow-up scan
  passed. The remediated Framework commit and exact-current-head Actions,
  review, and SonarQube evidence remain pending; no merge, Parent gitlink
  update, or MRTS action is authorized.
