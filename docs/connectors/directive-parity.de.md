# Connector-Direktive-Parität

**Sprache:** [English](directive-parity.md) | Deutsch

Status: aktueller, dem Adapter gehörender Apache- und NGINX-Code sowie HAProxy SPOA-Konfiguration

Dieses Dokument dokumentiert die Direktiven- und Konfigurationsunterstützung im lokalen Bereich
Connector-Implementierungen. Die Runtimeförderung ist immer noch evidenzbasiert; A
Die im Code vorhandene Direktive fördert allein nicht das vollständige Verhalten.

## Direktivenmatrix

| Direktive / Konfigurationsoberfläche | Apache | NGINX | HAProxy | Hinweise / Risiko |
| --- | --- | --- | --- | --- |
| `modsecurity` | Unterstützt | Unterstützt | Nicht anwendbar | HAProxy verwendet die HAProxy/SPOE/SPOA-Konfiguration, keine Server-`modsecurity_*`-Anweisungen. |
| `modsecurity_rules` | Unterstützt | Unterstützt | Nicht anwendbar | Das Laden der Regeln bleibt im Besitz des Connectors. HAProxy lädt Regeln über den SPOA-Agenten `rules-file`. |
| `modsecurity_rules_file` | Unterstützt | Unterstützt | Nicht anwendbar | Das HAProxy-Äquivalent ist `rules-file=/etc/modsecurity/haproxy-rules.conf`. |
| `modsecurity_rules_remote` | Unterstützt | Unterstützt | Nicht anwendbar | Das Laden von Remote-Regeln ist für Apache/NGINX Connector-eigener; Die HAProxy-Agentenkonfiguration macht diese Serveranweisung nicht verfügbar. |
| `modsecurity_use_error_log` | Unterstützt | Unterstützt | Nicht anwendbar | Nur Protokollierungsrichtlinie; Audit- und Interventionsverhalten sind getrennt. |
| `modsecurity_transaction_id` | Unterstützt | Unterstützt | Nicht anwendbar | Apache verwendet statische String-Semantik; NGINX verwendet komplexe Werte; HAProxy korreliert über HAProxy `unique-id` / SPOE `request_id`. |
| `modsecurity_transaction_id_expr` | Unterstützt | Nicht unterstützt | Nicht anwendbar | Nur-Apache-Ausdrucksanweisung. |
| `modsecurity_phase4_mode` | Unterstützt | Unterstützt | Nicht anwendbar | Begrenzte Phase-4-Kontrolle. Dies fördert nicht die vollständige RESPONSE_BODY-Unterstützung. |
| `modsecurity_phase4_content_types_file` | Unterstützt | Unterstützt | Nicht anwendbar | Begrenzte Zulassungsliste für Antwortinhaltstypen. |
| `modsecurity_phase4_log` | Unterstützt | Unterstützt | Nicht anwendbar | JSONL Phase 4 decision/evidence-Protokoll für Apache/NGINX. |
| `modsecurity_phase4_body_limit` | Unterstützt | Unterstützt | Nicht anwendbar | Begrenztes Phase-4-Body-Inspektionslimit. NGINX registriert die Direktive, mappt sie in die Common-Konfiguration und übergibt nach dem konfigurierten Limit keine weiteren Response-Bytes an ModSecurity; dies ist keine vollständige RESPONSE_BODY-Förderung. |
| `filter spoe engine modsecurity` | Nicht anwendbar | Nicht anwendbar | Unterstützt | HAProxy SPOE-Einstiegspunkt. |
| `http-request send-spoe-group` | Nicht anwendbar | Nicht anwendbar | Unterstützt | Sendet den Nachweis der Requestsphasen 1/2 an `haproxy-modsecurity-spoa`. |
| `http-response send-spoe-group` | Nicht anwendbar | Nicht anwendbar | Unterstützt | Sendet Antwortheader und begrenzte Evidence für den Response Body. |
| `decision-log` | Nicht anwendbar | Nicht anwendbar | Unterstützt | JSONL-Entscheidungsprotokoll des SPOA-Agenten, normalerweise `/var/log/haproxy-modsecurity/decision.jsonl`. |
| `audit-log` | Nicht anwendbar | Nicht anwendbar | Unterstützt | SPOA/libmodsecurity Überwachungsprotokollinstallation. |

## Apache-Anweisungen

