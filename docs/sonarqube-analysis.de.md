# SonarQube-Cloud-Analyse

**Sprache:** [English](sonarqube-analysis.md) | Deutsch

## Projekt und Analysemethode

Das Parent-Repository verwendet ein SonarQube-Cloud-Projekt,
`Easton97-Jens_ModSecurity-conector`, in der Organisation `easton97-jens`. Der
Organization-Key wurde aus der authentifizierten Projekt-API gelesen und nicht
aus dem GitHub-Kontonamen abgeleitet. Jede Standardvariante analysiert dieselben gepflegten
Parent-Komponenten. Framework und MRTS bleiben eigenständige Repositories und
Analysegrenzen.

Diese vier ähnlich benannten Mechanismen unterscheiden sich:

| Mechanismus | Konfiguration und Entscheidung |
| --- | --- |
| Cloud Automatic Analysis | Läuft auf Sonars Infrastruktur; liest `.sonarcloud.properties`, ignoriert `sonar-project.properties` und kann keine Coverage importieren. Für dieses Projekt deaktiviert lassen. |
| CI-basierte SonarScanner-CLI-Analyse | Gewählte Methode: `.github/workflows/sonarqube.yml` führt drei vollständige Parent-Scans mit derselben `sonar-project.properties` aus. |
| Automatische CLI-Konfiguration | `sonar.scanner.autoconfig.enabled=false` erhält die explizite Source-/Testzuordnung. Aktivierung würde die manuellen Source-/Testeinstellungen ignorieren und Warnungen erzeugen. |
| CFamily AutoConfig / Compilation Database | C/C++-Analyzermodi innerhalb des CI-Scans. AutoConfig leitet Compileroptionen ab; Compilation Database liest echte Buildbefehle über `sonar.cfamily.compile-commands`. Dieses Projekt wählt AutoConfig. |

Der Workflow pinnt die offizielle Scan-Action auf
`d209202bc7d53ff1cc128f7f907dac145c9d6ae9` (`v8.3.0`) und wählt explizit
SonarScanner CLI `8.2.0.6438`. Die Scanner-Signaturprüfung bleibt aktiviert.
Die Scanner-Konfiguration ist manuell; CFamily AutoConfig bleibt unabhängig von
`sonar.scanner.autoconfig.enabled`.

Die authentifizierte Bestandsaufnahme am 2026-10-25 fand Cloud Automatic Analysis
explizit deaktiviert und die automatische CLI-Konfiguration über den wirksamen
Standardwert deaktiviert. Eine frühere Standardbranch-Analyse desselben Tages
verwendete automatische Analyse mit Scanner `7.2.0.5079` und meldete beide
Warnungen zu fehlender Python-Version und fehlendem Test-Scope. Diese
historischen Ergebnisse validieren die neue Konfiguration nicht. Bestehende kanonische Projekteinstellungen, Regeln, Profile und Quality Gates
bleiben unverändert; die beiden neuen ungebundenen Advisory-Projekte sind unten beschrieben.

## Sprach- und Komponentenbestand

Der anfängliche Source- und Test-Scope beginnt jeweils bei `.`. Eng gefasste
Test-Inklusionsmuster unterscheiden die Kategorien; Sonar verwendet diese Muster
zusätzlich als Source-Ausschlüsse. Pfade werden relativ zur Repository-Wurzel
ausgewertet. Anfängliche Scope-Pfade enthalten keine Wildcards; die
Inklusions-/Exklusionsparameter unterstützen Muster.

| Sprache / Analyzer | Gepflegte Komponenten | Source-/Testzuordnung | Buildinformationen und Grenzen |
| --- | --- | --- | --- |
| Python | `ci/`, `scripts/`, `common/`, Connector-Werkzeuge, getracktes `.codex/bin/`, `tests/` | Python-Dateien unter `tests/`, verteilte Connector-Testmodule und deren Testhilfen sind Tests; Betriebswerkzeuge bleiben Sources. | `.python-version` pinnt `3.14.7`; `sonar.python.version=3.14` verwendet Sonars erforderliches Haupt-/Nebenversionsformat. |
| Go | `connectors/envoy/ext_proc`, `connectors/traefik/native_middleware`, `connectors/traefik/composite_middleware`, `connectors/traefik/response_observer` | `**/*_test.go` sind Tests; andere Go-Dateien und jede `go.mod` bleiben im Source-Scope. | Vier Module; `.go-version` ist `1.27.1`, die Modul-Sprachdirektiven sind `1.26.5`. Coverage muss innerhalb jedes Moduls erzeugt werden. |
| C / C++ | `common/`, alle sechs Connector-Familien, `tests/`, `fuzz/` | Sämtlicher C/C++-Code einschließlich Tests, Fixture-Modulen und Fuzz-Harnesses bleibt Source-Code, weil CFamily `sonar.tests` nicht unterstützt. | AutoConfig analysiert Translation Units im Scope; Header benötigen eine einbindende Translation Unit. Der gezielte Evaluator verwendet C++17. |
| Shell | `ci/`, `scripts/`, `common/`, Connector-Build-/Harness-Skripte | Gepflegte `.sh`-Skripte bleiben Sources, einschließlich Skripten in Connector-Verzeichnissen namens `build/`. | Bash/POSIX unterstützt. Die automatische Erkennung von `connectors/apache/build/apxs-wrapper.in` ist nicht nachgewiesen; ein Scope-Eintrag allein beweist keine Shell-Analyse. |
| GitHub Actions | `.github/workflows/` und zutreffende Action-Definitionen | Echte Workflows sind Sources; absichtlich ungültige Workflow-Fixtures sind Testdaten. | Eigener Actions-Analyzer; generisches YAML ersetzt keine Workflow-Semantik. |
| JSON / YAML | `config/`, Beispiele, Workflow- und Laufzeitkonfiguration | Gepflegte Konfiguration bleibt im Scope; negative Fixture-Verzeichnisse sind Testdaten. | Die Sprach-API führt beide Analyzer auf. `sonar.featureflag.cloud-security-enable-generic-yaml-and-json-analyzer=true` aktiviert ihr dokumentiertes Opt-in; die Ausführung in Scanner-Logs bestätigen. Generische Analyse versteht nicht jedes hostspezifische Schema oder eingebettete Sprache. |
| Weitere Formate | Host-`.conf`/`.cfg`, `.yaml.in`, Make/Autotools, TOML, Markdown, Patches | Bleiben enthalten, soweit nachfolgend nicht konkret ausgeschlossen. | Keine Behauptung einer eigenen semantischen Analyse dieser Formate. Secrets-/Textprüfung ersetzt, soweit zutreffend, keinen Sprach-Analyzer. |

