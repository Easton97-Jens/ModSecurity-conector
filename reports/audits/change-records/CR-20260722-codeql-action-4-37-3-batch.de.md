# Change Record: CodeQL-Action-4.37.3-Batch

**Sprache:** [English](CR-20260722-codeql-action-4-37-3-batch.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260722-codeql-action-4-37-3-batch` |
| Datum (UTC) | `2026-07-22` |
| Basis-Revision | `784d79b4e399e2cb64314a3ba63dcf1633c672bd` |
| Grenze | Nur Parent-CI-Security und Nachvollziehbarkeit; Framework, MRTS, Gitlinks und die ursprünglichen Dependabot-PRs #82, #83 und #84 bleiben unverändert. |

## Motivation und Problemstellung

Nach der atomaren v4.37.2-Delivery avancierte Dependabot die ausgewählten PRs
#82, #83 und #84 unabhängig zu getrennten v4.37.3-Updates für `init`,
`upload-sarif` und `analyze`. Jeder davon ist erneut eine unsichere
Teiltransaktion. Dieser task-owned Ersatz wendet das offizielle v4.37.3-Release
konsistent auf alle zehn bestehenden CodeQL-Action-Aufrufe und den Immutable
Lock an.

## Akzeptanzkriterien

- Vier `init`-, vier `analyze`- und zwei `upload-sarif`-Referenzen lösen
  auf den exakten offiziellen Commit `e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81`
  mit ihren v4.37.3-Kommentaren auf.
- `ci/tooling/security-tools.lock.yml` enthält dasselbe v4.37.3/SHA-Paar.
- Kein v4.37.2-CodeQL-Action-Pin, veränderliches Action-Tag, gemischte
  CodeQL-Version, Trigger-/Permission-/Input-/Action-Quellen-Änderung oder
  unverbundene Dependency-Änderung bleibt im abgegrenzten Diff.
- Fokussierte lokale Verträge, vollständiger diff-skopierter Security-Review
  und exakte PR-/Master-Evidence werden wahrheitsgemäß vor vollständiger
  Delivery festgehalten.

## Implementierungsentscheidung und Begründung

Das offizielle annotierte `github/codeql-action`-Tag `v4.37.3` hat Objekt
`c54b30b7df092240050e69945842bc67aee0f0f4` und zeigt auf Commit
`e4fba868fa4b1b91e1fdab776edc8cfbe6e9fb81`; GitHub meldet das Tag als unsigned
und den Ziel-Commit als PGP-verifiziert. Das offizielle Release wurde am
2026-07-22 veröffentlicht. Passende Workflow-Pins und Lock-Eintrag wechseln
atomar. Das frühere v4.37.2-Change-Record-Paar wird nur mit beobachteten
Delivery-Fakten korrigiert.

## Geänderte Dateien

- `.github/workflows/ci-security-codeql.yml`
- `.github/workflows/ci-security-osv.yml`
- `.github/workflows/ci-security-scorecard.yml`
- `ci/tooling/security-tools.lock.yml`
- Beide v4.37.2-Change-Record-Dateien, dieses englisch/deutsche Paar und beide
  Indizes.

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| Offizielle GitHub-API-Inspektion von Release, annotiertem Tag-Objekt und Ziel-Commit für v4.37.3 | bestanden: offizielles Tag zeigt auf den genannten unveränderlichen Commit; Tag-Signatur unsigned, Ziel-Commit PGP-verifiziert. |
| Exakte Inspektion der aktuellen Dependabot-PR-Diffs #82/#83/#84 | bestanden: die drei Teil-Diffs erfordern zusammen vier `init`-, vier `analyze`- und zwei `upload-sarif`-Updates. |
| `make check-ci-security-contract` | bestanden: die fokussierte Workflow-Security-Suite sowie actionlint-, zizmor- und gitleaks-Lock-Parser-Validierungen bestanden. |
| Scoped-v4.37.3-Inventur und `git diff --check` | bestanden: genau zehn Referenzen bleiben (vier `init`, vier `analyze`, zwei `upload-sarif`), die v4.37.2-SHA fehlt in den abgegrenzten Dateien und der Lock stimmt. |
| `python -m unittest -v tests.test_bilingual_docs` | bestanden: alle 11 fokussierten Bilingual-Dokumentations-Unit-Tests bestanden. |
| `make check-bilingual-docs` | blocked_environment: nur bereits bestehende fehlende Framework-Gitlink-Linkziele bleiben; kein Fehler benennt eine v4.37.3-Change-Record-Datei. |
| Vollständiger v4.37.3-Codex-Security-Diff-Scan | bestanden: vollständige Zehn-Dateien-Coverage, keine reportable Findings und keine aufgeschobene Scan-Arbeit; der generierte Report bleibt als task-owned Delivery-Evidence erhalten. |
| Exakte Replacement-PR- und resultierende-Master-Hosted-Checks | ausstehend; Ergebnisse werden erst nach Beobachtung ergänzt. |

## Security-Auswirkung

Dies ist eine CI-Supply-Chain-Änderung. Jeder CodeQL-Action-Aufruf bleibt auf
einen vollständigen SHA eines offiziellen Releases gepinnt. Permissions,
Checkout-Credential-Verhalten, Trigger, Job-Matrizen, Action-Quellen,
Secret-Handling, Scanner und Quality-Gate-Konfiguration bleiben unverändert.
Kein Security-Control wird abgeschwächt.

## Runtime-Evidence

Es ändert sich kein Connector-Runtime-Verhalten. Dieser Batch aktualisiert nur
die CI-Action-Provenienz und ihre zentrale Immutable-Registry.

## Bekannte Einschränkungen

Das offizielle annotierte Tag ist unsigned; die Evidence stützt sich auf das
offizielle Release, das annotierte Tag-Ziel, den vollständigen unveränderlichen
Commit und die von GitHub gemeldete Ziel-Commit-Verifikation. Das lock-weite
`checked_at` bleibt auf `2026-07-16`, weil dieser Batch nicht jeden
Lock-Eintrag revalidiert.

## Verbleibende Risiken

Das Update kann Upstream-Action-Risiko nicht eliminieren; unveränderliches
offizielles Pinnen und unveränderte CI-Controls begrenzen es. Der unabhängige
bestehende Sonar-Master-Quality-Gate-Blocker bleibt unter `FND-SONAR-0001`
getrackt und unverändert.

## Nicht ausgeführte Prüfungen mit Begründung

Exakte Replacement-PR-Checks, Review-/Thread-Status, PR-SonarQube-Evidence und
resultierende-Master-Workflows stehen noch aus. Der breite Bilingual-Checker
ist durch den absichtlich nicht ausgefüllten Framework-Gitlink
umgebungsbedingt blockiert und wird nicht als bestanden ausgegeben.

## Finaler Diff- und Review-Status

Der beabsichtigte finale Diff ist auf die zehn koordinierten v4.37.3-Pins, den
passenden Lock-Eintrag, korrekte v4.37.2-Delivery-Retention, dieses bilinguale
Paar und die beiden Indizes begrenzt. Der neue Supply-Chain-Security-Scan
bestand mit vollständiger Coverage und ohne reportable Finding; der geschützte
Delivery-Zyklus steht noch aus, und die ursprünglichen Dependabot-PRs bleiben
offen.
