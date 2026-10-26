# Native zielbezogene Sicherheitsanalyse

**Sprache:** [English](sonarqube-native-security.md) | Deutsch

SDK-Vorbereitung und Matrix mit zwölf Zielen verwenden `ubuntu-26.04`.
Der Aufrufer pinnt den geprüften Master-Broker `8ae707d72f1a8acb25d239e55e28a73cbc7522b1`
aus dem nutzerfreigegebenen [PR #422](https://github.com/Easton97-Jens/ModSecurity-conector/pull/422).
Geschützte manuelle Laufzeitprüfung und Hosted-Native12-Nachweis stehen aus.
[Aktuelle Readiness](pr-382-merge-readiness.de.md) und
[Ubuntu-Migrationsrecord](../reports/audits/change-records/CR-20261026-ubuntu26-workflow-migration.de.md)
trennen PR-/Master-Gate-Ergebnisse und quellgebundene Prüfungen.

## Umfang und aktueller Status

Die bestehende [breite Parent-Analyse](sonarqube-analysis.de.md) bleibt für
Python, Go, Shell, GitHub Actions, JSON/YAML und den vollständig konfigurierten
Parent-Quellumfang maßgeblich. Nur root `modules/**` und root `reports/**` sind
ausgeschlossen. Ihr CFamily-AutoConfig-Scan bleibt erhalten; er belegt keine
C/C++-Taintanalyse. Der separate [native Workflow](../.github/workflows/sonar-native-security.yml)
ergänzt eine Kompilierungsdatenbank je echtem Buildziel, insgesamt zwölf.

Die zwölf Entwicklungserfassungen verwenden Produktrevision
`542a98bc20a16f885f114375bfa5225a9364dcf2` und Entwicklungsstände der Hilfswerkzeuge.
Sie sind ausdrücklich `import_eligible=false`: erfolgreiche Kompilierung und
Export belegen den Buildkontext. Hosted-Scanner-Ausführung, CFamily-Taint/CTU,
Parsequalität, tatsächlich indexierte Eingaben, Serververarbeitung und
abschließende Ziel-Gates sind unbestätigt. Die aktuelle native
Sicherheitsprüfung ist unvollständig.

Coverage liegt außerhalb der Security- und Merge-Kriterien des Nutzers.
`sonar.coverage.exclusions=**` ändert ausschließlich Coverage. Sicherheitsregeln,
Quellanalyse, Quality Gates und das Warten auf Serververarbeitung bleiben aktiv.
Bestehende Organisationsprofile und Gates werden nicht ersetzt.

## Unabhängige Ziele

Jedes Ziel erhält ein eigenes Projekt in der Organisation `easton97-jens`. Sein
Key besteht aus `Easton97-Jens_ModSecurity-conector_native_` und der Ziel-ID mit
Unterstrichen statt Bindestrichen. Unabhängige Programme und Module verwenden
keine gemeinsame Datenbank: CFamily-Taint und CTU setzen ein gelinktes Ziel voraus.

Die Tabelle erfasst Erwartungen aus Entwicklungserfassungen, einschließlich
aus echten Compilerabhängigkeiten abgeleiteter Parent-Include-Eingaben. Dies
sind keine serverseitig indexierten Zahlen. Die zwölf Ziele enthalten zusammen
**611 Parent-TU-Kompilierungen**; Common-Dateien wiederholen sich zwischen Zielen,
die Zahl ist deshalb keine Anzahl eindeutiger Dateien.

| Ziel-ID | Parent-TUs | Parent-Include-Eingaben | Erwartete indexierte Parent-Eingaben | Zusätzlicher Buildkontext |
| --- | ---: | ---: | ---: | --- |
| `traefik-engine-service` | 64 | 75 | 139 | Kanonischer Engine-Service |
| `haproxy-spoa-runtime` | 50 | 62 | 112 | Kanonische SPOA-Runtime |
| `apache-native-module` | 33 | 46 | 79 | Installierter APXS-/APR-Kontext; begrenzte GCC-LTO-Einschränkung unten |
| `haproxy-htx` | 44 | 58 | 102 | 179 gepinnte Upstream-TUs |
| `envoy-ext-proc` | 64 | 75 | 139 | 22 Go-/generierte Kontext-TUs |
| `envoy-composite` | 64 | 75 | 139 | 22 Go-/generierte Kontext-TUs |
| `lighttpd-patched-module` | 62 | 71 | 133 | Gepinnte konfigurierte Host-Header |
| `nginx-dynamic-module` | 33 | 51 | 84 | Eine generierte Host-Glue-TU |
| `lighttpd-stock-sidecar` | 61 | 71 | 132 | Getrennter Build entspricht dem kanonischen Artefakt |
| `envoy-ext-authz` | 67 | 77 | 144 | Kanonischer Service |
| `traefik-forwardauth` | 68 | 78 | 146 | Kanonischer ForwardAuth-Service |
| `common-targeted-evaluator` | 1 | 0 | 1 | Ursprünglicher C++17-Evaluator; kanonische Artefaktgleichheit |

Das C++-Ziel kompiliert `common/scripts/modsecurity_targeted_eval.cc` mit
`-std=c++17 -Wall -Wextra -Werror` und einem dauerhaften Namespace des gewählten
SDKs. Sein Entwicklungsartefakt entspricht dem kanonischen Compile-/Link-Producer
Byte für Byte. Der Evaluator wird nicht ausgeführt. Dieser Build erhält keinen
C++23-Override.

## Build- und Quellidentität

[`prepare-sonar-native-ci.py`](../ci/checks/analysis/prepare-sonar-native-ci.py)
prüft die exakte saubere Checkout-Revision. Es initialisiert ausschließlich das
direkt gepinnte Framework, baut das kanonische gemeinsame ModSecurity-SDK
`3.0.17` und überträgt dessen Prefix samt Expat-Abhängigkeit in einem Archiv
desselben Laufs. Revision, Framework-/Quellidentität, Build-Provenienz,
Archivdigest und Bibliotheksdigest müssen übereinstimmen. Die Prüfung von
Archiveinträgen und Links begrenzt die Wiederherstellung auf den festen externen
Prefix-Teilbaum.

Die Matrix lädt die exakte Artefakt-ID und verwendet über Job-Outputs die
externe Wurzel des SDK-Producers erneut. Ein Retry ausschließlich fehlgeschlagener
nativer Jobs behält damit die erfolgreiche SDK-Identität, statt einen neuen
`run_attempt`-Pfad anzunehmen. Builds, Caches, Kompilierungsdatenbanken und
Scanner-Arbeitsdateien bleiben außerhalb des Checkouts. Vor Output-Erstellung
oder Rechteänderung wird bestehende, für andere schreibbare Verzeichnisabstammung
abgelehnt.

Die Werkzeuge in [`sonar-native-security/`](../ci/checks/analysis/sonar-native-security/)
erfassen erfolgreiche echte Compileraufrufe, Abhängigkeiten, Compileridentität,
Objekt-/Archiveingaben und den deklarierten Linkgraphen. Der Export verlangt den
exakten Parent-TU-Abschluss und seine tatsächlich eingebundenen Parent-Header.
Externe Upstream- oder Go-generierte TUs bleiben geprüfter Buildkontext; ihre
Datenbankeinträge behaupten keine Indexierung als Parent-Quellen.

Producer-eigenes Source-Mapping ändert den Compileroperanden vor der Ausführung
und prüft identische geordnete Include-Inhalte. Eine erfasste Datenbank wird
nicht umgeschrieben, um kopierte Dateien als ursprüngliche Eingaben auszugeben.
Die CGo-Provenienz bewahrt die offizielle Go-Link-/FIPS-/Build-ID-Producerkette.
Die Apache-Ausnahme lässt ausschließlich beobachtete interne GCC-LTO-/Debug-
Temporärdateien im privaten temporären Verzeichnis des Aufrufs zu; ursprüngliche
Parent-Objekte benötigen weiterhin Producer. Deren transiente Bytes werden
nicht aufbewahrt; daraus folgt kein vollständiger Provenienznachweis des finalen
ELFs. Host-Runtime-Qualifikation liegt außerhalb dieser Buildnachweise.

## Analyse- und Credential-Grenze

Beide Jobs beschränken die Ausführung auf Master-Pushes dieses Repositorys und
PRs desselben Repositorys. Checkout verwendet die exakt analysierte SHA,
lesende GitHub-Rechte, keine persistierten Credentials und keine rekursiven
Submodule. `SONAR_TOKEN` ist ausschließlich im offiziellen Scan-Schritt
vorhanden. Der geprüfte Vertrag des gesamten Workflows bindet Schritte, Skripte,
Defaults, Umgebung, Matrix, Projekt- und SCM-Identität; kanonische
Action-Updates müssen zum Lock passen.

Die offizielle Scan-Action ist auf `v8.3.0` gepinnt; CLI `8.2.0.6438` behält
Signaturprüfung und JRE-Provisioning. Generierte `project.settings` erhalten den
exakten Parent-TU-/Header-Scope ohne Übernahme des Source-/Testlayouts der
Repository-Wurzel. Der Scanner läuft aus der geprüften Checkout-Wurzel.
Die Konfiguration fordert:

- `sonar.cfamily.taintAnalysis=true` ohne explizites Taint-Zeitlimit;
- `sonar.cfamily.ctuAnalysis.branchSubstring=all branches` mit Dateisystemcache;
- höchstens zwei Analyzer-Threads, Fehler bei Speicherdruck `95` und
  Platten-/RAM-Vorprüfung anhand der erfassten Units;
- Warten auf das abschließende Quality Gate mit `600` Sekunden Server-Timeout.

Diese Einstellungen fordern Analysetiefe an; Logs müssen weiterhin belegen,
dass Taint nicht übersprungen, CTU-Kontext beibehalten und der erforderliche
Quellumfang geparst und indexiert wurde. Ein erfolgreicher Upload genügt nicht.
Neue Projekte können eine echte Default-Branch-Baseline und projektbezogene
Token-Autorisierung benötigen; fehlende Voraussetzungen bleiben Fehler, ohne
PR-Quellen als Master umzubenennen.

## Verbleibende Tiefen- und Nachweisgrenzen

Reine C++-Header-Wrapper ohne erfassten echten Consumer und die drei
I12-Instrumentierungsquellen in C++ bleiben im breiten
AutoConfig-Quellscope; dieser Workflow belegt für sie keine Taintanalyse. Externe
SDK-/Upstream-Implementierung, Go/C-sprachübergreifende Flüsse, nicht unterstützte
Dateiformate und tatsächliches Host-Verhalten werden durch die Zielerfassungen
nicht qualifiziert.

Historische I12-Host-, Matrix- und Oracle-Kampagnen bleiben geschlossen. Die
Connector-E2E-Auswahl bleibt `26`; es entsteht kein `I12_COMPLETE` oder
Runtime-Promotion. Framework-CLI-/Updater-Arbeit bleibt getrennt in
[Framework PR #138](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/138).
Der Parent-Framework-Gitlink bleibt unverändert; MRTS bleibt read-only. Framework-Revision `5ef4dc3c815c97121578cd34382b80088b9c61ec` schloss tatsächliche SDK-/Native-/Scanner-Analyse ab, einschließlich einer C-TU mit acht Taint-Regeln und Python mit 32 Taint-Regeln. CE-Task `AaF5sxOo8Px5fiPcdsNi` endete mit `SUCCESS`; sein Gate bleibt ausschließlich wegen Security-Rating 3 `ERROR`. Vier CLI-Flow-Behauptungen werden triagiert; dies bleibt vom Parent-Native12-Abschluss getrennt.

Die integrierte Auswahl nach Master-Übernahme bestand **94 Ausführungen / 342 expandierte Fälle ohne Skips**, beim Inventar `e13c73b981fd1399fbe0c161a8abd753d6cbc4d429957caa86d7c33e1f59bf7c`. Das Inventar deklariert 1992 Fälle / 918 Ausführungen: 97 Kernfälle / 77 Ausführungen plus 1895 autorisierte Offline-Fälle / 841 Ausführungen, mit 614 Quellbindungen und 1.672.802 Bytes. Die Auswahl enthält acht Inventarkontrollen einschließlich Überlauf-Abweisung und sieben Broker-Selektoren / 36 Fälle sowie korrigierte Helper-Capture-Pfad- und isolierte NGINX-Archivvertragskontrollen. Das frühere PASS 79/298 bei `06286b9ae1d1bac124a73c247893c2d522c15cce2dd52089a49f1bb7bd8759be` ist ein Vor-Merge-Zwischenstand. Lokale grüne Ergebnisse belegen keine Hosted-Native12-Analyse.

Neue CI am veröffentlichten Head, Analyzer-Logs, Server-Tasks, Gate-/Readback und quellbasierte Finding-Dispositionen bleiben für die Parent-Native12-/Ubuntu-Änderungen erforderlich.

## Referenzen

- [CFamily-Analysemodi](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [Ziel-Scope](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis), [Taint- und CTU-Konfiguration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis).
- [Deprecation-Ankündigungen](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals#deprecation-announcements); aktuelle Sprach- und Toolchain-Grenzen stehen im [breiten Leitfaden](sonarqube-analysis.de.md).
- [Change Record](../reports/audits/change-records/CR-20261026-sonar-native-security.de.md).
