# CR-20260820 — Full-Matrix-Evidence-Summary-Auswahl eingrenzen

**Sprache:** [English](CR-20260820-full-matrix-evidence-selector.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260820-full-matrix-evidence-selector` |
| Datum (UTC) | 2026-08-20 |
| Basis-Revision | `ab9cb2c276f159397ec2558b2d58cc260fd66ce2` |
| Finding | `FND-PARENT-0197` |
| Scope | Nur Parent-Evidence-Generator und Parent-Regressionstests |
| Framework-Grenze | Gitlink und verschachtelter `HEAD` bleiben `bd69ee96e0e7082317d4afe1232bee625665eb9a`; keine Framework-Source- oder Gitlink-Änderung |
| Delivery-Disposition | Ein späterer aktueller Benutzerauftrag autorisiert einen Parent-Draft-PR. Bei dieser Record-Revision sind Commit-, PR- und Hosted-Check-Fakten noch nicht beobachtet; der PR-Lifecycle/Task-Abschluss hält sie ohne selbstreferenzielle Commit-Schleife fest. |

## Motivation und Problemstellung

Der Full-Matrix-Completeness-Generator akzeptierte vor seinem späteren
strikten Report-Evidence-Gate einen rohen job-lokalen `summary.path`-Wert.
Dieser Wert konnte eine für den Prozess lesbare Datei außerhalb des festen
Job-Roots auswählen und Summary-Parsing sowie die `file_record()`-Metadaten- /
Hash-Verarbeitung erreichen. Das Problem ist eine Parent-Evidence-Integrity-
Grenze und keine Connector-Host-Runtime-Behauptung.

## Akzeptanzkriterien

- Ein externer `summary.path`-Selektor kann den ausgewählten Summary-Pfad
  nicht ändern.
- Ein Traversal-förmiger Selektor kann den ausgewählten Summary-Pfad nicht
  ändern.
- Eine direkte kanonische Summary bleibt auswählbar.
- Die zugehörige Generated-Report-Evidence-Integrity-Suite besteht.
- Die Reparatur bleibt Parent-only, startet keine Host-Runtime, ändert keine
  Framework-/MRTS-Source oder Gitlink und verwendet nur den separat
  autorisierten normalen Parent-Delivery-Pfad.

## Implementierungsentscheidung und Begründung

`summary_path()` liest die Legacy-Indirektion `summary.path` nicht mehr. Es
wählt nun nur bestehende feste Kandidaten unterhalb des Job-Roots und bewahrt
den direkten kanonischen `results/`-Fallback sowie den vorhandenen
`force-all/`-Kandidaten. Das Entfernen des unsicheren Selektors ist kleiner und
fail-closed gegenüber dem Versuch, einen beliebigen Pfad erst nach seinem Lesen
rückwirkend zu validieren.

Die Regressionssuite ergänzt den ursprünglichen externen Selektorfall, eine
Traversal-Variante und einen legitimen Direct-Canonical-Summary-Control. Kein
generiertes Artefakt wurde direkt bearbeitet.

## Security-Auswirkung

`FND-PARENT-0197` ist ein Parent-P2-`security_validated`-Finding mittlerer
Schwere und bestätigter Konfidenz. Die primären CWEs sind `CWE-73` (externe
Kontrolle eines Dateinamens oder Pfads) und `CWE-22` (Traversal-förmige
Variante). Ein Job-Evidence-Produzent, der `job_root/summary.path` schreiben
kann, konnte zuvor vor dem späteren Gate den lokalen Generator zum Lesen und
Hashen einer für den Prozess lesbaren beliebigen Datei veranlassen. Die
zurückgehaltene Reproduktion verwendete nur eine leere gutartige JSON-Fixture;
kein Secret, Request, Response, Cookie, Authorization-Wert oder rohes Log wurde
gelesen oder aufbewahrt.

## Geänderte Dateien

- `ci/evidence/reports/generate-full-matrix-job-completeness.py`
- `tests/test_generated_report_evidence_integrity.py`
- dieses englisch/deutsche Change-Record-Paar
- die gekoppelten Change-Record-Archivindizes

## Ausgeführte Befehle

Alle Befehle liefen lokal unter RTK-Vermittlung. Private
Temporary-Directory-Pfade sind absichtlich als `<private-task-root>` dargestellt.

- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-task-root>/test .venv/bin/python -m unittest -v tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_rejects_external_override tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_rejects_traversal_override tests.test_generated_report_evidence_integrity.GeneratedReportEvidenceIntegrityTests.test_summary_selector_keeps_canonical_direct_summary` — Exit `0`; ursprünglicher externer Selektor abgelehnt, Traversal-Variante abgelehnt, direkter kanonischer Control ausgewählt.
- `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<private-task-root>/test .venv/bin/python -m unittest -q tests.test_generated_report_evidence_integrity` — Exit `0`; `Ran 82 tests in 54.396s`, `OK`, `check-generated-report-layout: PASS`.
- `make check-common-security-contract check-common-flow-integrity check-directive-parity check-bilingual-docs` — Exit `0`; die relevanten statischen Parent-Contracts des Audits bestanden.
- `make check-common-memory-safety check-common-http-header-fuzz` mit einem registrierten privaten `BUILD_ROOT` — Exit `0`; begrenzte Memory-Safety- und 15-Sekunden-Header-Fuzz-Checks bestanden.
- `git diff --check` — Exit `0` vor der finalen Dokumentationsvalidierung; kein Whitespace-Fehler beobachtet.
- Fokussierte `check_change_record_pair`- plus `structural_pair_errors`-Prüfung aus `ci/checks/documentation/check-bilingual-docs.py` — Exit `0`; das neue Paar besitzt erforderliche Überschriften, übereinstimmende Identitätsfelder, Sprachumschalter und strukturelle Parität.
- `make check-bilingual-docs` wurde nach Ergänzung des neuen Paars gestartet, gab aber keine Diagnose aus und wurde nach ungefähr fünf Minuten mit Exit `130` unterbrochen; es zählt nicht als bestandene Prüfung.
- `make check-bilingual-docs` im isolierten Delivery-Worktree — Exit `2`;
  repository-weite bestehende Dokumentationslinks benötigen das nicht
  initialisierte Framework-Submodule. Es wurde kein Framework initialisiert,
  weil `SUBMODULE_SCOPE=METADATA_ONLY` gilt; dies ist eine blockierte breite
  Dokumentationsvoraussetzung und kein Change-Record-Paar-Fehler.

## Runtime-Evidence

Es gibt keine Host-Runtime-Evidence. `RUNTIME_AUTHORIZED=false` untersagt den
Start von Apache-, NGINX-, HAProxy-, Envoy-, Traefik- oder lighttpd-Hosts. Der
lokale Nachweis beschränkt sich auf Source-Verhalten und die zugehörige Python-
Testsuite.

Payload-sichere Receipts werden im externen Run
`20260820T000000Z-defensive-security-audit-770d35c` als
`evidence/evidence-selector-baseline.md` (SHA-256
`26e708ad3a51e7b42401fc4f615df40bd3efa2b25eab11c9b2a253c255a11d1c`) und
`evidence/evidence-selector-remediation.md` (SHA-256
`751cf0616d6dc1e4ac9ab78fd16522694b75e9e8add04adb4b7f813ea528b953`)
aufbewahrt.

## Nicht ausgeführte Prüfungen mit Begründung

- `make check-doc-links` wurde nicht ausgeführt, weil es `check-framework` und
  einen Framework-Dokumentationsprüfer aufruft; `SUBMODULE_SCOPE=METADATA_ONLY`
  schließt Framework-Inhalt aus diesem Audit aus.
- Der vollständige Post-Change-Validator `make check-bilingual-docs` ist kein
  bestandenes Ergebnis: Der ursprüngliche Lauf wurde ohne Fortschritt oder
  Diagnoseausgabe unterbrochen, und der frische isolierte Worktree-Lauf gab
  wegen für bestehende Links fehlendem Framework-Inhalt Exit `2` zurück. Die
  fokussierte Change-Record-Contract-/Paritätsprüfung oben ist die stärkste
  abgeschlossene Alternative.
- `make check-ci-security-contract` wurde im ursprünglichen Audit nicht
  ausgeführt: Sein Testset übt temporäres Git-Schreibverhalten außerhalb der
  damaligen Autorisierung aus. Die spätere normale Delivery-Autorisierung macht
  es nicht rückwirkend zu einer Selector-Regression; es bleibt `not_run`.
- Vollständige Connector-Lifecycle-, Build-, Config-Load- und Host-Smoke-
  Checks wurden wegen `RUNTIME_AUTHORIZED=false` nicht ausgeführt.
- Netzwerkgebundene Scans und Downloads wurden unter der ursprünglichen
  `NETWORK_AUTHORIZED=false`-Audit-Grenze nicht ausgeführt. Die spätere
  Delivery-Erweiterung autorisiert nur normale GitHub-Delivery; Hosted-PR-Checks
  stehen zur tatsächlichen Beobachtung aus und werden hier nicht behauptet.

## Bekannte Einschränkungen

Der Audit ist source-basiert und beweist nicht jeden Report-Consumer,
Deployment-Pfad oder Connector-Host-Verhalten. Der aktuell initialisierte
Framework-Checkout besitzt parallele dirty Änderungen außerhalb dieser Task;
nur Gitlink und `HEAD` wurden geprüft, und kein Framework-Inhalt wurde hier
geändert oder attribuiert.

## Verbleibende Risiken

Die Korrektur grenzt nur diesen Legacy-Summary-Selektor ein. Andere
Report-Eingaben, Host-Runtime-Verhalten, Hosted-Workflow-Semantik und
netzwerkgebundene Scanner-Ergebnisse liegen außerhalb der autorisierten
Evidence. `FND-PARENT-0197` ist lokal `fixed`, aber weder Delivery-verifiziert
noch geschlossen.

## Finaler Diff- und Review-Status

Der finale Review bei dieser Record-Revision beschränkt sich auf den
beobachteten lokalen Diff, die Source-to-Sink-Reproduktion, fokussierte
Regressionen, die 82-Test-zugehörige Suite, statische Parent-Contracts,
Evidence-Prüfsummen und den fokussierten Change-Record-Dokumentationsvertrag.
Der separat autorisierte Draft-PR-Lifecycle hält Branch-, Commit-, PR-Head-,
Hosted-Check- und Review-Fakten erst nach ihrer Beobachtung fest. Es werden
weder Merge, Resulting-Master-Validierung, Framework-Änderung, MRTS-Änderung
noch Gitlink-Update behauptet.
