# HAProxy-Testrahmenvertrag

**Sprache:** [English](test-framework-contract.md) | Deutsch

Status: aktuelle Eigentumsgrenze

Ausführbare Fälle, Matrixgenerierung, Laufzeit-Snapshots und generierte Berichte
sind im Besitz des Frameworks. Der HAProxy-Connector besitzt Quelle, Beispiele und die
Laufzeitumgebung, die das Framework aufruft.

## Connector-Eigentum

- `connectors/haproxy/src/`
- `connectors/haproxy/Makefile`
- `connectors/haproxy/harness/run_haproxy_smoke.sh`
- `examples/haproxy/`
- Connector-Metadaten und Ursprungsdateien

## Framework-Eigentum

- YAML-Fälle unter `modules/ModSecurity-test-Framework/tests/cases/`
- Fallauswahl- und Normalisierungshelfer
- Laufzeitmatrix-Orchestrierung
- Generierung eines Laufzeitvalidierungs-Snapshots
- Generierte Berichtsdarstellung

## Meldevertrag

- Standard-HAProxy-Smoke meldet die unterstützte Nicht-Former-XFAIL-Teilmenge:
  `55/55 PASS`.
- Alle erzwungenen HAProxy-Beweise bleiben getrennt:
  `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED / 6 NOT_EXECUTABLE`.
- Root-Zusammenfassungen sind konnektorneutral.
- HAProxy-Details auf Zeilenebene bleiben erhalten
  `reports/testing/generated/haproxy-runtime-results.generated.md`.
- Es gibt keinen Schreiber für synthetische Matrizen.

Phase 4 / RESPONSE_BODY ist `not_implemented` im ausgewählten SPOE/SPOP-Pfad.
Das ehemalige `wait-for-body`-Strict-Abort-Beispiel ist deaktiviert, veraltet und
nichtkanonisch; Es handelt sich nicht um aktuelle Laufzeitbeweise.
