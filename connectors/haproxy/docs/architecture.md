# HAProxy Scaffold Architecture

## Ziel

Dieses Dokument überträgt den adapter-owned Ansatz als Scaffold auf HAProxy.
Es beschreibt Optionen und offene Fragen, keine Implementierungszusage.

## Adapter-owned Grundsatz

- HAProxy-spezifische Build-/Runtime-Logik bleibt unter `connectors/haproxy/`.
- Gemeinsame, connector-neutrale Metadaten dürfen genutzt werden, wo passend.
- Server-Lifecycle und Runtime-Semantik sind HAProxy-spezifisch und noch zu
  prüfen.

## HAProxy-Lifecycle (noch zu prüfen)

- Start-/Stop-Verhalten in lokalen und CI-Umgebungen
- Reload-Semantik und Nebenwirkungen
- Worker-/Process-Modell und Zustandsgrenzen
- Request-/Response-Hookpunkte für ModSecurity-Entscheidungen

## Mögliche Integrationsmodelle (Optionen, keine Entscheidung)

- SPOE/SPOA-Modell
- Native Erweiterung/Filtermodell
- Lua-basierter Ansatz
- Externer Prüfservice

Hinweis: Diese Optionen sind als Arbeitsliste zu verstehen. Keine Option ist
hier als entschieden oder funktionsfähig belegt.

## Klare Nicht-Zusagen

- Apache-/NGINX-Runtime-Code darf nicht ungeprüft kopiert werden.
- Es wird keine Runtime-Parität mit Apache/NGINX behauptet.
- Response-Body-/Streaming-Verhalten ist noch zu prüfen.
