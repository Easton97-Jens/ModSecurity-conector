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
| `runtime/contracts/` | Parent-eigener kanonischer Runtime-Observation-Vertrag, semantischer Validator und striktes CLI | `validate-runtime-observation.py` |
| `runtime/lifecycle/` | Kanonische Runner, Normalisierer und Artefaktschreiber | Lifecycle-Make-Targets |
| `provisioning/` | Cache-v2-, Komponenten- und Toolchain-Vorbereitung | `make prepare-runtime-components` |
| `evidence/collectors/` | Capability-Erfassung | `make capabilities-*` |
| `evidence/reports/` | Berichtsgeneratoren und Refresh-Orchestrierung | `make refresh-all-reports` |
| `lib/` | Gemeinsame importierte Python-Helfer | Kein Einzel-Einstiegspunkt |
| `tools/` | Kleine CI-Status- und Wartungseingaben | Nur dokumentierter Aufrufer |

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

Die obigen Sechs-Connector-Make-Targets sind allgemeine lokale
Orchestrierungs-Targets. Sie sind nicht die zeitgesteuerte/manuelle
CI-Baseline. Diese Baseline ist das geschlossene Profil <code>no-crs</code> in
<code>.github/workflows/reusable-five-connectors-profile.yml</code>, das von
<code>all-connectors-no-crs.yml</code> aufgerufen wird. Es wählt nur Apache,
HAProxy, Envoy, Traefik und lighttpd, weist unbekannte Profile und
Connector-Zeilen ab und aggregiert nur die fünf gebundenen Ergebnis-/Receipt-
Paare. Es behauptet weder NGINX noch CRS, MRTS, eine vollständige Matrix oder
einen bestandenen gehosteten Runtime-Lauf.

## Evidence-Ablauf

1. Make löst Repository-, Build-, Cache-, Runtime- und Evidence-Roots auf.
2. `provisioning/` bereitet einen identity-gebundenen Cache-v2-Eintrag vor.
3. `runtime/lifecycle/` führt ein Hostprofil aus und schreibt payloadfreie lokale Daten.
4. `runtime/contracts/` validiert die identity-gebundene, payloadfreie Parent-Runtime-Observation.
5. Framework und `evidence/collectors/` normalisieren und validieren wiederverwendbare Katalogdaten.
6. `checks/evidence/` entscheidet, ob sie den gewählten Claim stützen.
7. `evidence/reports/` erzeugt versionierte Berichte neu; Generated-Ausgabe nie manuell ändern.

Exit `0` bedeutet technische Beendigung, nicht dass jeder Katalogfall `PASS` ist. `1` ist ein allgemeiner Fehler, `2` typischerweise ein Validierungs-/Aggregate-Fehler und `77` eine deklarierte fehlende optionale Voraussetzung. Ein rekursiver GNU-Make-Aufruf kann seine fehlgeschlagene Recipe als `2` berichten, obwohl der direkte Child-Prozess `77` lieferte; Aufrufer dürfen den ursprünglichen Status nicht aus diesem rekursiven Exitcode ableiten. Statussemantik steht unter [Testebenen](../docs/testing-and-evidence.de.md).

## Kanonischer Runtime-Observation-Vertrag

`runtime/contracts/` ist die Parent-eigene Grenze für kanonische
Runtime-Observations. `runtime-observation.schema.json` definiert die
Transportform; `runtime_observation.py` ist der einzige semantische Validator
und sichere Dateileser. Der Vertrag bindet Connector, Profil, Laufkennung,
Parent-Commit, Framework-Commit und MRTS-Commit für jedes Profil an die
Evidence. Er ist payloadfrei und erlaubt nur sichere relative Evidence-Referenzen,
damit keine Requests, Logs, Secrets oder absoluten Runner-Pfade zu
Berichtsmetadaten werden.

Der strikte Einstiegspunkt ist:

```sh
"$PYTHON" ci/runtime/contracts/validate-runtime-observation.py \
  --observation "<private-evidence-root>/runtime-observation.json" \
  --evidence-root "<private-evidence-root>" \
  --connector envoy --profile with-crs-no-mrts \
  --run-id RUN_ID --parent-sha PARENT_SHA --framework-sha FRAMEWORK_SHA \
  --mrts-sha MRTS_SHA \
  --policy strict
```

Die Standardeinstellung `--policy strict` gibt payloadfreies JSON aus und
liefert nur für `PASS` den Exitcode `0`; unsichere Eingaben,
Identitätsabweichungen, fehlende Evidence oder semantische Abweichungen
liefern `VALIDATION_FAILED` und Exitcode `2`. `--policy partial` meldet
unvollständige Evidence als `PARTIAL`, bleibt aber nicht erfolgreich. Ein
`PASS` verlangt übereinstimmende typisierte Erwartungen und Observations,
einen ausgewählten und ausgeführten Live-Framework-Fall, null Fehler bzw.
Abweichungen und keine Cleanup-Reste. No-MRTS-Profile dürfen ausschließlich
negative MRTS-Isolationsfakten enthalten und müssen zugleich den ausgewählten
klein geschriebenen vollständigen `mrts_commit` binden; sie dürfen keinen
MRTS-Runner aufrufen, kein Inventory laden, keinen Prozess oder Listener
starten und kein MRTS-Artefakt verwenden. `--mrts-sha` ist für jedes Profil
erforderlich.

