# NGINX Deckungsentscheidungsmatrix

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: teilweise, evidenzbasiert

Generierte Abdeckungsberichte sind keine automatische Laufzeit-Hochstufung.
NGINX bleibt teilweise; historische Force-All-Nachweise enthalten weiterhin
FAIL- und NOT_EXECUTABLE-Zeilen. Sie belegen keine kanonische
RESPONSE_BODY-Fähigkeit.

## Aktuelle Laufzeitzählungen

| Ziel | Ausgeführt | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Nachweis |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Standard-Smoke (historisch) | 60 | 60 | 0 | 0 | 0 | Schnappschuss der Laufzeitvalidierung |
| Force-All-Matrix (historisch) | 140 | 95 | 39 | 0 | 6 | erzeugter NGINX-Detailbericht |

## Nachweisquellen

- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `reports/testing/test-coverage-overview.md`
- `reports/testing/generated/nginx-runtime-results.generated.md`
- `/src/ModSecurity-conector-build/results/nginx-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/nginx-summary.json`

## Promotion-Regeln

- `PASS` bedeutet, dass die Live-Ausführung NGINX das erwartete Fallergebnis erbracht hat.
- `FAIL` bedeutet, dass die Live-Ausführung NGINX zu einem anderen Ergebnis geführt hat.
- `NOT_EXECUTABLE` bedeutet außerhalb des aktuellen Laufzeitbereichs.
- Ehemalige XFAIL- und Force-All-Zeilen bleiben vom Standard-Smoke-Status getrennt.
- Erstellte Berichte müssen über `make generate-test-matrix` aktualisiert werden.

Phase 4 / RESPONSE_BODY bleibt nicht hochgestuft; begrenzte Nachweise für einen
strikten Abbruch sind nur Laufzeitnachweise.

## Kanonische Entscheidung für Phase 4

Der native begrenzte NGINX-Response-Body-Filter ist Quellnachweis, aber kein
aktueller kanonischer Verhaltensnachweis. Jede ausführbare Phase-4- und
Late-Intervention-Facette bleibt bewusst `implemented_not_asserted`; der
Pre-Commit-Pfad ist wegen des aktuellen Body-Filter-Zeitpunkts ausgeschlossen.

| Facette | Zustand im Manifest | Abdeckungsentscheidung |
| --- | --- | --- |
| `response_body_buffered` und `phase4` | `implemented_not_asserted` | Allein die Filterverdrahtung belegt keine Ausführung. |
| `phase4_rule_evaluation` | `implemented_not_asserted` | Regel `1100301` beobachten; sichtbares 403 ist unabhängig. |
| `phase4_pre_commit_deny` | `not_implemented` | Der native Phase-4-Body-Filter läuft nach dem Response-Header-Pfad; keinen sichtbaren Phase-4-Deny ableiten. |
| `late_intervention` und `late_intervention_log_only` | `implemented_not_asserted` | Angefordertes `deny`, tatsächliches `log_only`, Late-Flag und unveränderten sichtbaren Status belegen. |
| `late_intervention_abort` | `implemented_not_asserted` | Tatsächliches `abort_connection` und `connection_aborted=true` belegen. |
| `late_intervention_status_metadata` | `implemented_not_asserted` | Ursprünglichen Host-, angeforderten WAF-, sichtbaren Client-Status sowie angeforderte und tatsächliche Aktion belegen. |

Ohne einen aktuellen passenden Host-Lauf lautet das Ergebnis `NOT_EXECUTED`,
nicht 403-`PASS`; Ereignisse bleiben zwingend metadatenbasiert.
