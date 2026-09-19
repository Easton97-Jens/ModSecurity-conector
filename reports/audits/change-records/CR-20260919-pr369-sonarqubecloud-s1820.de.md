# Change Record: PR-#369-SonarQube-Cloud-S1820-Sidecar-State-Remediation

**Sprache:** [English](CR-20260919-pr369-sonarqubecloud-s1820.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-pr369-sonarqubecloud-s1820 |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Vorgänger-PR-#369-Head | `c8b5faf2491ed2e4489ad8298a1083557bfba349` |
| Finding | `FND-SONAR-0089`; Sonar-Issue `AaCrebhgrY5Yi_GLZMw7` / `c:S1820` |
| Benutzerautorisierung | “das muss null sein und gib mir eine übersicht welche findings damit behoben sind” |
| Delivery-Status | Dieser Record begleitet einen scoped normalen Follow-up im bestehenden Parent-Draft-PR #369. Kein Merge, Auto-Merge, direkter `master`-Schreibvorgang, Framework-/MRTS-/Gitlink-Change, Control-Weakening oder Branch-Löschung ist autorisiert; die Exact-Successor-Head-Verifikation folgt nach einem normalen Push. |

## Motivation und Problemstellung

Der authentifizierte SonarQube-Cloud-Readback für PR #369 meldete einen offenen
MAJOR `CODE_SMELL`: `sidecar_exchange_state` hatte 24 direkte Felder, während
`c:S1820` höchstens 20 erlaubt. Obwohl das Quality Gate `OK` war, war der
angefragte PR-scoped Zero-Open-Issue-Zustand nicht erreicht.

## Akzeptanzkriterien

- `sidecar_exchange_state` hat höchstens 20 direkte Felder, ohne sein
  Endpunkt-, Transaktions-, Error-, Commit- oder Phasenreihenfolgeverhalten zu
  ändern.
- Der C17/Werror-Source-Contract und legitime Loopback-Endpunkt-/Allow-
  Controls bestehen.
- Die Analyse des exakten PR-#369-Nachfolgers hat null `OPEN`/`CONFIRMED`
  Issues und keinen `AaCrebhgrY5Yi_GLZMw7`-Record.
- Keine `NOSONAR`-, Exclusion-, Acceptance-, Scanner-, Workflow-, Regel- oder
  Quality-Gate-Änderung wird vorgenommen.

## Implementierungsentscheidung und Begründung

Die Reparatur führt `sidecar_request_endpoints` für die vier Kernel-abgeleiteten
Endpunktwerte und `sidecar_exchange_dependencies` für die unveränderlichen
`options`- und `runtime`-Referenzen ein. `sidecar_exchange_state` hat jetzt
exakt 20 direkte Felder. Nur Member-Zugriffspfade ändern sich; Initialisierung
und alle Parser-, Decision-, Error-, Response-Commit-, Late-Intervention- und
Fail-Closed-Branches bleiben in der bisherigen Reihenfolge.

## Security-Auswirkung

Dies ist eine Maintainability-Reparatur und keine Sicherheitslücke. Die
relevante Bewahrungsinvariante lautet, dass `getpeername()` und
`getsockname()` vor dem Common-Runtime-Transaktionsbeginn validierte IPv4-
Endpunktdaten liefern. Die Änderung fügt weder einen anfragekontrollierten
Fallback hinzu noch ändert sie Socket-, Konfigurations-, Parser- oder
Autorisierungs-Verhalten.

## Geänderte Dateien

- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `reports/audits/change-records/CR-20260919-pr369-sonarqubecloud-s1820.md`
- `reports/audits/change-records/CR-20260919-pr369-sonarqubecloud-s1820.de.md`

Das bestehende Change-Record-Index-Paar war bereits durch unabhängige Arbeit
verändert und wurde von diesem Follow-up absichtlich nicht geändert oder
gestaged.

## Ausgeführte Befehle

| Befehl oder Check | Ergebnis | Beobachtetes Ergebnis |
| --- | --- | --- |
| RTK-proxied `/usr/local/bin/sonar-with-env`-PR-#369-Issue- und Quality-Gate-Readback | bestanden | Ein `OPEN`/`CONFIRMED`-Issue, `AaCrebhgrY5Yi_GLZMw7` / `c:S1820`, wurde identifiziert; Quality Gate `OK` machte das Issue nicht null. |
| Direkte `sidecar_exchange_state`-Feldzählung | bestanden | Exakt `20` direkte Felder nach dem Refactor. |
| `StockSidecarSourceContractTest` | bestanden | 17 Tests einschließlich C17/Werror-Source-Harnesses. |
| C17/Werror-Sidecar-Build mit `CC=cc` | bestanden | External-Root-Build abgeschlossen. |
| C17/Werror-Sidecar-Build mit `CC=clang` | bestanden | Unabhängiger External-Root-Build abgeschlossen. |
| Vollständiger `self-test-lighttpd-stock-sidecar` | fehlgeschlagen | 33/34 Tests bestanden; der Immediate-Client-Reset-Event-Fall beobachtete sein Event nicht. |
| Derselbe Immediate-Reset-Fall aus unveränderter `HEAD`-Source kompiliert | fehlgeschlagen | Identisches Empty-Event-Ergebnis, daher nicht diesem Refactor zugeschrieben. |
| `git diff --check` für den Sidecar-Kandidaten | bestanden | Keine Whitespace-Fehler. |

## Runtime-Evidence

Der Allow-Pfad der vollständigen Loopback-Suite und
`test_loopback_endpoint_metadata_reaches_common_runtime` bestanden mit dem
Kandidaten-Binary. Dies ist begrenzte Loopback-Evidenz für die Bewahrung der
Kernel-abgeleiteten Endpunktinvariante; es ist keine Real-Stock-lighttpd-
Backend- oder Hosted-PR-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

Das reale Stock-lighttpd-Backend, die vollständige Connector-Matrix, Hosted-
Checks, frische Reviews und die SonarQube-Cloud-Analyse des exakten Nachfolgers
sind noch nicht ausgeführt, weil der normale Nachfolger noch nicht ausgeliefert
ist. Für sie wird kein Ergebnis behauptet.

## Bekannte Einschränkungen

Das vollständige Sidecar-Modul bleibt bei 33/34, weil sein Immediate-Client-
Reset-Event-Fall identisch auf unverändertem `HEAD` fehlschlägt. Diese bekannte
getrennte Runtime-Einschränkung bleibt `FND-PARENT-1091`; sie wird durch
`FND-SONAR-0089` weder geschwächt, akzeptiert noch als gelöst behandelt.

## Verbleibende Risiken

Der lokale Kandidat hat noch keinen SonarQube-Cloud-Readback für den exakten
Nachfolger-Head erhalten; daher ist `FND-SONAR-0089` `fixed`, nicht `verified`
oder `closed`. Das erforderliche Null-Ergebnis muss ohne Änderung der Sonar-
Controls belegt werden.

## Finaler Diff- und Review-Status

Der geprüfte Produktdelta ist datenrein und auf den privaten Sidecar-State
begrenzt. Dieses Follow-up staged nur die drei oben aufgeführten Dateien. Das
lokale `.codex`-Finding und sein payload-sicherer Evidence-Record sind
absichtlich nicht versioniert und ersetzen diesen Change Record nicht. Die
Exact-Successor-Head-Verifikation bleibt ausstehend.
