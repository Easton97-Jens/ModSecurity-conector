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
| 1 | Redirect verliert Quell-Audit; jedes Ziel prüft neu | Request-eigene, konfigurationsabhängige Wiederverwendung; natives Audit jeder Transaktion einmal vor Cleanup | Kompilierte echte Common-/Audit-Tests und native H1-Besitzerzahlen bestanden |
| 2 | Erhaltener Block-Header blockiert Fehlerseite erneut | Konfiguriertes WAF-Fehlerseitenziel und Status erfassen und abgleichen | Natives H1 mit eigener403/Header/ursprünglichem nativen403-Audit und allgemeinem Fehlerseiten-Negativfall bestanden |
| 3 | Optionaler Safe-Eventfehler setzt Transaktions-/Connectionfehler | Optionale Eventfehler diagnostizieren; echte Fehler und Strict-Abbruch bewahren | Kompilierte kontrollierte Eventfehler, echte Metadaten-Allokations- und EOS-Fehlerkontrollen bestanden; kein Host-Sink-Fehlernachweis behauptet |
| 4 | size_t-Beobachtungsüberlauf weist auf 32-Bit >4 GiB ab | Sättigende uint64-Zähler bis Common/Events; begrenztes Dateistreaming | Kompilierte UINT32-/UINT64- und modellierte >4-GiB-Dateiprüfungen |
| 5 | Geleerte ursprüngliche Datenlinks erreichen Writer | Nutzlast verbrauchen, eigene Steuerpuffer weiterreichen, Abschluss einmal | 9 kompilierte Kontrollen und nativer Handler mit zwei Daten- plus NULL-Callback bestanden; keine Writerfehler/Body-Lecks |
| 6 | Freie Nutzlast liefert Regel-ID | Vollständiger geordneter/escapter Engine-Datensatz mit Mehrdeutigkeitsprüfung | 28 Szenarien einschließlich echter Engine 3.0.14; alter Parser zeigt drei Fehler |
| 7 | Natives Response-Reject erfordert genaue englische Meldung | Validierter Append-Zustand und disruptive403 ohne Regel-ID | Echter kompilierter Collector-/Append-/P4-Pfad:18 Reject- und18 ProcessPartial-Varianten zu Modus/Commit/Prosa bestanden |
| 8 | Modusduplikat im selben Kontext akzeptiert | Duplikat-Sentinel; gemeinsame Modusvalidierung/Vererbung bewahrt | Kompilierter Setter/Merge und echte nginx -t-Fälle zu Duplikat/off/strict im Kind bestanden |
| 9 | Frühere Datei-/JSON-Verbesserungen vorhanden | Gleichen Append-Pfad, strukturierte Events und Escaping bewahren | Common-Helper-Smoke und betroffene kompilierte Pfade bestanden; verbesserte Helfer bewahrt |

Die explizite Lifecycle-Operation supersede_response beendet nach Response-Konfigurationsübergabe ausschließlich gesunde abgeschlossene P1/P2-Besitzer; Phasenmasken bleiben unverändert und P3/P4 werden nicht erfunden.

Der C-Callback liefert Text. Neuere C-Listen geloggter IDs ordnen diese keiner verursachenden disruptiven Regel zu; das erste/letzte Element zu wählen wäre unsicher. Der Parser validiert daher den vollständigen unterstützten nativen Datensatz und lässt mehrdeutige IDs unbekannt. Native NGINX-Entscheidungen mit notwendiger Korrelation verwenden den geschlossenen Fehlerpfad.

## Geänderte Dateien

`connectors/nginx/src/ngx_http_modsecurity_{access,body_filter,common,log,module}.*`, `ngx_http_modsecurity_phase4_observation.h`, `ngx_http_modsecurity_response_body_limit.h`; Common `rule_id.c/.h`, `transaction_contract.h`, `transaction_state.c`; Connector-/Common-README-Paare, Connector-Guide-Paar und dieser Record. Regressionstests liegen im getrennt freigegebenen Framework-Branch `test/nginx-fzipi-review`; Parent-Gitlink und MRTS bleiben unverändert.

## Ausgeführte Befehle

`rtk make check-nginx-c17` bestand mit echten konfigurierten NGINX1.31.8-Headern, passendem libModSecurity3.0.17-SDK und C17/Wall/Wextra/Werror. `rtk make build-nginx` bestand den nativen dynamischen Komponentenbuild. Ein frischer statischer NGINX1.31.8 mit ausschließlich im Test verwendetem Addon bestand ebenfalls mit8 logischen CPUs und gepinntem Archiv-SHA256 `0652b760b3b772d2ec17b47c2fc15d9a95e6fe35cd5b877eadc1a62d9bc75af1`.

Die abschließende explizite Framework-Unittest-Auswahl bestand75 Methoden aus10 betroffenen Modulen am Produktstand `b478aeb02c26bf6e44627f43b49678f1abc3081b` (`focused-final.json`). Parserprüfungen umfassen28 Szenarien und echte Engine3.0.14-Meldungen. Vier zusätzliche vorhandene Request-Native-Testmethoden und zwei direkte Szenarien des vorhandenen Helpers bestanden: Speicher- und Tempdatei-Append0 mit ProcessPartial erreicht EOS; kurze/fehlgeschlagene/veränderte Dateizustände bleiben terminal. Das aktualisierte Common-Adoption-Gate bestand und seine11 Mutationsmethoden wiesen28 negative Varianten ohne deaktivierte Prüfungen ab.

Altcode-Negativkontrollen reproduzierten Parser-, Zähler-, Safe-Sink-, Audit-/Kontext- und Buffer-Verwerfungsfehler; sie kompilierten erfolgreich vor den beabsichtigten Laufzeit-Assertions.

