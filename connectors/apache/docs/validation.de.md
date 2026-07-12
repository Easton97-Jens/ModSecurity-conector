# Apache-Validierung

**Sprache:** [English](validation.md) | Deutsch

Status: evidenzbasiert

Apache-Laufzeitansprüche erfordern einen konkreten Smoke- oder Matrix-Befehl und werden generiert
Beweise. Ein erfolgreicher Build allein ist kein Laufzeitdurchlauf.

## Befehle

```bash
git submodule update --init --recursive
make smoke-apache
make generate-test-matrix
make check-test-matrix
FORCE_ALL_CASES=1 make runtime-matrix-all
```

## Historische Beweise

Bei diesen Schnappschüssen handelt es sich nicht um aktuelle kanonische Facettenbeweise der Phase 4.

| Beweissatz | Versucht | PASS | FEHLER | GESPERRT | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Standard-Apache-Smoke-Test (historisch) | 54 | 54 | 0 | 0 | 0 |
| Apache Force-All (historisch) | 133 | 100 | 27 | 0 | 6 |

Ausführbare YAML-Fälle gehören dem Framework-Modul:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Die generierten Beweise werden aufgezeichnet in:

- `reports/testing/generated/apache-runtime-results.generated.md`
- `reports/testing/runtime-validation-snapshot.json`
- `reports/testing/test-coverage-overview.md`

## Nicht beansprucht

- Ohne eine passende Laufzeit wird kein umfassender Apache-Regressionssuite-Pass beansprucht
  Befehl und generiertes Ergebnis.
- Force-all-FAIL-Zeilen werden von der standardmäßigen Smoke-Zusammenfassung nicht ausgeblendet.
- Die vollständige RESPONSE_BODY-Unterstützung wird nicht gefördert.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft. Bei der Strict-Mode-Quellenverkabelung ist dies nicht der Fall
Beweise für einen echten Spätabbruch auf der Wirtsseite.

## Nativer P3- und separater P4-Hostnachweis

Verwenden Sie den nativen Hostpfad für den gesamten Lebenszyklus für Antwortheader und Antworttext
Beweise:

```bash
NO_CRS_RUN_ID=apache-native-$(date -u +%Y%m%dT%H%M%SZ) make full-lifecycle-apache
```

P3-Verweigerung und -Umleitung werden über den deterministischen Antwortheader ausgeführt
upstream, bevor Apache die Antwort festschreibt. Die sicheren und strengen P4-Fälle sind
Separate Real-Host-Fälle: Der Safe muss die sichtbare Antwort behalten und aufzeichnen
`log_only`, während strikt `connection_aborted` aufzeichnen muss. Ihre Veranstaltungsaufzeichnungen
Identifizieren Sie den ausgeführten Pfad mit `integration_mode: native-httpd-module`.

Überprüfen Sie die einzelnen Gehäuseteile `result.json`, `case-assert.log`, `error.log` und
Nur Metadaten `phase4.log` im generierten Host-Laufzeitverzeichnis. Ein Aufbau,
Quelleninspektion oder ein einzelner HTTP-Status sind kein Ersatz dafür
fallspezifische Ergebnisse.

## Kanonische Phase-4-Validierung

Die native Ausgabefilterimplementierung wird deklariert
`implemented_not_asserted` für jeden Response-Body und Late-Intervention
Facette.  Dieses Dokument spezifiziert daher Nachweisanforderungen, nicht a
aktueller PASS-Anspruch.

| Fall | Erforderliche Nachweise | Darf nicht aus | abgeleitet werden |
| --- | --- | --- |
| `phase4_rule_observed` | Echte Apache Phase-4-Regel `1100301` Beobachtung | ein sichtbarer 403 allein |
| `phase4_deny_before_commit` | Angeforderte Ablehnung, Header nicht festgeschrieben und übereinstimmender sichtbarer Clientstatus | ein Post-Commit-Match |
| `phase4_deny_after_commit_log_only` | Angeforderter `deny`, aktueller `log_only`, unveränderter sichtbarer Status, Verspätungskennzeichen | eine Regel-ID oder eine 403-Erwartung |
| `phase4_deny_after_commit_abort` | aktuell `abort_connection` und `connection_aborted=true` | ein allgemeiner Verbindungsfehler |
| Status-/Aktionsmetadaten | ursprünglicher Hoststatus, angeforderter WAF-Status, sichtbarer Status, angeforderte und tatsächliche Aktionen | ein einzelner `http_status`-Wert |

Wenn ein aktueller kanonischer Lauf diese Beobachtungen nicht liefern kann, ist er es
`NOT_EXECUTED`; Es wird kein Ergebnis aus der Quelleninspektion oder einer historischen Analyse gefördert
Matrix.  Ereignisse bleiben reine Metadaten und dürfen keine Antworttextdaten enthalten.
