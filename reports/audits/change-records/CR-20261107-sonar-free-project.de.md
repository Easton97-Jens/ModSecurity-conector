# CR-20261107-sonar-free-project

**Sprache:** [English](CR-20261107-sonar-free-project.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261107-sonar-free-project |
| Datum (UTC) | 2026-11-07 |
| Basis-Revision | a5f697c35acb5386d2037f91dfed10ad4b469cd9 |

## Motivation und Problemstellung

Die installierte globale Sonar-Integration führt bereits ausschließlich automatische Secrets-Prüfungen aus. Parent-Anweisungen erlaubten noch MCP und verlangten RTK pauschal auch für installierte Hooks; der ausdrückliche Free-/Datei-vor-Lesen-Vertrag fehlte. Bestehende Richtlinie und Entwicklungsanleitung aktualisieren, ohne die abgenommene globale Installation zu verändern.

## Akzeptanzkriterien

Bestehende AGENTS und geroutete Policy verlangen konsistent Secrets vor Lesezugriffen/Inhaltssuchen, stoppen bei Funden/Fehlern, erlauben Entwicklung nach sauberem Secrets-Scan, verbieten automatische Sammel-/Bezahlanalysen und lassen MCP deaktiviert. Explizites projektbezogenes Cloud-Binding, revisionsgebundene Evidence, vollständige bestehende CI-Scanner-Analysen und unabhängige PR-Gates am aktuellen Head erhalten. Nur Task-Änderungen auf codex/-Branch als Draft-PR gegen master liefern; niemals mergen.

## Implementierungsentscheidung und Begründung

Eine kanonische Sonar-Policy behalten und die bestehende RTK-Policy um die enge Ausnahme für installierte Codex-Hooks ergänzen. Unabhängigen Projekt-RTK-Hook erhalten. Nur geänderte Parent-Policy-Digests aktualisieren. Gleichwertige aktuelle EN/DE-Anleitung vor eindeutig historische Analyseaufzeichnungen stellen; obsolete Parent-lokale Scope-/Testbeispiele entfernen. Änderungen an Runtime, Scanner-Workflows, Analyseumfang oder Gates waren nicht erforderlich. Der früher dokumentierte Change-Record-Generator fehlt im aktuellen Checkout; das Paar verwendet direkt das aktuelle Framework-eigene Parent-Checker-Schema.

## Geänderte Dateien

- `AGENTS.md`
- `.codex/context/command-execution-policy.md`
- `.codex/context/index.md`
- `.codex/context/security/analysis-services-policy.md`
- `.codex/context/sonarqube-policy.md`
- `.codex/inheritance-manifest.toml`
- `docs/sonarqube-analysis.md`
- `docs/sonarqube-analysis.de.md`
- `reports/audits/change-records/CR-20261107-sonar-free-project.md`
- `reports/audits/change-records/CR-20261107-sonar-free-project.de.md`

## Ausgeführte Befehle

| Befehl / Verfahren | Ergebnis |
| --- | --- |
| `rtk bypass /usr/local/bin/sonar-with-env analyze secrets --stdin` | Abgegrenzte Scans für Anweisungen, geplante/geänderte Dateien und installierte Validierungseingaben mit Exit 0. Parent-Markdown/TOML/Python vor dem Lesen: 735 Dateien, 20 begrenzte Batches, alle Exit 0. Übrige aktive Konfiguration/Skripte: 129 Dateien, 683652 Bytes, Exit 0 vor Inhaltssuche. |
| `rtk bypass python3 .codex/bin/validate-codex-inheritance.py --check --repository parent` | Exit 0; Parent-Katalog und Digests konsistent. |
| `rtk bypass python3 .codex/bin/validate-v32-structure.py` | Exit 0; V3.2-Struktur OK. |
| `rtk make check-bilingual-docs PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` | Exit 0; bilinguale Dokumentation OK. |
| `rtk make check-doc-links PYTHON=/var/tmp/codex/ModSecurity-test-Framework/venv/bin/python` | Exit 0; Repository-Pfadreferenzen PASS und Dokumentationslinks OK. |
| `rtk bypass git diff --check` | Exit 0. |
| `rtk bypass /usr/local/bin/sonar-with-env quality-gate status -p Easton97-Jens_ModSecurity-conector` | Abfrage mit Exit 0; daraus kein Gate-Erfolg des aktuellen Task-Heads abgeleitet. |
| `rtk bypass /usr/local/bin/sonar-with-env api get '/api/measures/component?component=Easton97-Jens_ModSecurity-conector&metricKeys=coverage,duplicated_lines_density'` | Abfrage mit Exit 0; verfügbare Duplikationsmetrik zurückgegeben, Coverage ausgelassen. Nur letzter Cloud-Analysestand. |

Anfängliche Dokumentationschecks mit explizitem ursprünglichem Framework-Checkout endeten mit Exit 2, da dem isolierten Parent-Worktree die materialisierten Submodul-Linkziele fehlten. Ein separater detached Framework-Worktree am unveränderten gepinnten Commit `62b411e073551ef0fef22ab3d372e2489f2ae168` stellte diese Ziele bereit; beide Checks bestanden danach. Framework-/MRTS-Sources und Gitlinks bleiben unverändert.

## Security-Auswirkung

Secrets- und Fehlerbehandlung bleiben fail-closed; Rohbefunde und Zugangsdaten werden unterdrückt. Keine Regeln, Ausschlüsse, Anmeldung, Vertrauenseinstellungen, Privilegien oder Quality Gates wurden abgeschwächt. Installierte globale Hooks und ihre direkten Starter-/Scannerpfade wurden nicht verändert. CI behält ihren bisherigen Scanner- und Authentifizierungskontext.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht. Die bereitgestellte globale Automationsabnahme vom 2026-11-07 ist frühere Evidence: Beide Scanner-Kindprozesse endeten mit 0; Handler-Prozess-Exits wurden nicht aufgezeichnet. Manuelle Scans und erfolgreiche Abfragen dieses Tasks sind keine neue automatische Hook-Abnahme oder neue vollständige Qualitätsanalyse.

## Bekannte Einschränkungen

Ein ergänzender Konfigurationsscan einschließlich Reports mit etwa 19 MB endete mit Exit 1 und wurde nicht als Erfolg behandelt. Lesezugriffe/Änderungen stoppten; die relevante aktive Auswahl wurde auf 129 Dateien begrenzt und vor der Suche erfolgreich erneut geprüft. Historische JSON-Reports lagen außerhalb dieser Inventur und wurden weder geöffnet noch als erfolgreich geprüft behauptet. Hosted-Checks des aktuellen Heads und gegebenenfalls dessen Cloud-Gate sind am PR abzulesen; frühere Cloud-Ergebnisse qualifizieren diese Änderung nicht.

## Verbleibende Risiken

Die Dokumentations-/Control-Plane-Änderung erzeugt kein neues Connector-Runtime-Risiko. Separate Repositorys behalten ihre bestehenden Policy-Pins; dieser reine Parent-Task pinnt keine Child-Manifeste neu und behauptet keinen repositoryübergreifenden Vererbungserfolg. Geänderte AGENTS.md und lokale .sonar-config.json des ursprünglichen Checkouts bleiben erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Connector-Builds/Runtime-Matrizen und eine neue automatische Hook-Ereignisabnahme wurden nicht ausgeführt, da die Änderung ausschließlich Anweisungen und Dokumentation betrifft. Bezahl-/Sammelanalysen und MCP wurden nicht aufgerufen. Keine Framework-/MRTS-Sourceänderungen oder Delivery. Externer CI-/Gate-Status des aktuellen Heads wird nach Push am Draft-PR berichtet und hier nicht abgeleitet.

## Finaler Diff- und Review-Status

Der abgegrenzte Anweisungs-/Anleitungsdiff wurde vom Hauptagenten und unabhängig schreibgeschützt geprüft; kein Blocker wurde gefunden. Bestehende CI-Workflows, Scanner-Projekteigenschaften und Hookkonfiguration bleiben bytegenau unverändert. Exakte Delivery-SHA, PR-Link und Prüfgrenzen des aktuellen Heads stehen in PR-Metadaten und Task-Abschluss.