`rtk make check-common-helpers ON_DEMAND_TESTS=1`, `rtk make check-bilingual-docs check-doc-links`, ausgewählte kanonische Secrets-Scans und abschließende Whitespace-Prüfungen bestanden. Der anfängliche Doku-Fehler im isolierten Worktree wurde durch rein lesende Materialisierung seiner exakt gepinnten Framework-Linkziele behoben. Zwei abschließende Leerzeilen wurden korrigiert. Ein erster Unittest-Befehl mit kurzer Revision scheiterte vor Ausführung an der Quellenzulassung; der korrigierte Lauf mit vollständigem SHA bestand.

Vollständige tatsächliche Argumentlisten/Umgebung und Belege liegen unter `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review`; `run-focused.py` wählt die10 Testmodule explizit. Native Ausführung: `rtk bypass env ... python .../run_nginx_fzipi_review.py --connector-root <Parent worktree> --expected-head b478aeb02c26bf6e44627f43b49678f1abc3081b --artifact-manifest <static-fixture-v2>/artifact-manifest.json --nginx-binary <static-fixture-v2>/nginx-1.31.8/objs/nginx --output-root <run>/native-host-v2` im geprüften eskalierten lokalen Kontext. Keine Sicherheitskontrollen oder Pflichtgates wurden deaktiviert.

## Security-Auswirkung

Keine allgemeine Fehlerseiten-/Redirect-Ausnahme. Unbekannte Metadaten werden nie zur Freigabe. Optionale späte Safe-Beobachtung bricht die Auslieferung nicht ab; natives Reject und echte Verarbeitungsfehler bleiben Fehler. Die neuen Event-Datensätze enthalten keine Body-Daten. Kein Sicherheitsgate, Compiler-Warning oder Prüfpfad wurde abgeschwächt.

## Runtime-Evidence

Natives H1 bestand9 Szenarien am Produktstand `b478aeb02c26bf6e44627f43b49678f1abc3081b`: Phase2-Headerblock→konfigurierte403-Seite mit erhaltenem Auslöser und genau einem ursprünglichen nativen403-Audit; gewöhnliches try_files→ein Audit; andere Zielregeln→zwei getrennt verantwortete Audits; deaktiviertes Ziel→ein Quell-Audit; gewöhnliche Host403-Fehlerseite→WAF blockiert weiterhin; ersetzte Antwort→zwei späte Body-Callbacks plus NULL, keine ausgelieferten Originalbytes/Empty-Writer-Diagnosen; Modusduplikat abgewiesen und geerbtes Safe mit off/strict im Kind akzeptiert.

Framework-Identitäts-/Zugriffsvorprüfungen bestanden im selben Kontext. Beobachtet wurden Master-UID/GID0 und Worker-UID/GID65534; private Ausgabe war dem Worker verweigert. Master mit Exit0 eingeholt, Prozessgruppe verschwunden und Listener geschlossen. Beleg `/var/tmp/codex/ModSecurity-conector/runs/20261114-fzipi-review/native-host-v2/private/result.json`, SHA256 `0364231b54ca098f69666f52777bb0162460b1b1f5ae39001789f0c92388738b`. Der erste native Kandidat zeigte einen leeren Writer-Aufruf; dieser Produktfehler und eine zu enge Relative-Location-Testannahme wurden korrigiert und danach frisch erfolgreich gebaut/ausgeführt. Native Audit-Evidenz stammt aus libModSecurity-JSON und wird nicht durch Event-JSONL ersetzt.

## Bekannte Einschränkungen

Textmetadaten mit mehrdeutigem Roh-Framing bleiben unbekannt; notwendige Regelkorrelation verwendet den geschlossenen Fehlerpfad. Sättigung erhält jenseits UINT64_MAX eine Untergrenze. Die32-Bit-Grenzen sind realistische kompilierte Typ-/Arithmetikmodelle, kein nativer32-Bit-Host-Build oder Multi-GiB-Download. Safe-Sink-Fehler und Reject-/ProcessPartial-Varianten zu Prosa/Modus/Commit sind kompilierte echte Produktschnittstellen und keine zusätzlichen Host-Fehlerkampagnen. Keine H2-/H3- oder Vollmatrix-Qualifikation wird behauptet.

## Verbleibende Risiken

Framework-Regressionen werden getrennt ausgeliefert; der Parent-Gitlink bleibt unverändert. Remote-CI/Sonar und PR-Review am aktuellen Head bleiben Auslieferungsprüfungen. Kein Merge oder Deployment ist autorisiert.

## Nicht ausgeführte Prüfungen mit Begründung

Keine vollständige Connector-/historische I12-Matrix, Produktionsbereitstellung, H2-/H3-Qualifikation oder Merge: außerhalb dieses gezielten Auftrags. Dieser Record behauptet keinen bestandenen Remote-CI-/Sonar-Stand am aktuellen Head; der PR enthält die laufenden Auslieferungsprüfungen.

## Finaler Diff- und Review-Status

Alle acht zutreffenden Korrekturen und Erhaltungspunkt9 besitzen Quell-, gezielte Test- und dokumentierte Nachweise. Befunde der unabhängigen Quellprüfung sind korrigiert; sechs unabhängige Nachprüfungen bestanden. Der danach im echten Lauf gefundene Empty-Writer-Fehler wurde behoben und der frische native Lauf bestand. Task-Quellcommits02ca6440/48c4a996/b478aeb0 liegen auf `fix/nginx-fzipi-review`; dieser Dokumentationsabgleich ändert keine weitere Produktquelle. Remote-Auslieferung muss am tatsächlichen Head zurückgelesen werden; kein Merge erfolgte.
