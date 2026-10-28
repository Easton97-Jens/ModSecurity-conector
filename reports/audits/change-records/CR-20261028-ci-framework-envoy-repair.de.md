# Change Record: CR-20261028-ci-framework-envoy-repair

**Sprache:** [English](CR-20261028-ci-framework-envoy-repair.md) | Deutsch

Begrenzte Parent-CI-Reparatur und geprüftes Envoy-Abhängigkeitsupdate. Die lokale Prüfung ist abgeschlossen; gehostete CI- und Sonar-Prüfung des aktuellen Heads stehen aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-ci-framework-envoy-repair |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `f5523da040bd6325b369269ada074be6ba069c4f` |

## Motivation und Problemstellung

Die angefragte Prüfung umfasst Updater-Lauf `40576069804`, die Abhängigkeits-PRs [#423](https://github.com/Easton97-Jens/ModSecurity-conector/pull/423), [#424](https://github.com/Easton97-Jens/ModSecurity-conector/pull/424), [#425](https://github.com/Easton97-Jens/ModSecurity-conector/pull/425) und SonarQube-Befunde.

Der Updater lehnt den aktuellen Parent-Workflow ab, weil sein Validator weiterhin ein entferntes `--nginx-archive`-Argument verlangt. Der Workflow provisioniert inzwischen Runtime-Komponenten und reicht das gepinnte NGINX-Tupel durch `env -i` an den gehosteten Inventory-Runner weiter. Unabhängig davon ändern die Abhängigkeits-PRs eine im Inventar geprüfte `go.mod`, ohne deren geprüften Quelldigest zu aktualisieren. Dadurch entsteht `ACTIVE_INVENTORY_REJECTED`, bevor betroffene Tests laufen. PR #423 enthält bereits die separat in #424 und #425 vorgeschlagenen Abhängigkeitsversionen.

## Akzeptanzkriterien

| Kriterium | Nachweis und Status |
| --- | --- |
| Aktuelle gepinnte NGINX-Übergabe akzeptieren und fehlende, doppelte, ersetzte oder auskommentierte Weitergabe ablehnen | Gezielte positive Regression und 28 Weitergabevarianten lokal bestanden; gehosteter Updater-Neulauf steht aus. |
| Geprüftes kombiniertes Abhängigkeitsupdate aus #423 übernehmen | `go.mod` und `go.sum` sind byteidentisch zu PR-#423-Head `b55dafccd981654e43639d2038429eb2db637031`; Go-Build/Tests benötigen CI. |
| Nur geprüfte geänderte Inventarquellen neu binden und Auswahl erhalten | Drei explizite SHA256-Bindungen aktualisiert; natives Archiv neu generiert. Auswahl bleibt bei 100 Fällen / 80 Ausführungen; On-Demand-Archiv bleibt bei 1893 Fällen / 839 Ausführungen. Abschließende Inventarprüfungen stehen unten. |
| Sonar-Nachweise bewerten, ohne die Analyse abzuschwächen | Bestehende Fehler identifiziert; einzelne Issue-IDs und eine neue Analyse sind nicht verfügbar. Keine Befundreduktion und kein bestandenes Gate werden behauptet. |

## Implementierungsentscheidung und Begründung

Die veraltete Archivargument-Prüfung wird durch eindeutige, exakte Shell-Weitergabeprüfungen für alle sechs `NGINX_FIELDS` und das Parent-eigene Flag `NGINX_REQUIRE_PINNED_PROVENANCE` ersetzt. Der Zuweisungsabgleich ist an Zeilenpräfixe aus reinen Zuweisungen gebunden; ein Kommentar oder fremder Befehl erfüllt die Weitergabeprüfung nicht. Bestehende Prüfungen für Kandidatendaten, Parent-YAML/Python-Pins, Provenienz, Revisions-Lock und Schreibfreiheit bleiben erhalten. Die geschützte NGINX-Root-Broker-Kette bleibt unverändert.

Eine vorhandene Drift-Regression wird erweitert; es kommen keine automatischen Testselektoren hinzu. Die zwei geprüften Abhängigkeitsdateien aus #423 werden integriert: Envoy `v1.40.0`, gRPC `v1.84.0`, protobuf `v1.36.12` und genproto RPC `v0.0.0-20260720211330-0afa2a65878a`. Dies enthält den Versionsinhalt von #424/#425, ohne diese PRs zu mergen oder zu schließen. Nur die geprüften Quellbindungen für Validator, Testmodul und `go.mod` werden aktualisiert; das Spezialarchiv wird über seinen nativen Generator neu erstellt.

## Geänderte Dateien

| Dateien | Änderung |
| --- | --- |
| `ci/tools/verify-framework-candidate-contract.py` | Aktuelle Runtime-Weitergabegrenze des Workflows prüfen. |
| `tests/test_verify_framework_candidate_contract.py` | Vorhandenen Drift-Test um 28 negative Weitergabevarianten erweitern. |
| `connectors/envoy/ext_proc/go.mod`, `connectors/envoy/ext_proc/go.sum` | Geprüftes kombiniertes Update aus PR #423. |
| `config/testing/active-cases.json` | Nur drei geprüfte Quell-SHA256-Bindungen; Auswahl unverändert. |
| `reports/testing/test-selection-archive.generated.json` | Native Neugenerierung nach erneuter Bindung geprüfter Quellen. |
| `reports/audits/change-records/CR-20261028-ci-framework-envoy-repair.md`, `reports/audits/change-records/CR-20261028-ci-framework-envoy-repair.de.md` | Inhaltlich gleichwertige englische/deutsche Change Records. |

## Ausgeführte Befehle

Projekt-Shellbefehle verwenden aufgabeneigenes RTK `v1.0.1` unter `/workspace/scratch/5e0fa1c15f63/task-tools/rtk`, geprüft gegen die gepinnte Upstream-Prüfsumme. Die folgenden Befehle beschreiben ihre relevanten nativen Aufrufe; aufgabeneigene Umgebungs- und temporäre Pfade liegen außerhalb des Checkouts. Es wurden keine Zugangsdaten aufgezeichnet.

| Befehl oder Verfahren | Tatsächliches Ergebnis |
| --- | --- |
| RTK-gekapselte Python-3.11-Reproduktion mit Laden von `git show HEAD:ci/tools/verify-framework-candidate-contract.py` im Speicher | Exit 0: ursprünglicher Validator erzeugt exakt `NGINX exact-head archive argument must contain exactly one supported assignment` gegen die aktuelle Parent-Fixture. |
| `python3 -m unittest tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_current_parent_contract_matches_the_candidate_without_writing tests.test_verify_framework_candidate_contract.VerifyFrameworkCandidateContractTests.test_each_unprotected_handoff_layer_rejects_a_representative_drift` | Python 3.11: 2 Tests bestanden, Exit 0; Koordinator bestand dieselben gezielten Tests unabhängig unter Python 3.12.14. |
| `rtk bypass python3 ci/tools/update-test-archive.py`, danach `--check`; `rtk bypass python3 ci/tools/run-active-tests.py --check`; expliziter Vergleich mit der Basis | Alle Exit 0. Exakt drei geprüfte SHA256-Felder unterscheiden sich; beide vollständigen Ausführungslisten bleiben unverändert (100/80 Standard, 1893/839 auf Abruf). |
| `rtk bypass env ON_DEMAND_TESTS=1 python3 -m unittest -v tests.test_verify_framework_candidate_contract` | Exit 0: 29 Tests, zunächst 28 bestanden und 1 übersprungen. Nach Initialisierung des gepinnten Framework-Submoduls bestand der zuvor übersprungene Checked-out-common-Test separat (1/1, Exit 0). |
| `rtk bypass git diff --check` | Exit 0 für den kombinierten Diff. |
| `rtk bypass make check-bilingual-docs`; `rtk bypass make check-doc-links` | Beide Exit 0. Die erste Linkprüfung scheiterte nur am nicht initialisierten Framework; nach Checkout des exakten vorhandenen Gitlinks ohne dessen Änderung bestand sie. |

Der tatsächliche Updater-Kandidat `3a4f2281568139d94fda6b51dc2e07bb8fc06c67` wurde nur lesend abgerufen. Seine `ci/lib/common.sh` hat SHA256 `d42967158f7fe01a983ae0e27dca00ea02194362ec84275b16b87db10a703dee`. Der ursprüngliche Validator reproduzierte mit diesen Bytes exakt den gehosteten Fehler. Die korrigierte CLI bestand mit `--candidate-sha 3a4f2281568139d94fda6b51dc2e07bb8fc06c67 --framework-common /workspace/scratch/5e0fa1c15f63/task-state/candidate-common.sh --expected-parent-framework-sha 99a7985c1be92a2297b1b59208f64df6768f2cbf --candidate-framework-root modules/ModSecurity-test-Framework`. Dies belegt die Datenzulassung mit unverändertem Parent-Lock, nicht den gesamten gehosteten Updater.

## Security-Auswirkung

Der geänderte Validator ist eine reine Datenprüfgrenze für CI-Zulassung. Er erhält feste Quell-Pins und geschlossenes Fehlerverhalten und prüft dabei die tatsächliche Runtime-Übergabe des Workflows. Fehlende, doppelte, veränderte und auskommentierte Weitergabe wird ohne Parent-Schreibzugriffe abgelehnt. Keine Kandidaten-Shell wird ausgeführt. Framework/MRTS-Quellen, geschützter Broker, CI-Berechtigungen, Regeln, Quality Gates, Ausschlüsse und Unterdrückungen bleiben unverändert.

Das Abhängigkeitsupdate ändert eine sicherheitsrelevante Netzwerk-/Protokollbibliotheksgrenze. Statische Gleichheit mit dem geprüften Dependabot-Update beweist weder Runtime-Kompatibilität noch die Behebung von Schwachstellen; CI mit gepinnter Toolchain bleibt erforderlich.

## Runtime-Evidence

Es wurden keine gehostete Runtime, Connector-Matrix oder I12-Kampagne ausgeführt. Lokale Vertragstests belegen ausschließlich das Validatorverhalten. Bestehende bestandene Prüfungen anderer Revisionen qualifizieren den künftigen PR-Head dieser Änderung nicht.

## Bekannte Einschränkungen

Im Cloud-Checkout fehlen das ursprüngliche `/root/.agents/skills/goal-driven-execution/SKILL.md`, die lokale `.codex/config.toml` und konfigurierte externe Arbeitswurzeln. Die reversible Einrichtung verwendete aufgabeneigene Workspace-Pfade außerhalb des Repositorys und eine prüfsummenverifizierte RTK-Datei. Die ursprüngliche lokale Umgebung wurde nicht rekonstruiert.

Das im Repository gepinnte Python 3.15 und Go 1.26.9 sind nicht verfügbar. Lokale Python-3.11/3.12.14-Tests liefern nur begrenzte Kompatibilitätsnachweise. Sonar-CLI, der erforderliche `/usr/local/bin/sonar-with-env`, eine kompatible Sonar-Werkzeugverbindung und Container-Runtime sind hier nicht verfügbar. Ausgewählte Sonar-Plugin-Skills wurden gelesen; eine direkte Issue-Liste oder neue Analyse wurde nicht abgerufen. Auch die vom Nutzer verlinkte SonarCloud-Codeansicht lieferte CloudFront HTTP 403, einschließlich nach einmaligem Neuladen.

## Verbleibende Risiken

Die beobachteten Sonar-Gates für Master-Hauptanalyse und zwölf native Analysen schlagen fehl; einzelne Issue-IDs und vollständige aktuelle Metriken waren nicht verfügbar. Dependabot-Sonar-Jobs scheitern vor der Analyse mit HTTP 403. Diese Änderung belegt keine Befundreduktion und repariert keine Authentifizierung. Neue PR-CI kann separate bestehende Fehler oder Kompatibilitätsprobleme aufdecken.

Ein erfolgreicher lokaler Vertragstest beweist nicht, dass die übrigen Isolations-, Kandidatenprüfungs- und PR-Veröffentlichungsschritte des Updaters erfolgreich sind. Dafür ist nach Integration ein neuer gehosteter Lauf nötig.

## Nicht ausgeführte Prüfungen mit Begründung

Prüfung unter gepinntem Python 3.15, Go-1.26.9-Kompilation/Tests, gehostete Updater-Ausführung, vollständige Connector-Runtime-Arbeit und neue Sonar-Analyse wurden nicht ausgeführt, weil erforderliche lokale Toolchains/Dienste fehlen oder die gehostete Integration noch nicht stattgefunden hat. Dokumentations- und kombinierte Diff-Prüfungen bestanden wie oben dokumentiert. Historische I12-Nachweisarbeit bleibt außerhalb dieser begrenzten Reparatur.

## Finaler Diff- und Review-Status

Der integrierte Diff wurde geprüft; gezielte/vollständige betroffene Vertragstests, Inventarzulassung, generiertes Archiv, Dokumentation und Whitespace-Prüfung bestanden. Der lokale Stand ist für einen aufgabeneigenen Draft-PR vorbereitet. Die PR-Beschreibung muss nachfolgende Auslieferung und CI-Fakten des aktuellen Heads festhalten. Merge, Alt-PR-Abschluss, Master-Änderung, bestandenes Sonar-Gate oder Status `verified_pr` werden nicht behauptet.
