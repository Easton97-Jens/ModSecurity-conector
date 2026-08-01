# FND-PARENT-0015 — Traefik-Pfad-UDS erlaubt Same-UID-Endpoint-Umleitung nach Bereitschaft

## Identität / Identity

| Feld / Field | Wert / Value |
| --- | --- |
| ID | `FND-PARENT-0015` |
| Titel / Title | `Traefik-Pfad-UDS erlaubt Same-UID-Endpoint-Umleitung nach Bereitschaft` |
| Kategorie / Category | `security_candidate` |
| Repository / Repository | `parent` |
| Ownership / Ownership | `parent` |
| Priorität / Priority | `P1` |
| Schweregrad / Severity | `medium` |
| Konfidenz / Confidence | `probable` |
| Status | `blocked` |
| Machbarkeitsstatus / Feasibility status | `blocked_missing_evidence` |
| Release-Blocker / Release blocker | `true` |
| Security-Relevanz / Security relevance | `true` |

## Zusammenfassung / Summary

Der C-Listener beweist Pfad-Identity nur bis zu seiner initialen Bereitschafts-
Capture. Die Traefik-Middleware öffnet für jede Transaktion eine neue Pfad-UDS-
Verbindung ohne Peer-Identity-Prüfung. Ein bösartiger Same-UID-Prozess, der
`engine.sock` nach Bereitschaft neu bindet, kann spätere Middleware-Traffic zu
einem Fake-Endpoint umleiten.

## Beobachtetes Verhalten / Observed behavior

Der Runner wartet nur darauf, dass ein Socket-Pfad existiert, und startet dann
Traefik mit diesem Pfad. `unixSocketEngine.Open()` nutzt
`net.Dialer.DialContext("unix", socketPath)` für jede Transaktion. Ein
protokollgültiges RESULT mit Action allow wird akzeptiert und zu
`allowDecision()` abgebildet. Weder Runner noch Client binden diese Verbindung
an die originale C-Listener-Identity.

## Erwartetes Verhalten / Expected behavior

Die C-Selbstprobe vor Capture darf nur behaupten, dass ein Ersatz in ihrem
begrenzten Startup-Fenster geschlossen scheitert. Strikte Live-Client-zu-Engine-
Identity erfordert eine verifizierte Client-Peer-Identity- oder Descriptor- /
Abstract-Socket-Grenze; Pfadauswahl und `0700`-Rechte isolieren keine
bösartigen Same-UID-Prozesse.

## Auswirkung / Impact

Unter der Same-UID-Änderungsvoraussetzung kann ein Fake-Listener für neu
geöffnete Transaktionen ein gültiges Allow-Result zurückgeben, den beabsichtigten
ModSecurity-Entscheidungspfad umgehen und über die Verbindung gesendete Daten
erhalten. Deployment-spezifische Ausnutzbarkeit und echte Host-Reproduktion
sind nicht belegt; dies bleibt medium/probable statt High oder confirmed.

## Betroffene Dateien und Symbole / Affected files and symbols

### Dateien / Files

