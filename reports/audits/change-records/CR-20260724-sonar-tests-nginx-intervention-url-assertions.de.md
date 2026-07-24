# Change Record: Parent-NGINX-Intervention-URL-Ownership-Assertion-Reihenfolge für SonarQube Cloud S3415

**Sprache:** [English](CR-20260724-sonar-tests-nginx-intervention-url-assertions.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-tests-nginx-intervention-url-assertions |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Parent-SonarQube-Cloud-`python:S3415`-Code-Smells AZ-KYVTafYmbqbBXVNF7 (Zeile 35) und AZ-KYVTafYmbqbBXVNF8 (Zeile 42). |
| Grenze | Parent-Testquellcode sowie dieses englisch/deutsche Traceability-Paar und die Indizes. NGINX-C-Quellcode, Connector-Verhalten, Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions und generierte Artefakte bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten SonarQube-Cloud-Zeilen melden, dass zwei bestehende
`unittest`-Assertions im Parent-NGINX-Intervention-URL-Ownership-Test ihren
erwarteten Wert vor dem beobachteten Cleanup-Count- oder Return-List-Ergebnis
platzieren. Der bestehende Test erzwingt bereits NGINX-Lifetime- und Cleanup-
Invarianten; allein das Umkehren der ersten zwei Operanden verbessert die
Fehlerdiagnostik, ohne Prädikat oder akzeptiertes Verhalten zu ändern.

## Akzeptanzkriterien

- Nur die zwei ausgewählten SonarQube-Cloud-Assertions auf tatsächlichen Wert
  zuerst und erwarteten Wert danach korrigieren.
- Jedes NGINX-C-Source-Literal, jeden Failure-Branch-Control, Cleanup-Count,
  Return-List-Expectation, Fixture und jede Produktionsquelldatei bewahren.
- Das vollständige fokussierte Parent-Unit-Modul, die Selected-File-
  Syntaxprüfung, die Zwei-Aufruf-AST-Inventur und die Diff-Hygiene bestehen.
- Synchronisierte englisch/deutsche Change Records und Indizes pflegen.
- Exact-Head-GitHub- und SonarQube-Cloud-Draft-PR-Evidenz einholen, bevor die
  ausgewählten Keys als verifiziert beschrieben werden.

## Implementierungsentscheidung und Begründung

Jeder ausgewählte `assertEqual`-Aufruf übergibt jetzt seinen bestehenden
beobachteten Ausdruck zuerst und sein unverändertes erwartetes Literal oder
seine unveränderte Liste danach. Es wurden kein Test-Helper, C-Quellcode,
erwarteter Wert, Assertion-Nachricht, NGINX-Lifecycle-/Cleanup-Bedingung oder
Runtime-Verhalten geändert. Dies ist die kleinste repository-native Korrektur
für `python:S3415` und bewahrt die `unittest`-Prädikatsemantik.

## Security-Auswirkung

Die fokussierte Sicherheitsbewertung lautet `not_applicable`: Dies ist allein
diagnostische Argument-Reihenfolge in Parent-Testcode. Der Test liest einen
sicherheitsrelevanten NGINX-Intervention-Ownership-/Cleanup-Quellpfad, aber
dieser C-Quellcode und jede behauptete Lifetime-Invariante bleiben unverändert.
Das direkte Modul importiert nur Parent-/Python-Standardbibliothek und ruft
weder Framework, MRTS, eine Connector-Runtime, einen Netzwerk-Client noch einen
Subprozess auf. Es wird kein Sicherheitsbefund als behoben behauptet.

## Geänderte Dateien

- tests/test_nginx_intervention_url_ownership.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Fokussierte Kommandos nutzen Parent-.venv-Python,
`PYTHONDONTWRITEBYTECODE=1`, `PYTHONNOUSERSITE=1`, task-owned externes
`TMPDIR` und externes `PYTHONPYCACHEPREFIX`:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_nginx_intervention_url_ownership
- rtk proxy -- env ... <Parent .venv python> -m py_compile tests/test_nginx_intervention_url_ownership.py
- rtk proxy -- env ... <Parent .venv python> -c <AST-Inventur der zwei ausgewählten Assertions>
- rtk proxy -- git diff --check

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes NGINX-Intervention-URL-Ownership-Modul vor und nach der Änderung | bestanden: tests.test_nginx_intervention_url_ownership, jeweils 3 Tests. |
| Selected-File-Python-Syntax | bestanden: tests/test_nginx_intervention_url_ownership.py wurde mit Pycache außerhalb des Checkouts kompiliert. |
| AST-Inventur der ausgewählten Assertions | bestanden: Genau die zwei ausgewählten Anker (35 und 42) haben jetzt Actual-First-Operanden und unveränderte Expected-Werte. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| Bytecode-Scan des aktuellen Batch-Worktrees | bestanden: keine `*.pyc`-Datei. |
| tests.test_bilingual_docs und direkter Change-Record-/Index-Paritätscheck | bestanden: 11 Tests; beide Change Records haben 13 Level-two-Abschnitte sowie passende ID-, Basis-Revision-, Key- und Affected-Path-Literale. |
| make check-bilingual-docs | blocked_environment: Genau 20 vorhandene fehlende Framework-Gitlink-Linkziele; kein neuer Change-Record-Fehler. |
| make check-doc-links | blocked_environment: Genau 16 vorhandene fehlende Framework-Gitlink-Linkziele; es wurde kein Framework-Quellcode, Gitlink oder generiertes Artefakt geändert. |
| Hosted-Delivery-Checks | nicht ausgeführt nach Initial-Commit `bfb73bb`; sie sind auf dem finalen Draft-PR-Head erforderlich und werden nicht vorab behauptet. |

## Runtime-Evidence

Es wurde kein NGINX-Runtime-Verhalten geändert oder behauptet. Der fokussierte
Unit-Test liest bestehenden C-Quellcode und prüft Source-Level-Cleanup-/
Lifetime-Contract-Literale; er ist weder Host-Traffic- noch Produktions-
Runtime-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

- Connector-Builds, Konfigurationsprüfungen, Host-Runtime-Smoke-Tests,
  Protokollmatrizen, Framework-Checks und MRTS-Checks sind nicht anwendbar,
  weil keine Connector-/Runtime-Implementierung geändert wurde und
  Framework/MRTS ausgeschlossen sind.
- Ruff und Pyright sind nicht anwendbar: Es gibt keine Parent-Konfiguration
  und keines der beiden Executables existiert in der ausgewählten Parent
  `.venv`; für diese Diagnostik-Reihenfolgenkorrektur werden weder Tool
  installiert noch Konfiguration geändert.
- Draft-PR-Checks, SonarQube-Cloud-Quality-Gate, PR-Issue-Abfrage und
  Review-Status stehen nach dem Initial-Commit weiterhin aus und sind vor
  `verified_pr` erforderlich.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur zwei ausgewählte Parent-SonarQube-Cloud-Befunde.
Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog mit 1.474 Befunden
zu beheben.

## Verbleibende Risiken

Eine unbeabsichtigte Änderung eines Assertion-Werts könnte den NGINX-
Intervention-Ownership-/Lifetime-Control abschwächen. Der enge Diff, die
exakte Zwei-Aufruf-AST-Inventur, das vollständige fokussierte Modul und die
noch ausstehende Exact-Head-Hosted-Validierung reduzieren dieses Risiko. Aus
dieser Test-Diagnostikänderung wird kein Runtime- oder Security-Verhalten
abgeleitet.

## Finaler Diff- und Review-Status

Die Source-Korrektur und das anfängliche englisch/deutsche Traceability-
Material liegen im atomaren Commit `bfb73bb` auf Task-Branch
`codex/sonar-tests-nginx-intervention-url-assertions-20260724-master-5b8db00`
dessen Parent `5b8db00d44ab24f3a9f4216a00f7edee977b6898` ist. Der Branch ist
bei dieser Dokumentrevision noch nicht gepusht oder einem Pull Request
zugeordnet. Es gab keinen Merge, kein Default-Branch-Update, keine Framework-
Action, keine MRTS-Action, keine Scanner-Control-Änderung und keine
Suppression. Finale Delivery-Fakten werden erst nach ihrer Beobachtung ergänzt.
