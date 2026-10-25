# Change Record: CR-20261025-sonar-setup-remediation

**Sprache:** [English](CR-20261025-sonar-setup-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261025-sonar-setup-remediation |
| Datum (UTC) | 2026-10-25 |
| Basis-Revision | `9f44647593bac7947113558c6ad183ab118e80af` |

## Motivation und Problemstellung

Die vollständige Parent-Sonar-Einrichtung machte kumulierte Coverage- und
Security-Findings, unvollständigen nativen Buildkontext, sechs Shell-Parserwarnungen,
eine ignorierte Python-Architekturperspektive und fehlende unabhängige
JSON-/YAML-/Workflow-Scope-Guards sichtbar. Frisches authentifiziertes
Basis-Readback bestätigte die Analyse `52df415d-2c24-43a3-a63a-de6e79c37d60`
am Basis-SHA: Hauptgate `ERROR`, Security Rating E und Coverage auf neuem Code
0,6 % bei unveränderten Anforderungen A/80 %. Der Zeitraum `previous_version`
beginnt am 2026-05-14. Der paginierte Bestand von 663 Dateien enthält folgende
neue abdeckbare Zeilen: Python 57.281; C 27.420; C++ 184; Go 6.284. Ein Ergebnis
über geänderte PR-Zeilen darf nicht mit diesem kumulierten Hauptgate gleichgesetzt
werden.

## Akzeptanzkriterien

Parent-Source-/Testgrenzen und eigenständige Repository-Grenzen, Python-/Go-Pins,
alle gepflegten Sprachscopes, CFamily-Test-Sources, Haupt-/Advisory-Trennung und
exakte SHA-Provenienz erhalten. Echte breitere Coverage erzeugen, unsichere
Evidence-bestimmte Lesepfade ablehnen, gepflegte JSON-/YAML-/Workflows schützen
und jeden Shell-/Native-/Architekturbefund beheben oder präzise einordnen. Der
vollständige Abschluss verlangt Scanner, terminale Serververarbeitung,
Haupt-/Advisory-Gates, Sprachausführung, Coverage-Import und Warnungs-Readback
des finalen SHA. Dieser Entwicklungsrecord weist diese finalen Serverkriterien
nicht nach.

## Implementierungsentscheidung und Begründung

Das angeforderte Scanner-CLI-Update pinnt `8.2.0.6438` für alle drei Jobs. Der offizielle Release sowie Linux-x64-Archiv, Prüfsummen- und Signaturendpunkt wurden geprüft; die Signaturprüfung der Action bleibt aktiviert. Historische Basisergebnisse beziehen sich weiterhin auf `8.1.0.6389`. Durch Zurücksetzen von `scannerVersion` lässt sich der vorherige Binary-Pin wiederherstellen.

Der Coverage-Helper wählt aussagekräftige Provenienz-, Artefakt-, Lifecycle- und
Sicherheitstests aus. Die Python-Messung umfasst produktive Namespaces und
Subprozesse, Go erfasst Standard-Build-Pakete aller vier Module mit 37 benannten
Szenarien, und instrumentierte Common-Tests erzeugen echte gcov-Reports.
Frische Verzeichnisse, ein sauberer Checkout und SHA-Prüfungen verhindern
Wiederverwendung; die Finalisierung kombiniert Coverage aller Producer-Prozesse
und validiert auflösbare Python-Pfade. Gate, Profil, New-Code-Definition und
produktive Coverage-Ausschlüsse wurden nicht verändert.

Der Scope-Guard schützt nun gepflegte JSON-/YAML-Dateien und ausführbare
Workflows unabhängig, erhält die explizite Behandlung negativer Fixtures und
verlangt analysierbare Komponenteninhalte statt einer README. Fünf
POSIX-Shell-Dateien verwenden gleichwertige Arithmetik-, Heredoc-/Prozessbesitz-
und Case-Syntax. Der Scheduler `ci/runtime/lifecycle/run-full-matrix-parallel.sh` behält sein
erforderliches `exec 8<>` für FIFOs, bis die analyzerbezogene Prüfung vorliegt.

AutoConfig bleibt bestehen, weil bestehende echte Compilation Databases
Parent-Units auslassen. CI stellt reale Apache-/APR-/ModSecurity-Header über
unterstützte Include-Einstellungen und eine Compiler-Probe bereit. Vollständiger
nativer Host-/Generated-Header-Scope und C/C++-Taint bleiben unvollständig;
kopierte HTX-Sources benötigen vor einer Datenbankmigration eine Zuordnung mit
erhaltener Provenienz.

Evidence-Reader binden an aufrufereigene Wurzeln und No-follow-Deskriptoren
regulärer Dateien. Wurzeln aus Dateiinhalten dürfen keine Zugriffsrechte
erweitern. Private Job-Summaries, gespeicherte Logs, native Metadateneingaben
und Report-/Cache-Pfade werden an ihren Consumer-Grenzen behandelt. Legitime
konfigurierte externe Pfade und kanonische schreibgeschützte Fixtures bleiben
getrennte zugelassene Eingaben.

Der genaue Architekturvorschlag entfernt 14 ausgeschlossene Framework-/MRTS-Gruppen
und benennt 30 Parent-Labels mit `/` um; Parent-Muster, vier verschachtelte
Gruppen, Metadaten und die bestehende leere Liste `constraints` bleiben erhalten.
Das autorisierte CLI-Update schlug mit HTTP 415 fehl; Readback bestätigte ein
unverändertes Servermodell.

## Geänderte Dateien

- `connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go`.

- `.github/workflows/sonarqube.yml`, `ci/sonar-coverage.ini`, `ci/checks/analysis/run-sonar-coverage.py`.
- `ci/checks/analysis/check-sonar-scope.py`, `tests/test_sonar_scope.py`, `tests/test_sonar_coverage.py`.
- `ci/lib/evidence_inputs.py`, die betroffenen Evidence-Report-Generatoren, Lifecycle-Consumer und den vertrauenswürdig konfigurierten Komponenten-Postprocess-Aufruf in `ci/provisioning/components/prepare-runtime-components.py`, `tests/test_evidence_input_security.py`, `tests/test_sonar_evidence_boundaries.py`.
- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`, `connectors/envoy/harness/run_envoy_composite_matrix.sh`, `connectors/lighttpd/harness/run_patched_full_lifecycle.sh`, `connectors/haproxy/htx-overlay/resolve-modsecurity.sh`, `connectors/haproxy/harness/run_haproxy_smoke.sh`.
- `config/analysis/sonar-python-architecture.patch.json`, `docs/sonarqube-analysis.md`, `docs/sonarqube-analysis.de.md` und dieses Change-Record-Paar.

## Ausgeführte Befehle

Zusätzliche aktuelle Verifikation: Alle 82 bestehenden Generated-Evidence-Integrity-Tests bestanden. Die finale ausgewählte Python-Suite bestand 61 Tests nach Ergänzung von Metadaten-Parser-/Status- und Source-/Build-Pfadkontrollen. Die gemessene Bootstrap-, Go-/Native-, gemessene Finalizer- und anschließende Merge-Sequenz bestand lokal; alle vier Modulreports und 71 nativen Reports bleiben echte Entwicklungsnachweise.

Das unabhängige Security-Kandidatenreview fand erneutes Öffnen von Metadatenpfaden und fehlende Freigaben für konfigurierte Komponenten. Beides wurde reproduziert und korrigiert; 41 gezielte Tests bestanden einschließlich vollständiger Generatorausgabe, tatsächlichem Postprocessor-Aufruf, Staleness und autorisierten SONAME-Kontrollen. Der integrierte ausgewählte Python-Coverage-Lauf bestand anschließend 54 Tests. Die finale CI muss alle Reports aus ihrem sauberen analysierten SHA neu erzeugen.

Beobachtete Entwicklungsnachweise, keine Qualifikation des finalen Heads oder
gehosteter Runtime:

| Befehl oder Verfahren | Beobachtetes Ergebnis |
| --- | --- |
| `rtk bypass python3 ci/tools/new-change-record.py create --name sonar-setup-remediation --date 2026-10-25 --base-revision 9f44647593bac7947113558c6ad183ab118e80af` | Beide nativen Record-Vorlagen angelegt. |
| Gezielte Suite `tests.test_sonar_scope` und echter Scope-Checker | 18 Tests bestanden; 136 CFamily-Units und vier Go-Module erhalten. |
| `sh -n`, `bash -n`, `shellcheck --severity=error` auf allen sechs gemeldeten Skripten | Bestanden; beweist kein Sonar-Parsing. |
| Gezielte Shell-bezogene Python-Suites | 65 Tests liefen zunächst mit sieben Skips wegen fehlendem Framework; anschließend bestanden alle zwölf Scheduler-Tests mit dem sauberen exakten Framework-Gitlink. |
| Entwicklungsläufe der Coverage-Producer | Python: 33 Tests bestanden, 185 produktive Dateien vertreten; Go: alle 37 ausgewählten Fälle bestanden; nativ: 71 gcov-Reports über 62 Repository-Dateien einschließlich aller 58 Common-C-Dateien. |
| `tests.test_sonar_coverage` | Sechs Provenienz-/Report-Regressionen bestanden. |
| Bestehende Apache-C17-Source-Kompilierung mit installierten Apache-/APR-/ModSecurity-Headern | Bestanden; nur Kompilierungsnachweis. |
| Authentifiziertes Finding-/Gate-/Modell-Readback über den kanonischen Wrapper | Basis-Gate-/Finding-/Modellzustand bestätigt; 46 Vulnerability-Findings triagiert, keine Finding-Transitions. |
| Modell-PATCH über den kanonischen Wrapper mit CLI `1.10.1` | HTTP 415; anschließendes Readback bestätigte keine Serveränderung. |
| `rtk bypass python3 ci/tools/new-change-record.py check` | PASS für Struktur, keine Evidence-Validierung. |
| `rtk make check-bilingual-docs PYTHON=/root/git/ModSecurity-conector/.venv/bin/python` | PASS nach Initialisierung des Task-eigenen exakten Framework-Checkouts; die anfänglichen Linkfehler wegen fehlendem Framework sind behoben. |
| `rtk make check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python FRAMEWORK_ROOT=/var/tmp/codex/ModSecurity-conector/worktrees/sonar-setup-remediation/modules/ModSecurity-test-Framework` | PASS; Repository-Pfadreferenzen und Dokumentationslinks. |
| Gezielte Scope-/Coverage-/Evidence-/Native-Reader-Suites | 67 Tests bestanden vor den abschließenden Review-Korrekturen. |
| Acht ausgewählte Sonar-/PR-Grenzmethoden aus `tests.test_ci_security_workflows.CiSecurityWorkflowTest`; `rtk bypass actionlint .github/workflows/sonarqube.yml`; `rtk bypass zizmor --offline .github/workflows/sonarqube.yml` | PASS; Zizmor behält eine vorhandene konfigurierte Unterdrückung. |
| Gezielte Prüfung der Guide-Links und des Modell-Payloads | Alle geänderten Guide-Links lösen auf; Payload entspricht dem vorbereiteten Vorschlag mit 32 eindeutigen slashfreien Labels und unveränderten Constraints. |

Lokale Coverage-Entwicklung verwendete Python `3.14.4` und Go `1.27.3`; CI bleibt
auf Python `3.14.7` und Go `1.27.1` gepinnt. Finale integrierte Befehlsergebnisse
und tatsächliche Links des aktuellen Heads müssen nach Source-Integration vom
Koordinator abgeglichen werden.

## Security-Auswirkung

Gespeicherte JSON-Evidence konnte fremde Hostdateien für Summaries, Auszüge,
Refresh-Klassifikation oder Hashes auswählen. Korrekturen erzwingen
aufrufereigene Eingabewurzeln und deskriptorbasierte Lesezugriffe auf reguläre
Dateien einschließlich Symlink-/Traversal-Kontrollen. Legitime private
Runtime-/Cache- und kanonische Source-Eingaben bleiben erhalten. Eine entfernte
Ausnutzbarkeit wurde nicht nachgewiesen. Vierzehn Basis-Findings haben konkrete
Gegennachweise durch bestehende Kontrollen oder Operatorberechtigung; die übrigen
Dateiinhalt-Gruppen benötigen frische Scanner-Verifikation. Kein Finding wurde
für ein anderes Rating akzeptiert, unterdrückt oder als False Positive markiert.
Dieser Record enthält keine Credentials oder sensiblen Rohpayloads.

## Exakte Einordnung der Basis-Findings

Diese 46 Keys gehören zur Basisanalyse `52df415d-2c24-43a3-a63a-de6e79c37d60`
bei `9f44647593bac7947113558c6ad183ab118e80af`. Bestehende Kontrollen oder
bestimmungsgemäße Operatorberechtigung sind technische Gegennachweise, keine
False-Positive-Transitions in Sonar. Eine frische PR-Analyse schließt alte
Mainbranch-Finding-Keys nicht automatisch. Die erste Tabelle erfasst 14 Findings
mit bestehenden Kontrollen/Operatorberechtigung; die zweite erfasst 32 Findings
mit Korrekturen an Consumer-Grenzen.

| Exakte Basis-Finding-Keys | Source-Grenze | Technische Einordnung |
| --- | --- | --- |
| `AaF0eroXXd_g6jxuNaF2` | `ci/lib/framework_revision_pins.py` (`_sha`, `_git`) | Validierung als kleingeschriebener ASCII-SHA-1 vor Git-Argumentaufbau; keine Shell. |
| `AaF0erogXd_g6jxuNaF3` | `ci/tools/prepare-reviewed-framework-handoff.py` | Operator wählt eine neue Ausgabepatchdatei; `open("x")` verhindert Überschreiben. Keine engere Berechtigungsgrenze nachgewiesen. |
| `AaF0errHXd_g6jxuNaGG` | `ci/runtime/common/hostruntime_preflight.py` (`_approved_lock_path`) | Runtime-/Source-Zugehörigkeit wird vor dem Lesen des Locks geprüft. |
| `AaF0erquXd_g6jxuNaGE` | `ci/runtime/lifecycle/write-transport-lifecycle-artifacts.py` | Konfigurationseingaben für Hashes durchlaufen Runtime-/Source- oder kanonische Framework-Source-Prüfung. |
| `AaF0erqkXd_g6jxuNaGD` | `ci/runtime/lifecycle/resolve-full-lifecycle-profile.py` | Manifest-Eingabe durchläuft vor dem Laden `runtime_or_source_artifact_path`. |
| `AaF0erq1Xd_g6jxuNaGF` | `ci/runtime/lifecycle/run-full-matrix-job.py` | Kanonische Repositories, geprüfte Runtime-Pfade und validierte Run-ID gehen als Argumentliste ohne Shell an den Subprozess. |
| `AaF0erqcXd_g6jxuNaGC`, `AaF0erqcXd_g6jxuNaGB` | `ci/runtime/lifecycle/run-full-matrix-resume.py` | Kanonische Wurzeln, erlaubte Connector-/CRS-/MRTS-Werte, begrenztes numerisches Timeout und `shell=False`. |
| `AaF0erpfXd_g6jxuNaF6`, `AaF0erpfXd_g6jxuNaF7` | `ci/runtime/lifecycle/run-verified-case.py` (`write_json`) | `runtime_artifact_path` prüft das Ziel unmittelbar vor dem Schreiben. |
| `AaF0erp1Xd_g6jxuNaGA` | `ci/runtime/lifecycle/run-verified-report-run.py` (`prepare_verified_run_context`) | Das Ziel `current-run-id` wird aus validierten Runtime-Pfaden gebildet. |
| `AaF0erp1Xd_g6jxuNaF8` | `ci/runtime/lifecycle/run-verified-report-run.py` | Manifest-Ausgabe verwendet kanonisches `report_path`; JSON liefert Nutzdaten, keine Zielberechtigung. |
| `AaF0erpTXd_g6jxuNaF5` | `ci/runtime/lifecycle/write-engine-lifecycle-artifacts.py` | Rules-/Source-Pfade werden geprüft; Hashing verwendet `O_NOFOLLOW` und prüft einen regulären Dateideskriptor. |
| `AaF0erukXd_g6jxuNaGe` | `connectors/lighttpd/harness/patched_event_validation.py` | Explizit vom Operator gewählte Events-Eingabe; keine zusätzliche HTTP- oder privilegierte Berechtigungsgrenze nachgewiesen. |

| Exakte Basis-Finding-Keys | Source-Grenze | Technische Einordnung |
| --- | --- | --- |
| `AaF0ersUXd_g6jxuNaGb`, `AaF0ersUXd_g6jxuNaGc`, `AaF0ersUXd_g6jxuNaGa` | `generate-nginx-mrts-http500-cluster-analysis.py` | JSON-/JSONL- und Auszugs-/Body-Lesezugriffe verwenden aufrufereigene `EvidenceInputs`; Metadaten dürfen abgelehnte Pfade nicht erneut öffnen. |
| `AaF0errtXd_g6jxuNaGR`, `AaF0errtXd_g6jxuNaGO`, `AaF0errtXd_g6jxuNaGP`, `AaF0errtXd_g6jxuNaGN`, `AaF0errtXd_g6jxuNaGU`, `AaF0errtXd_g6jxuNaGM`, `AaF0errtXd_g6jxuNaGV`, `AaF0errtXd_g6jxuNaGQ`, `AaF0errtXd_g6jxuNaGL`, `AaF0errtXd_g6jxuNaGS`, `AaF0errtXd_g6jxuNaGK`, `AaF0errtXd_g6jxuNaGT` | `generate-verified-runtime-mismatch-analysis.py` | Aufrufereigene Wurzeln begrenzen gespeicherte Evidence-Pfade, verschachtelte Includes, Stat-/Fingerprint- und Lesezugriffe. |
| `AaF0erkjXd_g6jxuNaFz`, `AaF0erkjXd_g6jxuNaFv`, `AaF0erkjXd_g6jxuNaFt`, `AaF0erkjXd_g6jxuNaFw`, `AaF0erkjXd_g6jxuNaFx`, `AaF0erkjXd_g6jxuNaFy`, `AaF0erkjXd_g6jxuNaFu`, `AaF0erkjXd_g6jxuNaFs`, `AaF0erkjXd_g6jxuNaFr` | `generated_report_utils.py` sinks via `run-native-case-comparison.py` | Tatsächlich geladenes Run-Verzeichnis erhalten, kanonische Fixture-Identität ableiten und begrenzte Byte-Nachweise an Metadaten geben. Allgemeine Helper-Policy bleibt unverändert. |
| `AaF0erp1Xd_g6jxuNaF-`, `AaF0erp1Xd_g6jxuNaF9`, `AaF0erp1Xd_g6jxuNaF_` | `run-verified-report-run.py` | Private Summary-Lesezugriffe begrenzen und gespeicherte Refresh-Logs auf aufrufseitiges `VERIFIED_RUN_LOG_ROOT` beschränken; unsichere Eingaben dürfen `consumer_stale` nicht vortäuschen. |
| `AaF0eroJXd_g6jxuNaF1`, `AaF0eroJXd_g6jxuNaF0` | `best_effort_evidence_readers.py` sinks via report consumers | Betroffene Aufrufer verwenden `EvidenceInputs.json/jsonl`; allgemeines Verhalten der Best-effort-Reader bleibt unverändert. |
| `AaF0errYXd_g6jxuNaGH`, `AaF0errYXd_g6jxuNaGI`, `AaF0errYXd_g6jxuNaGJ` | `update-runtime-reports.py` (`file_proof`) | Nur Cache-Wurzeln oder explizit aufrufseitig freigegebene Komponenten-Dateien erlauben Hashes; finale SONAME-Ziele müssen eigenständig zugelassen sein. |

Angriffs-/Kontrolltests stehen in `tests/test_evidence_input_security.py` und
`tests/test_sonar_evidence_boundaries.py`; für SHA-/Lock-Kontrollen bestehen auch
Tests in `tests/test_framework_revision_pins.py` und `tests/test_hostruntime_preflight.py`.
Weder entfernte Ausnutzbarkeit noch absoluter Schutz gegen gleichzeitige
Änderungen durch dieselbe UID wird behauptet. Einordnungen von Operatoreingaben
erlauben künftigen privilegierten Service-Aufrufern keine beliebigen Pfade.

## Runtime-Evidence

Beobachteter PR-Zwischenstand: `13b17cbedaa8b7d7fe382ae500052f1cac4ded16`,
[Lauf 40231379831](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40231379831),
[Draft-PR #421](https://github.com/Easton97-Jens/ModSecurity-conector/pull/421).
Diese saubere kanonische CI bestand alle 61 ausgewählten Python-Tests, 37
Go-Szenarien und die nativen Common-Tests und importierte die echte Python-XML,
vier Go-Reports und native gcov-Reports. Scanner CLI `8.2.0.6438` und CFamily
`6.85.0.102562` wurden ausgeführt. Hauptprojekt-Compute-Engine-Task
`AaF0ymveZaGJAnPJkdcR` endete mit `SUCCESS`; Analyse-ID:
`d812ee4b-6300-430f-89e9-11f7eb7b7745`.

Das [Haupt-PR-Gate](https://sonarcloud.io/dashboard?id=Easton97-Jens_ModSecurity-conector&pullRequest=421)
war allein wegen Security Rating E auf neuem Code `ERROR`. Coverage auf neuem
Code **80,5 %** bestand den unveränderten Grenzwert 80 %; auch Reliability,
Maintainability, Duplikation und Hotspot-Review bestanden. Drei offene Findings
`pythonsecurity:S2083` verweisen auf die drei `os.open`-Operationen in
`EvidenceInputs._descriptor`. Unabhängige Source-Untersuchung und gezielte
Negativ-/Kontrollproben bestätigten bereits wirksame Grenzen: lexikalische
Freigabe vor dem Öffnen, No-follow-Verzeichnisdeskriptoren für jede Komponente
und ein regulärer finaler Deskriptor. Externe/Geschwisterpfade, Parent-Traversal,
relative Pfade und NUL-Eingaben werden vor dem Öffnen abgelehnt. Native Comparison
ersetzt gespeichertes `run_dir` durch das tatsächlich geladene Verzeichnis.
Die drei Hauptprojekt-Keys sind `AaF0ynIMY4cSrRUGTduD`,
`AaF0ynIMY4cSrRUGTduC` und `AaF0ynIMY4cSrRUGTduB`. Sie bleiben auf dem Server
offen; es gab keine False-Positive-Transition oder Unterdrückung. Die technische
Einordnung ist `no_change`, potenzielle Analyzer-Fehlalarme, kein nachgewiesener
Bypass der Grenze.

Die C++20- und C++23-Advisory-Scannerjobs scheiterten beide an ihren tatsächlichen
Gates, jeweils `ERROR`; C++20-Coverage auf neuem Code war 82,7 %. Ihre
eigenständigen vollständigen Branchergebnisse ersetzen nicht das Haupt-PR-Ergebnis.
Die frische Advisory-Analyse zeigte außerdem vier Findings `c:S5782` am
`memchr` mit Maximallänge in HAProxys `bounded_cstring_length`. Die unabhängige
Untersuchung bestätigte NUL-terminierte kurze Stringliterale und
Verzeichniseintragsnamen in den gemeldeten Fällen. Der [C-Komiteeentwurf N1570,
Abschnitt 7.24.5.1 Absatz 2](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf)
definiert sequenzielles `memchr`-Verhalten bis zum ersten Treffer; ein größerer
Grenzwert als die terminierte Zeichenfolge belegt allein kein Überlesen. Auch
der [GNU-C-Library-Vertrag für Suchfunktionen](https://snapshots.sourceware.org/glibc/trunk/latest/manual/html_node/Search-Functions.html)
beschreibt die Suche bis zum ersten Treffer. Diese vier Findings sind potenzielle
Analyzer-Fehlalarme mit `no_change`, keine bestätigten Pufferüberläufe oder
Server-Transitions. C++20-Keys: `AaF0yz5SaVChWkKVlx_W`, `AaF0yz5SaVChWkKVlx_X`,
`AaF0yz5SaVChWkKVlx_Z`, `AaF0yz5SaVChWkKVlx_Y`.

Ein eigenständiger Probeaufbau mit dem exakten Helper-Quelltext bestand unter
C17, Compilerwarnungen als Fehler, AddressSanitizer und UndefinedBehaviorSanitizer:
die drei gemeldeten Literale, einen terminierten 256-Byte-Puffer mit Grenze 4096,
NUL am letzten erlaubten Byte, begrenzte Ablehnung ohne Terminator und unveränderte
Ausgabe bei ungültigen Argumenten. Es gab keinen Sanitizer-Befund. Der produktive
Helper bleibt unverändert.

Eine ergänzende Cache-Regression trennt Berechtigung und Existenz: Ein externes
SONAME-Ziel muss bei Existenz und Abwesenheit denselben abgelehnten Nachweis ohne
Digest liefern. Nicht strikte Auflösung vermeidet den früheren vorzeitigen
Missing-Status; die 19 Evidence-Input-Tests bestanden. Die Auflösung kann weiterhin
Linkmetadaten abfragen; dies behauptet keine vollständig beobachtungsfreien
Zugriffe außerhalb zugelassener Wurzeln.

Alle 136 nativen Units blieben im Scope. Der Qualitätswert stieg von 77,52 auf
**91,28/100**; Funktionen mit Parsingfehlern sanken von 414 auf **193/2.260**.
Unaufgelöste Projekt-Includes sanken von 115 auf **46/1.132**; externe Includes,
Modulimporte und Header-Units blieben in diesem Scan nicht unaufgelöst.
Fehlende Host-/Generated-Header betreffen weiterhin NGINX, HAProxy und lighttpd;
C/C++-Taint bleibt in AutoConfig deaktiviert. Vier ursprüngliche Shell-Warnungen
blieben aus (Apache-Cleanup, Envoy-Harness, lighttpd-Harness und HAProxy-Harness).
Die gültige FIFO-Umleitung `8<>` des Schedulers und die Case-Muster des
HAProxy-Resolvers erzeugten bei diesem SHA weiterhin Warnungen. Eine weitere
gleichwertige Resolver-Schreibweise bestand lokale Syntaxprüfungen, ShellCheck,
fünf Resolver-Tests und neun Vorher-/Nachher-Architekturfälle. Die 44 ungültigen
Architekturlabels führten weiterhin zum Ignorieren der Intended-Perspektive.
Diese Beobachtungen sind an diesen Zwischen-SHA gebunden; nachfolgende
Source-Änderungen verlangen einen neuen sauberen Scan und Readback des exakten Heads.

Der zweite CI-Versuch bei `161bfd7118b7480d0d997ff1bd4a5157f97ca1d8`, [Lauf 40230777535](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230777535), bestand kanonisches Python-/Go-Setup, deckte aber eine bestehende dateisystemabhängige Go-Fixture auf: Löschen und Neuerzeugen einer geschlossenen regulären Datei erlaubte sofortige Inode-Wiederverwendung im Replacement-during-Close-Test. Die Fixture benennt nun das Original vor Erzeugung des Ersatzes um und garantiert damit einen anderen lebenden Inode; Ersatz-Erhaltungsassertion und produktiver Listener bleiben unverändert. Unabhängiges Source-Review stützte die Diagnose; gezielte Ersatz- und reale Socket-Cleanup-Tests bestanden lokal 20 Wiederholungen. Dies korrigiert Testdeterminismus und behauptet keine absolute Immunität gegen Same-UID-Races.

Die erste PR-Head-CI bei `d094e1dacd1f540b1ffcf35b7da5bd4b3c255665`, [Lauf 40230520936](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230520936), bestand kanonisches Python-Setup und alle 61 ausgewählten Python-Tests. Go-Setup wählte `1.27.1`; danach scheiterte der Coverage-Schritt vor dem Scan, weil setup-go globales Python im PATH vor die venv setzte (`No module named coverage`). Der Workflow nennt nun für jeden Coverage-Producer, Merge und Finalizer explizit den venv-Interpreter. Für diesen fehlgeschlagenen Versuch wird weder Scanner-Upload noch Gate-Ergebnis behauptet.

Finale integrierte lokale Coverage-Pipeline: Python54Tests, Go37Tests und native Common-Tests bestanden; die Finalisierung führte die echte Go-/Native-Producer-Prozess-Coverage mit der Python-XML zusammen und validierte sämtliche Reportpfade. Reports sind ausdrücklich als Entwicklungsnachweise aus nicht committeten Änderungen markiert; die finale CI muss sie für den sauberen Commit neu erzeugen. Lokale Source-, Workflow-, zweisprachige, Link-, Archiv- und Whitespace-Prüfungen bestanden. Keine vollständige gehostete Runtime-Qualifikation wird behauptet.

Es wurde keine gehostete Connector-Runtime-Evidence erhoben oder beansprucht.
Coverage-Tests, Source-Kompilierung, statische Checks und Scanner-Readback
beweisen jeweils nur ihre eigene Ebene. Historischer Basis-CI-Lauf:
[Lauf 40224506735](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40224506735).
CI-/Sonar-Verarbeitung und Haupt-/Advisory-Ergebnisse des finalen Commits liegen
in diesem Record noch nicht vor.

## Bekannte Einschränkungen

| Ausgangsbefund | Einordnung bei Erstellung |
| --- | --- |
| Security Rating E | `weiterhin offen`: Zwischen-PR-Gate bleibt E wegen drei fachlich begrenzten Deskriptor-Findings; keine Server-Transitions. |
| Coverage auf neuem Code 0,6 % | `behoben und nachgewiesen` für Zwischen-PR-Coverage 80,5 %; kumulierte Mainbranch-Coverage von 80 % bleibt `weiterhin offen`. |
| Fehlende native Includes / Parsingfehler | `weiterhin offen`: Zwischenqualität 91,28 und 193/2.260 Funktionsfehler belegen Verbesserung; NGINX-/HAProxy-/lighttpd-Kontextlücken bleiben. |
| Vollständige Parent-C/C++-Taintanalyse in AutoConfig | `begründete Analyzergrenze`: nicht unterstützter Modus und unabhängige ausführbare Targets bestehen fort. |
| Ignoriertes Python-Modell | `extern blockiert`: Medientyp-Fähigkeit der autorisierten CLI fehlt; exakter Vorschlag liegt vor. |
| Sechs Shell-Parserwarnungen | Vier beim Zwischen-SHA `behoben und nachgewiesen`; gültige FIFO-Syntax ist eine `begründete Analyzergrenze`; Resolver-Warnung bis zum Scan der neuen Schreibweise `weiterhin offen`. |
| Fehlender JSON-/YAML-/Workflow-Scope-Guard | `behoben und nachgewiesen`: gezielte lokale Guard-Regressionen bestanden. |

Die Hauptprojekt-UUID ist `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`; die Modell-ID
ist `cb04d3a3-7c8f-447c-99f0-ca49c97f054f`. Die effektiven Rollen
`architectureadmin`/`admin` waren vorhanden. Der genaue Body in
`config/analysis/sonar-python-architecture.patch.json` muss über den Editor für
die beabsichtigte Architektur oder einen autorisierten Client mit
`application/merge-patch+json` unter
`PATCH /api/v2/architecture/models/cb04d3a3-7c8f-447c-99f0-ca49c97f054f`
angewendet werden; danach muss ein Scan die Perspektivanwendung belegen. Beide
Advisory-Projekte haben keine Modelle und blieben unverändert.

## Verbleibende Risiken

Native Connector-Host-Pfade, Go-Tags `libmodsecurity` und alternative Plattformen
bleiben ungemessen. AutoConfig fehlen weiterhin vollständige Host-/Generated-Header-
Kontexte und C/C++-Taintunterstützung. Das kumulierte Coverage-Gate kann trotz
eines bestandenen PR-Gates für geänderte Zeilen rot bleiben. Die Durchsetzung
einer repositoryweiten kompakten Standardsuite wird nicht behauptet. Frische Analyzer-Importe, dateibezogenes Parsing und terminale
Gates bleiben erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Finale integrierte Source-Prüfungen und CI-/Sonar-Verifikation des aktuellen
Heads wurden bei Erstellung dieses Records noch koordiniert. Vollständige
native Host-/Runtime-Matrizen und alle historischen Tests wurden durch die
Dokumentationsarbeit nicht ausgeführt; ihr Scope ist die wahrheitsgemäße
Dokumentation der ausgewählten Prüfung. Framework-/MRTS-Sources und Gitlink
wurden nicht verändert. Das Architekturupdate ist mit der unterstützten
Schnittstelle der aktuellen kanonischen CLI nicht abschließbar. Die vollständige
zweisprachige Prüfung und die native Dokumentations-Linkprüfung bestanden nach
Initialisierung des exakt gepinnten Framework-Checkouts. Das native
Parent-Dokumentationsziel verwendet seinen deklarierten Parent-Interpreter für
das Framework-eigene Linkskript mit ausschließlich Standardbibliothek; keine
Framework-Paketumgebung wurde geändert.

## Finaler Diff- und Review-Status

Dokumentation und vorbereiteter Modell-Payload beschreiben den überprüfbaren
Patch. Der finale integrierte Diff, genaue Task-SHA, PR-Link und terminale Checks
müssen vom Koordinator abgeglichen werden. Dieser Record behauptet weder
`complete`, `verified_pr`, Merge noch eine Änderung an `master`.
