# HAProxy-Connector-TODO

**Sprache:** [English](TODO.md) | Deutsch

Status: HAProxy/SPOA/SPOP-Hostpfad (partial); kanonisches Capability-Manifest
vorhanden
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`

Kanonische Capability-Quelle: `connectors/haproxy/capabilities.json`.

Der Standard-Kompatibilitätspfad bleibt HAProxy/SPOA/SPOP. Das separate
Full-Lifecycle-Profil leitet `native-htx-filter` über
`full-lifecycle-haproxy-htx` an einen gepatchten HAProxy-3.2.21-HTX-Filter
weiter. Seine P1-/P3-Antworten, eine P2-Client-Antwort mit aufgezeichnetem
Versand an null oder ein Backend und der P4-Safe-`log_only`-Record sind bewusst
nicht hochgestuft und ändern weder die SPOP-Enforcement- noch die
Response-Body-Capability-Deklaration.

Frühere YAML-Matrix-Zählungen bleiben ausschließlich Legacy-Evidence. Sie
werden für diesen Branch nicht als kanonisches No-CRS-Ergebnis wiederverwendet,
und ohne einen neuen Run unter `$EVIDENCE_ROOT/haproxy/<run-id>/` wird keine
aktuelle PASS-Zählung behauptet.

Globale Gate-Definitionen sind in `docs/connectors/README.md` und
`docs/testing-and-evidence.md` zusammengefasst.

## Phase 0: Scaffold

- [x] Connector-Verzeichnis erstellt
- [x] README vorhanden
- [x] TODO vorhanden
- [x] Docs vorhanden
- [x] Harness-Contract dokumentiert
- [x] src-Platzhalter dokumentiert
- [x] kein lokaler Ordner `connectors/haproxy/tests`

## Phase 1: Origin / Metadata

- [x] `ORIGIN.md` für den aktuellen Repository-eigenen Starter hinzugefügt
- [x] `SOURCE_MAP.json` für den aktuellen Repository-eigenen Starter
      hinzugefügt
- [x] `metadata.c` und `metadata.h` hinzugefügt
- [x] lokaler SPOA-Agent-Starter-Quellcode dokumentiert
- [ ] Upstream-HAProxy-Quellcode ausgewählt und dokumentiert
- [ ] Upstream-HAProxy-Integrations-Headers/API dokumentiert
- [ ] Lizenz für produktiven Quellcode dokumentiert

## Phase 2: Build

- [x] Metadata-Build-Starter-Ansatz dokumentiert
- [x] Root-Compile-Guide in `docs/build/compilers/haproxy.md` dokumentiert
- [x] Metadata-Objekt-Build-Befehl dokumentiert
- [x] lokaler SPOA-Agent-Starter-Build dokumentiert
- [x] lokaler SPOA-Agent-Starter-Selbsttest dokumentiert
- [x] gemeinsame Include-/Source-Pfade dokumentiert
- [x] Starter-Artefaktpfad dokumentiert
- [ ] SPOP-Parser-/Library ausgewählt
- [ ] produktiver HAProxy-Adapter-Build-Ansatz dokumentiert
- [ ] produktive Include-Pfade dokumentiert
- [ ] produktive Library-Pfade dokumentiert
- [ ] produktiver Adapter-Artefaktpfad dokumentiert
- [ ] produktive Adapter-Build-Logs dokumentiert

## Phase 3: Harness

- [x] HAProxy-Runtime-Harness für Live-Framework-YAML-Request-seitige-Cases
      implementiert
- [x] Harness-Befehl dokumentiert
- [x] Harness-Evidence-Pfad dokumentiert
- [x] HAProxy-Binary-/Source-Build dokumentiert
- [x] HAProxy-Config dokumentiert
- [x] SPOE/SPOA-Config dokumentiert und für Live-Request-seitige-YAML-Runs
      verifiziert
- [x] diagnostischer Agent-Endpoint dokumentiert
- [x] ModSecurity-Integrationspunkt für materialisierte YAML-Rules dokumentiert
- [x] CRS-Integrationspunkt für den SQLi-Anomaly-Case dokumentiert
- [x] breiteres HAProxy-Runtime-Harness für gemeinsame ausführbare
      Request-seitige-YAML-Cases implementiert

## Phase 4: No-CRS Runtime

- [x] Phase-1-Header-Block-YAML-Smoke live durch HAProxy ausgeführt
- [x] `make test-haproxy-no-crs` für den HAProxy-Scope ausgeführt
- [x] PASS/FAIL/BLOCKED/NOT_EXECUTABLE-Zählungen für die No-CRS-Matrix
      dokumentiert
- [x] breitere No-CRS-Live-YAML-PASS/FAIL-Ausführung über gemeinsame
      Request-seitige-Cases

## Phase 5: With-CRS Runtime

- [x] CRS-SQLi-Anomaly-YAML-Smoke live durch HAProxy ausgeführt
- [x] `make test-haproxy-with-crs` für den HAProxy-Scope ausgeführt
- [x] CRS-Loaded-/Effective-Evidence für den Live-With-CRS-Run dokumentiert
- [x] PASS/BLOCKED/FAIL-Zählungen für den Live-With-CRS-Run dokumentiert
- [x] With-CRS-Matrix-PASS/FAIL/BLOCKED/NOT_EXECUTABLE-Zählungen dokumentiert
- [x] breitere With-CRS-Live-YAML-PASS/FAIL-Ausführung über gemeinsame
      Request-seitige-Cases

## Phase 6: Coverage Matrix

- [x] Phase-0/1/2-Starter-Status dokumentiert
- [x] HAProxy-Matrix-Target mit BLOCKED-/NOT_EXECUTABLE-Zeilen pro Case
      dokumentiert
- [x] getrennte No-CRS- und With-CRS-Ergebnisartefakte dokumentiert
- [x] produktiver Phase-2/3/4-Live-Status als partieller Request-seitiger
      Runtime-Pfad dokumentiert
- [x] Negativ-/Pass-through-Live-Evidence dokumentiert
- [ ] Audit-/Log-Live-Evidence dokumentiert
- [ ] RESPONSE_BODY-Blockierung bewertet

## Phase 7: Promotion

- [ ] berechtigt für `adapter-owned`
- [x] berechtigt für Live-Request-seitige-Runtime-Evidence bei gemeinsamen
      YAML-Cases
- [x] Ein begrenzter Legacy-`crs_sqli_anomaly_block`-Case wurde dokumentiert;
      dies ist kein breiter CRS-Claim und kein Teil der kanonischen
      No-CRS-Baseline.
- [ ] berechtigt für mehr als `partial`
- [ ] `make no-crs-baseline-haproxy` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-haproxy` validiert das zusammengeführte
      HAProxy-/Agent-Manifest, Schema, Claims, Layout, Event-Sicherheit und
      Capability-Konsistenz.

