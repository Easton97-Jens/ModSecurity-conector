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

- `.gitleaksignore` für die zwei exakten Dokumentations-Fingerprints öffentlicher Finding-IDs.
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
Ausnutzbarkeit wurde nicht nachgewiesen. Die Erstbewertung ordnete vierzehn Basis-Findings bestehenden Kontrollen oder Operatorberechtigung zu; die Marker-Bewertung war unvollständig und wird in der Fortsetzung ausdrücklich korrigiert; die übrigen
Dateiinhalt-Gruppen benötigen frische Scanner-Verifikation. Kein Finding wurde
für ein anderes Rating akzeptiert, unterdrückt oder als False Positive markiert.
Dieser Record enthält keine Credentials oder sensiblen Rohpayloads.

## Exakte Einordnung der Basis-Findings

Diese 46 Keys gehören zur Basisanalyse `52df415d-2c24-43a3-a63a-de6e79c37d60`
bei `9f44647593bac7947113558c6ad183ab118e80af`. Bestehende Kontrollen oder
bestimmungsgemäße Operatorberechtigung sind technische Gegennachweise, keine
False-Positive-Transitions in Sonar. Eine frische PR-Analyse schließt alte
Mainbranch-Finding-Keys nicht automatisch. Die erste Tabelle erfasst 14 ursprüngliche Kontroll-/Operatorbewertungen einschließlich der ausdrücklich korrigierten Marker-Bewertung; die zweite erfasst 32 Findings
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
| `AaF0erp1Xd_g6jxuNaGA` | `ci/runtime/lifecycle/run-verified-report-run.py` (`prepare_verified_run_context`) | Früherer Gegenbeleg unvollständig: kanonischer Zielpfad allein sicherte weder vorgezogenen Marker-Read noch Blatt-Symlink-/FIFO-Zugriffe. Fortsetzung reproduzierte den Defekt und korrigiert diese Bewertung; siehe Abschlussnachweis unten. |
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
Server-Transitions. C++20-Finding-IDs sind unter anderem `AaF0yz5SaVChWkKVlx_W`, `AaF0yz5SaVChWkKVlx_X`,
`AaF0yz5SaVChWkKVlx_Z`, `AaF0yz5SaVChWkKVlx_Y`.

Ein eigenständiger Probeaufbau mit dem exakten Helper-Quelltext bestand unter
C17, Compilerwarnungen als Fehler, AddressSanitizer und UndefinedBehaviorSanitizer:
die drei gemeldeten Literale, einen terminierten 256-Byte-Puffer mit Grenze 4096,
NUL am letzten erlaubten Byte, begrenzte Ablehnung ohne Terminator und unveränderte
Ausgabe bei ungültigen Argumenten. Es gab keinen Sanitizer-Befund. Der produktive
Helper bleibt unverändert.

Gitleaks meldete im PR-Bereich bei `8f632bdd` zwei generische API-Key-Treffer
für die öffentlichen Sonar-Finding-IDs oben, je einen pro Sprachfassung. Die
exakten Commit-/Pfad-/Regel-/Zeilen-Fingerprints stehen in `.gitleaksignore`;
keine Datei, Regel oder Credential-Schablone wird pauschal ausgeschlossen. Die
Formulierung vermeidet den Eindruck von Zugangsdaten. Diese technische
Nicht-Secret-Einordnung ändert keinen Sonar-Finding-Status. Der vollständige
Vier-Commit-PR-Bereich und aktuelle Record-Inhalt bestanden ohne ungeprüfte
Treffer; synthetische Credential-Muster lösten weiterhin die GitHub-PAT- und
generische API-Key-Regel aus, mit vollständiger Redigierung.

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

Der Folge-Source-Head `8f632bdd45f117ba7e8b025c1fbfac37cdad8cef`,
[Lauf 40232441972](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40232441972),
beendete die Serververarbeitung: Task `AaF01odhZaGJAnPJkdwU`, Analyse
`6759e9c6-2376-41a9-85cd-2df9de1d0ca6`, Status `SUCCESS`. Die Resolver-Warnung
fehlt nun: **Fünf von sechs ursprünglichen Shell-Warnungen sind nachgewiesen behoben**;
die unveränderte gültige Scheduler-FIFO-Syntax bleibt die dokumentierte Analyzergrenze.
Haupt-PR-Coverage bleibt bei 80,5 %, native Kennzahlen bleiben wie oben bei
91,28/193/46 und das Gate allein wegen der drei Deskriptor-Open-Findings auf
`ERROR`. Beide Advisory-Jobs scheiterten weiter an ihren tatsächlichen Gates.
Die zwei oben beschriebenen öffentlichen ID-Fehlalarme in Gitleaks benötigen
einen reinen Dokumentations-Folgecommit; dessen terminale CI-/Sonar-Nachweise
werden PR #421 beigefügt.

Der zweite CI-Versuch bei `161bfd7118b7480d0d997ff1bd4a5157f97ca1d8`, [Lauf 40230777535](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230777535), bestand kanonisches Python-/Go-Setup, deckte aber eine bestehende dateisystemabhängige Go-Fixture auf: Löschen und Neuerzeugen einer geschlossenen regulären Datei erlaubte sofortige Inode-Wiederverwendung im Replacement-during-Close-Test. Die Fixture benennt nun das Original vor Erzeugung des Ersatzes um und garantiert damit einen anderen lebenden Inode; Ersatz-Erhaltungsassertion und produktiver Listener bleiben unverändert. Unabhängiges Source-Review stützte die Diagnose; gezielte Ersatz- und reale Socket-Cleanup-Tests bestanden lokal 20 Wiederholungen. Dies korrigiert Testdeterminismus und behauptet keine absolute Immunität gegen Same-UID-Races.

Die erste PR-Head-CI bei `d094e1dacd1f540b1ffcf35b7da5bd4b3c255665`, [Lauf 40230520936](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40230520936), bestand kanonisches Python-Setup und alle 61 ausgewählten Python-Tests. Go-Setup wählte `1.27.1`; danach scheiterte der Coverage-Schritt vor dem Scan, weil setup-go globales Python im PATH vor die venv setzte (`No module named coverage`). Der Workflow nennt nun für jeden Coverage-Producer, Merge und Finalizer explizit den venv-Interpreter. Für diesen fehlgeschlagenen Versuch wird weder Scanner-Upload noch Gate-Ergebnis behauptet.

