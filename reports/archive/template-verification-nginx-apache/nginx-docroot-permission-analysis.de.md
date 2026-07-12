> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# NGINX Docroot-Berechtigungsanalyse

**Sprache:** [English](nginx-docroot-permission-analysis.md) | Deutsch

Status: übergeordnete Laufzeitumgebung repariert und überprüft

Date/time: 2026-05-30 15:49:59 UTC

## Umfang

Diese Analyse deckt den zuvor erstellten Laufzeitblocker NGINX ab
BLOCKED Zeilen, nachdem der NGINX Build erfolgreich war. Der Connector wird dadurch nicht verändert
Adaptercode, YAML Testfälle, Harness-Skripte oder die
`modules/ModSecurity-test-Framework` Submodul.

## Nachweise überprüft

- `Makefile`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `connectors/nginx/harness/nginx_smoke.conf`
- `modules/ModSecurity-test-Framework/ci/runtime/run-nginx-smoke.sh`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0/logs/`

## Docroot-Generierungspfad

1. `modules/ModSecurity-test-Framework/ci/runtime/run-nginx-smoke.sh` leitet sich ab
   `NGINX_HARNESS_WORK_ROOT` aus `NGINX_HARNESS_PARENT`, wenn nicht explizit
   Die Arbeitswurzel ist festgelegt.
2. `connectors/nginx/harness/run_nginx_smoke.sh` erhält diese Arbeitswurzel und
   setzt `RUNTIME_BASE` darunter.
3. Der Connector-Harness erstellt pro Fall Laufzeitverzeichnisse und -sätze
   `DOCROOT="$RUNTIME_ROOT/htdocs"`.
4. Der Harness ruft `case_cli.py materialize --docroot "$DOCROOT"` auf.
5. `runner_core.py` schreibt `index.html` und `__modsec_smoke_ready` in die
   bereitgestellte Docroot.
6. `connectors/nginx/harness/nginx_smoke.conf` verwendet `root "@@DOCROOT@@"` und
   `index index.html`.

## Berechtigungsgrund

Die Umgebung hat `/tmp` als:

```text
drwx------ root root /tmp
```

Sowohl der Submodul-Runner als auch der Connectorkabelbaum können auf `/tmp` zurückgreifen
für Root-eigene Ausführungen, wenn `NGINX_HARNESS_PARENT` nicht gesetzt ist. Der NGINX Worker-Benutzer
Hinweis im Connectorkabelbaum ist `nobody`. Eine Docroot unterhalb einer nicht durchquerbaren Datei
`/tmp` kann daher korrekt unterhalb des Arbeitsstamms erstellt und verwaltet werden
bleibt für den Worker immer noch unzugänglich, da das übergeordnete `/tmp`-Verzeichnis vorliegt
ist Modus `700`.

Der aktuelle erfolgreiche Lauf verwendet:

```text
NGINX_HARNESS_WORK_ROOT=/src/ModSecurity-conector-build/ModSecurity-conector-nginx-runtime-0
```

Der entsprechende Pfad ist befahrbar:

```text
drwxr-xr-x root   root    /
drwxr-xr-x root   root    src
drwxr-xr-x root   root    ModSecurity-conector-build
drwxr-xr-x nobody nogroup ModSecurity-conector-nginx-runtime-0
drwxr-xr-x nobody nogroup runtime
drwxr-xr-x nobody nogroup action_allow_phase1_pass
drwxr-xr-x nobody nogroup htdocs
-rw-r--r-- nobody nogroup index.html
```

## Übergeordneter Fix

Der übergeordnete `Makefile` enthält die sichere Standardeinstellung:

```make
NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)
export NGINX_HARNESS_PARENT
```

Dadurch bleibt der Submodulvertrag intakt, während NGINX Laufzeitarbeit erzwungen wird
das ausgewählte Build-Root anstelle des Prozessstandards `/tmp`.

Für diese Analyse wurde keine Submoduldatei geändert. Keine Connectorquelle, kein Harness
Skript, YAML Testfall oder lokaler Connector `tests` Verzeichnis wurde geändert oder
erstellt.

## Überprüfung

Ausgeführte Befehle:

```text
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Ergebnisse:

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | `nginx-summary.json`: 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | `connector-summary.json`: Apache 54 PASS, NGINX 54 PASS |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | `results/no-crs/nginx-summary.json`: 60 PASS, 0 FAIL, 0 BLOCKED |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | `results/with-crs/nginx-summary.json`: 61 PASS, 0 FAIL, 0 BLOCKED |

Aktuelle Zusammenfassungsdateien:

- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.json`

Aktuelle RC-Dateien:

- `/src/ModSecurity-conector-build/results/apache.rc`: `0`
- `/src/ModSecurity-conector-build/results/nginx.rc`: `0`

## Entscheidung

Die Zeilen 11 vor NGINX BLOCKED werden als environment/docroot klassifiziert.
Berechtigungsblocker. Die aktuellen `/src`-Läufe haben keine NGINX BLOCKED-Zeilen mehr.
Das aktuelle With-CRS-Ziel ist PASS für den ausgeführten `/src`-Bereich.

NGINX bleibt weiterhin `partial`, da die vollständige Laufzeitförderung das erfordert
Mindestmatrix und RESPONSE_BODY Sperrbeweis. `response_body_pass` ist
Nur Pass-Through-Nachweise und überprüft nicht die Blockierung des Antworttexts.
