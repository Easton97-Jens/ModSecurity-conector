# Change Record: Authentizität strikter Runtime-Result-Dateien

**Sprache:** [English](CR-20260718-result-file-authenticity.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260718-result-file-authenticity` |
| Datum (UTC) | `2026-07-18` |
| Basis-Revision | `c8ca0d92b630c18232b881855c4f5d1482568ea6` |
| Finding | `FND-PARENT-0030` |
| Grenze | Nur strikter Parent-Report-Evidence-Checker, Full-Matrix-Receipts, Lifecycle-Producer, fokussierte Tests und Dokumentation; Framework und MRTS bleiben unverändert. |

## Motivation und Problemstellung

Das strikte Report-Evidence-Gate akzeptierte kritischen `missing`-Input-Status
und Listen fehlender Inputs. Es vertraute außerdem abgeleiteten
Report-Datensätzen, ohne den entkoppelten Full-Matrix-Command-Receipt, das
Raw-Matrix-Manifest, Job-Identitäten, kanonische Artefaktpfade oder
Result-Datei-Prüfsummen unabhängig zu validieren. Eine vorab platzierte
`PASS`-Result-Datei oder ein kopierter Job-Receipt konnte daher zu einem Report
beitragen, ohne dass ein strikter Source-of-Truth-Receipt geprüft wurde.

## Akzeptanzkriterien

- Der strikte Modus akzeptiert nur schema-genehmigte kritische
  Runtime-Input-Zustände: `complete` sowie die dokumentierte selbstgenerierte
  Ausnahme des Refresh-Manifests; `missing`, `empty`, `unknown`, `partial`,
  `stale`, `blocked`, `failed`, `interrupted`, `skipped` und erfundene positiv
  wirkende Werte werden abgelehnt.
- Ein verifizierter Full-Run besitzt eine gültige Run-ID, genau einen
  erforderlichen Full-Matrix-Producer-Command und exakt die zwölf
  Connector/CRS/MRTS-Job-Identitäten.
- Der strikte Consumer akzeptiert nur die vom Parent-Runner ausgegebenen
  terminalen Full-Matrix-Zustände `runtime_completed` und
  `runtime_completed_with_mismatches`, nie einen ähnlich benannten ad-hoc
  Zustand.
- Jeder Job-Receipt ist an ausgewählte Run-ID, Connector, CRS-Variante,
  MRTS-Variante, kanonischen Job-Root und strukturierten Completion-Status
  gebunden.
- Logs, Build-Manifeste, Zusammenfassungen und Result-JSONL-Dateien sind
  reguläre, kanonische Dateien mit passenden Receipt-Hashes; Leaf- und
  Zwischenpfad-Escapes oder Symlinks schlagen fail-closed fehl.
- Ein vom Receipt bereitgestellter Summary-Pfad kann nur eine der zwei vorab
  aufgebauten kanonischen Summary-Positionen auswählen; er wird nie zu einem
  Dateisystempfad für Lesen, `stat` oder Hash-Operationen.
- Kritische Input-Receipts werden vor dem Root-Containment-Vergleich kanonisch
  aufgelöst, sodass `BUILD_ROOT:../...`, `framework:../...` und unpräfixiertes
  `../...` keine externe reguläre Datei authentifizieren können, auch wenn ihr
  deklarierter SHA-256-Wert übereinstimmt.
- Das Raw-Full-Matrix-Manifest bewahrt Receipt-Identität und Hash-Felder und
  stimmt exakt mit den Job-Receipts überein.
- Eine gefälschte Result-Datei, fremde Run-ID, kopierter
  Connector/Profile-Receipt, fehlendes Raw-Manifest, unvollständiger Job und
  ungültiger kritischer Report-Status werden abgelehnt; ein vollständiger
  gültiger Kontrolllauf bleibt akzeptiert.

## Implementierungsentscheidung und Begründung

Der strikte Checker validiert nun entkoppelte Runtime-Receipts, bevor er
abgeleitete Report-Claims akzeptiert. Er akzeptiert nur ein positives,
Reportnamen-bewusstes Input-Status-Schema. Er verankert den Command-Receipt am
ausgewählten Runtime-Build-Root und prüft dann Run-ID, Profil, erforderlichen
Full-Matrix-Command, das Raw-12-Zellen-Matrixset, jede kanonische Job-Position
und die SHA-256-Werte jedes strukturierten Artefakts. Frei formatierte Pfade in
den Receipts können den Checker nicht umleiten: Sie müssen dem erwarteten
lexikalisch kanonischen Ort entsprechen und reguläre Dateien ohne
Symlink-Komponente unterhalb des Evidence-Roots sein.

Kritische Input-Receipts verwenden dieselbe fail-closed Grenze: Der Checker
löst den beanspruchten Pfad und den vertrauenswürdigen Root vor dem
Containment-Vergleich auf und weist danach weiterhin Leaf- und
Zwischen-Symlink-Komponenten zurück. Dadurch kann eine lexikalische
`..`-Komponente keinen vertrauenswürdigen Präfix bewahren, während die
Filesystem-Operation eine externe Datei erreicht.

Der Full-Matrix-Generator bewahrt beim Umschreiben des Raw-Manifests `job_id`,
`verified_run_id`, Status, Hashes, Inputs und Outputs, damit der strikte
Consumer Quell- und abgeleitete Datensätze vergleichen kann. Der
Lifecycle-Producer ergänzt strukturierten Result-JSONL-Pfad und -Hash im
Job-Receipt. Das Verified-Run-Manifest schließt seine eigenen überschriebenen
Dateien aus seiner Generated-Output-Hash-Liste aus, damit nach einer
Regenerierung kein selbstreferenzieller stale Hash entsteht.
Der Report-Refresh-Producer gibt jede aggregierte Input-Status-Sammlung als
typisierte Liste aus, damit ein zukünftiger gültiger Record dasselbe Schema
besitzt, das der strikte Consumer verlangt.

Das fokussierte Raw-Matrix-Fixture aktualisiert seinen JSONL-Record aus der
vollständigen In-Memory-Zwölf-Job-Sammlung, die es konstruiert hat; es liest
keinen serialisierten Fixture-Record erneut, bevor es das feste Fixture-Manifest
umschreibt. Dadurch bleiben die Direct-Summary- und Hash-Mismatch-Controls
erhalten, während die Fixture-Rewrite-Grenze explizit bleibt.

Für Summary-Artefakte leitet der Checker beide erlaubten Positionen aus dem
enumerierten Connector und dem kanonischen Job-Root ab, bevor er Receipt-Daten
auswertet. Das Receipt kann nur den direkten oder den kanonischen
`force-all`-Zweig auswählen; es kann den Pfad für Lesen, `stat` oder Hashen
nicht konstruieren. Damit bleiben die zwei unterstützten Producer-Layouts
erhalten, während der Datenfluss vom Receipt zum Dateisystempfad entfällt.

## Security-Auswirkung

Diese Härtung der Parent-Result-Datei-Authentizität und des Report-Consumers
verwandelt Report-Claims in eine geprüfte Kette vom kanonischen
Runtime-Command-Receipt über eine vollständige Raw-Job-Matrix bis zu
Job-lokalen Artefakten. Sie etabliert keinen Connector-Host, Prozess,
Request/Response-Traffic, CRS-, MRTS- oder Framework-Claim unabhängig.
Autoritative Host-Lifecycle- und Framework-Integrationsbindungen bleiben
eigene Grenzen und werden hier nicht geändert.

## Geänderte Dateien

- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `ci/evidence/reports/refresh-connector-reports.py`
- `ci/runtime/lifecycle/run-full-matrix-parallel.sh`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `tests/test_generated_report_evidence_integrity.py`
- dieses englische/deutsche Change-Record-Paar und seine README-Indexlinks

## Ausgeführte Befehle

Für die fokussierten Python-Befehle bezeichnet `PARENT_PYTHON` den explizit
ausgewählten Parent-Virtualenv-Interpreter unter
`/absolute/path/to/ModSecurity-conector/.venv/bin/python`; der isolierte
PR-Worktree erstellt oder besitzt keine zweite Virtualenv.

| Befehl | Ergebnis |
| --- | --- |
| Initialer fixture-first-`unittest`-Lauf vor der Strict-Chain-Implementierung | Erwartet fehlgeschlagen: Acht Fixtures erreichten die fehlende Strict-Chain-Kontrolle, und der kritische Missing-Input-Status wurde nicht abgelehnt. |
| Fixture-first-Kontrolle für kritische Input-Traversal vor kanonischem Containment | Erwartet fehlgeschlagen: `BUILD_ROOT:../...`, `framework:../...` und unpräfixiertes `../...` akzeptierten jeweils eine korrekt gehashte externe reguläre Datei ohne Strict-Check-Fehler. |
| `rtk proxy /usr/bin/env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 "$PARENT_PYTHON" -m unittest -v tests.test_generated_report_evidence_integrity` nach der Implementierung | Bestanden: 35 Tests decken gefälschten `PASS`-Result-Inhalt/Checksum-Mismatch, fehlendes Raw-Manifest, unvollständigen Receipt, fremde Run-ID, kopierten Connector/Profile-Receipt, Leaf- und Zwischenpfad-Escapes/Symlinks, kanonisiertes Critical-Input-Traversal, fehlenden/erfundenen/malformatierten kritischen Input-Status, Manifest- und Metadata-Input-Digest-Mismatch, direkte und `force-all`-Summary-Auswahl samt Hash-Ablehnung, Summary/JSONL-Fallback-Auswahl, typisierte Producer-Arrays, Raw-Manifest-Erhalt, Verhinderung der Selbstreferenz und einen gültigen Zwölf-Zellen-Kontrollfall ab. |
| `rtk sh -n ci/runtime/lifecycle/run-full-matrix-parallel.sh` | Bestanden. |
| In-Memory-`compile()`-Validierung der drei geänderten Python-Quellen | Bestanden ohne Versuch checkout-lokaler Bytecode-Schreibvorgänge. |
| Striktes `make verified-report-evidence-gate` gegen aufbewahrte Evidence | Erwarteter Fehler: Es lehnt kritische Missing-Input-Zustände und nichtkanonische/fehlende Command-Receipts ab. Die bestehende stale Cross-Evidence `FND-CROSS-0001` bleibt ein separater fail-closed Blocker. |
| Governance-only Generated-Report-Layout-Check gegen aufbewahrte Evidence | Bestanden: Der Governance-only-Modus ist keine Runtime-Evidence-Behauptung. |
| `rtk git diff --check` | Bestanden. |

## Runtime-Evidence

Nicht etabliert. Die fokussierten Fixtures erzeugen nur synthetische Dateien,
um Rejection- und Kontrollsemantik des Consumers zu validieren. Es wurde kein
echter Connector-Host, Prozess-Lifecycle, Request-Traffic, CRS-, MRTS- oder
Integrationsmodus-Run gestartet oder behauptet.

## Bekannte Einschränkungen

Diese isolierte Parent-Remediation kann Framework-eigene Producer- oder
Host-Lifecycle-Findings nicht schließen. Synthetic-Probe-Host-Bindung und
autoritative Phase-4-Integrationsbindung bleiben separat nachverfolgte
Framework-Handoffs. Die aufbewahrten Reports bleiben absichtlich strikte
Gate-Fehler, weil Cross-Runtime-Evidence stale ist.

## Verbleibende Risiken

Ein unabhängiges Review reproduzierte außerdem eine gekoppelte Umschreibung
einer Result-JSONL, ihres veränderbaren Job-Receipts und ihrer veränderbaren
Raw-Matrix-Zeile. Dies erfordert einen abgekoppelten vertrauenswürdigen
Producer-Aggregate-Receipt und ist separat als `FND-PARENT-0031` auf einem
eigenen gestapelten Parent-Branch nachverfolgt; dieser Change Record behauptet
nicht, diese Producer-Authentizitätsgrenze zu schließen.

## Nicht ausgeführte Prüfungen mit Begründung

Eine vollständige Connector-/Runtime-Matrix benötigt separat bereitgestellte
Runtime-Komponenten und den autoritativen Framework-Harness, die in diesem
isolierten Worktree nicht verfügbar sind. Dieses Fehlen autorisiert weder
einen synthetischen Erfolg noch einen Governance-only-Ersatz. Der
Source-Remediation-Head `03e5088d8202a4eb14d891b31d149aa2f6081289` wurde
gepusht. Der aktuelle Draft-PR-Head enthält diese Dokumentationskorrektur.
Vollständige Exact-Head-CI-, CodeQL-, SonarQube-Cloud- und Review-Verifikation
sind für den aktuellen exakten PR-Head erforderlich. Kein Merge ist erfolgt und
keine Prüfung darf umgangen werden.

## Finaler Diff- und Review-Status

Der ursprüngliche Source-Remediation-Head
`03e5088d8202a4eb14d891b31d149aa2f6081289` wurde gepusht. Der aktuelle
Draft-PR-Head enthält diese Record-Korrektur und bleibt
`remediation_required`, bis dieser exakte Head unabhängig verifiziert ist. Es
wird keine Runtime-Evidence oder Merge behauptet.
