# Change Record: Parent-Zerlegung des Generated-Report-Layouts für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-generated-report-layout-decomposition.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-generated-report-layout-decomposition |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Receipts `AZ7K5CRYixFPtcnbna1Q`, `AZ7POyU1BW70q7L2nMJQ` und `AZ7POyU1BW70q7L2nMJR`; außerdem `python:S3776`-Receipts `AZ7K5CRYixFPtcnbna1U`, `AZ7K5CRYixFPtcnbna1V`, `AZ7K5CRYixFPtcnbna1X`, `AZ7K5CRYixFPtcnbna1Y` und `AZ7Tenm9HrNUCHtbhYSD`; sowie der Exact-Draft-PR-#149-Head-Receipt `AZ-mYAcnCVtpA6IZuHRU` für den wiederholten `.json`-Suffix. |
| Grenze | Ausschließlich Parent-Report-Layout-Checker und dessen bestehende Integritätstests. Framework wurde read-only am Parent-gepinnten `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` geprüft; MRTS, Gitlinks, generierte Reports, Runtime-Evidence, Workflows, Scanner-Policy, Suppressions und der externe SonarQube-Cloud-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Der ausgewählte Checker enthält wiederholte unveränderliche Literale und fünf
große Orchestratoren, die SonarQube Cloud als Maintainability Debt meldet. Er
ist zugleich ein fail-closed Consumer von Generated-Report- und
Runtime-Evidence. Der Refactor darf deshalb nur strukturelle Duplikate und
Komplexität entfernen, ohne Trust-, Hash-, Receipt-, Revisions-, Symlink- oder
Strict-Evidence-Controls zu lockern.

Die erste Exact-Draft-PR-Analyse fand anschließend einen neuen task-eigenen
`.json`-Literal-Receipt, der durch die strukturelle Extraktion sichtbar wurde.
Der normale Follow-up muss diese Literalduplizierung entfernen, ohne die
Suffix-Tests zu verändern.

## Akzeptanzkriterien

- Ausschließlich die vier wiederholten `python:S1192`-Literalfamilien durch
  unveränderliche Modulkonstanten ersetzen und ihre exakten Werte und Gates
  bewahren.
- Die fünf ausgewählten `python:S3776`-Orchestrierungspfade in schmale private
  Helper aufteilen, ohne Fehlertexte, Reihenfolge, Early Returns oder
  Control-Prädikate zu verändern.
- Critical-Input-Validierung, Aggregate-Receipt- und Revisionsbindung,
  descriptor-bound Reads, Stability-Revalidierung, Strict-Evidence-Semantik
  und die Unterscheidung `--governance-only` bewahren.
- Die fokussierte Evidence-Integrity-Suite und den Governance-Check bestehen
  lassen; Runtime-Evidence niemals nur für einen grünen Strict-Gate neu
  generieren.
- Den Kandidaten Parent-only halten und jede gehostete Sonar-Schlussfolgerung
  bis zur Beobachtung eines exakten Draft-PR-Heads aufschieben.

## Implementierungsentscheidung und Begründung

Die Änderung führt unveränderliche Konstanten für den In-Progress-
System-Proof-Environment-Key, seinen exakten Wert und den Generated-Report-
Dateinamenpräfix ein. Sie extrahiert reine Helper für System-Proof-
Markdown/JSON-Inhalte, Legacy-Reference-Candidate-Collection, HTTPS-
Repository-URL-Policy-Scanning, Registry-Output-Checks sowie vollständige und
unvollständige Runtime-Diagnostics.

Der Follow-up gibt dem identischen JSON-Dateinamen-Suffix einen einzigen
unveränderlichen Owner `JSON_FILE_SUFFIX` und verwendet ihn erneut in der
URL-Scan-Suffix-Allowlist, dem Generated-Report-JSON-Dispatch und der
JSON-Metadata-Path-Validation. Er bewahrt den Literalwert `.json` und alle
drei Prädikate exakt.

Die sensitiven Primitiven bleiben in ihren ursprünglichen Control-Pfaden:
`is_within`, `has_symlink_component`, `is_regular_file`,
`validate_critical_input_record`, Aggregate-Receipt-/Command-Receipt-Checks,
Revisionsbindung und Aggregate-Receipt-Stability-Validation. Der Refactor fügt
keinen Bypass, keinen Report-Refresh, keine Scanner-Suppression und keine
Änderung an einem Connector- oder Runtime-Vertrag hinzu.

