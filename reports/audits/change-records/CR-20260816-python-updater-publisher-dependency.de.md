# Änderungsnachweis: Abhängigkeit des Python-Updater-Publishers

**Sprache:** [English](CR-20260816-python-updater-publisher-dependency.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260816-python-updater-publisher-dependency |
| Datum (UTC) | 2026-08-16 |
| Basis-Revision | e1e3bc9bbd2a412721d4e4107e060160b75d01a6 |
| Delivery-Status | Der aktuelle Benutzer autorisierte eine fokussierte Parent-Reparatur, Commit, Push und einen neuen Draft-PR. Die gehostete Pull-Request-Validierung steht aus. Weder Master-Merge noch direkter Master-Write, Force-Aktion, Bypass oder Workflow-Rerun sind autorisiert. |
| Finding | FND-PARENT-0164; Ausgangsfehler: GitHub-Actions-Lauf 31935744923, Job 95137374091 |

## Motivation und Problemstellung

Der privilegierte Publisher-Job des Python-Patch-Updaters importierte Tests, die PyYAML benötigen, installierte jedoch die hash-gesicherten CI-Abhängigkeiten des Repositorys nicht. Seine verpflichtende Revalidierung schlug deshalb fehl, bevor er einen Update-Pull-Request erstellen konnte.

## Akzeptanzkriterien

- Der Publisher installiert die vorhandenen hash-gesicherten CI-Abhängigkeiten vor seinen privilegierten App-Token- und Revalidierungsphasen.
- Die Installation verwendet `--require-hashes` und endet mit `python3 -m pip check`.
- Ein Regressionstest belegt, dass der Abhängigkeitsschritt vor Token-Minting und CI-Sicherheitsrevalidierung bleibt.

## Implementierungsentscheidung und Begründung

Der Publisher verwendet nun denselben gesperrten Abhängigkeitsinstallationsvertrag wie der unprivilegierte Validator-Job. Es wurden weder Paketversionen, GitHub-App-Berechtigungen, Branch-Protection-Regeln noch Quality Gates abgeschwächt oder geändert.

## Security-Auswirkung

Die Fail-Closed-Grenze des Publishers bleibt erhalten: Die CI-Sicherheitsrevalidierung muss erfolgreich sein, bevor der Job sein repository-begrenztes Token minten oder einen Branch und Pull Request erstellen kann. Die Änderung umgeht weder Tests noch Hashes oder privilegierte Kontrollen.

## Geänderte Dateien

- `.github/workflows/update-python-version.yml`
- `tests/test_ci_security_workflows.py`

## Ausgeführte Befehle

- Zielgerichteter Workflow-Sicherheitsregressionstest: nach der Workflow-Änderung bestanden; gegen den Vor-Fix-Workflow schlug er erwartungsgemäß zuerst fehl.
- Fokussierte Python-Workflow- und Vertragstests: 85 bestanden.
- `ci/checks/common/check-python-version-contract.py --json`: bestanden, mit 42 erkannten Jobs und keinen Verstößen.
- `make check-ci-security-contract`: bestanden, mit 103 bestandenen Tests und 4 erwarteten fähigkeitsbeschränkten Skips.

## Runtime-Evidence

Der referenzierte Publisher-Job schlug beim Ausführen von `make check-ci-security-contract` mit `ModuleNotFoundError: No module named 'yaml'` fehl. Der Installer fügt PyYAML ausschließlich über den bestehenden hash-gesicherten Vertrag `requirements-ci.lock` hinzu.

## Bekannte Einschränkungen

Gehostete Pull-Request-Checks sind das nächste Delivery-Gate. Der erste zulässige Publisher-Aufruf nach einem Merge liefert die Ende-zu-Ende-Laufzeitbestätigung; bis dahin ist das Finding lokal behoben, aber nicht zur Laufzeit verifiziert.

## Verbleibende Risiken

Die nur für `master` geltende Admission des Publishers ist eine beabsichtigte Kontrolle. Deshalb können lokale und PR-Validierung seine erste zulässige Hosted-Ausführung nicht ersetzen. Der gesperrte Abhängigkeitsvertrag und der fokussierte Workflow-Sicherheitsregressionstest liefern den stärksten Pre-Merge-Nachweis, ohne diese Grenze zu lockern.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-Updater-Dispatch, App-Token-Mint, Publisher-Branch-Erstellung oder Master-Merge wurde ausgeführt. Die Publisher-Admission erlaubt absichtlich nur Master-Schedule- oder Manual-Dispatch-Läufe, und der Benutzer autorisierte weder Merge noch Rerun. Vollständige Connector-Runtime-Matrizen sind für diese reine CI-Änderung nicht relevant.

## Finaler Diff- und Review-Status

Der eingegrenzte finale Diff enthält nur den gelockten Publisher-
Abhängigkeitsschritt, seine Ordnungsregression und diesen gekoppelten
Nachvollziehbarkeitsrecord samt Index. `git diff --check` bestand. Commit,
Erstellung des Draft-Pull-Requests und gehostete Pull-Request-Checks sind die
verbleibenden Delivery-Schritte für diese Revision.
