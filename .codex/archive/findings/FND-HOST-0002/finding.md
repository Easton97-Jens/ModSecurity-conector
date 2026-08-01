# FND-HOST-0002 — Host prerequisites and optional analysis tools block selected evidence

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0002` |
| Title / Titel | `Host prerequisites and optional analysis tools block selected evidence` |
| Category / Kategorie | `tooling` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `host_environment` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `not_applicable` |
| Current scope disposition / Aktueller Scope-Status | `user_directed_current_local_test_scope` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

The host and local virtual environment remain at Python 3.14.4 while the Parent
contract declares 3.14.6, and native/optional tools remain unavailable. The
current user excludes exact local Python/native/optional-tool parity from the
current local test scope; this is not a product defect or evidence of an exact
hosted CI result.

## Observed behavior / Beobachtetes Verhalten

The canonical `.python-version` contains 3.14.6 and the workflow supplies it
to `actions/setup-python`, but the current host and local virtual environment
report Python 3.14.4 and no `python3.14.6` executable resolves on `PATH`.
Native host prerequisites and selected optional tools remain unavailable.

## Expected behavior / Erwartetes Verhalten

The finding is not applicable to the current local test scope. If exact local
Python/native/optional-tool parity becomes an acceptance or release criterion,
restore this triplet and rerun its original controls in an approved isolated
environment.

## Impact / Auswirkung

The unavailable local prerequisites do not block the user-selected current
scope. They remain unverified and cannot support a local exact-Python or hosted
CI claim.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `C++ evaluator`
- `apxs`
- `NGINX headers/source`
- `HAProxy headers/source`
- `Ruff`
- `Pyright`
- `actionlint`
- `zizmor`
- `gitleaks`
- `exact Python 3.14.6 CI lane`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '248,264p' .codex/reports/repository-full-assessment.md`
- `sed -n '1p' .python-version; python3 --version; command -v python3.14.6 || true`

## Evidence / Evidence

- Run ID: `20260716T193351Z-repository-full-assessment-0cb855ad`
  - Artifact: `.codex/reports/repository-full-assessment.md:248-264`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '248,264p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-16T22:46:50Z`; retention: `retained_local_report`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/136-python313-ci-lane-availability-final.log`; SHA-256:
    `36b6be11baae984e34c1babd5dcc4daa2bac83dbc2772756bfa36c99773ddaba`
  - Command: `python3 --version; command -v python3.13; if present,
    python3.13 --version; otherwise record unavailable`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T17:20:47Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

The retained evidence identifies the condition but does not establish a
product-code root cause. The Python CI-lane gap is a host-environment/version
availability limitation, not a product defect.

## Proposed remediation / Vorgeschlagene Remediation

No local provisioning is required for the user-selected current scope. Restore
this record and provision a reproducible isolated host/tool bundle only if
exact local parity becomes required.

## Acceptance criteria / Akzeptanzkriterien

- The archived record retains the observed host/tool condition and the current
  user scope decision without claiming it passed.
- No local exact-Python/native/optional-tool or hosted-CI result is represented
  as observed.
- If exact local parity becomes required, the complete triplet is restored and
  its original approved-environment controls are rerun.

## Validation plan / Validierungsplan

- Verify the lossless archive triplet, manifest hash, and removal from active
  finding summaries.
- If the scope is reactivated, record tool versions, commands, exits, and
  legitimate controls in an approved isolated environment.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- None for the user-selected current local scope. Restore this record before
  seeking an isolated exact Python/native/optional-tool environment.

## Blockers / Blocker

- None within the current local scope. The observed gaps remain retained for
  reactivation and are not represented as passed.

## Related findings / Verwandte Findings

- `FND-PARENT-0008`
- `FND-CROSS-0004`

## Residual risk / Restrisiko

No risk is accepted. Exact local Python/native/optional-tool validation and a
hosted CI result remain unobserved; restore and revalidate before relying on
either as an acceptance or release claim.

## Current user-directed archive and scope disposition — 2026-07-26

The current user selected a local test scope in which the exact local Python
3.14.6/native/optional-tool parity is cosmetic rather than a blocker because
GitHub can lead the host environment. Accordingly, this record is
`not_applicable` for that scope and is archived losslessly; it is not
technically closed or proven on an exact local or hosted CI lane.

Current decision evidence: run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.
No tool provisioning, host mutation, product change, or hosted CI execution
occurred. Before any local-parity, production, publication, or release claim,
restore the complete triplet and run its original approved-environment controls.

Archive location: `.codex/archive/findings/FND-HOST-0002/`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T17:20:47Z`: python_313_ci_lane_host_gap_recorded — The host
  supplied Python 3.14.4 and no `python3.13` executable. Focused Python
  contracts remain valid local control evidence but do not establish the
  declared Python-3.13 CI lane. No interpreter installation was attempted.

## Current Go toolchain blocker — 2026-07-23

Current master `a308d7b414f0859490fe7253e0683a4bde80b563` declares Go `1.26.5`
for the actual Envoy and Traefik modules. The installed host executable is
`go1.26.0 linux/amd64`; a controlled `GOTOOLCHAIN=local go mod graph` in the
Envoy module exits `1` before dependency resolution with:

```text
go.mod requires go >= 1.26.5 (running go 1.26.0; GOTOOLCHAIN=local)
```

No local `go1.26.5` executable or cached side-by-side toolchain was found. No
implicit download or installation was attempted. The safe next step requires
explicit current-user authorization for an official Go `1.26.5` toolchain used
only under the registered task cache; it must not replace a system/user-local
toolchain or modify project manifests as a side effect.

Retained evidence:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T161931Z-github-alert-reconciliation-20260723-65ec68cf/evidence/go/01-go-mod-graph-local-toolchain-block.log`
(SHA-256 `6fcac7c9821e4b4faf044b31777003615683879da3d4ad4b3042669d1a57e26c`).
## Go toolchain resolution for this task — 2026-07-23

The current user authorized an official Go 1.26.5 archive only inside the
registered task cache. Its SHA-256 matched
5c2c3b16caefa1d968a94c1daca04a7ca301a496d9b086e17ad77bb81393f053, and the
task-local executable reported Go 1.26.5 linux/amd64. It was used with isolated
GOCACHE, GOMODCACHE, GOPATH, GOTMPDIR, GOWORK=off, GOTOOLCHAIN=local, and
GOFLAGS=-mod=readonly.

That narrow Go blocker is resolved for this task: Envoy dependency validation
and Traefik fuzz validation completed, and Draft PRs #99 and #100 both passed
their exact-head checks. No system/user Go installation or global configuration
was changed. This does not resolve this finding's remaining Python 3.13, native
host, or optional-tool gaps, so its overall blocked status remains unchanged.

Retained delivery evidence:
 /var/tmp/codex/ModSecurity-conector/runs/20260723T165434Z-github-alert-remediation-go1265-4fc93743/evidence/delivery/20260723-draft-pr-delivery-alert-state.md
(SHA-256 7508110eef978259f0b9757df675844535b44bd5e6a4dc30c92d265da05110de).

## Current host prerequisite revalidation — 2026-07-26

The canonical Parent target is exact Python 3.14.6. The current host and local
virtual environment report only Python 3.14.4, no `python3.14.6` executable
resolves, and the scoped native/optional-tool inventory remains unavailable.
The retained current evidence is run
`20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`, artifact
`evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`, SHA-256
`81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.

No installation, host mutation, product change, or delivery action was
attempted. The finding remains `blocked_environment` pending an explicitly
authorized isolated tool bundle or host-owner provisioning.