Finale integrierte lokale Coverage-Pipeline: Python54Tests, Go37Tests und native Common-Tests bestanden; die Finalisierung führte die echte Go-/Native-Producer-Prozess-Coverage mit der Python-XML zusammen und validierte sämtliche Reportpfade. Reports sind ausdrücklich als Entwicklungsnachweise aus nicht committeten Änderungen markiert; die finale CI muss sie für den sauberen Commit neu erzeugen. Lokale Source-, Workflow-, zweisprachige, Link-, Archiv- und Whitespace-Prüfungen bestanden. Keine vollständige gehostete Runtime-Qualifikation wird behauptet.

Zum ursprünglichen Erstellungszeitpunkt wurde keine gehostete Connector-Runtime-Evidence erhoben oder beansprucht. Die Fortsetzung unten ergänzt den tatsächlichen Runtime-Readback bei `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` mit ausdrücklich begrenztem Scope.
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
| Sechs Shell-Parserwarnungen | Fünf bei `8f632bdd` `behoben und nachgewiesen`; gültige Scheduler-FIFO-Syntax ist eine `begründete Analyzergrenze`. |
| Fehlender JSON-/YAML-/Workflow-Scope-Guard | `behoben und nachgewiesen`: gezielte lokale Guard-Regressionen bestanden. |

Die Hauptprojekt-UUID ist `608d0a7b-481a-4f7e-acbf-ae8eb07c3be2`; die Modell-ID
ist `cb04d3a3-7c8f-447c-99f0-ca49c97f054f`. Die effektiven Rollen
`architectureadmin`/`admin` waren vorhanden. Der genaue Body in
`config/analysis/sonar-python-architecture.patch.json` benötigt einen unterstützten autorisierten Client mit
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

## Gezielte Fortsetzung von PR #421

Der vollständige [EN/DE-Abschlussnachweis](../../../docs/sonarqube-pr421-closeout.de.md) ordnet die sechs aktuellen Anforderungen dem exakten bisherigen Head `4ec7581056889f8c70f44c6725f6bfa65a7fc45b` zu. Haupt-CE-Task `AaF03ulBdkEpBguA0oKZ`, Analyse `081d99d7-c136-4a67-b039-96507ad472a4`, endete erfolgreich; das Gate bleibt allein wegen drei offenen `pythonsecurity:S2083` auf ERROR. Die vollständigen Flüsse unterscheiden `request` von aufrufseitigem `run_dir`; pro Issue sind Kontrollen, neun tatsächlich bestandene Angriffs-/Kontrolltests und eine konkrete False-Positive-Vorlage dokumentiert. Keine Issue-Transition wurde ausgeführt.

Die 23 historischen Findings je Advisory wurden unabhängig mit vollständigen normalisierten Flüssen geprüft: 22 Paare haben vorgeschlagene `not_actionable`-Gegenbelege, ein Marker-Paar erforderte erneute Prüfung. Die frühere Aussage oben zu `AaF0erp1Xd_g6jxuNaGA` war unvollständig. Tests reproduzierten vor der Korrektur Symlink-Lesen und externes Überschreiben von `current-run-id`; legitime Wiederherstellung bestand. Der Runner prüft nun Verzeichnisvertrauen vor Markerzugriff, liest begrenzt über gehaltene No-follow-/Nonblocking-Deskriptoren, prüft Dateityp/Eigentum/Modus/Linkanzahl und schreibt atomar. 16 Grenztests und acht verwandte Runtime-Tests bestanden; ein unabhängiges Review bestand die vorherigen sieben Markerfälle ohne konkreten verbleibenden Bypass. Eine abschließende Root-Prüfung reproduzierte danach mit dem achten Marker-Test, dass ein kurzes os.read einen gültigen Präfix vor nachfolgenden ungültigen Bytes akzeptierte. Eine begrenzte Leseschleife bis EOF oder maximal 4.097 Bytes behebt dies; der neue Test schlug vorher fehl und alle 16 Grenztests bestanden danach. Dieser achte Fall war nicht Teil des vorherigen unabhängigen Sieben-Fall-Reviews. Das belegt lokale Grenzkontrolle, keinen entfernten Exploit oder finalen Sonarabschluss.

Der frische Architekturvergleich bestätigt unverändert 14 Framework-/MRTS-Entfernungen und 30 Parent-Labelumbenennungen bei erhaltenen Mustern, vier Untergruppen und Constraints. CLI `1.10.1` bietet weiterhin keinen Headerparameter; erneuter autorisierter PATCH ergab HTTP 415, Server-Readback blieb identisch. Der Abschlussnachweis enthält exakten Requestumfang und Schritte für einen unterstützten Zugang mit `application/merge-patch+json`, ohne Wrapperumgehung oder ungeprüfte UI-Anweisung. Perspektivanwendung bleibt extern blockiert.

Der neue native Kontext-Helper und sechs bestandene Tests ergänzen echte Vertragspins, Archivprüfsummen und Configure-Provenienz. Ein realer Entwicklungsversuch konfigurierte NGINX erfolgreich, scheiterte dann jedoch an einer Abweichung des neuen lighttpd-Patchaufrufs vom bestehenden Parent-Patchweg. Der zweite Versuch bestand den unveränderten kanonischen Patch-/Stamp-/ABI-Weg, stoppte aber vor lighttpd-Konfiguration wegen fehlendem configure im genehmigten Archiv. Der dritte vollständige Headerprep-Entwicklungslauf bestand mit Exit 0, unverändertem Upstream-autogen unter Bash und echter gepatchter lighttpd-Konfiguration. Das Manifest hält `4ec7581056889f8c70f44c6725f6bfa65a7fc45b`, `uncommitted_changes: true`, elf Include-Verzeichnisse sowie Archiv-/Patch-/Configure- und Generated-File-Hashes fest. Neue Sonar-Zahlen fehlen weiterhin. `ci/checks/analysis/prepare-sonar-native-context.py` und `tests/test_sonar_native_context.py` ergänzen die Implementierung; die Workflow-Messung findet vor dem Coverage-Finalizer statt. Die ausgewählte Suite enthält nun 75 Methoden (61 bisherige, acht Marker-, sechs Header-Tests); die frische instrumentierte lokale Auswahl bestand alle 75 Tests in 7,256 s; Helper-Entwicklungs-Coverage ist 82,48 % für Linien und Branches, kein Sonar-Gatewert. Saubere Head-CI steht aus. Kein komponenteneigenes Skript wurde geändert. Keine unvollständige Compilation Database ersetzt AutoConfig. 193/2.260 Parsingfehler und 46/1.132 ungelöste Includes bleiben historische Head-Werte, C/C++-Taint bleibt ausdrücklich unbewiesen.

