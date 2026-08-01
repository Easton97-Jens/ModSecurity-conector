# Change Record: Vollständige Parent-CI-Runtime-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-ci-runtime-complete-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-runtime-complete-remediation` |
| Datum (UTC) | `2026-08-01` |
| Basis-Revision | `a7e2e70f307c91bc3da702b7240a1c4218cb2b79` |
| Ziel | Das aktuelle Parent-`ci/runtime`-SonarQube-Cloud-Inventar mit source-nativen Controls und fokussiertem Security-Review beheben und anschließend einen verifizierbaren Draft-PR veröffentlichen. |
| Grenze | Parent `ci/runtime/**`, das unmittelbar erforderliche Parent-`ci/lib/runtime_path_utils.py`, direkte Parent-Tests sowie dieses englische/deutsche Change-Record-Paar und seine Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gate, Exclusions, Suppressions, Workflows und `master` werden nicht geändert. |

## Motivation und Problemstellung

Die exakte `master`-SonarQube-Cloud-Analyse der Basis-Revision meldete in
`ci/runtime` 64 offene Einträge: 33 Vulnerabilities und 31 Code Smells bei null
Duplikatzeilen. Die betroffenen Lifecycle-Tools verarbeiten Runtime-Pfade,
wählen Subprocess-Argumente aus, schreiben Evidence und orchestrieren
begrenzte Jobs. Dies sind sowohl Security-relevante Grenzen als auch
Maintainability-Hotspots.

Die Arbeit entfernt deshalb doppelte Shell-Literale und backtracking-lastige
reguläre Ausdrücke, zerlegt hochkomplexe Lifecycle-Entscheidungen und begrenzt
Runtime-abgeleitete Ein- und Ausgabepfade auf einen privaten,
deskriptor-validierten Runtime-Root oder auf eine bestehende reguläre
Source-Datei unter einem kanonischen Parent-/Framework-Checkout.

## Akzeptanzkriterien

- Source-Fixes bewahren fail-closed Root-Ownership-, Mode-, No-Follow- und
  Containment-Controls vor jedem Runtime-Artefaktzugriff.
- Lifecycle-Child-Commands verwenden allow-gelistete Matrix-Tokens und
  kanonische Source-Roots; Timeouts bevorzugen weiterhin einen vollständigen
  Host-Job-Record.
- Bestehende Source-kompatible Report-, Status-, Event- und Evidence-Semantik
  bleibt durch fokussierte Regressionstests erhalten.
- Es wird weder `NOSONAR`, noch ein False-Positive-Wechsel, eine Suppression,
  Scanner-Konfiguration, Quality-Gate-Änderung oder Gitlink-Update verwendet.
- Der spätere exakte PR-Head benötigt frische GitHub-Actions- und
  SonarQube-Cloud-Evidence. Die New-Code-Abnahme bleibt null neue Issues und
  `0.0%` Duplikation; kein aktueller Eintrag wird vor dieser Analyse als
  behoben behauptet.

## Implementierungsentscheidung und Begründung

`runtime_artifact_path()` bleibt der zentrale Private-Runtime-Guard. Ein neuer
Companion erkennt für Lifecycle-Inputs, die eingecheckte Rules oder
Capabilities hashen müssen, ausschließlich reguläre nicht-symlinked
Source-Dateien unter den kanonischen Parent-/Framework-Roots. Alle anderen
Ein- und Ausgabepfade bleiben unter dem privaten Runtime-Root. Dadurch wird
keine Leseautorität auf beliebige Host-Pfade ausgeweitet.

Der Collector zerlegt nun Metadaten-Coercion, First-Byte-Validierung,
Raw-Event-Rejection und Case-Outcome-Evaluation in begrenzte Helper. Matrix-
und Native-Runner isolieren kanonischen Kontext, Child-Environment, Timeout
und Result-Klassifikation. Diese Änderungen bewahren die etablierten Verträge
und reduzieren gleichzeitig Decision-Nesting und wiederholte Literale.

## Bekannter nicht anwendbarer S5332-Hinweis

Der aktuelle `python:S5332`-Eintrag in
`ci/runtime/common/response-header-test-backend.py` ist kein remote
erreichbarer Produkt-HTTP-Service: Er bindet nur für Connector-Fixtures an
`127.0.0.1` und akzeptiert keinen Endpoint von einer nicht vertrauenswürdigen
Partei. Er ist bereits in `FND-SONAR-0001` mit hoher Konfidenz als
`not_actionable` dokumentiert. Diese Änderung markiert ihn weder als False
Positive noch akzeptiert sie ihn in SonarQube Cloud als Risiko; eine externe
Issue-State-Änderung erfordert eine getrennte aktuelle explizite Autorisierung.

## Geänderte Dateien

