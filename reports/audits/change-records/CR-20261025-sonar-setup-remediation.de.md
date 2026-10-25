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

## Runtime-Evidence

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
| Security Rating E | `weiterhin offen`: Source-Fixes und technische Triage belegen keinen frischen Rating-/Finding-Abschluss. |
| Coverage auf neuem Code 0,6 % | `weiterhin offen`: echte Messung erweitert; kumulierte Hauptbranch-Coverage von 80 % nicht nachgewiesen. |
| Fehlende native Includes / Parsingfehler | `weiterhin offen`: realer Headerkontext verbessert; finale Scanner-Deltas unbestätigt. |
| Vollständige Parent-C/C++-Taintanalyse in AutoConfig | `begründete Analyzergrenze`: nicht unterstützter Modus und unabhängige ausführbare Targets bestehen fort. |
| Ignoriertes Python-Modell | `extern blockiert`: Medientyp-Fähigkeit der autorisierten CLI fehlt; exakter Vorschlag liegt vor. |
| Sechs Shell-Parserwarnungen | `weiterhin offen`: lokal gleichwertige Umschreibungen und Syntaxprüfungen benötigen frische dateibezogene Sonar-Bestätigung. |
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
