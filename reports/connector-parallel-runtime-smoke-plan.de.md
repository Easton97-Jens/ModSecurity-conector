# Connector Parallel Runtime Smoke Plan

**Sprache:** [English](connector-parallel-runtime-smoke-plan.md) | Deutsch

Status: Parallelphase für Envoy, Traefik und lighttpd gestartet; lighttpd
Phase 1 wählt nun `sidecar_proxy` aus.

## Warum gängige msconnector-Verträge verwendet werden

`common/include/msconnector/` ist die konnektorneutrale Vertragsgrenze für alle
offene Connectors. Envoy, Traefik und lighttpd müssen ihre eigene Laufzeit übersetzen
Eingaben in diese gemeinsam genutzten Formen, anstatt connector-lokale Kopien davon zu erstellen
Anfrage, Antwort, Intervention, Status, Protokollierung, Fähigkeit, Herkunft,
Transaktions- oder Entscheidungsmodelle.

Die derzeit für die offenen Connectors verwendeten oder reservierten gemeinsamen Verträge sind:

| Area | Global component |
| --- | --- |
| Request mapping | `msconnector/request.h`, `msconnector/request.hpp` |
| Response mapping | `msconnector/response.h`, `msconnector/response.hpp` |
| Intervention/block decisions | `msconnector/intervention.h`, `msconnector/intervention.hpp` |
| Status values | `msconnector/status.h`, `msconnector/status.hpp` |
| Logging | `msconnector/logging.h`, `msconnector/logging.hpp` |
| Options/directives | `msconnector/options.h`, `msconnector/directives.h` |
| Capabilities | `msconnector/capabilities.h`, `msconnector/capabilities.hpp` |
| Origin/metadata | `msconnector/origin.h`, `msconnector/origin.hpp` |
| Transaction lifecycle and decision view | `msconnector/transaction.h`, `msconnector/transaction.hpp` |
| Rule-load stats | `msconnector/rule_load_stats.h` |

## Gemeinsame Logik

Die parallelen Runtime-Smoke-Einstiegspunkte teilen result/evidence beim Schreiben durch:

- `common/scripts/write_smoke_result.py`
- `common/scripts/run_blocked_runtime_smoke.sh`
- `common/scripts/run_local_runtime_smoke.py`
- `modules/ModSecurity-test-Framework/ci/common.sh`
- `modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh`

Diese Helfer zentralisieren:

- `result.json`, `summary.json`, `summary.txt` und `results.jsonl` Schreiben;
- die gemeinsamen `runtime_verified=false` / `production_ready=false` /
  `full_matrix_ready=false` / `crs_complete=false` Anspruchsvorgaben;
- `claims_not_allowed`;
- `missing_dependencies`;
- Exit-77 BLOCKED Ergebnissemantik, wenn lokale Abhängigkeiten fehlen;
- bedingte lokale Envoy/Traefik/lighttpd HTTP Smoke-Ausführung, wenn lokale Binärdateien vorhanden sind
  aus von common.sh verwalteten Pfaden aufgelöst;
- optionale gezielte Envoy/Traefik/lighttpd libmodsecurity-gestützte Smoke-Ausführung, wenn
  `DECISION_BACKEND=libmodsecurity` ist ausgewählt und lokale libmodsecurity
  headers/libraries werden aus von common.sh verwalteten Pfaden aufgelöst;
- optionale minimale und sekundäre CRS-Smoke-Ausführung für Envoy, Traefik und lighttpd wann
  `DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs` ist ausgewählt und
  lokale CRS plus lokale libmodsecurity werden aus von common.sh verwalteten Pfaden aufgelöst;
- die `msconnector_decision` status/intervention/reason Form, die von Open C verwendet wird
  Adapter;
- lokale Laufzeit-Binärsuche ohne globalen `PATH`-Fallback;
- Kompatibilitätszusammenfassungsdateien unter `$RESULTS_DIR`.

In den allgemeinen Hilfsprogrammen sind keine Connector-spezifischen Laufzeitbedingungen codiert. Jeder
Der Connector übergibt seinen eigenen Connector-Namen, den Integrationsmodus und den Grund für das Überspringen.
Fehlende Abhängigkeitsbeschreibung und Architekturentscheidungstext.

