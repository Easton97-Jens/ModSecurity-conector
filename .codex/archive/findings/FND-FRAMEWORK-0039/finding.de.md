# FND-FRAMEWORK-0039 — Kandidatenausgabe der Python-Wartung akzeptierte einen vom Aufrufer gewählten Dateisystempfad

## Identität

| Feld | Wert |
| --- | --- |
| Kategorie | security_validated |
| Repository / Ownership | framework / framework |
| Priorität / Severity | P1 / high |
| Konfidenz / Status | validated / fixed |
| Release-Blocker | ja |

## Evidenz und Auswirkung

Die Exact-Head-SonarCloud-Analyse des Framework-Draft-PR #39 meldet das offene
Issue `AZ-BJmyc1Sm1F-_jUkdR` (`pythonsecurity:S8707`) bei
`ci/tools/update-python-version.py:390`. Das Quality Gate ist ausschließlich
wegen Security on New Code C fehlgeschlagen. Die bisherige CLI akzeptierte für
`--write-candidate-file` ein Pfadargument und reichte es nach einer
Containment-Prüfung an `os.open` weiter. Damit bleibt an einer Dateisystemsenke
eine vom Aufrufer wählbare Pfadkonstruktion bestehen.

Die erforderliche Invariante ist strenger: Die Kandidatenvalidierung darf nur
das feste direkte Kind `$RUNNER_TEMP/framework-python-3.13-candidate` anlegen.
Es muss vor exklusiver Erzeugung fehlen bzw. darf kein Symlink sein; die
legitime Kandidaten-Setup-Action behält denselben festen Eingabepfad. Als
Nachweis wird kein unsicherer Write ausgeführt; die gehostete statische Analyse
ist der konkrete Auslöser.

## Remediation und Validierung

Die enge Reparatur entfernt die werttragende CLI-Pfadoption, leitet den festen
Kandidatendateinamen aus validiertem `RUNNER_TEMP` ab, behält exklusive
Erzeugung bei und ergänzt eine Regression, die ein zusätzliches Zielargument
zurückweist. Sie muss die vorhandenen Schedule/Manual-Gates, unabhängige
Auflösung, den Versionsvertrag und No-update/No-write erhalten. Fokussierte
Tests, Workflow-Lint, vollständiges Framework-Lint, ein quellenbezogener
Security-Review und der versiegelte 11-Dateien-Follow-up-Security-Diff-Scan
bestehen jetzt. Das Finding ist lokal `fixed`; eine frische
Exact-Current-Head-SonarCloud-Analyse muss das ursprüngliche S8707-Issue noch
schließen und das PR-Quality-Gate bestehen, bevor die Delivery verifiziert
werden kann.

## Historie

- 2026-07-20T20:10:08Z — die gehostete PR-#39-Analyse validierte das
  S8707-Finding; es bleibt ein Release-Blocker bis Remediation und
  Exact-Head-Reanalyse bestanden sind.
- 2026-07-20T21:12:33Z — die CLI wurde zu einem Flag ohne Wert geändert, und
  der Updater leitet ausschließlich `$RUNNER_TEMP/framework-python-3.13-candidate`
  ab. Die Extra-Ziel-Regressionsprüfung, legitime Kandidatenmaterialisierung,
  fokussierte und native Checks sowie der versiegelte Follow-up-Scan bestanden.
  Die gehostete Exact-Head-SonarCloud-Reanalyse steht noch aus; kein Merge,
  Parent-Gitlink-Update oder MRTS-Aktion ist autorisiert.
