# GitHub Actions-Aktualisierungsbericht

**Sprache:** [English](actions-update-report.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Dieser Bericht scannt `uses:`-Einträge in Root-Workflow-Dateien und dem angebotenen Framework-Modul.
Lokale Aktionen, Docker-Aktionen, dynamische Ausdrücke und SHA-gepinnte Aktionen werden nicht automatisch aktualisiert.

## Zusammenfassung

- `uses:`-Einträge gefunden: 33
- Aktualisierte Einträge: 0
- Bereits aktuelle Einträge: 24
- SHA-gepinnte Einträge: 0
- Übersprungene local/Docker/dynamic-Einträge: 0
- Übersprungene Submodul-Schreibvorgänge: 7
- Unbekannte Einträge: 2
- Fehler: 0
- Framework-Modul ist Submodul: ja

## Einträge

| Status | File | Line | Action | Current ref | New ref | Repository | Note |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| Unknown | .github/workflows/check-actions-versions.yml | 16 | actions/checkout | v7 | v7.0.0 | main | current ref was not found in releases; not downgrading |
| OK | .github/workflows/check-actions-versions.yml | 20 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/cleanup-artifacts.yml | 18 | actions/github-script | v8 | v8 | main | latest from releases |
| OK | .github/workflows/lint.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/lint.yml | 19 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/quick-framework-check.yml | 16 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/quick-framework-check.yml | 21 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/test-apache.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-apache.yml | 19 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/test-common.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-common.yml | 19 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/test-envoy.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-full-smoke-sequential.yml | 33 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-full-smoke-sequential.yml | 91 | actions/github-script | v8 | v8 | main | latest from releases |
| OK | .github/workflows/test-full-smoke-sequential.yml | 193 | actions/upload-artifact | v7.0.1 | v7.0.1 | main | latest from releases |
| OK | .github/workflows/test-haproxy.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-lighttpd.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-nginx.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/test-nginx.yml | 19 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/test-traefik.yml | 14 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| Unknown | .github/workflows/update-actions-versions.yml | 21 | actions/checkout | v7 | v7.0.0 | main | current ref was not found in releases; not downgrading |
| OK | .github/workflows/update-actions-versions.yml | 26 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| OK | .github/workflows/update-actions-versions.yml | 47 | actions/github-script | v8 | v8 | main | latest from releases |
| OK | .github/workflows/update-actions-versions.yml | 149 | actions/upload-artifact | v7.0.1 | v7.0.1 | main | latest from releases |
| OK | .github/workflows/verified-report-governance.yml | 16 | actions/checkout | v7.0.0 | v7.0.0 | main | latest from releases |
| OK | .github/workflows/verified-report-governance.yml | 21 | actions/setup-python | v6.2.0 | v6.2.0 | main | latest from releases |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml | 18 | actions/checkout | v6 | v7.0.0 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml | 20 | actions/setup-python | v6 | v6.2.0 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml | 50 | actions/github-script | v7 | v8 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/check-common-versions.yml | 152 | actions/upload-artifact | v7 | v7.0.1 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/cleanup-artifacts.yml | 18 | actions/github-script | v7 | v8 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/lint.yml | 14 | actions/checkout | v6 | v7.0.0 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
| Skipped submodule write | modules/ModSecurity-test-Framework/.github/workflows/test-common.yml | 14 | actions/checkout | v6 | v7.0.0 | module | module is a submodule; set SUBMODULE_UPDATE_TOKEN to write module updates |
