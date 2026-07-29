# Change Record: Parent-CI-Best-Effort-Evidence-Reader-Deduplizierung für SonarQube Cloud

**Sprache:** [English](CR-20260729-sonar-ci-best-effort-evidence-readers.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260729-sonar-ci-best-effort-evidence-readers` |
| Datum (UTC) | `2026-07-29` |
| Basis-Revision | `dbbc9c6aa2bca22fcd0385fa76b878873ccab2cc` |
| Bewertete Source-Revision | `b9008be7fc416d5e58a2305ab21dfacc4c7cef5f` |
| Grenze | Ausschließlich Parent `ci/lib/best_effort_evidence_readers.py`, seine vier direkten Parent-`ci/`-Consumer, dieses englische/deutsche Change-Record-Paar und die gepaarten Indizes. Keine `.github/`, keine Test-Source, kein Framework, kein MRTS, kein Gitlink, keine Scanner-Konfiguration, kein Quality Gate, keine Exclusion, keine Suppression und keine Default-Branch-Änderung sind enthalten. |
| SonarQube-Cloud-Verknüpfung | Zielt auf den führenden aktuellen Parent-`ci/`-Duplikat-Reader-Cluster; keine Regel, kein Quality Gate, keine Exclusion und keine Suppression werden geändert. |

## Motivation und Problemstellung

Vier CI-Evidence-/Lifecycle-Skripte enthielten byteidentische Best-Effort-
JSON-Object- und JSONL-Object-Reader. Der führende aktuelle `ci/`-
Duplikatcluster durfte daher nur reduziert werden, wenn das Parsing nicht
autoritativ bleibt und alle aufruferspezifischen Pfad-, Receipt- und
Statuskontrollen unverändert erhalten bleiben.

## Implementierungsentscheidung und Begründung

`ci/lib/best_effort_evidence_readers.py` besitzt jetzt genau zwei Helfer:
`read_json_object()` und `read_jsonl_objects()`. Die vier Aufrufer importieren
sie unter ihren vorhandenen Namen `read_json` und `read_jsonl`. Die Helfer
bewahren das frühere Verhalten exakt:

- JSON wird als UTF-8 dekodiert und liefert nur ein Object; unlesbare,
  fehlerhafte oder nicht-objektförmige Eingabe liefert `{}`.
- JSONL verwendet UTF-8-Ersatzdekodierung; leere, fehlerhafte und nicht-
  objektförmige Zeilen werden übersprungen, während gültige Object-Zeilen ihre
  Quellreihenfolge bewahren.

Die Änderung zentralisiert absichtlich weder Pfadauflösung noch Root-
Registrierung, Symlink-Policy, Receipt-Validierung, Raw-Line-Counting,
Statusklassifikation, Output-Writes oder Runtime-Command-Construction.
Insbesondere sind `report_path_safety` und `verified_full_matrix_receipt`
strengere Kontrollen und kein Ersatz für diesen Kompatibilitätshelfer.

## Akzeptanzkriterien

- Die vier früheren Reader bewahren identisches JSON/JSONL-Rückgabeverhalten.
- Der Raw-Nonblank-Line-Count des Lifecycle-Runners bleibt unabhängig von
  geparsten Object-Zeilen.
- Fehlende oder fehlerhafte Evidence bleibt gemäß jedem unveränderten Aufrufer
  unvollständig, partiell, `UNKNOWN` oder anderweitig nicht autoritativ; sie
  kann keinen erfolgreichen Full-Matrix- oder Merge-Readiness-Claim erzeugen.
- Keine Pfad-Root-, Receipt-, Write-, Subprocess-, Token-, Workflow-,
  Framework-, MRTS-, Gitlink-, SonarQube-Cloud-Setting- oder Test-Source-
  Verhaltensänderung.
- Ein zukünftiger exakter PR-Head muss null neue SonarQube-Cloud-Issues und
  `0.0%` New-Code-Duplizierung ohne Abschwächung einer Kontrolle erhalten.

## Geänderte Dateien

- `ci/lib/best_effort_evidence_readers.py`
- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `ci/evidence/reports/generate-nginx-mrts-http500-cluster-analysis.py`
- `ci/evidence/reports/generate-verified-runtime-mismatch-analysis.py`
- `ci/runtime/lifecycle/run-verified-report-run.py`
- `reports/audits/change-records/CR-20260729-sonar-ci-best-effort-evidence-readers.md`
- `reports/audits/change-records/CR-20260729-sonar-ci-best-effort-evidence-readers.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Selected-File-`py_compile` mit task-eigenem Bytecode-Cache | bestanden. |
| Direkter externer Master-Parity-Harness | bestanden: gültiges, fehlendes, fehlerhaftes, skalares/listenförmiges JSON; gemischtes JSONL; Lifecycle-Raw-Line-Count; und Full-Matrix-JSONL-Fallback. |
| Vier fokussierte vorhandene Testmodule | 107 Tests bestanden; ein Snapshot-Integrationstest ist `blocked_external_dependency`, weil dem isolierten Parent-Worktree absichtlich Framework `ci/lib/common.sh` fehlt. Die anderen acht Snapshot-Contract-Tests bestanden separat. |
| `git diff --check` | bestanden. |
| Formaler Codex-Security-Diff-Scan der fünf exakten Source-Dateien | bestanden: alle fünf Worklist-Zeilen erhielten Full-File-Receipts; keine reportierbare Finding. |

## Security-Auswirkung und Restrisiko

Der geänderte Code verarbeitet mutable Runtime-/Report-Evidence, die
generierte Readiness-Outputs beeinflussen kann. Seine sicherheitsrelevante
Invariante lautet, dass permissives Parsing allein keinen Pfad, kein Receipt
und keinen erfolgreichen Runtime-Zustand als vertrauenswürdig etablieren darf.
Der Helfer bleibt absichtlich nicht autoritativ; jeder Aufrufer behält die
früheren Run-ID-, Runtime-Root-, Output-Root-, Fixed-Matrix-, Strict-
Aggregate-Receipt- und Fail-Closed-Statuskontrollen.

Der Security-Scan fand keinen diff-induzierten Candidate. Bestehende
permissive Evidence-Reader und aufruferspezifisches Pfadverhalten werden durch
diese Deduplizierung nicht erweitert. Dieses Record beansprucht nicht, eine
unverbundene Security-Observation zu beheben, zu unterdrücken oder zu
schließen.

## Runtime-Evidence

Es wird keine Connector-Runtime, keine netzwerkgestützte Vorbereitung und
keine vollständige Host-Matrix beansprucht. Der direkte Parity-Harness und die
fokussierten Import-/Status-Tests validieren den geänderten Reader-Contract,
ohne generierte Report-Evidence zu schreiben. Die Full-Runtime-Matrix liegt
außerhalb dieser engen Duplikat-Entfernung.

## Bekannte Einschränkungen

- Die vollständige Connector-Runtime-Matrix benötigt Framework-Inhalt und
  generierte Evidence; sie wurde für diesen Source-only-Kompatibilitäts-
  Refaktor nicht ausgeführt.
- Ein vorhandener Snapshot-Integrationstest kann im absichtlich nicht
  befüllten Task-Worktree nicht laufen, weil Framework `ci/lib/common.sh`
  fehlt. Das ist eine externe Abhängigkeitsbeschränkung, kein geändertes
  Testergebnis.
- Der exakte Hosted-PR-Head bleibt die erforderliche Evidence für die
  ausgewählten SonarQube-Cloud-Metriken und GitHub-Checks.

## Verbleibende Risiken

Der Source-Refaktor benötigt weiterhin eine exakte Hosted-PR-Head-Analyse, um
zu belegen, dass er kein neues SonarQube-Cloud-Issue und keine New-Code-
Duplizierung erzeugt. Der fehlende Framework-Inhalt verhindert außerdem den
einen vorhandenen Snapshot-Integrationstest und eine vollständige Runtime-
Matrix in diesem isolierten Worktree; keine dieser Einschränkungen wird als
bestandenes Ergebnis verborgen.

## Nicht ausgeführte Prüfungen mit Begründung

- Keine `.github/`, kein Framework, kein MRTS, kein Gitlink und keine
  unverbundene Parent-Source wurden geändert oder ausgeführt, weil der Nutzer
  die Remediation auf Parent `ci/` und `scripts/` eingeschränkt hat.
- Kein Package-Install, kein netzwerkgestützter Connector-Build und keine
  Runtime-Matrix: Die Source-Änderung ist eine verhaltensbewahrende Evidence-
  Parser-Extraktion, und die direkten Contract-Kontrollen sind die engsten
  gültigen Checks.
- Hosted-SonarQube-Cloud-, GitHub-Actions-, Review- und Merge-Evidence werden
  nicht lokal hergeleitet und benötigen den späteren exakten PR-Head.

## Finaler Diff- und Review-Status

Der Source-Branch wurde gepusht und [Draft-PR #170](https://github.com/Easton97-Jens/ModSecurity-conector/pull/170)
gegen `master` vom initialen Head `9963a8dba82d11ca29c5f79ff59eb243b806f610`
geöffnet. Dieses Traceability-Follow-up erzeugt einen späteren exakten PR-Head;
es beansprucht daher nicht, dass Checks oder SonarQube-Cloud-Ergebnisse des
initialen Heads für diesen späteren Head gelten. Kein Hosted-Check, Review,
keine SonarQube-Cloud-Analyse, Freigabe oder Merge wird beansprucht, bevor sie
am späteren exakten PR-Head beobachtet wurden. Der formale Source-Security-
Report bleibt außerhalb des Repositorys als task-eigene Scan-Evidence erhalten.
