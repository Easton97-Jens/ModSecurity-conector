# Change Record CR-20260909-fail-closed-connector-remediation

**Sprache:** [English](CR-20260909-fail-closed-connector-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260909-fail-closed-connector-remediation |
| Datum (UTC) | 2026-09-09 |
| Basis-Revision | 26a560e64cbaf906c0d35bba199f65436830d1dd |
| Branch | security/audit-2026-09-09-fixes |
| Issue oder Pull Request | Beim Erstellen dieses Pre-Delivery-Records existierte keine Referenz. Der aktuelle Benutzer autorisierte einen separaten Parent-Draft-PR; seine beobachtete Referenz wird nach der Erstellung dokumentiert. |
| Delivery-Status | Die lokale Remediation ist für eine Draft-PR-Übergabe bereit. Commit, Push, Hosted-Checks, Review und Merge waren beim Erstellen des Records noch keine Fakten; Merge, Release, Deployment, ein Default-Branch-Write und eine Parent-Gitlink-Änderung sind nicht autorisiert. |

## Motivation und Problemstellung

Aktivierte Connector-Verarbeitung darf einen internen Transaktions-Setup- oder
nativen Response-Header-Verarbeitungsfehler nicht als harmlosen deaktivierten
oder nicht anwendbaren Pfad behandeln. Diese Parent-only-Remediation macht
diese Fehlerpfade terminal und bewahrt dabei das explizit deaktivierte
Verhalten sowie die bestehende Streaming-Grenze. Der private Audit,
Rohreproduktionen, Credentials und Runtime-Payloads sind ausgeschlossen.

## Akzeptanzkriterien

- Fehler beim Aufbau des aktivierten Apache-Request-Kontexts führen in den
  bestehenden Fail-Closed-Response-Pfad statt zu einem erfolgreichen Decline.
- Ein nicht erfolgreiches natives NGINX-Response-Header-Ergebnis wird terminal,
  stellt den PCRE-Allokationszustand genau einmal wieder her und ruft nicht den
  nächsten Header-Filter auf.
- Fokussierte Negativ- und legitime Control-Contracts bestehen; nicht
  verfügbare Host-Runtime-Proofs bleiben als blockiert statt bestanden
  dokumentiert.
- Englische/deutsche Connector-Dokumentation und dieser englische/deutsche
  Change Record beschreiben denselben Scope, dieselbe Evidence und dieselben
  Einschränkungen.
- Delivery bleibt auf einen gewöhnlichen Parent-Draft-PR beschränkt; es gibt
  keine Framework-/MRTS-Source-, Gitlink-, CI-Berechtigungs-, Merge-, Release-
  oder Deployment-Änderung.

## Implementierungsentscheidung und Begründung

Apache unterscheidet nun deaktivierte Verarbeitung von einem Fehler im
aktivierten Setup. Ein Request-Kontext wird erst veröffentlicht, nachdem
Ownership und Cleanup gültig eingerichtet sind; ein aktivierter Construction-,
Expression- oder Identifier-Fehler folgt dem bestehenden terminalen
Failure-Handling.

NGINX hält einen terminalen Response-Header-Processing-Fehler vor dem
Upstream-Header-Filter fest. Der Fehlerpfad stellt den PCRE-Allokationszustand
genau einmal wieder her, verwendet begrenztes generisches Logging, gibt
`NGX_ERROR` zurück und weist Reinvocation zurück. Die Test-Fixtures decken
Erfolg, null und weitere nicht erfolgreiche native Ergebnisse, Filterreihenfolge
und Cleanup ab.

Das bestehende progressive P4-Modell wurde geprüft, aber nicht verändert. Es
behauptet weiterhin keinen Full-Response-Holdback, keine Zero-Byte-Garantie,
keine Replacement-Response sowie keinen HTTP/2- oder HTTP/3-Reset ohne
Host-Evidence.

## Security-Auswirkung

Die betroffene Sicherheitsgrenze ist aktivierte Request-/Response-Inspection
während der Connector-Transaktions-Lifecycle-Verarbeitung. Vor dieser Änderung
konnte ein Fehler in einem aktivierten Pfad mit einem nicht anwendbaren Ergebnis
verwechselt werden; dadurch konnte Traffic ohne das vorgesehene Inspection-
Ergebnis fortgesetzt werden. Die Korrektur macht den Fehler an der Connector-
Grenze beobachtbar und terminal. Fokussierte statische und Fixture-Evidence
prüft die ursprüngliche Fehlerklasse, eine alternative Nicht-Erfolgs-Klasse und
deaktivierte/Allow-Controls erneut. Dieser Record enthält keinen sensitiven
Test-Payload und keine Produktionsdaten.

## Geänderte Dateien

- Apache-Implementierung und Bootstrap-Contract:
  `connectors/apache/src/mod_security3.c` und
  `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`.
- Apache-Dokumentation und Regression-Coverage:
  `connectors/apache/README.md`, `connectors/apache/README.de.md` und
  `tests/test_apache_request_transaction_cleanup.py`.
- NGINX-Implementierung:
  `connectors/nginx/src/ngx_http_modsecurity_common.h` und
  `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`.
- NGINX-Contracts und native Fault-Fixtures:
  `tests/test_nginx_upstream_security_contract.py`,
  `tests/test_nginx_p3_header_fixture.py`,
  `tests/run_nginx_p3_header_fixture.py`,
  `tests/nginx_p3_header_observer_fixture/` und
  `tests/nginx_p3_header_injector_fixture/`.
- Traceability: dieser gepaarte Change Record und die gepaarten Archivindizes.

Durch diesen Parent-Record werden keine Framework- oder MRTS-Source, kein
Parent-Gitlink, keine Workflow-Berechtigung und kein generierter historischer
Report verändert.

## Ausgeführte Befehle

| Befehl oder Prüfung | Ergebnis |
| --- | --- |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_apache_request_transaction_cleanup tests.test_apache_fail_closed tests.test_apache_connection_phase_contract` | Exit `0`; 22 fokussierte Apache-Contracts bestanden. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_nginx_p3_header_fixture tests.test_nginx_upstream_security_contract tests.test_native_api_fail_closed_contract tests.test_nginx_header_iteration_contract` | Exit `0`; 26 fokussierte NGINX-Contracts bestanden. |
| `rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest tests.test_p1_p4_vector_catalog tests.test_connector_capabilities tests.test_full_lifecycle_profiles tests.test_full_lifecycle_evidence tests.test_apache_phase4_response_regression_wiring tests.test_apache_phase4_rate_limit tests.test_nginx_phase4_runner_wiring tests.test_nginx_bounded_soak_contract` | Exit `0`; 73 begrenzte P4-Contract-Tests bestanden mit 3 erwarteten Runtime-Skips. |
| `rtk proxy env FRAMEWORK_ROOT=<task-framework-root> APACHE_C_STANDARDS_OUT=<task-owned-build-root> BUILD_ROOT=<task-owned-build-root> make check-apache-c17` | Exit `0`; Apache-C17-Standards-Kompilierung bestand. |
| `rtk proxy env FRAMEWORK_ROOT=<task-framework-root> BUILD_ROOT=<task-owned-build-root> NGINX_SOURCE_DIR=<task-owned-configured-source> make check-nginx-c17` | Exit `0`; NGINX-C17-Standards-Kompilierung bestand gegen die task-eigene konfigurierte Source. |
| `rtk proxy git diff --check` | Exit `0`; es wurde kein Whitespace-Fehler gemeldet. |
| `rtk proxy make check-bilingual-docs` | Exit `1`; die Struktur des gepaarten Change Records bestand nach der Korrektur, während dem Task-Worktree seine Framework-Submodul-Link-Targets fehlen. Dies etabliert keinen Dokumentations-Pass. |

## Runtime-Evidence

Es wird kein Apache- oder NGINX-Host-Runtime-Ergebnis behauptet. Die
fokussierten Tests üben nur die Connector-Contracts und die kontrollierte
Native-Fault-Fixture-Grenze aus. Es wurde kein Produktionsdienst kontaktiert.

## Nicht ausgeführte Prüfungen mit Begründung

- Der Non-Root-Apache-Loopback-Runner konfigurierte und baute, konnte aber nicht
  starten, weil Änderungen der Ownership auf dem Task-Dateisystem `EINVAL`
  zurückgaben, POSIX-ACL-Setup nicht verfügbar war und `/tmp` read-only war.
  Es wurde kein Root-Fallback verwendet.
- Das NGINX-Native-Loopback-Fixture weist Root-Ausführung absichtlich zurück und
  konnte wegen derselben Dateisystemursache die unprivilegierte Ownership-/ACL-
  Vorbereitung nicht abschließen. Es wird kein Native-Loopback-Ergebnis
  behauptet.
- Frische Exact-Head-Hosted-Checks, Review und SonarQube-Disposition existieren
  beim Erstellen des Pre-Delivery-Records noch nicht.

## Bekannte Einschränkungen

Die nicht verfügbaren Host-Runtime-Voraussetzungen lassen die ursprüngliche
Host-Level-Reproduktion und den legitimen Control-Proof als
`blocked_environment` offen. Statische und Fixture-Evidence begründet keine
clientseitig sichtbare HTTP/1.1-, HTTP/2- oder HTTP/3-Wirkung. Die P4-Prüfung
bleibt eine begrenzte No-Change-Entscheidung.

## Verbleibende Risiken

Die Code-Level-Fehlerpfade und fokussierten Regressionen stehen für die Review
bereit, aber die Findings bleiben lokal behoben mit ausstehender Host-
Verifikation. Sie werden nicht auf `verified` hochgestuft, und dieser Record
akzeptiert weder das Restrisiko noch beantragt er einen Merge.

## Finaler Diff- und Review-Status

Ein unabhängiger Scoped-Security-Diff-Review fand keinen konkreten Bypass in
den Apache-/NGINX-Änderungen und kein abgeschwächtes Test-Control. Der finale
Task-eigene Diff, die gepaarte Dokumentation, die staged-Dateiliste, Commit,
die Remote-/PR-Head-Beziehung und Hosted-Ergebnisse müssen während des
autorisierten Draft-PR-Lifecycle noch beobachtet werden.