## Geänderte Dateien

- ci/checks/documentation/check-generated-report-layout.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

- `PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -q tests.test_generated_report_evidence_integrity`
- `make report-governance`
- `make check-generated-report-layout`
- `make check-bilingual-docs check-doc-links`
- `make lint`
- `PYTHONPYCACHEPREFIX=/var/tmp/codex/ModSecurity-conector/build/report-layout-pycache /root/git/ModSecurity-conector/.venv/bin/python -P -m py_compile ci/checks/documentation/check-generated-report-layout.py`
- `git diff --check`

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussierte Generated-Report-Evidence-Integrity-Suite | bestanden: initial 74 Tests in 19.734 Sekunden; Follow-up 74 Tests in 22.406 Sekunden. |
| `make report-governance` | initial und nach dem JSON-Suffix-Follow-up bestanden: Der Runtime-Path-Policy-Selftest lehnte seine beabsichtigten unsicheren/read-only Fälle korrekt ab, und die Governance-only-Report-Layout-Validierung bestand. |
| Striktes `make check-generated-report-layout` | blocked_environment: Der Checker schlug fail-closed fehl, weil der Task-Umgebung aktuelle sealed Build-Receipts und Report-Inputs fehlen; keine Runtime-Evidence wurde aktualisiert oder überschrieben. |
| `make check-bilingual-docs check-doc-links` | initial und nach dem JSON-Suffix-Follow-up bestanden: Bilinguale Dokumentation, Repository-Path-References und die vom Framework bereitgestellten Documentation-Links bestanden. |
| Breites `make lint` | blocked_environment: Shell-/Python-Syntax, 85 Runtime-/Cache-Contract-Tests und Apache-Strukturchecks bestanden, doch die nicht zugehörige native `check-apache-c17-lint`-Stufe lieferte länger als fünf Minuten keine Ausgabe und der task-eigene Prozess wurde unterbrochen; ein Gesamterfolg wird nicht behauptet. |
| `py_compile` des geänderten Checkers | initial und nach dem JSON-Suffix-Follow-up bestanden. |
| `git diff --check` | initial und nach dem JSON-Suffix-Follow-up bestanden: kein Whitespace-Fehler. |
| Fokussierter Post-Diff-Security-Review | initial und für den JSON-Suffix-Follow-up bestanden: Es wurde kein sicherheitsrelevanter Verhaltensdrift und kein plausibler Befund identifiziert. |
| Initialer Draft-PR-#149-Head `e4ea6744012bf3a72db2be0b972c954ceefcedff` | erforderliche GitHub-Checks und Quality Gate `OK` bestanden, mit 0,0 Prozent New-Code-Duplizierung, aber einem neuen task-eigenen `python:S1192`-Receipt `AZ-mYAcnCVtpA6IZuHRU`; deshalb `remediation_required`, nicht finale Verifikation. |

## Security-Auswirkung

Die Änderung berührt eine Python-Evidence-Consumer-Grenze und erhielt einen
fokussierten Security-Review. Sie bewahrt Trusted-Root-, Regular-File-,
Symlink-, Hash-, Receipt-, Canonical-Path-, Revisions- und Stability-Controls
sowie den strikten fail-closed Ergebnispfad. Kein Security-Control, Quality
Gate, Scanner-Rule, keine Suppression, Access-Boundary, kein Connector und
kein Runtime-Verhalten wird geschwächt. Der Review beobachtete eine separate
Low-Confidence-Generated-Report-Symlink-Alias-Idee, reproduzierte sie aber
nicht; sie wird nicht stillschweigend in diesen Maintainability-Refactor
aufgenommen.

Der JSON-Suffix-Follow-up ändert ausschließlich einen unveränderlichen
String-Owner und dessen drei Verwendungen in derselben Datei. Er ändert keinen
kontrollierten Input, keine Filesystem-Operation, keine Trust-Root, kein
Path-Prädikat, keinen Error-Path, keine Deserialisierungsoperation und keinen
Sink.

## Runtime-Evidence

Es wurde keine Connector-, Host-, Protokoll- oder Produktions-Runtime-Evidence
erzeugt oder geändert. Die fokussierte Suite und der Governance-Check sind nur
Source-/Documentation-Contract-Evidence. Der nicht verfügbare Strict-Evidence-
Zustand wird bewusst als blockiert ausgewiesen, statt ihn durch generierte
Artefakte zu ersetzen.