## Laufzeitabhängigkeitsrichtlinie

Laufzeitabhängigkeiten werden von Connector-Smokes niemals global installiert. Die
Smoke-Tests dürfen nicht laufen `apt install`, `apt-get install`, `yum install`,
`dnf install`, `apk add`, `brew install`, `go install` oder `npm install -g` und
Sie dürfen keine Laufzeitartefakte unter `/usr/local`, `/usr/bin` oder `/opt` schreiben.

`modules/ModSecurity-test-Framework/ci/common.sh` ist die Quelle der Wahrheit für
Laufzeit-, Build-, Protokoll-, Cache-, Quell- und Komponenten-Cache-Pfade. Das Offene
Connector-Smoke Wrappers Quelle `connector-smoke-common.sh`, welche Quellen
`common.sh` und stellt die konnektorneutralen Suchhilfen bereit.

`common.sh` definiert die lokalen Open-Connector-Laufzeitkomponenten:

- Envoy: `ENVOY_COMPONENT_ROOT`, `ENVOY_RUNTIME_ROOT`, `ENVOY_CONFIG_ROOT`,
  `ENVOY_LOG_ROOT`, `ENVOY_RESULT_ROOT`, `ENVOY_BIN`, `ENVOY_SMOKE_PORT`,
  `ENVOY_UPSTREAM_PORT`, `ENVOY_AUTHZ_PORT` und `ENVOY_INTEGRATION_MODE`.
- Traefik: `TRAEFIK_COMPONENT_ROOT`, `TRAEFIK_RUNTIME_ROOT`,
  `TRAEFIK_CONFIG_ROOT`, `TRAEFIK_LOG_ROOT`, `TRAEFIK_RESULT_ROOT`,
  `TRAEFIK_BIN`, `TRAEFIK_SMOKE_PORT`, `TRAEFIK_UPSTREAM_PORT`,
  `TRAEFIK_AUTHZ_PORT` und `TRAEFIK_INTEGRATION_MODE`.
- lighttpd: `LIGHTTPD_COMPONENT_ROOT`, `LIGHTTPD_RUNTIME_ROOT`,
  `LIGHTTPD_CONFIG_ROOT`, `LIGHTTPD_LOG_ROOT`, `LIGHTTPD_RESULT_ROOT`,
  `LIGHTTPD_BIN`, `LIGHTTPD_SMOKE_PORT`, `LIGHTTPD_UPSTREAM_PORT`,
  `LIGHTTPD_AUTHZ_PORT` und `LIGHTTPD_INTEGRATION_MODE`.

Das maschinenlesbare Quellverzeichnis für Envoy, Traefik und lighttpd ist
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
`common.sh` pinnt die aktuellen offiziellen Komponentenmetadaten:

- Envoy `1.38.2`, aus den offiziellen Envoy GitHub-Veröffentlichungen.
- Traefik `3.7.5`, aus den offiziellen Traefik GitHub-Veröffentlichungen.
- lighttpd `1.4.84`, aus dem offiziellen Lighttpd 1.4.x-Release-Index.

Das Manifest spiegelt die Version, die Quelle URL, den Download URL, SHA256 URL und wider
erwarteter `$CONNECTOR_COMPONENT_CACHE/.../bin/...` Pfad für jede Komponente.
Die Download-Ausführung bleibt standardmäßig deaktiviert und erfordert eine explizite Ausführung
`ALLOW_RUNTIME_DOWNLOADS=1` Bereiten Sie die Ausführung mit der SHA256-Verifizierung vor.

Die passive Bestandsausgabe ist verfügbar über:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Reihenfolge der Abhängigkeitssuche:

1. explizite binäre Umgebungsvariable, wie `ENVOY_BIN`, `TRAEFIK_BIN` oder
   `LIGHTTPD_BIN`;
