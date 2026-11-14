# Change Record: CR-20261114-nginx-fzipi-review

**Sprache:** [English](CR-20261114-nginx-fzipi-review.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261114-nginx-fzipi-review |
| Datum (UTC) | 2026-11-14 |
| Basis-Revision | `5672c5ff562495ddbc47a1932b1641e0073746f5` |

## Motivation und Problemstellung

Die noch zutreffenden Punkte aus fzipis Review von [Upstream-PR #377](https://github.com/owasp-modsecurity/ModSecurity-nginx/pull/377) korrigieren. Der aktuelle Remote-master entspricht der Vergleichsrevision. Request-Datei-ProcessPartial, strukturierte Events und JSON-Escaping bleiben erhalten.

## Akzeptanzkriterien

Natives Audit und ursprünglichen Blockstatus bewahren, konfigurierte WAF-Fehlerseite ohne allgemeine Redirect-Ausnahme ausliefern, späte Safe-Antworten bei optionalem Eventfehler weiterliefern, Strict/native Limits/technische Fehler bewahren, Beobachtungsüberlauflimits und ungültige leere Downstream-Puffer vermeiden, echte Regelmetadaten bestimmen, natives Reject ohne Prosa klassifizieren und Modusduplikate abweisen.

## Implementierungsentscheidung und Begründung

| Punkt | Bisheriges Verhalten | Änderung | Ausgeführter Nachweis / Grenze |
| --- | --- | --- | --- |
| 1 | Redirect verliert Quell-Audit; jedes Ziel prüft neu | Request-eigene, konfigurationsabhängige Wiederverwendung; natives Audit jeder Transaktion einmal vor Cleanup | Kompilierte Audit-/Kontexttests; nativer Host-Lauf steht noch aus |
| 2 | Erhaltener Block-Header blockiert Fehlerseite erneut | Konfiguriertes WAF-Fehlerseitenziel und Status erfassen und abgleichen | Kompilierte positive/negative Routingtests; native Auslieferung steht noch aus |
| 3 | Optionaler Safe-Eventfehler setzt Transaktions-/Connectionfehler | Optionale Eventfehler diagnostizieren; echte Fehler und Strict-Abbruch bewahren | Kompilierte Sink-Fehlerkontrollen; integrierter Abschlusslauf steht aus |
| 4 | size_t-Beobachtungsüberlauf weist auf 32-Bit >4 GiB ab | Sättigende uint64-Zähler bis Common/Events; begrenztes Dateistreaming | Kompilierte UINT32-/UINT64- und modellierte >4-GiB-Dateiprüfungen |
| 5 | Geleerte ursprüngliche Datenlinks erreichen Writer | Nutzlast verbrauchen, eigene Steuerpuffer weiterreichen, Abschluss einmal | Kompilierte Speicher-/Datei-/Subrequest-/NULL-/Wiedereintrittskontrollen; Host-Handler steht aus |
| 6 | Freie Nutzlast liefert Regel-ID | Vollständiger geordneter/escapter Engine-Datensatz mit Mehrdeutigkeitsprüfung | 28 Szenarien einschließlich echter Engine 3.0.14; alter Parser zeigt drei Fehler |
| 7 | Natives Response-Reject erfordert genaue englische Meldung | Validierter Append-Zustand und disruptive403 ohne Regel-ID | C17-Prädikat mit positiven/negativen Log-/Zustandsfällen |
| 8 | Modusduplikat im selben Kontext akzeptiert | Duplikat-Sentinel; gemeinsame Modusvalidierung/Vererbung bewahrt | Kompilierter Setter-/Merge-Test; natives nginx -t steht aus |
| 9 | Frühere Datei-/JSON-Verbesserungen vorhanden | Gleichen Append-Pfad, strukturierte Events und Escaping bewahren | Betroffene Pflichtprüfungen ausgewählt; Endergebnisse unten |

Die explizite Lifecycle-Operation supersede_response beendet nach Response-Konfigurationsübergabe ausschließlich gesunde abgeschlossene P1/P2-Besitzer; Phasenmasken bleiben unverändert und P3/P4 werden nicht erfunden.

Der C-Callback liefert Text. Neuere C-Listen geloggter IDs ordnen diese keiner verursachenden disruptiven Regel zu; das erste/letzte Element zu wählen wäre unsicher. Der Parser validiert daher den vollständigen unterstützten nativen Datensatz und lässt mehrdeutige IDs unbekannt. Native NGINX-Entscheidungen mit notwendiger Korrelation verwenden den geschlossenen Fehlerpfad.

## Geänderte Dateien

`connectors/nginx/src/ngx_http_modsecurity_{access,body_filter,common,log,module}.*`, `ngx_http_modsecurity_phase4_observation.h`, `ngx_http_modsecurity_response_body_limit.h`; Common `rule_id.c/.h`, `transaction_contract.h`, `transaction_state.c`; Connector-/Common-README-Paare, Connector-Guide-Paar und dieser Record. Regressionstests liegen im getrennt freigegebenen Framework-Branch `test/nginx-fzipi-review`; Parent-Gitlink und MRTS bleiben unverändert.

## Ausgeführte Befehle

`rtk make build-nginx FRAMEWORK_ROOT=<Framework task worktree> ...`: erster nativer Build bestanden, NGINX1.31.8 und passende gecachte libModSecurity3.0.17; spätere Quellkorrekturen benötigen frische Build-Verifikation. `rtk bypass env ... python -m unittest ...test_nginx_response_body_limit`: bestanden. Integrierte gezielte Tests bestanden52 Methoden; die echte native Collector-/P4-Kette bestand weitere14 Methoden und Intervention-Ownership-Prüfungen4. Die Parserabdeckung umfasst28 Szenarien und eine echte Engine3.0.14-Intervention. Vollständige native C17-Kompilierung, Common-Helper-Smoke und zweisprachige Dokumentations-/Linkprüfungen bestanden. Das alte native Limitprädikat wurde mit fehlendem Log erfolgreich kompiliert und reproduzierte Exit10; das korrigierte Prädikat besteht. Altcode-Kontrollen zu verworfenen Body-/Steuerketten, Parser, Zählern/Safe-Sink und Lifecycle reproduzierten die früheren Verhaltensfehler. Ausgewählte Secrets-Scans bestanden mit0 über `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin`. Vollständige Befehle und Belege unter `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review`.

## Security-Auswirkung

Keine allgemeine Fehlerseiten-/Redirect-Ausnahme. Unbekannte Metadaten werden nie zur Freigabe. Optionale späte Safe-Beobachtung bricht die Auslieferung nicht ab; natives Reject und echte Verarbeitungsfehler bleiben Fehler. Die neuen Event-Datensätze enthalten keine Body-Daten. Kein Sicherheitsgate, Compiler-Warning oder Prüfpfad wurde abgeschwächt.

## Runtime-Evidence

Der erste native Build ist abgeschlossen und belegt ausschließlich Kompilierung. Der gezielte Host-Beleg liegt noch nicht vor. Noch kein nativer Audit-/Fehlerseiten-/Streaming- oder H2-/H3-Laufzeiterfolg wird behauptet.

## Bekannte Einschränkungen

Textmetadaten mit mehrdeutigem Roh-Framing bleiben absichtlich unbekannt. Gesättigte Beobachtungen liefern eine Untergrenze und keinen exakten Wert jenseits UINT64_MAX. Integrierte Build-/Laufzeit-/Dokumentationsprüfungen laufen noch.

## Verbleibende Risiken

Gezieltes internes Routing und Writer-Verhalten benötigen noch den echten Host-Lauf. Neue Framework-Tests werden getrennt ausgeliefert und aktualisieren den Parent-Pin nicht automatisch.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connector-/historische I12-Matrix, Produktionsbereitstellung, H2-/H3-Qualifikation oder Merge: außerhalb dieses gezielten Auftrags. Aktuelle PR-CI-/Sonar-Ergebnisse existieren noch nicht.

## Finaler Diff- und Review-Status

Die unabhängige Quellprüfung fand Lücken bei EOS-Validierung, abgelöstem Transaktionsumfang und Event-Allokationsdiagnose; alle drei Quellkorrekturen sind umgesetzt. Vollständige native C17-Kompilierung mit Warnings-as-Errors, Common-Helper-Smoke, zweisprachige Dokumentations-/Linkprüfungen und Whitespace bestanden. Branch `fix/nginx-fzipi-review`; Quellcommit `02ca6440` liegt für native Validierung eines sauberen Checkouts vor. Noch kein Push/PR/Merge. Tatsächliche Runtime- und Auslieferungsfakten werden vor Auslieferung abgeglichen.