Der Leser verlangt, dass die aktuelle UID den Evidence-Root und jedes
Unterverzeichnis besitzt, jeweils mit exakt Modus 0700, sowie reguläre
Evidence-Dateien mit exakt Modus 0600. Er weist symbolische und harte Links
ab, begrenzt Observations auf 1 MiB und weist doppelte JSON-Schlüssel sowie
nicht striktes UTF-8 ab. Envoy, lighttpd und Traefik besitzen Live-Producer-
Adapter. Apache und HAProxy stellen nur Schnittstellen bereit. NGINX bleibt
eine geschützte separate Grenze: Der gemeinsame Validator akzeptiert nur
seinen genehmigten Protected-Producer und Protected-Runtime-Evidence, während
dieser PR den Broker-Produktionspfad weder aufruft noch verändert. Die
Contract-Tests belegen Validator-Verhalten, kein gehostetes Runtime-Ergebnis.

## Statusdatensätze für optionale Voraussetzungen

`ci/tools/run-check-status.py` führt einen direkten Child-Befehl aus,
schreibt einen payloadfreien JSON-Datensatz und gibt eine `CHECK_STATUS`-JSON-
Zeile aus, bevor Make den Exitcode des Child-Prozesses ersetzen kann. Der
persistierte Datensatz ist der Statuskanal: Seine `schema_version` ist `2` und
`status_source` ist entweder `child_exit_code`, `parent_preflight` oder
`parent_explicit`. Child-`stdout` und Child-`stderr` werden nur zur Diagnose
weitergeleitet; keiner der beiden Streams kann einen Grund liefern oder ein
Workflow-Ergebnis autorisieren. Seine Datensätze verwenden dieses
kleingeschriebene Statusmodell:

| Status | Bedeutung | Standard-Workflow-Ergebnis |
| --- | --- | --- |
| `passed` | Die direkte Prüfung lief und war erfolgreich. | erfolgreich |
| `failed` | Die direkte Prüfung lieferte einen anderen Fehler als den deklarierten Blocked-Code. | Fehler |
| `blocked` | Die Prüfung ist relevant, aber eine deklarierte Voraussetzung ist nicht verfügbar. | Fehler, außer der `parent_preflight` dieses Runners zeichnet einen erlaubten strukturierten Grund auf |
| `not_applicable` | Der Aufrufer hält ausdrücklich fest, dass die Prüfung außerhalb des Scope dieses Jobs liegt. | Fehler, außer ihr Aufrufer erlaubt sie ausdrücklich |
| `not_executed` | Die Prüfung wurde absichtlich nicht gestartet und hat keine gültige Disposition. | Fehler |

Der Runner leitet aus seiner validierten `--check`-Kennung einen festen
Dateinamen unter `$(BUILD_ROOT)/check-status` ab; für die Apache-Cleanup-
Prüfung ist dies `apache-request-transaction-cleanup.json`. Er akzeptiert
keinen vom Aufrufer gewählten Statusdateipfad. `BUILD_ROOT` muss ein absoluter,
kanonischer, invocation-eigener externer Pfad sein; der Runner weist Checkout-lokale,
nichtkanonische und symbolisch verlinkte Roots oder Statusdateien vor dem
Schreiben zurück. Er öffnet das validierte Statusverzeichnis vor dem Start des
Child-Befehls und verwendet diesen Verzeichnis-Handle für die temporäre Datei
und das finale Ersetzen. Diese Datensätze sind CI-Steuerungs-Evidence, keine
kanonische Runtime-Evidence.

`make check-apache-request-transaction-cleanup` bleibt strikt: Sein
Python-Quellvertrag und der native Apache/APR-Harness müssen beide vollständig
sein, und eine fehlende Voraussetzung bleibt nichtnull. Dagegen behält
`make check-apache-request-transaction-cleanup-lint` denselben verpflichtenden
Python-Quellvertrag bei, verwendet jedoch den Parent-eigenen Preflight
`--blocked-if-missing-apache-development`. Bevor das Child startet, löst der
Runner `APXS_BIN`, dann `APXS`, dann `CI_APXS_BIN_CANDIDATES` (oder
`apxs`/`apxs2`) auf und verlangt ein ausführbares APXS, dessen Ergebnis von
`-q INCLUDEDIR` ein absolutes Verzeichnis mit `httpd.h` ist. Nur wenn dieser
Preflight fehlschlägt, zeichnet der Runner das strukturierte
`apache_development_prerequisite`-`blocked`-Ergebnis auf und erlaubt es für
dieses Lint-Target. Besteht der Preflight, läuft das Child; jedes Child-`77`,
einschließlich eines kopierten oder gefälschten `CHECK_STATUS_REASON`-Strings
in einem der beiden Ausgabestreams, bleibt ein nicht klassifiziertes Ergebnis
ungleich null. Die fünf dokumentierten Push-Workflows erreichen diese eine
Subprüfung über `make lint` oder `make quick-check`; kein anderes Target, kein
Common-Check und kein Connector-Check erbt diese Erlaubnis.

## Neue Datei hinzufügen

Eine neue Datei wird bei ihrer Verantwortung einsortiert, ihr Make-/Workflow-Aufrufer aktualisiert und über `Path(__file__).resolve()` oder ein aus `dirname -- "$0"` abgeleitetes `SCRIPT_DIR` lokalisiert. Keine Workspace-spezifischen Pfade, keine Duplikate eines `lib/`-Helfers und keine neue Runtime-Capability in dieser organisatorischen Änderung hinzufügen.
