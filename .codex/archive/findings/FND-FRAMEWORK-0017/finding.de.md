# FND-FRAMEWORK-0017 — CI-Security-Evidence-Contract akzeptiert erforderlichen Befehlstext nach Zuweisungs-Pseudoaufruf oder terminalem exec

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0017` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P1` / `medium` |
| Confidence / Status | `validated` / `fixed` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `true` |
| Security-relevant | `true` |

## Zusammenfassung, beobachtetes Verhalten und Auswirkung

Am Framework-PR-#27-Head
`82a091a3b6c3e5005126966bf3c6900208c8632b` bewiesen aufbewahrte in-memory-
Workflow-Mutationen zwei fail-open-Reachability-Regressionen am damaligen
Pre-Fix-Head:

1. `unused_scorecard_scan=disabled`, `unused_scorecard_scan[0]=disabled` und
   `unused_scorecard_scan["mode"]=disabled` werden als Funktionsaufrufe
   geparst, wenn der erforderliche Befehl nur in
   `unused_scorecard_scan() { ... }` steht.
2. `exec /usr/bin/true` beendet direkte Erreichbarkeit nicht, sodass ein
   späterer erforderlicher Scanner-Befehl akzeptiert wird, obwohl Bash ihn
   nicht ausführen kann.

Beide mutierten Scorecard-Workflows lieferten keine Contract-Fehler. Ein Pull
Request könnte damit textuelle Scanner-Evidence behalten, den Scanner
überspringen und das CI-Evidence-Gate irreführen. Der lokale semantische Bypass
ist validiert; externe Review- oder Branch-Protection-Konfiguration liegt nicht
im Checkout vor und ersetzte die notwendige fail-closed Reparatur nicht. Der
aktuelle exakte PR-Head enthält nun die durch Regressionen abgesicherte
Reparatur.

## Erwartetes Verhalten und Security-Grenze

Nur Befehle, die Bash auf einem direkt erreichbaren Pfad ausführen kann, dürfen
`require_commands()` erfüllen. Reine Zuweisungen dürfen keine Helper aufrufen,
und eine `exec`-Form mit echtem Befehl muss spätere Erreichbarkeit beenden.
Skalare und Array-Zuweisungen sind beide nicht aufrufend.
Zuweisungspräfixierte legitime Helper-Aufrufe, bare/redirection-only `exec` und
Befehle vor einem terminalen `exec` behalten ihr unterstütztes Verhalten.

Die betroffenen Framework-eigenen Dateien sind:

- `ci/checks/security/check-ci-security-evidence-contract.py`
- `tests/ci_security/test_ci_security_evidence_contract.py`
- die in-memory `.github/workflows/ci-security-scorecard.yml`-Testeingabe

Die betroffenen Symbole sind `FUNCTION_CALL`, `shell_function_call_name()`,
`direct_context_lines`,
`shell_function_blocks`, `control_flow_line_indexes` und
`reachable_shell_lines`.

## Voraussetzungen und Reproduktion

Der exakte #27-Head enthält den semantischen Checker und ein abgedecktes,
pull-request-gesteuertes Workflow-`run:`-Script enthält den erforderlichen
Scorecard-Befehl. Die aufbewahrte Pre-Fix-Reproduktion ersetzt diesen Befehl in
einem in-memory-Workflow durch jede Bypass-Variante und ruft
`workflow_errors()` auf. Die skalare und die `exec`-Variante lieferten am
exakten Head `[]`; eine Simulation des unmittelbar vorherigen
Leading-Identifier-Matchers lieferte auch für die Indexed-Array-Variante `[]`.

Die Source-unveränderte Evidence ist eine reguläre aufbewahrte Datei:

