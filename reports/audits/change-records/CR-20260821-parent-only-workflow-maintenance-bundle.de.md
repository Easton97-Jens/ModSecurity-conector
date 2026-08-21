# Change Record: Parent-only-Workflow-Wartungsbündel

**Sprache:** [English](CR-20260821-parent-only-workflow-maintenance-bundle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260821-parent-only-workflow-maintenance-bundle |
| Datum (UTC) | 2026-08-21 |
| Basis-Revision | \`aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf\` |
| Delivery-Status | Der bestehende Parent-only-Pull-Request [#311](https://github.com/Easton97-Jens/ModSecurity-conector/pull/311) ist der einzige Delivery-Weg. Nach der abschließenden Korrektur der veralteten Scaffold-Referenz stehen Exact-Head-Hosted-Checks aus; ein Merge ist nicht autorisiert. Die PRs #306–#308 werden durch diese Aufgabe weder verändert noch geschlossen. |

## Motivation und Problemstellung

Der Benutzer benötigt eine einzige Parent-only-Workflow-Wartung statt mehrerer
separater partieller Action-Updates, die einen zugehörigen CodeQL-Bestandteil
oder den zentralen Lock auslassen und CI rot machen können.

## Akzeptanzkriterien

- Ein Updater besitzt die GitHub-Action- und gesperrte Workflow-Tool-Wartung;
  die Legacy-Checker-/Updater-Workflows und -Skripte sind stillgelegt.
- Ein Kandidat aktualisiert den zentralen Lock zusammen mit jeder geprüften
  passenden Action-Referenz, einschließlich aller CodeQL-\`init\`-,
  \`analyze\`- und \`upload-sarif\`-Suffix-Vorkommen.
- Der Kandidat deckt jede Parent-Datei \`.github/workflows/*.yml\` explizit ab,
  sodass ein neu hinzugefügter lokaler Wrapper nicht stillschweigend vergessen
  werden kann.
- Dependabot erstellt keine separaten \`github-actions\`-Update-PRs; die
  bestehenden Python-Abhängigkeitsupdates bleiben aktiviert.
- Die Wartungsgrenze bleibt Parent-only: kein rekursiver Submodule-Checkout,
  Framework-/MRTS-Pfad, Modultoken, externer Remote, Gitlink-Update oder
  externer Modul-PR-Pfad bleibt bestehen.
- Eine fehlgeschlagene Kandidatenanwendung stellt ihre erlaubten Dateien
  bytegenau wieder her; die Action-Identitätszuordnung ist exakt statt
  substring-basiert.

## Implementierungsentscheidung und Begründung

- \`check-actions-versions.yml\`, \`update-actions-versions.yml\`, ihre
  Python-Skripte und Tests sowie ihre Legacy-Branch-/Report-Ignore-Regel wurden
  entfernt.
- \`update-workflow-tools.yml\` ist jetzt der einzige kanonische Workflow mit
  Resolver, Validator, Publisher und Outcome. Sein Publisher ist explizit auf
  das kanonische Parent-Repository, nicht-Fork, den Default-Branch \`master\`
  und ein erfolgreiches Resolver-Ergebnis begrenzt.
- Nur Dependabots \`github-actions\`-Ökosystemeintrag wurde entfernt. Der eine
  zentrale Lock und Updater erzeugen nun einen vollständigen Kandidaten statt
  drei unabhängige partielle PRs zu akzeptieren.
- \`ci/tools/update-workflow-tools.py\` wurde mit exaktem Remote-Action-Parsing,
  vollständiger Parent-Workflow-Inventargleichheit, expliziter Aufnahme des
  lokalen \`all-connectors-no-crs.yml\`-Wrappers und Rollback über jede erlaubte
  Update-Datei gehärtet.
- Native Workflow-Pin-Tests lösen jedes Remote-\`owner/repo\` auf seinen exakten
  zentralen-Lock-SHA auf. Die Regression-Suite beweist, dass ein
  CodeQL-Kandidat den zentralen Lock und alle zehn \`init\`-/\`analyze\`-/
  \`upload-sarif\`-Referenzen als Einheit ändert.
- Die veraltete Common-Scaffold-Assertion für den stillgelegten Legacy-Updater-
  Test wurde entfernt; die Parent-only-Wartungsregression weist diese veraltete
  Referenz künftig zurück.

## Security-Auswirkung

Der stillgelegte Legacy-Updater checkte Submodule rekursiv aus, akzeptierte ein
Modultoken, leitete einen Submodule-Remote ab und konnte außerhalb des
Parent-Repositorys schreiben oder einen PR öffnen. Seine Entfernung beseitigt
diese validierte Privileg- und Repository-Grenzverletzung. Der verbleibende
Updater bleibt allow-listed, fail-closed, SHA-gepinnt und verwendet die
einzige Parent-Kandidatengrenze.

Ein separates Medium-Confidence-Hardening-Follow-up behält explizite Response-
und Archivgrößenlimits für Release-Metadaten/-Assets fest. Es rechtfertigt
weder das Beibehalten des stillgelegten Modulpfads noch das Aufspalten von
Updates und wird separat als \`FND-PARENT-0205\` verfolgt.

## Geänderte Dateien

- \`.github/dependabot.yml\`
- \`.github/workflows/update-workflow-tools.yml\`
- \`.github/workflows/test-common.yml\`
- \`.gitignore\`
- \`ci/checks/common/check-python-version-contract.py\`
- \`ci/tools/update-workflow-tools.py\`
- \`docs/build/README.md\` und \`README.de.md\`
- \`docs/security/ci-security-tooling.md\` und \`.de.md\`
- \`tests/ci_security/test_ci_security_contract.py\`
- \`tests/ci_security/test_update_workflow_tools.py\`
- \`tests/security_regression/test_workflow_security_contract.py\`
- \`tests/test_ci_security_workflows.py\`
- stillgelegte Legacy-Actions-Wartungsworkflows, Skripte und Tests
- dieses gekoppelte Change-Record-Paar und die gekoppelten Archivindizes

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| \`tests.test_ci_security_workflows\` | bestanden: 28 Tests |
| \`tests.ci_security.test_update_workflow_tools\` | bestanden: 37 Tests einschließlich vollständigem CodeQL-Bündel und Rollback-Controls |
| \`tests.ci_security.test_ci_security_contract\` | bestanden: 13 Tests |
| \`tests.security_regression.test_workflow_security_contract\` | bestanden: 5 Tests |
| \`make check-ci-security-contract\` | bestanden: 122 Tests, 5 erwartete Capability-Skips und Validierung gepinnter Tool-Metadaten |
| \`make check-python-version-contract\` | bestanden: Python 3.14.7 und 40 Python-ausführende Workflow-Jobs |
| Alle Workflow-YAML parsen | bestanden |
| actionlint mit ShellCheck | bestanden |
| offline-zizmor | bestanden: keine Findings; 86 bestehende Suppressions berücksichtigt |
| `make check-bilingual-docs` | nur durch vorbestehende fehlende Ziele im absichtlich nicht initialisierten Framework-Gitlink blockiert; dieses gekoppelte Record-Paar besteht seine erforderlichen Section-Checks |

## Runtime-Evidence

Die synthetischen Kandidaten des Updaters führten den echten Copied-Tree-
Contract aus. Ein gültiger CodeQL-Kandidat ändert den zentralen Lock und jede
geprüfte init/analyze/upload-sarif-Referenz; ein injizierter späterer
Write-Fehler stellt jede erlaubte Datei wieder her. Es wurden kein Live-
Maintenance-Dispatch, kein Token-Mint, kein externer Modul-Write und keine
Submodule-Initialisierung ausgeführt.

## Bekannte Einschränkungen

Kein Framework- oder MRTS-Source, Gitlink, Submodule-Zustand, Token,
Modul-Remote, Legacy-Dependabot-PR oder Merge wird verändert.
\`make check-bilingual-docs\` bleibt durch vorbestehende fehlende Ziele im
absichtlich nicht initialisierten Framework-Gitlink blockiert; die Aufgabe
initialisiert oder verändert dieses getrennte Repository nicht. Hosted-Checks
auf dem exakten Successor-Head von PR #311 bleiben vor jeder \`verified\`- oder
Merge-Behauptung erforderlich.

## Verbleibende Risiken

Die lokale Korrektur ist nicht verified, bis der exakte Successor-Head von
PR #311 anwendbare Hosted-Checks besteht und nach einem autorisierten Merge die
Original-Controls auf resultierendem master bestehen. Das separate
Medium-Confidence-Response-/Asset-/Archiv-Resource-Limit-Hardening-Follow-up
bleibt als FND-PARENT-0205 erhalten.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-Maintenance-Workflow-Dispatch, GitHub-App-Token-Mint, externer
Modul-Write, Submodule-Initialisierung, keine Mutation von PR #306–#308 und
kein Merge wurden ausgeführt. Jeder dieser Schritte würde den Parent-only-
Maintenance-Scope überschreiten oder getrennte Autorität erfordern.

## Finaler Diff- und Review-Status

Der lokale Source-, Test-, Workflow- und Security-Review ist abgeschlossen;
aus stehen der finale Follow-up-Commit/Push zu #311 und die
Exact-Head-Hosted-Ergebnisse. Die Aufgabe behauptet nicht, dass PRs #306–#308
remote geschlossen, gemergt oder ersetzt sind.
