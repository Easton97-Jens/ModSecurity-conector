# FND-FRAMEWORK-0019 — Framework-CI-Sicherheits-Workflows sind mit dem kanonischen strikten YAML-Workflow-Sicherheitsvertrag inkompatibel

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-FRAMEWORK-0019` |
| Kategorie | `security_hardening` |
| Repository / Ownership | `framework` / `framework` |
| Priorität / Schwere | `P2` / `medium` |
| Confidence / Status | `validated` / `verified` |
| Machbarkeit | `feasible_now` |
| Release-Blocker | `false` |
| Security-relevant | `true` |

## Zusammenfassung und separate Grenze

## Aktuelle Master-Verifikation vom 2026-07-26

Die aufbewahrten #27/#29-Pre-Fix-Syntaxdiagnosen unten sind historisch.
Framework-master `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` besteht nun den
strikten fail-closed-Checker, die fokussierten Flow-Style-Negativ-Controls und
die legitimen Block-Mapping-/Action-Pin-Controls. Die Exact-Head- und
Resulting-Master-Hosted-Checks von PR #27 wurden erfolgreich beobachtet; die
strikte YAML-Regel wurde weder waived noch geschwächt.

Nachdem PR #27 mit dem #29-Workflow-Checker abgeglichen wurde, behielten seine
CI-Sicherheits-Workflows Flow-Style-YAML-Collections. Der kanonische Checker
lehnt diese Collections absichtlich fail-closed ab, weil kanonische
Block-Mappings Workflow-Berechtigungen und Action-Pins reviewbar halten. Dies
ist eine separate Syntax-Contract-Grenze: Sie ist weder die
Token-Minimalrechte-Berechtigungsinvariante von `FND-FRAMEWORK-0013` noch die
Downloader-Lock-Grenze von `FND-FRAMEWORK-0016`.

Der Scope umfasst `.github/workflows/ci-security-codeql.yml`,
`ci-security-dependency-review.yml`, `ci-security-osv.yml`,
`ci-security-quality.yml`, `ci-security-scorecard.yml`,
`ci-security-secrets.yml` und `ci-security-workflow-lint.yml`; dieselbe
Diagnostik erfasst außerdem die zugehörige Flow-Style-Collection in
`.github/workflows/cleanup-artifacts.yml`. Checker und fokussierte
Contract-Tests sind `ci/checks/security/check-github-actions-workflows.py` und
`tests/ci_security/test_framework_ci_security_contract.py`.

## Evidence und Reproduktion

Die aufbewahrte Pre-Fix-Evidence lautet:

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

Der kanonische Check meldete Flow-Style-YAML-Collections bei CodeQL Zeilen 5,
7 und 30; dependency-review Zeile 5; OSV Zeile 5; quality Zeile 5; Scorecard
Zeilen 5 und 7; secrets Zeile 5; workflow-lint Zeile 5; und cleanup-artifacts
Zeile 8. Er wurde nach Auflösung der zehn textuellen Merge-Konflikte im
normalen Abgleich mit Framework-`origin/master`
`7a12073c28e62a67492dd501b6513b9914fe5df8`, vor der #27-eigenen
Kompatibilitätsreparatur, erfasst. Kein Parent- oder MRTS-Pfad wurde geändert.

## Ursache, Auswirkung und Remediation

Die CI-Sicherheits-Syntax von PR #27 geht dem #29-kanonischen strikten Checker
voraus oder wurde nicht vollständig mit ihm abgeglichen. Flow-Style-Mappings
überstanden den normalen Branch-Abgleich und erzeugen damit einen
deterministischen Contract-Fehler statt eines Grundes, den Checker zu lockern.
Diese Syntax verschleiert Review-Grenzen für Berechtigungen und Action-Pins;
ihre Zulassung würde einen Security-Control schwächen.

Die #27-eigene Reparatur muss jede aufgeführte Flow-Style-Collection in das
kanonische äquivalente Block-Mapping überführen. Sie muss Scanner-Coverage,
gepinnte Action-Identitäten, den strikten Checker und die separate
Berechtigungsremediation `FND-FRAMEWORK-0013` erhalten. Keine Ausnahme und
keine Erweiterung der akzeptierten Syntax ist erlaubt.

## Akzeptanzkriterien und Validierungsplan

- Jeder aufgeführte Workflow enthält keine vom strikten Workflow-Sicherheits-
  Contract abgedeckte Flow-Style-YAML-Collection.
- Der kanonische Checker bleibt fail-closed und besteht `--check all` am finalen
  #27-Exact-Head.
- Fokussierte Negativregressionen lehnen Flow-Style-Mappings weiterhin ab.
- Legitime kanonische Block-Mappings für Berechtigungen und SHA-gepinnte
  Action-Definitionen bleiben akzeptiert.
- Anwendbare lokale Workflow-/Lint-Checks, frische Exact-Head-PR-Checks/Review
  und der Resulting-Master-Rerun von Original-Reproduktion und Legitimate
  Controls verifizieren den reparierten Workflow-Satz.

## Abhängigkeiten, Beziehungen, Restrisiko und Historie

Diese Arbeit hängt von der #27-eigenen YAML-Kompatibilitätsreparatur, der
separaten Berechtigungsremediation `FND-FRAMEWORK-0013`, frischen
Exact-Head-PR-Checks/Review und Resulting-Master-Validierung ab. Sie ist mit
`FND-FRAMEWORK-0013`, `FND-FRAMEWORK-0016` und `FND-SONAR-0005` verwandt.

Der aktuelle abgeglichene Pre-Fix-Workflow-Satz von #27 scheitert am strikten
Syntax-Contract. Es gibt noch keine Post-Fix-lokale, Exact-Head-Remote- oder
Resulting-Master-Evidence. Der strikte Checker wird ausdrücklich weder waived
noch geschwächt.

`2026-07-19T15:35:21Z`: Als validierter, separater Pre-Fix-#27/#29-
Workflow-Contract-Inkompatibilitätsrecord erstellt; keine aktuelle Remediation
oder Remote-Verifikation wird beansprucht.
