> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:57:56Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-full-runtime-matrix.py`
> Ziel erstellen: `generate-full-runtime-matrix`
> Besitzer: `connector`
> Schweregrad: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# Vollständige MRTS Laufzeitmatrix

**Sprache:** [English](full-runtime-matrix.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

Generierte Datei – nicht manuell bearbeiten.

- Erstellt unter: `2026-06-19T16:57:56Z`
- Variante läuft: **12**
- Gesamtversuche: **3928**
- Gesamt PASS/FAIL/BLOCKED/NOT_EXECUTABLE: **3157** / **771** / **0** / **0**
- Ausstehende Metadatenzeilen, die in Laufzeitzusammenfassungen beobachtet wurden: **2298**

## Variantenergebnisse
| Connector | Test variant | MRTS variant | Outcome | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending | Duration seconds | Summary | Log |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| apache | no-crs | no-mrts | FAIL | 133 | 122 | 11 | 0 | 0 | 0 | 342 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/apache/run.log |
| nginx | no-crs | no-mrts | FAIL | 140 | 115 | 25 | 0 | 0 | 0 | 577 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/nginx/run.log |
| haproxy | no-crs | no-mrts | FAIL | 133 | 122 | 11 | 0 | 0 | 0 | 278 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/no-mrts/haproxy/run.log |
| apache | no-crs | with-mrts | FAIL | 516 | 407 | 109 | 0 | 0 | 383 | 1314 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/apache/run.log |
| nginx | no-crs | with-mrts | FAIL | 523 | 407 | 116 | 0 | 0 | 383 | 3358 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/nginx/run.log |
| haproxy | no-crs | with-mrts | FAIL | 516 | 407 | 109 | 0 | 0 | 383 | 1090 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/no-crs/with-mrts/haproxy/run.log |
| apache | with-crs | no-mrts | FAIL | 134 | 122 | 12 | 0 | 0 | 0 | 366 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/apache/run.log |
| nginx | with-crs | no-mrts | FAIL | 141 | 115 | 26 | 0 | 0 | 0 | 641 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/nginx/run.log |
| haproxy | with-crs | no-mrts | FAIL | 134 | 122 | 12 | 0 | 0 | 0 | 312 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/no-mrts/haproxy/run.log |
| apache | with-crs | with-mrts | FAIL | 517 | 406 | 111 | 0 | 0 | 383 | 1423 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/results/force-all/apache-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/apache/run.log |
| nginx | with-crs | with-mrts | FAIL | 524 | 406 | 118 | 0 | 0 | 383 | 3594 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log |
| haproxy | with-crs | with-mrts | FAIL | 517 | 406 | 111 | 0 | 0 | 383 | 1225 | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/results/haproxy-summary.json | /var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/haproxy/run.log |

## MRTS Upstream-Konfigurationstests
| Connector | Variant | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Pending |
|---|---|---:|---:|---:|---:|---:|---:|
| apache | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | no-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| apache | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| nginx | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |
| haproxy | with-crs/with-mrts | 383 | 383 | 0 | 0 | 0 | 383 |

## Leitplanken
- `feature-demo` ist in Berichten sichtbar, wird jedoch nicht zur Laufzeit ausgeführt, es sei denn, `MODSECURITY_MRTS_INCLUDE_FEATURE_DEMO=1` ist festgelegt.
- MRTS Golden-Ausgaben unter dem Submodul sind nur golden/reference/drift Eingaben und keine Laufzeit-Case-Roots.
- `no-mrts`-Varianten sollten keine MRTS-Laufzeitfälle haben.
- Laufzeit-PASS/FAIL/BLOCKED-Werte stammen aus der Connector-Summary-JSON, nicht aus Klassifizierungsüberlagerungen.

## MRTS Nachweis der nativen Infrastruktur
- Apache nativ: `reports/testing/generated/mrts-native/mrts-native-apache.generated.md`
- NGINX PR24 nativ: `reports/testing/generated/mrts-native/mrts-native-nginx.generated.md`
- Native Zusammenfassung: `reports/testing/generated/mrts-native/mrts-native-summary.generated.md`
- Kombinierter nativer Bericht: `reports/testing/generated/mrts-native/mrts-native-full.generated.md`

Diese nativen MRTS-Berichte sind vom Connector-Vollmatrixbeweis getrennt.

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | `bca8c97edc4f6d5bab304488e596af2a047b9f5f17994cf72ef64ae748430ff8` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/full-runtime-matrix-runs.jsonl` | present | input file available |
