# Local Make Target Audit

**Language:** English | [Deutsch](local-make-target-audit.de.md)

Generated: 2026-07-06
Updated: 2026-07-06

Scope: Apache, NGINX, and HAProxy C-standard checks using Framework `ci/common.sh`
local dependency provisioning/reference helpers, plus local static,
compile, documentation, report-governance, and test-matrix governance checks.

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
| `make codex-check` | PASS | Static, compile, governance, docs, workflow, and helper checks completed |
| `make lint` | PASS | Static/lint checks completed; `actionlint` was unavailable locally and skipped by target policy |
| `make quick-check` | PASS | Quick static/compile/governance checks completed |
| `make report-governance` | PASS | Generated-report layout and runtime path policy governance only |
| `make check-test-matrix` | PASS | Test matrix generation/governance completed; no runtime execution |
| `python3 ci/check-bilingual-docs.py` | PASS | Bilingual report/doc links checked |
| `make check-bilingual-docs` | PASS | Makefile wrapper for bilingual report/doc links checked |
| `git diff --check` | PASS | No whitespace errors in current diff |
| `make check-common-helpers check-common-sdk-contract check-adapter-contracts check-directive-parity` | PASS | Common helper, SDK contract, adapter, and directive checks completed |
| `make check-generated-report-layout verified-report-evidence-gate` | PASS | Static generated-report layout/evidence gate only |
| `make check-apache-common-adoption` | PASS | Apache Common SDK structure checks completed |
| `make check-apache-c17` | PASS | `apxs`, APR flags, and libmodsecurity headers resolved from Framework cache |
| `make check-apache-c23` | PASS | `apxs`, APR flags, and libmodsecurity headers resolved from Framework cache |
| `make check-apache-future-c` | PASS | `apxs`, APR flags, and libmodsecurity headers resolved from Framework cache |
| `make check-nginx-common-adoption` | PASS | NGINX Common SDK structure checks completed |
| `make check-nginx-c17` | PASS | NGINX source headers and libmodsecurity headers resolved from Framework cache |
| `make check-nginx-c23` | PASS | NGINX source headers and libmodsecurity headers resolved from Framework cache |
| `make check-nginx-future-c` | PASS | NGINX source headers and libmodsecurity headers resolved from Framework cache |
| `make check-haproxy-common-adoption` | PASS | HAProxy Common SDK structure checks completed |
| `make check-haproxy-c17` | PASS | HAProxy source headers and libmodsecurity headers resolved from Framework cache |
| `make check-haproxy-c23` | PASS | HAProxy source headers and libmodsecurity headers resolved from Framework cache |
| `make check-haproxy-future-c` | PASS | HAProxy source headers and libmodsecurity headers resolved from Framework cache |
| `make check-remaining-connectors-common-adoption` | PASS | Remaining connector structure checks completed |
| `make check-remaining-connectors-c17` | PASS | Remaining connector C17 compile check completed |
| `make check-remaining-connectors-c23` | PASS | Remaining connector C23 compile check completed |
| `make check-remaining-connectors-future-c` | PASS | Remaining connector future-C compile check completed |
| `make check-remaining-connectors-c-standards` | PASS | Remaining connector aggregate C standard checks completed |

## CI Policy Probe

| Probe | Result | Reason |
|---|---|---|
| `GITHUB_ACTIONS=true make check-apache-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true make check-nginx-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true make check-haproxy-c17` | PASS | Existing Framework cache was available |
| `GITHUB_ACTIONS=true` with empty cache, Apache script | BLOCKED / 77 | CI intentionally does not local-provision missing APXS |
| `GITHUB_ACTIONS=true` with empty cache, NGINX script | BLOCKED / 77 | CI intentionally does not local-provision missing NGINX headers |
| `GITHUB_ACTIONS=true` with empty cache, HAProxy script | BLOCKED / 77 | CI intentionally does not local-provision missing HAProxy headers |

## Optional Targets

| Target | Status | Reason |
|---|---|---|
| `make verified-report-governance` | Not present | Workflow exists and runs `make report-governance`; no Makefile target exists |
| `make check-generated-reports` | Not present | No Makefile target exists |
| `make scaffold-lint` | Not present | No Makefile target exists |

## Intentionally Not Executed

Runtime verification was intentionally not executed in this local audit.

| Category | Status | Reason |
|---|---|---|
| Runtime verification run | SKIPPED intentionally | Would start live connector/server runtime checks |
| CRS runtime verification | SKIPPED intentionally | Would execute CRS runtime cases |
| Full-matrix runtime verification | SKIPPED intentionally | Would execute full runtime matrix jobs |
| Live Apache/NGINX/HAProxy server verification | SKIPPED intentionally | Would start real server runtimes |
| Envoy/Traefik/lighttpd runtime smokes | SKIPPED intentionally | Out of scope for this local non-runtime audit |
| Response body runtime verification | SKIPPED intentionally | Would require runtime smoke execution |