Python-Simulationskostengrenze bei `runtime_path_utils.py:69` und beide Predecessor-Meldungen bestanden nachweislich bereits im Basis-Hauptprojekt und beiden Basis-Advisories. Die vollständigen aktuellen Advisories zeigen sie erneut; ihr Fehlen im gecachten Haupt-PR beweist keine Reparatur. FIFO-`exec 8<>` bleibt semantisch erhalten. Diese dokumentierten Analyzergrenzen werden weder ausgeschlossen noch als PR-Regression ausgegeben.

Runtime-Lauf `40233061042` endete tatsächlich für fünf Connectoren und Aggregate erfolgreich, einschließlich Apache-Job `121290821692`: ausgewählter SQLi-Blockfall mit HTTP 403/Regel `942270`, Audit und Cleanup bestanden. Kompaktartefakt `12614940472` wurde inhaltlich und per Digest geprüft; Aggregate `12614138658` meldet nur ausgewählten Fall mit 5 passed/0 failed/6 blocked/13 not_run, `coverage_complete: false`, `merge_eligible: false`. Das ersetzt keine vollständige Runtime-Qualifikation. PR-Coverage 80,5 %, Advisory-Branch-Coverage 82,7 % und kumulierte Master-Baseline 0,6 % bleiben getrennt.

Dieser Entwicklungsstand benötigt nach den Source-Änderungen einen neuen sauberen Head, terminale CI und exakte CE-/Analyse-/Gate-/Coverage-/Warnungsnachweise aller drei Projekte. Der PR bleibt Draft; kein Merge und keine Änderung an `master` erfolgten. Vollständige IDs, Gatebedingungen, Einschränkungen und Reststatus stehen im Abschlussnachweis. Die neuen Dateien sind handgepflegte technische Dokumentation, keine kanonischen Scannerartefakte.

### Beobachteter Source-Änderungshead

Der saubere Source-Commit `59bc0842cea90d4052c0d005218fae3aca14c2b2` wurde in Lauf `40238653971` analysiert. Exaktes Scannerkontext-/CE-/Analyse-Rücklesen steht im Abschlussdokument: alle drei Servertasks SUCCESS, alle Gates allein wegen Security-Rating E auf ERROR. Tatsächliche PR-New-Code-Coverage beträgt 82,3 %, Advisory-Branch-New-Code-Coverage 83,7 %, mit importierter Python-XML, vier Go-Reports und 71 gcov-Reports. Alle 136 nativen Units bleiben enthalten; echte Host-Header verbessern Parsing auf 2/2.263 fehlerhafte Funktionen und lösen alle Projekt-Includes auf (0/1.132), Qualität 95,81. Ein externes Include und aggregierte Klassen-/Statementfehler bleiben nicht lokalisiert; AutoConfig deaktiviert C/C++-Taint weiterhin ausdrücklich.

Vollständige Schwachstelleninventare enthalten Hauptprojekt 8, C++20 27 und C++23 24. Das reparierte Marker-Finding verschwindet in beiden Advisories; C++23 lässt zusätzlich drei unveränderte Evidence-Reader-Findings aus, die andere Projekte behalten, ohne belegten Grund oder Statusänderung. Fünf neue Helper-Findings je Projekt erhielten unabhängiges vollständiges Flussreview, sechs bestandene Helper-Tests, acht abgewiesene Ausgabeangriffe, erlaubte Private-Root-Kontrolle und echte Literal-argv-/Sentinel-Kontrolle. Jedes hat eine einzelne False-Positive-Vorlage; Grenzen bei konkurrierendem Pfadaustausch desselben Benutzers und Upstream-Pfadnamenverhalten sind benannt. Keine Server-Issues wurden geändert. Beide vollständigen Advisories behalten die bestehenden Python-Kosten-/Predecessor-Warnungen; die Hauptprojekt-Architekturperspektive wird weiter ignoriert, FIFO-Semantik bleibt erhalten.

Fünf Nicht-Sonar-CI-Workflows scheiterten an diesem Source-Head an der Entwicklerpfad-Dokumentationsprüfung. Beide Leserdokumente nutzen nun die portable Interpreterform; lokale Variablendokumentation (101 Referenzen), Zweisprachigkeits-, Pfad- und Linkprüfungen bestehen. Kein Validator wurde abgeschwächt. Diese reine Dokumentationskorrektur benötigt einen neuen finalen Head-CI-/Sonar-Lauf, dessen aktueller Nachweis im PR abgeglichen wird, um einen selbstreferenzierenden Dokumentationscommit zu vermeiden. Früherer erfolgreicher Runtime-Nachweis bleibt ausdrücklich an eigenen SHA und ausgewählten Fall gebunden. Gesamtergebnis bleibt partial; Architekturanwendung, Issue-Entscheidungen, native/Taint-Restlücken und finales aktuelles Head-Rücklesen behalten ihre dokumentierten Einordnungen.

## Vollständige New-Code-Finding-Fortsetzung, 2026-10-26

Diese Phase ersetzt die frühere auf Sicherheit begrenzte Inventur und die
Einordnung ohne Transitions. Sauberer Ausgangshead des PR ist
`1aa9646a65e5b3bd85b911c99ff40be73eee2cd3`; die folgenden lokalen
Sourcekorrekturen sind bei Erstellung uncommittete Entwicklungsänderungen.
Der Abschluss des genauen Heads benötigt neue CI und Serveranalyse nach deren
Commit. Die Evidenz dieser Phase liegt unter
`/var/tmp/codex/ModSecurity-conector/runs/pr421-all-findings-20261026`.
Finding-Inventar, Source-/Datenflusskontrollen, Einzelaktionen und Readbacks
bleiben getrennt von Scannerwarnungen, Annotationen, Hotspots und Coverage.

### Inventur und anfängliche Analysebindung

Die Hauptabfrage verwendete `sinceLeakPeriod=true`,
`issueStatuses=OPEN,CONFIRMED`, `ps=100` und Seiten 1/2 ohne Typfilter:
100 plus 50 Ergebnisse, genau 150 verschiedene Findings. Sprachzahlen:
122 Shell und 28 Python; Qualitäten: 141 Wartbarkeit, acht Sicherheit und eines
Zuverlässigkeit. Legacy-Schweregrade: sechs MINOR, 116 MAJOR, 25 CRITICAL und
drei BLOCKER. Die separat abgefragten Security-Hotspots des Hauptprojekts
betrugen null. Die Advisory-Abfragen verwenden denselben New-Code-/Status-Scope:
C++20 31 und C++23 16 verschiedene Findings. Die früheren Gesamtzahlen von
27/24 Schwachstellen haben einen anderen Scope.

