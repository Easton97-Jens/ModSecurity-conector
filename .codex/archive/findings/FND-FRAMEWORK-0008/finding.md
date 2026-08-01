# FND-FRAMEWORK-0008 — Traefik native middleware runner had a hard-coded UDS path boundary

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0008` |
| Title / Titel | `Traefik native middleware runner had a hard-coded UDS path boundary` |
| Category / Kategorie | `runtime_defect` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `reproduced` |
| Status | `fixed` |
| Feasibility status / Machbarkeitsstatus | `feasible_now` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The former native middleware runner forced a UDS directory that could exceed
the Unix-socket pathname limit because no validated short-parent selection was
available.

## Observed behavior / Beobachtetes Verhalten

The Parent runner used a hard-coded `/var/tmp` child. It had no explicit,
validated short parent, and it did not reject all unsafe parent-path forms
before allocating the socket child.

## Expected behavior / Erwartetes Verhalten

The runner selects a validated short task-owned parent in explicit, `TMPDIR`,
then generated-fallback order and rejects unsafe paths before socket creation.

## Impact / Auswirkung

The path-length boundary is repaired and focused controls pass. Genuine
Traefik/libmodsecurity host lifecycle evidence remains unavailable; final
cleanup, manifest-leaf removal, and post-readiness endpoint-identity limits are
separately tracked by `FND-PARENT-0013`, `FND-PARENT-0014`, and
`FND-PARENT-0015`.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md`
- `connectors/traefik/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`

### Symbols / Symbole

- `TRAEFIK_ENGINE_SOCKET_PARENT`
- `resolve_engine_socket_parent`
- `traefik_engine_capture_bound_socket_identity`
- `Unix-domain socket path limit`

## Preconditions / Voraussetzungen

- An explicit parent or `TMPDIR`, when used, is a current-user-owned `0700`
  directory outside the checkout without symlink components.
- Genuine host lifecycle validation requires local Traefik and libmodsecurity
  runtime inputs.

## Reproduction / Reproduktion

- Set a long or unsafe UDS parent before the hardened runner selection, or run
  the focused parent/path contract tests.

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:542-576`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '542,576p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/056-traefik-engine-service-double-observation-race-regression.log`; type: `native_uds_c17_regression_log`; SHA-256: `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`
  - Command: focused native C17 engine-service build and lifecycle test; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/057-traefik-native-local-plugin-double-observation-contract.log`; type: `traefik_uds_contract_log`; SHA-256: `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`
  - Command: focused Python runner/source contracts; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

The Parent runner used a hard-coded `/var/tmp` child and did not expose a safe,
validated short-parent selection. This is not a Framework-owned code change.

## Proposed remediation / Vorgeschlagene Remediation

Make the supported test harness UDS root configurable or otherwise shorten it through an authorized interface.

## Acceptance criteria / Akzeptanzkriterien

- The native Traefik runner selects an authorized task-owned UDS root without
  path-length failure.
- Focused path, YAML, parent-identity, collision, startup, protocol, Allow,
  Blocking, and ordinary shutdown controls pass.
- Separate strict same-UID final-cleanup, manifest-leaf-removal, and
  post-readiness endpoint-identity issues are tracked rather than silently
  treated as fixed.

## Validation plan / Validierungsplan

- Run focused Python runner contracts and native C17 engine-service controls.
- Run the genuine native Traefik lifecycle when host inputs are available.
- Verify no external or original MRTS path is modified.

## Regression tests / Regressionstests

- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/build/test-engine-service-runtime.sh`

## Legitimate control tests / Legitime Kontrolltests

- Focused C engine Allow and Blocking controls through the native protocol lifecycle.

## Dependencies / Abhängigkeiten

- `FND-PARENT-0013`, `FND-PARENT-0014`, and `FND-PARENT-0015` track distinct
  strict same-UID cleanup, manifest-leaf, and endpoint-identity boundaries.

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0007`
- `FND-CROSS-0004`
- `FND-PARENT-0013`
- `FND-PARENT-0014`
- `FND-PARENT-0015`

## Residual risk / Restrisiko

The hard-coded short-path boundary is fixed. Live host runtime remains
`blocked_environment`, while distinct same-UID final cleanup, manifest-leaf,
and post-readiness endpoint-identity limits remain open in `FND-PARENT-0013`,
`FND-PARENT-0014`, and `FND-PARENT-0015`; no risk has been accepted.

## Current task update / Aktueller Task-Stand

The Parent native runner now accepts `TRAEFIK_ENGINE_SOCKET_PARENT`, then
`TMPDIR`, and otherwise creates a short private fallback parent. Configured
parents are absolute, current-user-owned, `0700`, outside the checkout, free
of symlink components and control characters. The YAML scalar is quoted and
the socket length is checked before and after allocation. The C service now
double-observes pathname identity around a bounded `SO_PEERCRED` self-probe
before recording ownership; deterministic pre-bind, post-bind, and post-probe
replacement controls pass.

- Feasibility: `feasible_now`
- Security result: focused path, YAML, parent-identity, collision, post-bind,
  post-probe, and replacement-sentinel controls passed.
- Evidence: `logs/056-traefik-engine-service-double-observation-race-regression.log`,
  SHA-256 `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`,
  exit `0`; and `logs/057-traefik-native-local-plugin-double-observation-contract.log`,
  SHA-256 `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`,
  exit `0` (13 tests).
- Runtime limitation: real Traefik/libmodsecurity Allow/Block lifecycle is
  `blocked_environment`; no host runtime claim is made.
- Strict same-UID disposition: `partial`; `FND-PARENT-0013` tracks final
  socket cleanup, `FND-PARENT-0014` manifest leaf removal, and
  `FND-PARENT-0015` post-readiness endpoint identity. This finding's short-path
  remediation is `fixed`.

## Subsequent task correction / Nachträgliche Task-Korrektur

This later Parent-only update supersedes the earlier current-task statement
about TMPDIR and a generated fallback. The production runner now requires only
TRAEFIK_ENGINE_SOCKET_PARENT; it does not select TMPDIR or generate a parent.
The lifecycle route carries the caller value as process-environment data, and
the native Make target preserves it as raw data before Python validation.
FND-PARENT-0019 records and closes the separately reproduced pre-validation
Make/shell interpretation path. The original short-path remediation remains
fixed and the existing same-UID residual findings remain unchanged.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_parent_fix — ownership corrected to Parent; the focused UDS security contracts passed while live runtime remains blocked.
- `2026-07-17T13:57:53Z`: phase_b_native_uds_controls_updated — the short-parent remediation remains fixed; C17 self-probe/double-observation controls and focused contracts passed, while `FND-PARENT-0013` tracks the separate final cleanup boundary.
- `2026-07-17T14:36:22Z`: same_uid_boundary_scope_corrected — the short-parent
  remediation remains fixed in scope; final review added distinct manifest-leaf
  and post-readiness endpoint-identity findings, `FND-PARENT-0014` and
  `FND-PARENT-0015`, without claiming them fixed.
