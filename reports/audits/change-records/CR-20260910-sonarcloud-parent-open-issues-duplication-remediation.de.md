# Change Record CR-20260910-sonarcloud-parent-open-issues-duplication-remediation: Parent-SonarCloud-Qualitätsremediation

**Sprache:** [English](CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260910-sonarcloud-parent-open-issues-duplication-remediation |
| Datum (UTC) | 2026-09-10 |
| Basis-Revision | 26a560e64cbaf906c0d35bba199f65436830d1dd |
| Scope | Nur Parent-ModSecurity-Connector; keine Framework-, MRTS-, Gitlink-, Scanner-, Regel-, Quality-Gate-, Suppression-, Exclusion- oder Merge-Änderung |
| Delivery-Status | PR #361 ist OPEN, kein Draft und hat Exact-Source-Head-Evidenz bei `963468c0c1ca43e4c8708e57e6c2ad87465a6faf`; dieser reine Dokumentationsabgleich benötigt einen finalen Successor-Head-Readback. Ein Merge ist nicht autorisiert. |
| Policy-Auflösung | Die Parent-Traceability-Policy verlangt diesen gepaarten Change Record für eine nicht triviale versionierte Produktänderung. Er verwendet den etablierten Archivpfad; kein paralleles Format oder Index wird eingeführt. |

## Motivation und Problemstellung

Der Nutzer verlangte die Remediation der 113 offenen SonarCloud-Issues und der
0,3-%-Duplizierungsmetrik mittels PR, beschränkt auf den ModSecurity Connector.
Die aktuelle authentifizierte Baseline-Evidenz enthält 113 OPEN CODE_SMELL-
Records: 112 Parent-eigene Records und einen Framework-eigenen Record. Der
Parent-Code benötigt echte verhaltensbewahrende Maintainability-Refaktoren statt
Scanner-Umgehungen.

## Akzeptanzkriterien

1. Ausschließlich Parent-eigene Connector-Source-, Test- und Traceability-
   Änderungen ausliefern.
2. Runtime-, Parser-, Prozess-, Dateisystem-, Protokoll-, Serialisierungs-,
   Timeout-, Ownership-, Cleanup- und Fail-Closed-Controls erhalten.
3. Kein NOSONAR, keine akzeptierten Issues, Exclusions, Scanner-/Regel-/
   Quality-Gate-Änderungen, gelöschten Tests oder abgeschwächten Assertions
   verwenden.
4. Den unveränderlichen exakten PR-Head mit SonarCloud-Issue-, Duplikat- und
   Quality-Gate-Readback sowie anwendbaren GitHub-Checks verifizieren.
5. Das separat besessene Framework-Issue und die repositoryübergreifenden
   Duplikatblöcke explizit berichten statt ein unbeobachtetes projektweites
   Nullergebnis zu behaupten.

## Implementierungsentscheidung und Begründung

- Die identifizierten Parent-Code-Smell-Gruppen werden an Ort und Stelle
  refaktoriert: kognitive Komplexität, Parameteranzahlen, verschachtelter
  Kontrollfluss, doppelte Literale, Exception-Kontexte und echte doppelte
  Kontroll-/Testblöcke.
- Eng abgegrenzte Helpers werden nur extrahiert, wenn sie bestehendes
  öffentliches Verhalten und Security-Controls erhalten; Connector-spezifische
  Tests bleiben bestehen statt einer generischen Abschwächung oder Löschung.
- Framework, MRTS, Gitlinks, SonarCloud-Projektsettings, Regeln und Quality
  Gate bleiben unverändert. Das eine Framework-Issue wird durch FND-SONAR-0004
  verfolgt.
- Die 820 bekannten Parent/Framework-Geschwister-Duplikatzeilen werden als
  FND-CROSS-0010 behandelt. Ein Parent-only-PR kann eigene echte
  Duplikatblöcke reduzieren, aber repositoryübergreifenden Content ohne
  getrennte Autorisierung und Delivery-Lifecycle nicht entfernen.
- Eine lokale Sonar-Vortex-Analyse war für die Organisation nicht verfügbar.
  Die maßgebliche Closure-Evidenz ist daher die spätere SonarCloud-Analyse des
  exakten PR-Heads, nicht ein ersetztes lokales Scanner-Ergebnis.

## Security-Auswirkung

Die Änderung berührt security-sensitive Event-Serialisierung, HTTP-/SPOA-
Protokollbehandlung, Subprocess-Supervision, PID-/Descriptor-Identität,
Dateisystem-Evidence-Publikation, native CGo-Bereinigung und
Loopback-Control-Pfade. Die Implementierung erhält JSON-Escaping,
Provenance-Grenzen, URI-Query-Redaction, Frame-Grenzen, Deadlines,
Loopback-Binding, PID-Reuse- und Peer-Prüfungen, O_NOFOLLOW-
Descriptor-Walks, Cleanup-Ownership und Fail-Closed-Verhalten.

Der formelle Security-Diff-Scan deckt den lokalen 28-Dateien-Parent-Diff
vollständig ab, meldet null berichtspflichtige Findings und liegt unter:

/var/tmp/codex/ModSecurity-conector/runs/sonarcloud-open-issues-duplication-20260910/security-diff-scan/report.md

Seine SHA-256 ist bdb80964abee0fc33154133762fb289f3611d0e9d2b6652db8083c0660a707e7.
Es wurde keine Deployment-Runtime ausgeführt.

## Geänderte Dateien

- ci/checks/connectors/apache/check-apache-common-adoption.py
- ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py
- ci/checks/documentation/connector_config_reference.py
- ci/runtime/lifecycle/with-crs-no-mrts-profile.py
- common/src/event.c
- common/src/json_escape.c
- connectors/apache/harness/apache_process_guard.py
- connectors/apache/harness/run_apache_smoke.sh
- connectors/envoy/ext_proc/internal/processor/common_runtime_engine.go
- connectors/envoy/ext_proc/internal/processor/processor.go
- connectors/envoy/ext_proc/internal/processor/processor_test.go
- connectors/haproxy/harness/run_haproxy_spop_cache_miss.sh
- connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c
- connectors/lighttpd/harness/lighttpd_backend_close_linux_guard.py
- connectors/lighttpd/harness/lighttpd_backend_close_probe.py
- connectors/lighttpd/harness/lighttpd_stock_lifecycle_probe.py
- connectors/lighttpd/harness/run_lighttpd_backend_close.sh
- connectors/lighttpd/harness/run_lighttpd_stock_lifecycle.sh
- connectors/lighttpd/tests/test_backend_close_harness_contract.py
- connectors/nginx/harness/run_nginx_smoke.sh
- connectors/traefik/native_middleware/engine_uds_test.go
- connectors/traefik/native_middleware/middleware_test.go
- tests/http_authorization_service_detached_worker_smoke.c
- tests/http_authorization_service_peer_close_smoke.c
- tests/test_apache_with_crs_profile_evidence_contract.py
- tests/test_apache_smoke_case_output_root.py
- tests/test_event_runtime_security_contract.py
- tests/test_haproxy_spop_peer_isolation_contract.py
- tests/test_haproxy_spop_selftest_cleanup_contract.py
- tests/test_haproxy_spop_sigpipe_peer_isolation_contract.py
- tests/test_protected_nginx_broker_caller.py
- tests/test_sonar_reliability_contract.py
- tests/_haproxy_spop_contract_helpers.py
- reports/audits/change-records/CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.md
- reports/audits/change-records/CR-20260910-sonarcloud-parent-open-issues-duplication-remediation.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

## Tests und tatsächliche Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| make check-haproxy-c17 | Bestanden |
| make check-haproxy-common-adoption | Bestanden |
| make check-common-helpers-c17 mit task-eigenem BUILD_ROOT | Bestanden |
| make check-connector-config-reference | Bestanden |
| make check-http-authorization-service-timeout mit task-eigenem BUILD_ROOT | Bestanden |
| Offline-Envoy go test ./... mit GOPROXY=off | Bestanden |
| Offline-Traefik go test ./... mit GOPROXY=off | Bestanden |
| Apache-Process-Guard-Suite | Bestanden: 58 Tests |
| Lighttpd-Backend-Close-Contract | Bestanden: 57 Tests |
| Lighttpd-Stock-Lifecycle-Contract | Bestanden: 11 Tests |
| With-CRS/no-MRTS-Profile-Suite | Bestanden: 23 Tests |
| HAProxy-Cleanup plus NGINX-Broker-Contracts | Bestanden: 15 Tests |
| Event-Runtime-Security-Contract | Bestanden: 7 Tests |
| Shell-Syntaxprüfungen für fünf geänderte Shells | Bestanden |
| gofmt -d für geänderte Go-Pfade | Bestanden; keine Ausgabe |
| git diff --check gegen Basis | Bestanden |
| Formeller Security-Diff-Scan | Bestanden; vollständige Abdeckung, null berichtspflichtige Findings |
| Finaler Security-Diff-Scan des zweiten Zyklus | Bestanden; vollständige Abdeckung, null berichtspflichtige Findings |
| Finaler Security-Diff-Scan der Testdeduplikation im dritten Zyklus | Bestanden; vollständige Abdeckung, null berichtspflichtige Findings |
| Finaler HAProxy-Helper-/Peer-/SIGPIPE-/Self-Test-/Sonar-Reliability-Vertragslauf | Bestanden: 48 Tests |
| Finale Python-Kompilierung des Helpers und seiner zwei Verbraucher | Bestanden |
| Isolierter Apache-Parent-SIGKILL-Kandidat-/Baseline-Recheck | Bestanden: 1,395s Kandidat, 1,327s Baseline |

Das intermittierende frühere Apache-Parent-SIGKILL-Timeout wird als
FND-PARENT-1084 verfolgt. Es wurde gegen Kandidat und Baseline beobachtet und
reproduzierte sich nicht in aktuellen isolierten Rechecks; kein Timeout und
keine Assertion wurde abgeschwächt.

## Runtime-Evidence

Es wurde keine produktive Connector-Deployment-Runtime ausgeführt. Fokussierte
Test-Fixtures üben nur lokale Prozess-, Protokoll- und Lifecycle-Controls aus
und werden nicht als Deployment- oder Protected-Host-Evidenz dargestellt. Der
abgeschlossene statische Security-Diff-Scan und fokussierte
Regressions-/Control-Suiten sind die verfügbare lokale Evidenz.

## Nicht ausgeführte Prüfungen mit Begründung

- Exact-Source-Head-SonarCloud-Quality-Gate-, OPEN/CONFIRMED-Issue- und
  Duplikat-Readback: Bestanden am Source-Head
  `963468c0c1ca43e4c8708e57e6c2ad87465a6faf` (Analysezeitpunkt
  `2026-09-10T11:04:34+0000`): Quality Gate `OK`, null Parent-
  OPEN/CONFIRMED-Issues, null neue Duplikatzeilen/-blöcke sowie eine
  Aggregatreduktion von 2.146/92 auf 1.919/81. Der normale reine
  Dokumentations-Successor benötigt weiterhin denselben Exact-Head-Readback.
- Exact-finaler-Dokumentations-Head-GitHub-Actions-Checks: Der normale
  Dokumentations-Follow-up benötigt nach dem Push seinen eigenen finalen
  Readback.
- Default-Branch-Post-Merge-SonarCloud-Metrik: Kein Merge ist autorisiert.
- Lokale Sonar-Vortex-Analyse: Für die Organisation nicht verfügbar.
- Ein Apache-With-CRS-Profile-Publication-Test: Blockiert, weil dem isolierten
  Parent-Worktree die separat besessene Framework-Case-CLI fehlt. Framework-
  Content und Gitlink wurden nicht hydriert oder geändert.
- Vollständiges ShellCheck: Blockiert durch vorbestehende Warnungen in
  unveränderten Apache-/NGINX-Zeilen; keine Warnung wurde unterdrückt.
- make check-bilingual-docs und make check-doc-links: Nach dem gepaarten Record
  und den Archivindex-Updates ausgeführt. Beide sind ausschließlich durch
  bestehende Links zu Zielen unter dem nicht materialisierten Framework-Gitlink
  blockiert; keiner meldet einen Change-Record-Überschriften- oder
  Sprachpaarfehler.

## Bekannte Einschränkungen

Die Default-Baseline hat ein Framework-eigenes OPEN-Issue:
AaA34UWlbqrRc02noCI3, python:S1192, bei
modules/ModSecurity-test-Framework/ci/checks/catalog/five_connectors_with_crs_no_mrts.py:112.
Es kann in dieser Parent-only-Aufgabe nicht behoben werden.

Das Baseline-Aggregat beträgt 2.146 duplizierte Zeilen, 92 Blöcke, 696.956
NCLOC und 0,3 % Dichte. 820 bekannte Parent/Framework-Geschwisterzeilen liegen
außerhalb des autorisierten Scopes. Ein PR kann nur Exact-Head-New-Code-/
task-eigene Ergebnisse beweisen; eine Default-Branch-Projektmetrik benötigt
einen späteren autorisierten Merge und eine Resulting-Master-Analyse.

## Verbleibende Risiken

Bis Exact-PR-Head-SonarCloud-Analyse und CI abgeschlossen sind, kann ein
verbleibendes lokales Issue, ein Duplikatblock oder eine Integrationsregression
entdeckt werden. Die Scope-Einschränkung ist nicht risikoakzeptiert:
Framework-Ownership und repositoryübergreifende Duplizierung bleiben explizite
Blocker für ein wörtliches projektweites Nullergebnis.

## Delivery-Abgleich vor dem finalen Dokumentations-Follow-up — 2026-09-10

- Branch: `agent/sonarcloud-open-issues-duplication-20260910`.
- Initialer Source-und-Record-Commit:
  `ed78748e15cafda884ae819482f91e7d3f7c7d9e`
  (`fix: remediate Parent SonarCloud quality issues`).
- Follow-up-Source-Commits:
  `920f478f5c894bc9b51a12686aef10b43b829afc`
  (`fix: resolve remaining SonarCloud issues`),
  `982b7d908f82f99680341cfab152ed8cc9062903`
  (`fix: clear final SonarCloud residuals`) und
  `963468c0c1ca43e4c8708e57e6c2ad87465a6faf`
  (`test: deduplicate HAProxy SPOP contract assertions`).
- Lokaler, Remote- und PR-Source-Head stimmten beim finalen Source-Readback
  mit `963468c0c1ca43e4c8708e57e6c2ad87465a6faf` überein.
- Pull Request: [#361](https://github.com/Easton97-Jens/ModSecurity-conector/pull/361)
  gegen `master`; er war OPEN und kein Draft.
- Der Source-Head ist mergeable mit `mergeStateStatus` `BLOCKED`, während
  Hosted-Checks laufen; keine Review-Entscheidung und kein Merge werden
  verzeichnet.
- Die SonarCloud-Analyse des exakten Source-Heads ist `OK` mit null Parent-
  OPEN/CONFIRMED-Issues, null neuen Duplikatzeilen/-blöcken und einer
  Aggregatduplikatreduktion von 227 Zeilen / 11 Blöcken. Die angezeigte
  Aggregatdichte bleibt wegen Rundung bei 0,3 %.
- Dieser Abgleich wird als normaler reiner Dokumentations-Follow-up ohne Amend,
  Force-Push oder Merge ausgeliefert. Sein exakter Successor-Head und seine
  Hosted-Ergebnisse müssen nach dem Push noch abgeglichen werden.

## Finaler Diff- und Review-Status

Lokale Source-, Test-, Formatter-, Diff- und Security-Reviews sind für den hier
beschriebenen Kandidaten abgeschlossen. Der exakte Source-Head erfüllt die
task-eigenen SonarCloud-Issue- und New-Duplication-Kriterien. Dieser
Dokumentationsabgleich wird ein normaler Follow-up-Commit; sein exakter finaler
PR-Head, Hosted-Check-Ergebnisse, SonarCloud-PR-Ergebnis, Review-Runde, Merge
und Cleanup-Ergebnis stehen noch aus. Eine Merge-Autorisierung wird nicht
behauptet.
