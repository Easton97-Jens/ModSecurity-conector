# FND-PARENT-0068 — Apache-Cleanup-Runner führen Compiler-Ausgabe aus vorhersagbaren gemeinsam genutzten temporären Bäumen aus

## Identität

- Kategorie: `security_validated`
- Repository / Ownership: `parent` / `parent`
- Priorität / Schweregrad / Konfidenz: `P3` / `low` / `validated` (`0.72`)
- Status / Machbarkeit: `in_progress` / `feasible_now`
- Release-Blocker / Candidate-Integration-Blocker / Sicherheitsrelevanz: `false` / `true` / `true`
- Connector / Protokoll / Profil: `apache` / `local/shared-host CI and test-runner filesystem execution boundary` / `vom Task eingeführter uncommitteter RulesSet-Cleanup-Snapshot plus identischer aktueller Request-Transaction-Cleanup-Sibling`

## Zusammenfassung

Zurückgehaltene Security-Diff-Evidence validiert eine vom Task eingeführte Pre-Remediation-Schwäche des Apache-RulesSet-Cleanup-Runners. Er wählt einen vorhersagbaren Default unter `/var/tmp/ModSecurity-conector-verified/build`, akzeptiert nur einen absoluten Pfad, erhält einen bestehenden Baum mit `mkdir -p`, linkt einen festen Binary-Namen und führt ihn aus. Auf einem Multi-User-Developer-Host oder Shared-Self-Hosted-Runner kann ein niedriger privilegierter Akteur diesen Baum vor dem Opferprozess vorab erzeugen oder racen.

Der identische bereits bestehende Request-Transaction-Cleanup-Runner bleibt auf Parent-master. GitHub-External-PR-/Token-Eskalation ist ausdrücklich widerlegt: Kein `pull_request_target`, kein untrusted Workflow-Input, kein writable Token und kein PR-Pfad erreichen diesen Runner. Diese Gegen-Evidence löscht den unabhängigen lokalen/shared-host-Ausführungspfad nicht. Das Finding ist remediation_required und `in_progress`, nicht fixed, verified, closed, committet, geliefert oder gemergt.

## Beobachtetes und erwartetes Verhalten

Der zurückgehaltene Pre-Remediation-Kandidaten-Snapshot besitzt die Root-Control bei `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh:8`, die absolute-only-Control bei `:19–25` und den `mkdir`-/Compiler-Output-/Execution-Sink bei `:82–91`. `OUT` stammt aus `APACHE_RULES_SET_CLEANUP_OUT`, `BUILD_ROOT` oder `/var/tmp/ModSecurity-conector-verified/build/apache-rules-set-cleanup`. `mkdir -p` erhält einen vorbestehenden Baum; der Compiler erzeugt den festen Dateinamen `apache-rules-set-cleanup` und das Skript führt ihn unmittelbar aus. Direkte Host-Evidence erfasst `/var/tmp` als `root:root` mode `1777`, während die vorhersagbaren Projekt-/Build-Parents gewöhnliche mode-`755`-Verzeichnisse sind.

Der aktuelle Parent-Source besitzt dasselbe Muster in `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh` bei Zeilen `8`, `19–25` und `81–89`: Output-Root-Selection, absolute-only-Check, `mkdir -p`, feste `apache-request-transaction-cleanup`-Binary und unmittelbare Ausführung. Jeder Runner muss stattdessen unter einem validierten temporären Parent ein frisches privates mode-`700`-Output-Verzeichnis erzeugen und nur darin kompilieren/ausführen. Ein geerbtes `OUT`, `BUILD_ROOT`, vorhersagbarer Default, bestehendes Verzeichnis, Symlink oder Final-Name-Replacement darf keine Autorität über Compiler-Ausgabe oder Ausführung erhalten.

## Impact, Source-to-Sink-Pfad und Voraussetzungen

```text
niedriger privilegierter lokaler/shared-host-Akteur -> vorhersagbarer sticky-/var/tmp-Output-Baum -> absolute-only-OUT-Control -> mkdir -p erhält attacker-owned Baum -> Compiler schreibt festen Binary-Namen -> Akteur raced Replacement -> Opfer-Skript führt ersetzten Pfad aus
```

