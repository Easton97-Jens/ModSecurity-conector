# FND-FRAMEWORK-0013 — Framework-Workflows erzwingen Token-Minimalrechte, kanonische Berechtigungen und sicheren PR-Checkout nicht konsistent

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0013` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `medium` |
| Confidence / Status | `validated` / `verified` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Aktueller Scope und Beobachtung

## Aktuelle Master-Verifikation vom 2026-07-26

Die folgenden Pre-Fix-Aussagen bleiben als historische Reproduktions-Evidence
erhalten. Sie werden von der aktuellen Disposition abgelöst: Framework-master
`47e50e7bc43ba7a3b5bad1a9448111794f664cc0` besteht den strikten
Workflow-Checker, die fokussierten CI-Security-/Permissions-/Action-Pin-
Controls und die aktuellen Master-Checks. Die Exact-Head- und
Resulting-Master-Hosted-Checks von PR #27 wurden ebenfalls erfolgreich
beobachtet. Keine Berechtigungsinvariante und kein strikter Checker wurde
geschwächt.

Dieses Finding ist erneut geöffnet. Der abgeglichene Workflow-Satz von
Framework-PR #27 verletzt erneut die Berechtigungsinvariante der Minimalrechte:
Der nicht vertrauenswürdige `pull_request`-CodeQL-Job `analyze` gewährt
`security-events: write`, und `cleanup-artifacts` drückt die erforderlichen
Top-Level-Berechtigungen nicht als kanonisches `contents: read`-Mapping aus.
Die historische Exact-Checkout-Remediation bleibt als Evidence erhalten,
etabliert jedoch nicht die Sicherheit der aktuell abgeglichenen
Workflow-Zusammensetzung.

Der aufbewahrte Pre-Fix-Checker beendete sich mit `1` und meldete beide
Diagnosen:

```text
.github/workflows/ci-security-codeql.yml: job 'analyze' grants a write permission in a pull_request workflow
.github/workflows/cleanup-artifacts.yml: top-level permissions must be exactly '{contents: read}'
```

Betroffene Pfade sind `.github/workflows/ci-security-codeql.yml`,
`.github/workflows/cleanup-artifacts.yml`,
`ci/checks/security/check-github-actions-workflows.py` und
`tests/ci_security/test_framework_ci_security_contract.py`. Die relevanten
Symbole und Invarianten sind `pull_request`, `analyze`, `security-events: write`,
Top-Level-`permissions`, `cleanup-artifacts` und
`check-github-actions-workflows.py --check all`.

## Evidence und Reproduktion

Die aktuelle aufbewahrte Pre-Fix-Evidence lautet:

- Run-ID: `20260719T081017Z-framework-pr-resolution-20260719-840082e0`
- Artefakt:
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr27-pre-fix-workflow-contract-diagnostics.md`
- Typ: `pre_fix_pr27_workflow_contract_diagnostics`
- SHA-256:
  `95237ba7fd80715e4fb9086298d4eb6e814d2cf575bc45ccfe4fd58489ab2c61`
- Working Directory: `/var/tmp/codex/worktrees/framework-ci-security`
- Befehl:
  `rtk env PYTHONDONTWRITEBYTECODE=1 python3 ci/checks/security/check-github-actions-workflows.py --check all`
- Exit-Status: `1`; beobachtet `2026-07-19T15:xxZ` (der bereitgestellte
  Receipt bewahrte die exakte Minute nicht); Retention: `retained_task_evidence`.

Der Zustand wurde nach normalem Abgleich von Framework-`origin/master`
`7a12073c28e62a67492dd501b6513b9914fe5df8` in
`agent/expand-framework-ci-security`, nach Merge-Konfliktauflösung und vor der
#27-eigenen Kompatibilitätsreparatur erfasst. Kein Parent- oder MRTS-Pfad wurde
geändert.

Historische Evidence bleibt unverändert erhalten und wird nicht als aktuell
umetikettiert: `20260718T084030Z-expand-framework-ci-security-be8fb24d`,
Artefakt `final-framework-ci-security-local-validation.md`, SHA-256
`979715e7ec9a24e700f04ab6722b5f717b1f229023a6c4de6051c675a79155c5`,
zeichnete einen lokalen Exit `0` am Source-Commit
`768a06b5b734547f8213cc6918c26ef4a8ef9f67` auf. Sie beweist nur die frühere
Exact-Checkout- und Scan-Range-Remediation, nicht die spätere abgeglichene
Workflow-Zusammensetzung.

