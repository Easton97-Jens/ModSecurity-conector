# Change Record: Parent-CI-Runtime-Path-Policy Fixed-Fixture Literal-Ownership für SonarQube Cloud S1192

**Sprache:** [English](CR-20260729-sonar-ci-runtime-path-policy-literals.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-runtime-path-policy-literals` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `5a345e3ff90cf5405caea5ff7ae4536b52f826c9` |
| Grenze | Ausschließlich Parent `ci/checks/security/check-runtime-path-policy.py`, sein direkter Parent-Test `tests/test_runtime_path_policy.py`, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine `scripts/`, keine Framework- oder MRTS-Quelle, kein Gitlink, keine SonarQube-Cloud-Regel, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Aktuelle `python:S1192`-Befunde `AZ9cRyb-HhV2CayPTPwj`, `AZ9cRyb-HhV2CayPTPwh`, `AZ9cRyb-HhV2CayPTPwi` und `AZ9cRyb-HhV2CayPTPwg` für wiederholte feste `/var/lib/foo`-, `/var/log/foo`-, `/etc/foo`- und `/usr/local/foo`-Self-Test-Fixtures. |

## Motivation und Problemstellung

Der Runtime-Path-Policy-Checker prüft feste abgelehnte Pfade bewusst über
seine Python-, Framework-Shell- und HAProxy-Self-Test-Zweige. Vier exakte
Test-Fixture-Strings kamen jeweils dreimal vor; SonarQube Cloud meldet sie als
vier `python:S1192`-Maintainability-Befunde. Diese Fixtures sind
Sicherheitskontrollen und keine austauschbaren kosmetischen Beispiele.

## Implementierungsentscheidung und Begründung

`VAR_LIB_SELFTEST_PATH`, `VAR_LOG_SELFTEST_PATH`,
`ETC_SELFTEST_PATH` und `USR_LOCAL_SELFTEST_PATH` besitzen jetzt die vier
wiederholten festen Strings. `PYTHON_BLOCKED_RUNTIME_PATHS` bewahrt die
bestehende geordnete Python-Denial-Menge mit sieben Pfaden;
`SHELL_SYSTEM_PATH_SELFTEST_PATHS` bewahrt die bestehende Shell-Teilmenge mit
sechs Pfaden; und `HAPROXY_BLOCKED_SOURCE_ROOTS` bewahrt die bestehende
HAProxy-Reihenfolge mit vier Pfaden. Kein Wert wird aus Environment,
Dateisystem, Konfiguration oder Tool-Output abgeleitet.

## Akzeptanzkriterien

- Die exakten sieben abgelehnten Python-Fixtures, sechs abgelehnten
  Shell-Fixtures und vier abgelehnten HAProxy-Source-Roots behalten ihre
  bisherigen Werte und ihre Reihenfolge.
- Die Python- und Shell-Policy-Self-Tests behalten ihr Allow/Deny-,
  Quoting- und Exit-Verhalten.
- Manipulierte Projekt-Roots, breite Runtime-Parents, `/etc`, `/root`,
  Source-Mounts und der legitime verifizierte externe Runtime-Root behalten
  ihre bisherigen Control-Ergebnisse.
- Ein zukünftiger exakter PR-Head muss null neue SonarQube-Cloud-Issues, null
  neue Duplikatzeilen und `0.0%` New-Code-Duplizierung erhalten, ohne Regeln
  oder Kontrollen zu schwächen.

## Geänderte Dateien

- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_runtime_path_policy.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-path-policy-literals.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-runtime-path-policy-literals.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Sechs fokussierte `python -B -m unittest -v`-Kontrollen aus `tests.test_runtime_path_policy` | bestanden. Sie decken Fixed-Fixture-Gruppierung, Python-Self-Test-Verhalten, gemockte Shell-Policy-Aufrufe, Broad-Parent-Denial, Mutable-Project-Root-Denial und Verified-Runtime-Root-Controls ab. |
| Direkte Kontrolle des geänderten Checkers mit der bestehenden read-only Framework-`common.sh`-Abhängigkeit | bestanden. Sie meldet die erwartete `/root`-Ablehnung und alle vier HAProxy-Blocked-Source-Root-Controls, danach `check-runtime-path-policy: PASS`. |
| Default-Policy-Subprocess-Test im unveränderten Main-Checkout | bestanden. Er bestätigt, dass ein vom Aufrufer vorgegebener Cache-Override den Default-Probe des Checkers nicht vergiften kann; er wird getrennt festgehalten, weil dem isolierten Task-Worktree die Framework-Abhängigkeit fehlt. |
| Python `-m py_compile` für den geänderten Checker und das direkte Testmodul mit externem Bytecode-Cache-Root | bestanden. |
| Direkte Change-Record-Paarvalidierung und `tests.test_bilingual_docs` | bestanden. Das Paar besitzt passende erforderliche Überschriften und Identitätswerte; das fokussierte Bilingual-Documentation-Testmodul führte 21 Tests erfolgreich aus. |
| Finales `git diff --check` | für den vollständigen Task-Diff mit sechs Dateien bestanden. |
| Fokussierte Sicherheitsvorprüfung | bestanden mit Disposition `already_safe`: Die Zentralisierung source-authored unveränderlicher Self-Test-Daten führt keinen neuen Input-, Dateisystem-, Subprocess-, Netzwerk-, Credential- oder Privilege-Pfad ein. |
| Finaler fokussierter Security-Diff-Review | bestanden ohne plausiblen diff-induzierten Security-Finding. Er bestätigte unabhängig, dass Werte, Gruppierung, Shell-Quoting, Subprocess-Konstruktion und Fail-Closed-Verhalten unverändert bleiben. |
| Initiale Exact-Head-SonarQube-Cloud-PR-Abfrage für #195 | erfüllte das Task-Kriterium nicht: ein neues `python:S3415` an der ergänzten Testassertion, während die Duplizierung `0.0%` blieb. Das Issue erkannte korrekt vertauschte `assertEqual`-Ist-/Soll-Argumente; der Test übergibt jetzt das source-authored Ist-Tupel zuerst und die lokalen Controls wurden erneut ausgeführt. |

## Security-Auswirkung

Der Checker ist sicherheitsrelevant, weil er prüft, dass Environment-Werte
keine breiten oder systembeschreibbaren Runtime-Pfade autorisieren können.
Seine Invariante lautet, dass nur der enge verifizierte externe Run-Root
beschreibbar ist; Source-Mounts bleiben read-only Inputs und
System-/privilegierte Pfade bleiben abgelehnt. Die Extraktion ändert weder
`policy_environment()`, `is_system_write_path()`,
`is_allowed_runtime_path()`, `verified_runtime_paths()`, Shell-Quoting,
Subprocess-Konstruktion, Fehlerbehandlung noch Exit-Verhalten.

Dieses Record beansprucht keine Security-Finding, Suppression oder Behebung.

## Runtime-Evidence

Es werden keine Connector-Runtime, keine Package-Installation, kein Download,
keine provisionierte Komponente, kein Netzwerkdienst und keine Host-Matrix
beansprucht. Die direkte Checker-Kontrolle ruft nur ihren etablierten
Policy-Self-Test-Pfad auf und prüft Denial-Verhalten; sie ist kein Nachweis
einer vollständigen HAProxy-Runtime.

## Nicht ausgeführte Prüfungen mit Begründung

- Das vollständige Modul `tests.test_runtime_path_policy` konnte im isolierten
  Task-Worktree seinen subprocess-basierten Default-Policy-Test nicht
  abschließen, weil dieser Worktree absichtlich keine materialisierte
  Framework-`ci/lib/common.sh` enthält. Derselbe Test besteht im unveränderten
  Main-Checkout, und der geänderte Checker bestand über die bestehende
  read-only Framework-Abhängigkeit in der fokussierten direkten Kontrolle.
  Es wurde keine Framework-Quelle als Workaround geändert oder initialisiert.
- `make check-runtime-path-policy` wurde im Task-Worktree aus derselben
  fehlenden Framework-Worktree-Abhängigkeit nicht ausgeführt. Dies wird nicht
  durch die Behauptung ersetzt, dass das Make-Target bestanden habe.
- Der vollständige Scan `check-bilingual-docs.py` wurde im isolierten
  Task-Worktree ausgeführt und meldet ausschließlich bereits bestehende Links
  in den fehlenden Framework-Checkout. Das Change-Record-Paar bestand seine
  direkte Strukturvalidierung und die fokussierten Bilingual-Documentation-
  Tests; es wurde keine Framework-Quelle materialisiert oder geändert, um den
  breiteren Scan passieren zu lassen.
- Kein breites Lint, keine Connector-Runtime, keine Provisionierung, kein
  Download, keine Package-Installation, keine Framework-/MRTS-Aktion, keine
  Gitlink-Änderung, keine `.github/`-Aktion und keine unverbundene Parent-
  Prüfung wurden ausgeführt, weil diese Aufgabe nur feste Parent-CI-
  Self-Test-Daten ändert.
- Gehostete GitHub-Actions-, SonarQube-Cloud-PR-Analyse-, Review- und
  Merge-Evidence existieren noch nicht und werden nicht lokal hergeleitet.

## Bekannte Einschränkungen

Die vier ausgewählten Befunde sind nur ein kleiner Teil des aktuellen
Parent-CI-SonarQube-Cloud-Backlogs. Der nicht belegte Clang-SARIF-Parser-
Komplexitätsbefund bleibt für einen späteren fokussierten PR getrennt.

## Verbleibende Risiken

Das Restrisiko beschränkt sich auf versehentliches Auslassen, Umordnen oder
falsches Gruppieren einer festen Fixture; der neue direkte Gruppierungstest
sowie die bestehenden Python- und Shell-Policy-Controls decken dieses Risiko
ab. Der exakte gehostete PR-Head muss noch belegen, dass die vier
`S1192`-Befunde fehlen und zugleich keine neue Issue oder Duplizierung
hinzukam.

## Finaler Diff- und Review-Status

Der task-owned Branch wurde gepusht und [Draft PR #195](https://github.com/Easton97-Jens/ModSecurity-conector/pull/195)
gegen `master` existiert. Als `master` fortschritt, bewahrte ein normaler Merge
des aktuellen `master` in den Task-Branch die veröffentlichte PR-Historie; nur
die zwei Change-Record-Indizes hatten Konflikte und beide Records wurden
behalten. Das eine neue SonarQube-Cloud-`python:S3415`-Issue am initialen
PR-Head ist lokal korrigiert. Der aktualisierte exakte Head muss noch gepusht
werden; gehostete Analyse, Reviews und Exact-Head-Verifizierung stehen weiter
aus. Es ist kein Merge nach `master` autorisiert oder beansprucht.
