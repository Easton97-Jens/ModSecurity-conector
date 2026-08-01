# FND-PARENT-0048 — Update-Submodules-Validierung verfügt nicht über ihre deklarierte PyYAML-Voraussetzung

## Identität

| Feld | Wert |
| --- | --- |
| ID | FND-PARENT-0048 |
| Kategorie | ci_failure |
| Repository / Ownership | parent / parent |
| Priorität / Schwere | P1 / not_applicable |
| Konfidenz / Status | confirmed / closed |
| Machbarkeit | feasible_now |
| Release-Blocker | ja |
| Sicherheitsrelevant | ja |

## Beobachtung und Auswirkung

Der autorisierte [Run 29981644356](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29981644356)
lief gegen Parent-`master` `ad953cdcbc8c05ede519661ca56c03cf7b1ac7f3`.
Er löste den Candidate `f73f8842f45318e2df8aff1d31855eeb7c20a22f` auf,
führte den read-only-Candidate-Checkout aus, wählte Python `3.14.6` und bestand
den Interpreter-Vertrag. Danach scheiterte `make quick-check` bei
`check-framework-fixture-syntax` mit:

```text
PyYAML is required for fixture syntax lint
```

Der Publisher wurde übersprungen. Kein Candidate-Branch, PR, Parent-Gitlink,
Framework-Source oder MRTS-Status wurde verändert. Dies blockiert die
Veröffentlichung gültiger Candidates, bleibt aber fail-closed und öffnet keinen
privilegierten Pfad.

## Ursache und sichere Reparaturgrenze

`requirements-dev.txt` deklariert bereits `PyYAML>=6,<7`, und der Checker
schlägt absichtlich fehl, wenn er diese Abhängigkeit nicht importieren kann.
Der Validierungsjob richtet den Interpreter ein, installiert aber vor `make
quick-check` keine Validierungsabhängigkeit.

Ein CI-only-PyYAML-6.0.3-Lock wird nach `Verify Python interpreter contract`
und vor `Run quick check without write permissions` installiert. Er verwendet
`--require-hashes` und `--only-binary=:all:` und akzeptiert nur das geprüfte
GitHub-hosted-Linux-x86_64-Wheel. Die plattformübergreifende Development-
Deklaration bleibt unverändert. Statische Coverage sichert Lock-Identität,
Hash und Reihenfolge ab. Berechtigungen, Candidate-Ausführungsgrenze,
Publisher, Parent-Gitlink, Framework und MRTS dürfen sich nicht ändern.

## Sicherheitsbewertung

Remote-Framework-Inhalt läuft nur im `contents: read`-Validator; der getrennte
Writer läuft nur nach Erfolg, validiert den vollständigen offiziellen SHA
erneut, checkt kein Submodule aus und ändert nur den Parent-Gitlink. Diese
Topologie ist `already_safe`. Die Korrektur fügt weder ein explizit injiziertes
Secret noch eine Schreibberechtigung oder einen Publisher-Pfad hinzu. Die neue
Package-Acquisition-Grenze ist hash-gelockt und weist Source-Distributionen
zurück.

## Akzeptanzkriterien und Validierungsplan

1. Der Validator installiert den CI-only-unveränderlichen-PyYAML-Lock in der
   dokumentierten Reihenfolge.
2. Der Lock akzeptiert nur den geprüften PyYAML-6.0.3-Linux-x86_64-Wheel-Hash
   und weist Source-Distributionen zurück.
3. Statische CI-Security-Coverage beweist Befehl, Lock-Identität/-Hash,
   Reihenfolge, exakte Job-Berechtigungen und Resolver → Validator →
   Publisher-Gating.
4. Fokussierte Workflow-Tests, Lock-Metadatenvalidierung, `make
   check-ci-security-contract`, ein fokussiertes Security-Diff-Review und
   `git diff --check` bestehen ohne lokale/System-Paketinstallation.
5. Ein task-eigener Parent-PR enthält Source, Regression, vollständigen
   englischen/deutschen Change Record und tatsächliche Evidenz; er wird von
   dieser Aufgabe nicht gemergt.
6. Erst eine spätere separat autorisierte Master-Integration mit einem
   frischen erfolgreichen Current-Master-Run kann diesen Befund verifizieren.

## Abhängigkeiten, Blocker und Restrisiko

`requirements-dev.txt` bleibt die plattformübergreifende Development-
Deklaration; der CI-only-Lock ist die unveränderliche Authority für diesen
hosted Linux-x86_64-Schritt. Der Lock schlägt bei einem Plattformwechsel bis zu
seiner Prüfung fail-closed fehl. Der nur auf `master` laufende Workflow kann
keinen neuen PR-Head beweisen; der Hosted-Workflow bleibt daher bis zu einer
separaten Master-Autorisierung ausstehend. Die Candidate-Veröffentlichung
bleibt bis dahin blockiert; es wird kein Sicherheitsrisiko akzeptiert.

## Evidenz

Aufbewahrter Beleg:
`/var/tmp/codex/ModSecurity-conector/runs/20260723T051154Z-fnd-parent-0045-update-submodules-validation-0a8cca09/evidence/update-submodules-run-29981644356.md`

SHA-256:
`ee0f259951d639b96624e9bccc84fd45f5384845eb95b42e84e75535e3baa412`

## Historie

- `2026-07-23T05:15:37Z` — Der einzelne autorisierte Current-Master-Dispatch
  zeigte diesen separaten Dependency-Preparation-Fehler, nachdem der Full-SHA-
  Resolver und der read-only-Candidate-Checkout erfolgreich waren. Der
  Publisher wurde korrekt übersprungen. Dieser Record ist von
  `FND-PARENT-0045` getrennt, weil Ursache und Reparaturgrenze verschieden
  sind.
- `2026-07-23T06:34:43Z` — Die erste `FND-PARENT-0048`-Korrektur-
  Implementierung führte den getrennten `FND-PARENT-0049` ein: Ein
  unquotierter `--only-binary=:all:`-Befehl machte den Workflow vor Validator-
  oder Publisher-Ausführung zu ungültigem YAML. `FND-PARENT-0048` bleibt die
  fehlende PyYAML-Voraussetzung; `FND-PARENT-0049` besitzt die YAML-Scalar-
  Quoting-Regression.

## Geschlossene Disposition — 2026-08-01

[PR #92](https://github.com/Easton97-Jens/ModSecurity-conector/pull/92) wurde
normal als `95fb4917b63dd8a5c5973bb49fd955bd3d2b29a3` gemergt und ist vom
aktuellen `origin/master` `59aba762f2d852fd917079ca8519e4ea7f49169c` erreichbar.
Der aktuelle Workflow installiert die hash-gesperrte Validierungsabhängigkeit
vor dem Quick Check; der aktuelle Master-Quick-Check bestand sowohl diesen
Installations- als auch den Read-only-Quick-Check-Schritt. Die exakten
PR-Checks bestanden.