- Run: `20260719T180448Z-framework-pr27-sonar-remediation-72a73203`
- Pfad:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T180448Z-framework-pr27-sonar-remediation-72a73203/evidence/fnd-framework-0017-pre-fix-reproduction.md`
- SHA-256:
  `b9c910089001ca9b67a45d2d3021f697c237b426ce221036b86fe52b2a334f67`
- Befehl:
  `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<task-run>/tmp/pycache python3 -c <in-memory Scorecard assignment-only and exec reachability mutations>`
- Exit-Code: `0`; beobachtet am `2026-07-19T18:05:00Z`.

Die Host-Python-Reproduktion belegt nur die Checker-Logik. Sie ist kein Ersatz
für die gepinnte CPython-3.12-CI-Umgebung des Frameworks, die lokal fehlt.

Die neu ergänzte fokussierte Regression-Suite endete vor der Reparatur ebenfalls
erwartungsgemäß mit `1`: Zehn bestehende Tests bestanden, und genau die
negativen Controls für Zuweisung-only und terminales `exec` schlugen fehl. Das
aufbewahrte Ergebnis liegt als
`evidence/fnd-framework-0017-pre-fix-regression-suite.md` im selben Run vor,
SHA-256 `8a74a663cad6e1664fb190913c78620cb2c356044e8c661b776235635293951b`.

Der Post-Fix-Lokal-Receipt ist
`evidence/fnd-framework-0017-final-local-validation.md` im selben Run,
SHA-256 `6afd44552895aeb9e2030f1a7d4acf0663e0ade7f111c4c5735c46dcdfb26039`.
Er dokumentiert die Indexed-Array-Simulation des vorherigen Matchers sowie die
bestehende fokussierte 12-Test-Suite, direkten Checker, Ruff-Checks, vollständiges
`make lint` und finales `git diff --check`. Das lokale Make-Target verwendet
CPython 3.14.4; Hosted-CPython-3.12-Exact-Head-Evidence bleibt deshalb nötig.

Diese Exact-Head-Evidence existiert nun für
`c323f9d937b63b97257b1ebc8be75e4fdaa3d697`: Alle aktuellen GitHub-Checks
bestanden, SonarCloud meldet null offene/bestätigte PR-New-Code-Issues und es
gibt keine Review-Threads oder Reviews. Der aufbewahrte Receipt ist
`evidence/fnd-framework-0017-exact-pr-head-validation.md`, SHA-256
`04eaa7e9762dd53c6d9847da98aec7e5c624fdf37e44083598b4c06ede805556`.

Der aktuelle exakte PR-Head ist das test-only Follow-up
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b`; es lässt den reparierten Parser
unverändert. Seine 20 erfolgreichen Checks, drei erwarteten Advisory-Skips,
der leere Review-Status, das SonarCloud-`OK`-Quality-Gate, null
offene/bestätigte Issues und null neue duplizierte Zeilen sind in
`evidence/pr27-6a4e057-exact-head-validation.md`, SHA-256
`cca00d78d239b9f2dc21b2ff4f7bf3ed75a0390eeff726254fa8153633b97f58`,
aufbewahrt.

## Root Cause und vorgeschlagene Remediation

Der Leading-Identifier-Matcher des Reachability-Parsers behandelt skalare und
Array-Zuweisungssyntax als Funktionsaufruf, und sein Terminal-Statement-Modell
erkennt `exit`, aber nicht `exec` mit einem Befehl. Die enge Reparatur parst
gewöhnliche führende Shell-Zuweisungswörter vor der Auflösung eines
Funktionsaufrufs, lehnt einen direkt von `[` gefolgten Identifier als
Nicht-Aufrufsyntax ab, erkennt nur `exec`-Formen mit echtem Befehl als terminal,
erhält bare/redirection-only-`exec`-Semantik und ergänzt negative sowie
gepaarte Legitimate-Control-Regressionen.

## Akzeptanzkriterien und Validierungsplan

- Skalare, Indexed-Array- und Quoted-Key-Array-Zuweisungen können einen nicht
  aufgerufenen Helper nicht erreichbar machen.
- Eine direkte `exec`-Form mit echtem Befehl verhindert, dass spätere
  erforderliche Befehle den Contract erfüllen.
- Ein zuweisungspräfixierter direkter Helper-Aufruf bleibt erreichbar.
- Befehle vor terminalem `exec` bleiben akzeptiert.
- Bestehende Kommentar-, Branch-hidden-command-, nicht aufgerufene Helper- und
  legitime Nested-OSV-Helper-Controls bleiben abgedeckt.
- Fokussierte lokale Checks, Source-Level-Security-Review und der finale
  Exact-PR-Head-CI-/Sonar-Zyklus bestehen ohne Abschwächung eines Workflow-,
  Permission-, Scanner- oder Evidence-Controls.