Der Bestand bei Basis `9913026c1feec85a1862d22987689a1ebcef6d97` umfasste 398
Python-, 135 C-, eine C++-, 103 `.h`-, acht `.hpp`-, 51 Go- (23 Go-Testdateien)
und 100 `.sh`-Dateien. Die Zahlen beschreiben getrackte Parent-Dateien und keine
serverseitig bestätigten analysierten Dateien. Es wurden keine generierten
Go-Quellen oder vendorten Quellverzeichnisse gefunden. Künftige Dateizahlen
müssen aus dem aktuellen Checkout abgeleitet werden statt diese Momentaufnahme
zu übernehmen.

## Scope-Ausschlüsse und Standards

| Bereich | Begründung und Behandlung |
| --- | --- |
| `modules/ModSecurity-test-Framework/**` | Eigenständiges Git-Submodul einschließlich verschachteltem MRTS; die Parent-Analyse importiert oder ändert seinen Code nicht. |
| `reports/testing/generated/**` | Generierte Evidence; gepflegte Generatoren bleiben im Scope. Andere Berichte und Attributionsdateien werden nicht explizit ausgeschlossen. |
| `build/**`, `dist/**`, `ci-artifacts/**`, `verified-runs/**`; lokale Ausgaben und Caches | Root-`/build/`, `/dist/`, `/compile_commands.json`, Umgebungen, Dependency-Caches und Laufzeitausgaben sind bereits SCM-ignoriert. SCM-Ausschlüsse aktiviert lassen. |
| Python-/Go-Test-Inklusionsmuster | Klassifikation entfernt diese Dateien aus der Source-Indizierung und vermeidet doppelte Indizierung; sie entfernt sie nicht aus der Analyse. |
| `tests/fixtures/python-version-contract/*.yml`, `tests/fixtures/python-version-contract/*.yaml`, `ci/fixtures/zizmor/*.yml`, `ci/fixtures/workflow-permission-contract/*.yml` | Ungültige/unsichere Workflow-Beispiele und ihre Kontrollen sind Testdaten statt ausführbarer Produktionsworkflows. Nur diese YAML-Dateien sind ausgeschlossen; Python-/C-Fixtures bleiben im Scope. |

Kein `**/build/**` hinzufügen: Das würde gepflegte Connector-Buildskripte
verbergen. Kein Connector und keine vollständige Sprache wird zum Unterdrücken
von Findings ausgeschlossen. Der Go-Analyzer schließt `vendor` standardmäßig
aus; es wurde kein solches gepflegtes Verzeichnis gefunden. Scanner-Standards,
SCM-Ignorierungen, Dateisuffixe, Größenlimits, geerbte globale Einstellungen und
nicht eingebundene Header können die tatsächlich analysierte Menge weiterhin
reduzieren. Scanner-Logs und serverseitige Datei-/Sprachmetriken prüfen, statt
anfänglichen Scope mit bestätigter Analyse gleichzusetzen. CI-Kommandozeilenwerte
überschreiben Konfigurationsdateiwerte, die wiederum Projekt-UI-Werte
überschreiben; bei fehlenden Dateien auch Organisations-/Globalausschlüsse prüfen.

## CFamily-Buildtreue

Der getrackte Parent-Bestand bei `9f44647593bac7947113558c6ad183ab118e80af`
enthält 136 native Translation Units: 135 C und eine C++. Dazu gehören native
Tests, Fixtures, Fuzz-Code und CI-Probes. Die bestehenden Targets
`make compile-db-nginx-c17` und `make compile-db-cpp17` erfassen nur die
NGINX-/Common-Deklaration und den gezielten Evaluator. Diese unvollständigen
Datenbanken würden andere Parent-Units aus der CFamily-Analyse entfernen.
AutoConfig und die Datenbankbeschränkung des Scope-Guards bleiben deshalb bis
zum Nachweis eines echten vollständigen Parent-Buildvertrags bestehen.

| Komponente | Realer Buildkontext, den eine vollständige Datenbank erhalten muss |
| --- | --- |
| Common | `ci/checks/common/check-common-helpers.sh` kompiliert alle 58 `common/src/*.c` und führt Helper-, Konstruktor- und Interventionstests aus. |
| NGINX | `make check-nginx-c17` benötigt konfigurierte Host-Header einschließlich `objs/ngx_auto_config.h`, ModSecurity-Header sowie Connector-/Common-Include-Pfade. |
| Apache | `make check-apache-c17` bezieht reale Optionen aus `apxs` und der APR-Konfiguration und kompiliert die fünf Connector-Sources sowie den deklarierten Common-Teil. |
| HAProxy | Die C17-Source-Prüfung erfasst den HTX-Filter nicht. `connectors/haproxy/htx-overlay/build-overlay.sh` baut ihn in einem echten Host-Baum mit Host-Defines und ModSecurity. |
| Envoy | Connector-/Composite-Service-Builds verwenden C17, pthread und ModSecurity; `ext_proc` verwendet den CGo-Build-Tag `libmodsecurity` und seine Common-Runtime-Bridge. |
| Traefik | Engine-Service-Builds verwenden C17, pthread und ModSecurity mit dem C++-Linker. Der Starter behält seinen eigenen C99-Vertrag. |
| lighttpd | Modul-Builds benötigen die generierte `config.h`, `HAVE_CONFIG_H`, Host-API-Defines und gepinnte Host-Header. Stock-Sidecar und gepatchter nativer Kontext bleiben getrennt. |