| Projekt | Anfänglicher CE-Task | Anfängliche Analyse | Beobachtete Bindung |
| --- | --- | --- | --- |
| Hauptprojekt | `AaF1LkTSF1KaAz-ccMvg` | `3a8694d2-6375-45ed-8133-f6506f4c9533` | `SUCCESS`, Source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |
| C++20 | `AaF1LUoAdkEpBguA0qDb` | `64b9b52e-649f-4b38-ba7e-3a88825baad0` | `SUCCESS`, Source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |
| C++23 | `AaF1LYWYZaGJAnPJkfuW` | `d8e56714-5881-4d40-bd7c-5cb51d3a1dee` | `SUCCESS`, Source `1aa9646a65e5b3bd85b911c99ff40be73eee2cd3` |

Alle drei Gates standen vor den Einzelentscheidungen auf ERROR, mit
Sicherheitsratings E/E/C; alle anderen Gatebedingungen bestanden und keine
wurde ignoriert. Importierte Coverage: 82,3 % Haupt-PR-Coverage auf neuem Code
und 83,7 % Advisory-Branch-Coverage auf neuem Code. Python-XML, vier Go-Reports
und nativer gcov-Import bleiben erforderlich; Entwicklungscoverage ist kein
CI-/Serverimport. Diese Prozentwerte beheben keine kumulierte Master-Coverage.
`main-initial-inventory.json`, `main-initial-summary.json` und
`analysis-bindings-initial.json` enthalten Inventur-/Bindungsnachweise; neue
Scans müssen damit verglichen werden.

### Einzelne Sicherheitsentscheidungen und lokale weitere Korrekturen

Die unabhängige Prüfung hielt 21 getrennte Entscheidungen mit vollständigen
Datenflüssen, Aufrufstellen, Source-/Sink-Gegennachweisen, Angriffs-/erlaubten
Kontrollen und Einzelkommentaren in `current-security-triage.json` fest.
Fünfzehn Angriffs-/Kontrollgruppen bestanden sowohl gegen die Ausgangssource
als auch den eingefrorenen korrigierten Kandidaten. Deskriptor-Eigentums-,
No-follow- und Regular-File-Kontrollen bleiben erhalten. Der Request-Inhalt
wählt nicht die aufrufgesteuerte Reader-Wurzel; die Helper-Ausgabepfade stammen
aus dem ausdrücklichen Operator-Aufruf oder festen privaten CI-Kindpfaden.
Kontrollen für literale Argumentlisten, abgelehnte Git-Identitäten und
nichtliterale Vertragsdaten bestanden ebenfalls; neue Git-bezogene Findings
sind dadurch nicht vorab klassifiziert.

Der aktuelle Nutzer autorisierte nachgewiesene False-Positive-Entscheidungen
ausdrücklich. Jedes der 21 Findings erhielt eine eigene `FALSE_POSITIVE`-
Transition und einen präzisen Kommentar: acht Hauptprojekt, acht C++20 und fünf
C++23. `security-fp-actions.json` und die drei Projekt-Status-Readbacks bestätigen
jeden Status und zugehörigen Kommentar. Es wurde kein Risiko akzeptiert; Gates,
Regelprofile, Coverage-Schwellen, New-Code-Anforderungen und Scope-Ausschlüsse
wurden nicht gelockert. Advisory-Entscheidungen besitzen eigene Datenflussnachweise.

Alle 142 Nicht-Sicherheitsfindings des Hauptprojekts sind lokal im Code
korrigiert; ein neuer Scan steht aus. Überlappende Advisory-Korrekturen betreffen
23/11 weitere Findings. Envoy besitzt 87 lokale Finding-Korrekturen, darunter
POSIX-sichere benannte Funktionsargumente und explizite No-op-Defaults. Die drei
HAProxy-/lighttpd-Skripte besitzen 35 Korrekturen, darunter gleichwertige
Verzweigungsvereinfachung, benannte Argumente und zentralisierte Cleanup-Texte.
Python-Korrekturen zerlegen komplexe Receipt-/Coverage-/Reportfunktionen,
erhalten die ASCII-Identitätsvalidierung und präzisieren beabsichtigte
Exception-Grenzen. Sicherheitsrelevante Deskriptor- und konfigurierte
Freigabekontrollen bleiben erhalten. Geänderte Dateien und Einzelnachweise stehen
in `envoy-shell-triage.json`, `host-shell-triage.json` und den Python-/nativen
Triage-Records. Aus den Codeänderungen wird kein Scannerabschluss abgeleitet.

Vor Veröffentlichung beobachtete Validierung: 19 Basis-Evidenztests bestanden
in 3,696 s; die fokussierte integrierte Auswahl bestand 44 Methoden in 4,711 s;
die instrumentierte integrierte Auswahl bestand 80 Python-Methoden in 7,829 s
mit gepinnter coverage 7.17.0. Elf tatsächliche Case-Identitätskontrollen
bestanden. Envoys 17 bestehende Tests und 42 Vorher-/Nachher-Charakterisierungen
bestanden; alle 20 eingebetteten Python-Heredocs waren bytegleich. Die
Host-Shell-Validierung bestand zwölf ausgewählte Tests und neun Lighttpd-
Äquivalenzfälle in 18 Ausführungen. Die Shellsyntax geänderter Skripte bestand.
ShellCheck behielt sechs bestehende Envoy- und zwölf bestehende HAProxy-Warnungen;
ein pauschaler ShellCheck-Erfolg wird nicht behauptet. Die gültige
FIFO-Semantik des Schedulers mit `exec 8<>` bleibt unverändert.

### Echter nativer Kontext und verbleibende Analyzergrenzen

Das vollständige Scannerlog identifizierte das verbleibende externe Include
als `ngx_http_v2.h`. Dem Distributions-SDK von ModSecurity `3.0.12` fehlten
`msc_rules_error_cleanup` und `msc_intervention_cleanup`, die der unveränderte
C++-Evaluator verwendet. Eine echte negative Syntaxprobe reproduzierte diese
API-Fehler; die genauen freigegebenen öffentlichen Header von `3.0.17`
kompilierten den unveränderten Evaluator unter C++17 mit Warnungen als Fehlern.
Kein Cleanup-Aufruf wurde entfernt, kein Header oder Compilerbefehl erfunden
und kein Feature-Define hinzugedichtet.

