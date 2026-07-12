# NGINX-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: Laufzeitpfad im Besitz des Adapters, evidenzbezogen

Der NGINX-Connector ist ein dynamisches NGINX-HTTP-Modul, das libmodsecurity v3 verwendet
öffentliche C-APIs. Produktive Quelle steht unter `connectors/nginx/src/`; Modul
Build-Metadaten befinden sich in `connectors/nginx/config`.

## Laufzeitform

```text
HTTP client -> source-built NGINX -> ngx_http_modsecurity_module.so -> libmodsecurity -> HTTP response
```

NGINX besitzt serverspezifisches Verhalten:

- Zugriffsphasenhandler
- Protokollphasenhandler
- Header-Filter
- Körperfilter
- Haupt- und Standortkonfiguration erstellen/zusammenführen
- Erstellen und Laden dynamischer Module
- begrenzte Beweise für einen strikten Abbruch der Phase 4

Diese Flächen sind nicht connector-neutral und müssen darunter bleiben
`connectors/nginx/`.

## Aktuelle Beweise

- Standard-Laufzeitrauch: `60/60 PASS`.
- Alle Laufzeitbeweise erzwingen: `140 Versuche / 95 PASS / 39 FAIL /
  0 BLOCKIERT / 6 NOT_EXECUTABLE`.
- Aufbau und Smoke-Testfluss: `docs/build/compilers/nginx.md`.
- Generierter Detailbericht:
  `reports/testing/generated/nginx-runtime-results.generated.md`.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; begrenzte strikte Abbruchbeweise sind
nur als Laufzeitbeweis dokumentiert/gemeldet.

## Grenzen

Die gemeinsam genutzte Ebene `common/` kann Direktivennamen, Optionsstandards usw. enthalten
Datenformen. Es verfügt nicht über NGINX-Phasen, Filter, Request-Body-Handling,
Antworttextverarbeitung, Transaktionseigentum oder Serverlebenszyklusverhalten.

## Gemeinsame SDK-Einführungsschicht

Die NGINX-Architektur sorgt dafür, dass die NGINX-API-Verarbeitung lokal erfolgt, während sie gemeinsam genutzt wird
Semantik in das Common SDK. Die Standortkonfiguration bettet `msconnector_config` ein,
NGINX-Direktivenregistrierungen verwenden allgemeine Direktivenmakros/Spezifikationen/Adapter und Thin
Mapper-Funktionen konvertieren `ngx_http_request_t` plus Antwortstatus in
`msconnector_request`/`msconnector_response` unter Common Mapper-Verträgen. Körper
Nutzlasten werden nicht in Ereignissen, JSONL oder Protokollen ausgegeben; nur Metadaten wie Größen
und Trunkierungszustand dargestellt werden. C17-Kompilierungsprüfungen decken diese Übernahme ab
Oberfläche, wenn NGINX/libmodsecurity-Header vorhanden sind, während C23/future-C-Prüfungen vorhanden sind
optional und Compiler-abhängig. Bei diesen Prüfungen handelt es sich lediglich um Kompilierungs-/Strukturnachweise.
