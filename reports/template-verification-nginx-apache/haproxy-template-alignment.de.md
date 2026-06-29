# HAProxy-Vorlagenausrichtung

**Sprache:** [English](haproxy-template-alignment.md) | Deutsch

Status: spoa-agent-starter
Laufzeitstatus: runtime-smoke-verified für `haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`
Vorlagenausrichtung: Gerüstausgerichtet plus lokaler SPOA Agentenstarter

HAProxy ist nicht mehr nur ein Metadaten-Build-Starter. Es wurde jetzt repo-autorisiert
ORIGIN/SOURCE_MAP Metadaten, ein lokaler SPOA Agentenstarter zur Kompilierungszeit mit a
lokaler synthetischer Selbsttest zur Anforderungsentscheidung und zwei verifizierte Live-Runtime-Smoke-Tests
Fälle. Dies ist kein produktiver HAProxy-Adapter und ist nicht umfassender CRS,
RESPONSE_BODY oder Vollmatrix verifiziert.

Das Framework-eigene HAProxy-Matrixziel zeichnet jetzt eine Zeile pro vorhandener Zeile auf
Framework-YAML Fall. Das letzte kombinierte Artefakt versuchte 141 YAML-Zeilen und
aufgezeichnet 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE und 10 nur zugeordnet
Inventareinträge. PASS ist auf das Live-With-CRS beschränkt
`crs_sqli_anomaly_block` YAML Fall. Das No-CRS
`haproxy_phase1_header_block` Smoke-Test bleibt ein erhaltener diagnostischer Alias und ist es auch
nicht als Rahmen `phase1_header_block` YAML Zeile beansprucht.

## Ansprüche nicht geltend gemacht

- Es wird kein lokaler `connectors/haproxy/tests`-Ordner verwendet.
- Vom Starter wird kein HAProxy API verwendet.
- Es ist nur eine minimale diagnostische SPOP-Handshake-Teilmenge vorhanden.
- Es ist keine vollständige SPOE/SPOA-Protokollimplementierung vorhanden.
- Die HAProxy-Laufzeit PASS wird nur für `haproxy_phase1_header_block` und beansprucht
`haproxy_crs_sqli_anomaly_block`.
- Über die minimale Phase-1-Diagnose hinaus wird kein umfassenderes No-CRS YAML PASS beansprucht
  Header-Block-Smoke-Alias.
- Über `crs_sqli_anomaly_block` hinaus wird kein weitergehender With-CRS YAML PASS beansprucht.
- Es wird kein RESPONSE_BODY Sperrergebnis beansprucht.
- Es wird kein negative/pass-through-Ergebnis beansprucht.
- Es werden keine audit/log-Nachweise geltend gemacht.

