# Lokales Make-Target-Audit

**Sprache:** [English](local-make-target-audit.md) | Deutsch

Erstellt: 2026-07-06
Aktualisiert: 2026-07-06

Umfang: Apache-, NGINX- und HAProxy-C-Standard-Checks mit lokaler
Abhaengigkeitsbereitstellung bzw. Cache-Referenzierung aus Framework
`ci/lib/common.sh`, plus lokale statische Checks, Compile-Checks,
Dokumentation, Report-Governance und Test-Matrix-Governance.

## Abhaengigkeitsquellen

| Abhaengigkeit | Lokale Quelle | Pfad | Ergebnis |
|---|---|---|---|
| Apache/APXS | Framework-Komponenten-Cache | `<verified-run-root>/component-cache/builds/connectors/apache/517a6c2a3f24c140ea3bb8bb8de23e5c05c0f98920507b237f66e2c37bb9ee6c/httpd/bin/apxs` | PASS |
| NGINX-Headers/Source | Framework-Komponenten-Cache | `<verified-run-root>/component-cache/builds/connectors/nginx/3a61dba1872aec9a36f06424d1db0c0dac957413f857a96b2950f39d0a341e1d/build/nginx-src` | PASS |
| HAProxy-Headers/Source | Framework-Komponenten-Cache | `<verified-run-root>/component-cache/sources/haproxy/haproxy-3.2.19` | PASS |
| libmodsecurity-Headers | Framework-Komponenten-Cache | `<verified-run-root>/component-cache/prefix/modsecurity/0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72/include` | PASS |

## Lokale Targets

| Target | Lokales Ergebnis | Grund |
|---|---|---|
| `make codex-check` | PASS | Statische Checks, Compile-Checks, Governance, Dokumentation, Workflows und Helper abgeschlossen |
| `make lint` | PASS | Static/Lint-Checks abgeschlossen; `actionlint` war lokal nicht verfuegbar und wurde gemaess Target-Policy ausgelassen |
| `make quick-check` | PASS | Schnelle Static-/Compile-/Governance-Checks abgeschlossen |
| `make report-governance` | PASS | Nur Generated-Report-Layout und Runtime-Path-Policy-Governance |
| `make check-test-matrix` | PASS | Test-Matrix-Generierung/Governance abgeschlossen; keine Runtime-Ausfuehrung |
| `python3 ci/checks/documentation/check-bilingual-docs.py` | PASS | Bilinguale Report-/Dokumentationslinks geprueft |
| `make check-bilingual-docs` | PASS | Makefile-Wrapper fuer bilinguale Report-/Dokumentationslinks geprueft |
| `git diff --check` | PASS | Keine Whitespace-Fehler im aktuellen Diff |
| `make check-common-helpers check-common-sdk-contract check-adapter-contracts check-directive-parity` | PASS | Common-Helper-, SDK-Contract-, Adapter- und Directive-Checks abgeschlossen |
| `make check-generated-report-layout verified-report-evidence-gate` | PASS | Nur statisches Generated-Report-Layout/Evidence-Gate |
| `make check-apache-common-adoption` | PASS | Apache Common-SDK-Strukturchecks abgeschlossen |
| `make check-apache-c17` | PASS | `apxs`, APR-Flags und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-apache-c23` | PASS | `apxs`, APR-Flags und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-apache-future-c` | PASS | `apxs`, APR-Flags und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-nginx-common-adoption` | PASS | NGINX Common-SDK-Strukturchecks abgeschlossen |
| `make check-nginx-c17` | PASS | NGINX-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-nginx-c23` | PASS | NGINX-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-nginx-future-c` | PASS | NGINX-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-haproxy-common-adoption` | PASS | HAProxy Common-SDK-Strukturchecks abgeschlossen |
| `make check-haproxy-c17` | PASS | HAProxy-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-haproxy-c23` | PASS | HAProxy-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-haproxy-future-c` | PASS | HAProxy-Source-Headers und libmodsecurity-Headers aus dem Framework-Cache aufgeloest |
| `make check-remaining-connectors-common-adoption` | PASS | Remaining-Connector-Strukturchecks abgeschlossen |
| `make check-remaining-connectors-c17` | PASS | Remaining-Connector-C17-Compile-Check abgeschlossen |
| `make check-remaining-connectors-c23` | PASS | Remaining-Connector-C23-Compile-Check abgeschlossen |
| `make check-remaining-connectors-future-c` | PASS | Remaining-Connector-future-C-Compile-Check abgeschlossen |
| `make check-remaining-connectors-c-standards` | PASS | Aggregierte Remaining-Connector-C-Standard-Checks abgeschlossen |

## CI-Policy-Probe

| Probe | Ergebnis | Grund |
|---|---|---|
| `GITHUB_ACTIONS=true make check-apache-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true make check-nginx-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true make check-haproxy-c17` | PASS | Vorhandener Framework-Cache war verfuegbar |
| `GITHUB_ACTIONS=true` mit leerem Cache, Apache-Skript | BLOCKED / 77 | CI provisioniert fehlendes APXS nicht lokal |
| `GITHUB_ACTIONS=true` mit leerem Cache, NGINX-Skript | BLOCKED / 77 | CI provisioniert fehlende NGINX-Headers nicht lokal |
| `GITHUB_ACTIONS=true` mit leerem Cache, HAProxy-Skript | BLOCKED / 77 | CI provisioniert fehlende HAProxy-Headers nicht lokal |

## Optionale Targets

| Target | Status | Grund |
|---|---|---|
| `make verified-report-governance` | Nicht vorhanden | Workflow existiert und fuehrt `make report-governance` aus; kein Makefile-Target vorhanden |
| `make check-generated-reports` | Nicht vorhanden | Kein Makefile-Target vorhanden |
| `make scaffold-lint` | Nicht vorhanden | Kein Makefile-Target vorhanden |

## Bewusst Nicht Ausgefuehrt

Der Runtime-Verifikationslauf wurde in diesem lokalen Audit bewusst nicht ausgefuehrt.

| Kategorie | Status | Grund |
|---|---|---|
| Runtime-Verifikationslauf | SKIPPED intentionally | Wuerde Live-Connector-/Server-Runtime-Checks starten |
| CRS-Runtime-Verifikation | SKIPPED intentionally | Wuerde CRS-Runtime-Cases ausfuehren |
| Full-Matrix-Runtime-Verifikation | SKIPPED intentionally | Wuerde Full-Runtime-Matrix-Jobs ausfuehren |
| Live Apache/NGINX/HAProxy Server-Verifikation | SKIPPED intentionally | Wuerde echte Server-Runtimes starten |
| Envoy/Traefik/lighttpd Runtime-Smokes | SKIPPED intentionally | Nicht Teil dieses lokalen Non-Runtime-Audits |
| Response-Body-Runtime-Verifikation | SKIPPED intentionally | Wuerde Runtime-Smoke-Ausfuehrung benoetigen |
