# Change Record: Parent-Common-Smoke-Writer-Output-Path-Containment für SonarQube-Cloud-Security-Befunde

**Sprache:** [English](CR-20260729-sonar-common-smoke-writer-path-security.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-smoke-writer-path-security |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | Original change base `9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; synchronized candidate base `154ee724eba4653fa6378fc3c8729ae433e65697` |
| Tracking | SonarQube Cloud `python:S5443` in `common/scripts/write_smoke_result.py:67` und `pythonsecurity:S8707` in den Zeilen 83, 90, 97, 347 und 348. Der getrennte `python:S3776`-Komplexitätsbefund liegt außerhalb dieses reinen Security-Batches. Der vorherige Head von PR #176 meldete keine neuen Security-Befunde oder Duplikate, aber vier test-only `python:S5778`-Code-Smells; der synchronisierte Teststruktur-Follow-up benötigt eine neue Exact-Head-Analyse. |
| Grenze | Parent-`common`-Runtime-Smoke-Evidence-Writer, sein fokussierter Python-Security-Regressionstest und gekoppelte Change-Record-/Index-Dokumente. Framework, MRTS, Gitlinks, Workflows, SonarQube-Policy und `master` werden nicht verändert. |

## Motivation und Problemstellung

Der direkte Writer akzeptierte Output-Roots, die nur absolut sein und außerhalb des Checkouts liegen mussten. Eine Pre-Fix-Direct-Invocation setzte `VERIFIED_RUN_ROOT` auf einen Task-Root und übergab `--evidence-root` unterhalb eines benachbarten Roots; sie erstellte Out-of-Root-`result.json`. Generische Schreibvorgänge folgten außerdem einem vorhandenen Output-Datei-Symlink, und `connector` wurde ohne Component-Check in Ergebnisdateinamen interpoliert.

## Akzeptanzkriterien

- Jeder schreibbare CLI-Root ist vor der Ausgabe ein absoluter, privater, symlinkfreier Nachfahre von `VERIFIED_RUN_ROOT`.
- Out-of-Root-Werte, Output-Directory-Symlinks, Output-Datei-Symlinks und Connector-Path-Traversal werden ohne externes Artefakt abgewiesen.
- Eine legitime private In-Root-Invocation behält JSON-, JSONL- und Status-Log-Artefakte.
- Bestehendes Runtime-Smoke-Path-Policy-Verhalten und Python-Syntax bleiben gültig.

## Implementierungsentscheidung und Begründung

Der Writer verwendet nun `verified_runtime_paths`, `is_safe_runtime_root` und `ensure_safe_runtime_directory`, bevor er einen Output-Dateinamen ableitet. Alle fünf schreibfähigen CLI-Roots werden gegen den verifizierten Runtime-Root geprüft; `connector` ist eine einzelne kleingeschriebene Dateinamen-Component. Output-Dateien nutzen `os.open` mit `O_NOFOLLOW`, werden auf Modus `0600` gesetzt und erst nach Verifikation ihrer Parent-Roots geschrieben. Das schützt direkte Invocation und den bestehenden `run_local_runtime_smoke.py`-Caller, ohne das unterstützte In-Root-Layout zu verändern.

## Security-Auswirkung

Kontrollierte Inputs sind `--evidence-root`, `--results-dir`, `--tmp-root`, `--log-root`, `--log-dir` und `--connector`; geschützte Assets sind Runtime-Evidence und Host-Dateien außerhalb des gewählten Runs; der Sink ist Datei-Erzeugung/-Truncation über JSON-/Text-Writer. Validierung erfolgt vor jedem Sink: Roots liegen unter dem verifizierten Runtime-Root und bestehen private No-Symlink-Checks, Connector kann keine Path-Component einführen, und Deskriptoren verweigern Symlink-Following. Der ursprüngliche Trigger endet nun mit `BLOCKED`; der legitime Control schreibt nur unter dem verifizierten Root. Keine Control wird geschwächt.

## Geänderte Dateien

- `common/scripts/write_smoke_result.py`
- `tests/test_write_smoke_result_security.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-smoke-writer-path-security.md`
- `reports/audits/change-records/CR-20260729-sonar-common-smoke-writer-path-security.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Tatsächliches Ergebnis |
| --- | --- |
| Direkte Pre-Fix-Writer-Invocation mit `evidence_root` außerhalb `VERIFIED_RUN_ROOT` | reproduziert: erstellte Out-of-Root-`result.json`. |
| Identische Post-Fix-Invocation | Closure-Control bestanden: endete mit `BLOCKED` und erzeugte kein neues externes Artefakt. |
| Direkte In-Root-Writer-Invocation | legitimer Control bestanden: erzeugte erwartete `result.json`, `common-results.jsonl` und `status.log` nur unterhalb des verifizierten Roots. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_write_smoke_result_security tests.test_common_runtime_smoke_crs_source_security tests.test_runtime_path_security` | bestanden, 50 Tests. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_bilingual_docs` | bestanden, 21 Tests. |
| `/root/git/ModSecurity-conector/.venv/bin/python -m py_compile common/scripts/write_smoke_result.py tests/test_write_smoke_result_security.py` | bestanden. |
| `git diff --check` | bestanden. |
| Initiale SonarQube-Cloud-PR-#176-Analyse | 0 neue Security-Befunde und 0 New-Code-Duplikatzeilen; 4 `python:S5778`-Test-Smells gefunden und im aktuellen Follow-up behoben. |

## Tests und tatsächliche Ergebnisse

| Control | Ergebnis |
| --- | --- |
| Legitimer Output | bestanden: private Evidence-, Results- und Log-Dateien unter dem verifizierten Root werden geschrieben. |
| Ursprünglicher Path-Escape-Trigger | bestanden: Out-of-Root-Evidence-Path wird vor einem externen Directory abgewiesen. |
| Directory-Symlink-Bypass | bestanden: symlinked Output-Directory wird abgewiesen. |
| Output-Datei-Symlink-Bypass | bestanden: `O_NOFOLLOW` weist `result.json`-Ersetzung ab. |
| Connector-Traversal-Bypass | bestanden: `../outside` wird vor Erzeugung eines Runtime-Roots abgewiesen. |

## Runtime-Evidence

Die direkten Writer-Controls verwenden echte CLI, Parser, Path-Validierung und Datei-Schreibgrenze. Keine Connector-Server-, Framework- oder MRTS-Runtime wurde gestartet.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Runtime-Matrizen wurden nicht ausgeführt, weil der Patch auf den Evidence-Writer begrenzt ist; direkte CLI- und bestehende Runtime-Path-Policy-Tests prüfen die veränderte Grenze.
- Ein vollständiger Repository-Security-Scan wurde nicht ausgeführt; die konkreten Befunde wurden am betroffenen Sink revalidiert, reproduziert und getestet.
- `make check-bilingual-docs` ist `blocked_environment`: Seine einzigen Fehler sind vorbestehende Links in das bewusst nicht initialisierte Framework-Submodul, während die fokussierte bilinguale Suite 21 Tests bestand. Submodul, Gitlink und Framework-Prüfungen bleiben außerhalb des Scopes.
- Eine neue Exact-Head-GitHub-Actions-, SonarQube-Cloud-PR-Analyse- und Review-Runde steht nach dem Teststruktur-Follow-up aus.

## Bekannte Einschränkungen

Der getrennte `python:S3776`-Komplexitätsbefund in `main` wird von diesem reinen Security-Batch nicht refaktoriert. Es gibt noch keine Connector-Host-Integration oder Hosted-Evidence.

## Verbleibende Risiken

Der Writer bleibt bewusst von der verifizierten Runtime-Umgebung des Callers abhängig. Fehlt sie oder ist sie breit oder unsicher, schlägt der Writer nun fail-closed fehl, anstatt einen anderen Root zu wählen. Eine Exact-Head-Hosted-Analyse bleibt nötig, bevor die gelisteten Sonar-Befunde als behoben gelten.

## Finaler Diff- und Review-Status

Der scoped Diff enthält nur Writer-Containment, seinen Security-Regressionstest und bilinguale Traceability. Lokale Security-Closure-, Bypass-, Legitimate-Control-, Syntax-, Runtime-Path-Regression- und Whitespace-Checks bestanden. PR #176 ist offen und kein Draft; kein Merge erfolgte. Eine frische Exact-Head-Hosted-Verifikation steht nach der normalen `master`-Synchronisierung und dem Teststruktur-Follow-up aus.
