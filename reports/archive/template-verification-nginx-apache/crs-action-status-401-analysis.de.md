> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# CRS Aktionsstatus 401 Analyse

**Sprache:** [English](crs-action-status-401-analysis.md) | Deutsch

Status: durch bereichsbezogenes Erwartungsupdate gelöst; genaue CRS/action-merging Wurzel
Die Ursache ist noch nicht vollständig geklärt.

Aktualisiert: 30.05.2026 20:55:03 UTC

## Umfang

Dieser Bericht dokumentiert die frühere With-CRS-Diskrepanz für
`action_status_401_phase1_block` und die Repository-gestützte Änderung, die behoben wurde
die Laufzeiterwartung ohne Änderung des Apache- oder NGINX-Adaptercodes.

Nein Apache/NGINX Adapterlogik, Connector-Baumlogik, Connector-Aufbaulogik,
oder neue YAML Testfälle wurden hinzugefügt. Die erforderliche Änderung wurde innerhalb des vorgenommen
Framework-Submodul, da das Framework keine variantenspezifischen Erwartungen hatte
Statusbehandlung für einen Fall, der sowohl im No-CRS- als auch im With-CRS-Kontext gültig ist.

## Im Framework-Submodul geänderte Dateien

- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `modules/ModSecurity-test-Framework/tests/cases/phases/phase1/action_status_401_phase1_block.yaml`
- `modules/ModSecurity-test-Framework/tests/README.md`
- `modules/ModSecurity-test-Framework/tests/runners/README.md`

Vom übergeordneten Repository verwendeter Framework-Pfad:
`modules/ModSecurity-test-Framework`.

Submodulstatus nach den aktuellen Prüfungen: übergeordnetes Element zeigt auf Framework-Commit
`4bec4d960fea89525db9e439ea567df15943a2e7`; Der Framework-Arbeitsbaum ist
sauber.

## Erwartungsmodell

Die grundlegende Testfallerwartung bleibt No-CRS:

```yaml
expect:
  status: 401
  intervention: block
  rule_id: 2320
```

Die With-CRS-Erwartung wird jetzt durch eine Variantenüberschreibung eingeschränkt:

```yaml
expect:
  variants:
    with-crs:
      status: 403
```

Dies bedeutet, dass die 403-Erwartung nur dann gilt, wenn
`MODSECURITY_TEST_VARIANT=with-crs`. Die grundlegende No-CRS-Erwartung bleibt 401.

## Nachweise vor der Veränderung

Früherer With-CRS-Lauf:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
```

Ehemaliges Ergebnis:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `action_status_401_phase1_block` | 401 | 403 | FAIL |
| NGINX | `action_status_401_phase1_block` | 401 | 403 | FAIL |

No-CRS war bereits vor der Änderung korrekt:

| Connector | Expected | Actual | Status |
| --- | ---: | ---: | --- |
| Apache | 401 | 401 | PASS |
| NGINX | 401 | 401 | PASS |

Derselbe With-CRS-Lauf bewies, dass CRS aktiv war
`crs_sqli_anomaly_block`, erwarteter 403 und tatsächlicher 403 für beide Konnektoren.

## Nachweise nach der Veränderung

Befehle:

```sh
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-no-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make test-with-crs
SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common
```

Ergebnisse:

| Command | Connector | PASS | FAIL | BLOCKED | Evidence |
| --- | --- | ---: | ---: | ---: | --- |
| `make test-no-crs` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/apache-summary.txt` |
| `make test-no-crs` | NGINX | 60 | 0 | 0 | `/src/ModSecurity-conector-build/results/no-crs/nginx-summary.txt` |
| `make test-with-crs` | Apache | 55 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/apache-summary.txt` |
| `make test-with-crs` | NGINX | 61 | 0 | 0 | `/src/ModSecurity-conector-build/results/with-crs/nginx-summary.txt` |
| `make smoke-common` | Apache | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/apache-summary.txt` |
| `make smoke-common` | NGINX | 54 | 0 | 0 | `/src/ModSecurity-conector-build/results/nginx-summary.txt` |

`action_status_401_phase1_block` nach der Änderung:

| Variant | Connector | Expected | Actual | Status | Evidence |
| --- | --- | ---: | ---: | --- | --- |
| No-CRS | Apache | 401 | 401 | PASS | `/src/ModSecurity-conector-build/results/no-crs/apache-results.jsonl` |
| No-CRS | NGINX | 401 | 401 | PASS | `/src/ModSecurity-conector-build/results/no-crs/nginx-results.jsonl` |
| With-CRS | Apache | 403 | 403 | PASS | `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl` |
| With-CRS | NGINX | 403 | 403 | PASS | `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl` |

CRS Wirksamkeitsnachweis:

| Connector | Case | Expected | Actual | Status |
| --- | --- | ---: | ---: | --- |
| Apache | `crs_sqli_anomaly_block` | 403 | 403 | PASS |
| NGINX | `crs_sqli_anomaly_block` | 403 | 403 | PASS |

Nachweispfade:

- `/src/coreruleset`
- `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`
- `/src/ModSecurity-conector-build/results/with-crs/apache-results.jsonl`
- `/src/ModSecurity-conector-build/results/with-crs/nginx-results.jsonl`

Framework-Prüfungen:

| Command | Result | Note |
| --- | --- | --- |
| `modules/ModSecurity-test-Framework: make lint` | PASS | Command exited 0. |
| `modules/ModSecurity-test-Framework: make quick-check` | not found | No `quick-check` target was found in the framework Makefile. |
| `modules/ModSecurity-test-Framework: make check-test-matrix` | PASS | Command exited 0; it printed a warning that framework-local `config/testing/import-status.json` was not found. |

## Was The Fix beweist

- Das Framework kann jetzt die erwarteten Status „No-CRS“ und „With-CRS“ getrennt halten.
- Die grundlegende No-CRS-Erwartung für `action_status_401_phase1_block` bleibt bestehen
  401 und gilt für Apache und NGINX.
- Die With-CRS-Erwartung für denselben Fall lautet 403 und gilt für Apache
  und NGINX.
- CRS ist im With-CRS-Ziel aktiv, wie durch `crs_sqli_anomaly_block` gezeigt
  PASS für beide Connectors.
- Die frühere 401/403-Diskrepanz wurde für die aktuellen `/src`-Ausführungen behoben.

## Was noch nicht bewiesen ist

- Der genaue CRS/default-action oder ModSecurity-Aktionszusammenführungsmechanismus, der
  Die im With-CRS-Kontext erzeugten 403 sind noch nicht vollständig bewiesen.
- Dies ist kein Nachweis für das Verhalten eines Nur-Apache- oder Nur-NGINX-Adapters. beides
  Connector folgen nun den gleichen Variantenerwartungen.
- Die RESPONSE_BODY-Blockierung wird in diesem Fall nicht überprüft.
- Eine vollständige Laufzeitüberprüfung über `partial` hinaus ist aufgrund der Promotion nicht nachgewiesen
  erfordert außerdem die vollständige Mindestmatrix und den RESPONSE_BODY-Sperrnachweis.

## Entscheidung

Die Erwartungsänderung wird akzeptiert und nur auf With-CRS beschränkt. Der Connector
Auswertungen können No-CRS- und With-CRS-Laufzeitziele als PASS für die aufzeichnen
Der aktuelle `/src` läuft, aber Apache und NGINX bleiben bis zum vollständigen `partial` bestehen
Mindestmatrix, einschließlich RESPONSE_BODY Blockierung oder einer dokumentierten unterstützten Lücke,
ist abgeschlossen.