Der Apache-Connector registriert derzeit:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_use_error_log on|off`
- `modsecurity_transaction_id <string>`
- `modsecurity_transaction_id_expr <apache-expression>`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

`modsecurity_transaction_id` behält die Semantik statischer Zeichenfolgen bei.
`modsecurity_transaction_id_expr` ist eine separate Opt-in-Apache-Zeichenfolge
Ausdruck. Statische und Ausdruckstransaktions-IDs schließen sich gegenseitig aus
Es gelten derselbe Apache-Kontext und während der Konfiguration gelten die normalen Überschreibungen des untergeordneten Kontexts
verschmelzen.

Die Unterstützung für Apache Phase 4 ist begrenzt. Der Connector kann die gepufferte Antwort prüfen
Bytes, protokollieren Phase-4-Entscheidungen und zeichnen strikte AbbruchEvidence auf, wenn eine Störung auftritt
Die Intervention erfolgt nach dem Festschreiben der Antwort. Es ist kein vollständiges RESPONSE_BODY
Förderung.

## NGINX-Anweisungen

Der NGINX-Connector registriert derzeit:

- `modsecurity on|off`
- `modsecurity_rules`
- `modsecurity_rules_file`
- `modsecurity_rules_remote`
- `modsecurity_transaction_id`
- `modsecurity_use_error_log on|off`
- `modsecurity_phase4_mode minimal|safe|strict`
- `modsecurity_phase4_content_types_file <path>`
- `modsecurity_phase4_log <path>`
- `modsecurity_phase4_body_limit <bytes>`

NGINX `modsecurity_transaction_id` verwendet einen komplexen NGINX-Wert und kann ihn auswerten
Variablen pro Anfrage. Die Apache-Ausdrucksdirektive `modsecurity_transaction_id_expr` wird für NGINX nicht registriert. Die NGINX-Phase-4-Unterstützung ist begrenzt: Das Body-Limit steuert, wie viele Response-Bytes an ModSecurity übergeben werden, und schreibt Truncation-Metadaten; dies ist keine vollständige RESPONSE_BODY-Förderung.

## HAProxy-Konfigurationsoberfläche

HAProxy implementiert keine Apache/NGINX `modsecurity_*`-Anweisungen. Die jetzige
Produktionspfad ist:

```text
HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity
```

Die unterstützte Konfiguration ist aufgeteilt in:

- HAProxy-Konfiguration: `filter spoe engine modsecurity`,
`http-request send-spoe-group`, `http-response send-spoe-group` und
Durchsetzungsregeln, die `txn.modsec.*`-Variablen lesen.
- SPOE-Konfiguration: Zuordnung von Requests- und Antwortnachrichtenargumenten in
`spoe-modsecurity.conf`.
- SPOA-Agent-Konfiguration: `listen`, `rules-file`, `decision-log`, `audit-log`,
`mode`, `fail-mode`, `request-body-limit`, `response-body-limit` und
`response-body-timeout`.

Der HAProxy-Runtimenachweis umfasst Request-Phasen 1/2, Response-Header-
Verdrahtung sowie Decision-/Audit-Protokolle. Das frühere Phase-4-Response-
Body-Sample ist deaktiviert, weil es `http-response wait-for-body` benötigte;
es ist keine Evidence für einen latenzarmen Response-Pfad. Es gibt keinen
Schreiber für synthetische Matrizen.

## Aufgeschobene und riskante Bereiche

Bucket-Brigaden, Ein- und Ausgabefilter, Körperpufferung, Interventionslaufzeit
Pfade, hook/filter-Reihenfolge, Transaktionseigentum und request/response
Das Lebenszyklusverhalten bleibt konnektorspezifisch. Sie dürfen nicht eingezogen werden
`common/` ohne separaten Design- und Runtimenachweis.

Phase 4 / RESPONSE_BODY ist im gewählten SPOE/SPOP-Pfad `not_implemented`;
das deaktivierte `wait-for-body`-Sample ist keine Runtime-Evidence.

## Gemeinsame Metadaten

`common/include/msconnector/directives.h` enthält den gemeinsamen Direktivennamen
Metadaten, die von Apache und NGINX verwendet werden.

`common/include/msconnector/options.h` enthält freigegebene option/default-Metadaten
für Aktivierung, Protokollierungsrichtlinie und begrenzte Phase-4-Optionen. Diese Header
enthalten keine Apache-Typen, keine NGINX-Typen, keine HAProxy-Typen, keine Hooks, keine Filter,
Keine Bucket-Brigaden, kein Transaktionseigentum und kein Anfrage- oder Response Body
Runtimeverhalten.
