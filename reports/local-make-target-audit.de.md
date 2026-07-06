# Lokales Make-Target-Audit

**Sprache:** [English](local-make-target-audit.md) | Deutsch

Erstellt: 2026-07-06

Umfang: Apache-, NGINX- und HAProxy-C-Standard-Checks mit lokaler
Abhaengigkeitsbereitstellung bzw. Cache-Referenzierung aus Framework
`ci/common.sh`.

## Abhaengigkeitsquellen

| Abhaengigkeit | Lokale Quelle | Pfad | Ergebnis |
|---|---|---|---|
| Apache/APXS | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | PASS |
| NGINX-Headers/Source | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/build/nginx-src` | PASS |
| HAProxy-Headers/Source | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/sources/haproxy/haproxy-3.2.19` | PASS |
| libmodsecurity-Headers | Framework-Komponenten-Cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include` | PASS |

## Lokale Targets

| Target | Lokales Ergebnis | Grund |
|---|---|---|
| `env -u GITHUB_ACTIONS -u CI make check-apache-c17` | PASS | `apxs` und APR-Flags aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-apache-c23` | PASS | `apxs` und APR-Flags aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-apache-future-c` | PASS | `apxs` und APR-Flags aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-c17` | PASS | NGINX-Source-Headers aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-c23` | PASS | NGINX-Source-Headers aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-future-c` | PASS | NGINX-Source-Headers aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-c17` | PASS | HAProxy-Source-Headers aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-c23` | PASS | HAProxy-Source-Headers aus dem Framework-Cache aufgeloest |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-future-c` | PASS | HAProxy-Source-Headers aus dem Framework-Cache aufgeloest |

## CI-Policy-Probe

| Probe | Ergebnis | Grund |
|---|---|---|
| `GITHUB_ACTIONS=true make check-apache-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true make check-nginx-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true make check-haproxy-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true` mit leerem Cache, Apache-Skript | BLOCKED / 77 | CI provisioniert fehlendes APXS nicht lokal |
| `GITHUB_ACTIONS=true` mit leerem Cache, NGINX-Skript | BLOCKED / 77 | CI provisioniert fehlende NGINX-Headers nicht lokal |
| `GITHUB_ACTIONS=true` mit leerem Cache, HAProxy-Skript | BLOCKED / 77 | CI provisioniert fehlende HAProxy-Headers nicht lokal |
