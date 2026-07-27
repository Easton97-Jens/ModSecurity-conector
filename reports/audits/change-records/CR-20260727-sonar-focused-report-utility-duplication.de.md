# Change Record: Parent-Focused-Report-Hilfsduplikatreduzierung für SonarQube Cloud

**Sprache:** [English](CR-20260727-sonar-focused-report-utility-duplication.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-focused-report-utility-duplication |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-Duplikatbaseline: 2.013 Zeilen und 0,4 Prozent. Kandidat: der exakt gemeinsame 78-Zeilen-Utility-Präfix des Nolog- und Response-Header-Focused-Report-Generators mit neun byte-/verhaltensgleichen Funktionen. |
| Grenze | Zwei Parent-Report-Generatoren, neuer Parent-Utility/Test und dieses EN/DE-Change-Record-Paar. Workflows, Report-Refreshes, generierte Reports, Runtime-Matrizen, Framework/MRTS-Quelle, Gitlinks, Sonar-Konfiguration, Suppressions, externer Issue-Status und Master bleiben unverändert. |

## Motivation und Problemstellung

Die beiden Focused-Report-Generatoren enthielten dieselbe kleine Utility-Schicht zweimal. Das erschwert die konsistente Prüfung von Safe-Read/Write, Pfadredaktion, dynamischem Import und JSON-Formatierung. Der Kandidat zentralisiert ausschließlich neun identische Funktionen und lässt generator-spezifisches Verhalten wie Nologs `action_value` bewusst lokal.

## Akzeptanzkriterien

- Die neun extrahierten Funktionen erhalten Return-Werte, Fehler, JSON-Formatierung und dynamischen Import.
- `report_path_safety` bleibt alleinige Safe-Root-/Dateicontainment-Kontrolle für Reads und Writes.
- Außenpfade bleiben als `<runtime-artifact>/<leaf>` redigiert; gültige In-Root-Dateien behalten relative Connector-/Framework-Labels.
- Beide Generatoren behalten lokale CLI, Safe-Root-Setup, Schema/Payload, Output-Aufrufe und spezifische Funktionen.
- Kein Report-Refresh, Runtime-All, Workflow-, Framework/MRTS-, Gitlink-, Suppression- oder Master-Change tritt auf.
- Eine neue exakte SonarQube-Cloud-Head-Analyse bestimmt die tatsächliche globale Duplikatänderung.

## Implementierungsentscheidung und Begründung

`ci/lib/focused_analysis_utils.py` besitzt nur UTC-Formatierung, sichere JSON/Text-Wrapper, List-Koerzierung, Queue-Totale, dynamischen Import, Pfadsanitisierung und quoted-comma Action-Parsing. Beide Generatoren behalten `add_safe_roots`, `add_report_roots`, `resolve_output_dir`, CLI, Schema/Payload und Output-Orchestrierung. Der Helper delegiert Dateizugriffe an unveränderte `report_path_safety`-Wrapper und konfiguriert oder mutiert `SAFE_ROOTS` nicht.

## Geänderte Dateien

- ci/evidence/reports/generate-nolog-audit-evidence-analysis.py
- ci/evidence/reports/generate-response-header-hook-analysis.py
- ci/lib/focused_analysis_utils.py
- tests/test_focused_analysis_utils.py
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.md
- reports/audits/change-records/CR-20260727-sonar-focused-report-utility-duplication.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

```sh
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest -v tests.test_focused_analysis_utils tests.test_generated_report_evidence_integrity tests.test_report_presentation_literals
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/evidence/reports/generate-nolog-audit-evidence-analysis.py --help
rtk proxy env PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 /root/git/ModSecurity-conector/.venv/bin/python -B ci/evidence/reports/generate-response-header-hook-analysis.py --help
rtk proxy git diff --check
```

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Focused-Utility-Vertrag | bestanden: 7 Tests für Shared Bindings, Parsing, Totale, In-Root-Read/Write, Outside-Root-Redaktion/Ablehnung, Safe-Root-Erhalt und Modulregistrierung. |
| Evidence-/Presentation-Regression | bestanden: 84 Tests; ihre generated-report-layout-Prüfung meldete `PASS`. |
| Beide Generator-`--help`-Entrypoints | bestanden ohne Report-Artefakte zu generieren oder zu refreshen. |
| Unabhängige Security-/Pfadreview | bestanden: kein Sicherheitsblocker und keine geänderte Safe-Root-/Evidence-Integrity-Kontrolle. |
| `git diff --check` | bestanden: keine Whitespace-Fehler. |

## Security-Auswirkung

Dies ist ein sicherheitsrelevanter Refactor, weil Report-Pfad- und Evidence-Utilities berührt werden. Der Helper delegiert Reads an `read_json_file`/`read_text_file`, Writes an `write_json_file` und Pfadklassifikation an `safe_existing_file`; diese Funktionen erzwingen konfigurierte Safe-Roots und Regular-File-Checks. Der Helper leert oder erweitert Safe-Roots nicht. Dynamische Imports behalten vorhandene feste aufrufergesteuerte Pfade und `sys.modules`-Registrierung vor Ausführung. Kein neuer Sicherheitsbefund wurde identifiziert.

## Dokumentationsstatus

Dieses EN/DE-Change-Record-Paar dokumentiert Umfang, lokale Validierung, die No-Refresh-Grenze und dass noch eine externe SonarQube-Cloud-Messung erforderlich ist. Beide Change-Record-Indizes sind aktualisiert.

## Runtime-Evidence

Es wurde kein Report-Refresh, Connector-Runtime, Protokolltest oder Produktionsverhalten ausgeführt oder behauptet. Die beiden `--help`-Aufrufe beweisen nur Direct-Script-Import/Argumentinitialisierung; die Testmodule prüfen Helper-/Evidence-Verträge.

## Bekannte Einschränkungen

Ein Bytevergleich vollständiger Reports vor/nach dem Kandidaten wurde nicht ausgeführt, weil Report-Refresh/Generierung ausdrücklich nicht im Scope ist. Helper-Level-Outside-Root-Verhalten ist direkt getestet; Traversal-/Symlink-Fälle erzwingt weiter die unveränderte `report_path_safety`-Implementierung und ihre Integritätssuite. SonarQube Cloud hat den Kandidaten nicht analysiert, daher wird keine globale Reduktion behauptet.

## Verbleibende Risiken

Der Shared-Dynamic-Import-Utility führt weiterhin vertrauenswürdige konfigurierte Script-Pfade aus; das ist eine vorhandene Vertrauensgrenze und wurde durch die Extraktion nicht erweitert. Eine spätere Integrationsfixture könnte beide Generatoren in einer dedizierten nicht-generierenden Output-Root vollständig ausführen. Der Kandidat trifft keine Aussage über andere Duplikatblöcke oder den 1.022-Item-Backlog.

## Nicht ausgeführte Prüfungen mit Begründung

- Kein `refresh-all-reports`, Runtime-All, 12-Zellen-Matrix, Generated-Report-Update oder Workflow-Change wurde ausgeführt, weil dies ausdrücklich out of scope ist.
- Connector-Builds und MRTS-Tests sind nicht anwendbar, weil keine Connector- oder Cross-Repository-Quelle geändert wurde.
- Gehostete GitHub-Checks und die exakte SonarQube-Cloud-Head-Analyse sind noch nicht erfolgt; dieser Record liefert weder globale Duplikatkennzahl noch Master-Merge-Autorisierung.

## Finaler Diff- und Review-Status

Der Kandidat ist auf zwei Parent-Report-Generatoren, kleinen Parent-Helper/Test und zweisprachige Traceability begrenzt. Unabhängige Security-/Pfadreview fand keinen Blocker. Commit-, Push-, PR-, Hosted-Check-, Sonar-Analyse- und Merge-Fakten werden erst nach Beobachtung dokumentiert.