## Kanonische Phase-4-Evidence

Das frühere begrenzte SPOA/SPOP-Response-Body-Sample ist deaktiviert, weil es
`http-response wait-for-body` erforderte und kein Response-Stream mit geringer
Latenz ist. `response_body_buffered`, `phase4` und
`phase4_rule_evaluation` sind im ausgewählten SPOE/SPOP-Pfad daher
`not_implemented`, bis er einen nativen HTX-/Filter-Response-Chunk-Adapter
verdrahtet. Die eingecheckte HTX-Route besitzt isolierte Echt-Host-P1-bis-P4-
Transport-Evidence einschließlich kanonischer P1-/P3-Precommit-Replies und ist
über das separate Full-Lifecycle-Profil ausgewählt. Der Ein-Block-P2-Probe
liefert dem Client eine 403 und zeichnet null oder einen beobachteten
Upstream-Request auf, ohne dessen Reihenfolge zu beweisen; er belegt kein
inkrementelles Forwarding. P4 Safe zeichnet `log_only` auf; Strict bleibt
`NOT EXECUTED`. Keines dieser Ergebnisse stuft die SPOP-Capabilities hoch.
Die Pre-Commit-/Status-Felder des Agenten sind policy-abgeleitet und nicht vom
Host beobachtet, daher bleiben `phase4_pre_commit_deny` und
`late_intervention_status_metadata` `not_implemented`. Der aktuelle Pfad hat
auch keinen Post-Commit-Punkt, kein sicheres `log_only` und kein striktes
`abort_connection`; der HTX-Source-/Harness-`log_only`-Record ist kein vom
Client validiertes kanonisches Late-Action-Ergebnis, sodass alle Late-
Intervention-Facetten `not_implemented` bleiben.

- [ ] Einen nativen Response-Chunk-Adapter in den ausgewählten Pfad verdrahten
      und die vollständige Transaction korrelieren, bevor versucht wird,
      `phase4_rule_observed` für Regel `1100301` durch kanonische Evidence zu
      beweisen.
- [ ] Einen echten Hostpfad implementieren, der Client-sichtbaren
      Response-Status und Commit-Zeitpunkt beobachtet, bevor
      `phase4_pre_commit_deny` oder Status-Metadata deklariert wird.
- [ ] Einen echten Post-Commit-Hostpunkt implementieren, bevor sicheres
      `log_only` oder striktes `abort_connection` hinzugefügt wird; Timeout,
      Agent-Fehler und generischer Disconnect sind keine Late-Intervention-
      Evidence.
- [x] Diese semantischen Cases als `NOT EXECUTED` und nicht ausgewählt
      beibehalten, solange ihre Capabilities `not_implemented` sind; niemals
      einen 403-`PASS` aus einer Response-Body-Rule-ID oder policy-abgeleiteten
      Feldern folgern.
