# FND-HOST-0004 — NGINX-HTTP/3-Nachweis ist durch fehlende HTTP/3-Client-Capability blockiert

## Identity / Identität

| Field / Feld | Value / Wert |
| --- | --- |
| ID | `FND-HOST-0004` |
| Title / Titel | `NGINX-HTTP/3-Nachweis ist durch fehlende HTTP/3-Client-Capability blockiert` |
| Category / Kategorie | `protocol_gap` |
| Repository / Repository | `host_environment` |
| Ownership / Ownership | `external_tool` |
| Priority / Priorität | `P2` |
| Severity / Severity | `not_applicable` |
| Confidence / Confidence | `confirmed` |
| Status | `not_applicable` |
| Current task disposition / Aktueller Task-Status | `user_directed_not_applicable_current_local_test_scope` |
| Release blocker / Release-Blocker | `false` |
| Security relevance / Security-Relevanz | `false` |

## Summary / Zusammenfassung

Das aktuelle curl unterstützt HTTP/2, aber nicht HTTP/3, und kein alternativer
H3-Client oder erzwungener protokollkorrelierter H3-Harness-Fall ist verfügbar.
Der aktuelle Nutzer schließt HTTP/3 aus dem aktuellen lokalen Testumfang aus;
dies ist weder ein NGINX-Connector-Fehler noch ein HTTP/3-Validierungsergebnis.

## Observed behavior / Beobachtetes Verhalten

Das aktuelle curl unterstützt HTTP/2, aber nicht HTTP/3; dies ist eine Client-Capability-Limitierung, kein NGINX-Connector-Fehler.

## Expected behavior / Erwartetes Verhalten

Das Finding ist für den aktuellen lokalen Testumfang nicht anwendbar. Wenn
HTTP/3 zu einem Akzeptanz-, Produktions-, Veröffentlichungs- oder
Release-Kriterium wird, ist dieses Tripel wiederherzustellen und ein
HTTP/3-fähiger Client plus ein protokollkorrelierter H3-Allow-Control
auszuführen.

## Impact / Auswirkung

Die nicht verfügbare HTTP/3-Route blockiert den nutzergewählten aktuellen Scope
nicht. Sie bleibt unverifiziert und kann keinen HTTP/3- oder
Connector-Behavior-Claim stützen.

## Affected files and symbols / Betroffene Dateien und Symbole

### Files / Dateien

- `.codex/reports/repository-full-assessment.md`

### Symbols / Symbole

- `curl 8.18.0`
- `--http3-only`

## Preconditions / Voraussetzungen

- The retained assessment evidence and its referenced revision remain available.

## Reproduction / Reproduktion

- `sed -n '561,570p' .codex/reports/repository-full-assessment.md`

## Evidence / Evidence

- Run ID: `20260717T085050Z-mrts-protocol-hardening-readiness-57010656`
  - Artifact: `.codex/reports/repository-full-assessment.md:561-570`
  - Type: `bilingual_assessment_report`; SHA-256: `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`
  - Command: `sed -n '561,570p' .codex/reports/repository-full-assessment.md`
  - Working directory: `/root/git/ModSecurity-conector`; exit code: `0`
  - Observed at: `2026-07-17T09:23:19Z`; retention: `retained_local_report`

## Root-cause analysis / Grundursachenanalyse

Die retained Evidence belegt den Zustand, aber keine Produktcode-Grundursache.

## Proposed remediation / Vorgeschlagene Remediation

Für den nutzergewählten aktuellen Scope ist keine HTTP/3-Aktion erforderlich.
Diesen Record wiederherstellen und einen autorisierten HTTP/3-fähigen Client
plus isolierte protokollkorrelierte Route nur bereitstellen, wenn H3
erforderlich wird.

## Acceptance criteria / Akzeptanzkriterien

- Der archivierte Record bewahrt den nicht verfügbaren HTTP/3-Client-/Harness-
  Zustand und die aktuelle Nutzer-Scope-Entscheidung, ohne einen H3-Pass zu
  behaupten.
- Keine HTTP/3-Client-Capability, H3-Runtime oder Connector-Behavior wird als
  beobachtet dargestellt.
- Wenn H3 erforderlich wird, ist das vollständige Tripel wiederherzustellen und
  ein HTTP/3-fähiger, protokollkorrelierter Allow-Control auszuführen.

## Validation plan / Validierungsplan

- Verlustfreies Archivtripel, Manifest-Hash und Entfernung aus aktiven
  Finding-Übersichten prüfen.
