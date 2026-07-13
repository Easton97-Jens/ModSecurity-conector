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

# MRTS Nativer Apache-Bericht

**Sprache:** [English](mrts-native-apache.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Erstellt unter: `2026-06-19T16:58:10Z`

## Ziel
- Ziel: `apache2_ubuntu`
- Quelle: `$MRTS_ROOT/config_infra/apache2_ubuntu`
- Infrastruktur: MRTS Upstream-Apache2-Ubuntu-native Infrastruktur
- Native MRTS-Nachweise sind von Connector-Vollmatrixbeweisen getrennt.

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
- APACHECTL_BIN: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/apachectl-mrts`
- httpd_binary: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/httpd/bin/httpd`
- mod_security3_so: `$CONNECTOR_COMPONENT_CACHE/builds/connectors/apache/898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67/build/output/apache/mod_security3.so`
- Connector_build_id: `898f5881e3417828948d291bba3adef6f4ab922b4eba6611bea0d8724727cc67`
- modsecurity_build_id: `0c409318fd2de4832f756d82abd85ef2c99e9e31d002a7bfc7d97ed83ab9bb72`
- go_ftw_binary: `$CONNECTOR_COMPONENT_CACHE/bin/go-ftw`
- albedo_binary: `$CONNECTOR_COMPONENT_CACHE/bin/albedo`

## Wege
- staged_infra_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/stage/infra`
- run_log_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log`
- job_json_path: `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json`

## Leitplanken
- tools/MRTS schreibgeschützt
- Systempfade sind schreibgeschützt
- Es wurden keine generierten MRTS-Artefakte festgeschrieben
- Native MRTS-Nachweise sind von Connector-Vollmatrixbeweisen getrennt

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json` | `234ac210219fe61948da3815ed6587a21d86497fad6ef1a2a4d67acab12f1eda` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `<verified-run-root>/build/mrts-native/apache2_ubuntu/job.json` | present | input file available |
