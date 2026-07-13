# CI-Werkzeuge

**Sprache:** [English](README.md) | Deutsch

Dieser Baum enthält Connector-Repository-Orchestrierung, Verträge und Evidence-Werkzeuge. Das Framework besitzt den wiederverwendbaren Case-Katalog; dieses Repository besitzt die Connector-Integration über `FRAMEWORK_ROOT`.

## Struktur

| Bereich | Verantwortung | Aufruf |
| --- | --- | --- |
| `checks/common/` | Common-SDK-, Build-, Flow-, Memory-, Directive- und Adapter-Verträge | passendes `make check-*`-Target |
| `checks/connectors/` | Connector- und Aggregate-Adoption-Verträge | `make check-<connector>-*` |
| `checks/documentation/` | Sprach-, Link-, Generated-Layout-, Pfad- und Variablenprüfungen | `make check-doc-links` |
| `checks/evidence/` | Lifecycle-, Fixture-, Capability- und Core-Completion-Prüfungen | Evidence-Targets |
| `checks/security/` | Runtime-Pfad- und Artefaktsicherheit | `make check-runtime-path-policy` |
| `runtime/common/` | Gemeinsame Pfad-, Prozess-, Port- und Fixture-Helfer | Nur Runner-Unterstützung |
| `runtime/lifecycle/` | Kanonische Runner, Normalisierer und Artefaktschreiber | Lifecycle-Make-Targets |
| `provisioning/` | Cache-v2-, Komponenten- und Toolchain-Vorbereitung | `make prepare-runtime-components` |
| `evidence/collectors/` | Capability-Erfassung | `make capabilities-*` |
| `evidence/reports/` | Berichtsgeneratoren und Refresh-Orchestrierung | `make refresh-all-reports` |
| `lib/` | Gemeinsame importierte Python-Helfer | Kein Einzel-Einstiegspunkt |
| `tools/` | Kleine Wartungseingaben | Nur dokumentierter Aufrufer |

Python-Dateien verwenden `snake_case.py`; etablierte Shell-Namen behalten ihre `kebab-case.sh`-Form. Stabile Dateinamen werden nicht nur aus kosmetischen Gründen umbenannt.

## Einstiegspunkte und Eingaben

Verwende Make-Targets statt verschachtelte Dateien aus einem beliebigen Arbeitsverzeichnis aufzurufen. Sie setzen repository-relative Roots und prüfen das Framework.

| Target | Zweck | Eingaben | Artefakte |
| --- | --- | --- | --- |
| `make quick-check` | Schnelle Vertrags-, Syntax- und Dokumentationsprüfung | `PYTHON`, `FRAMEWORK_ROOT` | Keine kanonische Runtime-Evidence |
| `make prepare-runtime-components` | Materialisiert oder verwendet Cache-v2-Eingaben erneut | `BUILD_ROOT`, `CACHE_ROOT`, `CONNECTOR_COMPONENT_CACHE` | Komponentenmanifest und lokaler Snapshot |
| `make full-lifecycle-<connector>` | Führt ein ausgewähltes natives HTTP/1.1-Kernprofil aus | `<connector>` = `apache`, `nginx`, `haproxy`, `envoy`, `traefik` oder `lighttpd`; `NO_CRS_RUN_ID` | Connector-Evidence |
| `make full-lifecycle-all-connectors` | Führt alle sechs ausgewählten Profile aus | `NO_CRS_RUN_ID`, beschreibbare Runtime-/Evidence-Roots | Sechs Result-Sets |
| `make check-six-connector-core-completion` | Validiert Aggregate-Evidence | Gleiche Run-ID und Evidence-Root | Aggregate PASS/FAIL |

`NO_CRS_RUN_ID` ist eine dateisystemsichere Laufkennung, beispielsweise `repository-cleanup-core-20260712T164725Z`. Keine Secrets, Benutzernamen oder Tickettexte verwenden. Details stehen in der [Variablenreferenz](../docs/reference/variables.de.md).

## Evidence-Ablauf

1. Make löst Repository-, Build-, Cache-, Runtime- und Evidence-Roots auf.
2. `provisioning/` bereitet einen identity-gebundenen Cache-v2-Eintrag vor.
3. `runtime/lifecycle/` führt ein Hostprofil aus und schreibt payloadfreie lokale Daten.
4. Framework und `evidence/collectors/` normalisieren und validieren diese Daten.
5. `checks/evidence/` entscheidet, ob sie den gewählten Claim stützen.
6. `evidence/reports/` erzeugt versionierte Berichte neu; Generated-Ausgabe nie manuell ändern.

Exit `0` bedeutet technische Beendigung, nicht dass jeder Katalogfall `PASS` ist. `1` ist ein allgemeiner Fehler, `2` typischerweise ein Validierungs-/Aggregate-Fehler und `77` eine deklarierte fehlende optionale Voraussetzung. Statussemantik steht unter [Testebenen](../docs/testing-and-evidence.de.md).

## Neue Datei hinzufügen

Eine neue Datei wird bei ihrer Verantwortung einsortiert, ihr Make-/Workflow-Aufrufer aktualisiert und über `Path(__file__).resolve()` oder ein aus `dirname -- "$0"` abgeleitetes `SCRIPT_DIR` lokalisiert. Keine Workspace-spezifischen Pfade, keine Duplikate eines `lib/`-Helfers und keine neue Runtime-Capability in dieser organisatorischen Änderung hinzufügen.
