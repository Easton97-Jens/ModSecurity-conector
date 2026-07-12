> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Überprüfung des Komponenten-Downloads

**Sprache:** [English](component-download-check.md) | Deutsch

Status: überprüft

## Umfang

In dieser Datei werden die Abhängigkeitsvorbereitung und die von verwendeten Nachweise für Laufzeitkomponenten aufgezeichnet
die Überprüfung des Apache- und NGINX-Connectors.

## Repository-lokale Connector-Quellen

- Von Laufzeitbuilds verwendete Apache-Connector-Quelle:
  `connectors/apache`
- NGINX Connector-Quelle, die von Laufzeit-Builds verwendet wird:
  `connectors/nginx`
- Externe Apache/NGINX-Connector-Repositorys waren für den nicht erforderlich
  dokumentierte `/src` Smoke-Lauf.

## Nachweise zur Quellenvorbereitung

- `make fetch-deps` mit `SOURCE_ROOT=/src` vorbereitet
  `/src/ModSecurity_V3`.
- NGINX Quell-Build heruntergeladen NGINX Release `release-1.31.1` in die
  buildroot während des dokumentierten `/src`-Laufs.
- Apache-Quell-Build vorbereitet PCRE2, httpd, APR, APR-util, libmodsecurity,
  und `mod_security3.so` im Buildroot während des dokumentierten `/src`-Laufs.

## Aktuelle Laufzeitbefehle

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS, NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs` | PASS | Apache 54 PASS, NGINX 60 PASS; both 0 FAIL and 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs` | PASS | Apache 55 PASS, 0 FAIL, 0 BLOCKED; NGINX 61 PASS, 0 FAIL, 0 BLOCKED. |

Nachweisdateien:

- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/connector-summary.json`
- `/src/ModSecurity-conector-build/results/no-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/with-crs/connector-summary.json`
- `/src/ModSecurity-conector-build/results/apache.rc`
- `/src/ModSecurity-conector-build/results/nginx.rc`

## CRS Vorbereitungsnachweis

Das aktuelle With-CRS-Ziel verwendete den Repository-gestützten Framework CRS-Flow:

- `modules/ModSecurity-test-Framework/ci/provisioning/fetch-crs.sh`
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-crs.sh`
- CRS Pin in `modules/ModSecurity-test-Framework/ci/lib/common.sh`:
  `CRS_GIT_REF=v4.26.0`
- Beobachteter CRS Quellpfad: `/src/coreruleset`
- Beobachtete CRS Laufzeitpräambel:
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`

CRS Fallbeweise:

- Apache `crs_sqli_anomaly_block`: PASS, erwartet 403, tatsächlich 403.
- NGINX `crs_sqli_anomaly_block`: PASS, erwartet 403, tatsächlich 403.

Das allgemeine With-CRS-Ziel ist jetzt PASS für den aktuell ausgeführten `/src`-Bereich.
`action_status_401_phase1_block` wird erwartet 403 und tatsächlich 403 in With-CRS;
Die grundlegende No-CRS-Erwartung bleibt 401.

## NGINX Build-Include-Vertrag

Aktuell akzeptierter Vertrag:

```text
MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include
```

`connectors/nginx/config` kann diese Variable konsumieren. Die NGINX Build-Protokolle danach
Der Include-Fix zeigt `common/include` im generierten Kompilierungspfad.

## NGINX Docroot-Vertrag

Aktuell akzeptierter übergeordneter Laufzeitvertrag:

```make
NGINX_HARNESS_PARENT ?= $(BUILD_ROOT)
export NGINX_HARNESS_PARENT
```

Dadurch bleiben die generierten NGINX Laufzeit-Docroots unterhalb des ausgewählten Buildroots. In
Dieser Arbeitsbereich `/tmp` ist der Modus `700`, daher ist ein Fallback-Docroot unter `/tmp` nicht vorhanden
sicher für den NGINX Arbeiter.

## Standard-Buildroot

Die letzte dokumentierte einfache `make smoke-common` ohne `/src` Umgebung war
blockiert, weil der Standard-Buildroot fehlte:

```text
<local-state-root>/sources/ModSecurity_V3
```

Dieser Standard-Buildroot-Blocker ist kein Fehler des aktuellen `/src` Smoke
Nachweise.

## Entscheidung

Die Komponentenvorbereitung ist ausreichend für die dokumentierte `/src` No-CRS,
Mit CRS und gemeinsamen Smoke-Nachweisen. CRS fetch/prepare lief für With-CRS und
Der CRS SQLi-Fall wurde für beide Konnektoren übergeben. Vollständige Laufzeitüberprüfung und
RESPONSE_BODY Sperrung bleibt nicht verifiziert.
