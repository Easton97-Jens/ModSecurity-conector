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
SonarScanner CLI `8.1.0.6389`. Die Scanner-Signaturprüfung bleibt aktiviert.
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

Die vorhandenen Targets `make compile-db-nginx-c17` und `make compile-db-cpp17`
erfassen NGINX/Common beziehungsweise den gezielten Evaluator. Sie liefern keine
vollständige Compilation Database aller sechs Familien oder sämtlicher
C-Test-/Fixture-Translation-Units. Eine solche unvollständige Datenbank würde
die Analyse still auf ihre Schnittmenge mit dem Source-Scope verengen.
AutoConfig erhält deshalb den breiteren Parent-Translation-Unit-Scope, ohne
Compilerbefehle zu erfinden oder allein für den Scan Host-Toolchains
hinzuzufügen. Siehe die [Buildanleitung](build/README.de.md).

Aktuelle Buildverträge verwenden überwiegend C17; der gezielte Evaluator
verwendet C++17 und das ältere `connectors/traefik/build/build-starter.sh` C99.
Host-Includes, generierte Header, Feature-Defines, cgo-Flags und optionale
C23-/Future-C-Profile unterscheiden sich je Build. AutoConfig leitet Optionen
ab und beweist keine Übereinstimmung seiner Konfiguration mit jedem Host/Profil.
Der C++-Berichtsstandard ist auf C++17 gepinnt; das steuert die Anwendbarkeit
von Regeln und beweist keinen erfolgreichen C++-Build. Keine exakte
C17-Kompilierungstreue behaupten oder einen gemeinsamen Satz inkompatibler
Host-Makros vorgeben. AutoConfig-Qualitätswarnungen und den Anteil verstandenen
Codes prüfen.

Header werden nur über einbindende Quelldateien analysiert. Mehrere unabhängige
Connector-Binaries werden als ein Projekt dargestellt: CFamily nimmt für
projektweite Analyse ein gelinktes Ziel an. Full-project-Regeln, Taint-Analyse
und Cross-Translation-Unit-Analyse können dadurch Präzision verlieren. Die
beobachtete AutoConfig-Implementierung deaktiviert C/C++-Taint-Analyse und nennt
eine Liste nicht verfügbarer Regeln; dieser Scan liefert keine C/C++-Taint-Abdeckung. Keine
Connector-Teilscans überschreiben das vermeintliche Gesamtergebnis desselben
Projekts. Ein künftiger Datenbankwechsel muss die echten Befehle erfassen, alle
beabsichtigten Translation Units mit den Einträgen vergleichen, erforderliche
Includes/generierte Dateien erhalten und unterstützte Varianten sowie fehlende
Units vor dem Moduswechsel dokumentieren.

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

Der Workflow checkt die analysierte Revision mit vollständiger Git-Historie aus.
Er verwendet den vorhandenen Secret-Namen `SONAR_TOKEN`; die Bestandsaufnahme
bestätigte die Existenz des Secrets, nicht seinen Wert, seine Gültigkeit oder
Analyseberechtigungen. Das Token ausschließlich in der Umgebung des
Scanner-Schritts halten. Fork-Pull-Requests erhalten keine Repository-Secrets;
der privilegierte Scan wird für sie übersprungen, statt nicht vertrauenswürdigen
Code über `pull_request_target` auszuführen.

Testklassifikation, Testausführung, Testausführungsbericht-Import und
Coverageimport sind getrennte Vorgänge. Ein Wert für `sonar.tests` führt keine
Tests aus. Nur für die ausgecheckte Revision erzeugte Berichte dürfen importiert
werden. Coverageberichte müssen existieren, ein unterstütztes Format verwenden
und Dateien unter dieser Projektbasis referenzieren; niemals leere Ersatzberichte
erzeugen. Native C/C++-Coverage wird nicht bereitgestellt. Python-Coverage wird für den
Konfigurationschecker durch Ausführung seiner echten CLI und acht gezielter
Unit-Testmethoden gemessen; das beansprucht keine Ausführung aller Parent-Python-Tests. Bestehende Laufzeittests bleiben getrennte Evidence
und werden durch ein statisches Analyseergebnis nicht impliziert.

Python-Coverage verwendet `coverage==7.17.0` (Apache-2.0, Python >=3.11, keine
Laufzeitabhängigkeiten), in `ci/requirements/sonar-coverage.txt` auf den offiziellen
PyPI-Universal-Wheel-SHA-256 gepinnt. CI erzeugt eine getrennte Umgebung unter
`$RUNNER_TEMP/sonar-python`, installiert ausschließlich Binärpakete mit
verpflichtenden Hashes und verwendet `ci/sonar-coverage.ini` für Branch-Coverage
und relative Pfade. CLI-Check und Unit-Tests erzeugen echte parallele Datendateien,
die zu `$RUNNER_TEMP/sonar-coverage/python.xml` kombiniert und über
`sonar.python.coverage.reportPaths` importiert werden. Das gezielte
Source-Verzeichnis ist `ci/checks/analysis`; seine beiden nicht ausgeführten
vorhandenen Skripte bleiben bei gemessener Null. Keine Coverage-Ausschlüsse oder
leeren Ersatzreports werden verwendet.

