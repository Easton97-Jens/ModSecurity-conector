# Change Record: Verifizierter Report-Evidence-Gate

**Sprache:** [English](CR-20260718-verified-report-evidence-gate.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-verified-report-evidence-gate` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Grenze | Nur Parent-Workflow und fokussierter Parent-Test; Framework und MRTS bleiben unverändert. |
| Grenze der Erweiterung 2026-07-26 | Parent-only Source-/Test-Remediation, die die öffentliche Framework-API am durch den bestehenden Gitlink festgehaltenen `77d73decd094a8f289fbe0ef2582f12430923e24` verwendet; Framework-/MRTS-Source und Gitlinks bleiben unverändert. |
| Finding-Status 2026-07-26 | `FND-PARENT-0050` und `FND-CROSS-0001` bleiben bis frische Evidence vorliegt offen; der #74-Apache-Producer-Blocker ist separat. |

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

### Kriterien der Erweiterung 2026-07-26

- Die Parent-Vorbereitung des ModSecurity-v3-Source verwendet die öffentliche
  Framework-API `ci_provision_approved_modsecurity_v3_checkout` statt einer
  generischen V3-Akquisition; abgelehnte Konfigurations- oder Bridge-Ergebnisse
  können nicht auf `prepare_git_component` zurückfallen.
- Der Parent reserviert ein marker-eigenes, aber fehlendes Staging-Child für
  die Fresh-only-API des Frameworks, verifiziert und versiegelt es danach und
  publiziert es erst nach Framework-Freigabe atomar.
- Nachfolgende Source-Metadaten verwenden verifiziertes `/usr/bin/git` mit
  einer minimalen, bereinigten Umgebung statt eines vom Aufrufer gesteuerten
  Git-Status.
- Eine nach der Provisionierung erfolgende abgelehnte Framework-Verifikation
  bewahrt einen vorhandenen vollständigen Final-Cache und entfernt nur
  Staging-Pfad und -Marker; sie kann weder einen Completion-Marker schreiben
  noch den abgelehnten Checkout publizieren.
- Lokale Parent- und read-only-Framework-Regressionskontrollen sind unten
  festgehalten; es wird keine Connector-Runtime-Evidence, kein Exact-Head-
  Hosted-Erfolg und kein Merge behauptet.

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
- `ci/provisioning/components/prepare-runtime-components.py` (Erweiterung
  2026-07-26): Ersetzt generische ModSecurity-v3-Akquisition durch die
  Framework-eigene Provisionierungs-Bridge und einen fail-closed Cache-
  Publication-Flow.
- `tests/test_prepare_runtime_components.py` (Erweiterung 2026-07-26): Deckt
  Bridge-Provenance, vertrauenswürdige Metadaten, den Ausschluss eines
  generischen Fallbacks und die Bewahrung bei Post-Provision-Rejection ab.

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

Die Erweiterung vom 2026-07-26 hält auch die ModSecurity-v3-Akquisition an der
Framework-eigenen Immutable-Provenance-Grenze. Der Parent verwendet die
festgehaltene öffentliche API für einen frischen Checkout, behält die
bestehende build-time-Framework-Verifikation bei und kann einen durch die
Bridge erzeugten Checkout erst nach einer separaten Post-Provision-
Verifikation publizieren. Die Metadaten-Probes verwenden den verifizierten
Host-Git-Pfad mit bereinigter Umgebung; keine generische Git-Akquisition,
Berechtigungs-, Secret-, Runtime- oder Report-Evidence-Kontrolle wird
geschwächt.

## Runtime-Evidence

Es wurde keine Connector-Runtime ausgeführt oder promotet. Die Änderung setzt
Evidence-Validierung durch; sie erzeugt keine Runtime-Evidence.

Die Parent-44-Test- und Framework-18-Test-Kontrollen vom 2026-07-26 sind nur
lokale Unit-/Security-Regression-Evidence. Sie belegen kein Connector-
Runtime-Ergebnis, kein Exact-Head-Hosted-Ergebnis, keine Review-Disposition,
keinen Merge und keine Resulting-Master-Evidence.

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

`FND-PARENT-0050` und `FND-CROSS-0001` bleiben bis frische Evidence vorliegt
offen. Der #74-Apache-Producer-Blocker ist von dieser Parent-only-V3-Bridge-
Erweiterung getrennt und wird hier weder behoben noch umklassifiziert.

## Verbleibende Risiken

Der fehlgeschlagene strikte Gate bleibt ein Delivery-Blocker, bis der Owner von
`FND-CROSS-0001` die veralteten Freshness-Einträge und die Checksum-Mismatch-
Evidence über den etablierten Runtime-Evidence-Pfad abgleicht. Er ist
Gegen-Evidence zu einem gefälschten Governance-only-Erfolg, nicht ein Defekt
dieses Gates.

Die Bridge scheitert fail-closed, wenn Framework-Provisionierung,
Post-Provision-Verifikation, Metadaten-Erhebung, Versiegelung oder atomare
Publication nicht abgeschlossen werden können. Das bewahrt einen vorhandenen
Final-Cache, statt ihn als frische Evidence zu behandeln. Frische Runtime-
Evidence, Exact-Head-Hosted-Validierung, Review- und Merge-Evidence bleiben
vor jeder Delivery-Erfolgsbehauptung erforderlich. Kein Risiko wird akzeptiert,
und der separate #74-Apache-Producer-Blocker bleibt außerhalb dieser
Erweiterung.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Generator-Refresh, Connector-Build, Runtime-Harness, Framework-Change
oder MRTS-Vorgang lief. Ein Refresh überschritte die etablierte Evidence-
Generator-Grenze und ersetzt keinen verifizierten Runtime-Run. Die aktuellen
GitHub-Actions-, CodeQL- und SonarCloud-Ergebnisse für den beobachteten
exakten PR-Head-SHA sind oben festgehalten.

Für die Erweiterung vom 2026-07-26 lief keine Connector-Runtime, kein Hosted-
Exact-Head-CI, SonarQube Cloud, Review, Merge, Resulting-Master-Workflow,
Framework-Change, MRTS-Vorgang oder #74-Apache-Producer-Remediation. Die
festgehaltenen lokalen Kontrollen können keine dieser Evidence-Klassen
ersetzen.

## Finaler Diff- und Review-Status

Der fokussierte lokale Regressionstest, YAML-Parse und Whitespace-Diff-Check
bestanden. Commit, Push, Erstellung des Draft-PRs, Exact-Head-Gleichheit,
GitHub Actions, CodeQL und SonarCloud sind oben beobachtet. GitHub meldet
keine Review-Entscheidung. Der Fehler des strikten Evidence-Gates hielt den
beobachteten Head auf `not_verified_pr`; diese Dokumentationskorrektur benötigt
vor einer neuen Delivery-Behauptung einen frischen Exact-Head-Zyklus. Kein
Merge ist autorisiert oder ausgeführt.

## Erweiterung: Öffentliche Framework-V3-Provisionierungs-Bridge im Parent (2026-07-26 UTC)

Diese datierte Erweiterung bewahrt die obenstehende Delivery-Evidence vom
2026-07-18 als historische Beobachtung. Sie hält eine getrennte Parent-only-
Remediation fest, die die öffentliche Framework-API
`ci_provision_approved_modsecurity_v3_checkout` an der durch den Parent-
Gitlink bereits festgehaltenen Framework-Revision
`77d73decd094a8f289fbe0ef2582f12430923e24` verwendet. Sie ändert weder
Framework-Source noch MRTS-Source oder Gitlinks.

Der Parent delegiert die ModSecurity-v3-Akquisition nicht länger an das
generische `prepare_git_component`. Nachdem der vorhandene Provenance-
Konfigurations-Guard besteht, reserviert er nur einen verwalteten Registry-
Marker für ein neues, fehlendes Staging-Child. Die Framework-API besitzt die
Erzeugung dieses frischen Childs. Der Parent führt danach eine Framework-
Checkout-Verifikation durch, liest Metadaten über verifiziertes `/usr/bin/git`
mit minimaler bereinigter Umgebung, versiegelt den verwalteten Cache-Eintrag
und publiziert ihn atomar. Ein vorhandener Final-Cache wird nicht berührt, bis
alle diese Schritte bestehen.

Die Post-Provision-Rejection-Regression erzeugt einen vorhandenen vollständigen
Final-Cache, lässt die Framework-Bridge nach Erzeugung des marker-eigenen,
fehlenden Staging-Childs Erfolg melden und lehnt dieses Child anschließend über
`verify_framework_approved_modsecurity_v3_checkout` ab. Sie beweist, dass der
zurückgegebene Record mit der Post-Provision-Guard-Klassifikation blockiert ist,
die Final-Cache-Inhalte und der Completion-Marker intakt bleiben, Staging-Pfad
und -Marker entfernt werden und weder `write_cache_entry_completion`,
`atomic_publish_dir` noch das generische `prepare_git_component` verwendet
werden.

### Lokale Kontrollen, beobachtet am 2026-07-26 UTC

| Kontrolle | Ergebnis |
| --- | --- |
| `rtk env PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 MODSECURITY_FRAMEWORK_TEST_ROOT=<read-only Framework at 77d73decd094a8f289fbe0ef2582f12430923e24> <Parent venv>/bin/python -m unittest -v tests.test_prepare_runtime_components tests.test_runtime_component_cache_contract` | bestanden: 44 Parent-Tests in 8.752s. |
| `rtk env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 TMPDIR=<task-owned external root> <Parent venv>/bin/python -m unittest -v tests.security_regression.test_modsecurity_v3_git_ref_provenance` im isolierten read-only-Framework-Worktree bei `77d73decd094a8f289fbe0ef2582f12430923e24` | bestanden: 18 Framework-Tests in 61.476s; es wurden nur task-eigene temporäre Fixtures verwendet, ohne Framework-Source-, Gitlink- oder MRTS-Modifikation. |
| `rtk git diff --check` im #55-Parent-Worktree vor diesem Dokumentations-Amendment | bestanden. |
| `rtk make check-bilingual-docs` nach diesem Dokumentations-Amendment | blocked_environment: 20 bestehende fehlende lokale Link-Ziele unterhalb des nicht initialisierten Gitlinks `modules/ModSecurity-test-Framework`; keine Diagnose nannte eines der beiden geänderten Change Records. |
| `rtk env PYTHON=<Parent venv> PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PIP_REQUIRE_VIRTUALENV=true PIP_DISABLE_PIP_VERSION_CHECK=1 make check-bilingual-docs` nach Materialisierung der bereits festgehaltenen Framework-/MRTS-Revisionen in diesem isolierten Task-Worktree | bestanden: `bilingual docs ok`; die Materialisierung änderte weder Framework-/MRTS-Source noch Gitlink, Branch oder Delivery-Status. |
| `rtk git diff --check` nach diesem Dokumentations-Amendment | bestanden. |

Dies sind lokale Kontrollergebnisse, keine Runtime-Evidence. Diese Erweiterung
behauptet keinen aktuellen exakten Parent-Commit, keinen Exact-Head-Hosted-CI-
Erfolg, kein SonarQube-Cloud-Ergebnis, keine Review-Entscheidung, keinen Merge
und kein Resulting-Master-Ergebnis.
