# FND-SONAR-0011 — Der exakte Head von Parent-PR #90 hat 23 nicht gate-blockierende Major-SonarQube-Cloud-Test-Code-Smells

## Klassifikation

- **Kategorie:** `sonarqube_finding` (`maintainability_code_smells`)
- **Repository / Ownership:** `parent` / `parent`
- **Priorität / Schwere / Confidence:** `P3` / `major` / `confirmed`
- **Status / Feasibility:** `closed` (archiviert) / `feasible_now`
- **Release-Blocker / sicherheitsrelevant:** nein / nein

## Beobachtung

Am exakten PR-#90-Head `06a4e71408a60e5a72a55065a653b9c4e79a1ecf` liefert
SonarQube Cloud 23 offene Major-`CODE_SMELL`-Issues, alle in Parent-
Testdateien. Zweiundzwanzig sind `python:S3415`-Beobachtungen zur
Assertion-Argument-Reihenfolge und eine ist `python:S5778` für eine
Exception-Assertion mit mehreren potenziell werfenden Aufrufen. Betroffen sind
`tests/test_go_version_contract.py` (10),
`tests/test_prepare_runtime_components.py` (2) und
`tests/test_update_go_version.py` (11).

Dies ist nicht gate-blockierend: Derselbe exakte Head hat Quality Gate `OK`,
New Maintainability `A` und 0,0 % duplizierten neuen Code. Der Befund ist vom
früheren Quality-Gate-Blocker `FND-SONAR-0010` getrennt.

## Evidence und Disposition

Die aufbewahrte Issue-Zusammenfassung ist
sonar-pr90-06a4e71-open-code-smells.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/sonar-pr90-06a4e71-open-code-smells.json`)
(SHA-256 `3dcf58c2a8380955d2db678ddcafd0d2804e57bb87a7145f440fbe064ca17b2d`).
Der passende Hosted-Quality-Gate-Receipt ist
hosted-pr90-06a4e71-validation.json (`/var/tmp/codex/ModSecurity-conector/runs/20260722T183342Z-pr80-go-toolchain-submodule-c30d4a37/evidence/hosted-pr90-06a4e71-validation.json`)
(SHA-256 `db38c89e5c1646e343ec022466d7fec899998dda05558ccf85789196d273ea20`).

Die aktuelle lokale Remediation und ihr vollständiger Security-Diff-Scan sind
in pr90-sonar-remediation-security-diff-scan-receipt.json (`/var/tmp/codex/ModSecurity-conector/runs/20260723T040316Z-pr90-sonar-master-ba49d4a2/evidence/pr90-sonar-remediation-security-diff-scan-receipt.json`)
(SHA-256 `55999ab8235aea150b5c703250d8fe8bae96328f9528e97a14a120ffb229bea0`)
aufbewahrt. Sie deckt den exakten Drei-Dateien-Lokalpatch ab und meldet
vollständige Abdeckung mit null reportable Security Findings.

Der Befund wird erfasst statt still unterdrückt. Der Nutzer hat die
Remediation und die geschützte Parent-Master-Integration ausdrücklich
autorisiert. Der abgeschlossene Patch führte nur die 22 erforderlichen
`assertEqual`-Operand-Reihenfolgenormalisierungen aus und isolierte die
unveränderte Prerelease-Fixture vom erwarteten `MetadataError`-Aufruf. Keine
Sonar-Regel, kein Quality Gate, keine Exclusion, Suppression,
False-Positive-Markierung oder Risikoakzeptanz änderte sich.

Der exakte PR-Head `0a1f6031418917e20e2e87aaf935b84b89ca3af1` hat ein
aktuelles Sonar-Issue-Ergebnis mit null offenen oder bestätigten Leak-Period-
Issues und Quality Gate `OK`; er wurde danach geschützt per Squash als
Parent-Master `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3` gemergt. Der
aufbewahrte kombinierte Receipt ist
pr90-protected-merge-and-master-validation-20260723T045207Z.json (`/var/tmp/codex/ModSecurity-conector/runs/20260723T040316Z-pr90-sonar-master-ba49d4a2/evidence/pr90-protected-merge-and-master-validation-20260723T045207Z.json`)
(SHA-256 `4826baec6075341a6a0c96f36dce51f89bd27381c394bbb63e445938b4da97e4`).
Die GitHub-Actions-Workflows auf resultierendem Master bestanden. Dessen
aktueller Sonar-Master-Quality-Gate-Fehler ist der unabhängige, bereits
bestehende Release-Blocker `FND-SONAR-0001`, keine Regression dieses Befunds.

## Sichere Remediation und Validierung

Die abgeschlossene test-only-Änderung bewahrt jedes Expected-/Actual-Pass/Fail-
Prädikat und alle bestehenden Controls. Die drei betroffenen Module bestanden
24 fokussierte Tests; die fokussierte 100-Test-PR-Suite, Contracts, ausgewählte
Kompilierung, Bilingual-Check und vollständige Security-Diff-Scan bestanden
ebenfalls. Die frische Hosted-Sonar-Issue-/Quality-Gate-Evidence und der
geschützte Merge erfüllen die Akzeptanzkriterien ohne Runtime-Code- oder
SonarQube-Cloud-Control-Änderung.

## Verlauf

- `2026-07-22T23:02:27Z`: als bestätigter nicht blockierender aggregierter
  Befund aus der Exact-Head-Sonar-Issue-Abfrage angelegt; keine Remediation
  oder Suppression angewendet.
- `2026-07-23T04:26:13Z`: nutzerautorisierte semantikerhaltende Remediation
  ist lokal abgeschlossen und Security-Diff-gescannt; Hosted-Exact-Head-
  Verifikation ist weiterhin ausstehend.
- `2026-07-23T04:52:07Z`: Exakter Head `0a1f603` bestand Required Checks und
  SonarQube Cloud mit null offenen/bestätigten Leak-Period-Issues und wurde
  danach geschützt per Squash als Master `ad953cd` gemergt; die anwendbaren
  GitHub Actions auf resultierendem Master bestanden. Der getrennte aktuelle
  Master-Quality-Gate-Fehler wird unter `FND-SONAR-0001` verfolgt.

- `2026-07-26T14:09:02Z`: Der aktuelle Nutzer autorisierte Abschluss und Archivierung, nachdem die betroffenen Current-Master-Regression-Suiten in der 144-Test-Control-Suite bestanden; die geänderten Testpfade sind vom verifizierten Master `ad953cd` bis `6ca7e1536ce7e93da68099db9c586b88852ff13e` unverändert.
