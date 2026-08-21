# Change Record: Parent-only-Workflow-Wartungsbündel

**Sprache:** [English](CR-20260821-parent-only-workflow-maintenance-bundle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260821-parent-only-workflow-maintenance-bundle |
| Datum (UTC) | 2026-08-21 |
| Basis-Revision | \`aaeb7c550d8943a584d21f0f5ca5a11cc3706cbf\` |
| Delivery-Status | Der bestehende Parent-only-Pull-Request [#311](https://github.com/Easton97-Jens/ModSecurity-conector/pull/311) ist der einzige Delivery-Weg. Der aktuelle Benutzer autorisiert seine kontrollierte `master`-Integration erst, nachdem frische Exact-Head-Checks sowie Review-/Thread-, Ruleset-, SonarCloud- und Squash-Merge-Voraussetzungen bestehen. Die Dependabot-PRs #306–#308 bleiben offen und unverändert, solange sie nicht separat autorisiert werden. |

## Motivation und Problemstellung

Der Benutzer benötigt eine einzige Parent-only-Workflow-Wartung statt mehrerer
separater partieller Action-Updates, die einen zugehörigen CodeQL-Bestandteil
oder den zentralen Lock auslassen und CI rot machen können. Zu Beginn dieses
Follow-ups enthielt #311 die von den Dependabot-PRs #306–#308 dargestellten
`github/codeql-action`-Aktualisierungen auf v4.37.7 noch nicht.

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
- Der zentrale `github/codeql-action`-Lock und alle zehn geprüften `init`-,
  `analyze`- und `upload-sarif`-Referenzen wechseln gemeinsam auf v4.37.7,
  Commit `ff2f1c621b7f889edc0d3c761ac2e6a3f8cdb0dd`.

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
- Das veraltete hartcodierte Python-Inventar wurde nach dem Stilllegen der zwei
  Legacy-Jobs korrigiert: 36 normale und insgesamt 40 Python-ausführende
  Workflow-Jobs. Die Regression stellt jetzt zusätzlich sicher, dass beide
  stillgelegten Workflow-Job-Identitäten abwesend bleiben.
- Der ausgewählte CodeQL-v4.37.7-Inhalt aus #306–#308 wurde als ein
  zusammenhängender Parent-Patch in #311 übernommen: zentraler Lock und jede
  der zehn passenden CodeQL-`init`/`analyze`/`upload-sarif`-Referenzen werden
  gemeinsam aktualisiert. Dadurch bleibt nicht die unvollständige Form der
  drei ursprünglichen Dependabot-PRs mit nur direkten Referenzen bestehen.

- Der gemeinsame Host-Runtime-Collector wurde gehärtet, nachdem der fokussierte
  Review einen vorab angelegten Same-User-Artefakt-Symlink-Overwrite
  reproduzierte. Er verwendet jetzt für jeden Collector-Read und -Write die
  bestehenden Private-Root-, No-Follow- und atomaren Artefakt-APIs;
  Regressionen weisen sowohl einen Evidence-Root- als auch einen finalen
  Status-Symlink ab und bewahren den externen Sentinel. Der separate
  NGINX-Workflow bleibt unverändert.

## Security-Auswirkung

Der stillgelegte Legacy-Updater checkte Submodule rekursiv aus, akzeptierte ein
Modultoken, leitete einen Submodule-Remote ab und konnte außerhalb des
Parent-Repositorys schreiben oder einen PR öffnen. Seine Entfernung beseitigt
diese validierte Privileg- und Repository-Grenzverletzung. Der verbleibende
Updater bleibt allow-listed, fail-closed, SHA-gepinnt und verwendet die
einzige Parent-Kandidatengrenze.

Der annotierte v4.37.7-Upstream-Tag löst zu
`ff2f1c621b7f889edc0d3c761ac2e6a3f8cdb0dd` auf. GitHub meldet für die
Verifikation des Ziel-Commits `valid`; das Tag-Objekt selbst ist unsigniert.
Der ausgewählte Patch bleibt damit ein unveränderlicher Action-Pin desselben
Upstreams statt einer veränderlichen Tag-Referenz.

Ein separates Medium-Confidence-Hardening-Follow-up behält explizite Response-
und Archivgrößenlimits für Release-Metadaten/-Assets fest. Es rechtfertigt
weder das Beibehalten des stillgelegten Modulpfads noch das Aufspalten von
Updates und wird separat als \`FND-PARENT-0205\` verfolgt.

Der Task-Review reproduzierte außerdem `MSC-SEC-HOSTRUNTIME-001`: Ein früherer
Collector-Fallback folgte nach der Ablehnung durch den sicheren Preflight einem
vorab angelegten `RUNNER_TEMP`-Symlink und erlaubte einen Same-User-Evidence-
Write außerhalb des vorgesehenen Artefakt-Subtrees. Der Successor verwendet
für Root-, Status- und Summary-Pfade die bestehenden descriptor-basierten,
atomaren `O_NOFOLLOW`-APIs. Die lokale Reparatur wird als `FND-PARENT-0206`
verfolgt; sie beweist Artefakt-Root-Integrität, behauptet aber weder Cross-User-
noch Secret-Access oder Privilege-Escalation.

## Geänderte Dateien

- `ci/runtime/common/collect_hostruntime_preflight_evidence.py`
- `tests/test_collect_hostruntime_preflight_evidence.py`
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
- `tests/test_python_version_contract.py`
- dieses gekoppelte Change-Record-Paar und die gekoppelten Archivindizes
- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`

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
| `tests.test_hostruntime_workflow_evidence_contract`, `tests.test_collect_hostruntime_preflight_evidence` und `tests.test_python_version_contract` | bestanden: 30 Tests nach der Python-Inventar-Korrektur |
| `python3 ci/checks/common/check-python-version-contract.py` | bestanden: Python 3.14.7 und 40 Python-ausführende Workflow-Jobs |
| `make check-ci-security-contract` (aktueller lokaler Successor) | bestanden: 122 Tests, 5 erwartete Capability-Skips und Validierung gepinnter Tool-Metadaten |
| actionlint mit ShellCheck | bestanden |
| offline-zizmor | bestanden: keine Findings; 86 bestehende Suppressions berücksichtigt |
| `make check-bilingual-docs` | nur durch vorbestehende fehlende Ziele im absichtlich nicht initialisierten Framework-Gitlink blockiert; dieses gekoppelte Record-Paar besteht seine erforderlichen Section-Checks |
| GitHub-API-Auflösung von `github/codeql-action` v4.37.7 | bestanden: Der annotierte Tag löst zu `ff2f1c621b7f889edc0d3c761ac2e6a3f8cdb0dd` auf; GitHub meldet die Verifikation des Ziel-Commits als `valid` |
| Follow-up-CodeQL-Lock-/Referenz-Unit-Contract | bestanden: 83 Tests über `tests.test_ci_security_workflows`, `tests.ci_security.test_update_workflow_tools`, `tests.ci_security.test_ci_security_contract` und `tests.security_regression.test_workflow_security_contract` |
| `make check-ci-security-contract` (Follow-up) | bestanden: 122 Tests, 5 erwartete Capability-Skips und Validierung der actionlint/zizmor/gitleaks-Lock-Metadaten |
| Alle Parent-Workflow-YAML parsen | bestanden: 27 `.github/workflows/*.yml`-Dateien |
| Collector-Symlink-Grenze und Runtime-Artefakt-Controls | bestanden: 44 Tests über Collector-, Runtime-Artefakt-, Host-Runtime-Workflow- und Python-Inventar-Contracts; beide vorab angelegten Symlink-Sentinels blieben unverändert |

## Runtime-Evidence

Die synthetischen Kandidaten des Updaters führten den echten Copied-Tree-
Contract aus. Ein gültiger CodeQL-Kandidat ändert den zentralen Lock und jede
geprüfte init/analyze/upload-sarif-Referenz; ein injizierter späterer
Write-Fehler stellt jede erlaubte Datei wieder her. Es wurden kein Live-
Maintenance-Dispatch, kein Token-Mint, kein externer Modul-Write und keine
Submodule-Initialisierung ausgeführt.

Die fokussierte Host-Runtime-Validierung reproduzierte den ursprünglichen
Same-User-`status.json`-Symlink-Overwrite nur in einem disposable externen
Scan-Pfad. Die Successor-Regression weist danach sowohl den Evidence-Root- als
auch den finalen Status-Symlink vor Command-Ausführung ab und bewahrt den
Sentinel bytegenau.

## Bekannte Einschränkungen

Kein Framework- oder MRTS-Source, Gitlink, Submodule-Zustand, Token,
Modul-Remote oder Legacy-Dependabot-PR wird verändert.
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

Das lokal behobene FND-PARENT-0206 benötigt weiter Exact-Head-Checks des
Successor-PRs und Resulting-Master-Evidence, bevor es verified werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Live-Maintenance-Workflow-Dispatch, GitHub-App-Token-Mint, externer
Modul-Write, Submodule-Initialisierung oder eine Mutation von PR #306–#308
wurde ausgeführt. Ein Merge ist noch nicht erfolgt: Der Successor-Head von
#311 benötigt noch die oben festgehaltenen frischen Hosted-Checks und
kontrollierten Integrationsvoraussetzungen.

## Finaler Diff- und Review-Status

Der lokale Source-, Test-, Workflow- und Security-Review läuft für den exakten
Successor von PR #311. Die aktuelle Aufgabe autorisiert einen kontrollierten
Squash-Merge erst, nachdem Exact-Head-Hosted-Checks und alle Repository-Regeln
bestehen. Der CodeQL-Patch verändert den separaten NGINX-Workflow nicht. Die
Aufgabe behauptet nicht, dass PRs #306–#308 remote geschlossen, gemergt oder
ersetzt sind.
