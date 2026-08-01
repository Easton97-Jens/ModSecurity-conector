# Change Record: Finale Parent-Common-SonarQube-Cloud-Remediation

**Sprache:** [English](CR-20260801-sonar-common-final-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-common-final-remediation` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `904a8fca64b35cd287348722b4bdc2260b4f64b3` |
| Tracking | Aktuelle Parent-`common/`-SonarQube-Cloud-Receipts `AZ7z-HdL4L5Jot4fEMXc` (`pythonsecurity:S8705`) und `AZ9MwjLo-bUaKQ_zSGBC` (`c:S3776`). |
| Grenze | Nur Parent `common/`, direkte Parent-Tests und dieses gepaarte Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, `.github/`, Sonar-Policy, Exclusions, Suppressions, Quality Gates, direkte `master`-Writes und Merge sind out of scope. |
| Delivery-Status | Die lokale Validierung ist unten erfasst. Ein task-eigener Draft-PR steht aus; dieser Record beansprucht keinen Commit, Push, Review, Hosted-Ergebnis oder Merge. |

## Motivation und Problemstellung

Das aktuelle Parent-`common/`-Inventar enthält genau zwei offene Zeilen. Der
lokale Smoke-Evaluator akzeptierte CLI-abgeleitete Bibliothekspfade in einem
Linker-RPATH-Argument und linkte über einen breiten Bibliotheksnamen. Der
Runtime-Konfigurationsloader behielt nach der vorigen Runtime-Remediation die
letzte Cognitive-Complexity-Zeile.

## Akzeptanzkriterien

- Beide aktuellen Receipts mit Source-Level-Remediation abdecken, ohne
  Scanner-Regel, Exclusion, Suppression oder `NOSONAR` zu ändern.
- Austauschbare oder Linker-Separator enthaltende Evaluator-Inputs vor einem
  Compiler-Prozess ablehnen und zugleich eine private reguläre lokale Library
  unterstützen.
- Runtime-Konfigurationsparsing, zeilennummerierte Fehler, File-Close-Ownership
  und C17-Kompatibilität erhalten.
- Fokussierte Negativ- und legitime Kontrollabdeckung ergänzen, New-Code-
  Duplikatzeilen auf null halten und frische SHA-gebundene Hosted-Sonar-
  Evidence erhalten, bevor der PR als verifiziert gilt.

## Implementierungsentscheidung und Begründung

`prepare_modsecurity_evaluator_inputs` löst und prüft jetzt jedes gewählte
Header-Verzeichnis, Bibliotheksverzeichnis, jede Bibliotheksdatei und
Regeldatei. Inputs müssen absolute, private/nicht ersetzbare reguläre
Filesystem-Objekte sein; das Linker-Verzeichnis weist Komma- und
Steuerzeichen-Separatoren zurück. Der Compiler bleibt der feste lokale C++-
Compiler und wird mit `shell=False` aufgerufen. Er linkt jetzt direkt die
verifizierte `lib_file`, statt `-lmodsecurity` aus einem breiten Suchverzeichnis
aufzulösen; der einzige RPATH ist das verifizierte Bibliotheksverzeichnis.

`parse_runtime_config_line` verschiebt die bestehenden Parser-Branches pro
Zeile aus `load_runtime_config`. Es bewahrt Whitespace-/Kommentar-Behandlung,
Long-Line-Rejection, Key/Value-Parsing, zeilennummerierte Fehler, Assignment
und das caller-owned `fclose`-Verhalten, ohne die öffentliche Runtime-API zu
ändern.

## Security-Auswirkung

Die kontrollierten Inputs sind die operator-bereitgestellten `MODSECURITY_*`-
Werte, die über den lokalen Smoke-Shell-Wrapper zur Python-CLI gelangen. Der
Sink ist der C++-Compiler-/Linker-Aufruf. Die Security-Invariante lautet, dass
ein Compiler-Prozess nur ein festes Executable sowie validierte reguläre Inputs
erhalten kann und dass ein Input über den RPATH-Wert keine zusätzlichen Linker-
Argumente injizieren kann.

Der fokussierte Negativ-Control übergibt ein Komma enthaltendes Library-
Verzeichnis und beweist, dass `subprocess.run` nicht aufgerufen wird. Der
legitime Control akzeptiert private reguläre Header, Library und Rule-Datei und
zeichnet dann ein direktes verifiziertes Library-File-Argument ohne `-L`- oder
`-lmodsecurity`-Fallback auf. Dies beansprucht keine Publisher-Provenance für
eine lokal developer-ausgewählte Library; normales geprüftes lokales
Provisioning bleibt die Trust-Boundary.

## Geänderte Dateien

- `common/scripts/run_local_runtime_smoke.py`
- `common/runtime/msconnector_runtime.c`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- Dieses englisch/deutsche Change-Record-Paar und beide Change-Record-Indizes.

## Ausgeführte Befehle

| Befehl / Kontrolle | Ergebnis |
| --- | --- |
| `python3 -m py_compile common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py` | bestanden |
| `python3 -m unittest -q tests.test_common_runtime_smoke_crs_source_security tests.test_local_runtime_smoke_request_body` | bestanden: 50 Tests einschließlich positiver Evaluator- und No-Process-Negativ-Controls |
| C17-`cc -std=c17 -Wall -Wextra -Werror -fsyntax-only` für `common/runtime/msconnector_runtime.c` mit den verfügbaren lokalen libmodsecurity-Headers | bestanden |
| `make check-common-sdk-contract`, `make check-common-security-contract`, `make check-common-memory-safety`, `make check-common-flow-integrity` | bestanden |
| C++17-Direct-Library-Evaluator-Link mit `-isystem`-Drittanbieter-Headern und verifiziertem RPATH; `ldd`-Readback | bestanden; der Output linkt gegen die gewählte `libmodsecurity.so.3` |
| `make check-common-helpers-c17` | in einem task-eigenen externen Build-Root bestanden |
| `make check-bilingual-docs`, `make check-doc-links` | ausschließlich durch vorhandene Links in das absichtlich nicht ausgecheckte Framework-Submodul blockiert; keine der Prüfungen meldet dieses Change-Record-Paar oder dessen Indizes |
| `git diff --check` | vor dem Staging bestanden; erneute Ausführung für den gestagten Patch vor dem Commit erforderlich |

## Runtime-Evidence

Es wurde keine Connector-Host-Runtime ausgeführt. Der C++-Output ist nur
Kompilierungs- und Dynamic-Linkage-Evidence; er belegt weder eine
libmodsecurity-Entscheidung noch Selected-Host-Traffic.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Connector-Host-Matrix wurde nicht ausgeführt, weil der
  Task nur Common-Source ändert und keine task-provisionierte Host-Matrix hat.
- Der direkte Runtime-Konfigurationsparser wurde nicht gegen einen vollständigen
  Live-libmodsecurity-Lifecycle ausgeführt; der Refactor hat C17-Syntax- und
  Common-Contract-Evidence, es wird aber kein Host-Runtime-Ergebnis beansprucht.
- Ein lokaler SonarQube-Scanner ist nicht installiert. Das maßgebliche Ergebnis
  mit null New Issues und null New Duplication muss vom exakten veröffentlichten
  PR-Head stammen.

## Bekannte Einschränkungen

Lokale Validierung kann das spätere Hosted Quality Gate nicht beweisen. Jeder
neue Hosted-Befund, jede Duplikation, jede fehlgeschlagene Prüfung oder jeder
actionable Review muss auf dem Task-Branch behoben werden, bevor der PR
verifiziert sein kann.

## Verbleibende Risiken

Der Evaluator kompiliert absichtlich gegen einen ausdrücklich ausgewählten
lokalen libmodsecurity-Build. Die neue Grenze verhindert austauschbare Inputs
und Linker-Argument-Injection, attestiert aber nicht unabhängig Publisher oder
Inhalt der Library.

## Finaler Diff- und Review-Status

Der lokale Source-Diff ist auf Parent `common/`, einen direkten Security-Test
und das bilinguale Traceability-Paar/-Index begrenzt. Der unabhängige
Security-Diff-Review hat vollständige Abdeckung und null reportable Findings
für diesen Working-Tree-Diff.
Die finalen lokalen Dokumentationsprüfungen sind ausdrücklich nur durch das
nicht ausgecheckte Framework-Submodul blockiert. Commit, Push, Draft-PR und
SHA-gebundene Hosted-Verifikation stehen noch aus. Kein direkter `master`-Write
oder Merge ist autorisiert.
