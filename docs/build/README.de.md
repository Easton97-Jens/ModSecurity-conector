# Build-Dokumentation

**Sprache:** [English](README.md) | Deutsch

Dieser Bereich erläutert, wie Root- und Connector-Make-Targets ausgewählte
Connector-Routen vorbereiten und bauen. Ein Build-, Link- oder Config-Load-
Ergebnis ist keine Runtime-Evidence und erhebt keinen Production-, CRS-,
HTTP/2-, HTTP/3-, vollständige-Matrix- oder Strict-für-alle-Connectoren-Claim.

## Build-Eingaben und sichere Pfade

Das Root-Makefile leitet seinen Arbeitsbaum unter
<code>VERIFIED_RUN_ROOT</code> ab. Setzen Sie für einen reproduzierbaren
lokalen Build <code>BUILD_ROOT</code> auf ein absolutes, beschreibbares
Verzeichnis außerhalb des Checkouts:

~~~sh
make build-nginx BUILD_ROOT="/srv/modsecurity-work/build"
~~~

<code>BUILD_ROOT</code> ist optional, weil das Makefile
<code>VERIFIED_RUN_ROOT/build</code> ableitet, wenn kein Wert bereitgestellt
wird. Der Beispielwert <code>/srv/modsecurity-work/build</code> ist ein
absoluter Runtime-Pfad, kein Repository-Default. Verwenden Sie weder
Repository-Root noch Systemverzeichnis oder einen Pfad mit Secrets. Details zu
Format, Scope, Auswirkung und Sicherheit stehen unter
[Konfigurationsvariablen](../reference/variables.de.md#runtime-und-repository-pfade).

Der Platzhalter <code>&lt;connector&gt;</code> bedeutet genau einen von
<code>apache</code>, <code>nginx</code>, <code>haproxy</code>,
<code>envoy</code>, <code>traefik</code> oder <code>lighttpd</code>.
Verwenden Sie zum Beispiel <code>make build-nginx</code>; schreiben Sie nicht
literally <code>make build-&lt;connector&gt;</code>.

## Target-Familien

| Target | Zweck | Voraussetzungen / wichtige Variablen | Erzeugte Ausgabe | Grenze |
|---|---|---|---|---|
| <code>make check-framework</code> | Prüft, dass das Framework verfügbar ist | <code>FRAMEWORK_ROOT</code> zeigt auf einen vorhandenen Framework-Checkout | Konsolenergebnis | Baut keinen Connector |
| <code>make setup-dev</code> | Installiert oder bereitet Entwicklungs-Python-Dependencies über das Framework vor | <code>PYTHON</code>, <code>FRAMEWORK_ROOT</code> | Änderungen der Entwicklungsumgebung außerhalb versionierter Sources | Bereitet nicht jede Host-Komponente vor |
| <code>make prepare-runtime-components</code> | Holt/baut wiederverwendbare gepinnte Host-Komponenten | Sichere Build-/Cache-Pfade, optionale Source-Pin-Variablen | Component-Cache und Environment-Snapshot | Führt keinen Connector-Lifecycle-Traffic aus |
| <code>make build-<connector></code> | Führt die ausgewählte Connector-Build-Stage aus | Framework, Build-Root, target-spezifische Host-Eingaben | Connector-spezifische Build-Ausgabe | Erfolgreicher Build ist kein Config- oder Runtime-Nachweis |
| <code>make build-all-connectors</code> | Führt die Build-Stage für alle sechs Connector-Namen aus | Alle relevanten Host-/Component-Voraussetzungen | Per-Connector-Build-Ausgabe | Aggregate-Build erzeugt keine Full-Lifecycle-Evidence |
| <code>make check-config-<connector></code> | Lädt/prüft die ausgewählte Connector-Konfiguration | Vorbereiteter ausgewählter Build und Konfiguration | Config-Load-Diagnostik | Sendet keinen Traffic |
| <code>make prepare-open-connector-runtimes</code> | Bereitet ausgewählte Envoy-, Traefik- und lighttpd-Host-Eingaben vor | Framework- und Cache-/Provisionierungs-Voraussetzungen | Component-Preparation-Ausgabe | Vorbereitung ist keine Capability-Promotion |
| <code>make lint</code> | Führt Source-, Contract- und dokumentationsorientierte Checks aus | Python, Shell-Tools, Framework, C-Toolchain, wo vorhanden | Diagnostik | Kein All-Host-Runtime-Test |

Prozess-Exit-Code <code>0</code> bedeutet nur, dass das aufgerufene Target
seinen technischen Vertrag erfüllte. <code>1</code> ist ein allgemeiner
Fehler, <code>2</code> ungültige Eingabe/Contract-Validierung und
<code>77</code> eine fehlende optionale oder erforderliche
Umgebungsvoraussetzung. Das Statusvokabular steht unter
[Testing](../testing-and-evidence.de.md).

## Parent-CI-Python-Versionsvertrag

**Change Record:** [CR-20260721-python314-go1265-toolchain-baseline](../../reports/audits/change-records/CR-20260721-python314-go1265-toolchain-baseline.de.md)

Dieser eingecheckte Parent-GitHub-Actions-Vertrag hält die implementierte
Interpreterstrategie, Workflow-Grenzen und lokale statische
Validierungsevidenz fest. Er stellt keine GitHub-Actions-Ausführung, keinen
Remote-CI-Lauf, Pull Request, Review oder Delivery-Erfolg dar.

### Kanonischer Interpreter und Strategie

Die eingecheckte Root-[`.python-version`](../../.python-version) ist die
einzige maschinenlesbare Interpreterquelle. Ihr erforderlicher Inhalt ist das
exakte stabile Release <code>3.14.6</code>. Jeder Python-ausführende Job aus
der folgenden Inventarisierung muss vor seiner ersten direkten oder indirekten
Python-Nutzung `actions/setup-python` ausführen mit:

~~~yaml
python-version-file: .python-version
check-latest: false
~~~

Das Versionsliteral darf nicht in Workflow-YAML dupliziert werden. Die
Setup-Action wird separat Action-gepinnt; ein Action-Lock-Record ist keine
Interpreterversionsquelle. Die akzeptierte Setup-Referenz ist der bereits
vorhandene unveränderliche Pin
`actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0`,
der auch in `ci/tooling/security-tools.lock.yml` dokumentiert ist; der
Contract-Checker muss diese v7-Referenz statt einer veralteten v6-Erwartung
validieren. Nach dem Setup muss der Workflow-Vertrag validieren, dass `python`
und `python3` äquivalente konfigurierte Python-<code>3.14.6</code>-Interpreter
auswählen, bevor einer der Namen, ein
Python-gestütztes Make-Target oder eine indirekte Framework-Prüfung verwendet
wird. Kein aufgelisteter Job darf auf einen ambienten Runner-, Bootstrap-,
Virtual-Environment- oder System-`python3`-Interpreter zurückfallen.

| Alternative | Entscheidung | Begründung |
| --- | --- | --- |
| Floating `3.14` | Abgelehnt | Eine spätere Runner-/Tool-Cache-Auflösung kann stillschweigend ein anderes Patch-Release auswählen und Patch Drift erzeugen. |
| Exaktes `3.14.6` aus einer eingecheckten `.python-version` | Ausgewählt | Der exakte stabile Patch ist reviewbar und reproduzierbar, während `python-version-file` allen abgedeckten Jobs dieselbe Quelle gibt. |
| Exakte Version plus permanenter Canary-Workflow | Abgelehnt | Die unabhängige schreibgeschützte Candidate-Validierungs-Stage unten validiert einen vorgeschlagenen Patch vor der Veröffentlichung; ein zusätzlicher Canary würde diese Kontrolle duplizieren, ohne die Publisher-Trust-Grenze zu ändern. |

### Vollständige Parent-Workflow-/Job-Inventarisierung

Diese 22-Job-Baseline-Inventarisierung ist die maßgebliche
Dokumentationstabelle für den verlinkten Change Record. „Vorhandenes
Minor-only-Setup“ und „Ambientes oder Bootstrap-Python“ beschreiben den
historischen Einführungspfad vor dem Vertrag; keine der beiden Bezeichnungen
ist ein aktueller Selector. Im eingecheckten Workflow-Vertrag hat jede Zeile
dasselbe explizite <code>3.14.6</code>-Setup und dieselbe
`python`/`python3`-Äquivalenzvalidierung.

| Workflow | Job | Python-Ausführungskette | Baseline-Zustand |
| --- | --- | --- | --- |
| `all-connectors-no-crs.yml` | `no-crs` | Direktes `python3`, Framework-Skripte und Python-gestützte Make-Targets | Vorhandenes Minor-only-Setup |
| `all-connectors-no-crs.yml` | `aggregate` | Direkte `python3`-Validierung und -Zusammenfassung | Ambientes oder Bootstrap-Python |
| `check-actions-versions.yml` | `check-actions-versions` | `python3 scripts/check-github-actions-versions.py` | Vorhandenes Minor-only-Setup |
| `ci-security-secrets.yml` | `pull-request-range` | `python3 ci/tools/fetch_security_tool.py` | Ambientes oder Bootstrap-Python |
| `ci-security-secrets.yml` | `advisory-full-history` | `python3 ci/tools/fetch_security_tool.py` | Ambientes oder Bootstrap-Python |
| `ci-security-workflow-lint.yml` | `actionlint` | Python-Tool-Fetcher und `python3 -m unittest` | Ambientes oder Bootstrap-Python |
| `ci-security-workflow-lint.yml` | `zizmor` | Python-Tool-Fetcher | Ambientes oder Bootstrap-Python |
| `lint.yml` | `scaffold-lint` | Python-Dokumentationscheck und nicht-PR-Python-gestütztes Setup/Lint | Vorhandenes Minor-only-Setup |
| `open-connectors-smoke.yml` | `open-connectors-smoke` | Direkte Zusammenfassung plus indirekte Python-Make-Targets | Vorhandenes Minor-only-Setup |
| `protocol-contract.yml` | `protocol-contract` | `python3 -m unittest` und Protocol-Client-Target | Vorhandenes Minor-only-Setup |
| `protocol-contract.yml` | `nginx-profile-and-client-preflight` | Inline-`python3` und Client-Make-Target | Vorhandenes Minor-only-Setup |
| `quick-framework-check.yml` | `quick-check` | Indirekte Setup-, Matrix- und Quick-Check-Python-Arbeit | Vorhandenes Minor-only-Setup |
| `test-apache.yml` | `apache-structure` | Bedingtes nicht-PR-Python-Setup und Quick-Check | Vorhandenes Minor-only-Setup |
| `test-common.yml` | `common-structure` | Bedingtes nicht-PR-Python-Setup und Quick-Check | Vorhandenes Minor-only-Setup |
| `test-envoy.yml` | `envoy-contract` | Indirektes Python in Connector-Checks | Ambientes oder Bootstrap-Python |
| `test-full-smoke-sequential.yml` | `manual-heavy-runtime-validation` | `.venv/bin/python -m py_compile` und Python-Make-Pfade | Ambientes oder Bootstrap-Python |
| `test-lighttpd.yml` | `lighttpd-contract` | Indirektes Python in Connector- und Shared-Checks | Ambientes oder Bootstrap-Python |
| `test-nginx.yml` | `nginx-structure` | Bedingtes nicht-PR-Python-Setup und Quick-Check | Vorhandenes Minor-only-Setup |
| `test-traefik.yml` | `traefik-contract` | Indirektes Python in Connector- und Shared-Checks | Ambientes oder Bootstrap-Python |
| `update-actions-versions.yml` | `update-actions-versions` | `python3 scripts/update-github-actions-versions.py --write` | Vorhandenes Minor-only-Setup |
| `update-submodules.yml` | `validate-submodule-update` | Indirektes Python über `make quick-check` | Ambientes oder Bootstrap-Python |
| `verified-report-governance.yml` | `report-governance` | Indirektes Python über `make report-governance` | Vorhandenes Minor-only-Setup |

Die Inventarisierung schließt Jobs ohne nachgewiesene Python-
Ausführungskette absichtlich aus, etwa Action-only-Security-Scans, Inline-
JavaScript-Cleanup und Shell-only-Checks. Ein neuer Python-ausführender Job
muss diesem Vertrag beitreten, bevor er Python verwenden darf. Der statische
Validator deckt die Workflow-Dateinamen `.yml` und `.yaml` ab.

### Vertrag für den sicheren Stable-Patch-Updater

Der Updater ist von den 22 Baseline-Jobs getrennt. Der eingecheckte Workflow
`.github/workflows/update-python-version.yml` hat genau drei Jobs:

| Job | Interpreter und Trust-Grenze | Erforderliches Verhalten |
| --- | --- | --- |
| `resolve-python-patch` | Läuft mit der aktuellen kanonischen `.python-version`; schreibgeschützt | Ruft nur die feste offizielle strukturierte Python-Release-API `https://www.python.org/api/v2/downloads/release/?is_published=true` über HTTPS mit exaktem Host `www.python.org`, ohne Redirects, mit `application/json`, begrenzter Response-Verarbeitung und Schema-Validierung auf. `--check` parst veröffentlichte, nicht-prerelease stabile `3.14.N`-Werte strikt, meldet einen Candidate nur bei einem höheren Patch und kann weder downgraden noch eine Minor-Serie überqueren. |
| `validate-python-patch` | Richtet den unabhängig aufgelösten Candidate-Patch ein; schreibgeschützt | Wiederholt die Kompatibilitätsvalidierung mit dem Candidate-Interpreter vor der Veröffentlichung. Sie ist unabhängig vom Current-Version-Interpreter des Resolvers und führt keine Source- oder Branch-Mutation aus. |
| `create-python-update-pr` | Läuft mit der aktuellen kanonischen `.python-version`; Default-Branch-gated Publisher | Löst den Candidate mit `--expected-version` vor `--update` erneut auf; nur dieser Job erhält `contents: write` und `pull-requests: write` und nur, um einen vorgeschlagenen Update-Pull-Request zu erstellen. |

Die einzigen Trigger sind der geplante Montagslauf und ein manueller
`workflow_dispatch`; es gibt keinen Push- oder Pull-Request-Trigger. Jeder Job
ist auf die Ref des Repository-Default-Branch gegatet und checkt diesen
vertrauenswürdigen Default-Branch ohne Submodules oder persistierte Checkout-
Credentials aus. Der Validierungsjob richtet die unabhängig aufgelöste
Candidate-Version ein, löst sie erneut auf, führt den fail-closed statischen
Vertrag aus, kompiliert die eingecheckten Python-Pfade und führt die fokussierten
Parent-nativen Contract-Tests aus, bevor der Publisher starten kann.

`--check` löst und validiert einen Candidate ohne Dateien zu ändern. `--update`
ist dem Publisher vorbehalten, nachdem die unabhängige Validierung und die
Expected-Version-Neuauflösung bestanden haben. Der Publisher ist kein Updater
für beliebige Python-Versionen: Er akzeptiert nur das strikte stabile
<code>3.14.N</code>-Format, niemals einen niedrigeren Patch, Prerelease,
alternative Minor-Serie oder unstrukturierte/HTML-Release-Daten.

Der Publisher verwendet den konstanten Branch
`automation/update-python-314` und den stabilen Titel
`chore(ci): propose Python 3.14 patch update`. Er erstellt einen Draft Pull
Request, wenn dieser Branch nicht existiert, oder aktualisiert einen bestehenden
repository-eigenen Draft-Update-Pull-Request erst nach Prüfung seines Head-
Repository, Default-Base und deaktivierten automatischen Merge sowie der
Beschränkung seines Merge-Base-Diffs auf `.python-version`; einen Branch ohne
diesen exakten Pull Request überschreibt er nicht. Damit erstellt er keine
doppelten Update-Pull-Requests und führt nie einen Force-Push aus. Sein englisch/deutscher Pull-
Request-Body enthält vorherige und vorgeschlagene Version, offizielle Release-
Identität, Metadatenquelle, Validierungsworkflow/-Run-URL,
`.python-version` als einzige geänderte Datei, die beibehaltene Python-3.14-
Minor-Version und das Fehlen eines automatischen Merge.

Der Publisher streamt die begrenzte REST-Pull-List-Antwort direkt von `gh api`
in seinen strikten Duplicate-Key-JSON-Selector. Der Selector besitzt keinen
aufrufergesteuerten Response-Dateipfad; beim Wiederverwenden eines bestehenden
Draft Pull Request überschreitet der Publisher daher keine Response-Datei- oder
Symlink/TOCTOU-Grenze.

Der Updater darf nicht auto-mergen, den Default-Branch beschreiben, force-
pushen, Repository- oder benutzerbereitgestellte `secrets.*` konsumieren,
Submodules initialisieren oder eine beliebige Project-Workload ausführen. Der
Publisher darf nur GitHubs automatisch bereitgestelltes Job-Token verwenden,
das durch seine zwei job-begrenzten Schreibrechte eingeschränkt ist, um den
Draft Pull Request zu erstellen oder den vorhandenen offenen Update-Pull-
Request zu aktualisieren; seine Repository-
Ausführung ist auf die festen Interpreter-Verifikations- und Updater-Pfade
begrenzt. Resolver und Validator bleiben schreibgeschützt. Die begrenzten
Schreibrechte des Publishers, das Default-Branch-Gate, die Neuvalidierung an
der Schreibgrenze und die ausschließlich PR-basierte Ausgabe verhindern, dass
Metadaten den Default-Branch direkt verändern.

Die unabhängige Validierungs-Stage ist die Evidence-Grenze für einen
vorgeschlagenen Patch; sie behauptet nicht, dass ein geplanter Lauf, Candidate,
Pull Request oder Merge stattgefunden hat. Solche Ergebnisse benötigen separat
beobachtete CI- und Delivery-Evidence.

### Beobachtete lokale Implementierungsvalidierung

Vor diesem Baseline-Upgrade schlug die Current-Master-Ausführung von
`make check-python-version-contract` fehl, weil ihr Python-spezifischer
Checker den alten v6-`actions/setup-python`-Pin erwartete, obwohl die
eingecheckten Workflows und der geprüfte Security-Lock bereits den
unveränderlichen v7-Pin verwendeten. Die Reparatur des v7-Checkers gehört zu
dieser exakten Versionsänderung; sie ändert weder vorhandenen Workflow-Pin
noch Lock-Eintrag, Berechtigungen, Trigger oder Publisher-Grenze.

Die verfügbaren lokalen Executables sind Python <code>3.14.4</code> und Go
<code>1.26.0</code>, nicht die geforderten exakten Baselines Python
<code>3.14.6</code> und Go <code>1.26.5</code>. Sie können nur Source-Level-
und statische Validierung unterstützen. Ein exakter GitHub-gehosteter
Workflow-Lauf, der die beiden deklarierten Versionen installiert, ist
erforderlich, bevor diese Änderung als verifizierte CI-Evidence gelten kann.
Der verlinkte Change Record hält tatsächliche Befehle, deren Ergebnisse und
eine etwaige Framework-abhängige Einschränkung der Dokumentationsprüfung fest,
ohne ein lokales Ergebnis in Connector-Runtime- oder Remote-CI-Evidence
umzudeuten.

## Compiler- und Linker-Variablen

Verwenden Sie Standard-Compiler-Umgebungsvariablen nur, wenn die lokale
Toolchain sie erfordert. Die Root-Defaults sind:

| Variable | Pflicht | Root-Default | Beispiel | Auswirkung / Sicherheit |
|---|---:|---|---|---|
| <code>PYTHON</code> | nein | <code>.venv/bin/python</code>, falls vorhanden, sonst <code>python3</code> | <code>PYTHON=python3</code> | Wählt Python-Interpreter für Skripte; vertrauenswürdiges Executable verwenden |
| <code>MSCONNECTOR_C_STD</code> | nein | <code>c17</code> | <code>MSCONNECTOR_C_STD=c23</code> | Wählt Common-Helper-C-Profil; nicht unterstützte optionale Profile können übersprungen werden |
| <code>MSCONNECTOR_CFLAGS</code> | nein | <code>-std=$(MSCONNECTOR_C_STD) -Wall -Wextra -Werror</code> | <code>MSCONNECTOR_CFLAGS="-std=c17 -Wall -Wextra -Werror"</code> | Flags für Common-Helper-Checks; Quoting erhalten |
| <code>CC</code>, <code>CXX</code> | nein | Shell-/Toolchain-Default | <code>CC=clang</code> | Wählen vertrauenswürdige C/C++-Compiler |
| <code>CPPFLAGS</code>, <code>CFLAGS</code>, <code>CXXFLAGS</code>, <code>LDFLAGS</code>, <code>LIBS</code> | nein | kein Root-Default | <code>CFLAGS="-O2"</code> | Fügt Compile-/Link-Eingaben hinzu; nicht vertrauenswürdige Flags können den Build ändern |
| <code>PKG_CONFIG_PATH</code>, <code>LD_LIBRARY_PATH</code>, <code>PATH</code> | nein | Shell-Default | <code>PKG_CONFIG_PATH="/srv/prefix/lib/pkgconfig"</code> | Ändert Tool-/Library-Discovery; auf vertrauenswürdige Pfade beschränken |

Die Schreibweise <code>$(MSCONNECTOR_C_STD)</code> oben ist eine
Make-Variablenreferenz, kein Shell-Kommando. Das Makefile löst sie vor dem
Ausführen eines Rezepts auf. Vollständige Formate, Defaults und
Framework-weitergereichte Source-Variablen stehen unter
[Konfigurationsvariablen](../reference/variables.de.md).

## Lokale C/C++-Diagnostik

Integrationsstufe 1 stellt eine reproduzierbare lokale C17/C++17-
Diagnosegrundlage bereit. Sie ist ausschließlich eine Source- und
Contract-Prüfung: Sie bereitet weder Runtime-Komponenten vor noch lädt oder
installiert sie Tools und beansprucht keine Runtime-, Production-, CRS- oder
Connector-Release-Evidence.

### Toolvoraussetzungen und Blockierungsstatus

Vor einer Diagnoseerfassung <code>make check-analysis-tools</code> ausführen.
Das Target gibt die tatsächlich ausgewählten Pfade und Versionen von
<code>CC</code>, <code>CXX</code>, <code>clangd</code> und Bear aus. Vor der
advisory Baseline <code>make check-clang-analysis-tools</code> ausführen; es
meldet unabhängig die ausgewählten Tools <code>clang-tidy</code>,
<code>clang</code> und <code>clang++</code>. Keines der Targets installiert,
lädt oder bereitet einen Ersatz vor.

Die advisory Baseline benötigt einen markierten, beschreibbaren
<code>CODEX_TEMP_ROOT</code> mit seinem Kind <code>tmp/</code>, mindestens 5 GiB
freiem Speicher sowie eine externe C17/C++17-Compilation-Database unterhalb
dieses Roots. Sie weist relative, im Checkout liegende, aus Symlinks
ausbrechende oder anderweitig unsichere CDB-/Ausgabepfade vor dem Erzeugen von
Ausgaben zurück. Fehlende Tools oder Voraussetzungen liefern Exit-Code
<code>77</code>; ungültige oder unsichere Parameter liefern Exit-Code
<code>2</code>; ein anderer Nicht-null-Exit-Code bedeutet einen technischen
Analysefehler.

Die Baseline fügt weder eine <code>.clang-tidy</code>- noch eine
<code>.clangd</code>-Datei hinzu. Sie verwendet eine explizite Inline-Tidy-
Konfiguration, wendet weder <code>--fix</code>, <code>--fix-errors</code>,
<code>--fix-notes</code> noch <code>--export-fixes</code> an und fügt keine
<code>NOLINT</code>-Einträge, Sanitizer-Flags, Production-Binary-Flags, ein
CI-Gate oder eine Workflow-Änderung hinzu.

### Capture- und C++17-Evaluator-Targets

| Target | Erforderliche lokale Eingabe | Ergebnis und Grenze |
|---|---|---|
| <code>make compile-db-nginx-c17</code> | Absolutes externes <code>COMPDB_OUTPUT</code>; vorhandene NGINX- und libmodsecurity-Header | Bear erfasst den direkten Compilerprozess von <code>check-nginx-c17</code>. Er deckt die in <code>connectors/nginx/config</code> deklarierten NGINX- und Common-Quellen einschließlich <code>common/src/late_intervention.c</code> ab. |
| <code>make check-targeted-evaluator-cpp17</code> | Absolutes externes <code>CPP_BUILD_ROOT</code>, <code>MODSECURITY_INCLUDE_DIR</code> und <code>MODSECURITY_LIB_DIR</code>; optionales absolutes <code>MODSECURITY_LIB_FILE</code> | Kompiliert nur <code>common/scripts/modsecurity_targeted_eval.cc</code> mit <code>-std=c++17 -Wall -Wextra -Werror</code>. Das lokale Binary wird nicht ausgeführt und ist kein Production-Artefakt. |
| <code>make compile-db-cpp17</code> | Dieselben C++17-Eingaben sowie dasselbe externe <code>COMPDB_OUTPUT</code> | Bear erfasst den echten Evaluator-Compilerprozess und führt dessen C++17-Eintrag atomar mit einer gültigen bestehenden Datenbank zusammen. Es wird kein Compilerkommando erfunden. |
| <code>make check-clangd-c17</code> | Ein zusammengeführtes externes <code>COMPDB_OUTPUT</code> mit NGINX-, Common- und Evaluator-Einträgen | Validiert die Datenbank und prüft je eine repräsentative NGINX-, Common- und C++17-Translation-Unit mit <code>clangd --check</code>. Es werden keine Fixes angewendet; Konfiguration, Background-Indexing, Clang-Tidy und clangd-Tweaks sind deaktiviert. |

### Advisory-Clang-Analysebaseline

| Target | Erforderliche lokale Eingabe | Ergebnis und Grenze |
|---|---|---|
| <code>make check-clang-analysis-tools</code> | Vertrauenswürdige Tools <code>clang-tidy</code>, <code>clang</code> und <code>clang++</code> auf <code>PATH</code> oder die entsprechenden Executable-Overrides | Meldet die ausgewählten Versionen, ohne Analyseausgaben zu erzeugen. Ein fehlendes Tool liefert <code>77</code>. |
| <code>make clang-tidy-baseline</code> | Absolutes <code>COMPDB_OUTPUT</code> und absolutes <code>ANALYSIS_OUTPUT</code>, beide unterhalb des markierten <code>CODEX_TEMP_ROOT</code> | Führt <code>clang-tidy</code> für jede validierte C17/C++17-Translation-Unit mit dem expliziten Profil <code>-*,bugprone-*,cert-*</code> aus. Schreibt Rohlogs und <code>clang-tidy-baseline.json</code> nur unterhalb von <code>ANALYSIS_OUTPUT</code>. |
| <code>make clang-analyzer-baseline</code> | Dieselben sicheren CDB-/Ausgabepfade | Ersetzt CDB-Compiler-Driver durch <code>clang</code> oder <code>clang++</code>, entfernt ausgabeschreibende Argumente und führt direkt <code>clang --analyze</code> mit dem Profil <code>core,unix,security,cplusplus,deadcode</code> und einer eigenen SARIF-Ausgabe aus. Schreibt <code>clang-analyzer-baseline.json</code>. Es benötigt kein <code>scan-build</code>. |
| <code>make clang-analysis-baseline</code> | Dieselben sicheren CDB-/Ausgabepfade | Führt beide advisory Pfade aus und schreibt ein normalisiertes <code>clang-analysis-baseline.json</code> sowie laufbezogene Rohlogs unterhalb von <code>ANALYSIS_OUTPUT</code>. |

Der Runner validiert, dass CDB-Einträge eindeutige, getrackte Repository-C/C++-
Quellen mit dem erforderlichen C17/C++17-Flag benennen, bevor er ein Ergebnis
schreibt. Er staged eine bereinigte Compilation-Database und entfernt nach der
Invocation nur dieses runner-eigene Staging-Kind; ein vom Aufrufer geliefertes
<code>ANALYSIS_OUTPUT</code> entfernt er nie rekursiv. Er erstellt vor und nach
jedem Lauf Snapshots der CDB, der analysierten Source-Inhalte und des
Arbeitsbaumstatus. Ein veränderter Snapshot ist ein technischer Fehler;
bereits vorhandene unabhängige Arbeitsbaumänderungen dürfen unverändert bleiben.

Das normalisierte JSON enthält immer CDB-SHA-256, Toolpfade und -versionen,
angeforderte und aktive Tidy-Checks, den direkten Static-Analyzer-Weg,
Translation-Unit-Zahlen, Rohartefakt-Referenzen, Findings, technische Fehler,
Read-only-Verifikation und null-inklusive Klassifikationssummen. Eine technisch
vollständige Baseline liefert <code>0</code>, auch wenn Findings vorhanden sind.
Die einzigen Klassifikationswerte sind:

~~~text
confirmed_bug
needs_validation
possible_security_candidate
false_positive
third_party_header
intentional_pattern
out_of_scope
~~~

Tool-Diagnosen sind Triage-Eingaben, kein automatischer Beweis.
Repository-Diagnosen beginnen normalerweise als <code>needs_validation</code>;
CERT-/Security-orientierte Checks können
<code>possible_security_candidate</code> sein; externe Header sind
<code>third_party_header</code>; externe Nicht-Header-Lokationen sind
<code>out_of_scope</code>. Die Baseline markiert ein Finding nie automatisch
als bestätigten Bug, False Positive oder beabsichtigtes Muster. Ein
<code>possible_security_candidate</code> ist ausdrücklich unbestätigt und
benötigt separate Codex-Security-Validierung, bevor eine Security-Schlussfolgerung
oder Source-Änderung erfolgt.

Jede Erfassung filtert generierte Probes und externe kopierte Quellen, behält
nur getrackte Checkout-Translation-Units, validiert C17/C++17 und
<code>-Wall -Wextra -Werror</code>, dedupliziert nach Translation-Unit und
veröffentlicht per atomarem Replace. Eine fehlgeschlagene Erfassung oder
Validierung lässt ein bestehendes <code>COMPDB_OUTPUT</code> unverändert. Der
Ausgabepfad und jeder erfasste Compiler-Output müssen absolut und außerhalb
des Checkouts liegen.

Einen externen Analyse-Root statt des ausgecheckten lokalen
<code>compile_commands.json</code> verwenden; der Root-Dateiname und
<code>/.cache/clangd/</code> werden absichtlich von Git ignoriert. Für eine
vollständige C17/C++17-Datenbank zuerst NGINX erfassen und dann C++17 in
dieselbe Datei zusammenführen:

~~~sh
make check-analysis-tools
make compile-db-nginx-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
make check-targeted-evaluator-cpp17 \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make compile-db-cpp17 \
  COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json" \
  CPP_BUILD_ROOT="/abs/build/cpp-evaluator-cdb" \
  MODSECURITY_INCLUDE_DIR="/abs/libmodsecurity/include" \
  MODSECURITY_LIB_DIR="/abs/libmodsecurity/lib"
make check-clangd-c17 COMPDB_OUTPUT="/abs/analysis/nginx/compile_commands.json"
~~~

<code>compile-db-cpp17</code> erhält gültige NGINX-Zeilen und ersetzt nur eine
passende Evaluator-Zeile; es kann daher auch vor der NGINX-Erfassung laufen.
Eine Datenbank mit nur einer Sprache ist weiterhin für ihr Capture-Target
gültig, aber <code>check-clangd-c17</code> schlägt eindeutig fehl, bis beide
erforderlichen Abdeckungsmengen vorhanden sind.

Für die advisory Pfade einen markierten externen Codex-Temp-Root verwenden. Die
CDB ist eine Eingabe aus den obigen Erfassungsschritten; die Baseline erfasst
sie nicht erneut und verändert sie nicht:

~~~sh
export CODEX_TEMP_ROOT="/abs/marked-codex-temp-root"
export TMPDIR="$CODEX_TEMP_ROOT/tmp"
export ANALYSIS_ROOT="$CODEX_TEMP_ROOT/analysis"
export COMPDB_OUTPUT="$ANALYSIS_ROOT/final-cpp-diagnostics/compile_commands.json"

make check-clang-analysis-tools

make clang-tidy-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/tidy"

make clang-analyzer-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/analyzer"

make clang-analysis-baseline \
  COMPDB_OUTPUT="$COMPDB_OUTPUT" \
  ANALYSIS_OUTPUT="$ANALYSIS_ROOT/clang-baseline/combined"
~~~

Diese erste Stufe besitzt keine Compilation-Database-Abdeckung für Apache,
HAProxy, Envoy, Traefik oder lighttpd. Sie führt keinen Connector-Traffic aus,
untersucht keine Runtime-Artefakte, verändert keine Product-Source, ändert das
Framework oder sein Submodul nicht und begründet keine Production- oder
Runtime-Freigabe.

## Cache- und Source-Provisionierung

<code>CACHE_ROOT</code> verwendet standardmäßig
<code>VERIFIED_RUN_ROOT/cache-v2</code> und
<code>CONNECTOR_COMPONENT_CACHE</code> dessen Kind <code>shared</code>.
Beide sind nach dem Ableiten absolute Cache-Pfade. Der Cache ist
wiederverwendbare Eingabe, keine kanonische Evidence.

Wählen Sie vor der Vorbereitung einen isolierten Elternpfad:

~~~sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
~~~

<code>VERIFIED_RUN_PARENT</code> ist optional; der Root wählt
<code>RUNNER_TEMP</code>, dann <code>TMPDIR</code>, dann den dokumentierten
Fallback <code>&lt;system-temporary-root&gt;</code>, wenn die Variable leer
ist. <code>&lt;system-temporary-root&gt;</code> bezeichnet den temporären
System-Fallback der Runtime; es ist ein Dokumentationsplatzhalter und ändert
keinen eingecheckten Runtime-Default. Das Beispiel ist ein empfohlener lokaler
Wert, kein Repository-Default. Setzen Sie
<code>SKIP_RUNTIME_COMPONENT_PREPARE=1</code> nur, wenn bereits ein gültiger
invocation-lokaler Snapshot und kompatibler Cache existieren. Dies bedeutet
nicht „fehlende Dependencies überspringen“.

Fortgeschrittene Source-/Provenance-Werte wie <code>HAPROXY_SOURCE_URL</code>,
<code>HTTPD_SHA256</code>, <code>NGINX_SOURCE_GIT_REF</code> und
<code>MODSECURITY_V3_GIT_REF</code> sind Framework-weitergereicht. URLs,
Revisionen, Checksums und Source-Pfade ändern die Provisionierungsidentität und
können Rebuilds auslösen. Sie ändern keine Connector-Capability und promoten
kein Ergebnis.

## Ausgewählte Build-Routen

| Connector | Build-Target | Ausgewähltes Full-Lifecycle-Profil | Build-/Integrationshinweis |
|---|---|---|---|
| Apache | <code>build-apache</code> | <code>native-httpd-module</code> | Native httpd-Modulroute; APXS- und Host-Eingaben werden getrennt provisioniert/geprüft |
| NGINX | <code>build-nginx</code> | <code>native-nginx-http-module</code> | Native NGINX-HTTP-Modulroute; Modul-, Prefix- und Worker-Pfade bleiben Host-spezifisch |
| HAProxy | <code>build-haproxy</code> | <code>native-htx-filter</code> | Native HTX-Filterroute; Source-/Build-Präsenz ist kein Response-Body-Claim |
| Envoy | <code>build-envoy</code> | <code>ext_proc</code> | Streamed-External-Processing-Route; ein alternativer ext_authz-Helper ist nicht stillschweigend die ausgewählte Route |
| Traefik | <code>build-traefik</code> | <code>native-middleware</code> | Native Middleware-Route mit lokalem UDS-Service; forwardAuth-Compatibility-Helper bleiben getrennt |
| lighttpd | <code>build-lighttpd</code> | <code>patched-native</code> | Gepatchte Native-Host-/Modulroute; Patch-/Build-Erfolg ist kein Full-Lifecycle-Nachweis |

Die Profilwerte werden von Full-Lifecycle-Targets geliefert. Setzen Sie
<code>FULL_LIFECYCLE_HOST_PROFILE</code> nicht manuell, um einen direkten oder
Compatibility-Build umzubenennen.

## Troubleshooting

| Symptom | Bedeutung | Sichere nächste Aktion |
|---|---|---|
| <code>BLOCKED: FRAMEWORK_ROOT is missing</code> / Exit <code>77</code> | Submodule-/Framework-Pfad ist nicht verfügbar | Submodule initialisieren oder <code>FRAMEWORK_ROOT</code> auf einen vertrauenswürdigen vorhandenen Framework-Checkout setzen |
| Build-Root wird abgewiesen | Ausgabe liegt im Checkout oder ist anderweitig unsicher | <code>BUILD_ROOT</code> oder <code>VERIFIED_RUN_PARENT</code> auf absoluten externen beschreibbaren Pfad setzen |
| Component Preparation fehlt | Cache/Snapshot fehlt oder Vorbereitung wurde übersprungen | <code>make prepare-runtime-components</code> ohne Skip-Flag ausführen |
| Compiler-Profil übersprungen | Optionales C-Profil ist nicht verfügbar | Dokumentierten Default-C17-Check verwenden oder Compiler mit optionalem Profil installieren |
| Config-Check schlägt fehl | Build, Host-Konfiguration oder Eingabedatei ist ungültig | Passendes Build-Target ausführen, sanitisiertes Log prüfen und dokumentierte Variablen verifizieren |

Kopieren Sie keine Roh-Logs mit Cookies, Authorization-Headers, TLS-Private-
Keys oder anderen sensitiven Werten in Issues oder kanonische Evidence.
