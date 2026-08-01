# FND-PARENT-0013 — Traefik pathname UDS cleanup retains a same-UID final unlink race

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-PARENT-0013` |
| Title / Titel | `Traefik pathname UDS cleanup retains a same-UID final unlink race` |
| Category / Kategorie | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priority / Priorität | `P1` |
| Severity / Severity | `medium` |
| Confidence / Confidence | `probable` |
| Status | `blocked` |
| Feasibility status / Machbarkeitsstatus | `blocked_missing_evidence` |
| Release blocker / Release-Blocker | `true` |
| Security relevance / Security-Relevanz | `true` |

## Summary / Zusammenfassung

The native UDS service revalidates pathname socket identity before cleanup, but
POSIX/Linux has no atomic unlink-if-this-inode operation. A hostile process
sharing the service UID and directory mutation authority can replace the final
pathname after `lstat()` and before `unlink()`.

## Observed behavior / Beobachtetes Verhalten

The strengthened double-observation and `SO_PEERCRED` self-probe close the
pre-capture replacement windows. The final cleanup nevertheless checks
device/inode/owner with `lstat()` and performs a separate pathname `unlink()`.

## Expected behavior / Erwartetes Verhalten

A strict foreign-object safety claim requires either no automatic pathname
deletion or a verified trust boundary that prevents same-UID directory
mutation. It must not claim unavailable atomic conditional unlink semantics.

## Impact / Auswirkung

The configured `0700` child protects against other UIDs and ordinary
replacement is fail-closed. It is not isolation from a hostile process with the
same UID, so the requested strict no-foreign-socket-cleanup guarantee is not
fully proven.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/README.md`
- `connectors/traefik/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`

### Symbols / Symbole

- `traefik_engine_remove_owned_socket`
- `TRAEFIK_ENGINE_SOCKET_PARENT`

## Preconditions / Voraussetzungen

- A hostile process shares the service effective UID.
- It can search and mutate the private UDS child directory.
- It replaces the pathname after final `lstat()` and before `unlink()`.

## Reproduction / Reproduktion

- Inspect `traefik_engine_remove_owned_socket()`: `lstat()` validates a
  pathname entry and `unlink()` consumes the pathname in a later operation.
- No documented POSIX/Linux unlink API accepts an expected inode, descriptor,
  or file-handle predicate.

## Evidence / Evidence

- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/058-traefik-uds-final-unlink-static-review.log`; type:
    `source_to_sink_security_review_log`; SHA-256:
    `207b674e7d6842521d6a25b0e0dd4432ba939e5fe6426538636ba12e14e336aa`
  - Command: focused `rg` source-to-sink review; working directory:
    `/root/git/ModSecurity-conector`; exit code: `0`; observed:
    `2026-07-17T13:57:53Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/056-traefik-engine-service-double-observation-race-regression.log`;
    type: `native_uds_c17_regression_log`; SHA-256:
    `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`
  - Command: focused native C17 engine-service build and lifecycle test;
    working directory: `/root/git/ModSecurity-conector`; exit code: `0`;
    observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Pathname AF_UNIX cleanup uses a check-then-unlink interface. The OS API has no
expected-object predicate for unlink, and the current architecture has a
same-UID private directory rather than a separately trusted cleanup authority.

## Proposed remediation / Vorgeschlagene Remediation

Choose and prove one new boundary: never automatically unlink pathname sockets
and surface `cleanup_incomplete`; use a separately owned trusted cleanup
authority; or establish compatible abstract-AF_UNIX support end to end. Do not
weaken existing pre-bind collision, identity, or cleanup-refusal controls.

## Acceptance criteria / Akzeptanzkriterien

- The final cleanup path never claims atomic unlink-if-inode behavior.
- Either automatic pathname deletion is disabled fail-closed, or an
  independently verified trust boundary prevents same-UID path replacement.
- Existing short-path, collision, symlink, replacement, Allow, Blocking,
  startup, shutdown, and residue controls remain covered where feasible.

## Validation plan / Validierungsplan

- Validate the selected boundary with a real hostile same-UID replacement test.
- Run the native C17 engine self-test and protocol lifecycle controls.
- Run focused runner contracts and the genuine host lifecycle when available.

## Regression tests / Regressionstests

- `connectors/traefik/build/test-engine-service-runtime.sh`
- `tests/test_traefik_native_local_plugin.py`
- A future real same-UID final-unlink boundary test after an architectural solution.

## Legitimate control tests / Legitime Kontrolltests

- Normal focused native-engine startup, protocol, Allow, and Blocking controls pass.
- A post-start replacement sentinel is retained and the service reports
  `socket_cleanup` rather than deleting it.

## Dependencies / Abhängigkeiten

- A user-authorized cleanup trust-boundary decision or compatible
  abstract-AF_UNIX design evidence.

## Blockers / Blocker

- No current repository-supported atomic conditional pathname unlink or
  separately owned cleanup authority.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0008`
- `FND-PARENT-0014`
- `FND-PARENT-0015`

## Residual risk / Restrisiko

The private-child design is collision mitigation across UIDs, but a same-UID
mutator may race the final `lstat()`-to-`unlink()` interval. No risk acceptance
has been provided by the current user.

## History / Historie

- `2026-07-17T13:57:53Z`: `current_task_security_boundary_identified` —
  post-bind and post-probe capture windows were hardened and tested, but
  source-to-sink review confirmed the separate final same-UID pathname limit.
  No architectural trust-boundary decision or user risk acceptance is present.
- `2026-07-17T14:36:22Z`: `related_same_uid_boundaries_separated` — the
  independent final review retained this final cleanup race separately from
  manifest leaf removal (`FND-PARENT-0014`) and post-readiness Traefik endpoint
  redirection (`FND-PARENT-0015`).
