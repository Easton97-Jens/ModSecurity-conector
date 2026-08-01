# FND-PARENT-0049 — Update-Submodules-Dependency-Befehl ist als YAML-Plain-Scalar ungültig

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0049 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schwere | P1 / not_applicable |
| Konfidenz / Status | confirmed / fixed |
| Machbarkeit | requires_user_decision |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Der Initial-Head `f22e3fdb322e93cf9b37e13ede13007c912e0f9b` des Draft-Parent-
[PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) ließ
fünf gemeinsame Struktur-/Quick-Check-Jobs vor der Framework-Candidate-
Validierung fehlschlagen. Der Framework-Workflow-YAML-Checker meldete:

```text
error .github/workflows/update-submodules.yml: invalid YAML
yaml.scanner.ScannerError: mapping values are not allowed here
line 94, column 83: --only-binary=:all: --require-hashes
```

Die eine Ursache betrifft `scaffold-lint`, `quick-check`, `apache-structure`,
`common-structure` und `nginx-structure`; es sind nicht fünf unabhängige
Defekte. Der Fehler tritt vor Candidate-Code und dem schreibfähigen Publisher
auf, schlägt daher fail-closed fehl und erweitert keine Privileggrenze.

Die Quoting-Korrektur und ihre statische Regression liegen auf dem exakten
PR-#92-Head `40a419d5b0f599566469060112b7e55dbab05744`. Seine 39 Hosted-
Checks sind terminal: 33 erfolgreich und 6 erwartungsgemäß übersprungen;
SonarQube Cloud bestand das Quality Gate mit null neuen Issues und null
Security Hotspots. Dies belegt die task-eigene PR-Korrektur, ist aber keine
Evidence des master-only-Workflows.

## Ursache und sichere Reparaturgrenze

Die erste Reparatur setzte `--only-binary=:all:` in einen unquotierten YAML-
Plain-Scalar. Sein schließender Doppelpunkt wird durch folgenden Leerraum als
Mapping-Trenner interpretiert. Den vollständigen `run:`-Befehl quoten und eine
statische Regression hinzufügen, die diese Quote verlangt. Exakten Hash-Lock,
`--require-hashes`, `--only-binary=:all:`, Validator-`contents: read` und den
getrennten gegateten Publisher bewahren. Framework, MRTS, Gitlink,
Berechtigungen, Secrets und Publisher-Code dürfen sich nicht ändern.

## Akzeptanzkriterien und Validierungsplan

1. PyYAML parst den Workflow nach Quoting des Befehls erfolgreich.
2. Statische Coverage verlangt den exakten quotierten Befehl und bewahrt seine
   Reihenfolge zwischen Interpreter-Contract und `make quick-check`.
3. Fokussierte Workflow-Security-Tests, `make check-ci-security-contract`,
   fokussierte bilinguale Tests und `git diff --check` bestehen.
4. Ein fokussierter CI-Supply-Chain-Security-Review deckt das Amendment ab.
5. Frische Exact-Head-PR-#92-Checks ersetzten die initialen Parserfehler auf
   `40a419d5b0f599566469060112b7e55dbab05744`. Nur eine spätere separat
   autorisierte Master-Integration kann den master-only-Ausgang von
   FND-PARENT-0049/FND-PARENT-0048/FND-PARENT-0045 verifizieren.

## Evidenz

Aufbewahrter Beleg:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/pr-92-yaml-scalar-failure.md`

SHA-256:
`68f7d8f2d693799369778f5111864954bacf679e75d5e02794ec73f9c0e9cce2`

Exact-Head-Erfolgsbeleg:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/pr-92-40a419d-exact-head-checks.md`

SHA-256:
`7aff214afed70a39ec9863fc855627e835a6eb66a48ed9873be894de20165d2e`

## Aktuelle Disposition

Der Befund ist `fixed`, nicht `verified`: Der ursprüngliche PR-Head-
Parserfehler reproduziert sich nicht mehr und die legitimen statischen Controls
bestehen, doch die generische Finding-Policy verlangt vor der finalen
Verifikation zusätzlich einen separat autorisierten Merge und einen
master-only-Workflow-Rerun. Es gab keinen Merge, Master-Change,
Framework-Candidate-Publication, Gitlink-Update oder MRTS-Aktion.

## Historie

- `2026-07-23T06:15:15Z` — Die initiale PR-#92-CI zeigte den ungültigen
  Plain-Scalar. Dieser Befund ist von FND-PARENT-0048 getrennt: jener beschreibt
  die fehlende Dependency, dieser die YAML-Encoding-Regression ihrer ersten
  Korrekturimplementierung.
- `2026-07-23T06:42:32Z` — Der finale PR-#92-Head
  `40a419d5b0f599566469060112b7e55dbab05744` schloss den Exact-Head-Hosted-
  Check-Zyklus erfolgreich ab; dieser Befund wechselte zu `fixed` bis zur
  separaten master-only-Verifikation.