2. Lokale, von common.sh verwaltete Caches und Laufzeitwurzeln:
   `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
   `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT` und
   `$SOURCE_ROOT`;
3. connector/project-defined lokale Abhängigkeitsverzeichnisse unter diesen Wurzeln;
4. Beenden Sie 77 mit BLOCKED-Nachweis, wenn keine lokale Binärdatei gefunden wird.

Für die offenen Connectors sind lokale Komponenten-Staging-Ziele verfügbar:

```sh
make prepare-envoy-runtime
make prepare-traefik-runtime
make prepare-lighttpd-runtime
make prepare-lighttpd-runtime-build
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
```

Ohne Opt-in melden sie eine bereits bereitgestellte lokale Binärdatei, sofern vorhanden und
Andernfalls beenden Sie 77, während Sie die Quelle drucken URL, korrigierte Version, URL herunterladen,
SHA256 Status und erwarteter Binärpfad. Mit Opt-in lädt Envoy herunter und
stellt die direkte Binärdatei bereit, Traefik lädt den Tarball herunter und stellt nur die bereit
`traefik` Binärdatei nach SHA256 Verifizierung und Lighttpd stellt die verifizierte Quelle bereit
unter `$CONNECTOR_COMPONENT_CACHE/lighttpd/src`. Mit explizit
`ALLOW_RUNTIME_BUILDS=1`, lighttpd konfiguriert, erstellt und installiert das angeheftete
Quelle unter `$CONNECTOR_COMPONENT_CACHE/lighttpd`, mit der erwarteten Binärdatei unter
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd`. Sie werden nicht global installiert
Pakete, schreiben Sie keine Systempfade und verwenden Sie kein globales PATH-Fallback.

Beispiele:

```sh
ENVOY_BIN=/lokaler/pfad/envoy make smoke-envoy
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```

Für Envoy, Traefik,
und lighttpd. Sie verwenden die gleiche aufgelöste Proxy-Laufzeitbinärdatei, wechseln jedoch die
auth/sidecar Entscheidungs-Backend vom einfachen lokalen Entscheidungsdienst zu einem lokalen
libmodsecurity C-API-Evaluator, der geladen wird
`common/rules/modsecurity_targeted_smoke.conf`:

```sh
DECISION_BACKEND=libmodsecurity make smoke-envoy
DECISION_BACKEND=libmodsecurity make smoke-traefik
DECISION_BACKEND=libmodsecurity make smoke-lighttpd
make smoke-envoy-modsecurity
make smoke-traefik-modsecurity
make smoke-lighttpd-modsecurity
```

Das Zielergebnis fügt `decision_backend`, `modsecurity_backend_verified`,
`modsecurity_rule_file`, `modsecurity_rule_id`, `modsecurity_rule_loaded`,
`intervention_status` und `decision_log_path`. Es kann untergehen
`modsecurity_backend_verified=true` nur, wenn libmodsecurity die Regel lädt
`1000001` und gibt den 403-Eingriff für `X-Modsec-Smoke: block` zurück.
Fehlende lokale libmodsecurity-Abhängigkeiten beenden 77 mit
`decision_backend=libmodsecurity`, `modsecurity_backend_verified=false` und
`missing_dependencies=["libmodsecurity"]`.
Der gemeinsame Resolver lebt in
`modules/ModSecurity-test-Framework/ci/connector-smoke-common.sh` und Suchen
nur explizite lokale Überschreibungen plus common.sh-verwaltete Komponenten, Build, Run, TMP,
Protokoll und Quellwurzeln. Es kann lokal verifizierte Komponenten-Caches unter wiederverwenden
`/tmp/ModSecurity-conector-verified` oder `/var/tmp/ModSecurity-conector-verified`
ohne auf globale libmodsecurity oder globale `pkg-config` zurückzugreifen.

