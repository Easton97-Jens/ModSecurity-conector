# Change Record: Advisory-Clang-Analysebaseline

**Sprache:** [English](CR-20260714-clang-analysis-baseline.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Titel | Advisory-Clang-Analysebaseline |
| Change-ID | CR-20260714-clang-analysis-baseline |
| Datum (UTC) | 2026-07-14T08:14:23Z |
| Autor oder ausführender Agent | Codex agent <code>/root</code> |
| Basis-Revision | 0fec00442b0031c206b627a44735f1eb07534d51 |
| Zugehöriges Issue oder Pull Request | None |
| Finale Revision | Not committed |

## Motivation und Problemstellung

Eine opt-in, advisory Clang-Tidy- und Clang-Static-Analyzer-Baseline für die
bereits vorhandene C17/C++17-Compilation-Database bereitstellen. Das Ergebnis
muss lokale Diagnosen sichtbar machen und klassifizieren, ohne Findings in
einen Source-Fix-, CI-Gate-, Runtime-, Production- oder Security-Release-Claim
zu verwandeln.

## Betroffene Komponenten und Sicherheitsgrenzen

Die Änderung betrifft Root-Make-Targets, einen reinen Analyse-Runner,
fokussierte Root-Contract-Tests, Entwicklerdokumentation, Variablenreferenz und
dieses Change-Record-Paar. Rohlogs, SARIF-Dateien, gestagte CDB-Kopien und
normalisiertes JSON verbleiben unter <code>$CODEX_TEMP_ROOT</code> außerhalb des
Checkouts.

Sie ändert weder Connector-Request-Verarbeitung, Product-C/C++-Source,
Framework-Source oder Submodulstatus, Workflows, CI-Policy, Runtime-Verhalten
noch Production-Konfiguration. Bereits vorhandene unabhängige
Arbeitsbaumänderungen wurden gesnapshottet und unverändert gelassen.

## Akzeptanzkriterien

| Kriterium | Status | Evidenz |
| --- | --- | --- |
| Vier opt-in advisory Targets existieren und fehlen aus Lint, Quick-Checks, Runtime-Tests und Workflows | Erfüllt | Makefile-Contract-Test und Target-Review |
| CDB- und Ausgabevalidierung ist absolut, außerhalb des Checkouts, auf markierten Temp-Root beschränkt und read-only | Erfüllt | Fokussierte Contract-Tests und Baseline-Read-only-Summaries |
| Findings lassen eine technisch vollständige Baseline nicht fehlschlagen | Erfüllt | Tidy-, Analyzer- und Combined-Baseline-Exits waren mit Findings <code>0</code> |
| Ungültige/unsichere Eingabe, fehlende Voraussetzungen und technische Tool-Fehler bewahren die dokumentierte Exit-Semantik | Erfüllt | Fokussierte Contract-Tests |
| Normalisiertes JSON enthält nur die erlaubten Klassifikationen und erforderlichen operativen Metadaten | Erfüllt | Fokussierte Contract-Tests und Combined-JSON-Review |
| Englische/deutsche Dokumentation und ein passendes Change-Record-Paar beschreiben dieselbe Grenze | Erfüllt | Bilingual-, Link- und Variablendokumentationschecks bestanden |

## Untersuchte Alternativen

- <code>scan-build</code> verwenden. Verworfen, weil es nicht installiert ist
  und direktes <code>clang --analyze</code> einen kontrollierten eigenen
  SARIF-Pfad bereitstellt.
- <code>.clang-tidy</code>, automatische Fixes, <code>NOLINT</code> oder ein
  CI-Gate hinzufügen. Verworfen, weil dies eine lokale advisory Baseline Source
  verändern oder Policy außerhalb dieser Aufgabe erzwingen würde.
- Alle Tool-Diagnosen als bestätigte Bugs oder Schwachstellen behandeln.
  Verworfen: Tool-Ausgabe ist Triage-Eingabe und Security-Kandidaten benötigen
  separate Codex-Security-Validierung.

## Implementierungsentscheidung und Begründung

<code>clang_analysis_baseline.py</code> mit schmalen Shell-/Make-Einstiegen
hinzufügen. Es validiert die bereitgestellte Compilation-Database vor der
Ausgabeerzeugung, verwendet <code>clang-tidy</code> mit expliziter Inline-
<code>-*,bugprone-*,cert-*</code>-Konfiguration und führt den Static Analyzer
direkt über <code>clang</code>/<code>clang++</code> mit dem Profil
<code>core,unix,security,cplusplus,deadcode</code> aus. Ursprüngliche
CDB-Compiler-Driver und ausgabeschreibende Flags werden nie ausgeführt oder
wiederverwendet.

Der Runner schreibt Rohartefakte nur unterhalb des bereitgestellten
Analyseverzeichnisses, normalisiert/dedupliziert Findings, behält alle sieben
erlaubten Klassifikationszähler und erfasst CDB-/Source-/Arbeitsbaum-Snapshots.
Tool-Nicht-null-Exits sind technische Fehler; Warnings mit erfolgreichem
Toolabschluss sind keine Gates.

## Geänderte Dateien

Versionierte Dateien im Scope sind:

- <code>Makefile</code>
- <code>ci/checks/analysis/check-clang-analysis-tools.sh</code> und
  <code>ci/checks/analysis/clang_analysis_baseline.py</code>
- <code>tests/test_clang_analysis_baseline.py</code>
- Englische/deutsche Paare <code>docs/build/README.md</code>,
  <code>docs/build/README.de.md</code>, <code>docs/reference/variables.md</code>
  und <code>docs/reference/variables.de.md</code>
- dieses englische/deutsche Change-Record-Paar und seine englischen/deutschen
  Indizes

Keine Product- oder Connector-Source, Framework-Datei oder -Pointer,
GitHub-Workflow, CI-Gate, <code>.clang-tidy</code> oder <code>NOLINT</code>-
Eintrag wird geändert.

## Hinzugefügte oder geänderte Tests

<code>tests/test_clang_analysis_baseline.py</code> wurde hinzugefügt. Seine acht
Contract-Tests decken fehlende und ungültige CDBs, relative/Checkout-/Symlink-
ausbrechende Pfade, fehlende Tools, unsichere Compilerargumente,
Read-only-Verhalten, Finding-Erfolgssemantik, technischen Tool-Fehler,
erforderliche normalisierte JSON-Felder, Klassifikationswerte, System- und
Drittanbieterheader, Staging-Cleanup und opt-in Make-Wiring ab.

## Ausgeführte Befehle

| Exakter Befehl | Exit-Code oder Ergebnis | Sanitisierte relevante Zusammenfassung | Kanonischer Evidence-Pfad | Run-ID |
| --- | --- | --- | --- | --- |
| <code>rtk make check-clang-analysis-tools</code> | 0 | LLVM 21.1.8 <code>clang-tidy</code>, <code>clang</code> und <code>clang++</code> waren verfügbar. | None | None |
| <code>rtk make clang-tidy-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 2 | Die anfängliche Make-Argumentschreibweise ließ den führenden <code>-</code>-Selektor als Option parsen; es entstanden keine Baseline-Artefakte oder Source-Änderungen. | None | None |
| <code>rtk make clang-tidy-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | Alle 32 Units endeten; 28 Rohvorkommen wurden zu 23 Findings normalisiert: 22 <code>needs_validation</code>, 1 unbestätigter <code>possible_security_candidate</code>. | <code>$ANALYSIS_OUTPUT/clang-tidy-baseline.json</code> | None |
| <code>rtk make clang-analyzer-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 1 | Die anfängliche C++-SARIF-Invocation zeigte ein fehlendes eigenes Rohausgabeverzeichnis; der Runner wurde korrigiert und keine Source geändert. | <code>$ANALYSIS_OUTPUT/clang-analyzer-baseline.json</code> | None |
| <code>rtk make clang-analyzer-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | Alle 32 Units endeten; 33 normalisierte <code>possible_security_candidate</code>-Findings wurden als unbestätigt gemeldet. | <code>$ANALYSIS_OUTPUT/clang-analyzer-baseline.json</code> | None |
| <code>rtk make clang-analysis-baseline COMPDB_OUTPUT="$COMPDB_OUTPUT" ANALYSIS_OUTPUT="$ANALYSIS_OUTPUT"</code> | 0 | Beide Pfade endeten über je 32 Units; 61 Rohvorkommen wurden zu 56 Findings normalisiert: 22 <code>needs_validation</code> und 34 unbestätigte <code>possible_security_candidate</code>. | <code>$ANALYSIS_OUTPUT/clang-analysis-baseline.json</code> | None |
| <code>rtk .venv/bin/python -m unittest -v tests.test_clang_analysis_baseline</code> | 0 | Acht fokussierte Analysis-Baseline-Contract-Tests bestanden. | None | None |
| <code>rtk .venv/bin/python -m unittest -v tests.test_c_cpp_diagnostics</code> | 0 | Fünf bestehende C/C++-Diagnostik-Contracts bestanden nach der Makefile-Integration. | None | None |
| <code>rtk make check-bilingual-docs</code> | 0 | Zweisprachige Dokumentstruktur und -parität bestanden. | None | None |
| <code>rtk make check-doc-links</code> | 0 | Repository- und Framework-Dokumentlinks bestanden. | None | None |
| <code>rtk make check-variable-documentation</code> | 0 | 85 dokumentierte Variablenreferenzen bestanden. | None | None |
| <code>rtk git diff --check</code> | 0 | Es wurden keine Whitespace-Fehler gemeldet. | None | None |

## Security-Auswirkung

Keine Änderung des Connector-Runtime-Sicherheitsverhaltens. Die Baseline
beschränkt lokale Pfad- und Compilerargumentbehandlung, verhindert automatische
Source-Rewrites und hält Rohartefakte außerhalb des Repositorys. Ihre 34
kombinierten <code>possible_security_candidate</code>-Ergebnisse sind
unbestätigte Tool-Signale, keine bestätigten Schwachstellen; sie benötigen
separate Codex-Security-Validierung vor Remediation- oder Disclosure-Arbeit.

## Dokumentationsänderungen

Der englische/deutsche Leitfaden für lokale Diagnostik und die
Variablenreferenz wurden mit Targets, sicheren Pfadanforderungen,
Check-Profilen, Exit-Codes, JSON-Schema-Grenze, Klassifikationen,
No-Fix-/No-Gate-Policy und advisory Einschränkungen aktualisiert. Dieser
englische/deutsche Change Record und die Begleitindex-Einträge wurden ergänzt.

## Runtime-Evidence

Für diese Änderung wurde keine Runtime-Evidence erhoben oder beansprucht. Die
CDB-getriebene Source-Analyse führt keinen Connector-Traffic aus und begründet
kein Runtime-, Production-, CRS-, Lifecycle- oder Security-Ergebnis.

## Bekannte Einschränkungen

- Die Abdeckung ist auf die bereitgestellte 32-Unit-Datenbank beschränkt: 31
  C17- und eine C++17-Translation-Unit. Apache, HAProxy, Envoy, Traefik und
  lighttpd sind nicht von dieser Datenbank abgedeckt.
- Tidy- und Analyzer-Diagnosen können mit Clang-Version, Target-Headern und
  Compilation-Database-Inhalt variieren.
- Die Baseline klassifiziert nur den Triage-Status; sie löst oder unterdrückt
  kein Finding.

## Verbleibende Risiken

Die 34 kombinierten möglichen Security-Kandidaten und 22
Validierungs-Findings benötigen menschliches Review. Header-Filtering und
Tool-Modellgrenzen können False Positives erzeugen oder Pfade auslassen. Die
Sicherheitskontrollen verhindern Ausgabepfad- und Source-Rewrite-Fehler, aber
sie ersetzen keinen dedizierten Security-Scan oder Runtime-Test.

## Nicht ausgeführte Prüfungen mit Begründung

- <code>make quick-check</code> und <code>make lint</code> werden nicht als
  advisory Baseline-Gate ausgeführt; fokussierte Contracts und erforderliche
  Dokumentationschecks liefern die relevante Source-Level-Verifikation.
- Builds, Konfigurationschecks, Runtime-/Lifecycle-Tests, Production-Deployment
  und Codex-Security-Validierung werden nicht ausgeführt. Sie liegen außerhalb
  dieser advisory Baseline und es wird keine Runtime-/Security-Schlussfolgerung
  beansprucht.

## Finaler Diff- und Review-Status

Die fokussierte Acht-Test-Baseline-Suite, die bestehende Fünf-Test-
Diagnostik-Suite, Dokumentationschecks, Link-Checks, Variablenreferenzcheck und
<code>git diff --check</code> bestanden. Die bereitgestellte CDB behielt
SHA-256 <code>c6f5c89e03811faf8f8a00e38066f9f79a303524ef7d94b5f1330634e70deb75</code>,
und Framework-Arbeitsbaum sowie Submodul-Pointer blieben unverändert. Der
Parent-Arbeitsbaum enthält unabhängige parallele Änderungen außerhalb dieses
Scopes; sie wurden nicht verändert oder zurückgesetzt. Dieser Record stimmt mit
den Advisory-Baseline-Dateien und tatsächlichen Ergebnissen überein. Der
beabsichtigte Commit-Betreff ist
<code>Add advisory Clang analysis baseline</code>.
