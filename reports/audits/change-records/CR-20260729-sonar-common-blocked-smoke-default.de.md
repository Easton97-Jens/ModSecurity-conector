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

Der `case` der ausgewählten Connector-Konfiguration an der getrackten
Sonar-Stelle hatte keinen `*)`-Arm. Auch der äußere Connector-Dispatch hatte
einen leeren Catch-all-Arm; sein finaler Fallback lag später. Das erhielt das
Verhalten, machte den Umgang mit nicht unterstützten Connectoren an dieser
Grenze aber nicht explizit.

## Akzeptanzkriterien

- Der getrackte `case` der ausgewählten Connector-Konfiguration enthält einen
  fail-closed-`*)`-Arm, der ein kontrolliertes Blocked-Dependency-Ergebnis erreicht.
- Jeder Wert des äußeren Connector-`case`, einschließlich unbekannter Werte, erreicht ein kontrolliertes Blocked-Dependency-Ergebnis.
- Der bekannte Envoy-, Traefik- und Lighttpd-Pfad bleibt unverändert.
- Das Skript bleibt POSIX-Shell-syntaktisch gültig; fokussierte Controls decken
  sowohl den Unknown-Connector-Dispatch als auch die innere `case`-Default-Struktur ab.

## Implementierungsentscheidung und Begründung

Der getrackte innere `case` hat nun einen `*)`-Arm, der den bestehenden
`connector_skip_missing_dependency`-Fallback mit den bereits aufgelösten
Runtime-Metadaten aufruft. Auch der äußere Catch-all ruft diesen Fallback
explizit auf. Beide Pfade sind fail-closed und erhalten den bekannten
Connector-Branch sowie die Runtime-Input-Grenze.

## Security-Auswirkung

Der relevante kontrollierte Input ist der Connector-Name. Die Invariante
lautet: Ein nicht unterstützter oder unvollständig konfigurierter Wert wählt
niemals einen Runtime-Harness, erzeugt Output-Paths oder führt einen
unbekannten Befehl aus. Beide Default-Arme kehren über den bestehenden
Blocked-Dependency-Control zurück, bevor solche Operationen stattfinden. Der
fokussierte Dispatch-Test verwendet einen Stub-Helper nur für Outer-Path-
Argumentrouting; ein separater struktureller fokussierter Control prüft, dass
der tatsächliche innere Konfigurations-`case` den fail-closed-Default hat.
Bekannte Branches bleiben Source-unverändert.

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
| `/root/git/ModSecurity-conector/.venv/bin/python -m unittest tests.test_run_blocked_runtime_smoke` | bestanden, 2 Tests. |
| `dash -n common/scripts/run_blocked_runtime_smoke.sh` | bestanden. |
| `shellcheck --shell=sh --severity=warning --exclude=SC1007 common/scripts/run_blocked_runtime_smoke.sh` | bestanden; SC1007 ist ein unveränderter POSIX-`CDPATH=`-Parsing-Hinweis in den Zeilen 14–17. |
| `git diff --check` | bestanden. |

## Tests und tatsächliche Ergebnisse

| Control | Ergebnis |
| --- | --- |
| Unknown-Connector-Dispatch | bestanden: Der synthetische Helper erhielt den konfigurierten Blocked-Reason und die Dependency; dies ist ein Outer-Path-Argumentrouting-Control. |
| Default der ausgewählten Connector-Konfiguration | bestanden: Ein fokussierter struktureller Control bestätigt, dass der getrackte innere `case` den fail-closed-Helper-Aufruf enthält. |
| POSIX-Shell-Syntax | bestanden. |

## Runtime-Evidence

Der fokussierte Dispatch-Test führt das echte Skript mit einem temporären
minimalen Helper- und Connector-Tree aus. Er erreicht den äußeren
Unknown-Connector-Default-Arm ohne Framework-/MRTS-Runtime-Dependencies. Der
strukturelle Control ist bewusst an den tatsächlichen S131-Konfigurations-
`case` gebunden; er behauptet keine vollständige Runtime-Ausführung dieses
ansonsten vom äußeren Guard geschützten Branches.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Runtime-Matrizen wurden nicht ausgeführt, weil der veränderte Fallback bewusst vor jedem unterstützten Runtime-Pfad blockiert; kein bekannter Connector-Branch wurde verändert.
- Repositoryweite Bilingual- und Dokumentationslink-Prüfungen werden in einem registrierten isolierten Worktree mit dem gepinnten Framework-Checkout ausgewertet; sie autorisieren keine Framework-, MRTS- oder Gitlink-Änderung.
- Exact-Head-Hosted-GitHub-Actions-, SonarQube-Cloud-PR-Analyse-, Review-, Thread- und Ruleset-Evidence bleiben vor einer Master-Integration zwingend.

## Bekannte Einschränkungen

Die vorhandenen `CDPATH=`-Zuweisungen erzeugen ShellCheck-SC1007-Hinweise, obwohl `dash -n` die POSIX-Shell-Syntax akzeptiert. Dieser Batch schreibt diese unabhängigen Zuweisungen nicht um.

## Verbleibende Risiken

Die vollständige Runtime-Matrix bleibt für unterstützte Connector-Routen
separat nützlich, ist aber für diese Fallbacks kein Beleg, weil die geänderten
Pfade vor jedem unterstützten Runtime-Harness blockieren. Exact-Head-Hosted-
Analyse und anwendbare Projektprüfungen bleiben zwingend, bevor der getrackte
S131-Befund als behoben gilt. Die Defaults erhalten die kontrollierte
Skip-Semantik, statt eine nicht unterstützte Connector-Ausführung zu versuchen.

## Finaler Diff- und Review-Status

Der scoped Diff enthält zwei fail-closed Default-Dispatch-Änderungen, zwei
fokussierte Regression-Controls und gekoppelte Traceability. Dieser Record
behauptet kein Remote-Update oder Master-Merge. Vor jeder Delivery-Aktion sind
exakter synchronisierter Kandidat, aktueller PR-Head, Reviews, Threads,
Required Checks und SonarQube-Cloud-Ergebnis erneut zu lesen.
