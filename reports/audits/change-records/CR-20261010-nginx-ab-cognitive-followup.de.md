# Change Record: CR-20261010-nginx-ab-cognitive-followup

**Sprache:** [English](CR-20261010-nginx-ab-cognitive-followup.md) | Deutsch

Begrenzte verhaltensgleiche Qualitätsfolgearbeit; keine neue Runtime-Freigabe.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261010-nginx-ab-cognitive-followup |
| Datum (UTC) | 2026-10-10 |
| Basis-Revision | `2686b07aaf64b0541d743b53970008bd86caa91f` |

## Motivation und Problemstellung

Die Analyse von PR #396 bei `2686b07aaf64b0541d743b53970008bd86caa91f` meldete genau zwei `python:S3776`-Findings: `canonical_semantics` mit Komplexität 20/15 und `verify_binding` mit 16/15. Diese Folgearbeit ändert ausschließlich die Struktur.

## Akzeptanzkriterien

Intervention-/Rule-/Phase-/Transaction-Zuordnung, Vorrang des ersten technischen Fehlers, Snapshot- gegenüber Completion-Zählern sowie exakte Fehlermeldungen und Prüfungsreihenfolge erhalten. Bestehende Negativkontrollen und zusätzliche Charakterisierungen müssen vor und nach der Refaktorierung bestehen; eine frische serverseitige Sonar-Bestätigung bleibt erforderlich.

## Implementierungsentscheidung und Begründung

`restore_intervention_decision` und `bound_append` extrahieren, ohne die ursprünglichen Prädikate oder ihre Reihenfolge zu ändern. Canonical-Fehler- und Snapshot-Wiederherstellung behalten ihre ursprüngliche Reihenfolge. Keine Unterdrückung, Schwellenänderung, neuen Evidence-Felder oder Validator-Lockerungen.

## Geänderte Dateien

`ci/runtime/lifecycle/collect-no-crs-source.py`, `ci/lib/first_byte_binding.py`, `tests/test_no_crs_outcome_projection.py`, `tests/test_nginx_first_byte_binding.py` und dieses EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Über `rtk proxy`, mit gemeinsamem Python 3.14.7 und `PARENT_TEST_FRAMEWORK_ROOT` auf dem separaten Framework-Worktree: `python -m unittest -v tests.test_no_crs_outcome_projection tests.test_nginx_first_byte_binding tests.test_collect_no_crs_source_helpers tests.test_collect_no_crs_source tests.test_native_first_byte_shell_environment`: jeweils 91 Tests vorher und nachher, Exit 0. Eine Offline-Differenzprüfung gegen die eingefrorene Basis verifizierte 4800 Canonical-Eingabe-/Erwartungskombinationen und 26 gültige/ungültige Binding-Receipts einschließlich exakter Rückgabewerte oder Exception-Typ/-Meldung, Exit 0. Native Change-Record-Vorlagengenerierung erfolgreich. Vollständiger nativer Lint und abschließende Dokumentationsprüfungen werden in der externen Folge-Evidence erfasst; ihre Ergebnisse werden nicht aus Unit-Tests abgeleitet.

## Security-Auswirkung

Verhaltensgleiche Refaktorierung sicherheitsrelevanter Evidence-Consumer. Cross-Transaction-Ablehnung, Fail-Closed bei Mehrdeutigkeit, Datei-/Hash-/Pfad-/Zeitprüfungen und Fehlerpriorität bleiben unverändert. Framework und MRTS bleiben unverändert.

## Runtime-Evidence

Keine Runtime-Ausführung oder neue Runtime-Evidence in dieser Qualitätsfolgearbeit. Offline-Fixtures belegen weder Full97 noch Exact-Head PASS.

## Bekannte Einschränkungen

Kein lokaler Scanner war freigegeben. Reduzierte Komplexität ist eine Source-Review-Erwartung, kein behauptetes frisches Sonar-Ergebnis. Gemeinsames Python 3.14.7 reproduziert Framework-CI-Python 3.14.8 nicht. Vollständiges `make lint` endete im isolierten nicht initialisierten Worktree mit Exit 2: Der bestehende Runtime-Pfadprüfer lädt das fehlende verschachtelte Framework-`ci/lib/common.sh` und ignoriert das angegebene externe `FRAMEWORK_ROOT`. `make check-bilingual-docs` und `make check-doc-links` endeten jeweils mit Exit 2 wegen bestehender Links in dieses fehlende Submodul. Keine Initialisierung, Symlinks oder Prüfer-Lockerung vorgenommen. Die reine Change-Record-Archivprüfung bestand; die dokumentierte Suite `tests.test_change_record tests.test_prepare_reviewed_framework_handoff` bestand 39 Tests, Exit 0. Ein früherer Bedienaufruf benannte ein nicht vorhandenes Dokumentationstestmodul und endete mit Exit 1; dies bleibt im externen Log erhalten und gilt nicht als Sourcefehler. Integrierter Lint-/Dokumentations-Re-run im bestückten Worktree bleibt erforderlich.

## Verbleibende Risiken

Frische CI/Sonar am integrierten Head und Koordinator-Review bleiben erforderlich. Historische Full97-Fehler und Einschränkungen geschützter Infrastruktur bleiben getrennt.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Full97, tatsächlicher NGINX-Request, Namespace-/Root-Vorgang, Remote-Veröffentlichung oder Scanner: ausdrücklich außerhalb dieses begrenzten Worker-Auftrags. Keine Behauptung, dass grüne Unit-Tests erforderliche Runtime-Evidence ersetzen.

## Finaler Diff- und Review-Status

Minimale Extraktion in zwei Produktdateien plus vier Charakterisierungsmethoden und generiertes EN/DE-Record-Paar. Worker führte keinen Commit/Push aus; Integration und abschließender Review gehören dem Koordinator.
