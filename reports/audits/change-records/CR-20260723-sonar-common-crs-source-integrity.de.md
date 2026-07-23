# Change Record: Common-CRS-Source- und generierte-Konfigurationsintegrität

**Sprache:** [English](CR-20260723-sonar-common-crs-source-integrity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260723-sonar-common-crs-source-integrity |
| Datum (UTC) | 2026-07-23 |
| Basis-Revision | a308d7b414f0859490fe7253e0683a4bde80b563 |
| Tracking | Parent-only-`python:S5443`-Keys `AZ70UrU3IhrooTjfZnAX`, `AZ70UrU3IhrooTjfZnAY` und `AZ70UrU3IhrooTjfZnAZ`; Draft-PR-#97-Follow-up für `pythonsecurity:S8707`-Key `AZ-PstOVmYfklgBeDadY`, zwei `python:S1192`-Keys und vier `python:S3415`-Keys; Pending-Canonical-Findings `FND-SONAR-0013` und `FND-SONAR-0014`. |
| Grenze | Nur Parent: Common-Python-Runner, Parent-Test, gepaarte Parent-Dokumentation und dieses Change-Record-Paar. Framework, MRTS, Gitlinks, Abhängigkeiten, SonarCloud-Controls, Suppressions, Exclusions, Quality Gates und Host-Protokollverhalten bleiben unverändert. |

## Motivation und Problemstellung

Wenn der CRS-Smoke libmodsecurity verwendet und keine explizite CRS-Quelle
ausgewählt ist, durchsuchte der Runner zuvor `RUNNER_TEMP`, `TMPDIR` und
gemeinsam genutzte temporäre Orte. Ein anderer lokaler Benutzer konnte einen
Baum vorbereiten, der wie eine CRS-Quelle aussieht. Der Runner akzeptierte nur
die oberflächliche Setup-/Rules-Struktur, erzeugte daraus `Include`-Einträge
und übergab die generierte Regeldatei an den lokalen libmodsecurity-Evaluator.
Die generierte Setup-/Rule-Datei und der Audit-Log-Ort werden ebenfalls aus
aufrufergewählten Ausgabepfaden abgeleitet; daher muss ihre Verzeichnis- und
Stale-File-Provenance geschützt sein, bevor die generierte Regeldatei den
Evaluator erreicht.

Dies ist eine lokale Cross-User-Configuration-Integrity-Grenze. Es wird weder
ein Remote-Request-zu-Parser-Pfad noch behauptet, dass beliebige CRS-Direktiven
Code-Ausführung erreichen; die Änderung verhindert, dass ein Smoke-Lauf den
Regelbaum eines anderen Benutzers stillschweigend als Quelle akzeptiert.

Die erste Exact-Draft-PR-#97-SonarCloud-Analyse meldete zusätzlich einen
agentischen Filesystem-Boundary-Kandidaten auf der direkten `--log-dir`-Route
des Runners. Vor dem Follow-up konnte eine direkte Invocation einen Output-Root
außerhalb des verifizierten Invocation-Baums auswählen und Konfigurations-/Log-
Verzeichnisse sowie bei libmodsecurity die Entfernung eines stale Decision-Logs
erreichen. Eine fokussierte Red-Regression bewies, dass ein außerhalb liegendes
`--config-root` erzeugt wurde, bevor der Runner zurückkehrte.

## Akzeptanzkriterien

- Die CRS-Discovery verwendet nur explizites `CRS_SOURCE_DIR` oder aus einer
  expliziten `--runtime-lookup-root` abgeleitete Pfade; kein Shared-Temporary-
  Fallback bleibt erhalten.
- Jede ausgewählte Quelle, Setup-Datei, Rules-Verzeichnis, eingebundene
  Rule-Datei, optionale eingebundene Plugin-Datei, generiertes Runtime-
  Verzeichnis, generierte Setup- und Rule-Datei sowie Audit-Log-Verzeichnis ist
  absolut, jeweils regulär/Verzeichnis, symlinkfrei, dem Runner oder root
  gehörend, nicht gruppen-/weltbeschreibbar und gegen Cross-User-Ancestor-
  Replacement geschützt.
- Ein in eine quotierte ModSecurity-Direktive interpolierter Pfad weist
  Anführungszeichen, Backslashes, Zeilenumbrüche und Glob-Metazeichen zurück; stale generierte
  Ausgabe wird ohne Symlink-Folge geöffnet und vor der Evaluator-Nutzung erneut
  geprüft.
- Gültige explizite Quellen und gültige Runtime-Lookup-Root-Quellen bleiben
  akzeptiert; fehlende oder unsichere Quellen liefern `SmokeBlocked` / Exit 77,
  bevor eine generierte Regeldatei den Evaluator erreicht.
- Jedes direkte Output-Argument (`--evidence-root`, `--results-dir`,
  `--tmp-root`, `--log-root`, `--log-dir` und `--config-root`) ist absolut,
  kanonisiert und unterhalb von `VERIFIED_RUN_ROOT` enthalten, bevor der Runner
  erzeugt, unlinkt, an den Evaluator übergibt oder den Result-Writer aufruft.
  Außerhalb liegende Roots und über Symlink aufgelöste Escapes liefern Exit 77
  ohne einen Runner-Write.
- Die ausgewählten Sonar-Keys werden auf einem frischen Exact-Draft-PR-Head
  ohne Suppression, False-Positive-State, Exclusion, Regel-/Profil- oder
  Quality-Gate-Änderung geprüft.

## Implementierungsentscheidung und Begründung

Die Validierung beginnt in `resolve_crs_source_dir()`, weil dies der schmale
Punkt ist, an dem jede wählbare Quelle zur Quelle der `Include`-Pfade für
`prepare_crs_smoke_config()` wird. Der Runner leitet keine Kandidaten mehr aus
Ambient-Temporary-Directory-Variablen ab. Seine verbleibenden expliziten
Kandidatformen werden per `lstat`, komponentenweiser Symlink-Zurückweisung,
Trusted-Owner-/Mode-Prüfung und Ancestor-Replacement-Prüfung kontrolliert,
bevor Konfiguration erzeugt wird. `prepare_crs_smoke_config()` wendet dieselbe
Grenze auf generierte Runtime- und Audit-Verzeichnisse an, erzeugt jedes
generierte Artefakt mit `O_NOFOLLOW` plus exklusiver Erstellung, weist
Directive-verändernde Pfadzeichen zurück und prüft den Parser-Input unmittelbar
vor der Evaluator-Nutzung erneut. Ein Sticky-Ancestor ist nur sicher, wenn
dieser Ancestor und sein geschütztes Kind dem Runner/root gehören; ein
Angreifer-owned-Sticky-Verzeichnis wird zurückgewiesen. Die Prüfung erlaubt
root-owned read-only Component-Bäume ebenso wie current-user-owned Bäume und
bewahrt damit den Prepared-Component-Lifecycle.

Das Control adressiert absichtlich Cross-User-Replacement. Same-UID-Races
bleiben wie bei den bestehenden Runtime-Path-Controls außerhalb dieses Claims.

Für das Exact-Head-Follow-up verwendet `validate_runtime_output_paths()` die
Parent-Policy `ci/lib/runtime_path_utils.py` für den verifizierten Runtime-
Root. Es löst und enthält alle sechs CLI-abgeleiteten Output-Ziele vor einer
Normalisierung oder Runner-Dateisystemoperation. Der Runner behält die
validierten `Path`-Objekte für seine ersten Konfigurations- und Log-Sinks;
normalisierte Werte werden nur für nachgelagerte Helper zurückgeschrieben. Das
feste CRS-Suffix wird vor dem Erzeugen des Konfigurationsverzeichnisses erneut
validiert, sodass ein bereits vorhandener `crs-smoke`-/`crs-secondary-smoke`-
Symlink die erste Root-Prüfung nicht umgehen kann. Das bewahrt das bestehende
Verified-Invocation-Layout, blockiert Outside-Root- und Symlink-Escapes vor
einem Write und hängt nicht von ununtersuchtem Framework-Verhalten ab. Dasselbe
Follow-up ersetzt die zwei duplizierten Literale und korrigiert die vier auf
dem initialen Exact-PR-Head gemeldeten Python-Assertion-Argumentreihenfolgen.

## Geänderte Dateien

- `common/scripts/run_local_runtime_smoke.py`
- `tests/test_common_runtime_smoke_crs_source_security.py`
- `docs/reference/variables.md` und `docs/reference/variables.de.md`
- dieses englische/deutsche Change-Record-Paar

Die etablierten Change-Record-Indizes werden nicht verändert, weil unabhängige
offene Draft-PRs diese Pfade bereits besitzen.

## Lokale Validierung

- `env PYTHONDONTWRITEBYTECODE=1 python -m unittest -v
  tests.test_common_runtime_smoke_crs_source_security`: alle 26 Fälle
  bestanden, einschließlich der Pre-Fix-Reproduktion eines Outside-Outputs,
  aller sechs direkten Output-Roots und eines relativen Pfads, die vor einem
  Runner-Write zurückgewiesen werden, eines breiten `/tmp`-Verified-Roots,
  eines bestehenden Symlink-Escapes, einer Symlink-Schleife und eines bereits
  vorhandenen CRS-Config-Suffix-Symlinks, die mit Exit 77 zurückgewiesen
  werden, sowie eines gültigen Verified-Root-Kontrollfalls zusätzlich zu den
  CRS-Source- und Generated-Output-Kontrollen.
- `python -m compileall -q common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py`:
  bestanden mit Bytecode außerhalb des Checkouts.
- `git diff --check`: bestanden.

## Ausgeführte Befehle

- `python -m unittest -v tests.test_common_runtime_smoke_crs_source_security`
- `python -m compileall -q common/scripts/run_local_runtime_smoke.py tests/test_common_runtime_smoke_crs_source_security.py`
- `python common/scripts/run_local_runtime_smoke.py --help`
- `git diff --check`

## Runtime-Evidence

Die fokussierte Python-Suite erreicht Production-Resolver, Direct-Runner-
Output- und Generated-Configuration-Grenzen. Sie beweist, dass ein
vorbereiteter Fake-CRS-Baum unter einer Ambient-Temporary-Umgebung nicht
ausgewählt wird; unsichere Source-, Evidence-, Runtime-, Audit-, Setup-Output-
und Rule-Output-Varianten werden zurückgewiesen, bevor ein Parser-Input
zurückkehrt; ein außerhalb liegendes direktes `--config-root` vor der Reparatur
erzeugt wurde, aber nun vor `write_result` oder einem vom Runner erzeugten
Verzeichnis zurückgewiesen wird; und ein Output-Escape über einen bestehenden Symlink,
eine Symlink-Schleife sowie ein bereits vorhandener CRS-Config-Suffix-Symlink
mit Exit 77 zurückgewiesen werden. Die legitimen Kontrollen bewahren ein gültiges
Verified-Root-Layout und eine generierte Konfiguration mit einem erlaubten
`Include`-Pfad unter der ausgewählten vertrauenswürdigen Quelle. Kein
Host-Connector und kein libmodsecurity-Evaluator wird durch diese Fixtures
gestartet.

## Security-Auswirkung und verbleibende Evidence

Der geänderte Pfad ist CRS-Kandidatenauswahl plus generierte Konfigurations-/
Audit-Ausgabe zum libmodsecurity-Rules-Parser sowie die CLI-Output-Grenze des
Direct-Runners. Die Controls weisen preseeded Temp, unsicheren Sticky-Parent,
Symlink, beschreibbaren Inhalt, stale Output, Directive-Injection-/Glob-
Expansion, Outside-Output-Root und Symlink-Output-Escape vor dem betroffenen
Sink zurück und bewahren legitime explizite Inputs und das Verified-Runtime-
Layout durch denselben Resolver/dieselbe Policy.

## Bekannte Einschränkungen

Der lokale kanonische `.codex/findings`-Store ist read-only gemountet. Das
EN/DE/JSON-Finding-Bundle bleibt daher als privates importbereites Artefakt
erhalten. Das Change-Record-Indexpaar wird bewusst nicht geändert, weil
unabhängige offene Draft-PRs diese Pfade besitzen.

## Verbleibende Risiken

Bis dieser Branch integriert ist, kann ungepatchter master weiterhin die alten
Ambient-Temporary-CRS-Kandidaten auswählen und Direct-Runner-CLI-Outputs aus
dem Verified-Runtime-Root herausführen. Same-UID-Races und Filesystem-ACL-
Semantik bleiben außerhalb des POSIX-Owner-/Mode-Cross-User-Integrity-Claims.
Es ist keine Risikoakzeptanz erfasst.

## Nicht ausgeführte Prüfungen mit Begründung

- Ein echter CRS-/libmodsecurity-Smoke läuft nicht, weil die dokumentierten
  lokalen Runtime-Komponenten nicht provisioniert sind.
- Der repository-weite Bilingual-Checker wird vor der Delivery ausgeführt; im
  isolierten Worktree kann er durch fehlende Framework-Submodule-Linkziele
  blockiert bleiben. Es wird keine Framework-Initialisierung oder Mutation
  versucht.
- Hosted Checks und Exact-Head-SonarCloud-Analyse hängen vom aktuellen Head
  ab. Sie werden nach dem Follow-up-Commit/-Push erneut ausgeführt und werden
  von diesem lokalen Pre-Delivery-Record nicht behauptet.

## Finaler Diff- und Review-Status

Das finale lokale Parent-only-Follow-up liegt auf Branch
`codex/sonar-common-crs-source-20260723-master-a308d7b`, basiert auf der
beobachteten master-Revision und aktualisiert den bestehenden Draft PR #97.
Finaler Change-aware-Security-Review, exakter Staged-Diff, Hosted Checks und
SonarCloud-Ergebnis müssen abgeglichen werden, bevor Verifikation behauptet
wird.

## Delivery-Status

Draft PR #97 ist offen und muss Draft und ungemergt bleiben. Dieses Follow-up
wird nur über seinen Task-Branch geliefert; es aktualisiert weder den
Default-Branch noch autorisiert es einen Merge.
