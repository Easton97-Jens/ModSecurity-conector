# Change Record: Parent-Focused-Report-Hilfsduplikatreduzierung für SonarQube Cloud

**Sprache:** [English](CR-20260727-sonar-focused-report-utility-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-focused-report-utility-duplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-Duplikatbaseline: 2,013 duplizierte Zeilen und 0.4 Prozent Dichte. Die erste exakte Analyse des Draft-PR #135 vor der aktuellen lokalen Remediation meldete 1,834 duplizierte Zeilen, 22 neue duplizierte Zeilen und 9.2% New-Code-Duplikierung. Dieser Head verfehlte das ≤3%-New-Code-Duplikat-Gate und meldete `python:S3776` sowie `python:S3358`. |
| Grenze | Neun fokussierte Parent-Report-Generatoren, ein Parent-Utility, ein fokussierter Parent-Test, dieses englisch/deutsche Change-Record-Paar und die bereits vorhandenen Indexeinträge. Workflows, Report-Refreshes, generierte Reports, Runtime-Matrizen, Framework/MRTS-Quelle, Gitlinks, Sonar-Konfiguration, Suppressions, externer Issue-Status und Master bleiben unverändert. |

## Motivation und Problemstellung

Die fokussierten Nolog- und Response-Header-Report-Generatoren duplizierten
ursprünglich eine kleine Utility-Schicht. Die erste Extraktion senkte die
beobachtete globale Zahl, aber ihre exakte Draft-PR-#135-Analyse scheiterte
weiterhin, weil der neue Helper vorhandene Implementierungszeilen duplizierte
und sein Quoted-Comma-Parser `python:S3776` und `python:S3358` meldete. Die
aktuelle lokale Remediation entfernt diese New-Code-Duplikatquellen ohne
Report-Refreshes oder Runtime-Arbeit: Sie nutzt vorhandene sichere Primitive
wieder und teilt verhaltensäquivalente Utility-Bindungen über neun fokussierte
Report-Generatoren. Generator-spezifische Analyse-, Payload-, CLI- und
Output-Verhalten bleiben lokal.

## Akzeptanzkriterien

- Die geteilten Utility-Bindungen bewahren frühere Return-Werte, Fehler, JSON-Formatierung, Dynamic-Import-Verhalten und `as_list`-Scalar-/List-Verhalten, einschließlich eines nichtleeren skalaren Leerzeichen-Strings.
- `report_path_safety` bleibt alleinige Safe-Root-/Dateicontainment-Kontrolle für Reads und Writes; der Helper konfiguriert oder mutiert `SAFE_ROOTS` nicht.
- Außenpfade bleiben als `<runtime-artifact>/<leaf>` redigiert; gültige In-Root-Dateien behalten relative Connector-/Framework-Labels.
- Alle neun Generatoren behalten ihre lokale CLI-Analyse, Safe-Root-Setup, Payload-/Schema-Zusammenstellung, Output-Aufrufe und generator-spezifischen Funktionen.
- `action_parts` bewahrt Quoted-Commas, gemischte Quotes, leere Segmente und unvollständige Quotes, ohne die frühere Komplexitäts-/Nested-Conditional-Struktur zu übernehmen.
- Kein Report-Refresh, Runtime-All, Workflow-, Framework/MRTS-, Gitlink-, Suppression- oder Master-Change tritt auf.
- Eine frische exakte SonarQube-Cloud-Head-Analyse, nachdem die uncommittete Remediation ausgeliefert ist, bestimmt statt eines lokalen Clone-Vergleichs das aktuelle Quality Gate und das globale Duplikatergebnis.

## Implementierungsentscheidung und Begründung

`ci/lib/focused_analysis_utils.py` aliasiert direkt `generated_report_utils.utc_now`, `report_path_safety.read_json_file`, `report_path_safety.read_text_file` und `report_path_safety.write_json_file` als `utc_now`, `read_json`, `read_text` und `write_json`. Es behält nur die fokussierte List-Koerzierung, Queue-Totale, den dynamischen Import, die Pfadsanitisierung und das Quoted-Comma-Parsing, die nicht bereits durch diese Primitive bereitgestellt werden.

Der Helper hält `as_list` mit den früheren Generatoren kompatibel: Listenelemente mit leerer String-Repräsentation werden gefiltert, während ein nichtleerer Non-List-Scalar unverändert als einzelner String zurückkehrt. `action_parts` ist in `_next_quote` und `_append_action_part` zerlegt; die direkte Contract-Suite deckt Quoted-, Mixed-Quote-, Empty-Segment- und Unterminated-Quote-Fälle ab. Die neun Generatoren importieren nur verhaltensäquivalente Bindungen, behalten ihr eigenes `add_safe_roots`, `add_report_roots`, `resolve_output_dir`, CLI-Handling, Schema-/Payload-Konstruktion und Output-Orchestrierung und ändern keinen Report-Path-Control.

## Geänderte Dateien

- ci/evidence/reports/generate-nolog-audit-evidence-analysis.py
- ci/evidence/reports/generate-response-header-hook-analysis.py
- ci/evidence/reports/generate-body-processor-analysis.py
- ci/evidence/reports/generate-rule-chain-semantics-analysis.py
- ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py
- ci/evidence/reports/generate-intervention-blocking-analysis.py
- ci/evidence/reports/generate-phase4-hard-abort-capability.py
- ci/evidence/reports/generate-remaining-failure-analysis.py
- ci/evidence/reports/generate-final-consistency-audit.py
- ci/lib/focused_analysis_utils.py
- tests/test_focused_analysis_utils.py
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.md
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_focused_analysis_utils tests.test_generated_report_evidence_integrity tests.test_report_presentation_literals tests.test_remaining_failure_analysis
rtk proxy bash -lc 'for task_file in ci/evidence/reports/generate-nolog-audit-evidence-analysis.py ci/evidence/reports/generate-response-header-hook-analysis.py ci/evidence/reports/generate-body-processor-analysis.py ci/evidence/reports/generate-rule-chain-semantics-analysis.py ci/evidence/reports/generate-no-mrts-intervention-nomatch-analysis.py ci/evidence/reports/generate-intervention-blocking-analysis.py ci/evidence/reports/generate-phase4-hard-abort-capability.py ci/evidence/reports/generate-remaining-failure-analysis.py ci/evidence/reports/generate-final-consistency-audit.py; do /root/git/ModSecurity-conector/.venv/bin/python -B "$task_file" --help >/dev/null || exit $?; done'
rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs
rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links
rtk proxy git diff --check
```

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussierte Utility-/Evidence-Regression-Module | bestanden: 86 Tests über `tests.test_focused_analysis_utils`, `tests.test_generated_report_evidence_integrity`, `tests.test_report_presentation_literals` und `tests.test_remaining_failure_analysis`. Die fokussierte Utility-Suite enthält Safe-Root-/Redaktions-/Write-Rejection-, Shared-Binding-, Scalar-/List-Koerzierung-, Dynamic-Import- und Quoted-Comma-Parser-Controls. |
| Generated-Report-Layout | bestanden: Der fokussierte Testbefehl meldete `check-generated-report-layout: PASS`. |
| Neun Generator-`--help`-Entrypoints | bestanden ohne Report-Artefakte zu generieren oder zu refreshen. |
| Fokussierte Security-/Pfadreview | bestanden: Direkte Aliase bewahren die bestehenden Safe-Root-/Evidence-Integrity-Controls; kein neuer Security-Blocker wurde identifiziert. |
| `make check-bilingual-docs` | bestanden: `bilingual docs ok`. |
| `make check-doc-links` | bestanden: `repository path references: PASS` und `doc links ok`. |
| `git diff --check` | bestanden: keine Whitespace-Fehler. |
| Erste exakte Draft-PR-#135-SonarQube-Cloud-Analyse | fehlgeschlagen: 22 neue duplizierte Zeilen und 9.2% New-Code-Duplikierung überschritten ≤3%; außerdem wurden `python:S3776` und `python:S3358` gemeldet. |
| Aktuelle uncommittete Remediation | extern nicht ausgeführt: Sie benötigt eine neue exakte SonarQube-Cloud-Head-Analyse nach einem beobachteten Commit und Push. |

## Security-Auswirkung

Dies ist ein sicherheitsrelevanter Refactor, weil Report-Pfad- und Evidence-Utilities berührt werden. Reads und Writes bleiben die bestehenden `report_path_safety.read_json_file`, `report_path_safety.read_text_file` und `report_path_safety.write_json_file`-Controls; die Pfadklassifikation bleibt `safe_existing_file`. Der Helper leert oder erweitert `SAFE_ROOTS` nicht. Dynamische Imports behalten ihre früheren festen aufrufergesteuerten Pfade und das `sys.modules`-Registrierung-vor-Ausführung-Verhalten. Kein neuer Security-Befund wurde identifiziert.

## Dokumentationsstatus

Dieses vollständige englisch/deutsche Change-Record-Paar beschreibt jetzt den erweiterten Neun-Generator-Kandidaten, den beobachteten ersten SonarQube-Cloud-Fehlschlag und die erforderliche frische Exact-Head-Analyse. Beide Change-Record-Indexeinträge bestanden bereits und benötigen keine zusätzliche Änderung.

## Runtime-Evidence

Es wurde kein Report-Refresh, Connector-Runtime, Protokolltest oder Produktionsverhalten ausgeführt oder behauptet. Die neun `--help`-Aufrufe beweisen nur Direct-Script-Import/Argumentinitialisierung; die Testmodule prüfen Helper- und Evidence-Contracts.

## Bekannte Einschränkungen

Ein Bytevergleich vollständiger Reports vor/nach dem Kandidaten wurde nicht ausgeführt, weil Report-Refresh/Generierung ausdrücklich out of scope ist. Helper-Level-Outside-Root-Verhalten ist direkt getestet; Traversal-/Symlink-Fälle erzwingt weiter die unveränderte `report_path_safety`-Implementierung und ihre Integritätssuite. Der lokale Clone-Vergleich ist keine SonarQube-Cloud-Evidence. Der aktuelle remediierte Stand ist uncommittet und hat daher kein neues Exact-Head-Ergebnis.

## Verbleibende Risiken

Der Shared-Dynamic-Import-Utility führt weiterhin vertrauenswürdige konfigurierte Script-Pfade aus; das ist eine vorhandene Vertrauensgrenze und wurde nicht erweitert. Eine spätere Integrationsfixture kann jeden Generator End-to-End gegen eine dedizierte nicht-generierende Output-Root ausführen. Dieser Kandidat trifft keine Aussage über andere Duplikatblöcke oder den breiteren 1,022-Item-Backlog.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein `refresh-all-reports`, Runtime-All, 12-Zellen-Matrix, Generated-Report-Update oder Workflow-Change wurde ausgeführt, weil jede dieser Aktionen ausdrücklich out of scope ist.
- Connector-Builds und MRTS-Tests sind nicht anwendbar, weil keine Connector- oder Cross-Repository-Quelle geändert wurde.
- Es gibt keinen frischen gehosteten GitHub-Check und keine exakte SonarQube-Cloud-Head-Analyse für die aktuelle uncommittete Remediation. Die vorherige exakte Draft-PR-#135-Analyse schlug fehl und kann diesen Follow-up nicht validieren.

## Finaler Diff- und Review-Status

Der erste exakte Head des Draft-PR #135 ist nicht für Review oder Merge bereit, weil seine SonarQube-Cloud-Analyse fehlgeschlagen ist. Die hier beschriebene erweiterte Remediation ist lokal, uncommittet und ungepusht; sie hat keinen neuen Remote- oder PR-Head. Es gab keine Framework-, MRTS-, Gitlink-, Ready-for-Review- oder Master-Action. Ein Commit/Push gefolgt von einer frischen Exact-Head-Analyse ist die erforderliche nächste Delivery-Validierung.