Für die gleichen drei offenen Connectors sind minimale CRS-Smokes verfügbar:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-envoy
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-lighttpd
make smoke-envoy-crs
make smoke-traefik-crs
make smoke-lighttpd-crs
make smoke-open-connectors-crs
```

Die CRS Quelle der Wahrheit bleibt in `common.sh`: `CRS_REPO_URL`, `CRS_GIT_REF`,
`CRS_SOURCE_DIR` und `CRS_RUNTIME_DIR`. Der Runner schafft nur
Connector-lokale Smoke-Konfiguration unter `$<CONNECTOR>_RESULT_ROOT/crs-smoke`.
Es verwendet die vorhandene minimale SQLi CRS-Nutzlast wieder
`/?id=1%20UNION%20SELECT%20password%20FROM%20users`; Die blockierte Anfrage muss
Rückgabe HTTP 403 von CRS Interventionsbeweis, nicht von der Zielregel
`1000001`. Erfolgreicher CRS-Smoke schreibt `crs-result.json` und
`crs-decision.log` und darf nur `crs_minimal_smoke_verified=true` setzen.
`crs_complete`, Produktionsbereitschaft, Vollmatrixbereitschaft und Antworttext
Verifizierung bleibt falsch.

Der sekundäre CRS-Smoke verwendet denselben lokalen CRS/libmodsecurity/runtime Pfad und
schaltet nur den Smoke-Fall CRS um:

```sh
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-envoy
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-traefik
MODSECURITY_RULESET=crs CRS_SMOKE_CASE=secondary make smoke-lighttpd
make smoke-envoy-crs-secondary
make smoke-traefik-crs-secondary
make smoke-lighttpd-crs-secondary
make smoke-open-connectors-crs-secondary
```

Die sekundäre Sonde ist
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`; Es darf die Zielregel nicht verwenden
`1000001` oder die minimale SQLi-Probe. Erfolgreicher Sekundärbeweis schreibt
`crs-secondary-result.json`, `crs-secondary-decision.log` und
`crs-secondary-audit.log`, extrahiert die eigentliche CRS-Regel ID/message aus der
Nachweis und darf nur `crs_secondary_smoke_verified=true` setzen. Wenn CRS,
libmodsecurity und die Laufzeit sind vorhanden, die sekundäre Sonde jedoch nicht
blockiert, das Ergebnis ist FAIL (`secondary_crs_probe_not_blocked` im Inventar),
nicht PASS und nicht GESPERRT. CRS, libmodsecurity oder Laufzeitabhängigkeiten fehlen
bleiben Exit 77/BLOCKED.

## Konnektorspezifische Logik

Envoy behält nur Envoy-spezifisches ext_authz-Design, Konfiguration und Smoke-Harness bei
Einstiegspunkt und Bridge-Starter-Code. Das Laufzeitziel der Phase 1 ist
`integration_mode=ext_authz`. Wenn eine lokale Envoy-Binärdatei aufgelöst wird, läuft ein Smoke-Test
Runner startet einen minimalen Upstream, einen minimalen ext_authz-Entscheidungsdienst und
Envoy mit generierter lokaler Konfiguration benötigt dann HTTP 200 für eine zulässige Anfrage
und HTTP 403 für eine blockierte Anfrage. `ext_proc` wird auf eine spätere Phase verschoben.
Mit `DECISION_BACKEND=libmodsecurity` verwendet derselbe ext_authz-Pfad die
gezielter libmodsecurity-Evaluator anstelle des einfachen Entscheidungs-Backends. Mit
`MODSECURITY_RULESET=crs`, es verwendet denselben ext_authz-Pfad für die minimale und
sekundäre CRS führt Smoke-Tests aus und dokumentiert CRS Nachweise separat.

Traefik behält nur Traefik-spezifisches ForwardAuth-Design, Konfiguration und Smoke-Test bei
Nutzen Sie den Einstiegspunkt und den Startcode für den lokalen Entscheidungsdienst. Die Laufzeit der Phase 1
Ziel ist `integration_mode=forwardAuth`. Wenn es sich um eine lokale Traefik-Binärdatei handelt
gelöst, startet der Smoke Runner einen minimalen Upstream, einen minimalen ForwardAuth
Entscheidungsdienst und Traefik mit generierter lokaler Konfiguration, erfordert dann HTTP
200 für eine erlaubte Anfrage und HTTP 403 für eine blockierte Anfrage. Ein Go-Plugin ist
außerhalb des Geltungsbereichs von Phase 1.
Mit `DECISION_BACKEND=libmodsecurity` verwendet derselbe ForwardAuth-Pfad die
gezielter libmodsecurity-Evaluator anstelle des einfachen Entscheidungs-Backends. Mit
`MODSECURITY_RULESET=crs`, es verwendet denselben ForwardAuth-Pfad für das Minimum
und sekundäre CRS führen Smoke-Tests aus und CRS Nachweise separat aufzeichnen.