Ein erfolgreicher Race kann einen Developer- oder Shared-Runner-Prozess dazu bringen, eine ersetzte lokale Binary unter der Opferidentität auszuführen oder Compiler-Ausgabe umzuleiten. Der Effekt ist für diesen Prozess potenziell hoch, aber der Vektor ist `localhost` und benötigt eine Multi-User-/Shared-Host-Timing-Voraussetzung. Die zurückgehaltene Attack-Path-Analyse kalibriert dies daher als low/P3. Die Evidence belegt weder einen öffentlichen Endpoint noch einen Remote-Exploit, GitHub-PR-/Token-Eskalation, Secret-Zugriff, Fleet-weiten Impact, Connector-Request-Processing-Effekt oder normalen Hosted-CI-Angreiferpfad.

Voraussetzungen sind ein niedriger privilegierter lokaler Akteur, der `/var/tmp` teilt, die Nutzung des vorhersagbaren Defaults oder eines anderweitig kontrollierbaren Output-Roots, ein Precreate/Race vor oder zwischen Compiler-/Linker-Output und Fixed-Name-Execution sowie gewöhnliche Apache/APXS/APR-Voraussetzungen, die den Runner bis zum Sink erreichen lassen.

## Betroffener Scope, Reproduktion und Evidence

- `ci/checks/connectors/apache/check-apache-rules-set-cleanup.sh`: `APACHE_RULES_SET_CLEANUP_OUT`, `BUILD_ROOT`, `OUT`, `mkdir -p`, `apache-rules-set-cleanup` und `BIN`.
- `ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh`: `APACHE_REQUEST_TRANSACTION_CLEANUP_OUT`, `BUILD_ROOT`, `OUT`, `mkdir -p`, `apache-request-transaction-cleanup` und `BIN`.

Den zurückgehaltenen begrenzten Validation- und Attack-Path-Report für den Pre-Remediation-RulesSet-Snapshot lesen, dann den aktuellen Request-Transaction-Sibling inspizieren. Für diese Record-Aufgabe keinen Live-Cross-User-Race ausführen: Er würde unsichere gleichzeitige Manipulation benötigen. Der deterministische Source-to-Sink-Pfad plus der beobachtete sticky Ancestor etablieren die begrenzte lokale/shared-host-Voraussetzung.

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| `validation_report.md` | `05bcf8565c7de8f6fcadf2f607e8266ff762fd5e7296d9434066c78a4eada6f7` | Begrenzter statischer Source-/Config-Trace und Host-Metadaten validieren den lokalen/shared-host-Pfad mit Konfidenz `0.72`; GitHub-PR-/Token-Pfad ist getrennt abwesend. |
| `attack_path_analysis_report.md` | `bf50d4a22613eeccc59d6b99d512e28f2d109c6315d21c097c22bf26f553171f` | Reportable localhost-Process-Execution-Pfad; hoher Effekt pro erfolgreichem Race, niedrige Likelihood, low/P3-Schweregrad. |
| Aktueller Request-Transaction-Sibling | `9c4594c75e8848085de9f7f4b7dcc61f8984a80a106d6351904254683d7a37a5` | Direkte Source-Beobachtung bestätigt die identische bereits bestehende Instanz. |

Der Pre-Remediation-Kandidat ist als `CWE-73`, `CWE-59` und `CWE-367` klassifiziert. Das Live-Candidate-Ledger änderte sich nach der Pre-Remediation-Beobachtung und enthält spätere Remediation-Validation-Daten; es wird deshalb absichtlich von der Acceptance-Evidence dieses Records ausgeschlossen. Die beiden hash-stabilen Berichte oben bestimmen den Finding-Status; dies beansprucht keinen aktuellen Candidate-Fix und ändert den Status `in_progress` nicht.

Die zurückgehaltenen Scan-Artefakte liegen unter `/var/tmp/codex/ModSecurity-conector/runs/selective-apache-prs-master-20260729/security-diff-scan/artifacts/05_findings/cand-apache-rules-set-cleanup-output-confinement/`.

## Root Cause und Remediation-Richtung

Das Runner-Design behandelt einen absoluten Pfad-String als ausreichende Autorität und verwendet ein deterministisches Verzeichnis unter einem sticky Shared-Ancestor wieder. `mkdir -p` etabliert weder Ownership, Frische, Berechtigungen, Non-Symlink-Identität noch eine Post-Link-Bindung. Der Compiler erzeugt danach einen vorhersagbaren Binary-Namen, den das Skript ausführt.

