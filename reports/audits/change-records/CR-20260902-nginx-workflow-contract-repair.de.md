# Change Record: NGINX-Workflow-Contract-Reparatur

**Sprache:** [English](CR-20260902-nginx-workflow-contract-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260902-nginx-workflow-contract-repair |
| Datum (UTC) | 2026-09-02 |
| Basis-Revision | 8743fceeb708c06329c14ac00a1f333945edf1d7 |
| Delivery-Status | Der Benutzer autorisierte eine Parent-only-Reparatur in einem eigenen Worktree und einen Draft PR. Commit, Push, PR-Erstellung, Exact-Head-Hosted-Checks und SonarQube-Cloud-Evidence stehen noch aus. Kein Merge, direkter master-Write, Force-Aktion, Bypass oder Auto-Merge ist autorisiert. |

## Motivation und Problemstellung

Fünf aktuelle master-Workflows—test-common, lint, test-apache,
quick-framework-check und test-nginx—stoppten am selben
make check-nginx-common-adoption Source-Contract-Fehler. Der Pre-Patch-Check
beendete sich mit Exit 2 und meldete zwei veraltete Assertions: Der
Response-Mapper-Guard lag nicht mehr inline in
ngx_http_modsecurity_body_filter, und die Seen-Byte-Buchhaltung nutzte nicht
mehr ctx->response_body_bytes_seen += len.

Der laufende NGINX-Code bleibt absichtlich korrekt:
ngx_http_modsecurity_prepare_response_body_filter besitzt Eligibility und
Mapper-Reihenfolge, während ngx_http_modsecurity_plan_limited_response_body den
Common-Body-Limit-Plan für plan.bytes_seen verwendet. Diese Reparatur richtet
den Checker an diesen laufenden Grenzen aus, statt Request- oder
Response-Verarbeitung zu ändern.

## Akzeptanzkriterien

- make check-nginx-common-adoption besteht und prüft die laufenden
  Helper-Grenzen statt der obsoleten Inline-Form.
- Der Checker verlangt weiterhin Once-only-, non-fatal-Mapper-Validierung nach
  den Context- und Phase-4-Eligibility-Guards.
- Der Checker verlangt weiterhin einen In-Scope-Guard vor der
  Response-Body-Ingestion und Common-Plan-Zuweisung von
  ctx->response_body_bytes_seen.
- Bestehende NGINX-Upstream-Security-Contracts und CI-Security-Workflow-
  Contracts bestehen ohne Suppression, Permission-Änderung, Scanner-Änderung
  oder Control-Lockerung.
- Ein Task-Branch und Draft PR werden erst nach Exact-Head-Review geliefert;
  diese Aufgabe führt keinen Merge aus.

## Implementierungsentscheidung und Begründung

Die Änderung ergänzt extrahierte statische Ansichten der laufenden
Preparation-, Body-Limit- und Chain-Append-Helper in
ci/checks/connectors/nginx/check-nginx-common-adoption.py. Sie prüft, dass der
Top-Level-Body-Filter an die Preparation delegiert; dass Preparation die Null-
und Intervention/Processed-Guards vor dem Mapper-Once-Helper ausführt; dass
Chain-Append vor Body-Ingestion für eine Out-of-Scope-Phase-4-Response
zurückkehrt; und dass der Common-Plan plan.bytes_seen bucht.

Es ändern sich keine NGINX-C-Source, Workflow-YAML, Action-Pins,
Job-Permissions, Trigger, Credentials, Dependencies, Framework-Source,
MRTS-Source, Gitlink-, Scanner- oder Quality-Gate-Konfiguration.

## Security-Auswirkung

Der betroffene Check beschreibt Response-Body-Inspektion, eine ausdrücklich
sicherheitsrelevante Grenze. Die Reparatur bewahrt non-fatal Mapper-Warnungen,
Once-only-Validierung, Phase-4-Scope-Guard und Common-Reject-Plan-Buchhaltung.
Sie erweitert weder einen Workflow-Token noch ändert sie eine Runtime-
Sicherheitsentscheidung.

Der Codex-Security-Scan des Parent-.github-Scopes fand keinen validierten High-
oder Critical-Severity-Befund. Die überprüften SARIF-Upload-Jobs behalten die
absichtlich allowlisteten contents: read plus security-events: write
Berechtigungen, die für Uploads benötigt werden; hier wird keine Workflow-Datei
geändert.

## Geänderte Dateien

- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.md
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch rtk proxy make check-nginx-common-adoption | Fehler reproduziert: Exit 2 mit genau den veralteten Mapper- und Seen-Byte-Assertions. |
| Post-Patch rtk proxy make check-nginx-common-adoption | Bestanden. |
| Kombinierte NGINX-Upstream-Security- und CI-Security-Workflow-Tests | Bestanden: 44 Tests. |
| Python-Kompilierung des geänderten Checkers | Bestanden. |
| rtk proxy git diff --check | Bestanden. |
| Codex-Security-Standard- und Post-Patch-Diff-Scans | Beide versiegelten Reports validieren mit vollständiger Abdeckung und 0 reportierbaren Findings. |
| make check-bilingual-docs | Nur durch 20 vorbestehende fehlende Framework-Gitlink-Targets blockiert; kein aktueller Change-Record-Pfad wurde gemeldet. |
| make check-doc-links / Repository-Path-Reference-Check | Nur durch denselben fehlenden Framework-Checkout und seine vorbestehenden Targets blockiert. |
| make lint | Erreichte Host-Runtime-Preflight und stoppte dann am fehlenden Framework-No-CRS-Baseline-Katalog; keine Framework-Initialisierung oder -Änderung war autorisiert. |
| Exact-Head-Hosted- und SonarQube-Cloud-Checks | Bis zur normalen Draft-PR-Delivery ausstehend. |

## Runtime-Evidence

Die Reparatur ist eine Source-Contract-Ausrichtung. Es wurde keine NGINX-
Runtime gestartet, kein Request- oder Response-Payload aufbewahrt und kein
privilegierter, geschützter oder Maintenance-Workflow dispatcht. Frische
Exact-Head-Hosted-Evidence bleibt nach PR-Lieferung nötig.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständigen Dokumentations- und Lint-Controls können in diesem Worktree
nicht abschließen, weil `modules/ModSecurity-test-Framework` nicht ausgecheckt
ist. Die beobachteten Dokumentationsfehler nennen ausschließlich fehlende
Framework-Targets, und Lint stoppt nach seinem verfügbaren lokalen Preflight am
Framework-No-CRS-Baseline-Katalog. Aus dieser Parent-only-Anfrage wird keine
Framework-Initialisierung, Dependency-Installation oder repository-übergreifende
Änderung abgeleitet. Vollständige Connector-Runtime-Matrizen und make quick-check
liegen außerhalb des Scopes der Checker-Reparatur.

## Bekannte Einschränkungen

Die lokale Validierung belegt den statischen Contract und die bestehenden
NGINX-Source-Security-Tests, nicht einen nativen NGINX-Build oder einen End-to-
End-Response-Flow. Das aktive Parent-Ruleset und Hosted-Workflow-Ausführung
bleiben externe Controls, die am exakten PR-Head beobachtet werden müssen.

SonarQube Cloud meldet aktuell ein bestandenes Quality Gate für die
Basisrevision, aber sieben historische projektweite offene Issues bleiben,
einschließlich eines Framework-eigenen Issues außerhalb dieser Parent-only-
Authority. Literales projektweites Zero benötigt daher eine User-Scope-
Entscheidung; kein Issue wird durch diese Änderung verborgen, unterdrückt oder
als False Positive markiert.

## Verbleibende Risiken

Der Checker wird absichtlich fehlschlagen, wenn ein künftiger Refactor die
extrahierten Helper-Beziehungen oder die erforderlichen Guards und Common-Plan-
Zuweisung entfernt. Hosted CI kann nach PR-Erstellung einen unabhängigen
Environment- oder Integrationsfehler zeigen. Diese Aufgabe behauptet nicht,
dass die sieben historischen SonarQube-Cloud-Issues gelöst sind.

## Finaler Diff- und Review-Status

Der finale lokale Diff-Check, fokussierte Source-Contract-Controls, kombinierte
Security-Contracts, Python-Kompilierung sowie versiegelte Codex-Security-
Standard-/Diff-Scans bestanden; beide Scans haben 0 reportierbare Findings.
Dokumentations-Controls sind nur durch den fehlenden Framework-Checkout
blockiert. Commit, Push, Draft-PR-Erstellung, Exact-Head-GitHub-Actions-Checks
und Exact-Head-SonarQube-Cloud-Analyse bleiben nötig. Kein Merge ist autorisiert.