Die unveränderliche Herkunftskette lautet Framework-Gitlink
`99a7985c1be92a2297b1b59208f64df6768f2cbf`, Vertragsblob
`496b5d8e0ec70d6d31f91aeaf08024050a5698ea`, freigegebener offizieller
ModSecurity-Commit `1925753989ccce977cdaae417b55c9726c7cf02c` und öffentlicher
Headerbaum `8daab1d1734506b687b21efd44169c273eabca6a`. Die Source-Datenbeschaffung
initialisiert und beschreibt keine Framework-/MRTS-Worktrees. Freigegebene
Header stehen vor apt-Headern; der echte NGINX-Include-Pfad `src/http/v2` kommt
hinzu, ohne ein HTTP/2-Featureprofil zu aktivieren. Passiver Vertragsparser und
Git-Objekt-Identitätsprüfungen des Helpers lehnen nicht unterstützte Vertragsdaten ab.

Elf native Kontexttestmethoden bestanden in 0,033 s. Die vollständige echte
Entwicklungsvorbereitung bestand mit Exit 0: NGINX 1.31.6, HAProxy 3.2.25,
lighttpd 1.4.85, ModSecurity 3.0.17, 13 echte Include-Verzeichnisse und elf
generierte/Source-Hashes, einschließlich tatsächlichem NGINX-Configure sowie
unverändertem kanonischem lighttpd-Patch, Bash-Autogen- und Configure-Pfad.
`native-context-integrated1/manifest.json` zeichnet Entwicklungssource und
Dirty-Status auf. Neue Parsing-/Include-Zahlen von null sind damit nicht
bewiesen. Alle unabhängigen Connector-Ziele und benötigten Varianten müssen
abgedeckt bleiben; keine partielle Compilation Database wurde eingesetzt.

Die offizielle CFamily-Dokumentation schließt C/C++-Taint in AutoConfig sowie
mit mehreren Codevarianten aus; projektweite Analyse nimmt außerdem ein
gemeinsam gelinktes Target an. Reporting-Standard-Override oder höherer Score
belegen keine Taintabdeckung. Python-Simulationskostengrenze und beide
Predecessor-Warnungen behalten ihre Basisgegennachweise und werden nicht als
PR-Regressionen behauptet. Scanner CLI 8.2.0.6438 und Scan-Action 8.3.0 wurden
gegen offizielle Release-/Inputverträge geprüft; signierte Scannerinstallation
und Sprach-/Reportparameterverträge bleiben erhalten.

### Architekturfähigkeit und Bereitschaft

Ein frischer Modellabruf bestätigte den genauen versionierten Patch:
14 ausgeschlossene Framework-/MRTS-Gruppen entfernen, 30 Parent-Labels umbenennen,
Parent-Muster, Metadaten, vier verschachtelte Gruppen und Constraints erhalten.
Der autorisierte Wiederholungsversuch lieferte erneut HTTP 415; das Readback
blieb identisch, aufgezeichnet in `architecture-application-result.json`.
Der erforderliche Medientyp lautet `application/merge-patch+json`. Die
installierte/neueste veröffentlichte CLI `1.10.1.16776` aus
`ef0f792b7c4bb18d2432015baae4984a6cd50d99` unterstützt im veröffentlichten
API-/HTTP-Client nur JSON/Form; Architekturkommandos unveröffentlichter Sources
sind kein installierter unterstützter Zugang. Der geprüfte Body benötigt einen
unterstützten autorisierten Merge-Patch-Client mit Einbindung des
vorgeschriebenen Wrappers, anschließend exaktes Modell-Readback und einen neuen
Scan als Perspektivanwendungsnachweis. Kein ungeprüfter UI-Import-/Editorweg
oder Credential-Wrapper-Bypass wird vorgeschrieben. Der Architekturstatus bleibt
`extern blockiert`.

Das aktive Master-Ruleset `19138299` fordert `actions`, `bounded-c-cpp`,
`envoy-go`, `traefik-go`, `actionlint` und `zizmor`, alle am Ausgangshead bestanden;
strikte Aktualität zur Basis und aufgelöste Review-Threads sind erforderlich.
Pflichtfreigaben sind null, Reviews/Threads waren leer und in den geprüften
Orten wurde keine CODEOWNERS gefunden. Klassische Branch-Protection-Details
lieferten 403; das belegt kein fehlendes Ruleset-Enforcement. Die lokale
Delivery-Policy fordert weiterhin das zutreffende aktuelle Haupt-Sonar-Gate.

Der Runtime-Workflow des Ausgangsheads `40239931958` endete erfolgreich für
fünf Connectoren und Aggregat; Apache-Job `121309664630` bewies den ausgewählten
SQLi-Fall mit HTTP 403, Audit und Cleanup. Die aggregierte Vertragsabdeckung
betrug fünf bestanden, null fehlgeschlagen, sechs blockiert und dreizehn nicht
ausgeführt, mit `coverage_complete: false` und `merge_eligible: false`. Das
qualifiziert keine vollständige Matrix. Aktuelle Artefakt-ZIP-Inhalte wurden
nicht unabhängig geprüft. Alle 18 Nicht-Sonar-PR-Workflows des Ausgangsheads
bestanden; diese Ergebnisse validieren nicht den nächsten Head.

Die Sourcekorrekturen sind lokal validiert, die einzelnen False-Positive-
Entscheidungen angewendet und zurückgelesen, nativer Scannerabschluss bleibt
`weiterhin offen`, und dokumentierte Taint-/Python-/FIFO-Grenzen bleiben
`begründete Analyzergrenze`. Finale saubere Head-Inventare, je Projekt
Source-SHA/Analyse/terminale Verarbeitung/Gates/Importe/Warnungen und CI werden
weiterhin benötigt. PR #421 bleibt Draft, solange Pflichtnachweise oder die
Architekturanwendung fehlen. Kein Merge, keine Master-Änderung, Gateabsenkung
oder breiter Ausschluss erfolgte. Der Koordinator hält die späteren genauen
Source-/Head-Ergebnisse im PR und aktuellen Abschlussnachweis fest; dieser
Entwicklungsphasen-Record behauptet keinen Abschluss.

### Dokumentationsvalidierung dieser Phase

Die vier Dokumentationsänderungen bestanden folgende tatsächlich ausgeführten
Befehle im Task-Worktree. Variablenreferenzen: 101; Zweisprachigkeitsprüfung,
Repository-Pfade und Framework-eigener nativer Linkchecker: bestanden.
Die Change-Record-Prüfung belegt nur die Struktur; Whitespace bestand.
Ein getrennter Vergleich bestätigte identische Anzahlen technischer
Inline-Literale und identische Codeblöcke in beiden EN/DE-Paaren.
Diese Dokumentationsprüfungen belegen keine finale CI, keinen Sonarabschluss
und keine Laufzeitqualifikation; dafür bleibt die Prüfung des genauen Heads
durch den Koordinator erforderlich.