lighttpd behält die lighttpd-spezifische sidecar/proxy-Dokumentation bei, die lokal generiert wird
Konfiguration, Smoke-Harness-Einstiegspunkt und Brückenstartercode. Die Phase 1
Modus ist `integration_mode=sidecar_proxy`. Natives Modul, FastCGI/SCGI, und
mod_magnet/Lua bleiben zurückgestellt. Wenn eine lokale Lighttpd-Binärdatei aufgelöst wird, wird die
Smoke Runner startet Lighttpd als lokalen Upstream und Sidecar-Entscheidungs-Proxy
als ausgewählte Entscheidungsgrenze, erfordert dann HTTP 200 für eine zulässige Anfrage
und HTTP 403 für `X-Modsec-Smoke: block`. Mit `DECISION_BACKEND=libmodsecurity`,
Derselbe Sidecar-Pfad verwendet den angestrebten libmodsecurity-Evaluator und kann festgelegt werden
`modsecurity_backend_verified=true` erst nachdem Regel `1000001` den 403 erzeugt
Intervention. Mit `MODSECURITY_RULESET=crs` läuft der gleiche sidecar_proxy-Pfad
Die minimalen und sekundären CRS führen Smoke-Tests aus und erfassen CRS Nachweise getrennt. Dies
bleibt ein Sidecar_proxy-Nachweis der Phase 1, keine Behauptung eines nativen Lighttpd-Moduls.

## Ansprüche weiterhin verboten

Starter/self-test-Nachweise und BLOCKED-Smoke-Nachweise dürfen Folgendes nicht beanspruchen:

- `runtime_verified=true`
- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `crs_minimal_smoke_verified=true` ohne CRS-gestützten 200/403-Nachweis
- `crs_secondary_smoke_verified=true` ohne sekundäre CRS-gestützte 200/403-Nachweise
- `response_body_verified=true`

Envoy, Traefik und lighttpd dürfen `runtime_verified=true` nur setzen, wenn die lokale
Runtime-Smoke beobachtet die tatsächlichen HTTP 200/403-Status über die aufgelösten lokalen
Laufzeit und ausgewählter Integrationsmodus. Sie dürfen weiterhin keinen Anspruch auf Produktion erheben
Bereitschaft, vollständige Matrixbereitschaft, CRS Vollständigkeit oder Antwortkörper
Überprüfung. Die offenen Konnektoren dürfen auch keine vollständigen Matrixberichte generieren.
Produktionsbereitschaftsberichte oder CRS-vollständige Ansprüche aus starter/self-test
Nachweise.

`modsecurity_backend_verified=true` ist verboten, es sei denn, das Ziel ist
libmodsecurity Smoke hat die Regel `1000001` geladen und die Blockierung erzeugt
Intervention durch libmodsecurity. Der einfache Entscheidungsdienst führt Smoke-Tests aus nie
beansprucht selbst ModSecurity-Kompatibilität.

`crs_minimal_smoke_verified=true` ist verboten, es sei denn, der CRS-Smoke-geladene CRS
von lokalen, von common.sh verwalteten Pfaden und beobachtete einen CRS-gestützten HTTP 403 mit a
CRS Regel ID/message. Auch dann bleibt `crs_complete=true` verboten.

`crs_secondary_smoke_verified=true` ist verboten, es sei denn, der sekundäre CRS führt Smoke-Tests aus
CRS aus lokalen, von common.sh verwalteten Pfaden geladen, die sekundäre XSS-Prüfung gesendet und
beobachtete eine CRS-gestützte HTTP 403 mit einer extrahierten CRS Regel ID/message. Even
dann bleibt `crs_complete=true` verboten.

