# Phase-4-Modus und Eigentümerschaft von Response-Body-Limits

**Sprache:** [English](phase4-mode-budget.md) | Deutsch

## Schnellorientierung

Phase 4 ist die Response-Body-Verarbeitung. Der Phase-4-Modus steuert das **Late-Intervention-Verhalten** und keine zweite connector-eigene WAF-Inspection-Byte-Policy.

libModSecurity besitzt die Response-Inspection-Aktivierung, MIME-Auswahl und WAF-Response-Byte-Limits über `SecResponseBodyAccess`, `SecResponseBodyMimeType` / `SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit` und `SecResponseBodyLimitAction`.

Legacy-Connector-Response-Limit-Einstellungen können aus Kompatibilitätsgründen weiterhin parsebar bleiben; `off`, `safe` und `strict` führen aber keine unterschiedlichen kumulativen WAF-Byte-Budgets mehr ein. Unabhängige Host-/Transport-Kapazitätslimits, begrenzter Speicher, Allokationsschutz, Timeouts und Message-/Frame-Limits gelten weiterhin.

## Geltungsbereich

Dieser Vertrag umfasst Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd in
diesem Repository. Der Phase-4-Modus steuert das Verhalten bei späten
Interventionen; er erzeugt keine zweite Response-Inspection-Policy im Connector.

## Eigentümerschaft

| Thema | Eigentümer | Erforderliches Verhalten |
| --- | --- | --- |
| Aktivierung der Response-Inspection und MIME-Auswahl | libModSecurity | `SecResponseBodyAccess`, `SecResponseBodyMimeType` und `SecResponseBodyMimeTypesClear` verwenden. |
| Byte-Limit der WAF-Response-Inspection | libModSecurity | `SecResponseBodyLimit` und `SecResponseBodyLimitAction` verwenden. |
| Verhalten bei späten Interventionen | Connector/Host | `off`, `safe` und `strict` behalten ihre hostspezifische Interventionssemantik. |
| Host-/Transportkapazität | Connector/Host | Chunk-/Frame-Limits, begrenzter Speicher, Allokationsgrenzen, Timeouts, Datei-Read-Validierung und Überlaufprüfungen bleiben unabhängige Controls. |

Kein gültiger Phase-4-Modus erzwingt ein zusätzliches Connector-eigenes
kumuliertes Response-Inspection-Budget. Insbesondere dürfen `safe` und
`strict` eine Response nicht allein deshalb abweisen oder abbrechen, weil ein
altes Connector-Inspection-Byte-Limit überschritten wurde.

## Kompatibilität

Alte Einstellungen wie `modsecurity_phase4_body_limit` dürfen während der
Konfigurationsmigration weiter akzeptiert werden. Sie sind
Kompatibilitätswerte, keine WAF-Inspection-Policy, und erzeugen kein nur für
`safe`/`strict` geltendes kumuliertes Response-Limit. Das Entfernen solcher
Einstellungen aus der öffentlichen Konfiguration ist eine getrennte Breaking
Change.

Common-Runtime-Werte wie `response_body_limit` dürfen weiterhin eine
begrenzte Host-/Transport- oder Speicherkapazität beschreiben, wenn der Host
diese Kapazität tatsächlich benötigt. Sie dürfen nicht als Ersatz für
`SecResponseBodyLimit` dargestellt werden.

## Streaming und Speicher

Das Entfernen des Connector-Inspection-Budgets erlaubt keine unbegrenzten
Allokationen. Native/streamende Connectoren sollen Body-Ranges inkrementell an
libModSecurity übergeben. File-backed NGINX-Buffer verwenden einen festen,
wiederverwendeten Scratch-Buffer, statt die gesamte Response zu allozieren.

Puffernde Kompatibilitätsrouten dürfen weiterhin eine Response ablehnen, die
nicht in ihren begrenzten Host-Speicher passt. Envoy-/gRPC-Chunk- oder
Message-Limits, HAProxy-Transportlimits, lighttpd-Sidecar-Kapazität,
Header-/Event-Limits, Korrelationskapazitäten, Timeouts, Pointer-Validierung,
Datei-Read-Prüfungen und Integer-Überlaufprüfungen bleiben aktiv.

## Native Fehler und Interventionsmodi

Echte Engine-, Speicher-, Transport-, Lifecycle- und Processing-Fehler bleiben
Fehler. Diese Änderung wandelt sie nicht in `log_only` um.

In NGINX `off` behält ein negatives natives Interventionsergebnis den
historischen Pfad
`ngx_http_filter_finalize_request(..., NGX_HTTP_INTERNAL_SERVER_ERROR)`.
Positive Statuswerte werden unverändert zurückgegeben; bei null läuft die
Verarbeitung weiter. Das Safe-/Strict-Verhalten bei späten Interventionen
bleibt von der Eigentümerschaft der Response-Limits getrennt.

Andere Integrationen behalten ihre eigenen Rückgabekonventionen und
unterstützten Late-Action-Mechanismen.

## Grenzen der Validierung

Source-Wiring und Unit-Tests können prüfen, dass alle gültigen Modi die alte
Connector-Inspection-Grenze nur noch auf ein Accounting-Maximum auflösen und
dass unabhängige Host-Limits weiter verdrahtet sind. Sie beweisen kein
Live-Verhalten für HTTP/1, HTTP/2, HTTP/3 oder hostspezifische Late-Aborts.

Der Change Record
[CR-20261004-engine-owned-response-limits](../reports/audits/change-records/CR-20261004-engine-owned-response-limits.de.md)
beschreibt Implementierungsumfang und Validierungsstatus dieser Migration.