Die lokale Implementierung ergänzt nun deterministische Scorecard-Mutationen
für jeden Bypass und jede gepaarte legitime Kontrolle; fokussierte semantische
Suite, direkter Checker, relevante Quality-Checks und Final-Diff-Review
bestehen, ebenso Hosted-Exact-Head-CI-/Sonar-Evidence. Resulting-Master-
Verifikation bleibt getrennt durch die explizite GitHub-Code-Scanning-
Default-Setup-Entscheidung gegated.

## Abhängigkeiten, verwandte Findings, Restrisiko und Historie

Verwandte Records sind `FND-FRAMEWORK-0012` und `FND-FRAMEWORK-0015`. Die
verbleibende Arbeit hängt von der getrennten Default-Setup-Entscheidung vor
Resulting-Master-Verifikation ab.

Der exakte PR-Head ist fixed, aber das getrennte Default-Setup-Setting-Gate
blockiert Trusted-Master- und Resulting-Master-Verifikation. Kein Risiko ist
akzeptiert.

- `2026-07-18T15:18:00Z`: Die historische Reparatur für Dead-Branch- und
  Uncalled-Function-Bypässe war lokal fixed.
- `2026-07-19T18:05:00Z`: Dieses Finding wurde von `fixed` auf
  `in_progress` erneut geöffnet, nachdem die Zuweisungs- und `exec`-Varianten
  am exakten #27-Head reproduziert wurden; es blockiert die #27-Integration bis
  zur Reparatur mit Regressionen.
- `2026-07-19T18:48:52Z`: Skalare, Indexed-Array-, Quoted-Key-Array- und
  terminale-`exec`-Reparaturen samt gepaarten legitimen Controls bestanden
  fokussierte und vollständige lokale native Validierung. Das Finding bleibt
  nur bis zu einem normalen Push mit Exact-Final-PR-Head-CI-/Sonar-Evidence
  `in_progress`.
- `2026-07-19T18:58:30Z`: Die zwei Framework-eigenen Dateien wurden als
  `f1ad17230072b460c7c85104efac381c19807bb6` committed und normal auf PR #27
  gepusht; Exact-Head-GitHub- und SonarCloud-Checks laufen.
- `2026-07-19T19:07:56Z`: Follow-up
  `c323f9d937b63b97257b1ebc8be75e4fdaa3d697` bestand alle aktuellen
  Exact-Head-Checks; SonarCloud lieferte null offene/bestätigte PR-New-Code-
  Issues und Review-Thread-/Review-Status sind leer. Das Finding ist `fixed`
  und wartet nur auf die getrennt gegatete Resulting-Master-Verifikation.
- `2026-07-19T19:34:25Z`: Das test-only Follow-up für Duplikation
  `6a4e057b2cef1f911ba25ab9f95e1b01b390691b` bestand seine vollständige
  Exact-Head-GitHub-/Sonar-Validierung. Der Parser bleibt unverändert; das
  Finding bleibt `fixed` bis zur Default-Setup-Entscheidung und der
  Resulting-Master-Verifikation.

## Beobachtung auf dem resultierenden Master — 2026-07-19T20:00:39Z

PR #27 wurde als Squash-Merge `6de40c1714410241e917e9083ee890a82fb2fdbb`
gemergt. Sein Source-Tree entspricht dem exakten PR-Head
`6a4e057b2cef1f911ba25ab9f95e1b01b390691b`, der Framework-Worktree ist sauber,
und es existiert kein `tools/MRTS`-Gitlink-Diff. `scaffold-lint`,
`python-ci-security-quality`, `common-structure`, Workflow-Lint und die
Default-Setup-CodeQL-Analysen bestanden auf diesem exakten Master-SHA.

Der erforderliche vertrauenswürdige Advanced-CodeQL-Uploader schlug dennoch für
alle drei Sprachen nach der Analyse fehl, weil Default Setup aktiviert bleibt.
Dieser unabhängige Konfigurationsfehler ist nun `FND-GITHUB-0006`; er verhindert
den Status `verified` für diesen Record, führt aber den behobenen Parser-Bypass
nicht wieder ein. Der aktuelle Nutzer autorisierte den Merge bei beibehaltenem
Default Setup, keine korrigierende Konfigurationsänderung. Es erfolgte keine
Parent-, MRTS-, direkte Master-, Bypass- oder Bereinigungsaktion.
