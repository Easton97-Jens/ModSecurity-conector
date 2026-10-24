# Change Record: CR-20261009-nginx-ci-terminal-fixture-seams

**Sprache:** [English](CR-20261009-nginx-ci-terminal-fixture-seams.md) | Deutsch

Nur Tests: Abgleich mit den aktuellen Native-Callback- und Cleanup-Schnittstellen.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-ci-terminal-fixture-seams |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `f63996290925f4b0c04d286506171825de9dc2ff` |

## Motivation und Problemstellung

Der gespeicherte CI-Scaffold-Fehler und die neue lokale Reproduktion zeigten fehlende Felder/Kollaboratoren im kompilierten Late-Error-Fixture sowie zwei veraltete Inline-Source-Assertions. Die Produktimplementierung delegiert Cleanup bereits und speichert den Native-Append-Rückgabewert vor dessen Prüfung.

## Akzeptanzkriterien

Beide vollständigen zugewiesenen Testmodule müssen bestehen; Terminal-/No-Forward-, Native-Return-, EOS-, Cleanup- und Fehlerursachenprüfungen bleiben erhalten. Produktquelle, Gate-Parser, Required-Auswahl und Runtime-Autorität bleiben unverändert.

## Implementierungsentscheidung und Begründung

Das begrenzte C-Fixture erhält die tatsächlichen Kontextfelder, den Disabled-Budget-Kollaborator und einen separat gezählten Completion-Observation-Kollaborator. Dessen Fehler wird vor Intervention geprüft. Assertions verfolgen den tatsächlichen delegierten Cleanup und gespeicherten Append-Rückgabewert. In-Memory-Mutationen müssen fehlenden/verspäteten Cleanup, fehlenden Common-Cleanup, ignorierte/überschriebene/fest codierte Native-Rückgabewerte und vorzeitige Append-Zählung ablehnen.

## Geänderte Dateien

Nur `tests/test_nginx_late_error_results.py`, `tests/test_nginx_upstream_security_contract.py` und dieses generierte EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Ausführung über `rtk proxy`, ohne Bytecode, mit externem `TMPDIR`/`RUNNER_TEMP` und explizitem `FRAMEWORK_ROOT`: `python -m unittest -v tests.test_nginx_late_error_results tests.test_nginx_upstream_security_contract`. Vor Änderungen: Exit 1, 18 Tests, zwei Fehler und ein Setup-Fehler (`D-ci-r1-red.log`). Danach: Exit 0, 31 Tests (`D-ci-r2-green.log`). Das Fixture kompiliert mit `-std=c17 -Wall -Wextra -Werror`. Generator `create --name nginx-ci-terminal-fixture-seams --base-revision f63996290925f4b0c04d286506171825de9dc2ff --date 2026-10-09` und `git diff --check` endeten beide mit 0. Vollständige Befehle und nachfolgende Dokumentationsprüfungen stehen im externen Taskbericht.

## Security-Auswirkung

Keine Änderung des produktiven Sicherheitsverhaltens. Negativprüfungen erhalten Fail-Closed-Native-Rückgabewerte, Cleanup-Reihenfolge und terminalen Wiedereintritt. Fehlende Sonar-Zählwerte bleiben FAIL; keine erfundene Null und keine Unterdrückung.

## Runtime-Evidence

Nur kompilierter Kontrollfluss und Source-Contract-Evidence. Kein nativer NGINX-Host, Server, Namespace-Supervisor oder Protected-Gate wurde ausgeführt. Parent-Required-Zahl bleibt 97.

## Bekannte Einschränkungen

Die produktiven Timing- und Completion-Observation-Implementierungen sind kontrollierte Kollaboratoren und hier nicht unabhängig verifiziert. Vollständige CI und tatsächliche Runtime-Prüfung bleiben Aufgabe des Koordinators. Die Change-Record-Strukturprüfung bestand (Exit 0). Gesamte Bilingual- und Link-Prüfung endeten jeweils mit 1: bestehende Links zeigen in das nicht initialisierte Framework-Submodule dieses isolierten Worktrees. Der explizite externe Framework-Override schreibt diese Links nicht um; kein Submodule wurde initialisiert.

## Verbleibende Risiken

Künftige Source-Schnittstellenänderungen können Fixture-Pflege erfordern. Bestehende Remote-Sonar-Findings und Unsicherheit des Decoration-Parsers werden durch diese Tests nicht behoben.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build, echter Native-/Runtime-Lauf, Remote-API-Schreibzugriff, MRTS-Initialisierung, Dependency-Installation, Stage/Commit/Push oder Shared-Source-Änderung: außerhalb dieses engen Testauftrags.

## Finaler Diff- und Review-Status

Begrenzte Änderungen anhand tatsächlicher Source und frischer RED/GREEN-Evidence geprüft. Lieferung als ungestagter Diff im isolierten Worktree zur Prüfung und Integration durch den Koordinator, nicht als Commit oder Runtime-Freigabe.
