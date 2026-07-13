# Apache-Planung

**Sprache:** [English](TODO.md) | Deutsch

Status: natives Apache-Modul; kanonisches Capability-Manifest vorhanden
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`

Der Framework-Katalog und die Integrationsanleitung befinden sich in
`modules/ModSecurity-test-Framework/docs/catalog-and-cases.md` und
`modules/ModSecurity-test-Framework/docs/connector-integration.md`.

- Lizenzanforderungen vor dem Importieren oder Anpassen von Code prüfen.
- Den PoC-Autotools-/APXS-Helper auf einem Host mit installierten Apache-
  Entwicklungstools validieren.
- Capability-Flags für Request-Body, Response-Body, Audit-Log, Reload und
  benutzerdefinierte Transaction-ID definieren.
- Nur bewiesene Apache-spezifische Tests nach
  `modules/ModSecurity-test-Framework/tests/upstream/connector-specific/apache/`
  portieren.
- Jedes wiederverwendete Konzept als `connector-specific` oder
  `engine-specific` dokumentieren.
- Das minimale Smoke-Harness erst nach einem echten HTTP-`403`-PASS in einen
  Connector-spezifischen Regressionstest überführen.

## Coverage-/Runtime-Entscheidungsmatrix

Das eingecheckte `capabilities.json` ist der Source-Contract für die neue
Baseline. Es erfasst die nativen Phase-1- bis Phase-4-Pfade als
`implemented_not_asserted`; kein Wert wird zu `verified` hochgestuft, bis ein
aktuelles kanonisches Ergebnis unter `$EVIDENCE_ROOT/apache/<run-id>/` vorliegt.

- [x] Coverage-Entscheidungsmatrix geprüft.
- [x] Kein lokaler Testordner.
- [x] Externe Framework-Testpfade referenziert.
- [x] Legacy-`phase1_header_block`-Runtime-Smoke-Evidence dokumentiert.
- [x] Legacy-Ergebnis von `/src` `make test-no-crs` dokumentiert; es ist nicht
      die durch diesen Branch eingeführte kanonische No-CRS-Baseline.
- [ ] Aktueller PASS von `/src` `make test-with-crs` dokumentiert; das aktuelle
      Ergebnis ist FAIL, weil `action_status_401_phase1_block` 401 erwartete und
      403 beobachtete.
- [x] Aktueller PASS von `/src` With-CRS `crs_sqli_anomaly_block` dokumentiert.
- [ ] Phase-1-Runtime-Evidence für mehr als den aktuellen Smoke-Case
      dokumentiert.
- [ ] Phase-2-Request-Body-Runtime-Evidence dokumentiert.
- [ ] Phase-3-Response-Header-Runtime-Evidence dokumentiert.
- [ ] Phase-4-Response-Body-Runtime-Evidence dokumentiert.
- [ ] RESPONSE_BODY-Blockierung verifiziert.
- [ ] Audit-/Log-Evidence dokumentiert.
- [ ] Negativer Pass-through-Case dokumentiert.
- [x] Connector-Status bleibt `partial`, bis die Matrix vollständig ist.
- [ ] `make no-crs-baseline-apache` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-apache` validiert Schema, Claims, Layout, Events und
      Capability-Konsistenz für denselben Run.

## Kanonische Phase-4-Evidence

Der Source-Contract deklariert die Response-Body- und Late-Intervention-
Facetten als `implemented_not_asserted`, nicht als `verified`. Ein historischer
Smoke nur mit Status oder eine Source-Inspektion kann sie nicht hochstufen.

- [ ] `phase4_rule_observed` mit Regel `1100301` über den echten Apache-
      Output-Filter-Pfad aufzeichnen; eine sichtbare 200 ist für diese
      Beobachtung gültig.
- [ ] `phase4_deny_before_commit` nur aufzeichnen, wenn Headers nicht committed
      waren und der Client den angeforderten Deny-Status erhält.
- [ ] Den sicheren späten Case nur mit angefordertem `deny`, tatsächlichem
      `log_only`, unverändertem sichtbaren Status und Late-Intervention-Metadata
      aufzeichnen.
- [ ] Den strikten späten Case nur mit tatsächlichem `abort_connection` und
      `connection_aborted=true` aufzeichnen.
- [ ] Separaten ursprünglichen Host-Status, angeforderten WAF-Status, sichtbaren
      Client-Status, angeforderte Aktion und tatsächliche Aktion in einem
      reinen Metadata-Event verifizieren.
- [ ] Einen nicht verfügbaren aktuellen Run als `NOT EXECUTED` beibehalten;
      niemals einen Regel-Match, ein Log-only-Ergebnis oder einen Abbruch in
      einen synthetischen 403-`PASS` umwandeln.
