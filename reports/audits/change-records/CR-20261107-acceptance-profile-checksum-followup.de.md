# Change Record: CR-20261107-acceptance-profile-checksum-followup

**Sprache:** [English](CR-20261107-acceptance-profile-checksum-followup.md) | Deutsch



## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261107-acceptance-profile-checksum-followup |
| Datum (UTC) | 2026-11-07 |
| Basis-Revision | `f89da27a293ef044e59a9582e9c814f4dabe1433` |

## Motivation und Problemstellung

Die verbleibenden Profil- und Abhängigkeitslücken der Vorbereitung schließen; die bereits behobenen NGINX-/Apache-/HTX-/SPOP-/ext_proc-Regressionen und 100 Standardfälle erhalten. Parent Draft PR #445 und Framework Draft PR #169 ohne Merge fortführen.

## Akzeptanzkriterien

Vollständige Envoy-ext_authz- und Traefik-ForwardAuth-Pfade mit Response-Companion sowie Traefik native unter TLS/H2 mit Safe/Strict unabhängig ausführen. Phasen-/Regel-/Request-/Transaktions-/Antwortzuordnung, aktive Peer-Isolation, Folgezugriff und natives Cleanup verlangen. Wiederholung am finalen Commitpaar und aktuelle verpflichtende gehostete Prüfungen entscheiden die Bereitschaft.

## Implementierungsentscheidung und Begründung

Eine explizit zugelassene Composite-Late-Action-Policy mit Safe als Vorgabe ergänzen. Strict protokolliert eine Abbruchanforderung getrennt vom tatsächlichen Downstream-Reset. Typisierte beobachtete Companion-Transportbeendigung schließt unvollständige native Transaktionen ohne erfundenes EOS oder Zuordnung zu einem unbekannten Endpunkt. Retained-Lebenszyklusereignisse an einen begrenzten Methoden-/URI-SHA-256 binden. Traefik native erhält phase4Mode Safe(Vorgabe)/Strict und erhält ein abgeschlossenes P2-Deny, wenn der nachfolgende Proxy danach http.ErrAbortHandler auslöst. Andere Panics und unvollständige Streams werden weitergereicht. Akzeptierte Composite-Responsechunks flushen, damit kleine Antworten progressiv bleiben. Phasenbesitzmasken der vollständigen logischen Profile bleiben unverändert; nur ihre nun implementierten Strict-Aktionszulassungsflags ändern sich.

Die aktuelle gehostete Advisory-Analyse meldete außerdem die Komplexität von parseResult in der Composite-Middleware. Das bestehende Prädikat für Terminal-Flags wird extrahiert, ohne die zugelassenen Opcode-/Flag-/Entscheidungs-/Status-/Wertkombinationen zu ändern; die vollständige vorhandene Protokoll-Regressionssuite bleibt maßgeblich.

## Geänderte Dateien

Envoy-Composite-Service/-Coordinator/-Transport und Common-Backend-Bridge; Traefik-Composite- und native Middleware; exakte Profilregistryflags; profilbezogene Capability-Begründungen; native Konfigurationsvorlagen und erzeugte Referenzen; ausgewählter Framework-Gitlink, Lock und 22 Workflow-Projektionen; dieser gepaarte Record. Adapter, Tests, unveränderlicher Apache-Metadatenabruf und natives Compilerinventar gehören zum Framework.

## Ausgeführte Befehle

Befehle verwenden RTK und explizite Quellwurzeln/Revisionen. Vorläufige tatsächliche Hostdiagnosen führten alle 24 neuen H2-IDs aus. Die nativen Traefik-Go-Tests führten 89 Top-Level-Tests / 195 eindeutige Blattszenarien ohne Skip aus; 13 Leserkontrollen und go vet bestanden. Finales Paar, betroffene Unit-Vereinigung, native Generatoren/Archiv/Pins, vollständige Policyvererbung und aktuelle gehostete CI-Nachweise stehen im externen Bericht; vorläufige Diagnosen qualifizieren das gelieferte Paar nicht.

## Security-Auswirkung

TLS-/Hostprüfung, private UDS-Eigentümerschaft, begrenzte Metadaten, Trennung von Engine/Host/Wire, exakte Quell-/Build-/Artefaktzulassung und Fehlerdiagnostik erhalten. Unbekannte Schließursachen bleiben zurückgewiesen. Keine Authentifizierung, Validierung, Scannerabdeckung, Compilerwarnung, Branchregel oder Quality Gate wird abgeschwächt. Das gemeinsame Common-Backend behält seine tatsächliche Identität getrennt von der logischen Host-/Handoff-Identität.

## Runtime-Evidence

Jeder vollständige logische Pfad führt seinen tatsächlichen Host und Response-Companion aus. Ein reiner Framework-Testobserver aktiviert native Traefik-Cleanupmetadaten; Wire- und native Access-Records belegen die physische Verbindung unabhängig. Frische Preflights im tatsächlichen Launcher und Quellzulassung vor/nach dem Lauf sind erforderlich. Vollständige SHAs, Nachweis der unveränderlichen Abhängigkeitsquelle, Fall-IDs, Fehler, Cleanup und Integritätsbelege bleiben extern.

## Bekannte Einschränkungen

Reine ungepaarte Autorisierungsdienste bleiben request-only. Leere SPOP-Bodyrahmung und aktuelle lighttpd-H1-Anwendbarkeit bleiben dokumentiert. Kein Geschwisterintegrationsmodell übernimmt ein anderes Profilergebnis. Die Gesamtabnahme ist ein getrennter Schritt.

## Verbleibende Risiken

Der vorhandene Sonar-SSH-Receiver weist Issue-POST-Transitionen trotz angebotener Servertransitionen zurück. Die 23 bisherigen Vorkommen wurden unabhängig neu bewertet; ohne gespeicherten Status-Readback wird kein Serverabschluss behauptet. Bestehende C++20-/C++23-Advisoryfehler und 84 Legacyinventarbefunde bleiben getrennt. Tatsächliche finale gehostete Sonar- und Apache-CRS/Aggregate-Ergebnisse sind erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Die umfassende Gesamtabnahme bleibt NOT_RUN. Kein lokaler Sonar-Scanner oder Setup, keine MRTS-Ausführung oder Änderung, kein Merge oder administrativer Eingriff erfolgt.

## Finaler Diff- und Review-Status

Normale Folgecommits und den nativen Framework-Publisher verwenden. Beide bestehenden Draft-PR-Branches, historische Nachweise und fremde Änderungen im ursprünglichen Arbeitsbereich erhalten. Finaler begrenzter Diff, erzeugte Dateien, exakte Pins und abgeschlossene aktuelle Head-Prüfungen werden im externen Bericht abgeglichen; dieser Record erklärt keine unabhängige Bereitschaft.
