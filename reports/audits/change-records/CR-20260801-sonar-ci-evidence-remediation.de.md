# Änderungsnachweis: Parent-CI-Evidence-SonarQube-Cloud-Bereinigung

**Sprache:** [English](CR-20260801-sonar-ci-evidence-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260801-sonar-ci-evidence-remediation` |
| Datum (UTC) | 2026-08-01 |
| Basis-Revision | `6b4aca18d390363764b96d85cd31969b9bb114a1` |
| Tracking | SonarQube-Cloud-`ci/evidence`-Baseline: 15 Security-Befunde, 1 Security-Hotspot, 96 Maintainability-Befunde, 327 duplizierte Zeilen und 1,6 % Duplikatdichte. |
| Grenze | Parent-`ci/evidence`, ein fokussierter Parent-Regressionstest und dieses deutsch/englische Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, Workflows, Scanner-Einstellungen, Suppressions, Exclusions, Quality Gates und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das aktuelle `ci/evidence`-Inventar enthält Befunde zu Dateisystemgrenzen und
URL-Policy, einen Security-Hotspot, komplexe Report-Generatoren, wiederholte
Literale, redundante Listenbehandlung und duplizierte Reportlogik. Die
Bereinigung muss fail-closed Evidence-Eingaben, Statusklassifikation,
Reportschemata und Source-Root-Containment bewahren, ohne SonarQube-Cloud-
Regeln, Exclusions, Suppressions oder Quality Gates zu verändern.

## Akzeptanzkriterien

- Jeder Baseline-`ci/evidence`-Source-Anchor erhält eine Source-Level-Behebung
  oder explizite Hosted-Analyse-Dispostion; Scanner-Einstellungen und
  Suppressions bleiben unverändert.
- Output-Pfade bleiben unter sicheren Roots, weisen Traversal und Symlink-
  Escapes ab und bewahren einen gültigen In-Root-Output-Pfad.
- Repository-Referenzen bleiben HTTPS-only, wo bestehende Policy dies verlangt.
- Der Capability-Katalog bewahrt alle 60 Namen und die kanonische Reihenfolge.
- Der finale Draft-PR-Head erhält frische Actions- und SonarQube-Cloud-Evidence
  vor jeder Merge-Entscheidung.

## Implementierungsentscheidung und Begründung

Schmale Parsing-, Klassifikations-, Rendering- und Datenkonstruktions-Helper
besitzen jetzt die vorher wiederholte Reportlogik. Bestehende root-gebundene
Writer behalten Output-Containment, der Default-Cache bleibt unter einer
benutzerprivaten Root und HTTPS-Validierung bleibt explizit. Der Capability-
Katalog wird nach Verantwortungsbereich gruppiert und in seiner bisherigen
kanonischen Reihenfolge zusammengesetzt, ohne das öffentliche Ergebnis zu
verändern. Ein fokussierter Test führt gültigen In-Root-Output aus und weist
Traversal, Symlink-Escape, unsichere Schemes und permissive Permissions ab.

## Geänderte Dateien

- `ci/evidence/collectors/connector_capabilities.py`
- neunzehn Parent-`ci/evidence/reports/*.py`-Dateien aus dem Task-Diff,
  einschließlich Report-Refresh-, Runtime-Mismatch-, System-Environment-,
  Remaining-Critical/Failure- und NGINX-HTTP-500-Generatoren
- `tests/test_evidence_output_security.py`
- die beiden Change-Record-Indizes und dieses englisch/deutsche Record-Paar

## Ausgeführte Befehle

| Befehl oder Prüfung | Ergebnis |
| --- | --- |
| `python -m py_compile` für alle 20 geänderten Python-Source-/Test-Dateien | bestanden. |
| `python -m unittest tests.test_generated_report_evidence_integrity tests.test_report_conditional_remediation tests.test_evidence_output_security` | bestanden: 93 Tests; eingebetteter Generated-Report-Layout-Check bestand. |
| `python ci/evidence/collectors/connector_capabilities.py check` | bestanden: 6 Connectoren und 60 Capabilities. |
| `git diff --check origin/master...HEAD` | vor Change-Record-Ergänzungen bestanden; erneuter Lauf nach Dokumentationsänderungen und vor Auslieferung. |
| Fokussiertes Parent-Security-Diff-Review | bestanden: explizite Receipts decken alle 20 rebasierten Diff-Dateien ab; kein reportable Security-Regression-Candidate gefunden. |

## Security-Auswirkung

Evidence-Pfade weisen Output-Traversal und Symlink-Escapes vor Veröffentlichung
weiter ab, verwenden den bestehenden Safe-Root-bound Writer und erzeugen
Owner-only-Capability-Output. HTTPS-only-Repository-Validierung und fail-closed
Runtime-Evidence-Prädikate bleiben aktiv. Das fokussierte Review prüfte
geänderte Path-, Cache-, Writer-, URL- und Evidence-Klassifikationslogik und
fand keine reportable Diff-Regression; es ist keine Repository-weite Security-
Bewertung.

## Runtime-Evidence

Fokussierte Python-Controls führen die geänderten Report-Helper mit temporären
task-eigenen Roots aus. Sie zeigen gültigen Output und weisen Traversal,
Symlink-Escape, unsichere Repository-Schemes und permissive Permissions ab.
Der Capability-Befehl führt seinen öffentlichen Katalog-Check aus. Dies sind
keine Behauptungen einer vollständigen Connector-Matrix oder externen Runtime.

## Bekannte Einschränkungen

Weder `radon` noch Python-`ruff` sind in der ausgewählten Umgebung verfügbar;
lokale Komplexitäts-/Duplikatzahlen ersetzen daher nicht SonarQube Cloud. Der
paketierte Security-Diff-Worklist-Filter schließt `ci` aus. Das Review band
darum die exakten 20 geänderten Pfade explizit und bewahrte einen Receipt pro
Datei. SHA-gebundene Hosted-Analyse bleibt die Wahrheit für Sonar-Status.

## Verbleibende Risiken

Ein nicht ausgeübter Connector-Integrationspfad oder eine Live-Artefaktform
außerhalb der Fixtures könnte noch einen Darstellungsunterschied zeigen. Das
absichtlich nicht initialisierte, out-of-scope Framework-Submodul verhindert,
dass die vollständige Parent-Suite ihre Framework-abhängigen Controls ausführt.
SHA-gebundene Hosted-Actions- und SonarQube-Cloud-Analyse bleiben vor einer
Merge-Entscheidung notwendig.

## Nicht ausgeführte Prüfungen mit Begründung

- Vollständige Connector-Builds, Runtime-Matrizen und Report-Generation wurden
  nicht ausgeführt: Der Task ändert Parent-Evidence-Tooling und besitzt keine
  task-eigene verifizierte Connector-Runtime-Evidence.
- Framework- und MRTS-Prüfungen wurden nicht ausgeführt. Der Task ist nur
  Parent; keine Quelle und kein Gitlink in diesen Repositories änderte sich.
- Die breitere Parent-Unittest-Suite kann Framework-abhängige Controls nicht
  abschließen, weil das absichtlich uninitialisierte Submodul
  `modules/ModSecurity-test-Framework/ci/lib/common.sh` nicht enthält. Das ist
  eine Umgebungseinschränkung, keine Behauptung einer bestandenen Full Suite.
- Hosted Actions, Review-Status und SHA-gebundene SonarQube-Cloud-Analyse
  benötigen den autorisierten Draft PR und stehen beim Verfassen noch aus.

## Finaler Diff- und Review-Status

Beim Verfassen dieses Records liegt der rebasierte Source-/Test-Checkpoint bei
`f9d48a12ba444efb294ae28aa7944cc5eedea87e` auf der genannten Basis. Er ist
auf Parent-`ci/evidence`, einen fokussierten Parent-Test und Traceability-
Dokumentation begrenzt. Es gibt keine Framework-/MRTS-/Gitlink-, Workflow-,
Dependency-, Scanner-Konfigurations-, Suppression-, Quality-Gate- oder
`master`-Änderung. Lokale Controls und das begrenzte Review bestanden. Commit,
Push, Draft PR, Hosted-Verifikation und Integration werden nicht behauptet;
dieser Record autorisiert keinen Merge.

### Auslieferungsautorisierung und vorgesehene Integration

Nachdem der PR `verified_pr` erreicht hatte, autorisierte der aktuelle Nutzer
explizit nur diese Parent-Integration mit „bringe das pr 215 in den master“.
Das autorisierte Inventar ist daher ausschließlich PR #215 von
`Easton97-Jens/ModSecurity-conector`; Framework, MRTS, Gitlinks und weitere
PRs sind nicht eingeschlossen. Das geschützte `master`-Ruleset verlangt einen
Pull Request, aufgelöste Review-Threads und seine sechs gelisteten
Status-Checks, aber null zustimmende Reviews. Es erlaubt Merge-, Squash- und
Rebase-Methoden. Die zwei letzten passenden Parent-Integrationen (#214 und
#212) sind Merge-Commits; deshalb ist ein SHA-gebundener Merge-Commit die
vorgesehene Methode. Finaler Head, Merge-Ergebnis und resultierende Master-
Evidence müssen vom Integrationstask beobachtet und aufbewahrt werden, statt in
diesem Pre-Merge-Record behauptet zu werden.