- `ci/lib/runtime_path_utils.py`
- `ci/runtime/common/resolve-runtime-paths.py`
- `ci/runtime/lifecycle/collect-no-crs-source.py`
- `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py`
- `ci/runtime/lifecycle/run-full-matrix-job.py`
- `ci/runtime/lifecycle/run-full-matrix-resume.py`
- `ci/runtime/lifecycle/run-mrts-native-full.sh`
- `ci/runtime/lifecycle/run-native-case-comparison.py`
- `ci/runtime/lifecycle/run-no-crs-baseline.sh`
- `ci/runtime/lifecycle/run-verified-case.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `ci/runtime/lifecycle/sanitize-full-lifecycle-log.py`
- `ci/runtime/lifecycle/write-*.py`-Lifecycle-Writer
- fokussierte `tests/test_*runtime*`, Resolver-, Engine-Artefakt- und
  Profile-Tests
- dieses Change-Record-Paar und seine Indizes

## Ausgeführte Befehle

| Befehl oder Control | Ergebnis |
| --- | --- |
| `python3 -m py_compile` für alle geänderten Python-Produktmodule und fokussierten Tests | bestanden. |
| `python3 tests/test_runtime_artifact_utils.py` | bestanden: 9 Tests. |
| `python3 tests/test_runtime_path_security.py` | bestanden: 21 Tests, einschließlich Symlink-Swap, normalisierter Parent-Traversal-Rejection, Generated-Report-Component-Allowlisting und Decimal-Only-Child-Timeout-Rendering. |
| `python3 tests/test_resolve_runtime_paths.py` | bestanden: 8 Tests. |
| `python3 tests/test_engine_lifecycle_artifacts.py` | bestanden: 5 Tests. |
| `python3 tests/test_full_lifecycle_profiles.py` | bestanden: 5 Tests. |
| `python3 tests/test_full_lifecycle_evidence.py` | bestanden: 19 Tests einschließlich des wiederhergestellten Same-Directory-Kompatibilitätspfads des Sanitizers und der Zurückweisung bereichsübergreifender Verwendung ohne benannte Runtime-Root. |
| `python3 tests/test_runtime_env_snapshot_contract.py RuntimeEnvironmentSnapshotContractTest.test_native_comparison_uses_the_wrapper_snapshot_not_shared_env RuntimeEnvironmentSnapshotContractTest.test_native_comparison_does_not_fallback_to_shared_env_for_an_invalid_snapshot` | bestanden: 2 direkte Snapshot-Selection-Controls. |
| `python3 tests/test_collect_no_crs_source_helpers.py` | bestanden: 3 Framework-unabhängige Collector-Helper-Tests. |
| `python3 tests/test_bilingual_docs.py` | bestanden: 22 Unit-Tests des Documentation-Checkers. |
| `sh -n ci/runtime/lifecycle/run-no-crs-baseline.sh` und `sh -n ci/runtime/lifecycle/run-mrts-native-full.sh` | bestanden. |
| `git diff --check` | am dokumentierten lokalen Stand vor der Delivery bestanden. |
| `python3 tests/test_collect_no_crs_source.py` | vor Testbeginn blockiert: Der Parent-gebundene Framework-Checkout enthält `ci/checks/catalog/no_crs_baseline.py` nicht. |
| `python3 tests/test_runtime_env_snapshot_contract.py` | nach 8 bestandenen Tests blockiert: Seine Wrapper-Integration benötigt dasselbe fehlende Parent-gebundene Framework-`ci/lib/common.sh`; die nativen Snapshot-Selection-Controls bestehen getrennt. |
| `python3 ci/checks/documentation/check-bilingual-docs.py` | nur durch vorbestehende Links in den fehlenden Parent-gebundenen Framework-Checkout blockiert; es wurde kein Change-Record-Fehler gemeldet. |

## Security-Auswirkung

Die geänderten Pfade decken CLI-/Environment-abgeleitete Dateisystemartefakte,
Source-Rule-Dateien, Shell-Subprocess-Argumente, Evidence-Streams und
Timeout-Cleanup ab. Der nächste Control ist der deskriptorbasierte
Private-Runtime-Validator, der nun vor den geänderten Writern greift. Legitime
private Roots, kanonische eingecheckte Source-Dateien und normale Job-Token-
Auswahl bleiben gültig; symlinked, außerhalb liegende und normalisierte
Traversal-Ziele werden vor Produktmutationen zurückgewiesen.

Keine Credential, kein Scanner, Test, Quality Gate, Repository-Setting oder
Workflow-Permission wird verändert. Das geprüfte Loopback-HTTP-Fixture bleibt
unverändert.

Die anfängliche Exact-Head-PR-Analyse meldete fünf neue Befunde: vier Taint-
Pfade (`pythonsecurity:S2083`, zwei `pythonsecurity:S8707` und
`pythonsecurity:S8705`) sowie `python:S1172`. Dieser Folgefix ersetzt den
direkten Pfad-Write des Sanitizers durch den vorhandenen atomaren
deskriptorbasierten Writer, begrenzt persistierte Diagnostics und Labels
positiv, validiert relative Report-Komponenten vor der Konstruktion und
rendert den Child-Timeout nur nach einer numerischen Grenzprüfung mit
`shell=False`. Die neue Exact-Head-SonarQube-Cloud-Analyse bleibt die
erforderliche Verifikation; es wurde kein Issue-Status geändert.

Der erste korrigierte Exact-Head entfernte diese fünf Befunde und bestand das
Quality Gate, aber sein exaktes SonarQube-Cloud-Inventar zeigte danach eine
`python:S3776`-Zeile in `load_runtime_env()`. Dieses Update zerlegt
Runtime-Root-Auswahl, Invocation-Snapshot-Validierung, Shared-Export-
Validierung und Export-Parsing in begrenzte Helper und bewahrt dabei denselben
No-Fallback-Snapshot-Vertrag. Die Analyse des nächsten exakten Heads bleibt
die erforderliche Verifikation.

## Kompatibilität und generierte Artefakte

Kein generiertes Artefakt wird committed. Bestehende Launcher-Optionen und
normale private Runtime-Orte bleiben unterstützt. Ungültige Pfade, die früher
einen Writer erreichten, können nun früher fehlschlagen; das ist die
beabsichtigte Sicherheitsänderung.

## Dokumentationsstatus

Das gepaarte Change Record und beide Indizes wurden ergänzt. Die fokussierte
Unit-Suite des bilingualen Checkers bestand; der repositoryweite Checker
erreichte die Records und meldete nur vorhandene fehlende Framework-Link-Ziele.

## Runtime-Evidence

Die fokussierte Evidence ist auf die oben aufgeführten direkten Python- und
Shell-Controls begrenzt. Sie beweist Private-Root-, Symlink- und lexikalische
Traversal-Rejection sowie normale Source-/Runtime-Artefaktbehandlung; sie ist
keine Connector-Matrix- oder Host-Runtime-Evidence.

## Bekannte Einschränkungen

Der vollständige Collector-Test und die Framework-abhängige Transport-
Integration können aus diesem frischen Parent-Worktree nicht laden, weil sein
gebundener Framework-Inhalt einen erforderlichen Catalog-Helper nicht enthält.
Diese Task initialisiert oder modifiziert weder Framework noch seinen Gitlink.
Vollständige Connector-Matrizen, Host-Setup, Paketinstallation und Live-
Multi-User-Races werden nicht behauptet.

## Verbleibende Risiken

Der exakte finale PR-Head benötigt weiterhin Hosted-Security-, Review- und
SonarQube-Cloud-Evidence. Der bekannte nur-Loopback-`S5332`-Hinweis bleibt ein
getrennter getrackter nicht anwendbarer Eintrag, bis eine autorisierte externe
Disposition ihn ändert.

Exact-Head-Hosted-Checks, SonarQube-Cloud-Ergebnis, Review und PR-Delivery-
Fakten stehen aus, bis der Task-Branch committed und veröffentlicht ist. Dieses
Record autorisiert keinen Merge und keine direkte `master`-Änderung.

## Nicht ausgeführte Prüfungen mit Begründung

- `tests/test_collect_no_crs_source.py` und seine Framework-gestützten
  Integrationsfälle können nicht importieren, weil
  `modules/ModSecurity-test-Framework/ci/checks/catalog/no_crs_baseline.py`
  an der Parent-gebundenen Revision fehlt; eine Änderung dieses Repositorys
  oder Gitlinks liegt außerhalb der Task-Grenze.
- Vollständige Connector-/Runtime-Matrizen, Host-Provisioning,
  Paketinstallation, Generated-Report-Refresh und Live-Cross-User-Race-Tests
  benötigen nicht verfügbare Native-Abhängigkeiten oder überschreiten den
  fokussierten Source-Remediation-Scope.
- GitHub Actions, Pull-Request-Secret-Scanning, Review und SonarQube Cloud
  benötigen den finalen exakten PR-Head und werden nicht aus lokalen Checks
  hergeleitet.

## Delivery-Status

Bei Erstellung des Records ist der Task-Worktree auf
`a7e2e70f307c91bc3da702b7240a1c4218cb2b79` rebaset. Es werden kein
Remote-Branch, kein PR, kein Hosted-Check, keine SonarQube-Cloud-Analyse, kein
Review und kein Merge behauptet. Vor der Delivery müssen lokaler, Remote- und
PR-Head als gleich verifiziert und Hosted-Ergebnisse für genau diesen Head
gelesen werden.

## Finaler Diff- und Review-Status

Der Source- und Direct-Test-Diff befindet sich im aktiven fokussierten
Security- und Final-Diff-Review. Ein verifizierter PR kann erst behauptet
werden, nachdem Review, Documentation-Validation, Commit, Veröffentlichung und
Exact-Head-Hosted-Readback abgeschlossen sind.
