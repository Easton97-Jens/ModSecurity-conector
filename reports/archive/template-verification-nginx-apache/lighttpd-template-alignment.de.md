> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# lighttpd-Vorlagenausrichtung

**Sprache:** [English](lighttpd-template-alignment.md) | Deutsch

Status: Brückenstarter
Laufzeitstatus: nicht überprüft
Vorlagenausrichtung: Bridge-Starter, nicht laufzeitverifiziert

Der Lighttpd-Connector verfügt jetzt über eine Repository-eigene Entscheidungsservice-Brücke
Starter. Es kompiliert und testet den lokalen Sondenfluss selbst im Vergleich zum Connector-neutralen
`common/` Helfer, es handelt sich jedoch nicht um eine Laufzeitadapterimplementierung.

Es wird kein lokaler `connectors/lighttpd/tests`-Ordner verwendet. Es werden keine Laufzeitansprüche geltend gemacht.
Ausführbare Tests bleiben im Besitz des Frameworks
`modules/ModSecurity-test-Framework/tests/cases/` und verwenden Sie gemeinsam genutzte Runner wie
`modules/ModSecurity-test-Framework/tests/runners/case_cli.py` wenn ein echter
Lighttpd-Build und -Harness sind vorhanden.

## Starterumfang

| Item | Status |
| --- | --- |
| `ORIGIN.md` | present for repo-owned bridge starter; no upstream source imported |
| `SOURCE_MAP.json` | present for repo-owned bridge starter |
| `metadata.c` / `metadata.h` | present |
| `src/lighttpd_build_starter.c` | present; compile-time probe only |
| `src/lighttpd_bridge.*` | present; local decision-service bridge starter only |
| `build/build_starter.sh` | present; compiles the metadata/probe starter |
| `build/bridge_starter.sh` | present; compiles and self-tests the bridge starter |
| `Makefile` starter targets | present |
| lighttpd API usage | none |
| FastCGI/SCGI protocol implementation | none |
| ModSecurity API usage | none |
| runtime harness | blocked entrypoint only |

## Phasenmatrix

| Phase | lighttpd status | Notes |
| --- | --- | --- |
| Phase 0 Scaffold | OK | Scaffold files are present. |
| Phase 1 Origin/Metadata | bridge-starter documented | No upstream lighttpd source imported; metadata records bridge-starter status. |
| Phase 2 Build | bridge-starter | Compile/self-test checks exist for local starter source only. |
| Phase 3 Harness | blocked entrypoint only | Connector-side runtime-smoke script writes BLOCKED evidence only. |
| Phase 4 No-CRS | not-run | No lighttpd No-CRS runtime evidence. |
| Phase 5 With-CRS | not-run | No lighttpd With-CRS runtime evidence. |
| Phase 6 Coverage Matrix | bridge-starter documented | lighttpd matrix references the global matrix. |
| Phase 7 RESPONSE_BODY | not-verified | No lighttpd response-body blocking evidence. |
| Phase 8 Negative/pass-through | not-verified | No lighttpd negative/pass-through evidence. |
| Phase 9 Audit/log | not-verified | No lighttpd audit/log evidence. |
| Phase 10 Promotion | not allowed beyond bridge-starter/partial | Missing adapter and runtime evidence blocks promotion. |

## Letzte lokale Starterprüfungen

`connectors/lighttpd/build/build_starter.sh`,
`make -C connectors/lighttpd build-bridge-starter`, und
`make -C connectors/lighttpd self-test-bridge` für lokale compile/self-test übergeben
Schecks. Dies beweist nicht das Verhalten des Lighttpd-Adapters oder der Laufzeit; die Brücke
Probe selbst meldet die lokale Entscheidung als blocked/not-verified.

## Blockierte Abhängigkeiten

Ein echter build/runtime Pfad bleibt bis zu einer ausgewählten Produktion gesperrt
Der Integrationspfad verfügt über Repository-gestützte Abhängigkeiten: lighttpd headers/SDK/source
oder FastCGI/SCGI/bridge Implementierung, Build-Flags, ModSecurity-Integration
Code, ein echter Lighttpd-Laufzeit-Harness und Framework-eigene No-CRS/With-CRS
Nachweise.

## Entscheidung

lighttpd ist nur ein Brückenstarter. Es darf nicht als Adapterbesitz eingestuft werden,
runtime-smoke-verifiziert, crs-verifiziert oder mehr als teilweise bis pro Connector
origin/metadata, echter Adapteraufbau, Harness, No-CRS, With-CRS, Abdeckung,
RESPONSE_BODY, negative/pass-through und audit/log Nachweise sind dokumentiert.

## Framework-Starter-Nachweis

`make connector-starter-checks` zeichnet die Ergebnisse des Lighttpd-Starters auf
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` und
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Diese Aufzeichnungen dienen ausschließlich der Nachweissicherung und werden aufbewahrt
`runtime_verified: false`, `runtime_status: not-verified` und
`response_body_verified: false`.

## Runtime-Smoke-Eintrittspunkt

`make smoke-lighttpd` ruft jetzt den Framework-eigenen Lighttpd-Runtime-Smoke auf
Runner, der versendet
`connectors/lighttpd/harness/run_lighttpd_smoke.sh`. Aktueller Status ist BLOCKED
weil dieser connector-seitige Einstiegspunkt nur Diagnosebeweise schreibt und nein
Es existiert ein echter Lighttpd-server/config/runtime-Harness. Die Laufzeit bleibt nicht überprüft
und RESPONSE_BODY bleibt nicht verifiziert.