- `connectors/traefik/src/traefik_engine_service.c`
- `connectors/traefik/scripts/runtime_native_smoke.py`
- `connectors/traefik/native_middleware/engine_uds.go`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`

### Symbole / Symbols

- `traefik_engine_capture_bound_socket_identity`
- `wait_for_socket`
- `unixSocketEngine.Open`
- `safeUnixSocketPath`
- `udsResult.decision`

## Voraussetzungen / Preconditions

- Ein bösartiger Prozess teilt die effektive Service-UID und kann das private
  UDS-Kindverzeichnis verändern.
- Er entfernt live `engine.sock` nach C-Readiness-Capture und bindet einen
  Ersatz vor Öffnen einer späteren Middleware-Transaktion.
- Der Ersatz liefert ein protokollgültiges Allow-Result.

## Reproduktion / Reproduction

- C-Readiness-Capture und das Fehlen späterer Pfadüberwachung verfolgen.
- `wait_for_socket()` verfolgen: Die Funktion akzeptiert jeden existierenden
  Socket-Pfad vor dem Traefik-Start.
- `unixSocketEngine.Open()` verfolgen: Die Funktion wählt den konfigurierten
  Pfad pro Transaktion erneut; `udsResult.decision()` bildet Action allow auf
  `allowDecision()` ab.

## Evidence / Evidence

- Run `20260717T114213Z-feasibility-runtime-remediation-838d9adc`,
  `logs/063-traefik-live-uds-redirection-static-review.log`, Source-to-Sink-
  Review, SHA-256
  `15d453ebcb8e013a3881f2897317ca5dca0f04c69a16920bda3e9137b7bb2406`, Exit
  `0`, beobachtet `2026-07-17T14:33:24Z`.
- `logs/062-same-uid-pathname-toctou-static-review.log`, SHA-256
  `2294d4ff41b1266a34a234da0db62072cadd51199efe37db979114ebcafc2dd2`, zeigt
  C-Capture- und Cleanup-Grenze.

## Grundursachenanalyse / Root-cause analysis

Vertrauen bewegt sich von C-Listener zu unabhängig wählendem Traefik-Client
über einen veränderbaren Pfad. Die C-seitige `SO_PEERCRED`-Selbstprobe fängt
einen Ersatz vor initialer Identity-Capture ab, aber es gibt keine spätere
Client-Peer-Validierung, Descriptor-Übergabe, Abstract-Socket-Mode oder
Live-Pfad-Identity-Bindung.

## Vorgeschlagene Remediation / Proposed remediation

Diese Grenze ohne verifiziertes Ende-zu-Ende-Design nicht als fixed behaupten.
Künftige Kandidaten sind Linux-only Abstract-AF_UNIX-Support, clientseitige
`SO_PEERCRED`-Validierung gegen sicher verwaltete erwartete Engine-Identity
oder Descriptor-Handoff. Jeder benötigt kompatible Traefik/Yaegi/Runtime-
Verträge, Restart-Semantik und feindliche Same-UID-Validierung; keiner ist ein
aktueller verifizierter Fix.

## Akzeptanzkriterien / Acceptance criteria

- Eine gewählte Client-zu-Engine-Identity-Grenze ist mit feindlichem Same-UID-
  Post-Readiness-Replacement validiert.
- Ein Fake-Endpoint kann weder eine neu geöffnete Middleware-Transaktion
  erhalten noch sie Allow als beabsichtigte Engine akzeptieren lassen.
- Bestehende Startup-Collision-, Path-Length-, YAML-Quoting-, Allow-, Blocking-,
  Shutdown- und Cleanup-Refusal-Controls bleiben abgedeckt.

## Validierungsplan / Validation plan

- Einen echten nativen Traefik/Yaegi-Host-Test mit deterministischem
  Post-Readiness-Replacement-Listener und Blocking-Request ausführen.
- Engine-Restart-/PID-Reuse-Semantik für jeden Peer-Identity-Ansatz testen.
- Linux-spezifischen oder portablen Fallback validieren, ohne Unsupported-
  Platform-Fail-Closed-Verhalten abzuschwächen.

## Regressionstests / Regression tests

- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/build/test-engine-service-runtime.sh`
- Ein künftiger echter Host-Post-Readiness-Replacement-Test.

## Legitime Kontrolltests / Legitimate control tests

- Fokussierte C-Engine-Protocol-/Lifecycle- und Python-Runner-Contracts
  bestanden für die engeren Pre-Capture-Hardening-Controls.

## Abhängigkeiten / Dependencies

- Ein verifiziertes Ende-zu-Ende-Traefik-Client-/Engine-Identity-Bound-Design
  und kompatible Host-Runtime-Evidence.

## Blocker / Blockers

- Keine aktuelle Client-Peer-Identity-Validierung, Descriptor-Übergabe oder
  unterstützter Abstract-AF_UNIX-Config-Vertrag.
- Keine echte native Traefik/Yaegi-Host-Runtime zur Validierung einer
  architektonischen Minderung.

## Verwandte Findings / Related findings

- `FND-FRAMEWORK-0008`
- `FND-PARENT-0013`
- `FND-PARENT-0014`

## Restrisiko / Residual risk

Aktueller Pfad und `0700`-Allokation mindern UID-übergreifende Kollisionen,
aber keinen feindlichen Same-UID-Endpoint-Rebind nach Bereitschaft. Es liegt
keine Risikoakzeptanz vor.

## Historie / History

- `2026-07-17T14:33:24Z`: `current_task_security_boundary_identified` —
  unabhängiges Source-to-Sink-Review unterschied Post-Readiness-Client-Redial
  und Allow-Result-Akzeptanz vom finalen Cleanup. Der Pfad hat bedingte
  Integrity-/Confidentiality-Auswirkung, aber keine aktuelle Ende-zu-Ende-
  Identity-Bound-Minderung oder Host-Reproduktion.