Beide Apache-Cleanup-Runner über einen auditierten Output-Confinement-Vertrag reparieren: Einen validierten temporären Parent wählen, mit `mktemp -d` ein frisches privates mode-`700`-Verzeichnis erzeugen, nur darin kompilieren und ausführen und extern gewählte deterministische Output-Root-Autorität zurückweisen oder entfernen. Negative Source-Contract-Coverage für vorab erzeugten Default oder `BUILD_ROOT`, Symlink und Final-Name-Replacement sowie legitime APR-Compile-/Run-Coverage ergänzen. Workflow-Berechtigungen, Scanner-Exclusions, Quality Gates, Compiler/APXS/APR-Verhalten oder Produktions-Apache-Verhalten nicht abschwächen.

## Akzeptanzkriterien und Validierungsplan

1. Beide Runner erzeugen vor Compiler-Ausgabe unter einem validierten temporären Parent ein frisches privates mode-`700`-Output-Verzeichnis.
2. Ein vorab erzeugter Default, geerbtes `BUILD_ROOT`/`OUT`, Symlink oder Final-Name-Replacement kann die von beiden Runnern aufgerufene Binary weder auswählen noch ersetzen.
3. Beide legitimen Apache/APXS/APR-Harnesses kompilieren und laufen in einer isolierten task-owned Umgebung.
4. Fokussierte Source-Contract-, Negative-Containment-, Legitimate-Control-, Shell-Syntax- und Security-Diff-Checks bestehen ohne Control-Schwächung.
5. Frische Exact-Head-Review- und Hosted-Checks liegen vor jeder Disposition `fixed`, `verified` oder `closed` vor.

Erforderliche Regressionen sind Fresh-Private-Directory-/No-Inherited-Output-Static-Contracts für beide Runner, Preseeded-Root-/Symlink-/Final-Name-Negative-Controls und Shell-Syntax. Legitimate Controls kompilieren und führen die RulesSet- und Request-Transaction-Harnesses mit verifizierten Apache/APXS/APR-Voraussetzungen in frischen task-owned Output-Verzeichnissen aus; normale Hosted-Caller behalten job-lokale Temporary-Roots und read-only Contents-Permissions.

## Deduplizierung, Abhängigkeiten und Restrisiko

Der Request-Transaction-Runner ist kein separates kanonisches Finding. Er hat denselben Parent-Owner, lokalen/shared-host-Source, absolute-only-Output-Root-Control, `mkdir -p`-Erhaltung, Fixed-Binary-Execution-Sink, Security-Invariant und Fresh-Private-Directory-Remediation. Er ist eine verwandte bereits bestehende Instanz dieses Findings. `FND-PARENT-0064` betrifft RulesSet-APR-Lifecycle-Cleanup und `FND-PARENT-0043` betrifft Request-Transaction-Memory-Lifecycle; keines besitzt diese Output-Confinement-/TOCTOU-Execution-Grenze.

Ein Follow-up benötigt einen task-owned Parent-Worktree, einen auditierten Temporary-Parent-Vertrag, Shell-`mktemp`, Apache/APXS/APR/libmodsecurity-Voraussetzungen für die legitimen Controls und frische Exact-Head-Hosted-Evidence. Der versiegelte Bericht bleibt Pre-Remediation-Evidence für den vom Task eingeführten RulesSet-Snapshot; der aktuelle Sibling bleibt ungelöst. Dieser Record beansprucht keinen Source-Fix, keinen Candidate-Current-Source, keinen PR, keinen Hosted-Exact-Head, keinen Merge, kein Master, keine Risikoakzeptanz und keine Schließung.

## Historie

- `2026-07-29T09:42:56Z`: Zurückgehaltene Validation- und Attack-Path-Evidence erzeugte `FND-PARENT-0068` für den lokalen/shared-host-Output-Confinement-Pfad.
- `2026-07-29T09:42:56Z`: Der identische bereits bestehende Request-Transaction-Runner wurde in dieses kanonische Finding dedupliziert, statt eine zweite ID zu erhalten.
- `2026-07-29T10:04:18Z`: Das veränderliche Post-Observation-Candidate-Ledger wurde von der Acceptance-Evidence ausgeschlossen; das Finding bleibt `in_progress`.
