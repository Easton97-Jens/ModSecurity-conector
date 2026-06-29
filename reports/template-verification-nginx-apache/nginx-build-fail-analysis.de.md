# NGINX Build-Fehleranalyse

**Sprache:** [English](nginx-build-fail-analysis.md) | Deutsch

Status: Build-Fix überprüft; Die aktuelle `/src` Laufzeit führt Smoke-Tests aus PASS für den ausgeführten Bereich

## Ursprünglicher Build-Fehler

Der frühere NGINX-Build ist während `nginx-make` fehlgeschlagen, da dies nicht der Fall war
gefunden:

```text
msconnector/rule_load_stats.h
```

Der Header ist im übergeordneten Repository vorhanden:

```text
common/include/msconnector/rule_load_stats.h
```

Der fehlerhafte Compilerpfad enthielt `common/include` nicht.

## Minimaler Bauvertrag

Akzeptierter aktueller Bauvertrag:

```text
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` unterstützt diese Variable. Die NGINX prepare/configure
Der Fluss übergibt es, sodass der generierte NGINX-Build enthalten kann
`common/include/msconnector/rule_load_stats.h`.

## Überprüfung

Postfix-build/runtime-Befehle:

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | NGINX built and ran; NGINX result was 61 PASS, 0 FAIL, 0 BLOCKED. |

Aktuelle Nachweisdateien:

- `/src/ModSecurity-conector-build/logs/nginx/nginx-make.log`
- `/src/ModSecurity-conector-build/nginx-build/nginx-src/objs/Makefile`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

Die frühere Nichtübereinstimmung der With-CRS-Laufzeiterwartungen wird durch eine bereichsbezogene Lösung behoben
With-CRS-Erwartung. Es handelte sich nicht um den früheren Fehler beim Erstellen des Include-Pfads.

## Beziehung zum Docroot-Blocker

Der Include-Pfad-Fehler und die späteren Laufzeitzeilen 11 BLOCKED waren getrennt
Probleme:

- Problem mit dem Einschlusspfad: NGINX Build konnte nicht gefunden werden
  `msconnector/rule_load_stats.h`.
- Laufzeit-Docroot-Problem: NGINX Worker konnte ein generiertes Docroot nicht durchlaufen
  übergeordnetes Element, als das Harness-Arbeitsstammverzeichnis in dieser Umgebung auf `/tmp` zurückfiel.

Der Docroot-Blocker ist dokumentiert in
`nginx-docroot-permission-analysis.md`.

## RESPONSE_BODY

RESPONSE_BODY Blockierung bleibt nicht verifiziert. `response_body_pass` ist
Nur Pass-Through-Nachweise.

## Entscheidung

Der NGINX Build-Fehler wurde für den dokumentierten `/src` Source-Build-Ablauf behoben.
NGINX No-CRS und With-CRS wurden im aktuellen Lauf bestanden. NGINX bleibt bestehen
`partial` weil vollständige Laufzeitmatrixbeweise und RESPONSE_BODY Blockierung vorliegen
nicht verifiziert.
