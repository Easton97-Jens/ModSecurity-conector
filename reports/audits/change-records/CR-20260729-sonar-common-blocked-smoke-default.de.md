# Change Record: Parent-Common-Blocked-Runtime-Smoke-Default-Dispatch für SonarQube Cloud S131

**Sprache:** [English](CR-20260729-sonar-common-blocked-smoke-default.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260729-sonar-common-blocked-smoke-default |
| Datum (UTC) | 2026-07-29 |
| Basis-Revision | 9f23ae2c5fe908cef38f203be03f93fda75a8dd7 |
| Synchronisierte Validierungsbasis | fda62539b6f0a710865707e3003b73ed4469f20e |
| Tracking | SonarQube Cloud `shelldre:S131` in `common/scripts/run_blocked_runtime_smoke.sh:119`. Kein gehosteter PR- oder Exact-Head-Status wird behauptet. |
| Grenze | Parent-`common`-Blocked-Runtime-Smoke-Dispatcher, sein fokussierter Dispatch-Regressionstest und gekoppelte Change-Record-/Index-Dokumente. Framework, MRTS, Gitlinks, Workflows, SonarQube-Policy und `master` werden nicht verändert. |

## Motivation und Problemstellung

Der äußere Connector-Dispatch hatte einen leeren Catch-all-Arm. Sein finaler Fallback lag später; das erhielt das Verhalten, machte den Umgang mit nicht unterstützten Connectoren an der `case`-Grenze aber nicht explizit.

## Akzeptanzkriterien

- Jeder Wert des äußeren Connector-`case`, einschließlich unbekannter Werte, erreicht ein kontrolliertes Blocked-Dependency-Ergebnis.
- Der bekannte Envoy-, Traefik- und Lighttpd-Pfad bleibt unverändert.
- Das Skript bleibt POSIX-Shell-syntaktisch gültig und der fokussierte Unknown-Connector-Control bleibt deterministisch.

## Implementierungsentscheidung und Begründung

Der Catch-all-Arm ruft nun denselben `connector_skip_missing_dependency`-Fallback auf, der bereits nach dem Dispatch verwendet wurde. Das macht das Endverhalten explizit, ohne den bekannten Connector-Branch zu verändern oder Runtime-Inputs zu erweitern.

## Security-Auswirkung

Der relevante kontrollierte Input ist der Connector-Name. Die Invariante lautet: Ein nicht unterstützter Wert wählt niemals einen Runtime-Harness, erzeugt Output-Paths oder führt einen unbekannten Befehl aus. Der neue Default-Arm kehrt über den bestehenden Blocked-Dependency-Control zurück, bevor solche Operationen stattfinden. Der fokussierte Test beweist diesen Pfad mit einem Stub-Helper; bekannte Branches bleiben Source-unverändert.

## Geänderte Dateien

- `common/scripts/run_blocked_runtime_smoke.sh`
- `tests/test_run_blocked_runtime_smoke.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- `reports/audits/change-records/CR-20260729-sonar-common-blocked-smoke-default.md`
- `reports/audits/change-records/CR-20260729-sonar-common-blocked-smoke-default.de.md`

## Ausgeführte Befehle

| Befehl oder Control | Tatsächliches Ergebnis |
| --- | --- |
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_run_blocked_runtime_smoke` | bestanden, 1 Test. |
| `dash -n common/scripts/run_blocked_runtime_smoke.sh` | bestanden. |
| `shellcheck --shell=sh --severity=warning --exclude=SC1007 common/scripts/run_blocked_runtime_smoke.sh` | bestanden; SC1007 ist ein unveränderter POSIX-`CDPATH=`-Parsing-Hinweis in den Zeilen 14–17. |
| `git diff --check` | bestanden. |

## Tests und tatsächliche Ergebnisse

| Control | Ergebnis |
| --- | --- |
| Unknown-Connector-Dispatch | bestanden: Der Helper erhielt den konfigurierten Blocked-Reason und die Dependency, und das Skript endete ohne Starten eines Harness erfolgreich. |
| POSIX-Shell-Syntax | bestanden. |

## Runtime-Evidence

Der fokussierte Test führt das echte Skript mit einem temporären minimalen Helper- und Connector-Tree aus. Er erreicht den Unknown-Connector-Default-Arm ohne Framework-/MRTS-Runtime-Dependencies.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Runtime-Matrizen wurden nicht ausgeführt, weil der veränderte Fallback bewusst vor jedem unterstützten Runtime-Pfad blockiert; kein bekannter Connector-Branch wurde verändert.
- Repositoryweite Bilingual- und Dokumentationslink-Prüfungen werden in einem registrierten isolierten Worktree mit dem gepinnten Framework-Checkout ausgewertet; sie autorisieren keine Framework-, MRTS- oder Gitlink-Änderung.
- Exact-Head-Hosted-GitHub-Actions-, SonarQube-Cloud-PR-Analyse-, Review-, Thread- und Ruleset-Evidence bleiben vor einer Master-Integration zwingend.

## Bekannte Einschränkungen

Die vorhandenen `CDPATH=`-Zuweisungen erzeugen ShellCheck-SC1007-Hinweise, obwohl `dash -n` die POSIX-Shell-Syntax akzeptiert. Dieser Batch schreibt diese unabhängigen Zuweisungen nicht um.

## Verbleibende Risiken

Die vollständige Runtime-Matrix bleibt für unterstützte Connector-Routen separat nützlich, ist aber für diesen Fallback kein Beleg, weil der geänderte Pfad vor jedem unterstützten Runtime-Harness blockiert. Exact-Head-Hosted-Analyse und anwendbare Projektprüfungen bleiben zwingend, bevor der Sonar-Befund als behoben gilt. Der Default-Arm erhält die bestehende kontrollierte Skip-Semantik, statt eine nicht unterstützte Connector-Ausführung zu versuchen.

## Finaler Diff- und Review-Status

Der scoped Diff enthält eine Default-Dispatch-Änderung, einen fokussierten Regressionstest und gekoppelte Traceability. Dieser Record behauptet kein Remote-Update oder Master-Merge. Vor jeder Delivery-Aktion sind exakter synchronisierter Kandidat, aktueller PR-Head, Reviews, Threads, Required Checks und SonarQube-Cloud-Ergebnis erneut zu lesen.
