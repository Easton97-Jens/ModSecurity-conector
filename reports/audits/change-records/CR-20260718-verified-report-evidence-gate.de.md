# Change Record: Verifizierter Report-Evidence-Gate

**Sprache:** [English](CR-20260718-verified-report-evidence-gate.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-verified-report-evidence-gate` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Grenze | Nur Parent-Workflow und fokussierter Parent-Test; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

Der Workflow `verified-report-governance` führte `make report-governance` aus.
Dessen Checker nutzt absichtlich `--governance-only`. Dadurch konnte ein
erfolgreiches Governance-Ergebnis erscheinen, obwohl kritische Runtime-Evidence
veraltet oder unvollständig war. Das strikte Target
`verified-report-evidence-gate` existierte bereits, wurde aber von keinem
Workflow aufgerufen.

## Akzeptanzkriterien

- Der Workflow für verifizierte Reports führt nach seinem Nicht-Evidence-
  Governance-Check das strikte `make verified-report-evidence-gate` aus.
- Ein fokussierter Regressionstest schlägt fehl, wenn der strikte
  Workflow-Aufruf entfernt wird oder vor dem Governance-Check steht.
- Die Änderung regeneriert keine Reports und behandelt Governance-Ausgabe nicht
  als Runtime-Evidence.
- Framework- und MRTS-Quellen, Gitlinks und generierte Report-Dateien bleiben
  unverändert.

## Implementierungsentscheidung und Begründung

`report-governance` bleibt der vorhandene Layout-/Pfad-/Dokumentations-Check;
der Workflow erhält danach einen separaten strikten Evidence-Gate-Schritt. Das
ist die engste Parent-native Durchsetzung: Das strikte Make-Target ruft den
gleichen Checker ohne `--governance-only` auf und scheitert damit geschlossen
bei veralteter oder blockierter kritischer Runtime-Evidence.

## Geänderte Dateien

- `.github/workflows/verified-report-governance.yml`
- `tests/test_ci_security_workflows.py`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl | Ergebnis |
| --- | --- |
| `make report-governance` mit task-eigenen Runtime-Roots | bestanden: Der Governance-only-Checker meldete `PASS`; sein Path-Policy-Helper führte in der Sandbox keinen erfolgreichen Systempfad-Write aus. |
| `python ci/checks/documentation/check-generated-report-layout.py --connector-root <Parent> --framework-root <Framework>` | erwarteter Fehler: Der strikte Modus lehnte aktuelle veraltete kritische Runtime-/Report-Inputs ab. |
| `PYTHONDONTWRITEBYTECODE=1 <Parent venv>/bin/python -m unittest -v tests.test_ci_security_workflows` vor der Workflow-Änderung | erwarteter Fehler: Der neue Regressionstest fand keinen Aufruf des strikten Gates. |
| `PYTHONDONTWRITEBYTECODE=1 <Parent venv>/bin/python -m unittest -v tests.test_ci_security_workflows` nach der Workflow-Änderung | bestanden: 6 Tests. |
| `git diff --check` | bestanden. |

## Security-Auswirkung

Der Workflow lässt einen Governance-only-PASS nicht länger als verifizierte
Runtime-Evidence gelten. Er verwendet die vorhandene strikte Report-Evidence-
Kontrolle und schwächt keine Stale-Input-, Blocked-Input-, Checksum-,
Manifest-, Pfad- oder Runtime-Diagnose-Checks ab.

## Runtime-Evidence

Es wurde keine Connector-Runtime ausgeführt oder promotet. Die Änderung setzt
Evidence-Validierung durch; sie erzeugt keine Runtime-Evidence.

## Bekannte Einschränkungen

Der aktuelle strikte Checker scheitert korrekt, weil kritische bestehende
Reports veraltet sind. Das ist als Cross-Repository-Evidence-Arbeit erfasst
und darf durch diese reine Workflow-Änderung weder unterdrückt, manuell
regeneriert noch umklassifiziert werden.

## Verbleibende Risiken

Die exakten Ergebnisse von GitHub Actions, CodeQL, SonarQube Cloud, Review und
PR-Head-SHA stehen bis zum
separaten Delivery-Schritt für diesen Branch aus.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Generator-Refresh, Connector-Build, Runtime-Harness, Framework-Change
oder MRTS-Vorgang lief. Ein Refresh überschritte die etablierte Evidence-
Generator-Grenze und ersetzt keinen verifizierten Runtime-Run. Delivery-Checks
sind nur für den finalen exakten PR-Head-SHA aussagekräftig.

## Finaler Diff- und Review-Status

Der fokussierte lokale Regressionstest und der Whitespace-Diff-Check bestanden.
Security-Review, Commit, Push, Pull Request, GitHub Actions, CodeQL, SonarQube
Cloud und Exact-Head-Verifikation stehen aus; kein Merge ist autorisiert oder
ausgeführt.