```text
rtk make check-variable-documentation check-bilingual-docs check-doc-links PYTHON=/root/git/ModSecurity-conector/.venv/bin/python
rtk bypass /root/git/ModSecurity-conector/.venv/bin/python ci/tools/new-change-record.py check
rtk bypass git diff --check
```

### Vollständige Triage und Annotation-/Source-Encoding-Follow-up

Die [vollständige Einzeltriage](../../../docs/sonarqube-pr421-triage.de.md) erfasst alle 150 Haupt-Issues und getrennte 31/16 Advisory-New-Code-Issues samt Code-/Flusskontext, Qualität/Schweregrad, Maßnahme und Nachweis. Alle eindeutigen IDs stimmen mit API-Seitengesamtzahlen überein; dies ist keine Security-only-Auswahl. Der aktuelle Abschluss ersetzt frühere No-Transition-/Current-Zahlenformulierungen und erhält ihre datierten Nachweise.

Alle 92 GitHub-Annotationen wurden über die installierte authentifizierte GitHub-CLI tatsächlich geladen/abgeglichen, nachdem der Plugin-Endpunkt abgewiesen wurde. Kategorien sind 50 Sonar-Inline-Issuereferenzen, 36 Runner-Image-Hinweise, zwei Go-Cachewarnungen, drei Scanner-Exitannotationen und eine CodeQL-Fallbackwarnung. Annotationsstufen/-zahlen sind keine zusätzlichen Sonar-Issues oder CI-Jobergebnisse. Derselbe unterstützte CLI-Lesezugriff belegt fehlende klassische Branch Protection (404); aktives Ruleset `19138299` ist maßgeblich.

Die zwei Cachewarnungen entsprechen tatsächlich fehlgeschlagenem Root-Modul-Lookup. `.github/workflows/ci-security-codeql.yml` verwendet nun vorhandene Envoy-`go.mod`/`go.sum` und natives Traefik-`go.mod` über `cache-dependency-path`, ohne Root-Modul/Prüfsumme zu erfinden oder Caching abzuschalten. Trusted-Go-Versionsauflösung und CodeQL-Lock/-Build/-Berechtigungen bleiben unverändert. Actionlint und Zizmor bestanden beide geänderten Workflows; drei bestehende CodeQL-Versions-/Lock-/Berechtigungsmethoden bestanden in 0.005 s. Aktuelle Head-CI muss Warnungsabschluss bestätigen.

`connectors/envoy/config/lib/tls_yaml_render.sh` enthielt ein wörtliches CR im gültigen Abweisungspattern: Git-Blame enumerierte 28 LF-Zeilen, universelle Reader 29. Darstellung desselben Bytes über gequotetes `$(printf '\r')` erhält Matching/Escaping/Status und ergibt 28/28 Sourcezeilen. Zwölf tatsächliche Vorher-/Nachher-Shellkontrollen haben identischen Status/stdout/stderr; zwei bestehende TLS-Methoden bestanden in 0.088 s. `tests/test_envoy_transport_hardening_contract.py` prüft nun sowohl abgewiesene LF- als auch CR-Pfade ohne Ausgabe. Korrigiert wird Sourcerepräsentation, keine Runtime-Akzeptanz; nächster Scanner muss Blame-Wiederherstellung belegen. Keine neue PR-verursachte Regression wird behauptet. Die Unused-Path-Fixture des nativen Tests wurde zusätzlich vor `assertRaises` verschoben; ihre bestehende Negativmethode bestand in 0.001 s.

Lokale echte vollständige Headervorbereitung und gemessener Python-Producer mit 80 Methoden bestanden; alle entsprechenden Entwicklungsnachweise sind dirty markiert und kein sauberer Head-Coverage-Import. Unabhängiges vollständiges Diffreview erfasste alle 37 geänderten Pfade vor dem neuen Triage-Paar; keine bestätigte Code-/Testregression gefunden. Finale Dokumentationschecks enthalten nun 103 Variablenreferenzen. Alle Sourcekorrekturen benötigen weiterhin neuen exakten Head-Scan, vollständigen Alt-/Neu-Issuevergleich und terminale CI; lokale Ergebnisse begründen keinen Merge oder Readiness-Anspruch.

## Gemessener Source-Scan vor dem nächsten Korrekturhead

Gültig für Source `900dddb49c43ec4479c4b75a91071cadb97893c4`. Dies ersetzt die früheren Pending-Aussagen zu den 197 Ausgangs-IDs und nativen Parsingresten. Es ist kein Nachweis für einen späteren Dokumentations-/Korrekturhead; der finale exakte Head wird nach dem Push im PR zurückgelesen.

| Project | CE task | Analysis ID | Processing / gate | Coverage |
| --- | --- | --- | --- | --- |
| Easton97-Jens_ModSecurity-conector | `AaF2aMqHwSmsgR9Bx9Lu` | `aed6171b-c278-4868-8f8c-ade346d8c306` | `SUCCESS` / `ERROR` | 83.3% |
| Easton97-Jens_ModSecurity-conector_cpp20_advisory | `AaF2aiZ-wSmsgR9Bx9Pa` | `683e6e06-c8f5-49a7-b495-541a0e637fb9` | `SUCCESS` / `ERROR` | 84.4% |
| Easton97-Jens_ModSecurity-conector_cpp23_advisory | `AaF2aeHVF1KaAz-ccXOp` | `37a38445-53d1-46e6-99d9-98ff4ffaea0e` | `SUCCESS` / `ERROR` | 84.4% |

Alle Ausgangs-IDs wurden einzeln zurückgelesen: Hauptprojekt 142 `FIXED` + 8 `FALSE_POSITIVE`, C++20 23 `FIXED` + 8 `FALSE_POSITIVE`, C++23 11 `FIXED` + 5 `FALSE_POSITIVE`. Je Projekt kamen zwei eigene neue IDs hinzu; die sechs neuen Findings stehen getrennt in der Einzeltriage. Noch kein vollständiger Abschluss aller 203 IDs wird behauptet.

Die Gates standen bei diesem Scan allein wegen `new_security_rating` 3 statt höchstens 1 auf ERROR. Andere Bedingungen bestanden: Zuverlässigkeit/Wartbarkeit 1, Duplikation 0.0%, Hotspotreview 100.0%, Coverage mindestens 80%; keine Bedingung wurde ignoriert. Die 83.3% sind Haupt-PR-Coverage, 84.4% Advisory-Branch-New-Code-Coverage; die kumulierte Master-Coverage bleibt getrennt.

