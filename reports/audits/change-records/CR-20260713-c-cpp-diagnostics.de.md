# Change Record: Reproduzierbare C- und C++-Diagnostik

**Sprache:** [English](CR-20260713-c-cpp-diagnostics.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Reproduzierbare C- und C++-Diagnostik |
| Change-ID | CR-20260713-c-cpp-diagnostics |
| Datum (UTC) | 2026-07-13T20:53:43Z |
| Autor oder ausführender Agent | Codex-Agent <code>/root</code> |
| Basis-Revision | 66c09cc4787025ac2babd9612d0f0bfdf7958f26 |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | Nicht committed |

## Motivation und Problemstellung

Eine reproduzierbare lokale Diagnostik-Grundlage für die repository-eigenen
NGINX-C17-Quellen und den gezielten C++17-Evaluator bereitstellen. Die frühere
Compilation Database ließ eine in der Connector-Konfiguration aufgeführte
Quelle aus; weder der Evaluator noch ein dokumentierter
<code>clangd</code>-Validierungspfad waren abgedeckt. Der Umfang ist nur
Integrationsebene 1: lokale Quellcode-Diagnostik, kein Runtime- oder
Produktionsqualitäts-Claim.

## Betroffene Komponenten und Sicherheitsgrenzen

Die Änderung betrifft lokale Make-Ziele, Repository-Checks, die Erzeugung der
Compilation Database, Entwicklerdokumentation und fokussierte Contract-Tests.
Sie verändert weder Connector-Request-Verarbeitung, ModSecurity-Policy,
extern bereitgestellte Header oder Bibliotheken, Framework-Quellen, den
Framework-Submodule-Pointer, CI-Workflows noch CI-Gating.

Die Compilation Database und der <code>clangd</code>-Cache sind absichtlich
lokal und unversioniert. Sie müssen an einen expliziten externen absoluten Pfad
geschrieben werden; <code>compile_commands.json</code> im Root und
<code>.cache/clangd/</code> sind ignoriert. Build-Produkte, Caches und
Toolausgaben bleiben außerhalb des Checkouts.
Angeforderte Output-Pfade werden kanonisiert und abgelehnt, bevor ein
Output-Verzeichnis angelegt wird, wenn sie innerhalb des Checkouts aufgelöst
werden.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Jede konfigurierte NGINX/Common-C-Quelle ist durch die C17-Liste repräsentiert | Erfüllt | Source-Parity-Contract-Test und <code>check-nginx-c-standard-wiring</code> bestehen; 31 Units werden erfasst. |
| Eine lokale C++17-Evaluator-Diagnostik und ein kompilierbarer C++-Eintrag der Compilation Database existieren | Erfüllt | Evaluator-Ziel und Validierung der zusammengeführten Datenbank bestehen. |
| Die zusammengeführte Datenbank bewahrt echte Bear-Befehle, filtert auf getrackte Quelldateien und wird extern atomar veröffentlicht | Erfüllt | Fokussierte Datenbank-Contract-Tests und beide Datenbank-Ziele bestehen. |
| <code>clangd</code> diagnostiziert NGINX-Modul, <code>late_intervention.c</code> und Evaluator ohne Fixes oder Tidy | Erfüllt | Fokussiertes <code>clangd</code>-Ziel besteht mit einer Datenbank aus 32 Units. |
| Dokumentation und Records erklären Umfang, Pfade, Tools, Einschränkungen und keinen Runtime-Claim auf Englisch und Deutsch | Erfüllt | <code>check-bilingual-docs</code>, Dokumentlink- und Variablen-Dokumentationschecks bestehen nach Hinzufügen des Change-Record-Paars. |

## Untersuchte Alternativen

- Die alte partielle Compilation Database beibehalten. Verworfen, weil sie
  eine in beiden Connector-Konfigurationszweigen enthaltene C-Quelle
  stillschweigend ausgelassen hat.
- Compiler-Befehle aus einer handgeschriebenen Quellliste synthetisieren.
  Zugunsten von Bear-erfassten Befehlen verworfen, damit die Datenbank echte
  Aufrufe abbildet.
- <code>.clangd</code>, <code>.clang-tidy</code>, statische Analyse,
  Sanitizer, CI-Gates oder einen Workflow hinzufügen. Verworfen, weil das den
  gewünschten lokalen Umfang der Integrationsebene überschreitet.
- NGINX-Header während des C17-Checks automatisch herunterladen oder
  bereitstellen. Verworfen; fehlende lokale Voraussetzungen liefern nun das
  dokumentierte blockierte Ergebnis.

## Implementierungsentscheidung und Begründung

Isolierte lokale Analyseziele ergänzen, die echte Compiler, Bear und
<code>clangd</code> benötigen. NGINX-C17-Befehle mit Bear erfassen, den
gezielten Evaluator unter C++17 mit den geforderten Warnungen kompilieren,
diesen Aufruf erfassen und nur validierte, getrackte Translation Units in eine
atomar ersetzte externe Datenbank zusammenführen. Die C17-Quellliste wird zum
exakten Paritätsvertrag mit beiden Connector-Konfigurationszweigen,
einschließlich <code>common/src/late_intervention.c</code>.

<code>clangd</code> erhält eine explizit bereitgestellte Kopie dieser Datenbank
und läuft mit deaktivierter Konfiguration und Tidy, ohne Tweaks, ohne
Background-Index und ohne Schreib-/Fix-Modus. Externe ModSecurity-Header werden
als System-Header übergeben, damit Warnungen Dritter das Ergebnis für den
repository-eigenen Evaluator nicht verfälschen.

## Geänderte Dateien

Versionierte Dateien im Umfang:

- <code>.gitignore</code> und <code>Makefile</code>
- <code>ci/checks/analysis/check-analysis-tools.sh</code>,
  <code>ci/checks/analysis/compile_database.py</code>,
  <code>ci/checks/analysis/compile-db-nginx-c17.sh</code>,
  <code>ci/checks/analysis/check-targeted-evaluator-cpp17.sh</code>,
  <code>ci/checks/analysis/compile-db-cpp17.sh</code> und
  <code>ci/checks/analysis/check-clangd-c17.sh</code>
- <code>ci/checks/connectors/nginx/check-nginx-c-standards.sh</code> und
  <code>ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py</code>
- <code>tests/test_c_cpp_diagnostics.py</code>
- Englisch-deutsche Paare <code>docs/build/README.md</code>,
  <code>docs/build/README.de.md</code>, <code>docs/reference/variables.md</code>
  und <code>docs/reference/variables.de.md</code>
- dieses englisch-deutsche Change-Record-Paar und seine englisch-deutschen
  Indizes

Keine Framework-Submodule-Dateien oder Pointer, keine Workflow-Dateien und kein
CI-Befehl wurden geändert. Absichtliche lokale, unversionierte Artefakte sind
nur die externe Compilation Database und optionale externe Build-Roots.

## Hinzugefügte oder geänderte Tests

<code>tests/test_c_cpp_diagnostics.py</code> hinzugefügt. Der Test prüft exakte
konfigurierte C-Quellparität, Zielverdrahtung und Umfangsgrenzen, validiertes
Zusammenführen von C17/C++17-Datenbanken, Deduplizierung, Ablehnung von
Root-Output und ungetracktem Input, Ablehnung vor Anlegen eines
Checkout-Verzeichnisses, beide Missing-Coverage-Fälle, den dokumentierten
Exit-77-Tool-Blocking-Pfad sowie die Bewahrung einer vorhandenen Datenbank nach
ungültiger Erfassung.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk sh -n ci/checks/analysis/*.sh ci/checks/connectors/nginx/check-nginx-c-standards.sh</code> | 0 | Shell-Syntax für neue lokale Analyse-Skripte und angepassten C17-Check bestanden. | None | None |
| <code>rtk PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile ci/checks/analysis/compile_database.py ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py tests/test_c_cpp_diagnostics.py</code> | 0 | Python-Syntax-Kompilierung bestanden und kein Bytecode verblieb. | None | None |
| <code>rtk PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics</code> | 0 | Fünf fokussierte Source-Parity-, Output-Pfad-, Tool-Blocking- und Datenbank-Contract-Tests bestanden. | None | None |
| <code>rtk TMPDIR=$CODEX_TEMP_ROOT/tmp-final-check PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_c_cpp_diagnostics</code> | 1 | Ein finaler Agent-Aufruf verwendete ein nicht vorhandenes externes temporäres Verzeichnis und scheiterte vor den Source-Tests; kein Repository-Source-Fehler trat auf. Nach Anlegen dieses kanonischen Task-Verzeichnisses bestanden dieselben fünf Tests. | None | None |
| <code>rtk python3 ci/checks/connectors/nginx/check-nginx-c-standard-wiring.py</code> | 0 | Direkte Wiring-Validierung bestanden. | None | None |
| <code>rtk make check-nginx-c-standard-wiring</code> | 0 | Make-Target-Wiring-Validierung bestanden. | None | None |
| <code>rtk make check-analysis-tools</code> | 0 | Konfigurierte C/C++-Compiler, Bear und <code>clangd</code> wurden gefunden und mit Version ausgegeben. | None | None |
| <code>rtk make check-nginx-c17 BUILD_ROOT=$BUILD_ROOT NGINX_SOURCE_DIR=$NGINX_SOURCE_DIR MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR</code> | 0 | Alle 31 konfigurierten NGINX/Common-C17-Translation-Units mit geforderten Warnungen kompiliert. | <code>$BUILD_ROOT/nginx-c17/</code> | None |
| <code>rtk make compile-db-nginx-c17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json NGINX_SOURCE_DIR=$NGINX_SOURCE_DIR MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR</code> | 0 | Bear-Erfassung validiert und 31 eindeutige C17-Units atomar veröffentlicht. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk python3 -m json.tool $ANALYSIS_ROOT/compile_commands.json</code> | 0 | Die veröffentlichte C17-Compilation-Database war valides JSON. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk make check-targeted-evaluator-cpp17 CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 2 | Initialer Versuch scheiterte, weil externe ModSecurity-Header unter <code>-Werror</code> Warnungen ausgaben. | None | None |
| <code>rtk make check-targeted-evaluator-cpp17 CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 0 | Wiederholung nach Behandlung externer Header als System-Header kompilierte den repository-eigenen Evaluator unter C++17; er wurde nicht ausgeführt. | <code>$BUILD_ROOT/cpp-evaluator/</code> | None |
| <code>rtk make compile-db-cpp17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json CPP_BUILD_ROOT=$BUILD_ROOT MODSECURITY_INCLUDE_DIR=$MODSECURITY_INCLUDE_DIR MODSECURITY_LIB_DIR=$MODSECURITY_LIB_DIR</code> | 0 | Erfasster Evaluator-Eintrag mit C17-Einträgen zusammengeführt; Datenbank enthielt 32 eindeutige Units. | <code>$ANALYSIS_ROOT/compile_commands.json</code> | None |
| <code>rtk make check-clangd-c17 COMPDB_OUTPUT=$ANALYSIS_ROOT/compile_commands.json</code> | 0 | Datenbankvalidierung sowie Diagnostik des NGINX-Moduls, <code>late_intervention.c</code> und Evaluators ohne Fehler abgeschlossen. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Dokumentationspaar-Validierung nach Hinzufügen dieses Change-Record-Paars bestanden. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository-Dokumentlinks nach Hinzufügen dieses Change-Record-Paars bestanden. | None | None |
| <code>rtk make check-variable-documentation</code> | 0 | Dokumentierte-Variablen-Validierung nach Hinzufügen dieses Change-Record-Paars bestanden. | None | None |

## Security-Auswirkung

Keine Änderung des Connector-Runtime-Sicherheitsverhaltens. Die neuen Skripte
validieren lokale Pfade, verlangen externe Output-Orte, filtern
Compilation-Database-Einträge auf getrackte Repository-Quellen und ersetzen
einen validierten Output atomar. Sie laden keine Voraussetzungen herunter,
aktivieren kein Umschreiben von Quellen und verarbeiten keinen Runtime-Traffic.
Diese Checks mindern die versehentliche Nutzung veralteter oder eingeschleuster
lokaler Einträge, ohne einen Security- oder Produktionsqualitäts-Claim zu
machen.

## Dokumentationsänderungen

Englisch-deutsche Anleitung zur lokalen Diagnostik in
<code>docs/build/README.md</code> und <code>docs/build/README.de.md</code>
hinzugefügt. Relevante Variablenbeschreibungen in
<code>docs/reference/variables.md</code> und
<code>docs/reference/variables.de.md</code> ergänzt. Dieses englisch-deutsche
Change-Record-Paar und Indexeinträge hinzugefügt.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht. Das
Evaluator-Binary wurde kompiliert, aber nicht ausgeführt; Diagnostik ist kein
Connector-Runtime- oder Produktionsqualitäts-Claim.

## Bekannte Einschränkungen

- Die Abdeckung beschränkt sich auf repository-eigene NGINX/Common-C17-Quellen
  und den einzelnen gezielten C++17-Evaluator; andere Connectoren und
  C++-Quellen sind nicht abgedeckt.
- Lokale Voraussetzungen und absolute externe Pfade sind nötig. Fehlende Tools
  oder lokale Voraussetzungen liefern Exit-Status 77 statt sie bereitzustellen;
  fehlende oder ungültige erforderliche Parameter liefern Exit-Status 2.
- <code>clangd</code> validiert ausgewählte Dateien aus der zusammengeführten
  Datenbank; es ist kein Static-Analysis-, Sanitizer- oder Runtime-Test.
- <code>-Werror</code> gilt für repository-eigenen Evaluator-Code. Externe
  ModSecurity-Header sind absichtlich System-Header; die Prüfung bewertet
  daher nicht die Warnungsqualität von Headern Dritter.

## Verbleibende Risiken

Compiler-, Bear- und <code>clangd</code>-Versionen können zwischen
Entwicklungsmaschinen abweichen, sodass Diagnostik trotz dokumentierter Flags
variiert. Die Ziele geben die gewählten Toolversionen aus und bewahren reale
erfasste Befehle. Künftige Änderungen an Quelllisten oder
Connector-Konfiguration brauchen weiter den Source-Parity-Contract-Test.

## Nicht ausgeführte Prüfungen mit Begründung

- <code>make quick-check</code> und <code>make lint</code> wurden nicht
  ausgeführt, weil die abgegrenzte lokale Diagnostikänderung fokussierte C17-,
  C++17-, Datenbank-, <code>clangd</code>-, Dokumentations- und
  Contract-Test-Evidenz hat; keines davon ist ein angefordertes CI-Gate.
- Statische Analyzer, Sanitizer, <code>clang-tidy</code>, Runtime-/Lifecycle-
  Tests und Produktions-Deployment-Checks wurden nicht ausgeführt, weil sie
  ausdrücklich außerhalb der Integrationsebene 1 liegen und kein Runtime-Claim
  erhoben wird.
- Der fokussierte Contract-Test übt über <code>check-analysis-tools</code>
  einen fehlenden Compiler aus und verifiziert Exit-Status 77. Eine separate
  manuelle Ausführung mit fehlender Voraussetzung war nicht nötig, weil die
  reale Validierungsumgebung die Voraussetzungen bereitstellte.

## Finaler Diff- und Review-Status

Der finale fokussierte Contract-Test, Dokumentationschecks, Whitespace-Review,
Submodule-Checks und die Statusinspektion bestanden nach dieser
Change-Record-Aktualisierung. Die finale externe Datenbank enthält 32
eindeutige Translation Units; die C17-, C++17- und <code>clangd</code>-Ziele
bestehen. <code>git diff --check</code> meldet keine Whitespace-Diagnostik;
sowohl Framework-Submodule-Diff als auch sein Worktree-Status sind leer. Ein
unabhängiges Read-only-Diff-Review fand und die Änderung korrigierte die
Checkout-Pfad-Ablehnung vor Verzeichnisanlage, Missing-Coverage-Tests, den
Exit-77-Test, den quotierten Toolaufruf und die Einschränkung für externe
Header. Es wurde kein Commit und kein Pull Request erstellt.
