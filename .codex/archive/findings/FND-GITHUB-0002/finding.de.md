# FND-GITHUB-0002 — Framework-Dependency-Review ist ohne Dependency-Graph-Zugriff nicht verfügbar

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-GITHUB-0002` |
| Titel | `Framework-Dependency-Review ist ohne Dependency-Graph-Zugriff nicht verfügbar` |
| Kategorie | `github_governance` |
| Repository | `framework` |
| Ownership | `github_configuration` |
| Priorität | `P1` |
| Severity | `not_applicable` |
| Confidence | `confirmed` |
| Status | `closed` |
| Release-Blocker | `true` |
| Security-Relevanz | `true` |

## Zusammenfassung

Der exakte Head `66d90872cfc0125536267d574b776d2e88d26b23` des Framework-Draft-PRs #27 hat einen korrekt gepinnten Dependency-Review-Job mit minimalen Berechtigungen, aber GitHub lehnte ihn ab, weil Dependency Review für dieses Repository nicht unterstützt wird. Der frühere zugehörige Dependency-Graph-SBOM-Endpunkt-Readback lieferte HTTP `404`. Dies ist ein GitHub-Konfigurations-/Zugriffsblocker und kein Framework-Workflow-Defekt, der verborgen oder abgeschwächt werden darf.

## Beobachtetes Verhalten

GitHub-Actions-Run `29647958872` auf dem exakten PR-#27-Head `66d90872cfc0125536267d574b776d2e88d26b23` meldete: `Dependency review is not supported on this repository. Please ensure that Dependency graph is enabled`. Eine frühere nur lesende Anfrage an `repos/Easton97-Jens/ModSecurity-test-Framework/dependency-graph/sbom` lieferte HTTP `404 Not Found`. Die anderen task-eigenen Security-Checks für den exakten aktuellen Head bestanden oder waren wie vorgesehen trigger-skipped.

## Erwartetes Verhalten

Das Framework-Repository stellt die von GitHub Dependency Review benötigte Dependency-Graph-Fähigkeit bereit, und ein Rerun auf dem exakten PR-#27-Head ist erfolgreich, ohne den Job zu unterdrücken, seine Fail-Policy zu ändern, Berechtigungen zu erweitern oder Review-Controls zu umgehen.

## Auswirkung

Der Draft-PR kann `verified_pr` nicht erreichen, solange ein erforderlicher Security-/Dependency-Check fehlschlägt. Dependency- und Lizenzänderungen können daher die vom Workflow vorgesehene repository-native GitHub-Review vermissen, bis die externe Konfigurations-/Zugriffsbedingung behoben ist.

## Betroffene Dateien und Symbole

- `.github/workflows/ci-security-dependency-review.yml`
- `dependency-review`
- `actions/dependency-review-action@a1d282b36b6f3519aa1f3fc636f609c47dddb294`
- GitHub Dependency Graph und sein SBOM-Endpunkt

## Voraussetzungen

- Framework-Draft-PR #27 bleibt auf `66d90872cfc0125536267d574b776d2e88d26b23` offen.
- GitHub Actions und die Dependency-Graph-API bleiben erreichbar.
- Ein Repository-Owner oder Administrator kann die Konfigurationsentscheidung treffen.

## Reproduktion

```text
rtk gh run view 29647958872 --log-failed
rtk proxy gh api -i repos/Easton97-Jens/ModSecurity-test-Framework/dependency-graph/sbom
```

## Evidenz

- Run-ID: `20260718T083435Z-expand-framework-ci-security-32892be1`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T083435Z-expand-framework-ci-security-32892be1/evidence/ci-security/framework-pr27-final-blockers.txt`
  - Typ: `exact_framework_pr_head_ci_and_dependency_graph_readback`
  - SHA-256: `1686ed164f9a892c08c6749ed5d9922269a7a026a442ddd477d62bd240848b5f`
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-ci-security`; Exit-Code: `1`
  - Beobachtet am: `2026-07-18T13:13:38Z`; Aufbewahrung: `retained_task_evidence`
- Run-ID: `20260718T084030Z-expand-framework-ci-security-be8fb24d`
  - Artefakt: `/var/tmp/codex/ModSecurity-conector/runs/20260718T084030Z-expand-framework-ci-security-be8fb24d/evidence/framework-pr27-final-remote-status.md`
  - Typ: `exact_final_pr_head_external_blocker_disposition`
  - SHA-256: `ccedabbe5e020bf43eb91ccf93b1e1484b8d11471e2817b6d078a95eeddb3552`
  - Arbeitsverzeichnis: `/var/tmp/codex/worktrees/framework-ci-security`; Exit-Code: `0`
  - Beobachtet am: `2026-07-18T14:26:12Z`; Aufbewahrung: `retained_task_evidence`

## Grundursachenanalyse

GitHub Dependency Review meldete, dass die benötigte Repository-Fähigkeit nicht unterstützt wird. Das SBOM-HTTP-`404` belegt, dass der Dependency-Graph-Endpunkt im beobachteten Zugriffs-/Konfigurationszustand nicht verfügbar ist; es unterscheidet allein nicht zwischen einer deaktivierten Funktion und einer anderen GitHub-seitigen Berechtigungs- oder Sichtbarkeitsbedingung.

## Vorgeschlagene Remediation

Ein autorisierter Repository-Owner oder Administrator muss Dependency Graph aktivieren oder anderweitig verfügbar machen, die Einstellung bzw. den Readback verifizieren und Dependency Review auf dem unveränderten exakten PR-#27-Head erneut ausführen. Der Workflow darf nicht als Ersatz deaktiviert, advisory geschaltet, übersprungen oder abgeschwächt werden.

## Akzeptanzkriterien

- Autorisierte GitHub-Konfigurations-Evidenz belegt, dass Dependency Graph für `Easton97-Jens/ModSecurity-test-Framework` verfügbar ist.
- Dependency Review endet erfolgreich für den exakten PR-#27-Head `66d90872cfc0125536267d574b776d2e88d26b23` oder einen späteren ausdrücklich verifizierten task-eigenen Head.
- Der immutable Action-Pin, Dependency-/Lizenz-Policy, minimale Berechtigungen und fail-closed Enforcement bleiben unverändert.

## Validierungsplan

- Die Fähigkeit mit autorisierter GitHub-API-Evidenz lesen.
- Nach der Konfigurationsänderung einen erfolgreichen Dependency-Review-Rerun für den exakten Head beobachten.
- Vor jedem `verified_pr`-Claim PR-SHA-Gleichheit, alle aktuellen Checks, SonarQube Cloud, Reviews und Review-Threads erneut prüfen.

## Regression und legitime Kontrolltests

- Dependency Review erreicht `completed/success` auf dem exakten aktuellen PR-Head.
- Eine harmlose Dependency-Manifest-Änderung wird vom gepinnten Action ohne zusätzliche Berechtigungen oder Token-Bypass ausgewertet.

## Abhängigkeiten und Blocker

- Abhängigkeit: Entscheidung und Konfigurationszugriff eines GitHub-Repository-Owners oder Administrators.
- Blocker: Der aktuelle Task autorisiert keine Änderungen an GitHub-Repository-Einstellungen.
- Blocker: GitHub meldet Dependency Review derzeit als unsupported und den SBOM-Endpunkt als nicht verfügbar.

## Verwandte Findings

- `FND-FRAMEWORK-0001` ist ein separater PR-Gate-Blocker und nicht dieselbe technische Ursache.

## Restrisiko

Es wird kein Risiko akzeptiert. Der PR bleibt ein Draft und darf nicht als `verified_pr` bezeichnet werden, bis dieser extern blockierte Check auf einem exakten aktuellen Head erfolgreich ist.

## Aktueller GitHub-Abgleich und Schließung — 2026-07-26

Dieser Abschnitt ersetzt die aktiven Blocker-Aussagen oben, bewahrt sie aber
als historische Evidence. Der nur lesende Framework-Dependency-Graph-SBOM-
Endpunkt liefert jetzt HTTP 200 mit einem SPDX-2.3-Dokument mit 12 Packages.
Framework-PR #42 ist gemergt; sein späterer Head
`dc6cf411e78b3f37f1e4be52edef59894560b1ae` beendete Dependency-Review-
Run 29978759046 und Job 89116042141 erfolgreich.

Der aktuelle Workflow verwendet weiterhin den unveränderlichen
dependency-review-Action-Pin, die contents-read-Permission, High-Severity-
und Runtime/Development-Fail-Policy, License- und Vulnerability-Checks sowie
warn-only false. Nichts wurde deaktiviert, advisory geschaltet, übersprungen
oder mit breiteren Berechtigungen versehen.

Der frühere PR-#27-HTTP-404/Unsupported-Fehler bleibt historische Evidence; er
wird nicht zu einem Pass umgeschrieben. Die jetzt verfügbare GitHub-Fähigkeit
und die spätere erfolgreiche fail-closed-Ausführung erfüllen das erlaubte
Later-Head-Kriterium des Findings. Der Status ist daher `closed`; das
vollständige Tripel wird archiviert. Bei Regression von Dependency Graph oder
des fail-closed Workflows wieder öffnen.

## Historie

- `2026-07-18T13:13:38Z`: `exact_pr_head_dependency_review_blocker_recorded` — Der exakte Head `5b2a26a41e7621e7b246aa1a060149252cfe3062` des Framework-Draft-PRs #27 schlug im GitHub-Actions-Run `29645450452` fehl, weil Dependency Review unsupported ist; der nur lesende Dependency-Graph-SBOM-Endpunkt lieferte HTTP `404`. Dieser Record ist bis zu einer autorisierten GitHub-Konfigurations-/Zugriffsdisposition blockiert und autorisiert keine Workflow-Code-Remediation.
- `2026-07-18T14:26:12Z`: `final_exact_pr_head_blocker_reconfirmed` — Der exakte Head `66d90872cfc0125536267d574b776d2e88d26b23` des Framework-Draft-PRs #27 schlug im Dependency-Review-Run `29647958872` erneut mit derselben Unsupported-Repository-/Enable-Dependency-Graph-Meldung fehl. Alle task-eigenen Security-Gates bestanden ansonsten; Status bleibt `blocked` bis zu einer autorisierten GitHub-Konfigurations- oder Zugriffsauflösung.