## Ursache, Auswirkung und Remediation

Die frühere Remediation etablierte exakte Checkout- und Scan-Range-Kontrollen,
aber der abgeglichene Workflow-Satz kombiniert weiterhin einen nicht
vertrauenswürdigen `pull_request`-CodeQL-Analysepfad mit `security-events: write`
und behält einen Cleanup-Permissions-Ausdruck bei, der den späteren kanonischen
strikten Checker verletzt. Ein angreiferkontrollierter Pull Request könnte
deshalb CodeQL mit einem schreibfähigen Token ausführen. Das nichtkanonische
Cleanup-Modell unterläuft außerdem den reviewbaren Permissions-Contract und
riskiert künftigen permissiven Drift.

Die #27-eigene Reparatur muss den strikten Checker unverändert lassen. Sie muss
CodeQL in einen schreibgeschützten, upload-freien nicht vertrauenswürdigen
`pull_request`-Pfad und einen vertrauenswürdigen Nicht-`pull_request`-Upload-Pfad
aufteilen, `cleanup-artifacts` in das kanonische Block-Mapping mit Top-Level
`contents: read` überführen und die bestehenden Kontrollen für exakten
PR-Head-Checkout und Scan-Range erhalten.

## Akzeptanzkriterien und Validierungsplan

- Kein durch `pull_request` ausgelöster Job gewährt eine Schreibberechtigung.
- Der CodeQL-`pull_request`-Pfad ist schreibgeschützt und lädt keine
  Security-Events hoch; jeder `security-events: write`-Upload bleibt auf einen
  vertrauenswürdigen Nicht-`pull_request`-Pfad begrenzt.
- `cleanup-artifacts` deklariert exakt das kanonische Top-Level-
  `contents: read`-Permissions-Mapping in Blocksyntax.
- Der strikte Workflow-Checker und die fokussierten Regressionstests bestehen
  am finalen #27-Exact-Head, ohne
  `ci/checks/security/check-github-actions-workflows.py` zu schwächen.
- Die Negativkontrollen lehnen eine PR-Schreibberechtigung und ein
  nichtkanonisches Cleanup-Modell ab; die Legitimate Controls akzeptieren den
  vertrauenswürdigen Upload-Pfad, das beabsichtigte Cleanup-Mapping und
  Default-Branch-`github.sha`-Verhalten.
- Frische Exact-Head-PR-Checks und der Review-Status werden beobachtet; danach
  werden Original-Reproduktion und Legitimate Controls auf dem resultierenden
  Framework-Master erneut ausgeführt, bevor der Lifecycle fortschreitet.

## Abhängigkeiten, Beziehungen, Restrisiko und Historie

Abhängigkeiten sind die #27-eigene Workflow-Kompatibilitätsreparatur, frische
Exact-Head-PR-Checks/Reviews und der Resulting-Master-Rerun. Dieser Record ist
mit `FND-FRAMEWORK-0012`, dem separaten YAML-Contract-Kompatibilitätsfinding
`FND-FRAMEWORK-0019` und `FND-SONAR-0005` verwandt.

Der aktuelle abgeglichene Pre-Fix-Tree von #27 scheitert nachweislich am
strikten Checker. Es gibt noch kein Post-Fix-lokales Ergebnis, kein
Exact-Head-Remote-Ergebnis und keine Resulting-Master-Verifikation. Keine
Berechtigungsinvariante, keine strikte YAML-Regel und kein Security-Control
ist waived.

`2026-07-18T15:18:00Z`: Die frühere lokale Exact-PR-Head-Remediation wurde bei
`768a06b` als fixed erfasst; diese Evidence bleibt historisch. `2026-07-19T15:35:21Z`:
Der aktuelle Zustand wurde reproduziert und das Finding von `fixed` auf
`in_progress` erneut geöffnet; kein aktueller Implementierungsstand wird als
fixed beansprucht.
