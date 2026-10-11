# Zuständigkeit für Body-Limits und Phase-4-Modus

**Sprache:** [English](phase4-mode-budget.md) | Deutsch

## Zuständigkeit

Request-Inspektionslimit und Aktion gehören zu `SecRequestBodyLimit` und
`SecRequestBodyLimitAction`; das eigenständige native `SecRequestBodyNoFilesLimit`
gilt zusätzlich für Request-Daten ohne Datei-Uploads. Response-Inspektionslimit
und Aktion gehören zu `SecResponseBodyLimit` und `SecResponseBodyLimitAction`.
Der Connector darf keinen Body-Limitdefault bereitstellen, Werte aus Regeltext
ermitteln, Direktiven einschleusen, Reject/ProcessPartial wählen oder vor der
Engine einen Body kürzen. Ausgelassene Direktiven behalten native
libModSecurity-Semantik.

| Gegenstand | Eigentümer | Verhalten |
| --- | --- | --- |
| P2-/P4-Inspektion und Limitaktionen | libModSecurity | Native Direktiven, Ergebnisse und Interventionen bestimmen die Inspektion. DetectionOnly behält die tatsächliche Engine-Semantik. |
| Access und Response-MIME-Geltungsbereich | libModSecurity | `SecRequestBodyAccess`, `SecResponseBodyAccess` und Response-MIME-Direktiven bleiben native Konfiguration. |
| Eingabe und Phasenabschluss | Connector | Vollständige gültige Chunks anbieten, native Ergebnisse bei jedem Append erfassen, disruptive Ergebnisse bis EOS erhalten und jede Phase einmal abschließen. |
| Späte P4-Behandlung | Connector/Host | `off`, `safe`, `strict` wählen unterstützte Host-Interventionsbehandlung, niemals Bodygröße oder Limitaktion. |
| Sicherheit | Connector/Host | Geprüfte Arithmetik, gültige Pointer, begrenzte einzelne Frames/Nachrichten, Descriptoren, Dateibereiche, Metadaten, Timeouts und begrenzten Arbeitsspeicher erhalten. |

## Entfernte Konfiguration

`request_body_limit`, `body_limit_action`, `modsecurity_request_body_limit`,
`modsecurity_body_limit_action`, HAProxy `request-body-limit`, Envoy
`max_request_body_bytes` und Traefik `maxRequestBodyBytes` entfernen.
Die zuvor entfernten Response-Optionen bleiben entfernt: `response_body_limit`,
`modsecurity_response_body_limit`, `modsecurity_phase4_body_limit`, HAProxy
`response-body-limit` und Envoy `max_response_body_bytes`. Entfernte Optionen
lassen die Konfiguration fehlschlagen, statt still ignoriert zu werden.
Es gibt keine kumulative Connector-Größenoption als Ersatz. Betreiber verwenden
ihre normale Engine-Regelkonfiguration; kein zusätzliches Connector-Limit ist
erforderlich. Die frühere Vorgabe zum Erhalt der Request-Policy ist aufgehoben.

## Arbeitsspeicher und Transport

Ein inkrementeller Arbeitspuffer wird bis EOS wiederverwendet; seine Kapazität
bestimmt nicht die erlaubte Gesamtbodygröße. NGINX-Dateieingabe behält
Descriptor-, Regular-file-, Bereichs- und geprüfte Lesevalidierung. MRC1 verwendet
einzelne 32-KiB-Body-Chunks und 64-KiB-Frames; Traefik-UDS und Envoy-gRPC behalten
Nachrichtenkontrollen. Header-/Eventmetadaten, Korrelationsregister und
Inaktivitäts-/Lebensdauertimeouts bleiben begrenzt. Private Dateipufferung erlaubt
dem Stock-lighttpd-Sidecar inkrementelle Inspektion und hält das Upstream-Replay
bis zum nativen P2-Allow zurück. Datenträgerfehler bleiben technische Fehler und
wählen kein Inspektionspräfix und keine Limitaktion.

`bytes_inspected` beschreibt der Engine angebotene Bytes, nicht das native
ProcessPartial-Präfix. Append null ist operationsspezifisch und darf bei gültigem
nativem ProcessPartial nicht als Allokations- oder Dateifehler gemeldet werden.
Natives Request-Reject kann während Append HTTP 403 liefern; ein anderer nativer
Pfad kann 413 liefern. Der Connector erhält das tatsächliche Ergebnis bis EOS.

## Aktive Gesamtbody-Einschränkungen

Für Autorisierungsprofile mit begrenzten Hostpuffern wird keine vollständige
Entfernung behauptet. Diese Grenzen bleiben von nativer Engine-Policy getrennt
und werden nicht als Arbeitspufferkapazität umbenannt:

| Aktiver Pfad | Tatsächlicher Wirkungsbereich | Einschränkung |
| --- | --- | --- |
| Envoy-ext_authz-Request-Autorisierung | Host-`max_request_bytes` ausgewählter Templates (4096 oder 33 Byte) | Ein begrenztes vollständiges Request-Sample erreicht die Autorisierung; ein Response-Observer macht die Request-Eingabe nicht inkrementell. |
| Traefik-forwardAuth-Request-Autorisierung | Host-`maxBodySize` ausgewählter Templates (4096 oder 33 Byte) | Der Host puffert den weitergeleiteten Request-Body; der Observer beseitigt diese Request-Grenze nicht. |
| Composite-Traefik-Autorisierungsantwort | Host-`maxResponseBodySize=32768` | Begrenzt die Autorisierungsantwort, nicht den Response-Body der Upstream-Anwendung. |
| HAProxy-SPOE-/SPOP-Request-Sample | Eine begrenzte Protokollnachricht mit `req.body` | Ein unvollständiges Sample belegt keine vollständige P2-Inspektion; natives HTX ist ein separates Profil. |

Die nativen Streamingprofile übernehmen diese Autorisierungsgrenzen nicht.
Envoy-ext_authz-Templates verwenden `allow_partial_message: false`; ausdrücklich
partielle oder mehrdeutige `x-envoy-auth-partial-body`-Metadaten werden vor dem
Öffnen der nativen Transaktion abgelehnt. Das prüft Transportvollständigkeit,
keine Connector-Inspektionsgröße oder -Aktion. Die Host-Sample-Grenze bleibt eine
offene Einschränkung.
Im Composite-Profil bleibt eine Buffer-Ablehnung vor der Autorisierung nur mit
interner Host-Provenienz 413; sie erzeugt keine native Entscheidung und kein EOS.
Ein Wechsel von Autorisierung zu nativem Streaming würde den Hostvertrag ändern
und benötigt eigene Nachweise. Unabhängige Host-Requestgrößenkontrollen wie
lighttpd `server.max-request-size` bleiben Hostkonfiguration.

## Nachweise

Jeder Body-Inspektionstest liefert Engine-Limit und Aktion seiner geprüften
Richtung ausdrücklich; Request-Fixtures ohne Datei-Uploads wählen zusätzlich
das native No-files-Limit. Helper haben keine impliziten Größen-/Aktionsdefaults.
Tests ohne Body-Inspektion benötigen keine künstlichen Limits.

Echte Library-Prüfungen unterscheiden unter/exakt/über Limit, native Aktionen
und DetectionOnly, Chunks und Dateien, dieselbe Payload unter verschiedenen
Limits und Marker jenseits früherer Connectorgrenzen. Builds und Quellverträge
belegen kein gehostetes HTTP/1, HTTP/2, HTTP/3, Buffer-Ownership oder
Late-Abort-Verhalten. Siehe [Stack-Checkliste](response-limit-stack-checklist.de.md).
