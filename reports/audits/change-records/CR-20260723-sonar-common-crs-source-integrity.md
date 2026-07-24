# Change Record: Common CRS source and generated-config integrity

**Language:** English | [Deutsch](CR-20260723-sonar-common-crs-source-integrity.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260723-sonar-common-crs-source-integrity |
| Date (UTC) | 2026-07-23 |
| Base revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Parent-only `python:S5443` keys `AZ70UrU3IhrooTjfZnAX`, `AZ70UrU3IhrooTjfZnAY`, and `AZ70UrU3IhrooTjfZnAZ`; Draft-PR #97 follow-up for `pythonsecurity:S8707` key `AZ-PstOVmYfklgBeDadY`, two `python:S1192` keys, and four `python:S3415` keys; pending canonical findings `FND-SONAR-0013` and `FND-SONAR-0014`. |
| Boundary | Parent Common Python runner, Parent test, paired Parent documentation, and this Change Record pair only. Framework, MRTS, gitlinks, dependencies, SonarCloud controls, suppressions, exclusions, Quality Gates, and host protocol behavior are unchanged. |

## Motivation and problem statement

When the CRS smoke uses libmodsecurity and no explicit CRS source is selected,
the runner previously searched beneath `RUNNER_TEMP`, `TMPDIR`, and shared
temporary locations. A different local user could prepare a directory that
looked like a CRS tree. The runner accepted only the superficial setup/rules
shape, emitted `Include` entries for it, and handed the generated rule file to
the local libmodsecurity evaluator. The generated setup/rule file and audit-log
location are also derived from caller-selected output paths, so their directory
and stale-file provenance must be protected before the generated rule file
reaches the evaluator.

This is a local cross-user configuration-integrity boundary. It does not claim
a remote request-to-parser path or that arbitrary CRS directives achieve code
execution; it prevents a smoke run from silently accepting a different user's
rule tree as its selected source.

The first exact Draft-PR #97 SonarCloud analysis also reported an agentic
filesystem-boundary candidate on the direct runner's `--log-dir` route. Before
the follow-up, a direct invocation could select an output root outside the
verified invocation tree and reach configuration/log directory creation and,
for libmodsecurity, stale decision-log removal. A focused red regression
proved that an outside `--config-root` was created before the runner returned.

## Acceptance criteria

- CRS discovery uses only an explicit `CRS_SOURCE_DIR` or paths derived from
  an explicit `--runtime-lookup-root`; no shared-temporary fallback remains.
- Every selected source, setup file, rules directory, included rule file,
  optional included plugin file, generated runtime directory, generated setup
  and rule file, and audit-log directory is absolute, regular/directory as
  appropriate, non-symlinked, owned by the runner or root,
  non-group/world-writable, and protected from cross-user ancestor replacement.
- A path interpolated into a quoted ModSecurity directive rejects quotes,
  backslashes, line breaks, and glob metacharacters; stale generated output is opened without
  following a symlink and revalidated before evaluator use.
- A valid explicit source and valid runtime-lookup-root source remain
  accepted; missing or unsafe source returns `SmokeBlocked` / Exit 77 before a
  generated rule file reaches the evaluator.
- Every direct output argument (`--evidence-root`, `--results-dir`,
  `--tmp-root`, `--log-root`, `--log-dir`, and `--config-root`) is absolute,
  canonicalized, and contained below `VERIFIED_RUN_ROOT` before the runner can
  create, unlink, pass to the evaluator, or invoke the result writer. Outside
  roots and symlink-resolved escapes return Exit 77 without a runner write.
- The selected Sonar keys are checked on a fresh exact Draft-PR head without a
  suppression, false-positive state, exclusion, rule/profile change, or
  Quality-Gate change.

## Implementation decision and rationale

Validation starts in `resolve_crs_source_dir()` because that is the narrow
point at which every selectable source becomes the source of `Include` paths
for `prepare_crs_smoke_config()`. The runner no longer derives candidates from
ambient temporary-directory variables. Its retained explicit candidate forms
are checked by `lstat`, component-by-component symlink rejection, trusted
owner/mode checks, and ancestor replacement checks before configuration is
generated. `prepare_crs_smoke_config()` applies the same boundary to generated
runtime and audit directories, creates each generated artifact with
`O_NOFOLLOW` plus exclusive creation, rejects directive-changing path
characters, and revalidates the parser input immediately before evaluator use.
An ancestor is sticky-safe only when that ancestor and its protected child are
runner/root-owned; an attacker-owned sticky directory is rejected. The check
permits root-owned read-only component trees as well as current-user-owned
trees, preserving the prepared-component lifecycle.

The control intentionally addresses cross-user replacement. Same-UID races
remain outside that claim, as they are for the existing runtime-path controls.

For the exact-head follow-up, `validate_runtime_output_paths()` reuses the
Parent `ci/lib/runtime_path_utils.py` verified-runtime-root policy. It resolves
and contains all six CLI-derived output destinations before normalization or
any runner filesystem operation. The runner retains the validated `Path`
objects for its first configuration and log sinks, while normalized values are
written back only for downstream helpers. The fixed CRS suffix is revalidated
before the configuration directory is created, so a pre-existing
`crs-smoke`/`crs-secondary-smoke` symlink cannot evade the initial root check.
This keeps the existing verified invocation layout valid, blocks outside-root
and symlink escapes before a write, and does not depend on uninspected
Framework behavior. The same follow-up replaces the two duplicated literals
and corrects the four Python assertion argument orders reported on the initial
exact PR head.

## Changed files

- `common/scripts/run_local_runtime_smoke.py`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- `docs/reference/variables.md` and `docs/reference/variables.de.md`
- this English/German Change Record pair

The established Change Record indexes are not changed because unrelated open
Draft PRs already own those paths.

## Local validation

- `env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v
  tests.test_common_runtime_smoke_crs_source_security`: passed all 26 cases,
  including the pre-fix outside-output reproduction, all six direct output
  roots, a relative path, and a broad `/tmp` verified root rejected before a
  runner write; an existing-symlink escape, a symlink loop, and a pre-existing
  CRS config-suffix symlink rejected with Exit 77; and a valid verified-root
  control, in addition to the CRS source and generated-output controls.
- `python -m compileall -q common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py`:
  passed with bytecode outside the checkout.
- `git diff --check`: passed.

## Commands executed

- `python -m unittest -v tests.test_common_runtime_smoke_crs_source_security`
- `python -m compileall -q common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py`
- `python common/scripts/run_local_runtime_smoke.py --help`
- `git diff --check`

## Runtime evidence

The focused Python suite reaches the production resolver, direct-runner output,
and generated-configuration boundaries. It proves that a prepared fake CRS
tree below an ambient temporary environment is not selected; unsafe source,
evidence, runtime, audit, setup-output, and rule-output variants are rejected
before a parser input is returned; an outside direct `--config-root` was
created before the repair but is now rejected before `write_result` or a
runner-created directory; and an existing-symlink output escape, a symlink
loop, and a pre-existing CRS config-suffix symlink are rejected with Exit 77.
The legitimate controls preserve a valid verified-root layout and a generated
config with an allowed `Include` path under the selected trusted source. No
host connector or libmodsecurity evaluator is started by these fixtures.

## Security impact and remaining evidence

The changed route is CRS candidate selection plus generated-config/audit output
to the libmodsecurity rules parser, and the direct runner's CLI-output boundary.
The controls reject preseeded temp, unsafe sticky parent, symlink,
writable-content, stale-output, directive-injection/glob-expansion, outside
output-root, and symlink-output-escape variants before the affected sink,
while keeping legitimate explicit inputs and the verified runtime layout
working through the same resolver/policy.

## Known limitations

The local canonical `.codex/findings` store is mounted read-only, so the
EN/DE/JSON finding bundle is retained as a private import-ready artifact. The
Change Record index pair is deliberately not changed because independent open
Draft PRs own those paths.

## Remaining risks

Until this branch is integrated, unpatched master can still select the old
ambient temporary CRS candidates and lets direct runner CLI outputs escape the
verified runtime root. Same-UID races and filesystem ACL semantics remain
outside the POSIX owner/mode cross-user-integrity claim. No risk acceptance is
recorded.

## Checks not run and rationale

- A real CRS/libmodsecurity smoke is not run because the documented local
  runtime components are not provisioned.
- The repository-wide bilingual checker is run before delivery; in this
  isolated worktree it can remain blocked by absent Framework-submodule link
  targets. No Framework initialization or mutation is attempted.
- Hosted checks and exact-head SonarCloud analysis are current-head dependent.
  They are rerun after the follow-up commit/push and are not claimed by this
  local pre-delivery record.

## Final diff and review status

The final local Parent-only follow-up is on branch
`codex/sonar-common-crs-source-20260723-master-a308d7b`, based on the observed
master revision, and updates existing Draft PR #97. The final change-aware
security review, exact staged diff, hosted checks, and SonarCloud result must
be reconciled before verification is claimed.

## Delivery status

Draft PR #97 is open and must remain Draft and unmerged. This follow-up is
delivered only through its task branch; it neither updates the default branch
nor authorizes a merge.