Der bestehende HTX-Build kopiert Parent-Sources in einen externen Host-Worktree.
Eine naive Erfassung zeichnet diese kopierten Pfade auf, die nicht den
Parent-Source-Pfaden entsprechen. Eine Zuordnung muss identischen Source-Inhalt
bei Erhalt der tatsächlichen Compilerargumente und Header nachweisen;
erfundene Compilerzeilen sind nicht zulässig.

CI installiert die bestehenden Apache-/APR-Header-Voraussetzungen und
kompiliert eine C17-Header-Probe.
`ci/checks/analysis/prepare-sonar-native-context.py` bereitet echte gepinnte
NGINX- und HAProxy-Sourcebäume sowie den kanonisch gepatchten lighttpd-Baum vor,
führt die tatsächlich erforderlichen Configure-/Autogen-Schritte aus und
zeichnet Archiv-, Patch-, Konfigurations- und generierte Header-Hashes auf.
Die unterstützten Einstellungen `sonar.cfamily.customCIncludes` und
`sonar.cfamily.customCppIncludes` verwenden diese Hostpfade neben `/usr/include`,
`/usr/include/apache2` und `/usr/include/apr-1.0`.

Die Entwicklungskorrektur vom 2026-10-26 bezieht außerdem offizielle öffentliche
ModSecurity-Header aus der durch den gepinnten Framework-Vertrag freigegebenen
Version und ordnet sie vor den Distributionsheadern ein. Dem Distributions-SDK
`3.0.12` fehlen Cleanup-APIs des unveränderten C++-Evaluators; eine tatsächliche
negative Syntaxprobe bestätigte diesen Versionskonflikt. Die freigegebenen
Header von `3.0.17` bestanden die entsprechende Syntaxprobe. Das echte
NGINX-Abhängigkeitsverzeichnis `src/http/v2` wird eingebunden, ohne
Feature-Defines zu erfinden oder das konfigurierte Hostprofil zu ändern.
Die vollständige Entwicklungsvorbereitung bestand mit 13 Include-Verzeichnissen
und 11 generierten/Source-Hashes. Das belegt die Header-Vorbereitung und die
ausgewählte Compilerprobe; verbleibende Parsing-/Include-Zahlen müssen neue
Scannerdiagnosen feststellen. Gehostetes Laufzeitverhalten ist damit nicht belegt.

Header werden über einbindende Translation Units analysiert. CFamily nimmt für
projektweite Betrachtungen ein gemeinsam gelinktes Target an, während dieser
Parent unabhängige Connector-Executables enthält. AutoConfig und mehrere Codevarianten unterstützen zudem
keine C/C++-Taintanalyse. Ein höherer Qualitätswert oder der C++-Reporting-Standard
beweisen deren Ausführung nicht. Eine spätere Datenbankstrategie muss jede
vorgesehene Unit und den benötigten Host-/Profilkontext erhalten und die
unabhängigen Targets berücksichtigen; siehe [Buildanleitung](build/README.de.md).

## Repositoryweite C++-Standard-Scans

Der Workflow führt den vollständigen Parent-Source-/Test-Scope dreimal aus.
Höhere Standards werden nicht auf Evaluator, Connector oder C++-Dateien
begrenzt. Python, Go, C, Shell, Actions, JSON und YAML behalten in jeder Variante
dieselbe Konfiguration und dieselben Coverage-Erzeuger. Das dokumentierte
`sonar.cfamily.reportingCppStandardOverride` von CFamily AutoConfig wählt C++17,
C++20 oder C++23 für Regelanwendbarkeit und standardabhängige Vorschläge.
Andere Sprachen behalten ihre eigenen Sprachverträge; dies ist statische Analyse
und kein nativer Compiler-Build.

| C++-Ziel | Sonar-Projekt | Entscheidung |
| --- | --- | --- |
| `c++17` | `Easton97-Jens_ModSecurity-conector` | Verbindliches kanonisches PR-/Hauptbranch-Ergebnis. |
| `c++20` | `Easton97-Jens_ModSecurity-conector_cpp20_advisory` | Unverbindliches vollständiges Parent-Ergebnis. |
| `c++23` | `Easton97-Jens_ModSecurity-conector_cpp23_advisory` | Unverbindliches vollständiges Parent-Ergebnis. |

Die beiden öffentlichen Advisory-Projekte wurden in `easton97-jens` manuell
angelegt und als ohne DevOps-Repository-Bindung sowie mit bereits deaktivierter
Automatic Analysis bestätigt. Sie verwenden explizit ihren eigenen
Analysebranch `master` und vermeiden automatische PR-Zuordnung. Sie können das
PR-Ergebnis des kanonischen Projekts nicht ersetzen. Ihre relevanten
Quality-Profile-Keys und das `Sonar way` Quality Gate stimmen mit dem kanonischen
Projekt überein; Regeln, Profile oder Schwellen wurden nicht abgeschwächt.
C++20/23 werden weniger vollständig als C++17 unterstützt; Analyzer-Grenzen und
Fehler bleiben sichtbar.

Nur die beiden höheren Standards verwenden über die feste Matrix
`continue-on-error: true`; `fail-fast: false` erhält alle Läufe. Jeder Scanner
wartet weiterhin auf sein echtes serverseitiges Gate. Die bilinguale
Jobzusammenfassung protokolliert tatsächliches Scanner-/Gate-Ergebnis, Revision,
Projekt und Compute-Engine-Task-Link einschließlich Fehlern. Advisory-Projekte
enthalten den letzten serialisierten Snapshot je Standard; beim Vergleich von
PRs jede Task-/Analyse-ID und den exakten SHA aufbewahren. Nur das maßgebliche
Projekt behält normale PR-Dekoration. Die ersetzten reinen Evaluator-Compiler-
Jobs sind entfernt.

## CI, Tests und Coverage

