# Prüfmatrix zur Body-Inspection

**Sprache:** [English](body-inspection-review-matrix.md) | Deutsch

Dies ist die kompakte aktuelle Routenübersicht für PR #410. Sie trennt Quell-
und Komponentennachweise von vollständiger gehosteter HTTP-Abnahme; keine Zeile
behauptet eine vollständige I12- oder V08–V10-Matrix.

| Profil | Request-/Response-Route | Aktuelle Grenze |
| --- | --- | --- |
| Apache native | Speicher-/Dateichunks erreichen P2; APR-Responsebrigaden erreichen P4 und erhalten natives Reject bis EOS. | Komponenten-/APR-Kontrollen bestehen; eine vollständige aktuelle httpd-Protokoll-/Commit-Matrix ist nicht belegt. |
| NGINX native | Validierte Speicher-/Dateieingaben sind inkrementell; Responsechunks und einmaliges EOS erreichen P4. | Quell-/Contractnachweise bestehen; eine vollständige aktuelle Hostmatrix für Speicher/Dateien und späten Abbruch ist nicht belegt. |
| HAProxy native HTX | Geliehene HTX-Request-/Responseblöcke und EOS nutzen den nativen Streamingpfad. | Für die vollständige Protokoll-/Strict-Matrix ist eine eigene integrierte Qualifikation nötig. |
| HAProxy SPOE/SPOP | Ein vollständig im Frame darstellbares Requestsample wird nur bei übereinstimmender typisierter Gesamtlänge, Framing und Samplelänge zugelassen; der native HTX-Companion besitzt den Responsestream. | Unbekannte/chunked oder ungerahmte HTTP/2-Samples werden hier nicht unterstützt; für vollständiges Streaming natives HTX verwenden. |
| Envoy ext_proc | Gestreamte Request-/Responsenachrichten erreichen P2/P4; die Kapazität gilt je Nachricht. | Quell- und native/CGo-Komponentennachweise ersetzen keine vollständige ext_proc-Hostmatrix. |
| Envoy ext_authz + Observer | Der Host puffert ein Authorization-Requestsample; der unabhängige Observer liefert Responsechunks und EOS. | `max_request_bytes` ist ein Host-Samplelimit; partielle oder mehrdeutige Metadaten scheitern vor nativer Allokation. |
| Traefik native UDS | Inkrementelle Request- und Anwendungsresponsechunks nutzen den Engine-UDS-Pfad. | Komponenten-/Protokollnachweise bestehen; vollständige gehostete Protokoll-/Commit-Abnahme bleibt getrennt. |
| Traefik forwardAuth + Observer | Authorization-Requests sind hostgepuffert; der Observer behandelt die Anwendungsresponse unabhängig. | `maxBodySize` ist ein Host-Requestlimit; `maxResponseBodySize=32768` begrenzt nur die Authorization-Antwort. |
| lighttpd Stock sidecar | Inkrementeller Eingang wird privat mit begrenztem RAM gespult und erst nach nativem Allow wiedergegeben; Responsefehler führen nicht zu Replay. | Aktuelle Komponentennachweise enthalten eine unveränderte RST-Delivery-Lücke; vollständige Deploymentproben bleiben getrennt. |
| lighttpd patched native | Validierte Speicher-/Dateichunks erreichen P2 und Responsechunks/EOS erreichen P4. | Quell-/Contractnachweise bestehen; eine vollständige aktuelle Patched-Hostmatrix ist nicht belegt. |

## Gemeinsamer Vertrag

- Native Engine-Direktiven besitzen Inspection-Limits und Aktionen. Connectoren
  leiten keine Limits aus Regeln ab, fügen keine Direktiven ein und wählen kein
  Inspection-Präfix.
- Angebotene, gespeicherte und nachweislich inspizierte Bytes sind verschiedene
  Fakten. DetectionOnly erzeugt kein disruptives Ergebnis.
- Common schließt P2/P4 einmalig ab, erhält den ersten technischen Fehler und
  lehnt Wiedereintritt nach Terminalfehler ab. EOS wird nur bei Hostzufuhr erfasst.
- Pointer-, Bereichs-, Descriptor-, Frame-, Timeout- und Korrelationsgrenzen sind
  Schutzmechanismen, keine kumulativen Bodybudgets.

## Verbleibende Limits

| Limit | Bedeutung |
| --- | --- |
| `SecRequestBody*` / `SecResponseBody*` | Native Engine-Policy. |
| Envoy `max_request_bytes` | Grenze des vollständigen Authorization-Samples; ext_proc für Streaming verwenden. |
| Traefik `maxBodySize` | Grenze des vollständigen Authorization-Requests; native UDS für Streaming verwenden. |
| Traefik `maxResponseBodySize=32768` | Speicherschutz der Authorization-Antwort, nicht Inspection der Anwendungsresponse. |
| HAProxy-SPOP-Frame-/Nachrichtengröße | Ein begrenztes vollständiges Sample; widersprüchliches oder nicht unterstütztes Framing scheitert vor der Engine. |

Builds, statische Contracts und Komponententests belegen nur ihre eigene Ebene.
Das aktuelle Lieferergebnis und offene Nachweisgrenzen stehen einmalig im
[Abschluss von PR #410](pr-410-i12-closeout-20261024.de.md).
