# Finding: Aggregate-Receipt-Traversal besitzt eine Intermediate-Symlink-TOCTOU-Race

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0037` |
| Status | `closed` (archiviert) |
| Priorität / Schweregrad | `P1 / high` |
| Owner | Parent |
| Root-Control-Grenze | path confinement; producer authenticity; result-file authenticity |
| Release-Blocker | no |

## Zusammenfassung

Der `FND-PARENT-0031`-Aggregate-Receipt-Helper führt einen lexikalischen
`lstat`-Pfadlauf aus und öffnet später den vollständigen Pfadnamen.
`O_NOFOLLOW` schützt nur die letzte Komponente, sodass ein konkurrierendes
Same-UID-Matrix-Child ein zuvor geprüftes Zwischenverzeichnis vor dem späteren
Open durch einen Symlink ersetzen kann.

## Evidence und Reproduktion

Die aufbewahrte Source-to-Sink-Review benennt die betroffenen Funktionen und
den genauen lstat-to-open-Flow. Die Fixture-first-Regression nutzt eine
einmalige `os.open`-Seam: Nach der lexikalischen Prüfung ersetzt sie
`BUILD_ROOT/inside` durch einen Symlink auf ein externes Verzeichnis. Vor der
descriptor-relativen Korrektur kann der Helper das externe reguläre Leaf lesen,
während er einen lexikalischen In-Root-Pfad behält. Eine parallele Writer-Seam
tauscht `verified-runs` vor der Receipt-Publikation und beweist nach dem Fix,
dass kein externer Receipt erzeugt wird.

## Root Cause

Der Helper prüft eine veränderbare Pfadnamenhierarchie und löst sie später
erneut auf. Leaf-only `O_NOFOLLOW` kann die zuvor geprüften
Zwischenkomponenten nicht Teil der Trust Boundary der späteren Operation machen.

## Gelieferte Remediation und aktuelle PR-Evidence

PR-#59-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` ersetzt die erneute
Pfadnamenauflösung bei Aggregate-Receipt-Lese- und Publikationsvorgängen durch
descriptor-relative Traversal ab einem gepinnten `BUILD_ROOT`-Descriptor.
Zwischenkomponenten verwenden `O_DIRECTORY|O_NOFOLLOW`; Receipt-Erstellung ist
exklusiv und descriptor-relativ mit `fchmod` und `fsync`. Der Runner nutzt den
descriptor-abgeleiteten Receipt-Record statt einen veränderbaren Pfadnamen
erneut zu hashen. Der finale Nachzug versiegelt Receipts mit Owner-read-only-
Modus `0400`. Die deterministischen Intermediate-Read- und verified-runs-
Publikations-Swaps scheitern fail closed. Aktuelle nicht übersprungene CI-,
CodeQL-, Sonar-Quality-Gate- und Null-Review/Thread-Gates bestanden vor dem
geschützten Squash-Merge auf Parent-master
`5a22cbf5206dbc2b7f53a9f961d72e37d567e188`. Die exakte Resulting-Master-
Reproduktion bestand 57/57 Evidence-Integrity-Controls, 11/11 Bilingual-
Controls, Shell-Syntax und Diff-Hygiene. Dieses Finding ist verified, nicht
closed.

## Akzeptanzkriterien

- Ein deterministischer Zwischenverzeichnis-Read-Swap scheitert fail-closed und
  hasht nie externe Bytes.
- Ein deterministischer `verified-runs`-Publikations-Swap scheitert fail-closed
  und erzeugt keinen Receipt außerhalb von `BUILD_ROOT`.
- Die gültige In-Root-Read- und vollständige Zwölf-Zellen-Aggregate-Receipt-
  Kontrolle bleiben akzeptiert.
- Der nutzerautorisierte kombinierte Parent-Draft-PR bewahrt getrennte
  Finding-Traceability; Framework/MRTS-Änderung oder Merge erfolgen nicht.

## Scope und Abhängigkeit

Dies ist Parent-owned und von `FND-PARENT-0026` und `FND-PARENT-0032`
verschieden: jene Findings steuern Caller-Roots und Runtime-Root-/Run-ID-
Autorität, während dieses einzelne Receipt-Helper-Operationen nach der
Root-/Pfadprüfung schützt. Es hängt als Implementierungsbasis von
`FND-PARENT-0031` ab. Der aktuelle Nutzer erlaubt ihren kombinierten/
gestapelten #59-Kandidaten, aber die Findings bleiben unabhängig verfolgt,
verified und nicht geschlossen.

## Verbleibendes Risiko

Die Receipt-Kette ist keine Signatur-, ACL-, Prozessidentitäts-, UID-Isolations-
oder External-Attestation-Grenze. Modus `0400` beschränkt nur Group-/Other-
Zugriff; ein Akteur mit beliebigem Same-UID-Schreibzugriff auf den Parent-
Evidence-Namespace bleibt außerhalb dieses lokalen Filesystem-Trust-Modells. Es
wird kein Risiko akzeptiert. Das exakte Source-Head-Gate und die
Original-Reproduktion auf Resulting-Master sind verified. `FND-CROSS-0001`
blockiert reale aktuelle Runtime-Evidence getrennt. `FND-SONAR-0001` lässt das
globale Master-Quality-Gate getrennt fehlschlagen; es wird weder akzeptiert noch
diesem Finding zugeschrieben.

## Aktuelle aufbewahrte Post-Merge-Evidence

`pr59-5a22cbf-postmerge-validation.json` in Run
`20260720T141403Z-pr55-pr59-master-integration-8a0b8640`, SHA-256
`7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`, erfasst
den exakten Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`, den
geschützten Squash-Master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, aktuelle
Gates und die Post-Merge-Original-Reproduktion sowie legitimen Kontrollen.

## Historie

- `2026-07-18T15:45:00Z` — durch aufbewahrte Parent-Source-to-Sink-Review
  validiert; separate Root Cause und Delivery-Branch zugeteilt.
- `2026-07-20T09:57:03Z` — fixed_on_current_pr_head: #59-Head
  `d4f88b886dac6fd5f483940015d6310bc239f814` liefert descriptor-relative
  Traversal/Publikation und den `0400`-Versiegelungsnachzug. Er bleibt Draft
  hinter aktuellem Master, daher sind Exact-Head-Revalidation, autorisierter
  Merge und Post-Merge-Original-Reproduktion weiter erforderlich.
- `2026-07-20T15:13:08+00:00` — verified_on_resulting_parent_master: aktuelle
  Source-Head-Gates bestanden und #59 wurde geschützt von
  `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` nach
  `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` squash-gemergt. Die aufbewahrte
  57/57-Original-Reproduktion/legitime-Control-Suite enthält Intermediate-
  Read- und Publikations-Swaps; 11/11 Bilingual-, Shell-Syntax- und Diff-
  Controls bestanden ebenfalls. `FND-SONAR-0001` bleibt unabhängig und nicht
  akzeptiert; dieses Finding ist nach Current-Master-Validierung durch den aktuellen Nutzer closed.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_unchanged_path_validation` — betroffene Pfade sind vom verifizierten Master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` bis `6ca7e1536ce7e93da68099db9c586b88852ff13e` unverändert; `tests.test_generated_report_evidence_integrity` bestand in der 144-Test-Control-Suite.
