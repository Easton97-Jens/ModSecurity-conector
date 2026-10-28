# Change Record: CR-20261028-submodule-native-prerequisites

**Sprache:** [English](CR-20261028-submodule-native-prerequisites.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261028-submodule-native-prerequisites |
| Datum (UTC) | 2026-10-28 |
| Basis-Revision | `cac9461a4e831ea5c45a1eeec4ef21ce63d203e9` |

## Motivation und Problemstellung

Lauf `40658370393`, Job `122715236041`, besteht die bisherigen NGINX- und PyYAML-Fixes und scheitert danach am ausgewählten Fall `apache.zero_result_releases_native_buffers_without_a_rule`. Dem Updater fehlen die von dieser Fixture benötigten und in normalen Quick-Check-Jobs bereits installierten Apache-/APR-/ModSecurity-Entwicklungsvoraussetzungen. Außerdem geht stdout des fehlgeschlagenen Namespace verloren, weil errexit nach der Command Substitution vor der Ausgabe beendet.

## Akzeptanzkriterien

Etablierte native Voraussetzungen vor Baseline-/Sandbox-Setup bereitstellen. Erfasste Diagnosen auch bei Fehlern ausgeben und den Fehlerstatus selbst dann erhalten, wenn stdout einen COMPLETE-Marker enthält. Quell-/Ausgabeprüfung, Cleanup und finale Fehlerdurchsetzung erhalten. Apache-C17-Ausgaben innerhalb der vorhandenen externen Wurzel halten und vollständige Standard-/Archivauswahl bewahren (100 Fälle / 80 Ausführungen; 1893 Fälle / 839 Ausführungen).

## Implementierungsentscheidung und Begründung

`build-essential apache2-dev libmodsecurity-dev` werden als Setup-Schritt unter dem normalen Runner nach dem Python-Interpretervertrag und vor Aufnahme der unveränderlichen Basis wiederverwendet. Werkzeuge, Header und Bibliotheken liegen anschließend hinter den vorhandenen schreibgeschützten Runtime-Mounts. Kein Compiler-Alias-Bypass oder breiteres Hostverzeichnis wird ergänzt.

Namespace-Status ausdrücklich erfassen, stdout ausgeben und anschließend vor Prüfung von COMPLETE den Fehler weitergeben. Stderr bleibt direkt sichtbar. Bestehende continue-on-error-, physische Prüf-, finale Durchsetzungs- und Cleanup-Gates bleiben unverändert.

Ein begrenztes Audit des restlichen Lint-Pfads fand beim Apache-C17-Script den Standard unter dem fehlenden `/var/tmp`. Die feste Kandidatenumgebung setzt nun `APACHE_C_STANDARDS_OUT` auf `/external/build/apache-c-standards`; `/var` wird nicht freigegeben.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`: native Voraussetzungen und Fehlerausgabe-/Statusbehandlung.
- `ci/tools/run-readonly-submodule-validation-namespace.py`: begrenzte Apache-Standards-Ausgabe.
- `tests/test_ci_security_workflows.py`, `tests/test_run_readonly_submodule_validation_namespace.py`: Regressionen für Voraussetzungen/Reihenfolge, Diagnose/Status/Cleanup und Ausgabegrenze. Eine neue Methode bleibt nur auf Abruf.
- `config/testing/active-cases.json`: vier geprüfte Quell-Hash-Felder, unveränderte Ausführungslisten.
- `reports/testing/test-selection-archive.generated.json`: native Neugenerierung; erhaltene Definitionen auf Abruf steigen auf 6194, ohne neue automatische Auswahl.
- `docs/build/README.md`, `docs/build/README.de.md` und dieses englisch/deutsche Record-Paar.

## Ausgeführte Befehle

Alle Projekt-Shell-Befehle verwendeten aufgabeneigenes RTK `v1.0.1`.

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Python 3.15.1: `ON_DEMAND_TESTS=1`-Unittest-Selektoren `test_update_submodules_separates_validation_from_publishing`, `test_submodule_namespace_failure_keeps_diagnostics_status_and_cleanup`, `test_candidate_environment_uses_only_namespace_views_for_sources` | Exit 0, 3 bestanden. Die Diagnoseregression prüft Erfolg, Kandidaten-Exit 17 mit COMPLETE-Marker sowie fehlenden Abschluss; stdout/stderr und Cleanup werden geprüft. |
| Gezielte Workflow-/Diagnosetests unter Python 3.12.14 und 3.15.1 | Beide bestanden; der im Speicher geladene ursprüngliche Workflow reproduziert den stdout-Verlust. |
| Ursprüngliche feste Umgebung im Speicher geladen | Apache-Standards-Ausgabeoverride fehlt; das Script fällt auf verbotenes `/var/tmp` zurück. Die korrigierte Umgebungsregression besteht. |
| Lokaler exakter Apache-Selektor | Scheitert im Setup an fehlenden Apache-/APR-Entwicklungsvoraussetzungen; keine Produktassertion läuft. Lokal wurden weder Systempakete installiert noch Skips ergänzt. |
| Positive normale CI-Kontrolle auf aktuellem Master: Lauf `40658304761`, Job `122714681042` | Abschließend erfolgreich auf derselben Quellrevision; Logs zeigen die Installation zuvor fehlender Apache-/APR-/ModSecurity-Entwicklungspakete und anschließend den bestandenen exakten Apache-Fall. Dies ist kein Ergebnis des gejailten Updaters. |
| Vollständige Inventarzulassung, exakter Auswahlvergleich, nativer Archivgenerator und `--check`, Variablendokumentation | Bestanden; vollständige Standard- und Abruf-Ausführungslisten bleiben unverändert. |
| Dokumentation und finale Whitespace-Prüfungen | Bestanden: zweisprachige Dokumentation, Links, Change-Record-Struktur und finale Whitespace-Prüfungen. |

## Security-Auswirkung

Quell- und Runtime-Mounts, feste Compiler, no-new-privileges, UID-/GID-Wechsel, Schreibproben, physische Inventar-/Ausgabeprüfungen, Sanitizer, Job-Berechtigungen, Ref-Allowlists und Publisher-Richtlinie bleiben unverändert. Natives Setup läuft vor Kandidatenausführung. Erfasste Kandidatenausgabe wurde bereits bei Erfolg ausgegeben; nun bleiben auch Fehlerdiagnosen erhalten, ohne einen Fehlerstatus oder Abschlussmarker als Erfolg zu akzeptieren.

## Runtime-Evidence

Lokale Shell-Regressionen belegen Diagnose-/Status-/Cleanup-Verhalten; Quell- und Umgebungstests belegen die feste Apache-Ausgabezuordnung. Normale CI des aktuellen Masters liefert eine positive native Fixture-Kontrolle. Der vollständige privilegierte Namespace mit diesem Patch benötigt nach normaler Integration weiterhin eine neue gehostete Ausführung; vollständiger Updater-, Hosted-Runtime- oder I12-Erfolg wird nicht behauptet.

## Bekannte Einschränkungen

Der ursprüngliche gehostete Traceback ist nicht verfügbar, weil stdout verworfen wurde und der Lauf keine Artefakte behielt. Die Voraussetzungsdiagnose wird durch Fixture-Setup-Anforderungen, den fehlenden Updater-Installationsschritt, lokale Reproduktion fehlender Voraussetzungen und die positive normale CI-Kontrolle derselben Quelle gestützt. Der reparierte Fehlerausgabepfad verhindert diesen Verlust bei weiteren Läufen. Lokale Namespace-/Sanitizer-Ausführung bleibt umgebungsbedingt eingeschränkt; kein Schutz wird dafür abgeschwächt.

## Verbleibende Risiken

Ein getrenntes nachgelagertes Publisher-Problem wurde durch rein lesendes Rendern des Kandidaten `3a4f2281568139d94fda6b51dc2e07bb8fc06c67` bestätigt: Der zentrale Lock-Digest ändert sich von `3981782d6ea6acc7e087a851709df220c83677bfeb92ee7836d1ec4e90b8d3b9` zu `880b1d19b6d78e52a1588033ce794a35d09e58040b8af763d90fcdb9f99c0d34`, aber Inventar-Begleitdateien des generierten PRs werden nicht aktualisiert/gestaged. Dies verursacht nicht den aktuellen Apache-Validierungsfehler. Es bleibt außerhalb dieser begrenzten Reparatur; seine Behebung verlangt unabhängig geprüfte Ableitung aus vertrauenswürdiger Basis und atomare Begleitdateibehandlung, keine bloße Allowlist-Erweiterung oder beliebige Hash-Erneuerung.

## Nicht ausgeführte Prüfungen mit Begründung

Neue vollständige gehostete Namespace- und Publisher-Ausführung benötigen normale Integration in eine erlaubte Ref. Keine Dispatch-Allowlist wird erweitert. Lokale native Ausführung ersetzt fehlende Entwicklungspakete oder nicht verfügbare Namespace-/Sanitizer-Unterstützung nicht. Keine neue Connector-Matrix, historische I12-Kampagne oder Sonar-Schließung wird behauptet.

## Finaler Diff- und Review-Status

Unabhängiges rein lesendes Review fand keinen materiellen Blocker in den vier Implementierungs-/Testdateien. Abschließende CI am tatsächlichen Head und Auslieferung stehen aus; Merge, Master-Änderung oder Status `verified_pr` werden nicht behauptet.