CI führt vier vorhandene Einzelszenario-Go-Tests aus, einen je Modul, nachdem
sie die Existenz jedes exakten Testnamens geprüft hat. Native
`go test -coverprofile`-Reports werden unter `$RUNNER_TEMP/sonar-coverage`
geschrieben, innerhalb ihrer Module mit `go tool cover` validiert und über
`sonar.go.coverage.reportPaths` mit ihren vier echten Pfaden importiert.
Das ist bewusst geringe Paket-Coverage:

| Modul | Paket / ausgewählter Test | Report |
| --- | --- | --- |
| `connectors/envoy/ext_proc` | `./internal/responseobserver` / `TestClientFramesBoundedOrderedOperations` | `envoy.out` |
| `connectors/traefik/native_middleware` | `.` / `TestMiddlewareForwardsRequestAuthorityAsHostHeader` | `traefik-native.out` |
| `connectors/traefik/composite_middleware` | `.` / `TestStripInternalHeadersRemovesTrailerForms` | `traefik-composite.out` |
| `connectors/traefik/response_observer` | `.` / `TestResponseHeaderEncodingUsesLengthThenBytesOrder` | `traefik-observer.out` |

Diese vier Fälle prüfen nicht alle Modulpakete, Envoys mit `libmodsecurity`
getaggte CGo-Integration, alternative Plattformen oder jede Connector-Laufzeit.
Es werden keine Testausführungsberichte importiert. Gemessene Null- oder geringe
Coverage bleibt sichtbar; keine Coverage-Exklusion oder Quality-Gate-Schwelle
wird gelockert.

## Validierung und Wartung

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

Der Scope-Checker vergleicht die Python-Minorversion, erhält sämtlichen
gepflegten Code und C/C++-Tests, prüft alle vier `go.mod`-Dateien und gibt
vollständige getrackte Pfadlisten aus. Er beweist keine Scanner-Ausführung und
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

Der erste CI-Scan von `b3c7785fd7033fc57394c1e4562d627e2b294c4f` wurde serverseitig
als Task `AaF0Nx8EdkEpBguA0kbW`, Analyse
`8436e500-b997-4b7a-b428-b577aca20a43`, verarbeitet. Die Server-Warnungsliste war
leer, beide ursprünglichen Python-Konfigurationsmeldungen fehlten. Der Scanner
bestätigte alle 136 CFamily-Compilation-Units als vollständig analysiert, einen
C/C++-Qualitätsscore von 77.52/100, das Laden aller vier Go-Reports sowie die
Ausführung der Python-, Shell-, Actions-, YAML- und JSON-Sensoren. Sein Quality
Gate scheiterte ausschließlich an 0% New-Code-Coverage; dies führte zum echten
Python-Coverage-Erzeuger. Diese Ergebnisse beschreiben die erste Revision; die
PR-Beschreibung enthält Verarbeitungs-/Gate-Evidence des aktuellen Heads.

Scanner-Logs enthalten weiterhin sechs Shell-Parsewarnungen in vorhandenen
Skripten: `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`,
`connectors/envoy/harness/run_envoy_composite_matrix.sh`,
`ci/runtime/lifecycle/run-full-matrix-parallel.sh`,
`connectors/lighttpd/harness/run_patched_full_lifecycle.sh`,
`connectors/haproxy/htx-overlay/resolve-modsecurity.sh` und
`connectors/haproxy/harness/run_haproxy_smoke.sh`. Sie bleiben im Scope; eine
selektierte Datei mit Parsewarnung beweist keine vollständige semantische
Analyse. Go-Testdateien erzeugen nach korrekter Testklassifikation außerdem
informative Warnungen zu ignorierten Duplikationsmeldungen.

Die gespeicherte serverseitige Python-Architekturperspektive `py Intended Model`
enthält 44 ungültige Gruppenlabels einschließlich ausgeschlossener Framework-/
MRTS-Pfade und früherer Test-/Infrastrukturgruppen. Ein Projektadministrator muss
dieses Intended Model prüfen und mit dem Parent-only-Source-/Test-Scope abgleichen.
Dieser Task entfernt das Modell nicht und deaktiviert keine Architekturprüfungen,
um Warnungen zu verbergen. Server-`warningCount=0` bedeutet keine Warnungsfreiheit
des Scanner-Logs.

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
