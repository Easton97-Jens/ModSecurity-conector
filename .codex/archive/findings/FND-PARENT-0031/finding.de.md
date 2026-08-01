# Finding: Strikte Runtime-Evidence besitzt keinen abgekoppelten Producer-Receipt für Full-Matrix-Artefakte

**Sprache:** [English](finding.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| ID | `FND-PARENT-0031` |
| Status | `closed` (archiviert) |
| Priorität / Schwere | `P1 / high` |
| Owner | Parent |
| Root-Control-Grenze | Producer-Authentizität; Result-Datei-Authentizität; Run-Identität |
| Release-Blocker | nein |

## Zusammenfassung

Der strikte Consumer berechnet einen Leaf-Result-Hash neu, vertraut aber der
veränderbaren `job.json` und der Raw-Matrix-Zeile, die denselben Hash
deklarieren. Ein gefälschtes `PASS`-Result mit synchronisierten veränderbaren
Receipt-Feldern besteht daher die aktuelle strikte Kette.

## Evidence und Reproduktion

In einer vollständigen temporären Parent-Fixture mit zwölf Zellen wurde eine
Result-JSONL durch gefälschten `PASS`-Inhalt ersetzt und ihr Hash in der
passenden `job.json` sowie Raw-Matrix-Zeile aktualisiert. Der strikte
Artifact-Chain-Verifier lieferte keine Fehler. Das aufzubewahrende
Reproduktionsziel ist in `finding.json` dokumentiert und wird vor Delivery
versiegelt.

## Root Cause

`verified-commands.json` beweist, dass der Full-Matrix-Command abgeschlossen
wurde, bindet aber weder Raw-Matrix noch jeden Job-Receipt oder jedes
erforderliche Leaf-Artefakt. Der strikte Checker vergleicht veränderbare
Dokumente, die gemeinsam umgeschrieben werden können.

## Gelieferte Remediation und aktuelle PR-Evidence

PR-#59-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` enthält nun den
kanonischen per-Run-Aggregate-Receipt
unter `verified-runs/<run-id>/` aus, bindet ihn in das Verified-Run-Manifest
und validiert ihn vor Annahme von Raw-/Job-/Leaf-Records. Er deckt gekoppelte
und alternative Umschreibungen, fremde Generator-Run-IDs, einen legitimen
Resume-Lauf und eine gültige Zwölf-Zellen-Kontrolle ab. `FND-PARENT-0037`
härtet die Intermediate-Path-Race des Helpers im selben nutzerautorisierten
kombinierten PR getrennt. Aktuelle nicht übersprungene CI-, CodeQL-, Sonar-
Quality-Gate- und Null-Review/Thread-Gates bestanden vor dem geschützten
Squash-Merge auf Parent-master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`.
Die exakte Resulting-Master-Reproduktion bestand 57/57 Evidence-Integrity-
Controls, 11/11 Bilingual-Controls, Shell-Syntax und Diff-Hygiene. Dieses
Finding ist verified, nicht closed.

## Akzeptanzkriterien

- Eine gekoppelte Result-/Job-/Raw-Receipt-Fälschung wird abgelehnt.
- Der abgekoppelte Aggregate-Receipt ist regulär, schema-valide und an den
  aktuellen Run gebunden; descriptor-relative Path-Confinement verfolgt
  `FND-PARENT-0037`.
- Ein gültiger vollständiger Kontrolllauf mit zwölf Zellen wird akzeptiert.
- Der nutzerautorisierte kombinierte Parent-Draft-PR bewahrt getrennte
  Finding-Traceability; keine Framework-/MRTS-Änderung und kein Merge erfolgen.

## Umfang und Abhängigkeit

Dies ist Parent-eigen und kein Duplikat von `FND-PARENT-0030`: Dieser Befund
etabliert strikte Consumer-Pfad-/Status-/Hash-Prüfungen, während dieser Befund
den separaten Producer-Authentizitätsanker etabliert. Der aktuelle Nutzer
erlaubt einen kombinierten/gestapelten #59-Delivery-Kandidaten, aber
`FND-PARENT-0030`, `FND-PARENT-0031` und `FND-PARENT-0037` bleiben unabhängig
verfolgt, verified und nicht geschlossen.

## Restrisiko

Die Receipt-Kette ist keine Signatur-, ACL-, Prozessidentitäts-, UID-Isolations-
oder External-Attestation-Grenze. Modus `0400` beschränkt nur Group-/Other-
Zugriff; ein Akteur mit beliebigem Same-UID-Schreibzugriff auf den Parent-
Evidence-Namespace bleibt außerhalb dieses lokalen Filesystem-Trust-Modells. Es
wird kein Risiko akzeptiert. Das exakte Source-Head-Gate und die
Original-Reproduktion auf Resulting-Master sind verified. Reale aktuelle
Runtime-Evidence bleibt durch `FND-CROSS-0001` getrennt blockiert.
`FND-SONAR-0001` lässt das globale Master-Quality-Gate getrennt fehlschlagen;
es wird weder akzeptiert noch diesem Finding zugeschrieben.

## Aktuelle aufbewahrte Post-Merge-Evidence

`pr59-5a22cbf-postmerge-validation.json` in Run
`20260720T141403Z-pr55-pr59-master-integration-8a0b8640`, SHA-256
`7749e6c6fd1ab198b54eb9704221d30aa150954db6130bec0317801a8afddc51`, erfasst
den exakten Source-Head `b9b22cc36958ba506278f3aa3fbc1d383ea6a151`, den
geschützten Squash-Master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188`, aktuelle
Gates und die Post-Merge-Original-Reproduktion sowie legitimen Kontrollen.

## Historie

- `2026-07-20T09:57:03Z` — fixed_on_current_pr_head: #59-Head
  `d4f88b886dac6fd5f483940015d6310bc239f814` enthält den abgekoppelten Receipt
  und die zugehörige descriptor-relative Korrektur. Er ist weiterhin Draft und
  hinter aktuellem Master, daher bleibt das Finding release-blocking bis zur
  normalen Synchronisierung, Exact-Head-Revalidation, autorisiertem Merge und
  Post-Merge-Reproduktion.
- `2026-07-20T15:13:08+00:00` — verified_on_resulting_parent_master: aktuelle
  Source-Head-Gates bestanden und #59 wurde geschützt von
  `b9b22cc36958ba506278f3aa3fbc1d383ea6a151` nach
  `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` squash-gemergt. Die aufbewahrte
  57/57-Original-Reproduktion/legitime-Control-Suite enthält gekoppelte
  veränderbare Result-/Job-/Raw- und Alternativ-Rewrite-Ablehnungen; 11/11
  Bilingual-, Shell-Syntax- und Diff-Controls bestanden ebenfalls.
  `FND-SONAR-0001` bleibt unabhängig und nicht akzeptiert; dieses Finding ist
  closed durch den aktuellen Nutzer nach Current-Master-Validierung.

- `2026-07-26T14:09:02Z`: `closed_by_current_user_after_current_master_unchanged_path_validation` — betroffene Pfade sind vom verifizierten Master `5a22cbf5206dbc2b7f53a9f961d72e37d567e188` bis `6ca7e1536ce7e93da68099db9c586b88852ff13e` unverändert; `tests.test_generated_report_evidence_integrity` bestand in der 144-Test-Control-Suite.