Der Workflow checkt `${{ github.event.pull_request.head.sha || github.sha }}`
mit vollständiger Historie aus und verwendet diese Revision für
`sonar.scm.revision`. Das bestehende `SONAR_TOKEN` steht nur dem Scanner-Schritt
zur Verfügung. Fork-PRs erhalten es nicht; es wird keine privilegierte
`pull_request_target`-Ausführung eingeführt.

Testklassifikation, Testausführung, Coverage-Erzeugung und Analyzer-Import
bleiben getrennte Vorgänge. `ci/checks/analysis/run-sonar-coverage.py` erzeugt
echte Reports in frischen Sprachverzeichnissen unter einer externen
`--output-root`. Das Werkzeug erfasst den SHA, prüft die Stabilität des Checkouts
und verlangt für CI einen sauberen Checkout. `--allow-dirty` dient nur der
lokalen Entwicklung und kennzeichnet Reports mit nicht committeten Änderungen.
Leere Ersatzreports oder Coverage-Ausschlüsse verdecken keine
Produktivcode-Lücken. Eine kurze externe `--temp-root` vermeidet
Unix-Socket-Pfadgrenzen in Tests.

Python verwendet die bestehende Hash-gepinnte Dependency `coverage==7.17.0` in
einer isolierten Umgebung unter `$RUNNER_TEMP/sonar-python`.
`ci/sonar-coverage.ini` misst produktiven Parent-Python-Code im gesamten
Repository einschließlich Namespace-Verzeichnissen und Subprozessen mit
relativen Dateipfaden. Die Auslassungen folgen den Grenzen eigenständiger
Repositories, Tests und generierter Ausgaben. Explizite Scope-, Provenienz-,
Artefakt- und Report-Sicherheitstests wählen aussagekräftiges Verhalten aus;
der Bestand `PYTHON_TESTS` im Helper ist für diese Prüfung maßgeblich. Die
XML-Validierung verlangt tatsächliche Ausführung und auflösbare
Repository-Dateien und normalisiert die Source-Wurzel auf `.`, ohne Zähler zu
verändern.

Go verwendet 37 benannte Lifecycle-/Sicherheitsszenarien aus dem Helper-Bestand
`GO_TESTS`. Jedes Modul führt `-mod=readonly -coverpkg=./... ./...` aus und erhält
nicht ausgeführte Pakete des Standard-Builds in der Messung. `go tool cover`
validiert jeden Report. Fehlende ausgewählte Testnamen führen sichtbar zum
Fehler.

| Modul | Report unter `$RUNNER_TEMP/sonar-coverage/go` |
| --- | --- |
| `connectors/envoy/ext_proc` | `envoy.out` |
| `connectors/traefik/native_middleware` | `traefik-native.out` |
| `connectors/traefik/composite_middleware` | `traefik-composite.out` |
| `connectors/traefik/response_observer` | `traefik-observer.out` |

Native Coverage stammt aus den bestehenden Common-Helper-, Konstruktor- und
Interventionstests, kompiliert mit
`-std=c17 -Wall -Wextra -Werror --coverage -O0`. Tatsächliche
`.gcda`-Ausführungszähler sind erforderlich. Das passende GCC-`gcov` erzeugt
individuelle Reports pro instrumentiertem Objekt, damit getrennt kompilierte
Binärdateien ihre Messungen nicht überschreiben. Alle 58 Common-C-Source-Dateien
müssen vertreten sein; Connector-Host-Runtime-Coverage wird nicht daraus
abgeleitet.

Auch die Go- und nativen Producer-Prozesse laufen unter Python-Coverage.
`--language finalize-python` gleicht alle drei Sprachmanifeste mit demselben
SHA ab, kombiniert Subprozessdaten mit `--append` und erzeugt sowie validiert
das Python-XML erneut. Der Scanner importiert `python/python.xml`, die vier
Go-Reports und `native/gcov` über `sonar.python.coverage.reportPaths`,
`sonar.go.coverage.reportPaths` beziehungsweise `sonar.cfamily.gcov.reportsPath`.
Erst frisches Scanner-Readback belegt den erfolgreichen Import.

Entwicklungsläufe meldeten 185 produktive Python-Dateien einschließlich ehrlicher
Nullwerte sowie 71 gcov-Reports über 62 Repository-Dateien einschließlich aller
58 Common-C-Dateien. Die ausgewählten Go-Tests bestanden mit Modul-Coverage von
27,5 %, 65,3 %, 69,0 % und 61,6 % in Tabellenreihenfolge. Wiederholte
Go-Blockzeilen verschiedener Testbinärdateien müssen zusammengeführt statt
addiert werden. Diese Beobachtungen verwendeten lokal Python `3.14.4` und Go
`1.27.3`; CI bleibt auf Python `3.14.7` und Go `1.27.1` gepinnt. Das sind
Entwicklungsnachweise, kein Import- oder Gate-Nachweis des finalen Commits.

Die Auswahl führt nicht jeden Parent-Test, jede Plattform,
Go-Integration mit dem Tag `libmodsecurity` oder jede Connector-Runtime aus.
Sie belegt nicht, dass das repositoryweite Ziel einer kompakten Standardsuite
bereits technisch erzwungen wird. Es werden keine Testausführungsreports
importiert; die Coverage-Schwellen bleiben unverändert.

## Sicherheit von Evidence-Eingaben

Die Basisabfrage lieferte 46 offene Vulnerability-Findings. Die Triage fand für
14 konkrete Kontrollen oder beabsichtigte Operatorberechtigung; die übrigen 32
verfolgen Pfade aus Dateiinhalten, die auf Aufruferseite validiert werden müssen.
Ein Rating allein beweist keine Sicherheitslücke. Kein Finding wurde allein für
ein anderes Gate akzeptiert, unterdrückt oder als False Positive umgestellt.

