# NGINX-Validierung

**Sprache:** [English](validation.md) | Deutsch

Status: evidenzbasiert

NGINX-Laufzeitansprüche erfordern einen konkreten Smoke- oder Matrix-Befehl und werden generiert
Beweise. Ein erfolgreicher Build allein ist kein Laufzeitdurchlauf.

## Befehle

```bash
git submodule update --init --recursive
make smoke-nginx
make generate-test-matrix
make check-test-matrix
FORCE_ALL_CASES=1 make runtime-matrix-all
```

## Historische Beweise

Bei diesen Schnappschüssen handelt es sich nicht um aktuelle kanonische Facettenbeweise der Phase 4.

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standardmäßiger NGINX-Smoke-Test (historisch) | 60 | 60 | 0 | 0 | 0 |
| NGINX Force-All (historisch) | 140 | 95 | 39 | 0 | 6 |

Ausführbare YAML-Fälle gehören dem Framework-Modul:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Die generierten Beweise werden aufgezeichnet in:

- `reports/testing/generated/nginx-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`
- `reports/testing/test-coverage-overview.md`

## Nicht beansprucht

- Ohne eine passende Laufzeit wird kein umfassender NGINX-Regressionssuite-Durchlauf beansprucht
  Befehl und generiertes Ergebnis.
- Force-all-FAIL-Zeilen werden von der standardmäßigen Smoke-Zusammenfassung nicht ausgeblendet.
- Die vollständige RESPONSE_BODY-Unterstützung wird nicht gefördert.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Bei der Strict-Mode-Quellenverkabelung ist dies nicht der Fall
Beweise für einen echten Spätabbruch auf der Wirtsseite.

## Native P3/P4-Hostnachweise und HTTP/2-Anwendbarkeit

Verwenden Sie das NGINX-Ziel für den gesamten Lebenszyklus, um das echte dynamische Modul auszuüben
der deterministische Antwort-Header vorgelagert:

```bash
NO_CRS_RUN_ID=nginx-native-$(date -u +%Y%m%dT%H%M%SZ) make full-lifecycle-nginx
```

Die P3-Deny- und Redirect-Zeilen sind Fälle von Antwortheadern. Das native Harness
zeichnet sie auf, bevor Header festgeschrieben werden, zusammen mit separaten P4-Safes und
strenge Aufzeichnungen. Ein gültiger P4-Datensatzname
`integration_mode: native-nginx-http-module`; Es muss immer noch das tatsächliche angezeigt werden
Post-Commit-Aktion, anstatt eine Regelübereinstimmung als sichtbaren 403 zu behandeln.

Überprüfen Sie für jeden nativen Harnesskoffer `nginx-version.log` und
`nginx-http2-applicability.json` im Hostprotokollverzeichnis dieses Falles. Letzteres
ist `NOT_APPLICABLE`, wenn die echte `nginx -V`-Ausgabe fehlt
`--with-http_v2_module`. Wenn es vorhanden ist, bleibt der Status `NOT_EXECUTED`
bis ein expliziter Connector-eigener HTTP/2-Fall und ein passender HTTP/2-Listener vorhanden sind
sind vorhanden. Dadurch wird verhindert, dass ein Build-Flag als Transport hochgestuft wird
Laufzeitbeweise.

## Kanonische Phase-4-Validierung

Der begrenzte NGINX-Antworttextfilter ist quellendeklariert
`implemented_not_asserted` für seinen ausführbaren Antworttext und
Aspekte der Spätintervention. `phase4_pre_commit_deny` ist `not_implemented`: das
Der native Body-Filter-Pfad wird nach dem Response-Header-Pfad ausgeführt. Folgendes
Beweise sind erforderlich, bevor eine verbleibende individuelle Facette gefördert werden kann.

| Fall | Erforderliche Nachweise | Darf nicht aus | abgeleitet werden |
| --- | --- | --- |
| `phase4_rule_observed` | Echte NGINX-Phase-4-Regel `1100301` Beobachtung | ein sichtbarer 403 allein |
| `phase4_deny_before_commit` | Im aktuellen NGINX-Body-Filter-Timing-Modell nicht ausführbar | Karosseriefilterverkabelung oder ein sichtbares 403 |
| `phase4_deny_after_commit_log_only` | Angeforderter `deny`, aktueller `log_only`, unveränderter sichtbarer Status, Verspätungskennzeichen | eine Regel-ID oder ein erwarteter Status |
| `phase4_deny_after_commit_abort` | tatsächlicher `abort_connection`, beibehaltener bereits sichtbarer Status und `connection_aborted=true` | ein Nur-Protokoll-Eintrag oder eine generische Trennung |
| Status-/Aktionsmetadaten | ursprünglicher Hoststatus, angeforderter WAF-Status, sichtbarer Status, angeforderte und tatsächliche Aktionen | ein überladenes Statusfeld |

Ein nicht ausgeführter aktueller Fall bleibt bestehen `NOT_EXECUTED`; es wird nie in a umgewandelt
403 `PASS`.  Ereignisse und Berichte enthalten nur Antwortmetadaten, niemals einen Text
Nutzlast.