## Bekannte Einschränkungen

Das strikte Layout-Gate kann lokal ohne aktuelle sealed Runtime-Receipts und
deren gebundene Report-Inputs nicht vollständig laufen. Das breite `make lint`
erreichte eine nicht zugehörige native Apache-C17-Stufe, die länger als fünf
Minuten keine Ausgabe lieferte; deshalb wurde der task-eigene Prozess sicher
unterbrochen und wird nicht als bestanden behauptet. Gehostete GitHub- und
SonarQube-Cloud-Evidence existiert für den noch nicht veröffentlichten
JSON-Suffix-Follow-up-Head nicht. Der initiale Draft-#149-Head besitzt
gehostete Evidence, wird aber nicht für einen späteren Head wiederverwendet.

Der unterbrochene Lint-Prozess hatte noch einen eindeutig task-eigenen
`check-apache-c17-lint`-Kindprozess. Er wurde über seinen exakten
Candidate-Worktree-Command identifiziert, mit `SIGTERM` beendet, und ein
anschließender read-only Prozesscheck fand keinen weiteren task-eigenen
Lint-Prozess. Die durch den Lint-Lauf geänderten generierten Cache-Reports und
temporären Snapshot-Skripte wurden vor dem finalen Diff-Review restauriert
beziehungsweise entfernt und sind nicht Teil dieser Änderung.

## Verbleibende Risiken

Eine Helper-Extraktion kann versehentlich eine Exception-, Error-Order- oder
Early-Return-Randbedingung verändern. Die bestehende 74-Fall-Integrity-Suite,
der Governance-Check, statischer Diff-Review und der fokussierte
Security-Review mindern dieses Risiko, doch eine Exact-Head-Hosted-Analyse
bleibt erforderlich, bevor ein Receipt als gelöst gilt. Der JSON-Suffix-
Follow-up benötigt eine neue Exact-Head-Hosted-Analyse, bevor sein
ursprünglicher Receipt als abwesend gilt. Die separate
Symlink-Alias-Idee benötigt eine eigene Reproduktionsaufgabe, bevor sie ein
Befund oder eine Hardening-Änderung werden kann.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein Report-Refresh, keine Runtime-Matrix, kein Connector-Build, keine
  Protokollmatrix und kein MRTS-Check wurden ausgeführt: Die ausgewählte
  Änderung ist ein Parent-Checker-Refactor und verändert kein Connector-/
  Runtime-Verhalten; Evidence zu regenerieren würde die Task-Grenze verletzen.
- Das strikte Gate wurde versucht, ist aber wegen fehlender/veralteter sealed
  Evidence blockiert, wie oben erfasst; Governance-only-Erfolg wird nicht als
  strikter Nachweis dargestellt.
- Das breite Lint-Target endete nicht, weil die nicht zugehörige native
  Apache-C17-Stufe ohne Ausgabe stagnierte; die abgeschlossenen Teilprüfungen
  sind erfasst, und fokussierte Checker-Validierung bleibt die relevante lokale
  Delivery-Evidence.
- Der initiale Draft-PR-#149-Head besitzt gehostete GitHub- und
  SonarQube-Cloud-Evidence, doch der neue JSON-Suffix-Follow-up ist noch nicht
  committet oder gepusht; sein Exact-Head-Hosted-Zyklus muss nach der
  Veröffentlichung neu starten.

## Finaler Diff- und Review-Status

Der initiale Scoped Commit wurde als Draft-PR #149 am exakten Head
`e4ea6744012bf3a72db2be0b972c954ceefcedff` veröffentlicht. Er bestand seine
erforderlichen GitHub-Checks und das SonarQube-Cloud-Quality-Gate, doch die
exakte Analyse meldete den neuen task-eigenen JSON-Suffix-Receipt. Der
uncommittete Follow-up enthält nur denselben Parent-Checker und dieses
wahrheitsgemäße englisch/deutsche Change-Record-Update; seine fokussierte
Suite, sein Governance-Check, seine Syntax-Compilation und sein
Whitespace-Review bestanden wie oben erfasst. Er behauptet keine frische
Hosted-Evidence, kein Ready, keinen Merge und keine Master-Integration; diese
benötigen den späteren exakten Head.