Bestätigte Lücken umfassten JSON-ausgewählte private Job-Summaries, gespeicherte
Refresh-Logs, NGINX-Report-Auszüge und manifestgewählte Cache-Hashes. Evidence
darf sich nicht selbst Zugriff auf einen anderen Hostpfad erteilen. Consumer
binden Lesezugriffe an die vertrauenswürdig konfigurierte Aufrufwurzel und
verwenden Deskriptoren regulärer Dateien ohne Linkverfolgung. Kanonische
schreibgeschützte Source-Fixtures und explizit konfigurierte externe
Runtime-/Cache-Pfade bleiben getrennte zulässige Eingaben. `build_root` oder
`log_root` aus Reports dürfen die Allowlist nicht erweitern. Die konkret
geänderten Consumer, Regressionsnachweise und verbleibenden Grenzen stehen im
[Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.de.md).
Für den scannerseitigen Abschluss ist frisches Sonar-Finding-/Rating-Readback
weiterhin erforderlich.

Cache-Nachweise akzeptieren einen finalen SONAME-Alias nur, wenn dessen physisches Ziel unabhängig im konfigurierten Cache oder als exakt freigegebene Datei autorisiert ist. Der normale Komponenten-Producer übergibt seine vertrauenswürdig konfigurierten Overrides an `update-runtime-reports.py --approved-component-file`; direkte Aufrufe können diese Option für explizit gewählte installierte Dateien wiederholen. Ein Manifest kann sich keine Datei oder Wurzel selbst freigeben. Abgewiesene Referenzen behalten den sichtbaren Status `rejected` ohne Digest.

## Validierung und Wartung

