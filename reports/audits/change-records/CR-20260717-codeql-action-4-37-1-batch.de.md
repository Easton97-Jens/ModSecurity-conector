# Change Record: CodeQL-Action-4.37.1-Batch

**Sprache:** [English](CR-20260717-codeql-action-4-37-1-batch.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260717-codeql-action-4-37-1-batch` |
| Datum (UTC) | `2026-07-17` |
| Basis-Revision | `02f9f98cdbbdd70bbc530ac1399974e53884f4e9` |
| Grenze | Nur Parent-CI-Security und Nachvollziehbarkeit; Framework, MRTS, Gitlinks und PR #51 bleiben unverändert. |

## Motivation und Problemstellung

Die Dependabot-PRs #48, #49 und #50 aktualisierten jeweils unabhängig einen
Teil von `github/codeql-action` von v4.37.0 auf v4.37.1. Die
Immutable-Action-Registry des Repository lehnte jede Teilaktualisierung
korrekt ab; außerdem erzeugte die Aktualisierung nur von `init` oder
`analyze` eine CodeQL-Konfigurationsversionsabweichung. Diese Änderung wendet
das verifizierte Release als einen konsistenten Batch an.

## Akzeptanzkriterien

- Jede Referenz von `github/codeql-action/init`,
  `github/codeql-action/analyze` und `github/codeql-action/upload-sarif`
  löst auf den vollständigen Commit
  `7188fc363630916deb702c7fdcf4e481b751f97a` mit ihrem v4.37.1-Kommentar auf.
- `ci/tooling/security-tools.lock.yml` enthält denselben v4.37.1-Commit.
- In den abgegrenzten Workflows bleibt keine CodeQL-Action-Referenz v4.37.0,
  kein veränderliches Action-Tag, keine gemischte CodeQL-Action-Version, keine
  unerwartete Action-Quelle, Permissions-Änderung, Trigger-Änderung oder
  Matrix-Änderung zurück.
- Fokussierte lokale Verträge sowie die resultierenden exakten PR- und
  `master`-Checks bestehen, bevor dieser Record für die Delivery finalisiert
  wird.

## Implementierungsentscheidung und Begründung

Die Releasequelle ist das offizielle annotierte Tag `v4.37.1` von
`github/codeql-action`. Sein Tag-Objekt
`bb16b9baa2ec4010b29f5c606d57d01190139edd` zeigt auf den offiziellen Commit
`7188fc363630916deb702c7fdcf4e481b751f97a`. Die zehn bestehenden
unveränderlichen Workflow-Referenzen und der zugehörige Registry-Eintrag werden
atomar aktualisiert. Die unabhängigen Dependabot-PRs werden erst abgelöst,
nachdem der Ersatz-Pull-Request erstellt und verlinkt ist.

## Geänderte Dateien

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- Dieses englisch/deutsche Change-Record-Paar.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `make print-python` | bestanden: Der ausgewählte Repository-Interpreter ist `/root/git/ModSecurity-conector/.venv/bin/python`. |
| `make check-framework` | bestanden: Das konfigurierte Framework-Root existiert; kein Framework-Inhalt wurde geändert. |
| `PYTHONDONTWRITEBYTECODE=1 make check-ci-security-contract` | bestanden: alle fünf fokussierten Tests sowie die Lock-Record-Validierungen für Actionlint, Zizmor und Gitleaks bestanden. |
| Checksum-verifiziertes Actionlint mit `/usr/bin/shellcheck` über jeden Workflow | bestanden. |
| Checksum-verifiziertes `zizmor --offline .github/workflows` | bestanden: keine Findings; 77 konfigurierte Suppressions wurden gemeldet. |
| Zizmor-sichere und absichtlich unsichere Fixtures | bestanden: sichere Fixture akzeptiert; unsichere Fixture erwartungsgemäß abgelehnt (Exit 14, Dangerous-Trigger-/Template-Injection-Findings). |
| Exact-Ten-Reference-Scoped-Diff-Invariant und `git diff --check` | bestanden: kein veralteter/gemischter CodeQL-Pin; Workflow-Diff ändert nur die zehn beabsichtigten `uses`-Zeilen. |
| Direkte Change-Record-Schema- und EN/DE-Strukturparitätskontrolle | bestanden. |
| Initiales `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | fehlgeschlagen, weil diesem neuen Record erforderliche Überschriften und Identitätsfelder fehlten; vor der finalen Kontrolle korrigiert. |
| Finales `PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs` | durch den nicht ausgefüllten Framework-Gitlink im isolierten Worktree blockiert; nur bereits bestehende Framework-Linkziele fehlten, und es blieb kein Change-Record-Schema-/Paritätsfehler. |
| `PYTHONDONTWRITEBYTECODE=1 make check-doc-links` | durch denselben nicht ausgefüllten Gitlink blockiert; sein Repository-Path-Checker meldete nur bestehende Framework-Linkziele. |

Der isolierte Task-Worktree enthält das Framework nur als nicht ausgefüllten
Gitlink. Deshalb meldete der erste Dokumentationsscan dort auch bereits
vorhandene Framework-Linkziele als nicht verfügbar. Es wurde kein abgegrenzter
Dokumentationslink geändert. Die finale Dokumentations-Evidence unterscheidet
einen erfolgreichen Schema-Check von einem umgebungslimitierten vollständigen
Link-Check.

## Security-Auswirkung

Dies ist eine Supply-Chain- und CI-Security-Änderung. Jeder CodeQL-Action-Aufruf
bleibt ein offizieller vollständiger unveränderlicher Release-Commit; Registry,
`init` und `analyze` verwenden dasselbe Release. Bestehende minimale
Permissions, Action-Quellen, CodeQL-Scope, Trigger, Secret-Handling und
Security-Checks bleiben erhalten. Kein Scanner, Quality Gate oder Schutz wird
abgeschwächt.

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Die aktuellen Dependabot-Job-
Logs zeigten, dass Teilaktualisierungen an der Immutable-Action-Registry
scheitern und Teilaktualisierungen von `init` oder `analyze` die
CodeQL-Versionskonsistenz verletzen; dieser Batch beseitigt beide Teilzustände
konstruktiv.

## Bekannte Einschränkungen

Der GitHub-Signaturstatus des offiziellen annotierten Tags ist `unsigned`.
Die Verifikations-Evidence stützt sich daher auf das offizielle
Upstream-Repository, Release, annotierte Tag-Ziel und den vollständigen
Commit-SHA statt auf eine Tag-Signaturbehauptung.

## Verbleibende Risiken

Der Batch kann Upstream-Action-Risiko nicht eliminieren. Das Pinnen des
offiziellen vollständigen Release-Commits, das Beibehalten der Registry-Evidence
und die unveränderten bestehenden CI-Security-Kontrollen begrenzen dieses
Dependency-Risiko. Es wird kein Risiko akzeptiert.

## Nicht ausgeführte Prüfungen mit Begründung

Exakte Replacement-PR-Checks, Review-/Thread-Status, SonarQube-Evidence und
finale `master`-Workflows stehen aus. Vollständige bilingualen/
Dokumentationslink-Ziele können in diesem isolierten Worktree nicht verifiziert
werden, weil sein Framework-Gitlink absichtlich nicht ausgefüllt ist; die
gezielte Change-Record-Schema-/Paritätskontrolle bestand. Kein Check wird als
bestanden dargestellt, bevor er auf dem relevanten exakten Head lief.

## Finaler Diff- und Review-Status

Fokussierte Security-Validierung, Scoped-Diff-Review und gezielte Change-
Record-Schema-/Paritätskontrolle bestanden. Der frühere Change-Record-
Schemafehler ist korrigiert. Die einzige lokale Einschränkung sind fehlende
Framework-Inhalte für die vollständigen Tree-Link-Checks. Exakte
Replacement-PR-Evidence, autorisierter Squash-Merge, finale `master`-
Workflows und sichere Wiederherstellung des Parent-Workspaces stehen weiterhin
aus.
