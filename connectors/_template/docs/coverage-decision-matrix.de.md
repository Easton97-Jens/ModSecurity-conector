# Deckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: geeignetes Gerüst, nicht laufzeitverifiziert

Deutsch: geeignet als Scaffold-Vorlage, nicht runtime-verifiziert.

Diese Datei ist eine generische Abdeckungs- und Promotion-Matrix für neue Connectors.
Framework-Abdeckung bedeutet, dass ein Fall oder Runner vorhanden ist. Laufzeitüberprüfung bedeutet,
dass ein konkreter Connector-Befehl ausgeführt wurde und ein dokumentiertes Ergebnis für
diesen Connector geliefert hat.

Neue Connectors dürfen keinen lokalen `connectors/<name>/tests`-Ordner hinzufügen.
Ausführbare Tests sind Eigentum des Frameworks.

Laufzeitnachweise sind nicht auf die Vorlage selbst anwendbar. Sie müssen von jedem
konkreten Connector geliefert werden.

## Nachweisquellen zum Ausfüllen

- Framework-Fälle:
  `modules/ModSecurity-test-Framework/tests/cases/`
- Connector-spezifische Fälle:
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
- Runner:
  `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Laufzeitbericht:
  `reports/template-verification-nginx-apache/verified-runtime-run.md` oder ein
  connector-spezifisches Äquivalent
- Summary-JSON:
`<BUILD_ROOT>/results/.../<connector>-summary.json`

## Statusvokabular

- `framework-covered`: Es existiert ein YAML/framework-Fall, der Connector jedoch nicht
  allein durch diese Tatsache laufzeitüberprüft.
- `runtime-smoke-verified`: Ein konkreter Befehl wurde für den benannten Connector
  und Fall ausgeführt und hat bestanden.
- `crs-verified`: Ein With-CRS-Befehl oder -Fall hat CRS-Nachweise und ein
  bestandenes Ergebnis.
- `partial`: Es gibt einige Struktur- oder Laufzeitnachweise, aber die Mindestmatrix
  ist unvollständig.
- `not-verified`: Es liegen keine ausreichenden Laufzeitnachweise vor.
- `fail`: Laufzeit wurde ausgeführt und die Erwartung wurde nicht erfüllt.
- `blocked`: Der Test konnte aufgrund der Umgebung, einer Abhängigkeit oder
  Harness-Voraussetzungen nicht ausgeführt werden.

## Connector-Variantenmatrix

| Phase / Gate | Framework cases present | No-CRS status | With-CRS status | Evidence path | Decision |
| --- | --- | --- | --- | --- | --- |
| Phase 1 / Request headers, URI, ARGS | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 2 / Request body, multipart, XML/JSON | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 3 / Response headers | fill per connector | required per connector | required per connector | required per connector | per-connector gate |
| Phase 4 / Response body | fill per connector | required per connector | required per connector | required per connector | RESPONSE_BODY blocking gate |
| RESPONSE_BODY blocking | fill per connector | runtime promotion gate | runtime promotion gate | required per connector | do not promote from pass-through/log-only |
| Negative/pass-through | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| Audit/log evidence | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| Startup/reload validation | fill per connector | required per connector | required per connector | required per connector | required before more than partial |
| CRS-specific behavior | fill per connector | not applicable | required per connector | required per connector | required for `crs-verified` |
| Promotion gate | fill per connector | required per connector | required per connector | required per connector | blocked until full matrix documented |

## Checkliste für Vorlagen

- [x] Status: Framework abgedeckt – Framework-Testpfade, auf die verwiesen wird.
- [x] Status: Framework abgedeckt – Kein lokaler `connectors/<name>/tests`-Ordner.
- [x] Status: absichtlich extern – Ausführbare Tests gehören dem Framework
      und muss referenziert und nicht in `connectors/_template/tests` kopiert werden.
- [ ] Status: Pro-Connector-Gate – Verifizierte Laufzeitlauf-Nachweisdatei verknüpft
      für den konkreten Connector.
- [ ] Status: Pro-Connector-Gate – No-CRS-Ergebnis dokumentiert.
- [ ] Status: Pro-Connector-Gate – With-CRS-Ergebnis dokumentiert.
- [ ] Status: Pro-Connector-Gate – Phase-1-Laufzeitnachweis dokumentiert.
- [ ] Status: Pro-Connector-Gate – Laufzeitbeweis für Anforderungstext der Phase 2
      dokumentiert.
- [ ] Status: Pro-Connector-Gate – Phase-3-Antwort-Header-Laufzeitnachweis
      dokumentiert.
- [ ] Status: Pro-Connector-Gate – Phase-4-Antworttext-Laufzeitbeweis
      dokumentiert.
- [ ] Status: Laufzeit-Promotion-Gate – RESPONSE_BODY Blockierung verifiziert mit
      command/result/log Nachweise.
- [ ] Status: Pro-Connector-Gate – Audit/log Nachweise dokumentiert.
- [ ] Status: Pro-Connector-Gate – Negative/pass-through Fall dokumentiert.
- [x] Status: geeignetes Gerüst – Vorlage bleibt nicht laufzeitverifiziert; jeder
      konkreter Connector bleibt `partial` bestehen, bis die erforderliche Matrix vollständig ist.

## RESPONSE_BODY Tor

Erforderlich vor Inanspruchnahme der RESPONSE_BODY-Sperrung:

- [ ] Framework-Testfall vorhanden
- [ ] erwarteter Blockierungsauslöser dokumentiert
- [ ] tatsächliches Sperrergebnis dokumentiert, zum Beispiel HTTP 403
- [ ] log/report Nachweise dokumentiert
- [ ] Befehl dokumentiert
- [ ]-Connector dokumentiert
- [ ] Apache und NGINX separat dokumentiert, wenn ein gemeinsamer Anspruch geltend gemacht wird

Dies ist kein Vorlagenfehler. Es handelt sich um ein Laufzeit-Promotion-Gate für konkrete
Connectors.

## Mindestnachweis für mehr als `partial`

- [ ] No-CRS PASS für die beanspruchten connector/scope.
- [ ] With-CRS PASS für die beanspruchten connector/scope.
- [ ] `phase1_header_block` oder gleichwertiger Phase 1 command/result/report Pfad.
- [ ] Request-Body-Blockierung command/result/report Pfad.
- [ ] Antwort-Header-Blockierung command/result/report Pfad beim Framework
      Unterstützung vorhanden ist.
- [ ] Antwortkörper blockiert command/result/log Nachweise.
- [ ] Audit/log Nachweise.
- [ ] Startup/reload Validierung.
- [ ] Negative/pass-through Fallbeweise.
- [ ] Keine unaufgelösten FAIL/BLOCKED-Zeilen in der beanspruchten Mindestmatrix.

## Entscheidung

Das Template ist als Scaffold-Vorlage geeignet. Es ist bewusst nicht
runtime-verifiziert und enthält keine produktive Connector-Implementierung.
Neue Connectoren müssen pro Connector Gates für Origin, Metadata, Build,
No-CRS, With-CRS, Coverage Matrix und Runtime Evidence erfüllen, bevor sie über
teilweise darüber hinaus bewertet werden können.
