# Change Record: NGINX-Workflow-Contract-Reparatur und Envoy-gRPC-Sicherheitsupdate

**Sprache:** [English](CR-20260902-nginx-workflow-contract-repair.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260902-nginx-workflow-contract-repair |
| Datum (UTC) | 2026-09-02 |
| Basis-Revision | 8743fceeb708c06329c14ac00a1f333945edf1d7 |
| Delivery-Status | Der erste Reparatur-Commit wurde normal gepusht und erstellte Draft PR #351; dessen erster exakter Head bestand alle gemeldeten Hosted-Checks und SonarClouds PR-Quality-Gate mit null PR-Issues. Eine während dieser Delivery entdeckte High-Severity-Runtime-Dependency-Remediation wird nun demselben Draft PR hinzugefügt und benötigt frische Exact-Successor-Evidence. Kein Merge, direkter master-Write, Force-Aktion, Bypass oder Auto-Merge ist autorisiert. |

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

Während der normalen Draft-PR-Delivery meldete GitHub den offenen Dependabot-
Alert #3: `GHSA-vp52-pcj8-j9qc` / `CVE-2026-84304`. Die direkt aufgelöste
Envoy-ext_proc-Runtime-Dependency `google.golang.org/grpc v1.82.1` liegt im
betroffenen Bereich bis v1.83.0; v1.83.1 ist die erste gepatchte Version. Ein
unabhängiges Boundary-Review bestätigte, dass produktive Standalone- und
Composite-Server grpc-go vor Anwendungslimits für Body/Nachricht verwenden;
deshalb ist das enge Sicherheitsupdate für eine sichere Delivery erforderlich.

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
- Envoy ext_proc löst grpc-go v1.83.1 mit seinem vollständigen tidy-
  Modulgraphen auf; der Security-Floor-Contract verwirft das frühere v1.82.1-
  Minimum.
- Readonly-Modulverifikation, Tests, Build und Vet bestehen mit task-eigenen
  Caches; bestehende Listener-, Nachrichtengrößen-, Stream- und UDS-
  Schutzmaßnahmen bleiben unverändert.
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
Job-Permissions, Trigger, Credentials, Framework-Source, MRTS-Source,
Gitlink-, Scanner- oder Quality-Gate-Konfiguration. Die einzige Dependency-
Änderung ist die direkte Envoy-grpc-go-Sicherheitsremediation und die vom Go-
Tool verlangte tidy-Graph-Anpassung: grpc-go v1.83.1, dessen Prüfsumme, das
von grpc-go ausgewählte genproto-RPC-Requirement samt Prüfsumme, das bereits
ausgewählte direkte x/sys-Requirement und transitiv ausgewählte OpenTelemetry-
1.44-Prüfsummen.

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

FND-PARENT-1011 erfasst das High-Severity-gRPC-Dependency-Finding. Der Patch
hebt nur das direkte Requirement, vollständige aufgelöste Prüfsummen, den
semantischen CI-Floor und die gepaarte Modul-Dokumentation auf v1.83.1 an. Er
behauptet nicht, dass Connector-Nachrichtenlimits, Loopback-Konfiguration oder
die UDS-Autorisierung des Response Observers den Upstream-Transportfix ersetzen.

## Geänderte Dateien

- ci/checks/connectors/nginx/check-nginx-common-adoption.py
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.md
- reports/audits/change-records/CR-20260902-nginx-workflow-contract-repair.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md
- connectors/envoy/ext_proc/go.mod
- connectors/envoy/ext_proc/go.sum
- connectors/envoy/ext_proc/README.md
- connectors/envoy/ext_proc/README.de.md
- tests/test_ci_security_workflows.py

## Ausgeführte Befehle

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Pre-Patch rtk proxy make check-nginx-common-adoption | Fehler reproduziert: Exit 2 mit genau den veralteten Mapper- und Seen-Byte-Assertions. |
| Post-Patch rtk proxy make check-nginx-common-adoption | Bestanden. |
| Kombinierte NGINX-Upstream-Security- und CI-Security-Workflow-Tests | Bestanden: 44 Tests. |
| Python-Kompilierung des geänderten Checkers | Bestanden. |
| rtk proxy git diff --check | Bestanden. |
| Codex-Security-Standard- und Post-Patch-Diff-Scans | Beide versiegelten Reports validieren mit vollständiger Abdeckung und 0 reportierbaren Findings. |
| gRPC-Pre-Patch-Dependency- und Transport-Boundary-Triage | Dependabot #3, direkte v1.82.1-Auflösung, produktive Servergrenze und v1.83.1 als erste gepatchte Version bestätigt. |
| go mod tidy -diff | Nach der vollständigen notwendigen grpc-go-Modulgraph-Anpassung bestanden. |
| go mod verify | Bestanden: alle Module verifiziert. |
| go test -mod=readonly ./... | Bestanden: alle acht Envoy-ext_proc-Packages. |
| go build -mod=readonly -buildvcs=false ./... | Bestanden; `-buildvcs=false` ist nur nötig, weil die Sandbox Go den Lesezugriff auf VCS-Stamping-Metadaten verweigert. |
| go vet -mod=readonly ./... | Bestanden. |
| Unabhängiges Codex-Security-Bypass-/Regression-Review | Bestanden: kein verbliebener vulnerabler Auflösungsweg oder Regression legitimen Verhaltens validiert; `GOWORK=off`-Modulverifikation und vollständige Modullisten-Evidenz bestanden. |
| make check-bilingual-docs | Nur durch 20 vorbestehende fehlende Framework-Gitlink-Targets blockiert; kein aktueller Change-Record-Pfad wurde gemeldet. |
| make check-doc-links / Repository-Path-Reference-Check | Nur durch denselben fehlenden Framework-Checkout und seine vorbestehenden Targets blockiert. |
| make lint | Erreichte Host-Runtime-Preflight und stoppte dann am fehlenden Framework-No-CRS-Baseline-Katalog; keine Framework-Initialisierung oder -Änderung war autorisiert. |
| First-Draft-PR-#351-Exact-Head-Hosted-Checks und SonarCloud-PR-Analyse | Vor der gRPC-Remediation bestanden; Successor-Head-Evidence bleibt erforderlich. |

## Runtime-Evidence

Die Reparatur ist eine Source-Contract-Ausrichtung. Es wurde keine NGINX-
Runtime gestartet, kein Request- oder Response-Payload aufbewahrt und kein
privilegierter, geschützter oder Maintenance-Workflow dispatcht. Frische
Exact-Head-Hosted-Evidence bleibt nach PR-Lieferung nötig.

Die Dependency-Remediation startet ebenfalls keinen Connector-Listener und
behält keinen Traffic. Sie belegt Modulintegrität und Source-Level-
Kompatibilität durch Readonly-Tests, Build und Vet des Moduls, statt einen
Availability-Angriff gegen gRPC-Transportpufferung auszuführen.

## Nicht ausgeführte Prüfungen mit Begründung

Die vollständigen Dokumentations- und Lint-Controls können in diesem Worktree
nicht abschließen, weil `modules/ModSecurity-test-Framework` nicht ausgecheckt
ist. Die beobachteten Dokumentationsfehler nennen ausschließlich fehlende
Framework-Targets, und Lint stoppt nach seinem verfügbaren lokalen Preflight am
Framework-No-CRS-Baseline-Katalog. Aus dieser Parent-only-Anfrage wird keine
Framework-Initialisierung, Dependency-Installation oder repository-übergreifende
Änderung abgeleitet. Vollständige Connector-Runtime-Matrizen und make quick-check
liegen außerhalb des Scopes der Checker-Reparatur. Für die gRPC-Änderung gibt
es keinen geeigneten sicheren lokalen Exploit-Replay; stattdessen werden das
authentifizierte Advisory, der Auflösungsnachweis und Standard-Modul-Controls
verwendet.

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

Der Dependabot-Alert des Default-Branches bleibt bis zu einem autorisierten
Merge offen. Dieser Task kann den PR-Successor-Head validieren, aber weder eine
Default-Branch-Remediation behaupten noch den Merge durchführen.

## Verbleibende Risiken

Der Checker wird absichtlich fehlschlagen, wenn ein künftiger Refactor die
extrahierten Helper-Beziehungen oder die erforderlichen Guards und Common-Plan-
Zuweisung entfernt. Hosted CI kann nach PR-Erstellung einen unabhängigen
Environment- oder Integrationsfehler zeigen. Diese Aufgabe behauptet nicht,
dass die sieben historischen SonarQube-Cloud-Issues gelöst sind. Das direkt
remedierte gRPC-Transportrisiko bleibt auf master vorhanden, bis der Draft PR
reviewt ist und ein autorisierter Akteur ihn merget; ein solcher Merge liegt
außerhalb der aktuellen Delivery-Autorisierung.

## Finaler Diff- und Review-Status

Die ursprüngliche Workflow-Reparatur ist committed, gepusht und als Draft PR
#351 eröffnet; deren erster exakter Head bestand die Hosted-Checks und das
SonarCloud-PR-Quality-Gate mit null Issues. Der kombinierte Successor-Diff
bestand fokussierte NGINX-Controls, 44 Python-Security-Contract-Tests,
Readonly-Go-Modulvalidierung/Tests/Build/Vet und den tidy-Diff-Control.
Dokumentations-Controls bleiben nur durch den fehlenden Framework-Checkout
blockiert. Das unabhängige Codex-Security-Bypass-/Regression-Review bestand;
Immutable-Commit-Diff-Scan, normaler Push und Exact-Successor-Hosted-/SonarCloud-
Evidence bleiben erforderlich. Kein Merge ist autorisiert.
