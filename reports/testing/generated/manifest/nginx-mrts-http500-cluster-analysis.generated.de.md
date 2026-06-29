> Generierte Datei – nicht manuell bearbeiten.
>
> Erstellt unter: `2026-06-19T16:58:04Z`
> Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
> Datenquellenrichtlinie: `verified-inputs-only`
> Generator: `ci/generate-nginx-mrts-http500-cluster-analysis.py`
> Ziel erstellen: `generate-nginx-mrts-http500-cluster-analysis`
> Besitzer: `manifest`
> Schweregrad: `critical`
> Connector SHA: `5c9a0ceb2fb04dbc31347f1adc762512ed7fbf9f`
> Framework-SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Eingabestatus: `complete`

# NGINX with-crs/with-mrts HTTP-500-Clusteranalyse

**Sprache:** [English](nginx-mrts-http500-cluster-analysis.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Tabellen, IDs, Pfade und Metriken bleiben absichtlich unverändert. Bei einer Neuerzeugung der englischen Quelle muss diese Datei geprüft und aktualisiert werden.

## Zusammenfassung

- Verifizierte Lauf-ID: `2026-06-16T19-12-00Z-614c8049`
- Job: `nginx:with-crs:with-mrts`
- Primärblocker: `none`
- HTTP-500-Fehler: `0`
- Wahrscheinliche Ursache: Historische Nachweise: NGINX Worker konnte /root-eigene Laufzeiteltern nicht durchlaufen, auf die generierte Docroot war nicht zugegriffen und try_files /index.html wurde in einer Schleife in HTTP 500 ausgeführt. Neue Ausführungen sollten im Worker-Docroot-Preflight blockiert werden, bevor dies zu einem Nachweis für eine Laufzeitinkongruenz wird.
- Klassifizierung: `harness_environment_error`; sekundär `nginx_config_error`
- Vertrauen: `high`

## Cluster-Zählungen

| Group | Count | Classification | Representative Cases |
| --- | --- | --- | --- |
| Missing/Empty | - | - | - |

## Fehlermuster

| Error Pattern | Count | Example | Affected Cases |
| --- | --- | --- | --- |
| Missing/Empty | - | - | - |

## Repräsentative Fälle

| Case | Expected | Actual | Access | Error Pattern | Classification | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| Missing/Empty | - | - | - | - | - | - |

## Nachweis der Grundursache

- 0 HTTP-500-Zeilen verfügen über einen Umschreibe- oder internen Umleitungszyklus, während intern nach „/index.html“ umgeleitet wird.
- Für 0 HTTP-500-Zeilen wurde die htdocs/index.html-Berechtigung in den Fehlerprotokollen der letzten Ausführung verweigert.
- Historische Namensbeweise zeigen, dass /root 0700 ist, während NGINX Worker-Benutzer niemand ist; Die generierten Dateien darunter sind ansonsten lesbar.
- Im Final-Run-Cluster wurde kein segfault/core/module-load-Fehlermuster beobachtet.

## Minimale Reproduktion

- Minimaler Fall: `mrts_100000_mrts_002_args_a_get_100000_1`
- Bestehender Hersteller-Reproduzierer: `VERIFIED_RUN_FULL_MATRIX_JOB_TIMEOUT_SECONDS=3600 make verified-full-matrix-job CONNECTOR=nginx CRS=with-crs MRTS=with-mrts`
- Ziel zum Hinzufügen: `make verified-nginx-mrts-case CASE=mrts_100000_mrts_002_args_a_get_100000_1 CRS=with-crs MRTS=with-mrts`
- Hinweise: Der Connector-Harness unterstützt TEST_CASE intern, aber der verifizierte Vollmatrixpfad stellt noch kein Einzelfallziel mit CRS/MRTS-Setup und isolierten Job-Metadaten bereit.

## Fixplan

| Fix | File/Path | Risk | Expected Effect | Needs New Verified Run |
| --- | --- | --- | --- | --- |
| Keep verified NGINX Full-Matrix harness roots under VERIFIED_RUN_ROOT/NGINX_HARNESS_PARENT outside /root. | ci/run-full-matrix-parallel.sh / Makefile NGINX_HARNESS_PARENT | medium | Eliminates docroot Permission denied or reports it as a BLOCKED preflight before the 500 cluster can form. | True |
| Add a readiness/permission preflight that blocks NGINX jobs when worker user cannot traverse DOCROOT parents. | connectors/nginx/harness/run_nginx_smoke.sh | low | Classifies future inaccessible-docroot evidence as BLOCKED instead of runtime FAIL. | True |
| Add a verified single-case Full-Matrix target for NGINX with CRS/MRTS setup and job metadata. | Makefile / ci/run-full-matrix-job.py | low | Provides minimal repro without rerunning the 524-case NGINX job. | False |

## Datenquellen

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | `31606405e016d20afb67ce650aaf098b8194133d87869846344929e74c70b8f9` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | `d1425a9d5db6ec05270dd7292078437ab1ffd4981efdaadc8b1bf9da902e621f` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | `efc447466ad8121a9316477b087e74a7155148082320a9cd57805aa3327f675e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | `59dd481e19225c369952c566eca3981cb002c7050b699ee45be6dfdbef2d2603` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | `a54dc3f43ffc6d2eb4493ad56c58e6eff959cb2ce1380f5eb3d4b4e02003f5c2` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | `340546dbab42432eef255f99fda65c0d4301db589d6ac5c9f2a201a94326420e` | `2026-06-16T19-12-00Z-614c8049` | present |
| Declared input | `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | `dc995160b411295185768edbc7e7fa59e9ae41374fe3494b68341d0a4407e4c7` | `2026-06-16T19-12-00Z-614c8049` | present |

## Datenverfügbarkeit / fehlende Informationen

| Input | Status | Notes |
|---|---|---|
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/job.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/run.log` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-summary.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/full-matrix/with-crs/with-mrts/nginx/results/force-all/nginx-results.jsonl` | present | input file available |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.json` | present | input file available |
| `reports/testing/generated/manifest/verified-runtime-mismatch-analysis.generated.json` | present | input file available |
| `/var/tmp/ModSecurity-conector-verified/build/verified-runs/2026-06-16T19-12-00Z-614c8049/verified-commands.json` | present | input file available |
