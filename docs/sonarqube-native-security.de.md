# Native zielbezogene Sicherheitsanalyse

**Sprache:** [English](sonarqube-native-security.md) | Deutsch

SDK-Vorbereitung und alle zwölf Ziele verwenden `ubuntu-26.04`; [aktuelle Readiness](pr-382-merge-readiness.de.md) bindet finale Lieferung und individuelle Dispositionsnachweise.

## Umfang und aktueller Status

Die bestehende [breite Parent-Analyse](sonarqube-analysis.de.md) bleibt für
Python, Go, Shell, GitHub Actions, JSON/YAML und den vollständig konfigurierten
Parent-Quellumfang maßgeblich. Nur root `modules/**` und root `reports/**` sind
ausgeschlossen. Ihr CFamily-AutoConfig-Scan bleibt erhalten; er belegt keine
C/C++-Taintanalyse. Der separate [native Workflow](../.github/workflows/sonar-native-security.yml)
ergänzt eine Kompilierungsdatenbank je echtem Buildziel, insgesamt zwölf.

Am veröffentlichten Parent `011cb197` schloss [Lauf 40392396874](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40392396874) SDK-Vorbereitung und alle zwölf nativen Build-/Capture-/Index-/CTU-/Taint-Analysen ab: insgesamt 611 Compilation Units, keine partiellen Units und 100 % Indexierung je Ziel. Vor Einzeltriage bestanden drei native Gates, neun scheiterten. Zwanzig von 22 Workflows bestanden; die breiten C++17/20/23-Gates scheiterten. Die Quellprüfung bestätigte zwölf Python-Security-Issues und 39 native Issue-Instanzen als False Positives; alle 36 Main-/Advisory-Python-Instanzen und 39 nativen Instanzen sind einzeln als False Positive aufgelöst und frisch zurückgelesen. Ursprüngliche Job-Ergebnisse bleiben unverändert. Diese Analyse liegt vor dem endlichen Abschlusscommit und ist keine Abnahme des finalen Heads. Siehe [zentralen Status](pr-382-merge-readiness.de.md).

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

[`prepare-sonar-native-ci.py`](../modules/ModSecurity-test-Framework/connector_suite/modsecurity_connector_ci/checks/analysis/prepare-sonar-native-ci.py)
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

Der oben genannte veröffentlichte Lauf belegte tatsächliches CTU/Taint und Indexierung aller zwölf Ziele. Ein erfolgreicher Upload allein bleibt unzureichend; spätere Revisionen benötigen eigene Analyzer-/Serverergebnisse. Die erste native PR-Analyse wurde erfolgreich abgeschlossen; keine Baseline-Voraussetzung blockierte sie.

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
Framework-Revision `03da9353561bf632a1f7bfc71b0a2671ec7aa257` bestand alle zwölf CI-Workflows und Sonar und ist Ready; kein Framework-Merge wurde durchgeführt. Parent-Framework-Gitlink `99a7985c1be92a2297b1b59208f64df6768f2cbf` und MRTS bleiben unverändert. Broker #422 ist bereits autorisiert bei `8ae707d72f1a8acb25d239e55e28a73cbc7522b1` integriert; kein weiterer Master-Merge ist autorisiert.

Die automatische Auswahl umfasst jetzt 100 expandierte Fälle / 80 Ausführungen einschließlich dreier Schutzkontrollen. Weitere 1893 Fälle / 839 Ausführungen sind ausschließlich ausdrücklich auf Abruf verfügbar. Automatische Coverage-Katalogbefehle wurden entfernt; der erhaltene Collector verlangt `--on-demand`. Coverage ist laut Benutzeranweisung für den Merge irrelevant. Breite Quell-/Scanner-/Gate-Analyse bleibt aktiv; nur root `modules/**` und root `reports/**` sind ausgeschlossen.

Readback der einzelnen False-positive-Dispositionen und Abnahme des finalen Heads bleiben im [zentralen Status](pr-382-merge-readiness.de.md); der beobachtete Lauf wird nicht auf unveröffentlichte Änderungen übertragen.

## Referenzen

- [CFamily-Analysemodi](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/analysis-modes), [Ziel-Scope](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/understanding-the-analysis), [Taint- und CTU-Konfiguration](https://docs.sonarsource.com/sonarqube-cloud/analyzing-source-code/languages/c-family/customizing-the-analysis).
- [Deprecation-Ankündigungen](https://docs.sonarsource.com/sonarqube-cloud/deprecations-and-removals#deprecation-announcements); aktuelle Sprach- und Toolchain-Grenzen stehen im [breiten Leitfaden](sonarqube-analysis.de.md).
- [Change Record](../reports/audits/change-records/CR-20261026-sonar-native-security.de.md).
