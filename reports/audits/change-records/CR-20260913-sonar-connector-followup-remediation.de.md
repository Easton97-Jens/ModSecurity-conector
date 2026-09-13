# Change Record CR-20260913-sonar-connector-followup-remediation: Parent-Connector-Sonar-Follow-up-Remediation

**Sprache:** [English](CR-20260913-sonar-connector-followup-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260913-sonar-connector-followup-remediation |
| Datum (UTC) | 2026-09-13 |
| Basis-Revision | `7b61b262332be8c89275542c1fa22d6ecb1f57e2` |
| Scope | Ausschließlich Parent-ModSecurity-Connector-Source, direkt betroffene Tests und dieser gekoppelte Traceability-Record. Keine Framework-, MRTS-, Gitlink-, Scanner-, Regel-, Quality-Gate-, Suppression-, Exclusion-, Dependency- oder Workflow-Änderung. |
| Delivery-Status | Offener PR [#368](https://github.com/Easton97-Jens/ModSecurity-conector/pull/368) auf `agent/sonar-connector-followup-20260913`; sein erster veröffentlichter Head war `2e27799d15e6789aaa89887c6a8ca18a67a01f42`. Dieser Head bestand das Quality Gate mit null neuen Duplikatzeilen/-blöcken, zeigte aber drei neue C-Issues. Die korrigierende lokale Source-/Dokumentationsaktualisierung ist uncommittet und benötigt einen zweiten Commit, normalen Push und einen vollständigen Exact-Head-Verifikationszyklus. |
| Policy-Auflösung | Die Parent-Traceability-Policy verlangt dieses englisch/deutsche Change-Record-Paar für die nicht triviale versionierte Remediation. Die Archiv-README wird als etablierter Index aktualisiert. |

## Motivation und Problemstellung

Frische wrapper-authentifizierte SonarQube-Cloud-Evidenz für Resulting-Master
`7b61b262` meldete 17 OPEN-Records: 16 Parent-eigene Records in zehn Dateien
und einen separat besessenen Framework-Record. Der Nutzer autorisierte einen
Parent-only-Follow-up-PR zur Remediation der Connector-Findings. Die Änderungen
müssen die Parent-Findings durch verhaltensbewahrende Wartungsarbeit statt durch
Analyse-Umgehungen entfernen.

## Akzeptanzkriterien

1. Alle 16 aktuellen Parent-Sonar-Findings erfassen und beheben, ohne Analyse
   oder Controls zu unterdrücken, zu akzeptieren, auszuschließen oder zu
   schwächen.
2. Parser-Grenzen, Prozess-/Datei-Ownership, Event-Serialisierung,
   Protokoll-Frame-Limits, Timeout-, Cleanup-, Restart- und Fail-Closed-
   Verhalten erhalten.
3. Framework, MRTS, Gitlink, Projekteinstellungen, Regeln, Quality Gate,
   Dependencies und Workflows unverändert lassen.
4. Fokussierte lokale Controls, den finalen Scoped-Security-Diff und den
   exakten PR-Head mit SonarQube Cloud und den erforderlichen GitHub-Checks
   verifizieren.
5. Das verbleibende Framework-Issue und die Grenzen der Aggregatduplikation
   ehrlich berichten statt ein unbeobachtetes projektweites Nullergebnis zu
   behaupten.

## Implementierungsentscheidung und Begründung

- Begrenzte Helper-Extraktionen für die C- und Python-Pfade mit kognitiver
  Komplexität anwenden und ihre bestehende Validierung, Ownership, Bereinigung
  und ihr Fehlerverhalten erhalten.
- Ausschließlich die redundanten Apache-Literal-/Exception-Konstrukte und
  mehrdeutigen Go-Parameternamen ersetzen; öffentliche Interfaces, Limits und
  Verhalten bleiben unverändert.
- Den HAProxy-Production-Notify-Task-Allocation-Pfad konsolidieren, wodurch
  ein aktueller Parent-Duplikatblock ohne breite metrikgetriebene Refaktorierung
  entfernt wird.
- Die neu gemeldete lange Parameterliste des Helpers durch den bereits
  initialisierten Production-Result-Context ersetzen und zwei nur-lesende
  Pointer `const` machen; dies behebt die drei C-Findings des ersten Readbacks,
  ohne Task-Ownership, Join-Reihenfolge oder Response-Behandlung zu ändern.
- Direkte Contract-Tests behalten und enge Parser-Grenztests ergänzen, statt
  Assertions zu löschen oder abzuschwächen.
- Weder das Framework-eigene Issue noch Scanner-Konfiguration, Sonar-Settings,
  Quality Gate, Exclusions oder Suppressions verändern.

## Security-Auswirkung

Die Remediation berührt security-relevante Event-Serialisierung, begrenztes
TCP-Table-Parsing, HTTP-Request-Behandlung, Subprocess-Supervision, SPOP-
Deadlines, Socket-/Descriptor-Cleanup und native Ownership-Übergänge. Der
Source-Review erhält JSON-Escaping und Redaction, Byte-/Line-/Frame-Grenzen,
Malformed-Input-Rejection, Loopback-/Deadline-Verhalten, `MSG_NOSIGNAL`-
Behandlung, Owner-Queue-Destroy-Reihenfolge und Fail-Closed-Exits. Für diesen
exakten Kandidaten ist der Post-Readback-terminale Security-Diff mit
vollständiger Abdeckung und null reportbaren Findings abgeschlossen;
historische PR-#361-Evidenz wird weder verwendet noch als Evidenz für diesen
Follow-up akzeptiert.

## Geänderte Dateien

- common/src/event.c
- connectors/apache/harness/apache_process_guard.py
- connectors/envoy/ext_proc/internal/compositetraefik/forwardauth.go
- connectors/envoy/ext_proc/internal/compositetraefik/uds.go
- connectors/envoy/ext_proc/internal/responseobserver/client.go
- connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c
- connectors/lighttpd/harness/lighttpd_backend_close_linux_guard.py
- connectors/lighttpd/tests/test_backend_close_harness_contract.py
- connectors/traefik/composite_middleware/middleware.go
- tests/http_authorization_service_detached_worker_smoke.c
- tests/test_haproxy_spop_peer_isolation_contract.py
- tests/test_haproxy_spop_selftest_cleanup_contract.py
- tests/test_sonar_reliability_contract.py
- reports/audits/change-records/CR-20260913-sonar-connector-followup-remediation.md
- reports/audits/change-records/CR-20260913-sonar-connector-followup-remediation.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Tests und tatsächliche lokale Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Envoy-Response-Observer- und Composite-Traefik-Go-Packages | Bestanden |
| Traefik-Composite-Middleware-Go-Modul | Bestanden |
| Apache-Process-Guard-Suite | Bestanden: 58 Tests |
| Kombinierte fokussierte Python-Contract-Auswahl | Vor den drei Post-Readback-C-Korrekturen bestanden: 191 Tests |
| Common-C17-Helpers | Bestanden |
| Common-Security-, Memory-Safety-, Flow-Integrity- und Authorization-Timeout-Controls | Bestanden |
| HAProxy-Common-Adoption | Bestanden |
| Modifizierte HAProxy-Source, strikte C17-`-Wall -Wextra -Werror -fsyntax-only` | Bestanden |
| Event-/Detached-Worker-fokussierte Contracts mit ASan/UBSan und Event-JSON-Smokes | Bestanden |
| Common-SDK-Serialisierungs-Contract | Nach der finalen Event-Serialisierungs-Contract-Abstimmung bestanden |
| Erster PR-#368-SonarQube-Cloud-Readback | Quality Gate `OK` und null neue Duplikatzeilen/-blöcke, aber drei OPEN helper-eingeführte C-Findings (`c:S107` und zwei `c:S995`); lokal korrigiert und ein frischer Exact-Head-Readback steht aus |
| Ausgewählte fokussierte Post-Readback-Contract-Auswahl | Bestanden: 161 Tests |
| HAProxy-Source nach Readback, striktes C17 `-Wall -Wextra -Werror -fsyntax-only` | Bestanden |
| HAProxy-/Sonar-fokussierte Contracts nach Readback | Bestanden: 38 Tests |
| Detached-Worker-Timeout-/Lifecycle-Smoke nach Readback | Bestanden |
| Lighttpd-fokussierte Contract-Suite | Bestanden: 58 Tests |
| HAProxy-fokussierte Contracts | Bestanden: 52 Tests |
| Task-scoped `make check-haproxy-c17` | Blockiert: Sein Helper endet mit 77, weil der isolierte Parent-Worktree absichtlich kein Framework-`ci/lib/common.sh` hat; Make meldet Exit 2 |
| Vollständiger HAProxy-Runtime-Self-Test | Nicht ausgeführt: Er benötigt separat provisionierte HAProxy-/libmodsecurity-Runtime-Artefakte und wird nicht durch die lokalen Static-/Contract-Ergebnisse ersetzt |

## Ausgeführte Befehle

Alle aufgezeichneten Befehle verwendeten den Repository-RTK-Proxy. Zu den
abgeschlossenen lokalen Befehlen gehören fokussierte Envoy- und Traefik-`go
test`-Läufe, Apache- und kombinierte Python-`unittest`-Auswahlen, die Common-
und HAProxy-Make-Checks, direkte C17-Syntaxkompilierung, `gofmt -d` und `git
diff --check`. Der SonarQube-Cloud-Zugriff verwendet ausschließlich
`/usr/local/bin/sonar-with-env`. Der erste Exact-PR-#368-Readback ergab Quality
Gate `OK`, null neue Duplikatzeilen/-blöcke und drei OPEN task-eigene
C-Findings; die fokussierten C17-, Contract- und Detached-Worker-Smoke-Checks
bestanden nach deren lokaler Korrektur, einschließlich der ausgewählten
161-Test-Contract-Auswahl. Der Post-Readback-terminale Security-Diff ist mit
vollständiger Abdeckung und null reportbaren Findings abgeschlossen; nach dem
nächsten normalen Push ist ein neuer Exact-Head-Hosted-Readback erforderlich.

## Runtime-Evidence

Es wurde keine produktive Connector-Deployment-Runtime oder Protected-Host-
Runtime ausgeführt. Die erfolgreichen Tests sind fokussierte lokale Fixtures
und native Smoke-Controls; sie werden nicht als Produktions-Runtime-Evidenz
dargestellt.

## Nicht ausgeführte Prüfungen mit Begründung

- Der Post-Readback-formelle terminale Security-Diff ist vor dem Staging mit
  vollständiger Abdeckung und null reportbaren Findings abgeschlossen; der
  finale gestagte Scoped-Diff-Review bleibt Teil des Delivery-Preflights.
- Frische Exact-PR-Head-GitHub-Checks, Sonar-Quality-Gate, Issue-/Duplikat-
  Readback, Review-Status und Current-Base-Mergeability benötigen den nächsten
  normalen Push; die Ergebnisse des ersten PR-Heads sind für die korrigierende
  Aktualisierung veraltet.
- Der vollständige HAProxy-Runtime-Self-Test ist nicht ausgeführt, weil dem
  isolierten Parent-Worktree separat provisionierte HAProxy-/libmodsecurity-
  Artefakte fehlen. Er wird nicht durch die bestandenen lokalen Static-/
  Contract-Checks ersetzt.
- Task-scoped `make check-haproxy-c17` ist durch den absichtlich nicht
  materialisierten Framework-Gitlink blockiert; der Helper endet vor der
  Kompilierung mit 77.

## Bekannte Einschränkungen

- Das verbleibende Projekt-Finding ist Framework-eigen:
  `AaA34UWlbqrRc02noCI3` (`python:S1192`) bei
  `modules/ModSecurity-test-Framework/ci/checks/catalog/five_connectors_with_crs_no_mrts.py:112`.
  Es bleibt außerhalb dieses Parent-only-PRs.
- Das Default-Branch-Aggregat von 1.939 Duplikatzeilen / 83 Blöcken / 0,3 %
  enthält Framework-Content. Nur ein Exact-PR-Head-Scan kann New-Code- und
  task-eigenes Duplikatergebnis beweisen; ein Resulting-Master-Aggregat erfordert
  einen separat autorisierten Merge und eine spätere Analyse.

## Verbleibende Risiken

FND-PARENT-1088s Akzeptanz ist auf nicht verfügbare historische PR-#361-
Payloads begrenzt. Sie verzichtet nicht auf, ersetzt nicht und liefert keine
Evidenz für diesen PR. Das erste PR-#368-Quality-Gate war `OK`, aber sein
Exact-Head-OPEN-Inventar identifizierte drei neue helper-eingeführte
C-Findings. Ihre lokale Korrektur ist noch nicht committet oder gepusht; daher
stehen die neuen Exact-Head-GitHub-Checks, Mergeability, Review-Status,
Quality-Gate, OPEN/CONFIRMED-Inventar und Duplikat-Readback aus.

## Finaler Diff- und Review-Status

Bei dieser Record-Aktualisierung haben alle 16 Parent-Findings eine scoped
Source-/Test-Remediation. Der erste Hosted-Scan identifizierte zusätzlich drei
neue Helper-Findings; die Korrekturen der langen Parameterliste und der
nur-lesenden Pointer bestanden ihre direkten C17-, ausgewählten 161-Test-
Contract-, 38-Test-fokussierten Subset- und Detached-Worker-Smoke-Checks. Der
frühere terminale Security-Diff ist durch diese Änderungen überholt; der
Post-Readback-terminale Security-Diff hat vollständige Abdeckung und null
reportbare Findings. Der korrigierende Kandidat bleibt uncommittet, bis der
finale gestagte Diff-Review und der Delivery-Zyklus fertig sind. Der finale
Status wird noch nicht als verifiziert behauptet. Kein Merge ist autorisiert
oder behauptet.
