# lighttpd-Connector-TODO

**Sprache:** [English](TODO.md) | Deutsch

Status: nativer `minimal_runtime_smoke` für Phase-1-Headers
Kanonischer No-CRS-Status: `supported_not_verified` / `NOT EXECUTED`
Metadata-Evidence-Zustände: `link_verified`, `minimal_runtime_smoke` und
`partial_runtime_path`.

Kanonische Capability-Quelle: `connectors/lighttpd/capabilities.json`.

Das Standard-Kompatibilitäts-Target bleibt das native Stock-Modul. Das
Full-Lifecycle-Profil leitet `patched-native` über
`full-lifecycle-lighttpd-patched`, das einen passenden lighttpd-1.4.84-Core
und ein Modul für einen isolierten Phase-1-Smoke bereitstellt. Seine
eingecheckte Runtime verwendet beide Body-Modi als `none`; daher kann sie weder
Body- noch Phase-4-Capabilities hochstufen, obwohl die gepatchte ABI jetzt
geliehene HTTP/1.1-Request-Ranges und Identity-Entity-Response-Ranges vor dem
Transfer-Framing bereitstellt.

## Abgeschlossen

- [x] Repository-eigener Origin und Source Map dokumentiert.
- [x] Bereitstellung von gepinntem lighttpd-1.4.84-Quellcode/Binary verfügbar.
- [x] Native Plugin-Initialisierung, Config-Registrierung, Defaults und Cleanup
      implementiert.
- [x] Request-Metadata und längenbegrenztes Header-Mapping implementiert.
- [x] Response-Metadata und längenbegrenztes Header-Mapping implementiert.
- [x] Common-Runtime, Rule-Loading, Transaction-ID, Decisions, Limits,
  Flow-Guard, DoS-Guard, Events und JSONL in Live-Host-Callbacks verdrahtet.
- [x] Phase-1-Deny auf `http_status_set_err()` abgebildet.
- [x] Transaction-Finish/Destroy und Mapper-Storage-Cleanup implementiert.
- [x] C17-PIC-Shared-Module-Build mit `-Wall -Wextra -Werror` implementiert.
- [x] Build und Bridge-Selbsttest getrennt.
- [x] Echter Modul-/Config-Load-Check implementiert.
- [x] Request-freier echter Process-Start-Smoke implementiert.
- [x] Separater echter Host-200/403-Runtime-Smoke implementiert.
- [x] Enger JSONL-Event-Metadata-Check implementiert.

## Vor breiteren Runtime-Claims erforderlich

- [x] Versionierter 1.4.84-Source-Patch definiert begrenzte geliehene HTTP/1.x-
      Request-Body-Capture und besitzt einen Compile-only-Check; keine
      Runtime-Capability wird hochgestuft.
- [x] Dediziertes Patched-Host-Target kopiert, patcht, konfiguriert, baut,
      installiert, staged und ABI-lädt einen passenden 1.4.84-Core plus Modul.
      Das Full-Lifecycle-Profil wählt seinen isolierten 200/403-Phase-1-
      Host-Smoke aus; er bleibt nicht hochgestuft und belegt weder Body- noch
      Phase-4-Evidence.
- [ ] Request-Body-Truncation-Metadata bewahren und testen.
- [ ] Ausgewählte Phase-2-Request-Body-Artefakte für den gepatchten Pfad
      ausführen und aufbewahren.
- [x] Versionierter 1.4.84-Source-Patch definiert einen begrenzten HTTP/1.1-
      Identity-Entity-Body-/EOS-Hook vor dem Transfer-Framing. Er liefert
      geliehene Ranges, monotone Offsets und genau ein EOS; Socket-Short-
      Write-/EAGAIN-Retries erfolgen später und können eine Range nicht erneut
      einspeisen.
- [ ] Echtes Response-Streaming mit Identity-Body-Daten ausführen; gzip/br
      bleiben `NOT EXECUTED`, bis Filter-Reihenfolge und Dekompressions-Scope
      belegt sind.
- [ ] Phase-4- und Late-Intervention-Verhalten testen.
- [ ] Den implementierten Response-Header-Hook mit einer echten Phase-3-Rule
      ausüben; bis dahin bleiben `response_headers` und `phase3`
      `implemented_not_asserted`, nicht verifiziert.
- [ ] Redirects, Drops, Connection-Aborts und andere als 403 Decisions
      verifizieren.
- [ ] Multi-Worker-, Concurrency-, Keep-Alive-, HTTP/2- und Abort-Path-Tests
      hinzufügen.
- [ ] Nativen No-CRS-Negativ-/Pass-through- und erweiterte Rule-Cases ausführen.
- [ ] Nativen CRS-Smoke nur mit expliziter lokaler CRS-Evidence hinzufügen.
- [ ] Long-running-, Memory-, Cleanup- und Fault-Injection-Evidence hinzufügen.
- [ ] Security-Review und Production-Hardening abschließen.
- [ ] Relevante vollständige Matrix ausführen.
- [ ] `make no-crs-baseline-lighttpd` erzeugt aktuelle kanonische Evidence.
- [ ] `make evidence-check-lighttpd` validiert Native-Module-Evidence und
      ersetzt niemals den Legacy-Bridge-/Sidecar-Selbsttest.

Bis diese Punkte belegt sind, Status bei `minimal_runtime_smoke` /
`partial_runtime_path` belassen und alle Claims zu Body, CRS, Security,
Production und vollständiger Matrix auf false halten.

## Kanonische Phase-4-Implementierungsgrenze

Das Stock-Modul besitzt keinen Response-Body-Hook. Das gepatchte 1.4.84-Modul
besitzt einen Identity-Entity-Body-Source-Pfad, aber kein kanonisches Streaming-
Host-Ergebnis. Die folgenden Facetten bleiben daher für das ausgewählte
Evidence-Profil `not_implemented`: `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort` und
`late_intervention_status_metadata`.

- [x] Einen begrenzten nativen Identity-Entity-Body-Hook mit explizitem EOS
      implementieren, bevor Phase-4-Cases zur Ausführung ausgewählt werden.
- [ ] Regel `1100301` getrennt vom sichtbaren Deny-Status beweisen.
- [ ] Pre-Commit-Deny, sicheres `log_only` und striktes
      `abort_connection` als getrennte Outcomes mit reiner
      Real-Client-Metadata-Evidence beweisen; Strict bleibt derzeit
      `NOT EXECUTED`.
- [ ] Ursprünglichen Host-Status, angeforderten WAF-Status, sichtbaren
      Client-Status, angeforderte Aktion, tatsächliche Aktion, Commit-Status
      und Connection-Abort-Status zum relevanten Event-Beweis hinzufügen.
- [x] Bis dahin Phase-4-Ergebnisse als `NOT EXECUTED` beibehalten (oder sie
      durch Capability-Auswahl auslassen), nicht als `UNSUPPORTED`; dies ist
      kein Claim, dass lighttpd niemals einen geeigneten Response-Body-Hook
      unterstützen kann.
