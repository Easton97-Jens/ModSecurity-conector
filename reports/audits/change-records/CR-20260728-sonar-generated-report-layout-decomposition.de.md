# Change Record: Parent-Zerlegung des Generated-Report-Layouts für SonarQube Cloud

**Sprache:** [English](CR-20260728-sonar-generated-report-layout-decomposition.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-generated-report-layout-decomposition |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-`python:S1192`-Receipts `AZ7K5CRYixFPtcnbna1Q`, `AZ7POyU1BW70q7L2nMJQ` und `AZ7POyU1BW70q7L2nMJR`; außerdem `python:S3776`-Receipts `AZ7K5CRYixFPtcnbna1U`, `AZ7K5CRYixFPtcnbna1V`, `AZ7K5CRYixFPtcnbna1X`, `AZ7K5CRYixFPtcnbna1Y` und `AZ7Tenm9HrNUCHtbhYSD`. |
| Grenze | Ausschließlich Parent-Report-Layout-Checker und dessen bestehende Integritätstests. Framework wurde read-only am Parent-gepinnten `47e50e7bc43ba7a3b5bad1a9448111794f664cc0` geprüft; MRTS, Gitlinks, generierte Reports, Runtime-Evidence, Workflows, Scanner-Policy, Suppressions und der externe SonarQube-Cloud-Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Der ausgewählte Checker enthält wiederholte unveränderliche Literale und fünf
große Orchestratoren, die SonarQube Cloud als Maintainability Debt meldet. Er
ist zugleich ein fail-closed Consumer von Generated-Report- und
Runtime-Evidence. Der Refactor darf deshalb nur strukturelle Duplikate und
Komplexität entfernen, ohne Trust-, Hash-, Receipt-, Revisions-, Symlink- oder
Strict-Evidence-Controls zu lockern.

## Akzeptanzkriterien

- Ausschließlich die drei wiederholten `python:S1192`-Literale durch
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
| Fokussierte Generated-Report-Evidence-Integrity-Suite | bestanden: 74 Tests in 19.734 Sekunden. |
| `make report-governance` | bestanden: Der Runtime-Path-Policy-Selftest lehnte seine beabsichtigten unsicheren/read-only Fälle korrekt ab, und die Governance-only-Report-Layout-Validierung bestand. |
| Striktes `make check-generated-report-layout` | blocked_environment: Der Checker schlug fail-closed fehl, weil der Task-Umgebung aktuelle sealed Build-Receipts und Report-Inputs fehlen; keine Runtime-Evidence wurde aktualisiert oder überschrieben. |
| `make check-bilingual-docs check-doc-links` | bestanden: Bilinguale Dokumentation, Repository-Path-References und die vom Framework bereitgestellten Documentation-Links bestanden. |
| Breites `make lint` | blocked_environment: Shell-/Python-Syntax, 85 Runtime-/Cache-Contract-Tests und Apache-Strukturchecks bestanden, doch die nicht zugehörige native `check-apache-c17-lint`-Stufe lieferte länger als fünf Minuten keine Ausgabe und der task-eigene Prozess wurde unterbrochen; ein Gesamterfolg wird nicht behauptet. |
| `py_compile` des geänderten Checkers | bestanden. |
| `git diff --check` | bestanden: kein Whitespace-Fehler. |
| Fokussierter Post-Diff-Security-Review | bestanden: Es wurde kein sicherheitsrelevanter Verhaltensdrift und kein plausibler Befund identifiziert. |

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
SonarQube-Cloud-Evidence existiert für diesen noch nicht veröffentlichten
Kandidaten-Head nicht.

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
bleibt erforderlich, bevor ein Receipt als gelöst gilt. Die separate
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
- Es lief noch keine gehostete GitHub-Actions- oder SonarQube-Cloud-Analyse,
  weil der Kandidat noch nicht committet, gepusht oder als Draft-PR geöffnet
  wurde.

## Finaler Diff- und Review-Status

Vor der Delivery enthält der Scoped Diff nur den Parent-Checker sowie dieses
Traceability-/Documentation-Paar samt Index-Update. `git diff --check`, die
fokussierte Integrity-Suite, der Governance-Check, Syntax-Compilation und der
unabhängige Security-Review haben die oben erfassten tatsächlichen
Dispositionen. Dieser Record behauptet keinen Commit, Push, Pull Request,
Hosted-Check, kein SonarQube-Cloud-Ergebnis und keine Master-Integration; jeder
Zustand benötigt separate Exact-Head-Evidence.
