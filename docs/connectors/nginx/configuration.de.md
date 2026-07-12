<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# NGINX-Konfiguration

**Sprache:** [English](configuration.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Konfigurationsmodell

Der Adapter verwendet vorhandene NGINX-Direktiven wie `modsecurity on` und `modsecurity_rules_file`. Dynamisches Modul, Prefix und Phase-4-Modus werden über vorhandene Harness-Variablen gewählt.

## Minimal, Safe und Strict

Die [annotierten NGINX-Beispiele](../../../examples/nginx/README.de.md) sind die vollständige lokale Quelle. Ersetzen Sie jeden Pfad, Port und Endpoint für den Zielhost. Minimal und Safe gehören zum dokumentierten Kern; Strict wird nur dort beschrieben, wo der Host und aktuelle Evidence es tragen. Kopieren Sie keine Kompatibilitätskonfiguration als ausgewählten Kernpfad.

## Defaults, Body-Scope und Logging

Nur vorhandene Hostdirektiven und Harness-Optionen sind in den Beispielen aufgeführt. Body- und Content-Type-Verhalten bleiben host- und profilgebunden; keine Konfiguration erlaubt einen connector-eigenen vollständigen Response-Buffer. Nutzen Sie payloadfreie Connector-/Evidence-Logs und speichern Sie keine Secrets in Regeln, Pfaden oder Kommandozeilen.

## Validierung

Führen Sie `make check-config-nginx` vor dem Start aus. Der Kernlauf `make full-lifecycle-nginx` benötigt beschreibbare Runtime- und Evidence-Roots; prüfen Sie das Ergebnis immer anhand der Artefakte.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `NGINX_PREFIX` | Optional | absolute generated prefix | Provisioning or caller | `/srv/modsecurity-work/nginx-runtime/nginx` |
| `NGINX_BINARY` | Optional | executable NGINX path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/sbin/nginx` |
| `NGINX_MODULE` | Optional | dynamic module path | Derived from `NGINX_PREFIX` | `<nginx-prefix>/modules/ngx_http_modsecurity_module.so` |
| `NGINX_PHASE4_MODE` | Optional | `minimal`, `safe`, or `strict` where host supports it | Caller/harness | `safe` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
