# Entscheidungsmatrix für die Apache-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: teilweise, evidenzbasiert

Generierte Abdeckungsberichte sind keine automatische Laufzeit-Hochstufung.
Apache bleibt teilweise; historische Force-All-Nachweise enthalten weiterhin
FAIL- und NOT_EXECUTABLE-Zeilen. Sie belegen keine kanonische
RESPONSE_BODY-Fähigkeit.

## Aktuelle Laufzeitzählungen

| Ziel | Ausgeführt | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Nachweis |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Standard-Smoke (historisch) | 54 | 54 | 0 | 0 | 0 | Schnappschuss der Laufzeitvalidierung |
| Force-All-Matrix (historisch) | 133 | 100 | 27 | 0 | 6 | erzeugter Apache-Detailbericht |

## Nachweisquellen

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/testing/test-coverage-overview.md`
- `reports/testing/generated/apache-runtime-results.generated.md`
- `/src/ModSecurity-conector-build/results/apache-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/apache-summary.json`

## Promotion-Regeln

- `PASS` bedeutet, dass die Live-Apache-Ausführung das erwartete Fallergebnis erbracht hat.
- `FAIL` bedeutet, dass die Live-Apache-Ausführung zu einem anderen Ergebnis geführt hat.
- `NOT_EXECUTABLE` bedeutet außerhalb des aktuellen Laufzeitbereichs.
- Ehemalige XFAIL- und Force-All-Zeilen bleiben vom Standard-Smoke-Status getrennt.
- Erstellte Berichte müssen über `make generate-test-matrix` aktualisiert werden.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; begrenzte Nachweise für einen
strikten Abbruch sind nur Laufzeitnachweise.

## Kanonische Entscheidung für Phase 4

Im kanonischen No-CRS-Modell ist der native Apache-Response-Pfad vorhanden,
aber durch keinen aktuellen Lauf über den echten Host belegt. Die folgenden
Quellzustände bleiben deshalb bewusst `implemented_not_asserted`.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered` und `phase4` | `implemented_not_asserted` | Die begrenzte Filterverdrahtung ist kein Laufzeitnachweis. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | Regel `1100301` beobachten; kein 403 verlangen. |
| `phase4_pre_commit_deny` | `implemented_not_asserted` | Nicht festgeschriebene Header und passenden sichtbaren Sperrstatus belegen. |
| `late_intervention` und `late_intervention_log_only` | `implemented_not_asserted` | Angefordertes `deny`, tatsächliches `log_only` und unveränderten sichtbaren Status belegen. |
| `late_intervention_abort` | `implemented_not_asserted` | Tatsächliches `abort_connection` und `connection_aborted=true` belegen. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | Ursprünglichen Host-, angeforderten WAF-, sichtbaren Client-Status sowie angeforderte und tatsächliche Aktion belegen. |

Fehlt ein aktueller passender Lauf, lautet das Fallergebnis `NOT_EXECUTED`; es
ist kein 403-`PASS`. Ereignisse und Berichte bleiben metadatenbasiert.
