> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:10Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `framework:ci/generate-mrts-native-report.py`
> Ziel erstellen: `mrts-native-full-run`
> Besitzer: `mrts`
> Schweregrad: `optional`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

<!-- retained-historical-generated-output -->
> Aktueller Refresh-Status: `skipped_missing_input`. Dieser Report bewahrt einen früheren evidenztragenden Snapshot, weil keine neuen verifizierten Eingaben vorliegen. Grund: required input missing or empty.

# MRTS Native NGINX PR24 Bericht

**Sprache:** [English](mrts-native-nginx.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Erstellt unter: `2026-06-19T16:58:10Z`

## Ziel
- Ziel: `nginx-pr24`
- Quelle: `Framework PR24 overlay`
- PR Quelle: https://github.com/owasp-modsecurity/MRTS/pull/24
- Infrastruktur: MRTS PR24 NGINX + libmodsecurity3 native Infrastruktur
- Native MRTS-Nachweise sind von Connector-Vollmatrixbeweisen getrennt.

## PR Metadaten
- PR Nummer: `24`
- PR Kopf SHA: `134ea7e35d72e7d72294b66d80dafa07daa5fc92`
- Captured_at_utc: `2026-06-09T15:18:21Z`
- upstream_status: `open-pr`
- Stabilität: `experimental`
- Ersatzhinweis: Nach der Zusammenführung im Upstream durch $MRTS_ROOT/config_infra/nginx_linux ersetzen

## Status
- Status: **FAIL**
- Klassifizierung: `optional_native_modsecurity_semantics_difference`
- Optionaler Nachweis: `true`
- Kritischer Merge-Blocker: `false`
- Hinweise: Apache und NGINX native MRTS erreichen das Backend und schlagen nur bei Fall 100003-1 fehl, dem ARGS-Vergleich der Phase 4.

## Zählt
- versucht: **13**
- bestanden: **12**
- fehlgeschlagen: **1**
- blockiert: **0**
- nicht_ausführbar: **0**

## Bekannte Einschränkungen
- `phase4_native_limitation`
- `RESPONSE_BODY non-promoted`

## Erste fehlgeschlagene Fälle
- Fall: `100003-1`
Regel ID: `100003`
  Phase: `4`
  Variable/target: `ARGS` / `ARGS`
  Erwartet: HTTP 200 Backend-Antwort plus ModSecurity-Protokoll-ID 100003
  Tatsächlich: HTTP 200 Backend-Antwort beobachtet; erwartete Phase-4-Protokoll-ID 100003 fehlt
  Klassifizierung: `native_modsecurity_semantics` / `phase4_native_limitation`
  Zusammenfassung der Nachweise: Native ModSecurity erreicht die Anforderungs- und frühere Anforderungserfassungsphasen, aber die ARGS-Regel der Phase 4 protokolliert keine nativen Apache- oder NGINX-Nachweise.
  Regel: `SecRule ARGS "@contains attack" "id:100003, phase:4, deny, t:none, log"`
  Anfrage: `POST /?foo=attack`

## Laufzeitkomponenten
- MRTS_NATIVE_NGINX_BIN: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/sbin/nginx`
- MRTS_NATIVE_NGINX_MODULE_DIR: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules`
- ngx_http_modsecurity_module_so: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/nginx/d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12/nginx/modules/ngx_http_modsecurity_module.so`
- Connector_build_id: `d2677435815a2aede4a9886c78a8bc4c79d43ddaa387735b77e0ea9480e32f12`
- modsecurity_build_id: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- go_ftw_binary: `$CONNECTOR_COMPONENT_CACHE/bin/go-ftw`
- albedo_binary: `$CONNECTOR_COMPONENT_CACHE/bin/albedo`

## Wege
- staged_infra_path: `$MRTS_NATIVE_ROOT/nginx-pr24/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/nginx-pr24/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/nginx-pr24/job.json`

## Leitplanken
- tools/MRTS schreibgeschützt
- Systempfade sind schreibgeschützt
- Es wurden keine generierten MRTS-Artefakte festgeschrieben
- Native MRTS-Nachweise sind von Connector-Vollmatrixbeweisen getrennt

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | `161d7c17ed090bfe0cb7842c33c98251d8d217b73de5f09e8b886a5cbc0970a7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/build/mrts-native/nginx-pr24/job.json` | present | input file available |
