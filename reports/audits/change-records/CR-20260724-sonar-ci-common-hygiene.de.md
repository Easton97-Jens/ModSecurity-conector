# Change Record: Parent-CI/Common-SonarQube-Cloud-Hygiene-Behebung

**Sprache:** [English](CR-20260724-sonar-ci-common-hygiene.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260724-sonar-ci-common-hygiene |
| Datum (UTC) | 2026-07-24 |
| Basis-Revision | 5b8db00d44ab24f3a9f4216a00f7edee977b6898 |
| Tracking | Fünf aktive Parent-SonarQube-Cloud-Code-Smells: AZ9cRyZWHhV2CayPTPwW, AZ7POyUhBW70q7L2nMJP, AZ8d8_z6E36x1qGA4xhZ, AZ9cRyZ9HhV2CayPTPwb und AZ9cRyWTHhV2CayPTPuh. |
| Grenze | Parent-ci/-Checker-Quellcode sowie dieses englisch/deutsche Traceability-Paar und die Indizes. Framework, MRTS, Gitlinks, Scanner-Konfiguration, Quality Gates, Suppressions, Runtime-Verhalten der Connectoren und generierte Artefakte bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten SonarQube-Cloud-Zeilen melden zwei unbenutzte private Hilfsparameter (python:S1172) und drei wiederholte statische Literale (python:S1192) in Parent-CI-, Evidence-, Common-SDK-Contract- und Dokumentations-Checkern. Die Zeilen sind Maintainability-Code-Smells; die drei S1192-Zeilen haben in Sonar die Priorität CRITICAL, aber ausschließlich einen Maintainability-Impact und keinen validierten Sicherheitsimpact.

## Akzeptanzkriterien

- Nur die zwei als unbenutzt nachgewiesenen Parameter entfernen und ihre jeweils einzigen lokalen Aufrufer aktualisieren.
- Jedes wiederholte Literal einmal benennen, ohne seinen Stringwert, Checker-Ergebnis, Control-Reihenfolge, Ausgabetext oder die Source-Contract-Assertion zu verändern.
- Fokussierte Parent-Unit-/Check-Ziele, Syntax-Parsing, Source-Occurrence-Review, Bytecode-Scan und Diff-Hygiene-Prüfungen bestehen.
- Vollständige englisch/deutsche Change Records und Indizes pflegen.
- Exact-Head-GitHub- und SonarQube-Cloud-Draft-PR-Evidenz einholen, bevor ein ausgewählter Key als verifiziert beschrieben wird.

## Implementierungsentscheidung und Begründung

promotion_errors akzeptiert seinen unbenutzten Parameter run_dir nicht mehr, und network_cache_status akzeptiert seinen unbenutzten Parameter env nicht mehr. Ein repo-weiter Call-Graph-Review fand jeweils einen lokalen Aufrufer.

DEFAULT_WEB_SERVER_STATUSES, SUCCESS_RETURN_LITERAL und NOT_EXECUTED_STATUS ersetzen nur gleichbedeutende Vorkommen von "403,501", "return 0" und "NOT EXECUTED". Das deterministische Reverse-Order-Control-Input "501,403" bleibt explizit. Alle bisherigen Source-Contract-Probes und Fehlertexte behalten ihre exakten Werte.

## Security-Auswirkung

Die normale Sicherheitsbewertung lautet not_applicable: Dieser mechanische Patch verändert weder Datei-/Pfadverarbeitung, Subprozesse, Credentials, Berechtigungen, Parsing, Logging, Scanner-Controls noch Connector-Enforcement. Er ändert nur interne unbenutzte Signaturen und modul-lokale unveränderliche Konstanten und bewahrt die vorhandenen sicherheitsorientierten Common-SDK-Source-Probes. Es wird kein Sicherheitsbefund als behoben behauptet.

## Geänderte Dateien

- ci/checks/evidence/check-full-lifecycle-evidence.py
- ci/checks/evidence/check-runtime-producer-readiness.py
- ci/checks/common/check-block-status-generator.py
- ci/checks/common/check-common-sdk-contract.py
- ci/checks/documentation/check-no-crs-doc-consistency.py
- reports/audits/change-records/README.md und README.de.md
- dieses englisch/deutsche Change-Record-Paar

## Ausgeführte Befehle

Die fokussierten Kommandos nutzten Parent-.venv-Python,
PYTHONDONTWRITEBYTECODE=1, PYTHONNOUSERSITE=1 und ein task-owned externes
TMPDIR:

- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_full_lifecycle_evidence
- rtk proxy -- env ... <Parent .venv python> -m unittest -v tests.test_runtime_producer_readiness_path_policy
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-block-status-generator
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-common-sdk-contract
- rtk proxy -- env ... make PYTHON=<Parent .venv python> check-no-crs-doc-consistency
- rtk proxy -- env ... <Parent .venv python> -c <AST parse for the five changed modules>
- rtk proxy -- git diff --check

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Fokussiertes Full-Lifecycle-Unit-Modul | bestanden: tests.test_full_lifecycle_evidence, 17 Tests. |
| Fokussiertes Runtime-Producer-Path-Policy-Unit-Modul | bestanden: tests.test_runtime_producer_readiness_path_policy, 4 Tests. |
| check-block-status-generator | bestanden: block_status_generator: pass. |
| check-common-sdk-contract | bestanden: common-sdk-contract: pass. |
| check-no-crs-doc-consistency | bestanden: no-crs-doc-consistency: PASS. |
| AST-Parse aller fünf geänderten Python-Module | bestanden. |
| Fokussierter Source-Occurrence-Review | bestanden: Jedes ausgewählte Literal kommt einmal als Modulkonstante vor; beide Helper-Definitionen und -Aufrufe enthalten nur ihre verwendeten Parameter. |
| git diff --check und pyc-Scan des getrackten Worktrees | bestanden: keine Whitespace-Fehler und keine Bytecode-Dateien. |
| tests.test_bilingual_docs | bestanden: 11 Tests. |
| Direkte Repository-Change-Record-Paar-Validierung | bestanden: erforderliche Abschnitte, Identitätswerte, Heading-Level und Tabellenstruktur stimmen für dieses EN/DE-Paar überein. |

## Runtime-Evidence

Es wurde kein Connector-Runtime-Verhalten verändert oder behauptet. Die Checks sind Parent-lokale Source-/Evidence-/Dokumentations-Controls und keine Host-Traffic- oder Produktions-Runtime-Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

- make check-runtime-producer-readiness wurde nicht ausgeführt, weil sein Make-Target check-framework voraussetzt; das fokussierte Parent-Testmodul deckt den geänderten build_payload-Pfad ab und Framework ist out of scope.
- Connector-Builds, Host-Runtime-Smoke-Tests, Protokollmatrizen, Framework- und MRTS-Checks wurden nicht ausgeführt, weil kein Connector-/Runtime-Code geändert wurde und Framework/MRTS ausgeschlossen sind.
- make check-bilingual-docs ist ausschließlich durch 20 vorhandene fehlende Framework-Gitlink-Linkziele blocked_environment. Derselbe Lauf meldet keinen Fehler in diesem neuen Change-Record-Paar, und die direkte Paar-Validierung bestand.
- make check-doc-links ist ausschließlich durch 16 vorhandene fehlende Framework-Gitlink-Linkziele blocked_environment; es wurde kein Framework-Quellcode, Gitlink oder generiertes Artefakt geändert, um dies zu umgehen.
- Die Hosted-GitHub-/SonarQube-Cloud-Exact-Head-Verifikation steht bis zur Draft-PR-Delivery noch aus.

## Bekannte Einschränkungen

Dieser Batch korrigiert nur fünf ausgewählte Parent-SonarQube-Cloud-Befunde. Er behauptet nicht, den breiteren SonarQube-Cloud-Backlog mit 1.474 Befunden zu beheben.

## Verbleibende Risiken

Eine versehentliche Abweichung zwischen Konstante und Literal könnte einen statischen Checker abschwächen. Die fokussierten Checker-Ausführungen, der exakte Source-Occurrence-Review, AST-Parsing und Diff-Review reduzieren dieses Risiko. Hosted-Exact-Head-Analyse bleibt erforderlich.

## Finaler Diff- und Review-Status

Die Source-Implementierung liegt im initialen Commit e09886ca4713798fc47e1304c651fd0e7216a692 auf einem Branch mit Basis 5b8db00d44ab24f3a9f4216a00f7edee977b6898. Draft PR #111 existiert für diesen Branch, bleibt offen und Draft und ist nicht gemergt. Die exakte Current-Head-Remote-, GitHub-, SonarQube-Cloud- und Review-Evidenz wird im PR und im Task-Receipt festgehalten, statt einen selbstreferenziellen Change-Record-Commit zu erzeugen. Kein Merge, Default-Branch-Update, Framework-Action oder MRTS-Action ist autorisiert oder erfolgt.