Der Workflow folgt der [offiziellen Scan-Action-Schnittstelle](https://github.com/SonarSource/sonarqube-scan-action#configuration): `scannerVersion=8.2.0.6438`, unterstützte `args`, vollständige Checkout-Historie und standardmäßige OpenPGP-Prüfung. Report-Properties verwenden Pfade relativ zur Projektwurzel, berechnet aus dem externen Runner-Verzeichnis; die Reports selbst bleiben außerhalb des Checkouts.

| Sprache | Angewandter Dokumentationsvertrag |
| --- | --- |
| C / C++ | Unterstützte AutoConfig-Include-Einstellungen und nativer `.gcov`-Import; partielle Compilation Databases ersetzen nicht den vollständigen Parent-Scope. AutoConfig kann keine C/C++-Taintanalyse liefern. |
| Go | Die gepinnte Go-1.27-Toolchain wird unterstützt. Jedes Modul behält sein `go.mod`, die `*_test.go`-Klassifizierung und vor dem Scan erzeugte Standardreports aus `-coverprofile`. |
| Python | `sonar.python.version=3.14` verwendet Major.Minor; echte Cobertura-XML nutzt relative Quelldateinamen sowie Branch- und Subprozess-Messung. |
| Shell | Bash und POSIX sind die offiziell unterstützten Dialekte. Tatsächliche Shebangs, `.sh`-/`.bash`-Quellscope und Verhaltensprüfungen erhalten; lokale Syntaxerfolge beweisen kein Sonar-Parsing. |
| Workflows / JSON / YAML | Dedizierte Actions-Analyse und dokumentiertes generisches JSON-/YAML-Opt-in bleiben aktiviert; negative Workflow-Fixtures behalten ihre eng begrenzte Behandlung. |

Bei Änderungen an `.python-version` im selben Change `sonar.python.version` auf
den Haupt-/Nebenversionswert aktualisieren, wenn sich die Minorversion ändert; reine Patch-Updates erhalten ihn. Bei Updates von `.go-version` oder
`go.mod` alle Module erneut prüfen; jeden Moduldeskriptor im Source-Scope halten.
Beim Hinzufügen von Tests oder Fixture-Verzeichnissen die Klassifikationsmuster
prüfen, ohne CFamily-Dateien in den Test-Scope zu verschieben. Die
Sonar-Konfigurationsvalidierung des Repositorys sowie die bilingualen
Dokumentations-/Linkprüfungen über den erforderlichen lokalen Ausführungswrapper
ausführen; tatsächliche Ergebnisse im Change Record festhalten:

```sh
rtk bypass .venv/bin/python ci/checks/analysis/check-sonar-scope.py --json
rtk bypass .venv/bin/python -m unittest -v tests.test_sonar_scope
rtk make check-bilingual-docs
rtk make check-doc-links
```

Der Scope-Checker vergleicht die Python-Minorversion, schützt gepflegte
JSON-/YAML-Dateien und echte Workflows unabhängig, erhält Connector-Buildskripte,
C/C++-Test-Sources sowie die verteilte Python-/Go-Testklassifikation, prüft alle
vier `go.mod`-Dateien und gibt vollständige getrackte Pfadlisten aus. Nur die
bestehenden unmittelbaren Verzeichnisse negativer Workflow-Fixtures werden
explizit getrennt behandelt. Eine README ersetzt keinen analysierbaren
Komponentencode und keine Konfiguration. Er beweist keine Scanner-Ausführung und
bildet nicht jeden SCM-/Analyzer-Standard nach. Der zentrale Workflow-/Tool-Updater
pflegt den Scan-Action-Pin; die explizite `scannerVersion` bei Änderungen am
Scanner CLI separat prüfen.

Vor dem Aktivieren oder erneuten Ausführen der CI prüfen, dass Administration →
Analysis Method Automatic Analysis weiterhin deaktiviert hat. Wurde es erneut
aktiviert, muss ein berechtigter Projektadministrator es vor dem CI-Scan
deaktivieren; niemals beide Modi parallel betreiben. Bestätigen, dass das
vorhandene `SONAR_TOKEN` Analysen ausführen darf. Diese Repository-Änderung
impliziert weder Secret-Rotation noch externe Einstellungsänderungen.

Für den tatsächlichen PR-Head Commit-SHA, Scannerversion, Compute-Engine-Task-ID
und Analyse-ID aufbewahren. Das Ende der Serververarbeitung abwarten und dann
das Quality Gate genau dieser Analyse zurücklesen. Die resultierenden Warnungen
auf die beiden ursprünglichen Python-Meldungen sowie neue Warnungen zu
ignorierten Parametern, Source/Test, AutoConfig oder fehlenden Berichten prüfen.
Ein erfolgreicher Upload, eine lokale Scope-Prüfung, historische Analyse oder
ein bestandenes Gate einer anderen Revision ist diese Bestätigung nicht.
Verbleibende Findings und ein unzugängliches/ausstehendes/fehlgeschlagenes Gate
sichtbar lassen; niemals Regeln oder Schwellen für ein Bestehen abschwächen.

## Beobachtete Cloud-Grenzen und externe Folgeaktion

Der [PR-#421-Abschlussnachweis](sonarqube-pr421-closeout.de.md) dokumentiert die
unabhängigen Einzelentscheidungen, Marker-Korrektur, echte gepinnte
Host-Header-Vorbereitung, den Vergleich der Analyzergrenzen mit der Basis und
finale Runtime-Nachweise. Seine revisionsgebundenen Ergebnisse und externen
Schritte ergänzen die historischen Beobachtungen unten; PR-Coverage qualifiziert
nicht die kumulierte Master-Coverage.

Authentifiziertes Readback bestätigte erneut die Basisrevision
`9f44647593bac7947113558c6ad183ab118e80af`, Analyse
`52df415d-2c24-43a3-a63a-de6e79c37d60`, aus
[Lauf 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735).
Das Hauptgate war `ERROR`: Security Rating E auf neuem Code und 0,6 % Coverage
bei Schwellenwerten A und 80 %. Der Zeitraum `previous_version` beginnt am
2026-05-14. Das paginierte Datei-Readback enthielt 663 Dateien und folgende neue
abdeckbare Zeilen: Python 57.281; C 27.420; C++ 184; Go 6.284. Diese kumulierte
Hauptbranch-Basis unterscheidet sich vom Gate über geänderte PR-Zeilen. Ein
grüner PR darf nicht als behobene kumulierte Hauptbranch-Coverage gelten.

Die Basis verwendete Scanner CLI `8.1.0.6389` und CFamily `6.85.0.102562` und
meldete 136 native Units, Qualität 77,52/100, Parsingfehler in 414/2.260
Funktionen und 115/1.132 unaufgelöste projektbezogene Includes. AutoConfig
deaktivierte die C/C++-Taintanalyse. Python-, Go-, CFamily-, Shell-, GitHub-Actions-,
YAML- und JSON-Sensoren liefen; die ursprünglichen Warnungen zu fehlender
Python-Version und Testzuordnung fehlten. Das sind Basisbeobachtungen, keine
Ergebnisse eines späteren SHA.

Der erste abgeschlossene PR-Scan von `13b17cbedaa8b7d7fe382ae500052f1cac4ded16`
verwendete Scanner `8.2.0.6438` und CFamily `6.85.0.102562`.
[Lauf 40231379831](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40231379831)
importierte echte Python-, Vier-Modul-Go- und Common-gcov-Reports. Servertask
`AaF0ymveZaGJAnPJkdcR` endete mit `SUCCESS`, Analyse
`d812ee4b-6300-430f-89e9-11f7eb7b7745`. Das PR-Gate blieb allein wegen
Security Rating E auf `ERROR`: drei `S2083`-Findings an den Opens des
Deskriptor-Readers. Die unabhängige Angriffs-/Kontrollprüfung bestätigte Wurzel-,
No-follow- und Deskriptorkontrollen; es gab keine Finding-Transition. Die
Coverage auf neuem Code betrug 80,5 % und bestand die 80-%-Schwelle. Beide
Advisory-Scans hatten fehlgeschlagene Gates. Alle 136 nativen Units blieben
analysiert; die Qualität stieg auf 91,28/100, mit Parsingfehlern in 193/2.260
Funktionen und 46/1.132 unaufgelösten Projekt-Includes (zuvor 115).
Fehlende Host-/Buildheader für NGINX, HAProxy und lighttpd sowie
die AutoConfig-Taintgrenze bleiben bestehen. Der Change Record enthält die
vollständige Basis-Finding-Einordnung und Messergebnisse; Folge-Heads müssen
separat im PR geprüft werden.

Der Folgescan von `8f632bdd` in [Lauf 40232441972](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40232441972)
beendete ebenfalls die Serververarbeitung und bestätigte die verschwundene
Resolver-Warnung. Fünf ursprüngliche Shell-Warnungen sind damit behoben; die
gültige Scheduler-FIFO-Form bleibt die einzelne dokumentierte Shell-Parsergrenze.
Gate und Coverage bleiben ERROR/E und 80,5 %. Ergebnisse des finalen reinen
Dokumentations-Folgecommits stehen in PR #421.

Die folgende Tabelle dokumentiert historisch `13b17c` / `8f632bdd` und ist
keine aktuelle Finding-Inventur. Die vollständige Fortsetzung vom 2026-10-26
unten und der [Abschlussnachweis](sonarqube-pr421-closeout.de.md) ersetzen
die damaligen offenen Finding-Entscheidungen.

| Ausgangsbefund | Historische Einordnung dieser Heads |
| --- | --- |
| Haupt-Security-Rating E | `weiterhin offen`: Sourcekorrekturen haben Regressionstests; das PR-Gate bleibt wegen drei geschützter Deskriptor-Opens auf E. Gegennachweise sind ohne Server-Transitions dokumentiert. |
| Haupt-Coverage auf neuem Code 0,6 % | PR-Import bei 80,5 % `behoben und nachgewiesen`; kumulierte Master-Coverage bis zu einer entsprechenden Hauptanalyse `weiterhin offen`. |
| Fehlende native Includes / Parsingfehler | Gemessene Verbesserung auf Qualität 91,28 und Fehler in 193/2.260 Funktionen; verbleibende Hostkontexte `weiterhin offen`. |
| Vollständige Parent-C/C++-Taintanalyse unter AutoConfig | `begründete Analyzergrenze`: nicht unterstützter Modus und Annahmen zu unabhängigen Targets bleiben ausdrücklich bestehen. |
| Ignoriertes beabsichtigtes Python-Modell | `extern blockiert`: genaue Modellkorrektur liegt vor; der nötige PATCH-Medientyp wird von der autorisierten CLI nicht unterstützt. |
| Verlust von JSON-/YAML-/Workflow-Scope | `behoben und nachgewiesen`: gezielte lokale Regressionen beweisen den Guard; Analyzer-Ausführung bleibt eine eigene Prüfung. |
| Sechs Shell-Parserwarnungen | Fünf bei `8f632bdd` `behoben und nachgewiesen`; Scheduler `begründete Analyzergrenze`. |

Jede gemeldete Shell-Datei verwendet `#!/bin/sh` und bestand `sh -n`, `bash -n`
sowie ShellChecks Prüfung auf Fehlerniveau. Dynamische Oktalausdrücke im
Apache-Cleanup wurden auf explizite Oktalvariablen umgestellt. Heredoc-Producer
im Hintergrund in Envoy, lighttpd und HAProxy verwenden nun eine Subshell mit
`exec`, wodurch die Prozessidentität von `$!` erhalten bleibt. HAProxys
Architektur-Case-Muster verwenden einzelne Arme, maskierte Leerzeichen und
explizite No-op-Rümpfe. Das
`exec 8<>"$candidate"` des Schedulers erhält die erforderliche
Lese-/Schreib-FIFO-Semantik.

| Datei | Lokale Klassifikation und Änderung |
| --- | --- |
| `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh` | Gültige POSIX-Oktalarithmetik; explizite Oktalvariable erhält Berechtigungsmasken. Warnung bei `13b17c` verschwunden. |
| `connectors/envoy/harness/run_envoy_composite_matrix.sh` | Gültiger Hintergrund-Heredoc; Subshell plus `exec` erhält Argumente, Umleitungen und PID. Warnung bei `13b17c` verschwunden. |
| `ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Gültige Lese-/Schreib-FIFO-Umleitung; unverändert, weil getrennte Opens das Blockier-/EOF-Verhalten ändern. Warnung bei `13b17c` besteht. |
| `connectors/lighttpd/harness/run_patched_full_lifecycle.sh` | Gültiger Hintergrund-Heredoc; gleichwertige Subshell-/`exec`-Form. Warnung bei `13b17c` verschwunden. |
| `connectors/haproxy/htx-overlay/resolve-modsecurity.sh` | Gültige quotierte Case-Muster bei `13b17c` weiter gemeldet; einzelne Muster mit maskierten Leerzeichen erhalten das Verhalten und beseitigten die Warnung bei `8f632bdd`. |
| `connectors/haproxy/harness/run_haproxy_smoke.sh` | Gültiger Hintergrund-Heredoc; Subshell/`exec` erhält optionales `setsid` und PID. Warnung bei `13b17c` verschwunden. |

Der minimale Parser-Reproduktionsfall des Schedulers lautet:

```sh
#!/bin/sh
prepare() {
    if exec 8<>"$1"; then
        :
    fi
}
```

Dieses FIFO-Open nicht durch getrennte blockierende Opens ersetzen oder seine
Datei ausschließen. Der neue Scan muss die sechs im Change Record genannten
Dateien einzeln bestätigen; lokale Syntaxprüfung allein reicht nicht.

Das Servermodell `py Intended Model` enthält 46 Gruppen auf oberster Ebene.
Seine 44 ungültigen Labels enthalten `/`: 30 gehören zum Parent, 14 verweisen
auf ausgeschlossenes Framework/MRTS. Der genaue überprüfbare Request-Body liegt
unter [`config/analysis/sonar-python-architecture.patch.json`](../config/analysis/sonar-python-architecture.patch.json).
Er entfernt nur diese 14 externen Gruppen, benennt die 30 Parent-Labels mit `_`
um und erhält alle Parent-Muster, Metadaten, vier verschachtelten Gruppen sowie
die bestehende leere Liste `constraints`. Er löscht die Perspektive nicht und
erfindet keine Architektur-Constraints. Beide Advisory-Projekte haben derzeit
keine Modelle.

Hauptprojekt-UUID: `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`; Modell-ID:
`cb04d3a3-7c8f-447c-99f0-ca49c97f054f`. Authentifizierte Lesezugriffe verwenden
`/api/v2/architecture/models?projectId=608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`.
Das autorisierte Update über `/usr/local/bin/sonar-with-env` und CLI `1.10.1`
lieferte HTTP 415:
`PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f`
verlangt `application/merge-patch+json`, diese CLI hat jedoch keine unterstützte
Medientyp-Option. Die effektiven Rollen `architectureadmin`/`admin` waren
vorhanden; anschließendes Readback bestätigte keine Änderung. Der wiederholte autorisierte Request am 2026-10-26 lieferte erneut HTTP 415;
das Readback bestätigte das unveränderte Modell. Die installierte CLI
`1.10.1.16776` ist die neueste veröffentlichte Version. Ihre veröffentlichte
API-Implementierung unterstützt JSON-/Form-Medientypen ohne Header-Override;
Architekturkommandos aus unveröffentlichtem Upstream-Code bieten keinen
unterstützten installierten Zugang. Der genaue geprüfte Body muss über einen
unterstützten autorisierten Client mit diesem Medientyp und Einbindung des
vorgeschriebenen Authentifizierungswrappers angewendet werden. Danach sind die
erhaltenen Parent-Muster, verschachtelten Gruppen und Constraints zurückzulesen
und die Perspektivanwendung durch eine neue Analyse nachzuweisen. Ein geprüfter
UI-Editor-/Importweg wird nicht behauptet. Dieses Dokument erlaubt keinen
Wrapper-, Credential- oder Authentifizierungs-Workaround.

CI-/Sonar-Links des finalen Heads, terminale Verarbeitung, Haupt-/Advisory-Gates,
Sprachausführung, Reportimporte und Nachher-Ergebnisse jeder Warnung müssen nach
der Beobachtung im Change Record festgehalten werden. Ein erfolgreicher Upload,
ein älteres grünes Ergebnis, `warningCount=0` oder die Conclusion eines
Advisory-Jobs allein reichen nicht.

## Vollständige PR-Finding-Fortsetzung, 2026-10-26

Die frisch paginierte Hauptprojektabfrage für PR #421 verwendete
`sinceLeakPeriod=true`, `issueStatuses=OPEN,CONFIRMED` und alle Finding-Typen:
100 plus 50 Ergebnisse, 150 verschiedene Findings. Davon betreffen 122 Shell
und 28 Python: 141 Wartbarkeit, acht Sicherheit und eines Zuverlässigkeit.
Die Legacy-Schweregrade ergeben sechs MINOR, 116 MAJOR, 25 CRITICAL und drei
BLOCKER. Die getrennten Advisory-Inventare im gleichen New-Code-/Status-Scope
enthalten 31 und 16 Findings; das sind nicht die älteren Gesamtzahlen von
27 und 24 Schwachstellen. Die Security-Hotspots des Hauptprojekts wurden
separat geprüft: null.

Der geprüfte Ausgangssource ist `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3`.
Alle drei zugehörigen Servertasks endeten erfolgreich; vor den neuen
Einzelentscheidungen standen ihre Gates auf ERROR. Echte Reportimporte ergaben
82,3 % Haupt-PR-Coverage und 83,7 % Advisory-Branch-Coverage auf neuem Code.
Keiner dieser Werte behebt die kumulierte Master-Coverage. Spätere uncommittete
Entwicklungsänderungen und deren lokale Coverage ersetzen keinen CI-Import
eines sauberen Heads.

Nach unabhängiger Prüfung vollständiger Datenflüsse und Sources sowie
Angriffs-/erlaubten Kontrollen wurde die neue ausdrückliche Nutzerautorisierung
für 21 einzelne `FALSE_POSITIVE`-Transitions mit Finding-spezifischen Kommentaren
verwendet: acht Hauptprojekt, acht C++20 und fünf C++23. Jeder Status und der
zugehörige Kommentar wurden zurückgelesen. Es wurden keine Risiken akzeptiert
und keine Regeln, Profile, Gates oder Schwellen abgesenkt. Diese tatsächlichen
Serverentscheidungen ersetzen die historischen Aussagen ohne Transitions oben;
neue Findings benötigen eine eigene Prüfung. Die 142 Nicht-Sicherheitsfindings
des Hauptprojekts und 23/11 der Advisories sind lokal im Code korrigiert; der
neue Scan steht aus. Benannte POSIX-Funktionsargumente, gleichwertig vereinfachte
Kontrollflüsse und Python-Komplexitäts-/Testkorrekturen erhalten die jeweiligen
Schnittstellen und Sicherheitskontrollen. Tatsächliche Vorher-/Nachher-
Charakterisierungen der Shell und die instrumentierte Python-Auswahl mit
80 Methoden bestanden. Sechs bestehende Envoy- und zwölf HAProxy-ShellCheck-
Warnungen bleiben unverändert; ein insgesamt sauberer ShellCheck-Lauf wird
nicht behauptet. Der Scheduler erhält das FIFO-Verhalten von `exec 8<>`.

Die Architekturanwendung bleibt wie oben beschrieben extern blockiert. Nativer
Scannerabschluss, neue Finding-Zahlen und CI/Sonar des finalen Heads bleiben
offen, bis eine neue saubere Sourcerevision terminale Nachweise für alle drei
Projekte besitzt. Python-Simulationskosten- und Predecessor-Meldungen bleiben
begrenzte Analyzergrenzen mit Basisnachweis. PR #421 bleibt Draft, solange
Pflichtkriterien fehlen. [Change Record](../reports/audits/change-records/CR-20261025-sonar-setup-remediation.de.md)
und [Abschlussnachweis](sonarqube-pr421-closeout.de.md) trennen lokale Korrekturen,
tatsächliche Serverentscheidungen und verbleibende Nachweise. Ein Merge oder
eine Änderung an master wird nicht behauptet.

## Offizielle Referenzen

- [SonarScanner CLI und automatische Konfiguration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/scanners/sonarscanner-cli)
- [Cloud Automatic Analysis](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/automatic-analysis)
- [Anfänglicher Scope](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/setting-initial-scope) und [Pfadmuster](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/project-analysis/setting-analysis-scope/excluding-files-based-on-patterns)
- [CFamily-Modi](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [Konfiguration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis) und [tatsächlicher Analyseumfang](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis)
- [Python](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/python), [Go](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/go) und [Shell](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/shell)
- [GitHub Actions](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/github-actions), [JSON](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/json) und [YAML](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/yaml)
- [Coverage](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/overview) und [Coverage-Importparameter](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/test-coverage-parameters)
- [Gepinnte Scan-Action](https://github.com/SonarSource/sonarqube-scan-action/tree/d209202bc7d53ff1cc128f7f907dac145c9d6ae9)

- [Gepinnte Python-Coverage-Version und Universal-Wheel](https://pypi.org/project/coverage/7.17.0/)
- [Python-Coverage-Import](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/python-test-coverage)

- [Manual project creation](https://docs.sonarsource.com/sonarqube-cloud/managing-your-projects/administering-your-projects/setting-up-project)
- [DevOps binding](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/about-sonarqube-cloud-solution/resources-structure/binding-with-dop)

- [Native C/C++ coverage / Native C/C++-Coverage](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/test-coverage/c-c-objective-c-test-coverage)

- [Scanner CLI 8.2.0.6438](https://github.com/SonarSource/sonar-scanner-cli/releases/tag/8.2.0.6438)
- [CFamily-Taintanalyse](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis#taint-analysis)
- [CLI 1.10.1.16776](https://github.com/SonarSource/sonarqube-cli/releases/tag/1.10.1.16776), [veröffentlichtes API-Kommando](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/commands/api/api.ts), [veröffentlichter HTTP-Client](https://github.com/SonarSource/sonarqube-cli/blob/ef0f792b7c4bb18d2432015baae4984a6cd50d99/src/core/server/http-client.ts)