Alle drei Scans importierten ein Python-XML, vier Go-Reports und 71 gcov-Reports. Scope bleibt 1,350 Sources, 243 Tests, 136 native Translation Units und vier Go-Module. Tatsächliche native Ergebnisse: Qualität 100/100, Fehler in 0/2,263 Funktionen, 0/6 Klassen, 0/33,778 Statements; 0/1,132 unaufgelöste Projekt-Includes und null externe Includereste. Das belegt den gemessenen Parsing-/Include-Abschluss; unabhängige Targets/Varianten und in AutoConfig deaktiviertes C/C++-Taint bleiben getrennte Grenzen.

Hauptwarnungen bleiben die 44 ungültigen Architekturlabels, der gültige FIFO-Parserfall und die TLS-Meldung „changed but without having changed lines“. Fehlender TLS-Blame wird nicht mehr gemeldet; die verbliebene Änderungszeilenwarnung verhindert eine vollständige TLS-Warnungsabschlussbehauptung. Beide Advisories behalten vier WARN-Meldungen (FIFO-Parser, zwei Predecessor, FIFO-Syntax) und den INFO-Simulationskostenskip bei `ci/lib/runtime_path_utils.py:69`; das sind keine sechs weiteren Issue-IDs.

Beide früheren CodeQL-Warnungen zum fehlenden Root-go.mod sind behoben. Eine andere Traefik-Logwarnung bleibt: Modulcache-Verzeichnis existiert nicht, da das ausgewählte Modul nur die Standardbibliothek nutzt und keine Abhängigkeiten benötigt. Kein künstlicher Cacheordner und keine Cacheabschaltung wurden eingeführt. Go-Overlay-Cachemiss und C/C++-Fallback auf eine normale vollständige Datenbank bleiben getrennte Hinweise bei erfolgreicher Analyse.

Die neue `python:S3776`-Komplexität im Vertragsdecoder ist im nächsten Korrekturhead lokal zerlegt; elf Tests einschließlich zweier passiver ungültiger Vertragswerte bestanden in 0.035 s. Die drei neuen `pythonsecurity:S8705`-Git-Findings wurden separat geprüft und mit eigenen Kommentaren als FP umgestellt und zurückgelesen; Details folgen unten. Erneute Analyse bleibt ausstehend; die begrenzte Runtime des 900-Sources ist nun terminal nachgewiesen. Architektur bleibt extern blockiert, PR Draft.

Nachweisdateien: `900-evidence-summary.json`, `900-analysis-bindings.json`, `900-*-baseline-readback.json`, `900-*-log-evidence.json`, `900-github-codeql-warnings.json` unter dem externen Run `pr421-all-findings-20261026`.


### Neue Git-FPs: angewendete Einzelentscheidungen

Alle drei neuen `pythonsecurity:S8705`-IDs wurden getrennt anhand vollständiger
20-Location-Flüsse und zehn tatsächlicher Aufrufstellen geprüft. Fünf echte
Git-Argumentproben sowie eine erlaubte und vier abgewiesene Output-Root-Kontrollen
bestanden; sicherheitsrelevante Kontrollen sind im nächsten Kandidaten
AST-identisch. Git-global-config, PATH, Templates und `GIT_*` sind ausdrücklich
nicht isoliert; diese Prüfung belegt keinen Schutz gegen einen bereits
kompromittierten Ausführungsbenutzer oder dessen Toolkonfiguration.

Jedes Finding erhielt seinen eigenen konkreten FP-Kommentar und eine
`FALSE_POSITIVE`-Transition; Status und genauer Kommentar wurden einzeln
zurückgelesen. Nachweise: `900-new-security-triage.json`,
`900-new-fp-actions.json`, `main-900-fp-readback.json`,
`cpp20-900-fp-readback.json`, `cpp23-900-fp-readback.json`. Damit sind insgesamt
24 FPs angewendet (9/9/6); 176 Ausgangs-IDs sind `FIXED`, drei neue
Komplexitäts-IDs bleiben lokal korrigiert vor neuem Scannerbeweis.

### Terminaler Runtime-Nachweis am 900-Source

[Runtime-Lauf 40267347652](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/40267347652)
ist am Source `900dddb49c43ec4479c4b75a91071cadb97893c4` terminal SUCCESS für
alle sechs Jobs, einschließlich Apache `121392518485` und Aggregat
`121396280699`. Tatsächlicher Apache-Fall `crs_sqli_anomaly_block`: HTTP 403,
deny, CRS-Regel `942270`, Profil `native-httpd-module`, Cleanup vollständig,
Apache-Validierung bestanden. Gelesene Artefakt-JSONs bestätigen genau fünf
technisch bestandene Zellen und funktional nur `selected_crs_block_case_only`:
24 Vertragszeilen mit fünf bestanden, null fehlgeschlagen, sechs blockiert und
dreizehn nicht ausgeführt; `coverage_complete: false`, `merge_eligible: false`.

Identität: Framework `99a7985c1be92a2297b1b59208f64df6768f2cbf`, MRTS
`8a6bb546c4c81d8ffc7be801dceac60c6925685f`, CRS
`e03a4f6dabc7a30ebd8c52c97d28a154f590a48f`, Profil
`with-crs-no-mrts-40267347652-1`. Apache-/HAProxy-Allow-Kontrolle bleibt
`not_observed`, no-MRTS ist `workflow/source_declared`; bei Envoy/lighttpd/Traefik
sind Allow 200, Block 403 und no-MRTS `runtime_observed`. Rohes Apache-Audit und
Ergebnisse liegen hier nur als Hashreferenzen vor. Artefakt-JSON wurde aus
verwaltet heruntergeladenen ZIP-Bytes im Speicher gelesen; ein unabhängig
verifizierter ZIP-Digest wird nicht behauptet. Das ist kein Nachweis für die
vollständige Runtime-Matrix oder einen späteren Sourcehead. Quellen:
`900-runtime-terminal.json`, `900-runtime-apache-artifact-json.json`,
`900-runtime-aggregate-artifact-json.json`.

### Separater frischer Master-Coverage-Readback

Authentifiziertes Readback am 2026-10-26 um 04:25 UTC bestätigt weiterhin
Master-Coverage 0.6% und Master-New-Code-Coverage 0.6345357841049332%.
Die letzte Masteranalyse `52df415d-2c24-43a3-a63a-de6e79c37d60` stammt von
`2026-10-25T19:08:47+0000`, Revision
`9f44647593bac7947113558c6ad183ab118e80af`: 91,169 abdeckbare Zeilen,
90,641 unabgedeckte Zeilen, 394 Bedingungen und 341 unabgedeckte Bedingungen.
`master-coverage-readback.json` ist der getrennte aktuelle Lese-Nachweis;
die verbesserten PR-/Advisory-Prozente beheben diese Mastergrößen nicht.

