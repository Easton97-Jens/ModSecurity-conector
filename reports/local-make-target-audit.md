# Local Make Target Audit

**Language:** English | [Deutsch](local-make-target-audit.de.md)

Generated: 2026-07-06

Scope: Apache, NGINX, and HAProxy C-standard checks using Framework `ci/common.sh`
local dependency provisioning/reference helpers.

## Dependency Sources

| Dependency | Local source | Path | Result |
|---|---|---|---|
| Apache/APXS | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | PASS |
| NGINX headers/source | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/build/nginx-src` | PASS |
| HAProxy headers/source | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/sources/haproxy/haproxy-3.2.19` | PASS |
| libmodsecurity headers | Framework component cache | `/var/tmp/ModSecurity-conector-verified/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include` | PASS |

## Local Targets

| Target | Local result | Reason |
|---|---|---|
| `env -u GITHUB_ACTIONS -u CI make check-apache-c17` | PASS | `apxs` and APR flags resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-apache-c23` | PASS | `apxs` and APR flags resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-apache-future-c` | PASS | `apxs` and APR flags resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-c17` | PASS | NGINX source headers resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-c23` | PASS | NGINX source headers resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-nginx-future-c` | PASS | NGINX source headers resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-c17` | PASS | HAProxy source headers resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-c23` | PASS | HAProxy source headers resolved from Framework cache |
| `env -u GITHUB_ACTIONS -u CI make check-haproxy-future-c` | PASS | HAProxy source headers resolved from Framework cache |

## CI Policy Probe

| Probe | Result | Reason |
|---|---|---|
| `GITHUB_ACTIONS=true make check-apache-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true make check-nginx-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true make check-haproxy-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true` with empty cache, Apache script | BLOCKED / 77 | CI intentionally does not local-provision missing APXS |
| `GITHUB_ACTIONS=true` with empty cache, NGINX script | BLOCKED / 77 | CI intentionally does not local-provision missing NGINX headers |
| `GITHUB_ACTIONS=true` with empty cache, HAProxy script | BLOCKED / 77 | CI intentionally does not local-provision missing HAProxy headers |
