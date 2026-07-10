# Traefik Connector

Status: `minimal_runtime_smoke` ausschließlich für den `forwardAuth`-Request-Pfad.
Der Connector besitzt einen eigenen C17-Entry-Point und bleibt für Request-Body,
Upstream-Response, CRS, Security, Produktion und Full Matrix bewusst
`not_verified` / `connector-gap`.

- Common Config wird über `traefik_modsecurity_config_init()` initialisiert.
- Request- und Response-Mapper sind dünne Funktionen, keine Makro-Aliase.
- `traefik_forwardauth_service_main.c` registriert das Hostprofil beim neutralen
  HTTP-Authorization-Service; `X-Forwarded-Uri` hat Vorrang.
- Der Build ist compile-/link-only; Config-Check und Start-Smoke sind getrennt.
  Der Start-Smoke startet Service und echtes Traefik mit temporärer
  forwardAuth-File-Provider-Config, sendet aber keine Requests.
- Response-Header/-Body des Upstreams sind für `forwardAuth` nicht verfügbar.
- Es gibt keine Produktions-, CRS-, Full-Matrix-, Runtime- oder RESPONSE_BODY-Verifikationsbehauptung.