## Parallele Laufzeit-Smoke-Artefakte

Jeder Connector schreibt Connector-spezifische Artefakte:

| Connector | Evidence root | Fallback |
| --- | --- | --- |
| Envoy | `$VERIFIED_RUN_ROOT/envoy-smoke/` | `$BUILD_ROOT/results/envoy-smoke/` |
| Traefik | `$VERIFIED_RUN_ROOT/traefik-smoke/` | `$BUILD_ROOT/results/traefik-smoke/` |
| lighttpd | `$VERIFIED_RUN_ROOT/lighttpd-smoke/` | `$BUILD_ROOT/results/lighttpd-smoke/` |

Jeder `result.json` enthält mindestens:

- `connector`
- `integration_mode`
- `runtime_verified`
- `full_matrix_ready`
- `production_ready`
- `crs_complete`
- `response_body_verified`
- `allowed_request_status`
- `blocked_request_status`
- `evidence_root`
- `timestamp`
- `skipped_reason`
- `missing_dependencies`
- `claims_not_allowed`
- `crs_secondary_smoke_verified`
- `crs_smoke_case`

Der manuelle Workflow `.github/workflows/open-connectors-smoke.yml` führt das Öffnen aus
Connector-Laufzeitpfad mit `TMPDIR=/tmp`, bereitet Envoy, Traefik und vor
Lighttpd-Laufzeitkomponenten, führt einfache, gezielte libmodsecurity aus, minimal
CRS- und sekundäre CRS-Smoke-Tests sowie Upload
`ci-artifacts/open-connectors/` als `open-connectors-smoke-evidence`. Die
Artefakt ist ein kopiertes Nachweisbündel aus `/tmp/ModSecurity-conector-verified/`
plus Laufzeitinventarausgabe; Es ist keine Produktion, Vollmatrix,
CRS-vollständiger oder Response-Body-Anspruch.

## Aktuelle erwartete Ergebnisse

`make smoke-envoy`, `make smoke-traefik` und `make smoke-lighttpd` werden als Ziel ausgewählt
Runtime-Smoke-Einstiegspunkte. In Umgebungen ohne die ausgewählte lokale Laufzeit
Binärdateien müssen sie 77 mit BLOCKED-Nachweisen beenden, anstatt einen Erfolg zu melden.
Bei lokalen Envoy- oder Traefik-Binärdateien ist der Erfolg erst nach einem echten Local zulässig
HTTP-Smoke erzeugt die erwarteten 200/403 Status.

Aktuelle Blocker:

- Envoy: BLOCKED, wenn die lokale `envoy`-Binärdatei nicht über `ENVOY_BIN` verfügbar ist
  oder von common.sh verwaltete lokale Pfade.
- Traefik: BLOCKED, wenn die lokale `traefik`-Binärdatei nicht über verfügbar ist
  `TRAEFIK_BIN` oder common.sh-verwaltete lokale Pfade.
- lighttpd: BLOCKED, wenn die lokale `lighttpd`-Binärdatei nicht verfügbar ist
  `LIGHTTPD_BIN` oder common.sh-verwaltete lokale Pfade oder wenn die angeheftete Quelle
  Build kann nicht lokal ausgeführt werden. Quelldownload und lokaler Build erfordern beides
  explizites Opt-in.

## Doppelte Vermeidung

Die vorherigen Connector-lokalen Inline-JSON-Writer im Envoy, Traefik und
Die Lighttpd-Harnesses wurden durch herkömmliche Helfer ersetzt. Die Connector-Harnesses
Geben Sie jetzt nur noch Adapterparameter an. Das kleine Connector-lokale Entscheidungsergebnis
Strukturen wurden auch durch Aliase für `msconnector_decision` ersetzt, so dass
nur Connector-spezifische Adapterfunktionsnamen. Anfrage, Antwort, Status,
Interventions-, Fähigkeits-, Ursprungs-, Protokollierungs-, Transaktions- und Entscheidungsverträge
bleiben in `common/include/msconnector/`.

Apache, HAProxy und Nginx werden durch diese parallele Phase nicht verändert.
