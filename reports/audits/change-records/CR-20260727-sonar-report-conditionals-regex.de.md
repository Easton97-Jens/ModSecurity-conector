# Change Record: Parent-Report-Generator-Conditionals und Access-Log-Regex für SonarQube Cloud

**Sprache:** [English](CR-20260727-sonar-report-conditionals-regex.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-report-conditionals-regex |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-`python:S3358`-Code-Smells AZ9cRyi6HhV2CayPTPyU, AZ9cRyi6HhV2CayPTPyV, AZ9cRyiqHhV2CayPTPyD, AZ9cRyiqHhV2CayPTPyE, AZ9cRyiqHhV2CayPTPyF, AZ9cRyiqHhV2CayPTPyG, AZ9cRyiqHhV2CayPTPyH, AZ9cRyiqHhV2CayPTPyI, AZ9cRyiqHhV2CayPTPyJ, AZ9cRyiqHhV2CayPTPyK, AZ9cRyiqHhV2CayPTPyL, AZ9cRyiqHhV2CayPTPyM, AZ9cRyiqHhV2CayPTPyO, AZ7POyVcBW70q7L2nMJZ, AZ7POyVcBW70q7L2nMJb, AZ7POyVcBW70q7L2nMJc, AZ7POyVcBW70q7L2nMJd, AZ7POyVcBW70q7L2nMJe, AZ7POyVcBW70q7L2nMJf, AZ7HxAmX_i61V0DF6_GO, AZ7HxAmX_i61V0DF6_GR, AZ7HxAmF_i61V0DF6_GH, AZ7HxAne_i61V0DF6_Gk, AZ7HxAlw_i61V0DF6_GD, AZ7HxAoH_i61V0DF6_G0 und AZ7HxAoH_i61V0DF6_G2; sowie `python:S8786` AZ8hz86oUa5zTy8Lzy9R. |
| Grenze | Neun Parent-Report-Generator-Module, eine Parent-In-Memory-Regression-Suite, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Erzeugte Reports, Report-Generator-Mains, Workflows, Makefiles, Scanner-Konfiguration, Quality Gates, Suppressions, externer Sonar/GitHub-Status, Framework/MRTS-Inhalt, Gitlinks und Delivery bleiben unverändert. |

## Motivation und Problemstellung

Sechsundzwanzig aktuelle `python:S3358`-Befunde verwenden verschachtelte
Conditional-Expressions in Report-Generation und Rendering-Logik. Ihre
Prioritäten und lazy Fallbacks müssen beim besseren Lesbarmachen exakt bleiben.
Separat verwendete `access_status()` eine backtrackende Regular Expression über
NGINX-Access-Log-Request-Text. Der Receipt `AZ8hz86oUa5zTy8Lzy9R` kennzeichnet
superlineare Worst-Case-Arbeit bei fehlerhaften wiederholten `HTTP/`-Fragmenten.

## Akzeptanzkriterien

- Genau die 26 receipt-gemappten verschachtelten Conditional-Expressions durch
  äquivalente geordnete Branches ersetzen.
- Fallback-Reihenfolge, lazy f-string-Konstruktion, Report-Status-Strings,
  Quoted-Action-Parsing und bestehende Report-/Evidence-Semantik bewahren.
- Nur die `access_status()`-Request-/Status-Regex durch begrenztes lineares
  Parsing ersetzen und dabei gültige Combined-Log-Status-Extraktion sowie die
  Ablehnung fehlerhafter Records beibehalten.
- Fokussierte Regression-Coverage hinzufügen und bestehende Evidence-Integrity-
  und Präsentationsverträge bewahren.
- Dieses englisch/deutsche Change-Record-Paar und Indizes pflegen, ohne
  erzeugte Reports, Workflow-, Framework-, MRTS-, Gitlink- oder Delivery-
  Änderungen hinzuzufügen.

## Implementierungsentscheidung und Begründung

Die `python:S3358`-Ausdrücke verwenden jetzt lokale `if`/`elif`-
Entscheidungsbäume in der ursprünglichen Prioritätsreihenfolge. Der Missing-Job-
Fallback liest den sekundären Record weiterhin nur, wenn der primäre Wert keine
Liste ist, und die Incomplete-Matrix-Nachricht wird weiterhin nur in ihrem
gewählten Branch formatiert. Die Quote-State-Behandlung behält ihre frühere
Close/Open/Retain-Transition.

`access_log_status()` scannt Quote-begrenzte Request-Felder einmal, validiert
dieselbe Request- und dreistellige Statusform und gibt den ersten gültigen
Status jeder Zeile zurück, ohne `re.search()` aufzurufen. `access_status()`
behält Datumsfilter und Last-Status-Auswahl bei. Das separate `re.match()` für
Evidence-Path-Erkennung bleibt unverändert.

## Geänderte Dateien

- `ci/evidence/reports/generate-body-processor-analysis.py`
- `ci/evidence/reports/generate-connector-roadmap.py`
- `ci/evidence/reports/generate-intervention-blocking-analysis.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-nolog-audit-evidence-analysis.py`
- `ci/evidence/reports/generate-response-header-hook-analysis.py`
- `ci/evidence/reports/generate-rule-chain-semantics-analysis.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `tests/test_report_conditional_remediation.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_report_conditional_remediation` bestand: 5 Tests.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_generated_report_evidence_integrity` bestand: 74 Tests, einschließlich `check-generated-report-layout: PASS`.
- `rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 <Parent .venv python> -B -m unittest -v tests.test_report_presentation_literals` bestand: 3 Tests.
- Die drei Suiten bestanden insgesamt 82 Tests. Ein AST-Review fand null verschachtelte `IfExp`-Nodes in jeder der acht S3358-gemappten Source-Dateien.
- Der Source/Test-Kandidat `git diff --check` bestand, bevor dieses Change-Record-Paar angelegt wurde.
- Nach einem ausschließlich lesenden Checkout der im Parent festgeschriebenen
  Framework-Revision `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` bestand
  `rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
  check-doc-links`: `bilingual docs ok`, `repository path references: PASS`
  und `doc links ok`.

## Security-Auswirkung

`AZ8hz86oUa5zTy8Lzy9R` ist ein lokalisierter Verfügbarkeits-/Performance-
Kandidat in einem Parent-Report-Generator: Client-abgeleiteter Request-Text
kann von NGINX geloggt werden, später von `read_lines()` aus Test-Evidence
gelesen und an `access_status()` übergeben werden. Die Korrektur entfernt die
unbegrenzte Backtracking-Suche aus diesem Source-to-Sink-Pfad, ohne Input-Pfade,
Safe-Root-/Output-Controls, Report-Provenance, Status-Semantik, Subprocesses,
Netzwerkzugriff oder Publication zu ändern. Die 26 reinen Lesbarkeits-
Branch-Änderungen lockern keinen Security-Control.

## Runtime-Evidence

Die fehlerhafte Eingabe vor der Änderung benötigte 0.000653 s, 0.002457 s und
0.009628 s für 200, 400 und 800 wiederholte `HTTP/`-Segmente. Der Kandidaten-
Parser lieferte `None` in 0.000003 s, 0.000002 s und 0.000002 s für dieselben
Eingaben. Er stimmte für sieben gezielte Kompatibilitätsfälle und 10.000
deterministisch erzeugte Fälle mit der vorherigen Regex-Ausgabe überein. Die
fokussierte Suite prüft außerdem gültige Combined-Log-Extraktion, die Ablehnung
fehlerhafter Zeilen ohne `re.search()` und Last-Status-Auswahl. Es liefen keine
Connector-, Report-Generator-Main-, Output-Writer-, Framework-, MRTS- oder
Host-Runtime.

## Bekannte Einschränkungen

Der lokale Parent-Interpreter ist Python 3.14.4, während der CI-Version-File-
Vertrag Python 3.14.6 verlangt; dies ist somit same-minor lokale Evidence. Der
aktuelle Worktree ist ein uncommitteter Kandidat auf Basis von
`1b0f8825f3510b99b603bb6cd6f0777e1710358e`; er ändert keinen externen
SonarQube-Cloud-Status.

## Verbleibende Risiken

Der Parser-Ersatz könnte sich bei ungewöhnlichen fehlerhaften Quote-Sequenzen
anders verhalten. Die direkten gültigen/fehlerhaften Controls und 10.007
Vergleichsfälle reduzieren dieses Risiko; eine frische SonarQube-Cloud-Analyse
auf exaktem ausgeliefertem Head bleibt aber erforderlich, bevor die aufgeführten
Receipts extern als behoben gelten können.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Report-Generierung und die Full-Runtime-Matrix wurden absichtlich
  nicht ausgeführt, weil sie Evidence lesen oder schreiben können und Runtime-/
  Framework-Eingaben außerhalb dieses fokussierten Source/Test-Batches
  benötigen.
- Es gab keine GitHub-CI, keine SonarQube-Cloud-PR-Analyse, kein Review,
  keinen Pull Request, keinen Merge und kein Default-Branch-Update.

## Finaler Diff- und Review-Status

Der Kandidat ist lokal, uncommittet und ungepusht. Es gibt keine Staging-,
Commit-, Push-, Pull-Request-, MRTS- oder Gitlink-Action. Das im Parent
festgeschriebene Framework wurde ausschließlich für Dokumentationsprüfungen
lesend initialisiert; sein Source, sein Gitlink und der verschachtelte MRTS-
Status bleiben unverändert. Parent-Delivery und die Hosted-SonarQube-Cloud-
Analyse des exakten Heads bleiben getrennte Schritte.
