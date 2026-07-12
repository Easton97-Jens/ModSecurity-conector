# Full-Lifecycle-Runtime-Root-Audit

**Sprache:** [English](full-lifecycle-runtime-root-audit.md) | Deutsch

Dieser Bericht rekonstruiert nur Pfade und Binärmetadaten; er enthält keine rohen Umgebungswerte oder Payloads.

- Lauf-ID: `full-lifecycle-all-20260711T155358Z`
- Erstellt: `2026-07-11T18:59:19Z`

## apache

- Ziel: `full-lifecycle-apache`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/apache/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/apache/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/apache/ee6c15e623ee74d0660bf8324093bb11e60f807710e3d92d9d5242748605081b/httpd/bin/httpd`
- Aufgelöste Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/apache/ee6c15e623ee74d0660bf8324093bb11e60f807710e3d92d9d5242748605081b/httpd/bin/httpd`
- Existiert/ausführbar: `True` / `True`
- Eigentümer/SHA-256: `root:0 / c101941d42b9298a3802ce51db8b36b29a2fc2f112a9c6a85a29d83c913917a0`
- Fremder Connector-Root erkannt: `False`

## nginx

- Ziel: `full-lifecycle-nginx`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/nginx/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/nginx/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/nginx/2328a427520369bb45b0e36b442ba7d8a9eb8d7bea06f5b852ce757207e36cae/nginx/sbin/nginx`
- Aufgelöste Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/nginx/2328a427520369bb45b0e36b442ba7d8a9eb8d7bea06f5b852ce757207e36cae/nginx/sbin/nginx`
- Existiert/ausführbar: `True` / `True`
- Eigentümer/SHA-256: `root:0 / 870c91e0cb2234126f5b70e25c3bc089502efdfb53990faf0ad73bcccb24242e`
- Fremder Connector-Root erkannt: `True`

## haproxy

- Ziel: `full-lifecycle-haproxy`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/haproxy/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/haproxy/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/haproxy/04708323416d773dd2227dda20efdde5e92064f3f903cbdc2b099d3d03bfff8b/haproxy-runtime/haproxy/sbin/haproxy`
- Aufgelöste Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/builds/connectors/haproxy/04708323416d773dd2227dda20efdde5e92064f3f903cbdc2b099d3d03bfff8b/haproxy-runtime/haproxy/sbin/haproxy`
- Existiert/ausführbar: `True` / `True`
- Eigentümer/SHA-256: `root:0 / b228c1df80b1c1567f72db3a088b41cf148e7c3f39cb2e21591384aff2c1b1ba`
- Fremder Connector-Root erkannt: `True`

## envoy

- Ziel: `full-lifecycle-envoy`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/envoy/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/envoy/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/envoy/bin/envoy`
- Aufgelöste Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/envoy/bin/envoy`
- Existiert/ausführbar: `True` / `True`
- Eigentümer/SHA-256: `root:0 / 87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899`
- Fremder Connector-Root erkannt: `True`

## traefik

- Ziel: `full-lifecycle-traefik`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/traefik/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/traefik/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/traefik-connector/traefik-forwardauth`
- Aufgelöste Binärdatei: `fehlend`
- Existiert/ausführbar: `False` / `False`
- Eigentümer/SHA-256: `- / -`
- Fremder Connector-Root erkannt: `True`

## lighttpd

- Ziel: `full-lifecycle-lighttpd`
- Evidence-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/no-crs-evidence/lighttpd/full-lifecycle-all-20260711T155358Z`
- Raw-Run-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build/canonical-raw/no_crs_baseline/lighttpd/full-lifecycle-all-20260711T155358Z`
- Build-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/build`
- Komponenten-Cache-Root: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache`
- Erwartete Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/lighttpd/bin/lighttpd`
- Aufgelöste Binärdatei: `<historical-run-root:ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z>/component-cache/lighttpd/bin/lighttpd`
- Existiert/ausführbar: `True` / `True`
- Eigentümer/SHA-256: `root:0 / 83cb905568496eea3813eee5ab32ba9614f49b1479ece86acd0103617087ad97`
- Fremder Connector-Root erkannt: `True`

## Herleitung der Umgebung

- `BUILD_ROOT`: Makefile: VERIFIED_BUILD_ROOT defaultet auf VERIFIED_RUN_ROOT/build; ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh leitet den Wert unverändert weiter.
- `CONNECTOR_COMPONENT_CACHE`: Historisches Makefile/ci/provisioning/cache/with-runtime-components.sh leitete den Cache aus VERIFIED_RUN_ROOT/component-cache ab.
- `EVIDENCE_ROOT`: ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh leitete den historischen Default aus BUILD_ROOT/no-crs-evidence ab.
- `NO_CRS_RAW_ROOT`: Historisches ci/runtime/lifecycle/run-no-crs-baseline.sh leitete den Default aus BUILD_ROOT ab.
- `TRAEFIK_CONNECTOR_BIN`: Von connectors/traefik/scripts/runtime_smoke.py abgeleiteter historischer Default; keine explizite persistierte Zuweisung wurde gefunden.
- `VERIFIED_RUN_ROOT`: Aufruferumgebung der historischen kanonischen Aggregate-Ausführung.

## Erkenntnisse

- Das historische Aggregate reichte einen VERIFIED_RUN_ROOT an alle Connectoren weiter; nur Raw-Evidence-Unterverzeichnisse waren connector-spezifisch.
- Historisch las ci/runtime/lifecycle/run-no-crs-baseline.sh runtime-env.sh und manifest.json aus VERIFIED_RUN_ROOT/component-cache statt aus CONNECTOR_COMPONENT_CACHE.
- Das historische Traefik-Full-Lifecycle-Ziel startete runtime-smoke ohne forwardAuth-Build-Voraussetzung; der abgeleitete Binärpfad fehlte daher, statt nicht ausführbar zu sein.
- Der historische Make-Wrapper übersetzte einen Child-Exit 77 in einen Make-Fehlerstatus und verlor damit die ursprüngliche BLOCKED-Klassifikation an der Stage-Grenze.