## Aktueller gemessener Sourceabschluss — 2026-10-26

Source `d5450cd3d88e7ac20c5fdee3e4173c65f5626ca8`. Alle drei CI-Analysejobs und terminalen Servertasks sind erfolgreich; alle Gates sind `OK`. Dies ist der genaue Sourceabschluss vor dem Dokumentationscommit. Der folgende Dokumentationshead benötigt eigene neue CI-/Sonar-Nachweise im PR; diese Ergebnisse werden nicht auf ihn übertragen.

| Project | CE task | Analysis ID | Processing / gate | New-code coverage |
| --- | --- | --- | --- | --- |
| Easton97-Jens_ModSecurity-conector | `AaF2d1wrF1KaAz-ccYSb` | `5ca2a23e-9296-4c2d-8fbc-fa4d9a6b97eb` | `SUCCESS` / `OK` | 83.5% |
| Easton97-Jens_ModSecurity-conector_cpp20_advisory | `AaF2dvPAk-m4lzyjm-LE` | `fd25c86a-c9f5-4cb3-8cd5-6e2a3e59ba69` | `SUCCESS` / `OK` | 84.6% |
| Easton97-Jens_ModSecurity-conector_cpp23_advisory | `AaF2dqhewSmsgR9Bx97p` | `085ce801-0376-4963-9864-25391aae003b` | `SUCCESS` / `OK` | 84.6% |

| Project | Reviewed IDs | `FIXED` | `FALSE_POSITIVE` | OPEN/CONFIRMED | Hotspots |
| --- | ---: | ---: | ---: | ---: | ---: |
| Main PR 421 | 152 | 143 | 9 | 0 | 0 |
| C++20 advisory | 33 | 24 | 9 | 0 | 0 |
| C++23 advisory | 18 | 12 | 6 | 0 | 0 |
| Total | 203 | 179 | 24 | 0 | 0 |

Die 203 verschiedenen IDs bestehen aus den vollständig paginierten Ausgangsinventaren 150/31/16 und sechs Neufunden. Jede ID wurde separat zurückgelesen. Alle Typen im New-Code-OPEN/CONFIRMED-Scope ergeben null; getrennte Hotspotabfragen ebenfalls null. Die drei neuen Komplexitäts-IDs sind tatsächlich `FIXED`; die drei neuen Git-Sicherheits-IDs bleiben mit einzeln geprüften Kommentaren `FALSE_POSITIVE`. Kein Risiko wurde akzeptiert; keine Regel, Schwelle, Gatebedingung oder New-Code-Anforderung wurde abgeschwächt und kein breiter Ausschluss eingeführt.

Alle sechs unveränderten Gatebedingungen bestehen: Reliability/Security/Maintainability jeweils 1 bei höchstens 1; `new_coverage` 83.5/84.6/84.6 bei mindestens 80; `new_duplicated_lines_density` 0.0 bei höchstens 3; `new_security_hotspots_reviewed` 100.0 bei mindestens 100. Keine Bedingung wurde ignoriert. Die 83.5% sind PR-Coverage, 84.6% Advisory-Branch-New-Code-Coverage. Frisches separates Master-Readback bestätigt weiterhin 0.6% Gesamtcoverage; der PR behebt sie nicht.

Alle drei Scans erhalten 1,350 Sources, 243 Tests, 136 native Translation Units und vier Go-Module; je Projekt wurden Python-XML einmal, vier Go-Reports und 71 gcov-Reports importiert. Native Qualität bleibt 100/100: Parsingfehler in 0/2,263 Funktionen, 0/6 Klassen, 0/33,778 Statements; 0/1,132 unaufgelöste Projekt-Includes und null externe Includereste. Das belegt den gemessenen Parsing-/Include-Abschluss, nicht C/C++-Taint.

Verbleibende Scannerwarnungen sind getrennt von den 203 IDs: Hauptprojekt 46 WARNs (44 Architekturlabels, FIFO-Parser, TLS-Datei ohne geänderte Zeilen), jedes Advisory vier WARNs (FIFO-Parser, zwei Predecessor, FIFO-Syntax) plus INFO-Simulationskostenskip bei `ci/lib/runtime_path_utils.py:69`. C/C++-Taint bleibt in AutoConfig ausdrücklich deaktiviert; mehrere Varianten/unabhängige Ziele bleiben gesonderte Grenzen. Fehlender TLS-Blame ist verschwunden, die Änderungszeilenwarnung bleibt. Python-/FIFO-Grenzen haben Basisgegennachweise und werden nicht als PR-Regression behauptet.

Terminaler Runtime-Nachweis gehört getrennt zu Source `900dddb49c43ec4479c4b75a91071cadb97893c4`, Lauf `40267347652`: alle sechs Jobs erfolgreich einschließlich Apache; ausgewählter 403-/CRS-/Audit-/Cleanup-Nachweis, keine vollständige Matrixqualifikation. Details und Artefaktgrenzen stehen im 900-Abschnitt. Der Source-Scan überträgt Runtimebelege nicht auf einen anderen Head.

| Restpunkt | Einordnung nach Sourcebeweis |
| --- | --- |
| 203 Finding-IDs | 179 `behoben und nachgewiesen`, 24 nachgewiesene Fehlalarme |
| Gemessene native Parsing-/Includereste | `behoben und nachgewiesen` |
| C/C++-Taint, Python-Simulationskosten/Predecessor, gültiges FIFO | `begründete Analyzergrenze` |
| Architekturmodell mit 44 Labels, wiederholter HTTP 415 und unverändertes Readback | `extern blockiert` |
| Verbliebene TLS-Änderungszeilenwarnung, abschließende CI/Sonar am Dokumentationshead | `weiterhin offen` |

Source-Findings/Gates sind damit abgeschlossen; externe Architekturanwendung und finale Head-Verifikation verhindern weiterhin eine vollständige technische Abschlussbehauptung. PR #421 bleibt Draft, Gesamtstatus **teilweise abgeschlossen/blockiert**. Kein Merge und keine Änderung an master. Quellen: `d545-evidence-summary.json`, `d545-analysis-bindings.json`, `d545-*-baseline-readback.json`, `d545-*-log-evidence.json` und getrennte Hotspotreadbacks im Run `pr421-all-findings-20261026`.
