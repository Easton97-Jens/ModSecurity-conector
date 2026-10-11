# Phase-4-Modus und Zuständigkeit für Response-Body-Limits

**Sprache:** [English](phase4-mode-budget.md) | Deutsch

## Geltungsbereich

Dieser Vertrag umfasst Common Runtime und sämtliche Response-Routen von Apache,
NGINX, HAProxy, Envoy, Traefik und lighttpd einschließlich Middleware,
Companions und Sidecars. Der Phase-4-Modus steuert die Host-Interventionsbehandlung.

## Zuständigkeitsvertrag

Response-Body-Inspection-Limit und Limit-Aktion werden ausschließlich durch
`SecResponseBodyLimit` und `SecResponseBodyLimitAction` festgelegt.
Der Connector besitzt dafür keine eigene Option, keinen Default und
keine zweite Durchsetzungslogik.

| Gegenstand | Eigentümer | Erforderliches Verhalten |
| --- | --- | --- |
| Aktivierung und MIME-Auswahl der Response-Inspection | libModSecurity | `SecResponseBodyAccess`, `SecResponseBodyMimeType`, `SecResponseBodyMimeTypesClear` bleiben Engine-Konfiguration. |
| Response-Inspection-Limit und Reject/ProcessPartial | libModSecurity | Native Direktiven besitzen Limit, Aktion, Ergebnisse und Interventionen. |
| Response-Daten und native Ergebnisse | Connector | Vollständige geliehene Chunks sicher übergeben; native Operationsergebnisse und Interventionen erfassen; Phase abschließen. |
| Späte Interventionen | Connector/Host | Bestehende `off`, `safe`, `strict` und unterstützte Hostaktionen bleiben erhalten. Kein Modus wählt ein Response-Limit. |
| Technische Sicherheit | Connector/Host | Begrenzte Arbeitsbuffer, Protokollframes/-nachrichten, echte Pufferspeicherkapazität, Datei-/Descriptor-/Pointerprüfungen, Overflow, Timeouts und Metadatenlimits bleiben unabhängig. |

Der Connector parst keine Engine-Regeln zur Limitermittlung und schleust keine
Engine-Defaultdirektive ein. Includes, Vererbung und ausgelassene Konfiguration
behalten die native libModSecurity-Semantik. `body_limit_action` gilt nur für die
bestehende Request-Policy.

## Kompatibilität

`response_body_limit`, `modsecurity_response_body_limit`,
`modsecurity_phase4_body_limit`, HAProxy `response-body-limit` und Envoy
`max_response_body_bytes` aus der jeweiligen Konfiguration entfernen. Entfernte
Optionen werden abgelehnt; es gibt keinen Alias oder Ersatz für ein kumulatives
Response-Limit. Es entsteht keine neue Produktiv-Konfigurationspflicht.
Betreiber konfigurieren Engine-Limits über ihre normale Regelkonfiguration.

## Streaming und Speicher

Streaming-Adapter übergeben jeden gültigen Chunk an libModSecurity ohne
Connector-Kürzung oder kumulative Inspection-Grenze. Eine Arbeitsblockgröße ist
keine erlaubte Gesamtgröße einer Response. Geprüfte Zähler erkennen Overflow,
ohne `SIZE_MAX` als Engine-Limit oder Allokationsgröße einzusetzen.

NGINX behält begrenzten wiederverwendbaren Datei-Scratch und prüft Dateibereiche.
MRC1 behält 32-KiB-Body-Chunks und 64-KiB-Frames; diese Grenzen gelten pro
Nachricht. Envoy behält gRPC-Nachrichtenlimits. Traefik behält UDS-Frame- und
Chunkprüfungen. HAProxy behält SPOP-/HTX-Transportprüfungen. Der aktive
lighttpd-Sidecar streamt durch begrenzten Scratch-Speicher. Seine alte
Gesamtresponse-Pufferung ist auskompiliert und setzt kein aktuelles Laufzeitlimit.
Header, Events, Korrelationsregister,
Descriptoren und Timeouts bleiben begrenzt.

Der Response-Zähler `bytes_inspected` erfasst die der Engine angebotenen Bytes.
Er behauptet nicht, dass die Engine nach ihrer Wahl von ProcessPartial jedes Byte
inspiziert hat.

## Native Fehler und Interventionsmodi

Echte Engine-Limitinterventionen bleiben native Ergebnisse. `ProcessPartial`
wird durch die Engine gewählt und ausgeführt und niemals mit einem
Connector-Bytezähler simuliert. Ein Append-Ergebnis allein ist keine
Allow-Entscheidung. Native Rückgabeverträge, Interventionserfassung,
Phasenabschluss und Protokollierung tatsächlicher Hostaktionen bleiben
operationsspezifisch. Technische Engine-, Speicher-, Transport- und
Lebenszyklusfehler bleiben Fehler; `safe` wandelt sie nicht in erfolgreiche
Log-only-Ergebnisse um.

## Nachweisgrenze

Jeder Response-Inspection-Test muss beide Direktiven ausdrücklich in seiner
eigenen Konfiguration wählen. Gemeinsame Fixture-Helper verlangen Limit und
Aktion als Argumente; globale Defaults oder payloadabhängige Werte gibt es
nicht. Tests ohne Response-Inspection benötigen keine künstliche
Response-Limitkonfiguration.

Echte Engine-Integration prüft die Limitwirkung getrennt von Adapterverträgen
mit Stubs. Builds und Unit-/Vertragstests sind keine gehosteten HTTP/1-, HTTP/2-,
HTTP/3- oder Late-Abort-Nachweise. Die getrennte
[Stack-Checkliste](response-limit-stack-checklist.de.md) führt Implementierung,
Tests und fehlende echte Hostnachweise auf.
