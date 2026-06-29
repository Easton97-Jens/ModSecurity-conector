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

# MRTS Native Infrastructure Report

**Sprache:** [English](mrts-native-full.generated.md) | Deutsch

Erstellt unter: `2026-06-19T16:58:10Z`

## Zusammenfassung
- PASS: **0**
- FAIL: **2**
- BLOCKED: **0**
- NOT_RUN: **0**

## Native Berichte aufteilen
- Apache nativ: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 nativ: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native Zusammenfassung: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Kombinierter nativer Bericht: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Diese nativen MRTS-Berichte sind vom Connector-Vollmatrixbeweis getrennt.

## Zusammenfassung des nativen Ziels
| Target | Status | Classification | Critical blocker | Attempted | PASS | FAIL | BLOCKED | Reason | Run log | Summary |
|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| apache2_ubuntu | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/apache2_ubuntu/run.log` | `$MRTS_NATIVE_ROOT/apache2_ubuntu/job.json` |
| nginx-pr24 | FAIL | `optional_native_modsecurity_semantics_difference` | false | 13 | 12 | 1 | 0 | native MRTS go-ftw run failed | `$MRTS_NATIVE_ROOT/nginx-pr24/run.log` | `$MRTS_NATIVE_ROOT/nginx-pr24/job.json` |

## Apache2 Ubuntu Native Infra
- Quelle: `$MRTS_ROOT/config_infra/apache2_ubuntu` inszeniert unter `MRTS_NATIVE_ROOT`.
- Der Nachweis ist ein nativer MRTS-Infrastrukturbeweis und ersetzt nicht den Nachweis für Connector-Smoke.

## NGINX PR24 Native Infra
- PR URL: https://github.com/owasp-modsecurity/MRTS/pull/24
- PR Nummer: 24
- PR Kopf SHA: `134ea7e35d72e7d72294b66d80dafa07daa5fc92`
- Aufgenommen bei UTC: `2026-06-09T15:18:21Z`
- Upstream-Status: `open-pr`
- Stabilität: `experimental`
- Ersetzungshinweis: Nach der Zusammenführung im Upstream durch $MRTS_ROOT/config_infra/nginx_linux ersetzen

## Bekannte Einschränkungen
- Phase 4 und RESPONSE_BODY native Nachweise werden weiterhin nicht promoted.
- Fehlende native Binärdateien, Module, Go-FTW oder Backend-Tools werden als BLOCKIERT gemeldet.

## Fehlende Abhängigkeitsbehebung
- In diesem Lauf wurden keine fehlenden nativen Abhängigkeiten gemeldet.

## Vergleichshinweise
- Vergleichen Sie native MRTS-Ergebnisse mit Connector-Smoke-Nachweisen nach Ziel und Korpus.
- Klassifizierungsmetadaten erklären Lücken, ändern aber nie die Laufzeit PASS/FAIL/BLOCKED.

## Leitplanken
- Natives Staging erfolgt gemäß `MRTS_NATIVE_ROOT`; Repository-Quellen sind schreibgeschützte Eingaben.
- `tools/MRTS`- und MRTS-Definitionen werden durch die native Berichtsgenerierung nicht bearbeitet.
- Generierte MRTS-Regeln, go-ftw YAML, Ladedateien, Protokolle und native Ergebnisse werden nicht festgeschrieben.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/mrts-native/apache2_ubuntu/job.json` | `234ac210219fe61948da3815ed6587a21d86497fad6ef1a2a4d67acab12f1eda` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/mrts-native/nginx-pr24/job.json` | `161d7c17ed090bfe0cb7842c33c98251d8d217b73de5f09e8b886a5cbc0970a7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/mrts-native/apache2_ubuntu/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/mrts-native/nginx-pr24/job.json` | present | input file available |
