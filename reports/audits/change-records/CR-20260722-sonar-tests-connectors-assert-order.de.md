# Change Record: Parent-Tests und Lighttpd-Assert-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260722-sonar-tests-connectors-assert-order.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260722-sonar-tests-connectors-assert-order |
| Datum (UTC) | 2026-07-22 |
| Basis-Revision | 961b4fa37cee257a9d50542b3968005e0e21f556 |
| Tracking | Zwanzig Parent-only python:S3415 Code Smells: elf in tests/test_python_interpreter_contract.py und neun in connectors/lighttpd/tests/test_patched_host_contract.py. |
| Grenze | Parent-Test-Source sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, Production-Connector-Source, Scanner-Konfiguration, Quality Gates, Suppressions und Runtime-Verhalten bleiben unverändert. |

## Motivation und Problemstellung

SonarQube Cloud meldet `unittest.TestCase.assertEqual`-Aufrufe, deren Expected-
und Actual-Operanden vertauscht sind. Die Assertions drücken bereits die
beabsichtigten Testpredikate aus; das ausschließliche Vertauschen ihrer ersten
beiden Operanden richtet die Fehlerdiagnostik an der Projektkonvention aus,
ohne Vergleich oder Pass-/Fail-Ergebnis zu ändern.

Die ausgewählten offenen Key-Gruppen sind `AZ-KYVWifYmbqbBXVNJf` bis
`AZ-KYVWifYmbqbBXVNJp` im Interpreter-Contract und
`AZ-KYU9VfYmbqbBXVNCV` bis `AZ-KYU9VfYmbqbBXVNCd` im Lighttpd-Contract.

## Akzeptanzkriterien

- Exakt die ersten zwei Operanden der 20 ausgewählten `assertEqual`-Aufrufe
  vertauschen.
- Testpredikate, optionale Fehlermeldungen, Testeingaben, Expected-Werte,
  Return-Code-Checks und External-Command-Verhalten bewahren.
- Die zwei betroffenen Testmodule und fokussierte legitime Security-Controls
  bestehen lassen.
- Beide Change-Record-Sprachen und beide Indizes gleichwertig halten.
- Frische SonarQube-Cloud- und Hosted-Check-Evidence für den exakten Draft-
  PR-Head einholen, bevor ein ausgewählter Key als behoben gilt.

## Implementierungsentscheidung und Begründung

Der Interpreter-Contract liefert jetzt jedes Process-Result oder jeden
geparsten Payload-Wert zuerst und den festen Expected-Wert danach. Der
Lighttpd-Contract macht dasselbe für Subprocess-Return-Codes, projizierte
Status-Sets, Evidence-Pfade und Phase-4-Summary-Werte. Optionale Assertion-
Messages behalten ihr ursprüngliches drittes Argument. Kein Prädikat,
Fixture, Process-Invocation, Host-Konfiguration oder Production-Source wurde
verändert.

Dieser Batch bleibt absichtlich auf die geprüften 20 S3415-Keys begrenzt.
Andere Sonar-Befunde, einschließlich verbleibender Test-Smells und
Vulnerability-Type-Observations, bleiben getrennte Arbeit.

## Security-Auswirkung

Die geänderten Tests prüfen Executable-Validation sowie Lighttpd-Host-/
Evidence-Contracts, aber die Änderung betrifft nur die Reihenfolge der
Diagnostik. Trust-Boundary, Untrusted-Input, Subprocess-Argument,
Executable-Choice, Konfiguration, Network-Action, Authorization-Entscheidung,
Evidence-Regel und Security-Control ändern sich nicht. Fokussierte negative
Controls beweisen weiterhin, dass ein fremdes erwartetes Executable nicht
ausgeführt wird, unbewiesenes Content-Encoding abgelehnt wird und nur
begrenzte End-of-Stream-Metadata projiziert wird. Durch diesen reinen
Maintainability-Batch wird kein Security-Finding als behoben beansprucht.

## Geänderte Dateien

- tests/test_python_interpreter_contract.py
- connectors/lighttpd/tests/test_patched_host_contract.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Tests und tatsächliche Ergebnisse

| Befehl oder Check | Ergebnis |
| --- | --- |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m py_compile tests/test_python_interpreter_contract.py connectors/lighttpd/tests/test_patched_host_contract.py | bestanden. |
| rtk proxy -- env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=<task-owned path> <selected-python> -m unittest -v tests.test_python_interpreter_contract connectors.lighttpd.tests.test_patched_host_contract | bestanden: 23 Tests. |
| Fokussierte negative Security-Controls: fremdes erwartetes Executable wird nicht ausgeführt; unbewiesenes Content-Encoding wird abgelehnt; Result-Writer projiziert begrenzte EOS-Metadata | bestanden: 3 Tests. |
| Source-Occurrence-Review | bestanden: exakt die 20 ausgewählten assertEqual-Aufrufe verwenden Actual-first-Reihenfolge und behalten ihre optionalen Message-Argumente. |
| git diff --check | bestanden. |

Der Draft-PR [#89](https://github.com/Easton97-Jens/ModSecurity-conector/pull/89)
existiert jetzt für Branch `agent/sonar-s3415-tests-connectors-assertions-20260722`.
Zum Erstellungszeitpunkt stimmten sein Head, der lokale Commit und der Remote-
Branch auf `2012eb37565729fb7fc8a1f902953149ee9cadbe` überein. Frische
Exact-Head-SonarQube-Cloud- und GitHub-Actions-Ergebnisse stehen noch aus und
werden nicht aus diesem Datensatz abgeleitet.

## Runtime-Evidence

Es änderte sich kein Connector-Runtime-Verhalten und es wird keines
beansprucht. Das betroffene Lighttpd-Contract-Modul führt begrenzte
Test-Fixtures aus; es ist weder ein Production-Host-Runtime-Deployment noch
ein Framework-/MRTS-Lauf.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine vollständige Connector-Build- oder Host-/Runtime-Matrix: Diese
  Änderung vertauscht nur Test-Diagnostik-Argumente und die vollständigen
  betroffenen Testmodule bestanden.
- Kein Framework- oder MRTS-Test und keine -Änderung: Sie sind aus diesem
  Parent-only-Task ausgeschlossen.
- Vollständige Hosted-Checks und SonarQube-Cloud-PR-Analyse stehen für den
  aktuellen exakten Draft-PR-Head noch aus.

## Bekannte Einschränkungen

Dieser Batch behandelt nur 20 ausgewählte python:S3415 Observations. Er
beansprucht weder, den größeren SonarQube-Cloud-Backlog zu leeren, noch nicht
verfügbare Runtime-Umgebungen zu validieren.

## Verbleibende Risiken

Ein versehentlicher Operandentausch außerhalb einer ausgewählten Assertion
könnte Fehlerdiagnostik irreführend machen. Der finale Source-Occurrence-
Review, 23 Tests der betroffenen Module und fokussierte negative Security-
Controls reduzieren dieses Risiko; frische Hosted-Exact-Head-Analyse bleibt
vor verifizierter Delivery erforderlich.

## Finaler Review-Status

Lokale Implementierung und fokussierte Validierung sind auf dem Parent-only-
Task-Branch abgeschlossen. Draft-PR #89 ist offen und als Draft markiert;
sein initialer exakter Head wurde gegen lokale und Remote-Git-Metadaten
verifiziert. Hosted-Checks, Sonar-Analyse und Quality Gate stehen noch aus.
Es werden weder Review-Freigabe noch Merge oder Default-Branch-Änderung
beansprucht oder autorisiert.
