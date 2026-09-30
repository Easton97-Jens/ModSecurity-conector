# Change Record: manueller Framework-Updater ohne feste Struktursperre

**Sprache:** [English](CR-20260930-manual-framework-updater.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260930-manual-framework-updater |
| Datum (UTC) | 2026-09-30 |
| Basis-Revision | `9bc87cbdb600b09c6edd02667a75b117a1f09eea` |
| Zugehörige Auslieferung | Parent-Draft-PR #398; Framework-Draft-PR #132 |

## Motivation und Problemstellung

[Updater-Job 109955091216](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/36735191087/job/109955091216) wies einen neueren Framework-Candidate allein deshalb zurück, weil das `common.sh`-Gerüst nicht mehr zu einem festen Parent-Digest passte. Der Benutzer will den Parent-Updater nur manuell starten und neue Framework-Struktur ohne diese feste Hash-Sperre akzeptieren. Der vorherige direkte Pin in PR #398 zeigte außerdem einen veralteten verschachtelten ModSecurity-Gitlink im Framework; dessen separate Korrektur ist Framework-PR #132.

## Akzeptanzkriterien

Der Parent-Updater hat ausschließlich `workflow_dispatch`, keinen Zeitplan. Ein manuell gestarteter Publishing-Lauf darf neue Framework-Struktur ohne Änderung eines freigegebenen Digests validieren und vorschlagen. Candidate-Git-Zustand, offizieller Origin/Lineage, begrenzte Quell-Datensyntax, Parent-NGINX-Übergabe, isolierte Validierung, enge Publisher-Rechte und Draft-/No-Auto-Merge-Verhalten bleiben Pflicht. Dieser Parent-PR pinnt keinen aktuellen Framework-Candidate direkt.

## Implementierungsentscheidung und Begründung

Den Vergleich mit dem festen Digest aus beiden aktiven Parent-Prüfungen entfernen; begrenzte UTF-8-Lesevorgänge, Quell-Datenparser und unabhängige NGINX-/Parent-Verträge bleiben bestehen. Bekannte indirekte Shell-Zielschreibvorgänge zusätzlich zu vorhandenem `eval` und direkten Mutationen zurückweisen. Wöchentlichen Trigger entfernen und `workflow_dispatch` im Resolver-Gate und Regressionstest verlangen. Parent-Gitlink und Projektionen auf die Basisrevision zurücksetzen, damit der Benutzer den Updater nach separater Prüfung und Merge von Framework-PR #132 starten kann.

## Geänderte Dateien

- `.github/workflows/update-submodules.yml`
- `ci/tools/verify-framework-candidate-contract.py`
- `ci/tools/check-reviewed-version-handoff.py`
- `tests/test_ci_security_workflows.py`
- `tests/test_update_submodules_local_git.py`
- `tests/test_verify_framework_candidate_contract.py`
- `tests/test_reviewed_version_handoff.py`
- `docs/reviewed-version-upgrades.md`
- `docs/reviewed-version-upgrades.de.md`
- `reports/audits/change-records/CR-20260930-manual-framework-updater.md`
- `reports/audits/change-records/CR-20260930-manual-framework-updater.de.md`

## Ausgeführte Befehle

Workflow, beide aktiven Digest-Prüfungen, relevante Tests, Parent-/Framework-Revisionen und die fehlgeschlagenen PR-Jobs wurden über die GitHub-Verbindung geprüft. Der offizielle ModSecurity-v3.0.17-Git-Tree bestätigte unabhängig die Framework-Gitlink-Abweichung. Kein lokaler Repository-Befehl oder Test wird als bestanden behauptet. Hosted-Current-Head-Checks bleiben nach dem Folgecommit erforderlich.

## Security-Auswirkung

Die feste Freigabe des ausführbaren Shell-Struktur-Digests entfällt bewusst auf ausdrücklichen Benutzerwunsch. Ein manueller Start macht beliebige Framework-Shell-Änderungen nicht sicher; statische Prüfungen können nicht alle indirekten Mutationen ausschließen. Der Candidate läuft weiterhin in der schreibgeschützten Validierungs-Sandbox, und der Updater erstellt nur einen Draft-PR. Vollständiger Diff, Provenienz, CI und Runtime-Evidenz müssen vor einem Merge menschlich geprüft werden. Andere Provenienz-, NGINX-, Token-, Pfad-, Rechte- und No-Auto-Merge-Kontrollen bleiben erhalten.

## Runtime-Evidence

Kein neuer Connector-Runtime-Pass ist nachgewiesen. Der vorherige Parent-PR-Head scheiterte bei der NGINX-Bereitstellung mit `modsecurity_v3_framework_provisioning_failed`; Framework-PR #132 korrigiert eine statisch bestätigte verschachtelte Gitlink-Ursache. Nach Framework-Integration sind ein neuer Parent-Updater-PR und dessen Exact-Head-Runtime-Prüfungen nötig.

## Bekannte Einschränkungen

Ein manueller Updater garantiert keinen Erfolg unter allen Umständen: ungültige Candidate-Daten, NGINX-Abweichung, Sandbox-Fehler, inkompatible Dependencies oder ein unsicherer Maintenance-Branch-Zustand können weiter blockieren. Framework-PR #132 ist nicht gemergt. Bis dieser Parent-PR `master` erreicht, bleibt der bestehende wöchentliche Zeitplan aktiv.

## Verbleibende Risiken

Ohne festen Struktur-Digest gelangen künftige Shell-Kontrollflussänderungen in die Sandbox-Validierung und nach unzureichend geprüftem Merge eines generierten Draft-PR möglicherweise später zur Runtime-Ausführung. Das gezielte Muster für indirekte Schreibvorgänge sperrt bekannte Fälle, ist aber kein vollständiger Shell-Parser. Menschliche Prüfung und Current-Head-CI sind wesentliche Restkontrollen.

## Nicht ausgeführte Prüfungen mit Begründung

Lokaler Secrets-Scan, repository-native Unit-/Lint-/Dokumentationsprüfungen, `git diff --check` und Runtime-Tests liefen in dieser projektlosen Windows-Task nicht; die SonarQube-CLI wurde nicht neu autorisiert. Hosted-GitHub-Actions und SonarCloud am finalen PR-Head müssen separat geprüft werden. Statische GitHub-Quellprüfungen ersetzen keine ausgeführten Tests.

## Finaler Diff- und Review-Status

Parent-PR #398 bleibt Draft und wird nicht gemergt. Der finale kumulative Diff darf nur die Regel für den manuellen Updater, ihre Tests und EN/DE-Dokumentation/Record enthalten; der vorherige direkte Framework-Pin wird durch einen normalen Folgecommit rückgängig gemacht. Framework-PR #132 und spätere manuelle Updater-Auslieferung bleiben getrennt.
