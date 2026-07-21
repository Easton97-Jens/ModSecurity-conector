# Change Record: Parent-Readiness-Pfadkonstante für SonarQube Cloud S1192

**Sprache:** [English](CR-20260721-sonar-s1192-readiness-path.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260721-sonar-s1192-readiness-path |
| Datum (UTC) | 2026-07-21 |
| Basis-Revision | 2ade0d40983b7af21a65b8cd2884866b85626393 |
| Tracking | Ein Parent-only-python:S1192-Code-Smell: AZ9cRybOHhV2CayPTPwc. |
| Grenze | Nur der Remaining-Connectors-Claim-Policy-Checker sowie dieses Parent-Traceability-Paar/der Index; Framework, MRTS, Gitlinks, Connector-Runtime, Scanner-Konfiguration und Quality Gates bleiben unverändert. |

## Motivation und Problemstellung

Der relative Pfad zum englischen Readiness-Report kam im Claim-Policy-Checker
dreimal vor: einmal in der Report-Liste und zweimal beim eigenständigen Lesen
des englischen Reports. SonarQube-Cloud-Regel python:S1192 meldet dieses
wiederholte Literal. Der Checker ist ein Repository-Policy-Control; deshalb
müssen ausgewählter Report, Existence-Check, Decoding-Verhalten, Diagnostik,
Regular-Expression-Checks und Connector-Statusauswertung exakt erhalten bleiben.

## Akzeptanzkriterien

- Eine Modulkonstante für reports/current/readiness.md definieren und jede
  zuvor gemeldete Verwendung darüber führen.
- Reihenfolge der englischen/deutschen Report-Liste sowie jede vorhandene
  Policy-Entscheidung und Diagnostik unverändert lassen.
- Vor einer Delivery den nativen Claim-Policy-Target sowie Syntax-/Static- und
  Traceability-Checks ausführen.
- Bevor behauptet wird, dass der Key behoben ist, frische SonarQube-Cloud-
  Evidence für den exakten Draft-PR-Head einholen.

## Implementierungsentscheidung und Begründung

READINESS_REPORT_EN ist ein unveränderliches modulweites relatives Pfad-Literal.
REPORTS verwendet die Konstante für seinen englischen Eintrag; das separate
Lesen des englischen Reports baut einen Path aus derselben Konstante und
verwendet diesen Path für die vorhandene is_file-/read_text-Sequenz wieder.
Der deutsche Report-Eintrag, der Diagnostic-String, alle Regex-Patterns und
der gesamte Control Flow bleiben unverändert.

Dies bleibt absichtlich bei einem Source/Key statt bei einem mechanischen
projektweiten python:S1192-Sweep. Andere doppelte Literale können Commands,
Protokoll-Tokens, Report-Inhalt oder Generator-Semantik kodieren und benötigen
jeweils eine eigene Prüfung.

## Security-Auswirkung

Der betroffene Pfad ist ein hartcodierter repository-relativer Wert, kein Wert
aus einer untrusted Source. Die Extraktion ändert weder File-Access-
Autorisierung noch Normalisierung, Path-Containment, Runtime-Protokollverhalten,
Authentifizierung, Autorisierung, Logging, Scanner-Konfiguration, Quality
Gates, Suppressions, NOSONAR-Marker oder False-Positive-Dispositions. Eine
fokussierte Bewertung ergab keine Änderung einer Security Boundary, die eine
separate Security-Finding-Remediation erfordert.

## Geänderte Dateien

- ci/checks/connectors/all/check-remaining-connectors-claim-policy.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| rtk proxy env TMPDIR=<task-owned path> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 make check-remaining-connectors-claim-policy | bestanden: remaining connectors claim policy: ok. |
| rtk proxy env PYTHONPYCACHEPREFIX=<task-owned path> python3 -m py_compile ci/checks/connectors/all/check-remaining-connectors-claim-policy.py | bestanden. |
| Fokussierte Source-Structure-Assertion | bestanden: Report-Liste und separates Englisch-Lesen gehen von READINESS_REPORT_EN aus; keine direkte ROOT-/reports/current/readiness.md-Konstruktion bleibt. |
| Fokussierter Change-Record-Contract | bestanden: alle erforderlichen englischen/deutschen Abschnitte und übereinstimmenden Identity-Werte sind vorhanden. |
| rtk proxy env TMPDIR=<task-owned path> PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tests.test_bilingual_docs | bestanden: 11 Tests. |
| rtk proxy git diff --check | bestanden. |

Hosted-Exact-Head-Evidence bleibt zukünftige Arbeit; dieser Record behauptet
keine unbeobachteten CI-, SonarQube-Cloud-, Review- oder Delivery-Ergebnisse.

## Runtime-Evidence

Es ändern sich keine Connector-Runtime-Pfade. Der fokussierte native Target
führt den vorhandenen Policy-Checker gegen aktuelle Parent-Report- und
Metadata-Dateien aus.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Connector-Build-/Runtime-Matrix ist für diese
  semantikerhaltende Policy-Checker-Konstantenextraktion nicht anwendbar; es
  änderten sich weder Connector-Source noch Runtime-Harness.
- Der vollständige Repository-Bilingual-Checker dient hier nicht als Evidence,
  da er Framework-verlinktes Material außerhalb dieses Parent-only-Tasks
  einschließt. Stattdessen werden Paar und Index fokussiert validiert.

## Bekannte Einschränkungen

Diese Änderung behandelt nur eine aktuelle Sonar-Beobachtung. Der native Target
beweist aktuelles Policy-Checker-Verhalten, nicht eine vollständige Connector-
Runtime-Matrix.

## Verbleibende Risiken

Der größere Parent-only-SonarQube-Cloud-Backlog bleibt separat getrackt.
Hosted-Exact-Head-SonarQube-Cloud- und GitHub-Actions-Evidence sind für einen
Draft-PR weiterhin erforderlich; er muss ungemergt bleiben.

## Finaler Diff- und Review-Status

Der beabsichtigte Source-Diff ist eine Konstantenextraktion ohne
Policy-Verhaltensänderung, ergänzt durch bilinguale Traceability. Bevor ein
Draft-PR als verifiziert gilt, müssen finaler Diff, exakte lokale/Remote/PR-SHA-
Gleichheit, anwendbare GitHub-Checks, SonarQube-Cloud-Quality-Gate,
Selected-Key-Query und PR-Status für den tatsächlichen Head erneut geprüft
werden.