## Gemeinsame Regeln und verwendeter Code

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`

## Starterbeweis

| Item | Status | Evidence |
| --- | --- | --- |
| Origin file | present | `connectors/haproxy/ORIGIN.md` |
| Source map | present | `connectors/haproxy/SOURCE_MAP.json` |
| Metadata source | present | `connectors/haproxy/metadata.c`, `connectors/haproxy/metadata.h` |
| Metadata build | PASS | `make -C connectors/haproxy build-metadata` |
| SPOA starter build | PASS | `make -C connectors/haproxy build-spoa-starter` |
| Local self-test | PASS | `make -C connectors/haproxy self-test-spoa` |
| Local HAProxy binary prepare | PASS | framework `ci/prepare-haproxy-runtime.sh` prepares HAProxy under `/src/ModSecurity-conector-build` |
| Diagnostic SPOP subset | PASS for diagnostic scope only | `make -C connectors/haproxy self-test-spoa-runtime` verifies a minimal diagnostic SPOP handshake subset |
| SPOE config syntax | syntax-valid | `make smoke-haproxy` generates config under `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` |
| Diagnostic HAProxy-to-agent runtime | diagnostic-enforcement-verified | fresh run-specific NOTIFY, arg extraction, ModSecurity 403, set-var ACK, block 403, and pass 200 evidence for No-CRS and With-CRS minimal scopes |
| ModSecurity binding | live-enforcement-verified | local libmodsecurity C API signatures verified; phase-1 header block and CRS SQLi anomaly decisions enforced by HAProxy over SPOA |
| Productive adapter build | BLOCKED for broader adapter ownership | Full SPOA implementation and live PASS/FAIL execution for currently BLOCKED framework rows are missing |
| Runtime smoke | PASS for two cases | `make smoke-haproxy` verifies `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block` |
| Combined matrix | partial | `make runtime-matrix-haproxy`; 141 YAML rows, 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |
| No-CRS split matrix | partial | `make test-haproxy-no-crs`; 141 YAML rows, 0 YAML PASS, 0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE, 10 MAPPED_ONLY; diagnostic alias preserved separately |
| With-CRS split matrix | partial | `make test-haproxy-with-crs`; 141 YAML rows, `crs_sqli_anomaly_block` PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |

## Phasenmatrix

| Phase | Area | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter plus ModSecurity binding self-test; productive build BLOCKED |
| Phase 3 | Harness | PASS for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`; broader harness incomplete |
| Phase 4 | No-CRS | partial; diagnostic alias PASS, YAML rows otherwise BLOCKED/NOT_EXECUTABLE |
| Phase 5 | With-CRS | partial; `crs_sqli_anomaly_block` YAML PASS, other rows BLOCKED/NOT_EXECUTABLE |
| Phase 6 | Coverage Matrix | HAProxy generated beside Apache/NGINX; mapped-only inventory separate |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | partial only |

## Framework-Starter-Nachweis

`make connector-starter-checks` zeichnet die Ergebnisse des HAProxy-Starters auf
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` und
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Diese Aufzeichnungen dienen ausschließlich der Nachweissicherung und werden aufbewahrt
`runtime_verified: false`, `runtime_status: not-verified` und
`response_body_verified: false`.

## Runtime-Smoke-Eintrittspunkt

`make smoke-haproxy` ruft jetzt den Framework-eigenen HAProxy runtime-smoke auf
Runner, der an `connectors/haproxy/harness/run_haproxy_smoke.sh` sendet.
Der aktuelle Status ist PASS für `haproxy_phase1_header_block` und
`haproxy_crs_sqli_anomaly_block`.
HAProxy `3.2.19` Quellenerfassung wird nur im Framework `common.sh` angeheftet;
die offizielle Prüfsummendatei und Quell-Makefile-Unterstützung für
`TARGET=linux-glibc` wurden überprüft, bevor die PIN hinzugefügt wurde. Der lokale HAProxy
Binärdateien können unter vorbereitet werden
`/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy`.
`make smoke-haproxy` überprüft auch eine minimale diagnostische SPOP Handshake-Teilmenge
und validiert die generierte SPOE-Konfigurationssyntax mit `haproxy -c`. Es startet live
HAProxy, der diagnostische SPOP-Agent und ein lokales Backend zeichnen dann auf
`spoe_config_status: syntax-valid`,
`spoe_runtime_status: diagnostic-enforcement-verified`,
`modsecurity_binding_status: live-enforcement-verified`,
`runtime_verified: true`, Block-Probe 403 und Pass-Probe 200. Das With-CRS
Unterbereichsdatensätze `crs_verified: true` nur für
`haproxy_crs_sqli_anomaly_block`; Die überprüften Fälle sind auf diesen beschränkt
`haproxy_phase1_header_block` und `haproxy_crs_sqli_anomaly_block`.
`make runtime-matrix-haproxy`, `make test-haproxy-no-crs` und
`make test-haproxy-with-crs` Schreiben Sie den Matrixbeweis unter
`/src/ModSecurity-conector-build/results/`, einschließlich geteilter `no-crs/` und
`with-crs/` Verzeichnisse. RESPONSE_BODY, weiter No-CRS/With-CRS live YAML
Ausführung, negative/pass-through, audit/log und vollständige Matrixbeweise bleiben bestehen
nicht verifiziert.
