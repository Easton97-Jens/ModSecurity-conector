# Change Record: Verified report evidence gate

**Language:** English | [Deutsch](CR-20260718-verified-report-evidence-gate.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260718-verified-report-evidence-gate` |
| Date (UTC) | `2026-07-18` |
| Base revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Boundary | Parent workflow and focused Parent test only; Framework and MRTS are unchanged. |
| 2026-07-26 extension boundary | Parent-only source/test remediation that uses the public Framework API recorded by the existing gitlink at `77d73decd094a8f289fbe0ef2582f12430923e24`; Framework/MRTS source and gitlinks remain unchanged. |
| 2026-07-26 finding status | `FND-PARENT-0050` and `FND-CROSS-0001` remain open pending fresh evidence; the #74 Apache producer blocker is separate. |

## Motivation and problem statement

The `verified-report-governance` workflow ran `make report-governance`, whose
checker deliberately uses `--governance-only`. It could therefore report a
successful governance result while critical runtime evidence was stale or
incomplete. The strict `verified-report-evidence-gate` target already existed
but no workflow invoked it.

## Acceptance criteria

- The verified-report workflow executes the strict
  `make verified-report-evidence-gate` after its non-evidence governance
  check.
- A focused regression test fails if the strict workflow invocation is
  removed or placed before the governance check.
- The change neither regenerates reports nor treats governance output as
  runtime evidence.
- Framework and MRTS source, gitlinks, and generated report files remain
  unchanged.

### 2026-07-26 extension criteria

- Parent ModSecurity v3 source preparation uses the public Framework
  `ci_provision_approved_modsecurity_v3_checkout` API instead of generic V3
  acquisition; rejected configuration or bridge results cannot fall back to
  `prepare_git_component`.
- The Parent reserves a marker-owned but absent staging child for the
  Framework's fresh-only API, then verifies, seals, and atomically publishes
  it only after Framework approval.
- Follow-up source metadata uses verified `/usr/bin/git` with a minimal,
  scrubbed environment rather than caller-controlled Git state.
- A post-provision Framework verification rejection preserves an existing
  complete final cache and removes only the staging path and marker; it cannot
  write a completion marker or publish the rejected checkout.
- Local Parent and read-only Framework regression controls are recorded below;
  no connector runtime evidence, exact-head hosted success, or merge is
  claimed.

## Implementation decision and rationale

Keep `report-governance` as the existing layout/path/documentation control and
add a distinct strict evidence-gate step to the workflow. This is the narrowest
Parent-native enforcement point: the strict Make target already invokes the
same checker without `--governance-only`, so it fails closed on stale or
blocked critical runtime evidence.

## Changed files

- `.github/workflows/verified-report-governance.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- this English/German Change Record pair
- `ci/provisioning/components/prepare-runtime-components.py` (2026-07-26
  extension): replace generic ModSecurity v3 acquisition with the
  Framework-owned provisioning bridge and fail-closed cache publication flow.
- `tests/test_prepare_runtime_components.py` (2026-07-26 extension): cover
  bridge provenance, trusted metadata, generic-fallback exclusion, and
  post-provision rejection preservation.

## Commands executed

| Command | Result |
| --- | --- |
| `make report-governance` with task-owned runtime roots | passed: the governance-only checker reported `PASS`; its path-policy helper attempted no successful system-path write in the sandbox. |
| `python ci/checks/documentation/check-generated-report-layout.py --connector-root <Parent> --framework-root <Framework>` | expected failure: strict mode rejected current stale critical runtime/report inputs. |
| `PYTHONDONTWRITEBYTECODE=1 <Parent venv>/bin/python -m unittest -v tests.test_ci_security_workflows` before the workflow change | expected failure: the newly added regression test found no strict gate invocation. |
| `PYTHONDONTWRITEBYTECODE=1 <Parent venv>/bin/python -m unittest -v tests.test_ci_security_workflows` after the workflow change | passed: 6 tests. |
| `git diff --check` | passed. |

## Security impact

The workflow no longer lets a governance-only PASS stand in for verified
runtime evidence. It uses the existing strict report evidence control and does
not weaken stale-input, blocked-input, checksum, manifest, path, or runtime
diagnostic checks.

The 2026-07-26 extension also keeps ModSecurity v3 acquisition at the
Framework-owned immutable-provenance boundary. The Parent uses the recorded
public API for a fresh checkout, retains the existing build-time Framework
verification, and cannot publish a bridge-created checkout until a separate
post-provision verification has passed. The metadata probes use the verified
host Git path with a scrubbed environment; no generic Git acquisition,
permission, secret, runtime, or report-evidence control is weakened.

## Runtime evidence

No connector runtime was executed or promoted. The change enforces evidence
validation; it does not create runtime evidence.

The 2026-07-26 Parent 44-test and Framework 18-test controls are local
unit/security-regression evidence only. They do not establish a connector
runtime result, exact-head hosted result, review disposition, merge, or
resulting-master evidence.

## Delivery evidence (observed 2026-07-18 UTC)

- The implementation was committed and pushed on
  `agent/harden-evidence-integrity` as
  `42b31f1c84c0c915a5cb65119714613fbf3e0c40`
  (`ci: enforce verified runtime evidence gate`).
- Draft PR [#55](https://github.com/Easton97-Jens/ModSecurity-conector/pull/55)
  was `OPEN` against `master` at observation. At that observation, local `HEAD`,
  `origin/agent/harden-evidence-integrity`, and the PR head all resolved to
  `42b31f1c84c0c915a5cb65119714613fbf3e0c40`.
- CodeQL passed (check run `88069241639`); SonarCloud Code Analysis passed
  (check run `88069255373`).
- The check view at that observation contained two `report-governance` failures:
  [job `88069138522`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29640117282/job/88069138522)
  and [job `88069198804`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29640140820/job/88069198804).
  In the latter, setup and `Generated report governance` passed while
  `Verified runtime evidence gate` failed. Other observed checks passed or
  were skipped by their documented scope; no pending or cancelled result was
  observed.
- The delivery state at that observed head was `not_verified_pr`. This is intentional fail-closed
  behavior: a strict-gate failure cannot be treated as runtime-evidence
  success.

## Known limitations

The current strict checker correctly fails because existing critical reports
are stale. `FND-CROSS-0001` (`Evidence freshness manifest contains stale
entries and SHA mismatches`) remains `validated`; its current assessment
records 58 stale entries and 9 SHA mismatches. This cross-repository evidence
work must not be silenced, regenerated by hand, or reclassified by this
workflow-only change.

`FND-PARENT-0050` and `FND-CROSS-0001` remain open pending fresh evidence.
The #74 Apache producer blocker is separate from this Parent-only V3 bridge
extension and is neither fixed nor reclassified here.

## Remaining risks

The failed strict gate remains a delivery blocker until the owner of
`FND-CROSS-0001` reconciles the stale freshness entries and checksum mismatch
evidence through the established runtime-evidence path. It is counterevidence
to a forged governance-only success, not a defect in this gate.

The bridge fails closed if Framework provisioning, post-provision verification,
metadata collection, sealing, or atomic publication cannot complete. That
preserves an existing final cache rather than treating it as fresh evidence.
Fresh runtime evidence, exact-head hosted validation, review, and merge
evidence remain required before any delivery-success claim. No risk is
accepted, and the separate #74 Apache producer blocker remains outside this
extension.

## Checks not run and rationale

No generator refresh, connector build, runtime harness, Framework change, or
MRTS operation ran. A refresh would cross the established evidence-generation
boundary and cannot be substituted for a verified runtime run. The current
GitHub Actions, CodeQL, and SonarCloud results are recorded above for the
observed exact PR head SHA.

For the 2026-07-26 extension, no connector runtime, hosted exact-head CI,
SonarQube Cloud, review, merge, resulting-master workflow, Framework change,
MRTS operation, or #74 Apache producer remediation ran. The recorded local
controls cannot substitute for any of those evidence classes.

## Final diff and review status

The focused local regression test, YAML parse, and diff whitespace check
passed. Commit, push, Draft PR creation, exact-head equality, GitHub Actions,
CodeQL, and SonarCloud are observed above. GitHub reports no review decision.
The strict evidence-gate failure kept that observed head at `not_verified_pr`;
this documentation correction requires a fresh exact-head cycle before any
new delivery claim. No merge is authorized or performed.

## Extension: Parent Framework public V3 provisioning bridge (2026-07-26 UTC)

This dated extension preserves the 2026-07-18 delivery evidence above as a
historical observation. It records a separate Parent-only remediation that
uses the Framework public
`ci_provision_approved_modsecurity_v3_checkout` API at the Framework revision
already recorded by the Parent gitlink,
`77d73decd094a8f289fbe0ef2582f12430923e24`. It makes no Framework-source,
MRTS-source, or gitlink change.

The Parent no longer delegates ModSecurity v3 acquisition to generic
`prepare_git_component`. After the existing provenance configuration guard
passes, it reserves only a managed registry marker for a new, absent staging
child. The Framework API owns creation of that fresh child. The Parent then
performs a Framework checkout verification, reads metadata through verified
`/usr/bin/git` with a minimal scrubbed environment, seals the managed cache
entry, and atomically publishes it. An existing final cache is not touched
until all of those steps pass.

The post-provision rejection regression creates an existing complete final
cache, lets the Framework bridge report success after creating the marker-owned
absent staging child, and then rejects that child through
`verify_framework_approved_modsecurity_v3_checkout`. It proves that the
returned record is blocked with the post-provision guard classification, the
final cache contents and completion marker remain intact, the staging path and
marker are removed, and neither `write_cache_entry_completion`,
`atomic_publish_dir`, nor generic `prepare_git_component` is used.

### Local controls observed on 2026-07-26 UTC

| Control | Result |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 MODSECURITY_FRAMEWORK_TEST_ROOT=<read-only Framework at 77d73decd094a8f289fbe0ef2582f12430923e24> <Parent venv>/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract` | passed: 44 Parent tests in 8.752s. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external root> <Parent venv>/bin/python -m unittest -v tests.security_regression.test_modsecurity_v3_git_ref_provenance` in the isolated read-only Framework worktree at `77d73decd094a8f289fbe0ef2582f12430923e24` | passed: 18 Framework tests in 61.476s; only task-owned temporary fixtures were used, with no Framework source, gitlink, or MRTS modification. |
| `rtk git diff --check` in the #55 Parent worktree before this documentation amendment | passed. |
| `rtk make check-bilingual-docs` after this documentation amendment | blocked_environment: 20 existing missing local link targets below the uninitialized `modules/ModSecurity-test-Framework` gitlink; no diagnostic named either changed Change Record. |
| `rtk env PYTHON=<Parent venv> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-bilingual-docs` after materializing the already-recorded Framework/MRTS revisions in this isolated task worktree | passed: `bilingual docs ok`; materialization changed no Framework/MRTS source, gitlink, branch, or delivery state. |
| `rtk git diff --check` after this documentation amendment | passed. |

These are local control results, not runtime evidence. No current exact Parent
commit, exact-head hosted CI success, SonarQube Cloud result, review outcome,
merge, or resulting-master result is claimed by this extension.
