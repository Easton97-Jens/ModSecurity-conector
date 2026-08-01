# Change Record: Parent CI checks remaining SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-ci-checks-followup-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-checks-followup-remediation` |
| Date (UTC) | 2026-08-01 |
| Base revision | `caabf33c11d6002f9a1661f215ed195d6e141253` |
| Tracking | Current Parent `ci/checks/` inventory: 4 vulnerabilities, 5 maintainability findings, 0 security hotspots, and 0 duplicated lines. |
| Boundary | Parent `ci/checks/`, directly required Parent tests, and this English/German Change Record/index pair. Framework, MRTS, Gitlinks, workflows, scanner settings, suppressions, and `master` are unchanged. |

## Motivation and problem statement

The current master analysis retains nine unresolved source rows below
`ci/checks/`: `pythonsecurity:S2083` once, `python:S5443` three times,
`python:S108` once, and `python:S3776` four times. They concern a
test-matrix report writer, runtime-policy fixtures, an empty lifecycle branch,
and configuration-reference parsing/default/metadata dispatch. The remediation
must retain the checkers' fail-closed filesystem and runtime-path contracts
while addressing every source cause without a SonarQube Cloud setting,
suppression, exclusion, Quality-Gate workaround, or `NOSONAR` marker.

## Implementation decision and rationale

The language-switch generator now writes only paths selected by its checked-in
report registry after regular-file, resolved-in-checkout, and anti-symlink
validation. Its text rewrite is a pure helper with explicit negative controls.
The runtime-policy self-test now supplies the verified run root to child
temporary-path variables and uses a child of that root as its non-system
control fixture; it no longer sets broad `/tmp` fixtures.

The lifecycle checker represents the `profile` selection through its existing
empty error set instead of an empty control-flow branch. The configuration
reference keeps the generated inventory bytes stable while extracting YAML
line/stack/inline-field handling, source-default assertions, Envoy listener
selection context, and Traefik middleware/router descriptions into focused
helpers. This limits each responsibility without changing the documented
connector metadata contract.

## Acceptance criteria

- All nine current Parent `ci/checks/` SonarQube Cloud rows receive a source-level remediation without changing scanner controls.
- Report writes remain confined to selected regular, non-symlink files below the checkout, and the verified runtime-root control remains accepted.
- The exact Draft-PR head must show zero scoped open issues, zero new issues, and 0.0% New-Code duplication.

## Changed files

- `ci/checks/documentation/connector_config_reference.py`
- `ci/checks/documentation/ensure-test-matrix-language-switches.py`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_ensure_test_matrix_language_switches.py`
- `tests/test_runtime_path_policy.py`
- `reports/audits/change-records/README.md`, its German companion, and this
  English/German Change Record pair.

## Security impact

The report updater continues to reject symbolic links, non-regular files, and
resolved paths outside the checkout before a write is attempted. The new
registry-owned write path removes the generic caller-provided write target.
The runtime policy self-test continues to reject system and broad mutable
paths; using its verified run root for `RUNNER_TEMP` and `TMPDIR` narrows the
child process environment rather than broadening it. No credential, network,
workflow permission, scanner, or quality-control boundary is changed.

## Validation

| Command | Result |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m pip check` | passed: no broken requirements; selected Parent interpreter is Python 3.14.4. |
| Focused `unittest` selection for report switches, runtime-path controls, lifecycle evidence, and connector configuration reference | passed: 33 tests. |
| `python ci/checks/documentation/check-connector-config-reference.py` | passed: all eight inventories. |
| `python ci/checks/documentation/ensure-test-matrix-language-switches.py` | passed: `ok`, with no generated-file drift. |

## Commands executed

The commands in **Validation** were observed in the isolated Parent worktree.
`git diff --check`, final documentation validation, security-diff review, and
exact-head hosted validation remain separate final milestones.

## Runtime evidence

Not applicable. The change affects static Parent CI checkers and documentation
generation. The in-tree regular-file and rejected symlink/traversal controls
are filesystem-boundary evidence, not a connector runtime claim.

## Checks not run and rationale

- The one direct `RuntimePathPolicyTest.test_default_policy_selftest_ignores_caller_cache_overrides` subprocess control cannot run in this isolated Parent worktree because the Parent-pinned Framework Gitlink is intentionally not materialized there. It fails before exercising the changed Parent logic when its required `modules/ModSecurity-test-Framework/ci/lib/common.sh` path is absent. Framework materialization or modification is outside this task's authority.
- Full connector builds, runtime matrices, and Framework/MRTS checks were not run because no connector product source, Framework source, MRTS source, or Gitlink is in scope.
- Exact-head GitHub Actions, review state, and SonarQube Cloud results require the subsequent Draft PR and are not claimed by this local record.

## Known limitations and next evidence

The exact task-owned PR head must receive fresh SonarQube Cloud analysis before
the nine source rows can be marked fixed. The PR must show zero open scoped
issues, zero new issues, and 0.0% New-Code duplication. Required GitHub Actions
must be read at that same head. This record neither authorizes nor claims a
merge.

## Remaining risks

Structural documentation refactors can reveal an unusual template-path
diagnostic difference outside the focused fixtures. The security-sensitive
write and runtime-root boundaries have direct negative and legitimate controls,
but the exact PR head still needs independent hosted/Sonar verification.

## Final diff and review status

At record authoring, the candidate is limited to Parent `ci/checks/`, focused
Parent tests, and bilingual traceability files. No Framework/MRTS/Gitlink,
workflow, dependency, scanner configuration, suppression, or `master` change
is present. The final scoped review and delivery are not yet claimed.
