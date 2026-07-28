# Change Record: Parent-Shell-Dispatch-Rule-Remediation für SonarQube Cloud S131 und S7679

**Sprache:** [English](CR-20260727-sonar-shell-dispatch-rules.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260727-sonar-shell-dispatch-rules |
| Datum (UTC) | 2026-07-27 |
| Basis-Revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Parent-SonarQube-Cloud-Shell-Code-Smells: 59 aktuelle OPEN-shelldre:S131-Keys und 27 aktuelle OPEN-shelldre:S7679-Keys, insgesamt 86 Receipt-Keys in 30 Parent-Shell-Skripten. |
| Grenze | Die unten gelisteten 30 Parent-Shell-Skripte, dieses englisch/deutsche Change-Record-Paar und seine Indizes. Makefiles, Workflows, generierte Reports, Framework, MRTS, Gitlinks, SonarQube-Cloud-Konfiguration, Quality Gates, Suppressions, externer Issue-Status, Push, Pull Request und Merge bleiben unverändert. |

## Motivation und Problemstellung

Die aktuelle Receipt-Inventur meldet fehlende explizite Dispatch-Defaults und
direkte Positionsparameter-Verwendungen in Parent-Shell-Skripten. Der Code
besitzt sicherheitsrelevante Runtime-, Pfad-, Prozess- und Evidence-Grenzen,
weshalb die Behebung gequotete Argumentbehandlung erhalten und unbekannte
Selektoren nicht in einen kompatiblen oder promoteten Fallback überführen darf.

## Akzeptanzkriterien

- Alle 86 Receipt-basierten shelldre:S131- und shelldre:S7679-Vorkommen
  bearbeiten.
- Normale No-op-Fälle, die bereits sicher waren, erhalten und unbekannte
  Connector-, Stage-, Protokoll-, Host-Action- und Runtime-Selektoren dort
  explizit fail-closed behandeln, wo eine Dispatch-Entscheidung erfolgt.
- Die skalare und gequotete Semantik jedes zu einem benannten Local
  umgeschriebenen Positionsparameters erhalten.
- POSIX-Shell-Syntaxchecks für alle 30 Skripte, fokussierte Parent-Verträge,
  negative Selektorkontrollen und Whitespace-Review bestehen.
- Ein gleichwertiges englisch/deutsches Change-Record-Paar pflegen und keinen
  SonarQube-Cloud-Issue vor einer neuen exakten Kandidaten-Head-Analyse als
  geschlossen behaupten.

## Implementierungsentscheidung und Begründung

Jeder vorhandene Validierungsfall behält seine Ablehnung und sein
Exit-Verhalten. Ein expliziter No-op-Default wurde nur ergänzt, wenn das
unpassende POSIX-case-Verhalten bereits ein sicherer erfolgreicher No-op war.
Mapping- oder Dispatch-Switches lehnen nun unbekannte Werte ab, bevor sie
einen Geschwister-Connector, eine Runtime-Komponente, ein Hostbinary oder
einen Evidence-Pfad wählen können. Jedes S7679-Vorkommen bindet den
Positionsparameter zuerst und verwendet ihn weiterhin mit den bestehenden
Quotes.

## Geänderte Dateien

- ci/checks/common/check-common-helpers.sh
- ci/checks/connectors/apache/check-apache-request-transaction-cleanup.sh
- ci/provisioning/cache/runtime-components-inventory.sh
- ci/runtime/lifecycle/consume-no-crs-selected-cases.sh
- ci/runtime/lifecycle/run-connector-stage.sh
- ci/runtime/lifecycle/run-full-lifecycle-all-connectors.sh
- ci/runtime/lifecycle/run-no-crs-baseline.sh
- ci/runtime/lifecycle/run-remaining-connector-target.sh
- common/scripts/run_blocked_runtime_smoke.sh
- connectors/envoy/build/build_connector.sh
- connectors/envoy/build/build_ext_proc.sh
- connectors/envoy/config/prepare_envoy_config.sh
- connectors/envoy/config/prepare_envoy_ext_proc_config.sh
- connectors/envoy/config/prepare_envoy_ext_proc_runtime_config.sh
- connectors/envoy/harness/run_envoy_connector_runtime.sh
- connectors/envoy/harness/run_envoy_ext_proc_runtime.sh
- connectors/envoy/harness/start_envoy_connector.sh
- connectors/haproxy/harness/run_haproxy_htx_runtime.sh
- connectors/haproxy/htx-overlay/build-overlay.sh
- connectors/lighttpd/build/apply_core_patch.sh
- connectors/lighttpd/build/build_patched_core.sh
- connectors/lighttpd/build/build_patched_host.sh
- connectors/lighttpd/harness/check_patched_lifecycle_host.sh
- connectors/lighttpd/harness/prepare_native_smoke.sh
- connectors/lighttpd/harness/run_patched_full_lifecycle.sh
- connectors/nginx/harness/run_nginx_smoke.sh
- connectors/traefik/build/build-connector.sh
- connectors/traefik/build/build-engine-service.sh
- connectors/traefik/build/build-native-middleware.sh
- connectors/traefik/scripts/start-smoke.sh
- reports/audits/change-records/CR-20260727-sonar-shell-dispatch-rules.md
- reports/audits/change-records/CR-20260727-sonar-shell-dispatch-rules.de.md
- reports/audits/change-records/README.md
- reports/audits/change-records/README.de.md

## Ausgeführte Befehle

- Receipt-Abgleich für alle 59 shelldre:S131- und 27 shelldre:S7679-Keys.
- rtk proxy sh -n für jedes der 30 geänderten Shell-Skripte.
- Fokussierte Parent-Unittest-Module für Selected-Runner-Wiring,
  Runtime-Snapshot-Integrität, NGINX-Protokoll-Harness,
  Envoy-Transport-Härtung, Traefik-Runtime-Root-Sicherheit und
  CI-Security-Workflows.
- HAProxy-HTX-Overlay-Statikvertrag sowie Remaining-Connector-Build- und
  Start-Wiring-Verträge.
- Negative Kommando-Kontrollen: ungültiger Connector und ungültige Stage in
  run-connector-stage sowie ungültiger Connector in run-no-crs-baseline.
- rtk proxy git diff --check.
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs.
- rtk proxy env PYTHONDONTWRITEBYTECODE=1 make check-doc-links.

Der isolierte Task-Worktree initialisiert den vom Parent festgeschriebenen
Framework-Gitlink ausschließlich für Test- und Dokumentationsabhängigkeiten.
Weder Framework-Quellen, Parent-Gitlink, Framework-Branch noch Framework-Pull-
Request ändern sich.

## Tests und tatsächliche Ergebnisse

| Kommando oder Check | Ergebnis |
| --- | --- |
| Receipt-Abgleich | bestanden: 59 von 59 S131-Fällen haben einen expliziten Default und 27 von 27 S7679-Vorkommen binden vor der Verwendung ein benanntes Positionsparameter-Local. |
| POSIX-Shell-Parsing | bestanden: sh -n endete mit 0 für alle 30 geänderten Skripte. |
| Fokussierte Parent-Verträge | bestanden: 50 Tests über Selected-Runner-Wiring, Runtime-Environment-Snapshot, NGINX-Protokoll, Envoy-Transport, Traefik-Runtime-Root-Sicherheit und CI-Security-Workflow-Module. |
| HAProxy-HTX-Vertrag | bestanden: der Overlay-Vertrag meldete jede erforderliche Lifecycle-, Event- und No-Buffer-Invariante als PASS. |
| Remaining-Connector-Build- und Start-Wiring | bestanden: beide Checks meldeten ok. |
| Negative Selektorkontrollen | bestanden: ungültiger Connector und ungültige Stage in run-connector-stage sowie ungültiger Connector in run-no-crs-baseline endeten jeweils mit 2, bevor ein Framework-/Runtime-Kommando oder Evidence-Write erreicht wurde. |
| git diff --check | bestanden: kein Whitespace-Fehler. |
| make check-bilingual-docs | bestanden: bilingual docs ok. |
| make check-doc-links | bestanden: repository path references: PASS und doc links ok. |

## Security-Auswirkung

Eine fokussierte Source-to-Sink-Sicherheitsreview fand keinen neuen Fail-open,
keine Command-Injection und keinen unsicheren Datei-Output-Pfad. Bestehende
unsichere Pfad-, Run-ID- und Port-Ablehnungen bleiben erhalten. Explizite
Mapping- und Dispatch-Defaults behandeln unbekannte Connector-, Stage-,
Protokoll-, Host-Action- und Komponenten-Selektoren nun fail-closed. Das eine
leere Ergebnis für ein unbekanntes Ruleset bleibt fail-closed, weil jeder
Consumer zuvor die Existenz der resultierenden JSON-Datei verlangt. Es wird
kein Security-Befund als behoben behauptet; dies sind
Maintainability-Signale mit erhaltenen und verstärkten sicherheitsrelevanten
Kontrollen.

## Dokumentationsstatus

Dieses englisch/deutsche Change-Record-Paar dokumentiert die Shell-only-
Remediation. Die abgeschlossenen Repository-Dokumentationschecks melden
bilingual docs ok, repository path references PASS und doc links ok. Keine
generierte Dokumentation oder Report wurde bearbeitet.

## Runtime-Evidence

Es wurde keine teure Connector-Matrix, kein Host-Build und kein
Report-produzierender Runtime-Lauf ausgeführt. Die fokussierten Verträge
belegen statische Dispatch-, Pfad- und Transportinvarianten; sie sind keine
Evidence eines vollständigen Connector-Lifecycle-Laufs.

## Bekannte Einschränkungen

SonarQube Cloud hat diesen Kandidaten-Head noch nicht analysiert. Die 86
aktuellen Befunde können erst nach einer frischen Analyse des exakten
ausgelieferten Commits verschwinden. Vollständige Host-/Lifecycle-Matrizen
bleiben bewusst lokal und wurden nicht für diesen Source-only-
Maintenance-Kandidaten verwendet.

## Verbleibende Risiken

Der Patch umfasst 30 Skripte, deshalb könnte ein fehlplatzierter Default einen
seltenen Selektor beeinflussen. Receipt-Abgleich, Syntaxchecks, fokussierte
Valid-Route-Tests, negative Selektorkontrollen und die unabhängige
Sicherheitsreview reduzieren dieses Risiko. Eine neue exakte gehostete Analyse
bleibt zum Nachweis des Scanner-Ergebnisses erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Connector-Build- oder Lifecycle-Matrix wurde nicht
  ausgeführt, weil sie große externe Runtime-Artefakte erzeugt und für die
  Validierung des expliziten Shell-Dispatch-/Source-Vertrags nicht erforderlich
  ist. Sie bleibt ein lokaler Validierungspfad, keine GitHub-Workflow-
  Anforderung.
- Gehostete SonarQube-Cloud-Analyse und GitHub-CI sind für diesen
  uncommitteten lokalen Kandidaten noch nicht verfügbar.
- Zum Zeitpunkt dieses Records wurden keine Framework-Test-Suite, kein
  MRTS-Test, keine Framework-Source-Modifikation, keine MRTS-Source-
  Modifikation, kein Commit, Push, Pull Request oder Master-Merge durchgeführt.

## Finaler Diff- und Review-Status

Der Task-Worktree-Kandidat enthält die 30 abgegrenzten Parent-Shell-Änderungen
und sein erforderliches bilinguales Traceability-Material. Der autoritative
Parent-Checkout, Framework-Quellen, MRTS-Quellen, Parent-Gitlink,
Scanner-Kontrollen und externe SonarQube-Cloud-Issue-Status bleiben unverändert.