- Bei Reaktivierung des Scope einen HTTP/3-fähigen Client-Probe und
  protokollkorrelierten NGINX-H3-Allow-Control ausführen.

## Regression tests / Regressionstests

- Add or retain a focused regression/evidence control for the recorded condition.

## Legitimate control tests / Legitime Kontrolltests

- Run the unaffected allow/control behavior in the same scoped environment.

## Dependencies / Abhängigkeiten

- Keine für den nutzergewählten aktuellen lokalen Scope. Diesen Record vor der
  Anforderung eines isolierten HTTP/3-fähigen Clients und einer NGINX-H3-Runtime
  wiederherstellen.

## Blockers / Blocker

- Keine innerhalb des aktuellen lokalen Scope. Der nicht verfügbare
  Client-/Harness-Zustand bleibt für die Reaktivierung aufbewahrt und wird nicht
  als bestanden dargestellt.

## Related findings / Verwandte Findings

- `FND-FRAMEWORK-0009`

## Residual risk / Restrisiko

Es wird kein Risiko akzeptiert. HTTP/3-Client-Capability, ein
protokollkorrelierter H3-Harness-Control und Connector-Behavior bleiben
unbeobachtet; vor jeder H3-, Produktions-, Veröffentlichungs- oder
Release-Nutzung wiederherstellen und neu validieren.

## Current task disposition / Aktueller Task-Stand

`not_applicable` für den nutzergerichteten aktuellen lokalen Testumfang

Die Feature-Liste des aktuellen curl 8.18.0 enthält HTTP2, aber kein HTTP3,
und weder `nghttp` noch `h3` lösen über `PATH` auf. Der Parent-Harness zeichnet
für die H3-Route absichtlich nur Start-/TCP-Readiness auf und meldet danach
`not_executable`, bis ein erzwungener protokollkorrelierter Fall verdrahtet ist.
HTTP/2-Verfügbarkeit ist kein HTTP/3-Nachweis.

Aktuelle Evidence: Run `20260726T173136Z-fnd-host-remediation-20260726-7837c9e2`,
Artifact `evidence/fnd-host-0002-0003-0004-0006-current-revalidation.md`,
SHA-256 `81fdeceb0f34806cd781ee3adf0c8d57d6619d78549fef7e37313e90a4d545bf`.
Es erfolgten keine Client-Installation, NGINX-Runtime, Produktänderung oder
Delivery-Aktion. Der aktuelle Nutzer schließt HTTP/3 aus dem aktuellen lokalen
Testumfang aus; dies ist kein Pass und kein technischer Abschluss. Dieses
vollständige Tripel wiederherstellen und einen HTTP/3-fähigen,
protokollkorrelierten H3-Allow-Control vor jedem H3-, Produktions-,
Veröffentlichungs- oder Release-Claim ausführen.

## Aktuelle nutzergerichtete Archiv- und Scope-Disposition — 2026-07-26

Der aktuelle Nutzer wählte einen lokalen Testumfang, in dem HTTP/3 Zukunfts-
arbeit statt einer aktuellen Akzeptanzdimension ist. Daher ist dieser Record
für diesen Scope `not_applicable` und wird verlustfrei archiviert; er ist weder
technisch geschlossen noch über HTTP/3 bewiesen.

Aktuelle Entscheidungs-Evidence: Run
`20260726T180544Z-fnd-host-archive-20260726-8b20e52d`, Artifact
`evidence/fnd-host-user-directed-archive-scope-disposition.md`, SHA-256
`50f77adb2bfbe8dbea9341bb4012ed67acaa4bf43a540ef3268f7ef2121c666b`.
Es erfolgten keine H3-Client-Installation, H3-Runtime, Connector-Validierung,
Produktänderung oder Delivery-Aktion. Vor jeder künftigen H3- oder
Release-Nutzung wiederherstellen und neu validieren.

Archivpfad: `.codex/archive/findings/FND-HOST-0004/`.

## History / Historie

- `2026-07-17T10:43:59Z`: bootstrap_created — Created from retained evidence. No remediation, verification, closure, or risk acceptance was performed.
- `2026-07-17T13:12:00Z`: current_task_scope_recorded — `out_of_scope_for_current_task`
- `2026-07-26T17:34:26Z`: current_http3_capability_revalidation — curl 8.18.0
  bleibt HTTP2-fähig, hat aber keine HTTP3-Feature; kein alternativer lokaler
  Client löst auf, und der Parent-Harness bewahrt `not_executable`, statt ein
  Liveness-Ergebnis zu promoten. Das Finding ist `blocked_external_dependency`.
