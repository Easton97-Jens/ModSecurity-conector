# FND-PARENT-0057 — Draft Parent PR #74 expands PR-controlled workflow output at a template-to-shell boundary

## Identity

| Field | Value |
| --- | --- |
| ID | FND-PARENT-0057 |
| Category | security_candidate |
| Repository / ownership | parent / parent |
| Priority / severity / confidence | P1 / medium / probable |
| Status / feasibility | in_progress / feasible_now |
| Release blocker | yes |
| Security assessment | plausible |
| Exact scope | Draft Parent PR #74, head 9046c69cc49145e70b18b5fc86a7c3fe67926d5a |

## Summary, scope, and invariant

The exact-head hosted zizmor job exited 11 with a template-injection signal at
.github/workflows/verified-report-governance.yml:150:31. The legacy Bash step
expanded a verified-evidence-paths staged-root workflow output after
checked-out PR code could write it. The same retained observation records
SonarQube Cloud vulnerability pythonsecurity:S8707 key
AZ-fw-Tf7_zRPd2N8_S2 at
ci/evidence/reports/stage-verified-full-matrix-evidence.py:65, where the
then-user-selectable --github-output reached Path.open.

The current local correction removes --github-output and Path.open entirely.
A static workflow step creates the private stage parent with umask, mktemp, and
chmod, sends only stage_parent through the workflow output into the
VERIFIED_EVIDENCE_STAGE_ROOT step environment mapping, and has stage/final
commands expand the quoted shell variable. No PR-derived step output may enter
run-script source through a GitHub Actions expression, and the stage CLI has
no user-selectable output-file sink.

This remains a plausible trust-boundary correction, not a claim of exploit
execution, credential disclosure, or successful bypass. It is separate from
the aggregate Quality-Gate record FND-SONAR-0016 and the full-matrix
port-range reliability record FND-PARENT-0058.

## Evidence and reproduction

Retained evidence is
/var/tmp/codex/ModSecurity-conector/runs/20260726T185607Z-pr74-fast-validation-hosted-followup/evidence/hosted-observation.md
(run 20260726T185607Z-pr74-fast-validation-hosted-followup, SHA-256
5c64b4fe03ed670b0d2c25c58c2f770b59ae53bab10851ced35bd9012117d956,
2,978 bytes). The read-only GitHub Actions failed-log and SonarQube Cloud
PR-#74 Quality-Gate/issues readback exited 0. PR #74 remains Draft; no risk
acceptance, close, merge, or delivery is claimed.

To reproduce the original condition, read GitHub Actions run 30215550687
failed logs, inspect the legacy workflow-output-to-stage-root source-to-sink
path, and trace the former --github-output argument to Path.open. To validate
the local correction, confirm that the CLI no longer exposes that argument or
sink; verify the static umask/mktemp/chmod stage-parent allocation,
stage_parent-only output hand-off into VERIFIED_EVIDENCE_STAGE_ROOT, and
quoted shell-variable use by both stage and final commands.

## Remediation, acceptance, and validation

The implemented local remediation removes --github-output and Path.open
entirely. It keeps private stage allocation workflow-owned through
umask/mktemp/chmod, maps only stage_parent through the output into
VERIFIED_EVIDENCE_STAGE_ROOT step environment, and supplies the stage/final
commands only a quoted shell variable. The strict full report-governance
producer remains required; the eight-second preflight is only an early
rejection path.

The correction is accepted only when:

- a successor exact PR #74 zizmor analysis has no active template-injection
  finding at the workflow path;
- no PR-written step output is interpolated into a run script;
- --github-output is absent or rejected by the stage CLI, and Path.open is not
  a reachable output-file sink;
- the static private parent, stage_parent-only environment hand-off, and
  quoted shell-variable commands are proven by focused negative and legitimate
  controls;
- the strict full producer, repository-native security checks, exact successor
  SonarQube Cloud, review, and protected integration pass without a rule,
  Quality-Gate, exclusion, suppression, coverage, Framework/MRTS/Gitlink, or
  control-weakening change; and
- FND-SONAR-0016 reaches its zero-open-findings criterion.

## Dependencies, residual risk, and history

Dependencies are FND-SONAR-0016 exact-successor zero-open-finding validation
and fresh hosted workflow, full-producer, review, and protected-integration
evidence. The local correction is implemented but unverified: it must prove
that the static private-parent environment hand-off preserves intended
controls without a new trust boundary. FND-PARENT-0058 remains a separate
test/runtime evidence-reliability defect.

The initial plausible correction was allocated at 2026-07-26T18:56:07Z. At
2026-07-26T19:55:51Z, the local removal of --github-output and Path.open plus
the static stage-parent environment hand-off was recorded. The finding remains
in_progress; no fixed, verified, or delivery disposition is claimed.
