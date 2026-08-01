# FND-FRAMEWORK-0008 — Traefik-Native-Middleware-Runner hatte eine hard-coded UDS-Pfadgrenze

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0008` |
| Title / Titel | `Traefik-Native-Middleware-Runner hatte eine hard-coded UDS-Pfadgrenze` |
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

Der frühere Native-Middleware-Runner erzwang ein UDS-Verzeichnis, das das
Unix-Socket-Path-Limit überschreiten konnte, weil keine validierte
Short-Parent-Auswahl verfügbar war.

## Observed behavior / Beobachtetes Verhalten

Der Parent-Runner verwendete ein hard-coded `/var/tmp`-Kind. Er hatte keinen
expliziten validierten Short-Parent und lehnte nicht alle unsicheren
Parent-Pfadformen vor der Allokation des Socket-Kinds ab.

## Expected behavior / Erwartetes Verhalten

Der Runner wählt einen validierten kurzen task-owned Parent in der Reihenfolge
explizit, `TMPDIR` und erzeugter Fallback und lehnt unsichere Pfade vor der
Socket-Erstellung ab.

## Impact / Auswirkung

Die Path-Length-Grenze ist repariert und fokussierte Controls bestehen. Echte
Traefik/libmodsecurity-Host-Lifecycle-Evidence bleibt nicht verfügbar; finale
Cleanup-, Manifest-Leaf-Entfernungs- und Post-Readiness-Endpoint-Identity-
Grenzen werden getrennt durch `FND-PARENT-0013`, `FND-PARENT-0014` und
`FND-PARENT-0015` verfolgt.

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

- Ein expliziter Parent oder `TMPDIR` ist bei Nutzung ein dem aktuellen Benutzer
  gehörendes `0700`-Verzeichnis außerhalb des Checkouts ohne Symlink-Komponenten.
- Echte Host-Lifecycle-Validierung erfordert lokale Traefik- und
  libmodsecurity-Runtime-Eingaben.

## Reproduction / Reproduktion

- Einen langen oder unsicheren UDS-Parent vor der gehärteten Runner-Auswahl
  setzen oder die fokussierten Parent-/Path-Contract-Tests ausführen.

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:542-576`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '542,576p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/056-traefik-engine-service-double-observation-race-regression.log`; type: `native_uds_c17_regression_log`; SHA-256: `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`
  - Command: fokussierter nativer C17-Engine-Service-Build- und Lifecycle-Test; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`
- Run ID: `20260717T114213Z-feasibility-runtime-remediation-838d9adc`
  - Artifact: `logs/057-traefik-native-local-plugin-double-observation-contract.log`; type: `traefik_uds_contract_log`; SHA-256: `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`
  - Command: fokussierte Python-Runner-/Source-Contracts; working directory: `/root/git/ModSecurity-conector`; exit code: `0`; observed: `2026-07-17T13:55:00Z`; retention: `retained_task_log`

## Root-cause analysis / Grundursachenanalyse

Der Parent-Runner verwendete ein hard-coded `/var/tmp`-Kind und stellte keine
sichere validierte Short-Parent-Auswahl bereit. Dies ist keine
Framework-eigene Codeänderung.

## Proposed remediation / Vorgeschlagene Remediation

Den unterstützten Test-Harness-UDS-Root konfigurierbar machen oder ihn über eine autorisierte Schnittstelle verkürzen.

## Acceptance criteria / Akzeptanzkriterien

- Der native Traefik-Runner wählt einen autorisierten task-owned UDS-Root ohne
  Path-Length-Fehler.
- Fokussierte Path-, YAML-, Parent-Identity-, Collision-, Startup-, Protocol-,
  Allow-, Blocking- und Ordinary-Shutdown-Controls bestehen.
- Getrennte strikte Same-UID-Final-Cleanup-, Manifest-Leaf-Entfernungs- und
  Post-Readiness-Endpoint-Identity-Probleme werden verfolgt und nicht still als
  behoben behandelt.

## Validation plan / Validierungsplan

- Fokussierte Python-Runner-Contracts und native C17-Engine-Service-Controls ausführen.
- Den echten nativen Traefik-Lifecycle bei verfügbaren Host-Eingaben ausführen.
- Verifizieren, dass kein externer oder ursprünglicher MRTS-Pfad geändert wird.

## Regression tests / Regressionstests

- `tests/test_traefik_native_local_plugin.py`
- `connectors/traefik/build/test-engine-service-runtime.sh`

## Legitimate control tests / Legitime Kontrolltests

- Fokussierte C-Engine-Allow- und Blocking-Controls durch den nativen
  Protocol-Lifecycle.

## Dependencies / Abhängigkeiten

- `FND-PARENT-0013`, `FND-PARENT-0014` und `FND-PARENT-0015` verfolgen
  getrennte strikte Same-UID-Cleanup-, Manifest-Leaf- und Endpoint-Identity-
  Grenzen.

## Blockers / Blocker

- None / Keine

## Related findings / Verwandte Findings

- `FND-PARENT-0007`
- `FND-CROSS-0004`
- `FND-PARENT-0013`
- `FND-PARENT-0014`
- `FND-PARENT-0015`

## Residual risk / Restrisiko

Die hard-coded Short-Path-Grenze ist behoben. Die Live-Host-Runtime bleibt
`blocked_environment`, während getrennte Same-UID-Final-Cleanup-, Manifest-
Leaf- und Post-Readiness-Endpoint-Identity-Grenzen in `FND-PARENT-0013`,
`FND-PARENT-0014` und `FND-PARENT-0015` offen bleiben; es gibt keine
Risikoakzeptanz.

## Current task update / Aktueller Task-Stand

Der Parent-Native-Runner akzeptiert jetzt `TRAEFIK_ENGINE_SOCKET_PARENT`, dann
`TMPDIR` und erzeugt ansonsten einen kurzen privaten Fallback-Elternpfad.
Konfigurierte Elternpfade sind absolut, dem aktuellen Benutzer gehörend,
`0700`, außerhalb des Checkouts sowie frei von Symlink-Komponenten und
Steuerzeichen. Der YAML-Skalar ist quotiert und die Socket-Länge wird vor und
nach der Allokation geprüft. Der C-Service beobachtet die Pathname-Identität
jetzt doppelt um eine begrenzte `SO_PEERCRED`-Selbstprüfung herum, bevor er
Ownership erfasst; deterministische Pre-Bind-, Post-Bind- und Post-Probe-
Replacement-Controls bestehen.

- Feasibility: `feasible_now`
- Security-Ergebnis: fokussierte Path-, YAML-, Parent-Identity-, Collision-,
  Post-Bind-, Post-Probe- und Replacement-Sentinel-Controls bestanden.
- Evidence: `logs/056-traefik-engine-service-double-observation-race-regression.log`,
  SHA-256 `fd8d6bafee0adf474880625b73c26e719a114e60d44036fb141fc940658b36da`,
  Exit `0`; und `logs/057-traefik-native-local-plugin-double-observation-contract.log`,
  SHA-256 `8103a918dbb83bd07437f347cf9d30c6484391821b8459a8e5510fd05ad15dae`,
  Exit `0` (13 Tests).
- Runtime-Einschränkung: realer Traefik/libmodsecurity-Allow/Block-Lifecycle
  ist `blocked_environment`; es wird keine Host-Runtime-Behauptung aufgestellt.
- Strict-Same-UID-Disposition: `partial`; `FND-PARENT-0013` verfolgt finales
  Socket-Cleanup, `FND-PARENT-0014` Manifest-Leaf-Entfernung und
  `FND-PARENT-0015` Post-Readiness-Endpoint-Identity. Die Short-Path-
  Remediation dieses Findings ist `fixed`.

## Nachträgliche Task-Korrektur / Subsequent task correction

Dieses spätere Parent-only-Update übersteuert die frühere Current-Task-Aussage
zu TMPDIR und erzeugtem Fallback. Der Produktions-Runner verlangt jetzt nur
TRAEFIK_ENGINE_SOCKET_PARENT; er wählt kein TMPDIR und erzeugt keinen Parent.
Die Lifecycle-Route übergibt den Aufruferwert als Prozess-Environment-Daten,
und das native Make-Target erhält ihn vor der Python-Validierung als Raw-Daten.
FND-PARENT-0019 verfolgt und schließt den getrennt reproduzierten
Pre-Validation-Make-/Shell-Interpretationspfad. Die ursprüngliche
Short-Path-Remediation bleibt fixed und die bestehenden Same-UID-
Residual-Findings bleiben unverändert.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: phase_b_parent_fix — Ownership auf Parent korrigiert; fokussierte UDS-Security-Contracts bestanden, während Live-Runtime blockiert bleibt.
- `2026-07-17T13:57:53Z`: phase_b_native_uds_controls_updated — die Short-Parent-Remediation bleibt fixed; C17-Self-Probe-/Double-Observation-Controls und fokussierte Contracts bestanden, während `FND-PARENT-0013` die getrennte finale Cleanup-Grenze verfolgt.
- `2026-07-17T14:36:22Z`: same_uid_boundary_scope_corrected — die Short-
  Parent-Remediation bleibt im Scope fixed; finales Review fügte getrennte
  Manifest-Leaf- und Post-Readiness-Endpoint-Identity-Findings,
  `FND-PARENT-0014` und `FND-PARENT-0015`, hinzu, ohne sie als fixed zu
  behaupten.
