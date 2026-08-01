# FND-PARENT-0071 — Apache-Smoke-Runtime lässt ein von ServerRoot aufgelöstes MIME-Artefakt aus

## Identität

- Kategorie: runtime_defect
- Repository / Ownership: parent / parent
- Priorität / Schweregrad / Konfidenz: P1 / not_applicable / validated
- Status / Machbarkeit: fixed / feasible_now
- Release-Blocker / Candidate-Integration-Blocker / Sicherheitsrelevanz: true / false / true
- Scope: Resulting Parent-master 154ee724eba4653fa6378fc3c8729ae433e65697, tree-identical to final PR #183 head 4e4dfb36e1b05f7eda38450fd3710e3a04905118

## Zusammenfassung

**Aktuelle Resulting-Master-Disposition — 2026-07-29T11:27:25Z.** PR #183
mergte als Master `154ee724eba4653fa6378fc3c8729ae433e65697`; Tree
`c4d08e66d9b1929f4a56c81f3d5a021ea6ce4ef0` entspricht finalem Head
`4e4dfb36e1b05f7eda38450fd3710e3a04905118`, und alle 14 Master-SHA-Workflows
waren erfolgreich. Detached-Master-fokussierte Apache/MIME-Unit-Checks und
`make check-apache-common-adoption` bestanden. Diese Fakten ersetzen die
historische Kandidat-only-Formulierung unten, aber keinen frischen
Resulting-Master-Live-Start-/Readiness-/403-/`SIGUSR1`-Lauf; das Finding bleibt
`fixed`, nicht `verified` oder `closed`.

Der Apache-Smoke-Harness erzeugte nur `conf/mime.types`, obwohl die gerenderte
Konfiguration `ServerRoot` auf den erzeugten Runtime-Root setzt und das
verfügbare Apache-`mod_mime` sein Standard-`mime.types` bei
`$ServerRoot/mime.types` auflöst. Der Pre-Fix-Konfigurationsparse meldet
`Syntax OK`, aber der Apache-Prozess schlägt vor jedem Request mit `AH01597` für
die fehlende Root-Level-MIME-Datei fehl.

Eine mutierbare lokale Reparatur erzeugt das generierte MIME-Artefakt an beiden
Stellen. Zurückgehaltene Controls zeigen danach einen live HTTP/1.1
`phase2_args_block`-Deny mit 403 und einen `SIGUSR1`-Graceful-Restart mit
wiederhergestellter Readiness. Der Record ist **nur lokal fixed**: Er bleibt ein
P1-Apache-Smoke-/Runtime-Release-Blocker, bis ein unabhängiger committeter
PR-Exact-Head und eine Reproduktion auf dem resultierenden Master vorliegen. Er
ist weder verified noch closed.

## Evidence und Grenze

| Artefakt | SHA-256 oder Ergebnis | Evidence |
| --- | --- | --- |
| Pre-Fix-Configtest | bbafef10c22b9323fa5589564990f57fbf57f9a632381d5e765dc5a3b25b4a1b | `apache2 -t` meldet `Syntax OK`; Parsing beweist keine Prozess-Liveness. |
| Pre-Fix-Apache-Error-Log | 0c7791f4b9935d6eda358d1c47dfcee2cc0baf547331b776ea3ea6ae5ded6fff | `AH01597` nennt das fehlende `ServerRoot/mime.types` vor jedem Request. |
| Mutierbare Harness-Reparatur | 9046a8caff239fa0bfe430224eb2819e2f01fa1e49fb50a16c21bf37fee7ece2 | Definiert und schreibt `MIME_TYPES_ROOT_FILE` zusätzlich zur vorhandenen `conf/`-Datei. |
| Mutierbarer Static-Contract | 167413ac60fee5dd215d2c9524d0bded1d344ee1425bc3284193ede9502e8399 | Fokussierter Test muss auf einem committeten PR-Head erneut laufen. |
| Root- und `conf/`-MIME-Artefakte | fafe925e793113aff60a22955ace0e8ddc4c3b068117f71b97d1897a58983317 | Beide generierten Dateien existieren mit gleichem Inhalt. |
| Post-Fix-phase-2-Control | cbfb2a07f77347b3554933173065063b237eca437e11882fe45db407afc11f1c | Live Apache meldet expected/actual HTTP 403 und `status=pass`. |
| Post-Fix-Restart-Log | ac01ca9bf7ea2615e4c02842b1b1dfd06ef0404962957ca68737406673f6566d | Zeichnet `SIGUSR1 received` und Graceful-Restart auf. |

Der Git-HEAD des Task-Worktrees bleibt
`9f23ae2c5fe908cef38f203be03f93fda75a8dd7`; die Two-Location-Reparatur ist
ein uncommitteter Working-Tree-Delta. Die zurückgehaltenen Runtime-Artefakt-
Hashes sind schreibgeschützte Beobachtungen im registrierten Task-Root, kein
versiegeltes Exact-PR-Head-Evidence-Set.

## Grundursache und Remediation-Richtung

`run_apache_smoke.sh` befüllte nur die conf-relative MIME-Datei, während
`apache_smoke.conf` den erzeugten Runtime-Root zu `ServerRoot` macht. Die
Runtime-Standardauflösung benötigt die Root-Level-Datei, bevor Apache startet;
ein reiner Syntax-Konfigurationstest führt diese Open-Operation nicht aus.

Die nachgewiesene Dual-Location-Artefaktänderung und den fokussierten Static-
Contract in einen getrennten Parent-PR promoten. Auf seinem exakten Head beide
erzeugten Pfade, Konfigurationsparsing, live Apache-Readiness, den HTTP/1.1-
403-Control und Graceful-Restart-/Readiness beweisen. Danach den ursprünglichen
Startup-Zustand und die Controls auf dem resultierenden Master wiederholen,
bevor verified oder closed gesetzt wird.

## Akzeptanz und Abgrenzung

Akzeptanz verlangt beide generierten MIME-Orte in einer frischen Runtime,
echten Apache-Prozessstart/-Readiness, phase-2-HTTP/1.1-403, SIGUSR1-Graceful-
Restart-/Readiness und einen negativen Static-Contract für einen One-Location-
Harness. Die unabhängig committete Reparatur muss Exact-Head- und
resulting-master-Validierung bestehen.

Dieser Record ist von FND-PARENT-0070 getrennt: 0070 besitzt die APXS-DSO-
Source-Materialisierung in `connectors/apache/build/apxs-wrapper.in`; dieser
Record besitzt die Runtime-Konfigurationsartefakt-Platzierung in
`connectors/apache/harness/`. Er beweist nicht, dass das getrennte
FND-PARENT-0064-RulesSet-APR-Lifecycle-Problem repariert wurde.

## Historie

- 2026-07-29T11:27:25Z: Die oben genannten Resulting-Master-Delivery-Fakten
  wurden abgeglichen; frische Master-Live-Start-/Readiness-/403-/`SIGUSR1`-
  Validierung bleibt nötig.

- 2026-07-29T10:33:55Z: zurückgehaltene Pre-Fix-`AH01597`-Evidence und lokale
  Reparatur-Controls erzeugten den kanonischen Parent-Runtime-Defekt-Record.
  Die Reparatur ist nur lokal fixed, bis committed-Exact-Head- und
  resulting-master-Validierung vorliegt.
