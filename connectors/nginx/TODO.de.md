# NGINX-Planung

**Sprache:** [English](TODO.md) | Deutsch

Status: natives NGINX-Modul; kanonisches Capability-Manifest vorhanden
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`

Der Framework-Katalog und die Integrationsanleitung befinden sich in
`modules/ModSecurity-test-Framework/docs/catalog-and-cases.md` und
`modules/ModSecurity-test-Framework/docs/connector-integration.md`.

- Lizenzanforderungen vor dem Importieren oder Anpassen von Code prüfen.
- Strategie für dynamischen gegenüber statischem Modul-Build entscheiden.
- Capability-Flags für Request-Body, Response-Body, HTTP/2, Audit-Log, Reload
  und benutzerdefinierte Transaction-ID definieren.
- Von nginx-tests abgeleitete Cases in
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`
  behalten.
- Filter-Reihenfolge vor der Implementierung dokumentieren.

## Coverage-/Runtime-Entscheidungsmatrix

Das eingecheckte `capabilities.json` ist der Source-Contract für die neue
Baseline. Es erfasst die nativen Phase-1- bis Phase-4-Pfade als
`implemented_not_asserted`, außer `phase4_pre_commit_deny`, das
`not_implemented` ist, weil der Body-Filter nach dem Response-Header-Pfad
läuft. Kein Wert wird zu `verified` hochgestuft, bis ein aktuelles kanonisches
Ergebnis unter `$EVIDENCE_ROOT/nginx/<run-id>/` vorliegt.

- [x] Coverage-Entscheidungsmatrix geprüft.
- [x] Kein lokaler Testordner.
- [x] Externe Framework-Testpfade referenziert.
- [x] Build-Contract `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`
      dokumentiert.
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
- [x] Den aktuellen gepinnten Host auf einen anwendbaren HTTP/2-Pfad geprüft:
      Seine `nginx -V`-Konfiguration besitzt kein `--with-http_v2_module`,
      daher wird für diesen Host-Build kein HTTP/2-Lifecycle-Case ausgeführt
      oder beansprucht.
- [ ] RESPONSE_BODY-Blockierung verifiziert.
- [ ] Audit-/Log-Evidence dokumentiert.
- [ ] Negativer Pass-through-Case dokumentiert.
- [x] Connector-Status bleibt `partial`, bis die Matrix vollständig ist.
- [ ] `make no-crs-baseline-nginx` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-nginx` validiert Schema, Claims, Layout, Events und
      Capability-Konsistenz für denselben Run.

## Kanonische Phase-4-Evidence

Der Source-Contract belässt die ausführbaren Response-Body- und Late-
Intervention-Facetten bei `implemented_not_asserted`, bis ein aktueller
kanonischer NGINX-Host-Run jedes Verhalten getrennt beweist.
`phase4_pre_commit_deny` ist ausdrücklich `not_implemented`: Der native
Body-Filter besitzt keinen Response-Body-Decision-Point vor den Headers.

- [ ] `phase4_rule_observed` mit Regel `1100301` aufzeichnen; eine
      Rule-Observation darf nicht in eine sichtbare 403-Anforderung
      umgeschrieben werden.
- [x] `phase4_deny_before_commit` aus der NGINX-Runner-Auswahl heraushalten:
      Das Timing des Phase-4-Body-Filters kann keine uncommitted Response
      begründen.
- [ ] Sicheres Post-Commit-Verhalten als angefordertes `deny`, tatsächliches
      `log_only`, unveränderter sichtbarer Status und
      `late_intervention=true` verifizieren.
- [ ] Striktes Post-Commit-Verhalten als tatsächliches `abort_connection` mit
      `connection_aborted=true` verifizieren; ein vorheriger Client-Status kann
      sichtbar bleiben.
- [ ] Reine Metadata-Events mit ursprünglichem Host-Status, angefordertem
      WAF-Status, sichtbarem Client-Status, angeforderter Aktion und
      tatsächlicher Aktion verifizieren.
- [ ] `NOT EXECUTED` beibehalten, wenn ein aktueller kanonischer Run fehlt;
      niemals `PASS` aus Filter-Verdrahtung oder einer Phase-4-Rule-ID folgern.
