# Full-Lifecycle Runtime-Root-Audit

**Language:** English | [Deutsch](full-lifecycle-runtime-root-audit.de.md)

This report reconstructs paths and binary metadata only; it contains no raw environment values or payloads.

- Run ID: `full-lifecycle-all-20260711T155358Z`
- Generated: `2026-07-11T18:59:19Z`

## apache

- Target: `full-lifecycle-apache`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/apache/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/apache/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/apache/ee6c15e623ee74d0660bf8324093bb11e60f807710e3d92d9d5242748605081b/httpd/bin/httpd`
- Resolved binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/apache/ee6c15e623ee74d0660bf8324093bb11e60f807710e3d92d9d5242748605081b/httpd/bin/httpd`
- Exists/executable: `True` / `True`
- Owner/SHA-256: `root:0 / c101941d42b9298a3802ce51db8b36b29a2fc2f112a9c6a85a29d83c913917a0`
- Foreign connector root detected: `False`

## nginx

- Target: `full-lifecycle-nginx`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/nginx/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/nginx/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/nginx/2328a427520369bb45b0e36b442ba7d8a9eb8d7bea06f5b852ce757207e36cae/nginx/sbin/nginx`
- Resolved binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/nginx/2328a427520369bb45b0e36b442ba7d8a9eb8d7bea06f5b852ce757207e36cae/nginx/sbin/nginx`
- Exists/executable: `True` / `True`
- Owner/SHA-256: `root:0 / 870c91e0cb2234126f5b70e25c3bc089502efdfb53990faf0ad73bcccb24242e`
- Foreign connector root detected: `True`

## haproxy

- Target: `full-lifecycle-haproxy`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/haproxy/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/haproxy/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/haproxy/04708323416d773dd2227dda20efdde5e92064f3f903cbdc2b099d3d03bfff8b/haproxy-runtime/haproxy/sbin/haproxy`
- Resolved binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/builds/connectors/haproxy/04708323416d773dd2227dda20efdde5e92064f3f903cbdc2b099d3d03bfff8b/haproxy-runtime/haproxy/sbin/haproxy`
- Exists/executable: `True` / `True`
- Owner/SHA-256: `root:0 / b228c1df80b1c1567f72db3a088b41cf148e7c3f39cb2e21591384aff2c1b1ba`
- Foreign connector root detected: `True`

## envoy

- Target: `full-lifecycle-envoy`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/envoy/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/envoy/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/envoy/bin/envoy`
- Resolved binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/envoy/bin/envoy`
- Exists/executable: `True` / `True`
- Owner/SHA-256: `root:0 / 87744a1fc998d677078c9703113a192d0830badc6888662441632847fcb38899`
- Foreign connector root detected: `True`

## traefik

- Target: `full-lifecycle-traefik`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/traefik/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/traefik/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/traefik-connector/traefik-forwardauth`
- Resolved binary: `missing`
- Exists/executable: `False` / `False`
- Owner/SHA-256: `- / -`
- Foreign connector root detected: `True`

## lighttpd

- Target: `full-lifecycle-lighttpd`
- Evidence root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/no-crs-evidence/lighttpd/full-lifecycle-all-20260711T155358Z`
- Raw run root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build/canonical-raw/no_crs_baseline/lighttpd/full-lifecycle-all-20260711T155358Z`
- Build root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/build`
- Component cache root: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache`
- Expected binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/lighttpd/bin/lighttpd`
- Resolved binary: `/var/tmp/ModSecurity-conector-full-lifecycle-apache-first-byte-20260711T142155Z/component-cache/lighttpd/bin/lighttpd`
- Exists/executable: `True` / `True`
- Owner/SHA-256: `root:0 / 83cb905568496eea3813eee5ab32ba9614f49b1479ece86acd0103617087ad97`
- Foreign connector root detected: `True`

## Environment derivation

- `VERIFIED_RUN_ROOT`: caller environment of the historical canonical aggregate invocation
- `BUILD_ROOT`: Makefile: VERIFIED_BUILD_ROOT defaults to VERIFIED_RUN_ROOT/build and ci/run-full-lifecycle-all-connectors.sh forwards it unchanged
- `EVIDENCE_ROOT`: ci/run-full-lifecycle-all-connectors.sh defaults it from BUILD_ROOT/no-crs-evidence
- `NO_CRS_RAW_ROOT`: ci/run-no-crs-baseline.sh default derived from BUILD_ROOT
- `CONNECTOR_COMPONENT_CACHE`: Makefile/ci/with-runtime-components.sh default derived from VERIFIED_RUN_ROOT/component-cache
- `TRAEFIK_CONNECTOR_BIN`: connectors/traefik/scripts/runtime_smoke.py inferred default; no explicit persisted assignment was recorded

## Findings

- The historical aggregate forwarded one VERIFIED_RUN_ROOT to every connector; only raw evidence subdirectories were connector-qualified.
- ci/run-no-crs-baseline.sh historically read runtime-env.sh and manifest.json from VERIFIED_RUN_ROOT/component-cache instead of CONNECTOR_COMPONENT_CACHE.
- The Traefik full-lifecycle target dispatched runtime-smoke without a forwardAuth build prerequisite, so the inferred binary path was missing rather than non-executable.
- The historical Make wrapper translated a child Exit 77 into a Make failure status, losing the original BLOCKED classification at the stage boundary.
