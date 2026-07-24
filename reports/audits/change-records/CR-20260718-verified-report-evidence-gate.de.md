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

## Delivery-Evidence (beobachtet am 2026-07-18 UTC)

- Die Implementierung wurde auf `agent/harden-evidence-integrity` als
  `42b31f1c84c0c915a5cb65119714613fbf3e0c40`
  (`ci: enforce verified runtime evidence gate`) committed und gepusht.
- Draft-PR [#55](https://github.com/Easton97-Jens/ModSecurity-conector/pull/55)
  war zum Beobachtungszeitpunkt gegen `master` `OPEN`. Zu dieser Beobachtung lösten lokales `HEAD`,
  `origin/agent/harden-evidence-integrity` und der PR-Head alle auf
  `42b31f1c84c0c915a5cb65119714613fbf3e0c40` auf.
- CodeQL bestand (Check-Run `88069241639`); SonarCloud Code Analysis bestand
  (Check-Run `88069255373`).
- Die Check-Ansicht zu dieser Beobachtung enthielt zwei `report-governance`-Fehler:
  [Job `88069138522`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29640117282/job/88069138522)
  und [Job `88069198804`](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/29640140820/job/88069198804).
  Im zweiten Job bestanden Setup und `Generated report governance`, während
  `Verified runtime evidence gate` fehlschlug. Andere beobachtete Checks
  bestanden oder wurden gemäß ihrem dokumentierten Scope übersprungen; kein
  ausstehendes oder abgebrochenes Ergebnis wurde beobachtet.
- Der Delivery-Status am beobachteten Head war `not_verified_pr`. Dies ist beabsichtigtes
  Fail-Closed-Verhalten: Ein Fehler des strikten Gates darf nicht als Erfolg
  der Runtime-Evidence gelten.

## Bekannte Einschränkungen

Der aktuelle strikte Checker scheitert korrekt, weil kritische bestehende
Reports veraltet sind. `FND-CROSS-0001` (`Evidence freshness manifest contains
stale entries and SHA mismatches`) bleibt `validated`; seine aktuelle
Bewertung erfasst 58 veraltete Einträge und 9 SHA-Mismatches. Diese
Cross-Repository-Evidence-Arbeit darf durch diese reine Workflow-Änderung
weder unterdrückt, manuell regeneriert noch umklassifiziert werden.

## Verbleibende Risiken

Der fehlgeschlagene strikte Gate bleibt ein Delivery-Blocker, bis der Owner von
`FND-CROSS-0001` die veralteten Freshness-Einträge und die Checksum-Mismatch-
Evidence über den etablierten Runtime-Evidence-Pfad abgleicht. Er ist
Gegen-Evidence zu einem gefälschten Governance-only-Erfolg, nicht ein Defekt
dieses Gates.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Generator-Refresh, Connector-Build, Runtime-Harness, Framework-Change
oder MRTS-Vorgang lief. Ein Refresh überschritte die etablierte Evidence-
Generator-Grenze und ersetzt keinen verifizierten Runtime-Run. Die aktuellen
GitHub-Actions-, CodeQL- und SonarCloud-Ergebnisse für den beobachteten
exakten PR-Head-SHA sind oben festgehalten.

## Finaler Diff- und Review-Status

Der fokussierte lokale Regressionstest, YAML-Parse und Whitespace-Diff-Check
bestanden. Commit, Push, Erstellung des Draft-PRs, Exact-Head-Gleichheit,
GitHub Actions, CodeQL und SonarCloud sind oben beobachtet. GitHub meldet
keine Review-Entscheidung. Der Fehler des strikten Evidence-Gates hielt den
beobachteten Head auf `not_verified_pr`; diese Dokumentationskorrektur benötigt
vor einer neuen Delivery-Behauptung einen frischen Exact-Head-Zyklus. Kein
Merge ist autorisiert oder ausgeführt.
