# Entscheidungsmatrix für die Apache-Abdeckung

**Sprache:** [English](coverage-decision-matrix.md) | Deutsch

Status: teilweise, evidenzbasiert

Bei der generierten Abdeckungsberichterstattung handelt es sich nicht um eine automatische Laufzeiterhöhung. Apache bleibt
teilweise, weil Force-All-Nachweise immer noch die Zeilen FAIL und NOT_EXECUTABLE haben
Die vollständige RESPONSE_BODY-Unterstützung wird nicht promoted.

## Aktuelle Laufzeitzählungen

| Target | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE | Evidence |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Default smoke | 54 | 54 | 0 | 0 | 0 | runtime validation snapshot |
| Force-all matrix | 133 | 100 | 27 | 0 | 6 | generated Apache detail report |

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
- Former-XFAIL- und Force-All-Zeilen bleiben vom standardmäßigen Smoke-Status getrennt.
- Erstellte Berichte müssen über `make generate-test-matrix` aktualisiert werden.

Phase 4 / RESPONSE_BODY bleibt nicht promoted; begrenzte strikte Abbruchbeweise sind
documented/reported nur als Laufzeitbeweis.
