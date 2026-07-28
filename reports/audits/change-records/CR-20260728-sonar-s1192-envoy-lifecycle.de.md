# Change Record: Parent-Envoy-Lifecycle-Literal-Ownership für SonarQube Cloud S1192

**Sprache:** [English](CR-20260728-sonar-s1192-envoy-lifecycle.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260728-sonar-s1192-envoy-lifecycle |
| Datum (UTC) | 2026-07-28 |
| Basis-Revision | 8e8acb8dab1cd03723de269cab7da7dd62e5e010 |
| Kandidatenbezeichnung | Parent-#154-Kandidat. Dies ist nur eine lokale Kandidatenbezeichnung; es werden weder gehosteter Pull-Request-Status noch Remote-Head-SHA, Review-Ergebnis oder Delivery-Ergebnis festgehalten. |
| Tracking | Parent-SonarQube-Cloud-python:S1192-Issue-Keys AZ9cRyqOHhV2CayPTPzr, AZ9cRyqOHhV2CayPTPzq und AZ9cRyZWHhV2CayPTPwQ. Ihre gehosteten Zustände nach der Änderung sind noch nicht verfügbar. |
| Betroffene Komponenten | Envoy-HTTP-Smoke-Helper-Lifecycle-Fixture und Parent-Full-Lifecycle-Evidence-Checker mit ihren fokussierten Python-Contract-Tests. |
| Grenze | Parent-only-Kandidat: connectors/envoy/harness/envoy_smoke_helper.py, ci/checks/evidence/check-full-lifecycle-evidence.py, ihre zwei fokussierten Tests sowie dieses englisch/deutsche Change-Record-Paar und seine zwei Indizes. Framework, MRTS, Gitlinks, Workflows, Scanner-Konfiguration, generierte Reports und externer Issue-Status bleiben unverändert. |

## Motivation und Problemstellung

Die ausgewählten Parent-Dateien wiederholen drei unveränderliche Literale, die
SonarQube Cloud als python:S1192-Maintainability Debt meldet: /phase4-marker,
text/plain und events.jsonl. Die wiederholten Werte sind Teil von
HTTP-Lifecycle-Fixtures und Full-Lifecycle-Evidence-Ladevorgängen; die
Behebung muss deshalb Duplikate entfernen, ohne Request-Routing,
Response-Metadaten, Artefaktauswahl oder die bestehenden Evidence-Gates zu
ändern.

## Akzeptanzkriterien

- /phase4-marker, text/plain und events.jsonl erhalten jeweils genau einen
  unveränderlichen Module-Level-Owner, der an den ausgewählten Call-Sites
  wiederverwendet wird.
- Der Phase-4-Default-Pfad des Envoy-Helpers, Marker-Response-Body, HTTP-Status
  und content-type-Verhalten bleiben erhalten.
- Lifecycle-Counter-, Artefaktprofil-, Event-Identitäts- sowie
  First-Byte/No-Buffer-Evidence-Validierung bleiben beim Laden desselben
  events.jsonl-Artefakts erhalten.
- Die Änderung bleibt Parent-only und behält die fokussierten Contract-Tests
  als lokale Verhaltensevidence bei.
- Die drei bereitgestellten Live-SonarQube-Cloud-Keys werden festgehalten, aber
  erst nach einer frischen Exact-Head-Hosted-Analyse als erledigt behandelt.
- Die englischen/deutschen Records und Indizes bleiben äquivalent,
  einschließlich aller erforderlichen Change-Record-Überschriften.

## Vorheriges und neues Verhalten

Vor der Änderung verwendete der ausgewählte Code wiederholte Stringliterale
direkt: Der Envoy-Helper wiederholte /phase4-marker in Routing und CLI-Defaults
sowie text/plain in Response-Headern, während der Lifecycle-Checker
events.jsonl beim Laden von Event-Records für drei Evidence-Pfade wiederholte.
Das neue Verhalten gibt diesen exakten Werten die statischen Owner
PHASE4_MARKER_PATH, TEXT_PLAIN_CONTENT_TYPE und EVENTS_FILENAME und ersetzt
die vorhandenen Verwendungen durch diese Owner. Literale, Branch-Prädikate,
Funktionsaufrufe, Protokollwerte und Validierungsentscheidungen bleiben
unverändert.

## Implementierungsentscheidung und Begründung

Die Konstantenextraktion bleibt in den zwei betroffenen Python-Modulen. In
connectors/envoy/harness/envoy_smoke_helper.py liefert PHASE4_MARKER_PATH sowohl
den Upstream-Handler-Vergleich als auch den phase4-first-byte-Default, während
TEXT_PLAIN_CONTENT_TYPE die drei vorhandenen content-type-Header liefert. In
ci/checks/evidence/check-full-lifecycle-evidence.py liefert EVENTS_FILENAME die
vorhandenen Event-Dateilesen in lifecycle_errors, first_byte_errors und
no_buffer_errors.

Es wird weder ein Helper eingeführt noch eine Bedingung, ein Request-Input,
eine Output-Payload, ein JSONL-Parser, ein Evidence-Record-Filter oder ein
Fehlerpfad geändert. Dies ist die kleinste Literal-Ownership-Änderung, die die
ausgewählten python:S1192-Issues adressieren kann und zugleich die etablierten
HTTP- und Evidence-Verträge erhält.

## Security-Auswirkung

Die begrenzte Änderung berührt eine HTTP-Fixture und Evidence-Consumer-Pfade;
deshalb verwendete die fokussierte Sicherheitsreview dieses Invariant: Das
Verschieben unveränderlicher Literale darf weder Phase-4-Route,
Response-Content-Type, Marker-Payload noch die strikte Auswahl des von
Lifecycle-Evidence-Checks verwendeten Event-Artefakts verändern. Kontrollierter
Loopback-Request-Pfad, Response-Header/-Body, JSONL-Laden, Artefaktprofil-Gate,
Event-Identitätsprüfung und Counter-/Error-Handling behalten ihre bestehenden
Kontrollen.

Die fokussierte Review ist genehmigt: Innerhalb dieses Literal-Extraction-Scopes
wurden weder sicherheitsrelevanter Verhaltensdrift noch plausible oder
berichtspflichtige Findings identifiziert. Dies ist weder ein vollständiger
Envoy-Deployment- noch ein repositoryweiter Security-Scan und behauptet kein
gehostetes SonarQube-Cloud-Ergebnis.

## Geänderte Dateien

- connectors/envoy/harness/envoy_smoke_helper.py
- ci/checks/evidence/check-full-lifecycle-evidence.py
- tests/test_envoy_transport_hardening_contract.py
- tests/test_full_lifecycle_evidence.py
- reports/audits/change-records/README.md und README.de.md
- dieses englische/deutsche Change-Record-Paar

## Ausgeführte Befehle

| Befehl oder Kontrolle | Ergebnis |
| --- | --- |
| Managed Exact-Worktree /root/git/ModSecurity-conector/.venv/bin/python -B tests/test_envoy_transport_hardening_contract.py | bestanden: 9/9 Tests. |
| Managed Exact-Worktree /root/git/ModSecurity-conector/.venv/bin/python -B tests/test_full_lifecycle_evidence.py | bestanden: 18/18 Tests. |
| git diff --check für den Kandidaten | bestanden; keine Whitespace-Fehler. |
| Fokussierte Sicherheitsreview des begrenzten HTTP/Evidence-Invariants | genehmigt; kein Finding. |
| Begrenzte Change-Record-Paar-Überschriften-/Identitäts-/Strukturparitätsprüfung und begrenzte Dokumentations-Diff-Prüfung | bestanden; nur für dieses Paar und die zwei Change-Record-Indizes, ohne Framework- oder MRTS-Zugriff ausgeführt. |

## Tests und tatsächliche Ergebnisse

| Befehl oder Prüfung | Ergebnis |
| --- | --- |
| tests/test_envoy_transport_hardening_contract.py | bestanden: 9/9. Der hinzugefügte Contract prüft, dass der phase4-first-byte-Default /phase4-marker bleibt, die Response HTTP 200 mit text/plain bleibt und der Marker-Body unverändert bleibt. |
| tests/test_full_lifecycle_evidence.py | bestanden: 18/18. Der hinzugefügte Contract prüft die Lifecycle-Inventory-Akzeptanz mit dem passenden events.jsonl-Artefakt, ohne den Lifecycle-Counter-Vertrag zu ändern. |
| Kandidaten-git diff --check | bestanden; kein Whitespace-Fehler. |
| Begrenzte englisch/deutsche Change-Record-Parität und Index-Link-Review | bestanden; alle erforderlichen Überschriften, Sprachumschalter, Identitätsfelder, technischen Literale und Index-Links sind vorhanden. |

## Runtime-Evidence

Es wurde keine externe Envoy-, xDS-, ext-proc-, Common/libmodsecurity-,
Host-Proxy-, Framework- oder MRTS-Runtime-Evidence erzeugt oder geändert. Die
fokussierten Python-Module liefern nur Source- und
Controlled-Loopback-Contract-Evidence. Insbesondere werden die erhaltenen
HTTP- und Evidence-Invarianten nicht als Production-Runtime-Capability
behauptet.

## Bekannte Einschränkungen

Die bereitgestellte lokale Testevidence beweist nur die ausgewählten
Parent-Verträge und Literalwiederverwendung. Sie beweist weder ein komplettes
Envoy-Deployment noch eine vollständige Connector-Matrix oder die Abwesenheit
unabhängiger SonarQube-Cloud-Findings. Für die drei referenzierten Issue-Keys
enthält dieser Record keinen Hosted-Status nach der Änderung.

## Verbleibende Risiken

Ein künftiger Caller könnte ein neues hart codiertes äquivalentes Literal
einführen oder eine umgebende HTTP-/Evidence-Kontrolle außerhalb dieses
fokussierten Scopes ändern. Die statischen Owner, direkten Contract-Tests,
lokale Whitespace-Review und fokussierte Sicherheitsreview verringern dieses
Risiko, aber eine frische Exact-Head-SonarQube-Cloud-Analyse ist weiterhin
erforderlich, bevor ein aufgeführtes Issue als erledigt erklärt wird.

## Nicht ausgeführte Prüfungen mit Begründung

- Gehostete Pull-Request-Checks, Exact-Head-SonarQube-Cloud-Analyse, Quality
  Gate-Auswertung, Review, Merge und Master-Integration waren für diesen
  Kandidaten nicht verfügbar und werden nicht behauptet.
- Kein vollständiger Envoy-Build, Integrationslauf, Connector-/Runtime-Matrix-,
  Framework- oder MRTS-Check wurde ausgeführt: Sie liegen außerhalb des
  Parent-only-Literal-Remediation- und Dokumentationsscopes.
- Repositoryweite make check-bilingual-docs und make check-doc-links wurden
  nicht ausgeführt, weil ihre konfigurierten Checks Framework- und/oder
  MRTS-Status untersuchen; die Aufgabe erlaubt ausdrücklich nur begrenzte
  Dokumentationsparitäts- und Diff-Prüfungen ohne Framework-/MRTS-Zugriff.

## Finaler Diff- und Review-Status

Der lokale Parent-#154-Kandidat enthält die begrenzte Literal-Ownership-
Änderung, ihre fokussierten Contracts und dieses gepaarte Traceability-Update.
Die oben festgehaltenen bereitgestellten Exact-Worktree-Testergebnisse,
Kandidaten-Whitespace-Review, fokussierte Sicherheitsreview und begrenzte
Dokumentationsreview bestehen. Es werden weder Commit, Push, gehosteter
PR-Check, SonarQube-Cloud-Issue-Status nach der Änderung, Quality Gate,
Review-Genehmigung, Merge noch Default-Branch-Update behauptet.
