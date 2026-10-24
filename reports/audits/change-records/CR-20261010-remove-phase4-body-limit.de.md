# Change Record: CR-20261010-remove-phase4-body-limit

**Sprache:** [English](CR-20261010-remove-phase4-body-limit.md) | Deutsch


## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-remove-phase4-body-limit |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `b4044d10682cb2881c218fe84cebe41e61b235c2` |

## Motivation und Problemstellung

Der Benutzer verlangt ausdrücklich die repositoryweite Entfernung von `modsecurity_phase4_body_limit`, einschließlich Apache und Common, vor Fortsetzung der bisherigen NGINX-Exact-Head-Arbeit. Der veraltete Kompatibilitätswert war bereits keine WAF-Inspection-Policy der Engine.

## Akzeptanzkriterien

Kein aktiver Parser, keine Registrierung, kein Konfigurationsfeld, kein unterstütztes Beispiel und kein generiertes Konfigurationsinventar enthält die entfernte Einstellung. Die Required-ID `invalid_size` bleibt bestehen und prüft ausdrücklich die echte Unknown-Directive-Ablehnung des früher gültigen Inputs `modsecurity_phase4_body_limit 1048576;`. Engine-Response-Limit-Cases und unabhängige Ressourcenschutzgrenzen bleiben unverändert.

## Implementierungsentscheidung und Begründung

Die öffentliche Direktive entfernen statt stillschweigend ignorieren. `SecResponseBodyLimit` und `SecResponseBodyLimitAction` bleiben Engine-Policy. Unabhängige Request-/Response-Speicherdefaults von 1048576 Bytes behalten dedizierte Namen; Überlauf-, Chunk-/Datei-Read-, Allokations- und Host-Guards bleiben erhalten. Die Framework-Vertragsmigration wird getrennt verantwortet; MRTS bleibt unverändert.

## Geänderte Dateien

Common-Konfiguration, Direktiven-Spec/-Adapter und Modus-Accounting; Apache-/NGINX-Registrierungen und Harness-Konfiguration; abhängige Host-Aufrufer und betroffene Tests. Dokumentationspaare: connectors/apache/README, connectors/nginx/README, docs/phase4-mode-budget, docs/testing-and-evidence, examples/apache/README und examples/nginx/README. Acht Beispieldirektiven entfernen. ci/checks/documentation/connector_config_reference.py aktualisieren und beide Apache-/NGINX-configuration-reference-Paare sowie reports/connector-configuration-inventory.json neu generieren. Historische Change Records unverändert lassen.

## Ausgeführte Befehle

`rtk proxy python3 -B -m unittest tests.test_logical_connector_all_examples.LogicalConnectorAllExamplesTests.test_removed_phase4_body_limit_is_absent_from_host_examples`: anfangs Exit 1 mit acht erwarteten Beispiel-Failures. Nach Entfernung `rtk proxy python3 -B -m unittest tests.test_logical_connector_all_examples`: Exit 0, 12 Tests. `rtk proxy make generate-connector-config-reference`: Exit 0, fünf generierte Dateien aktualisiert. `rtk proxy make check-connector-config-reference`: Exit 0, alle 21 generierten Dateien aktuell. `rtk proxy make check-bilingual-docs`: Exit 0. Weitere integrierte Validierung wird separat vom Koordinator dokumentiert und hier nicht behauptet.

Precommit-Prüfungen des Koordinators am Removal-Worktree auf der obigen Basisrevision: Configtest-Driver24 + Selected-Wiring17 + Collection-/Dispatch58 Tests Exit0; Produkt-Fokus45 Tests Exit0; Common-C17 und kompilierte Hardcap-/Default-Assertions Exit0; vier Adoption-Targets Exit0. Vollständiges natives Parent-`make lint` Exit0 in166.955s, mit vier temporären Clean-Framework-Root-SKIPs, die nach Framework-Commit erneut geprüft werden müssen. Die unabhängige breite77-Testauswahl enthält weiterhin drei Failures und einen Error, separat auf dem eingefrorenen b404 reproduziert; keine Assertions abgeschwächt. Zugewiesene Shell-Syntaxprüfungen bestehen; ShellCheck enthält16 identische Baseline-Findings. Dies sind Worktree-Prüfungen, keine Clean-New-Head-Runtime-Behauptung.

## Security-Auswirkung

Beabsichtigte Breaking Change der Konfiguration/API; Betreiber müssen die Direktive entfernen. Dies deaktiviert keine Response-Inspection der Engine und erlaubt keine unbegrenzten Allokationen. Bestehende unabhängige Ressourcenschutzgrenzen bleiben erforderlich. Die Required-Auswahl wird nicht verkleinert; fehlende Evidence kann nicht PASS werden.

## Runtime-Evidence

Dieser Dokumentationscheckpoint behauptet keinen frischen HTTP-/Configtest-Runtime- oder Full97-Nachweis des Removal-Heads. Frühere b404-Runtime-Evidence beweist nur ihr historisches Source-Tupel.

## Bekannte Einschränkungen

Früher gültige Konfigurationen mit der entfernten Direktive scheitern jetzt beim Konfigurationsladen. Die vier Engine-Response-Limit-Cases bleiben unabhängig und Required.

## Verbleibende Risiken

Integrierte connectorübergreifende Kompilierung und frische sourcegebundene Config-/Runtime-Prüfungen müssen das endgültig gelieferte Tupel bestätigen; Dokumentations- und Unit-Test-Erfolg allein ist kein solcher Nachweis.

## Nicht ausgeführte Prüfungen mit Begründung

Full97 und Protected Exact-Head wurden für diese Entfernung nicht ausgeführt. Sie bleiben getrennte Bereitschafts-/Autorisierungsgates. CI, Sonar, Delivery und finale sourcegebundene Runtime-Ergebnisse werden nicht aus früheren Heads abgeleitet.

## Finaler Diff- und Review-Status

Begrenzter Dokumentations-/Generator- und kombinierter Source-Diff durch Koordinator und unabhängigen Read-only-Reviewer geprüft; keine eingeführte Regression gefunden. Generierte Dateien durch den nativen Generator geändert. Die bestehende Apache-Duplicate-Field-Abwesenheitsprüfung bleibt aktiv. Der Dokumentationsworker führte keinen Commit, Push, Merge oder PR-Statuswechsel aus; Koordinator-Delivery und echte New-Head-Runtime bleiben separat.
