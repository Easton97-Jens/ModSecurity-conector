<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Open-Connector-Build-Wege

**Sprache:** [English](overview.md) | Deutsch

## Zweck

Envoy, Traefik und lighttpd verwenden repository-eigene Build- und
Runtime-Komponenten. Dieser Index fasst nur ihre aktuellen ausgewählten Wege
zusammen; alle Details stehen in den Einzelanleitungen und in der
[vollständigen Compilerübersicht](README.de.md).

| Connector | Anleitung | explizite Runtime-Vorbereitung | Full Lifecycle | ausgewähltes Profil |
| --- | --- | --- | --- | --- |
| [Envoy](envoy.de.md) | `prepare-envoy-runtime` | `full-lifecycle-envoy-ext-proc` | `ext_proc` |
| [Traefik](traefik.de.md) | `prepare-traefik-runtime` | `full-lifecycle-traefik-native` | `native-middleware` |
| [lighttpd](lighttpd.de.md) | `prepare-lighttpd-runtime-build` | `full-lifecycle-lighttpd-patched` | `patched-native` |

## Aktiver Weg

1. `make check-framework` ausführen.
2. Die in der Tabelle genannte Runtime-Vorbereitung ausführen, wenn ein Host
   oder dessen Cache-Eingabe noch fehlt.
3. `make build-<connector>`, `make check-config-<connector>`,
   `make start-smoke-<connector>` und `make runtime-smoke-<connector>` als
   getrennte Stufen ausführen.
4. Mit einem sicheren `NO_CRS_RUN_ID` den tabellierten Full-Lifecycle-Target
   und anschließend `make evidence-check-<connector>` ausführen.

Der Build von Envoys `ext_authz`-Service, Traefiks ForwardAuth-Service oder
einer lighttpd-Bridge kann als Kompatibilitätsdiagnose vorkommen. Keine dieser
Routen ersetzt den tabellierten ext_proc-, native-middleware- oder
patched-native-Hostweg.

## Versionen, Cache und Grenzen

`make runtime-components-inventory` und `make runtime-components-sources`
zeigen die vorbereitete Cache-v2-Provenienz. Ein erfolgreiches Herunterladen,
Entpacken, Bauen, Konfigurationsladen oder Starten ist noch kein
Produktions-, CRS-, HTTP/2-, HTTP/3-, Strict- oder vollständiger
Capability-Nachweis. Siehe die [Variablenreferenz](../../configuration/variables.de.md)
und die [Evidenzregeln](../../evidence/README.de.md).
