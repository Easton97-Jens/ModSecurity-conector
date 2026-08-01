# FND-PARENT-0038 — Apache-Phase-4-Response-Bypass

## Klassifizierung

| Feld | Wert |
| --- | --- |
| Kategorie | security_validated |
| Repository / Ownership | Parent / parent |
| Priorität / Schwere | P0 / high |
| Konfidenz / Status | validated / fixed |
| Release-Blocker | ja |
| Security-relevant | ja |
| Feasibility | feasible_now |
| Aktueller lokaler Kandidat | `93c5f30c181710f5c2cecf207fb92aaecb215035` plus fokussierte ungepushte Parent-Remediation |

## Zusammenfassung, Auswirkung und Invariante

Vor der Remediation konnte Apache eine Response-Brigade downstream weitergeben,
bevor libModSecurity `RESPONSE_BODY` bei EOS verarbeitete. Ein disruptiver
Phase-4-Deny konnte folglich geschützten Bytes über die Response-Commit-Grenze
folgen. Normale interne Redirects konnten außerdem die ursprüngliche
Transaction beibehalten, während sie den Filter- und Handler-Pfad des
Target-Requests zurücksetzten.

Ein Remote-Requester, der einen Response-Body erzeugen kann, der eine
bereitgestellte Phase-4-Deny-Regel matcht, könnte Inhalt erhalten, den die
Policy unterdrücken soll. Kein Byte, das Phase 4 berücksichtigen kann, darf
downstream gelangen, bevor `msc_process_response_body` und seine Intervention
entschieden haben. Ein unsicherer Redirect darf außerdem weder geschützten
Inhalt freigeben noch einen Target-Quick-Handler oder normalen Target-Handler
aufrufen.

## Betroffener Scope, Preconditions und Reproduktion

- `connectors/apache/src/msc_filters.c` — Held-Response-Lifecycle- und
  Terminal-Filter-Helper.
- `connectors/apache/src/mod_security3.c` —
  `apache_phase4_redirect_is_terminal_error_emission`,
  `hook_phase4_redirect_quick_handler`, `hook_phase4_redirect_handler` und
  `apache_phase4_terminal_error_redirect_note`.
- Parent-Harness- und Regression-Scope:
  `connectors/apache/harness/{mod_phase4_terminal_rogue.c,run_apache_smoke.sh}`,
  `ci/runtime/lifecycle/run-apache-phase4-response-regression.sh` und
  `tests/test_apache_phase4_response_regression_wiring.py`.

Die Precondition ist eine native Apache/libModSecurity-Phase-4-Response-Body-
Regel und eine direkte oder interne-Redirect-Response-Route. Der Requester
benötigt keine lokale Berechtigung. Das historische URI-Target-Control zeichnete
eine Internal-Redirect-Response mit dem Deny-Marker auf; seine zentralen
Artefakte bleiben fehlend oder unversiegelt und werden nur in `finding.json`
aufbewahrt.

Frische Exact-Dependency-Tests führten zuerst
`redirect-target-handler-abort-h1` vor der fokussierten Reparatur aus. Der Lauf
endete mit `1` und loggte sowohl die Connector-Ablehnung als auch
`ModSecurity Phase4 redirect target handler executed`; damit ist belegt, dass
ein Abbruch im Insert-Filter-Pfad den Target-Handler nicht stoppte.

## Aktuelle aufbewahrte Evidence

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| Pre-Fix-Target-Handler-H1-Log | `ada09ca5545220b3c2e9afee4b54d069eae66257f2b615ba1678350f3dd7c040` | Exit `1`, Ablehnung und Marker vorhanden |
| Post-Fix-Target-Handler-H1-Log | `c02afef668fc16a98ed026d3b5e0587975ed4fedd7f29184e5059021afafe021` | Exit `0`, Ablehnung vorhanden und Marker fehlt |
| Post-Fix-Target-Handler-H2-Log | `264f67f18b99979f60b6a6ecec2c40d808937aca6c0e293aa8ce94f606c7de22` | Exit `0`, Ablehnung vorhanden und Marker fehlt |
| Exact-Native-Matrix-Report | `2218e7d5545f6b09dcb43d1b0779889fc778a16d3f3f65e2246598c3b54e4627` | serielle 30-Control-Matrix Exit `0` |
| Versiegeltes Native-Manifest | `1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548` | aktuelles Evidence-Inventar |

Alle aktuellen Artefakte liegen im aufbewahrten Task-Run
`20260719T162259Z-pr60-exact-head-revalidation-dfba422e`; vollständige Pfade,
Befehle, Working Directory, Zeitstempel und Retention-Status stehen im
kanonischen JSON-Record.

## Root Cause und Remediation

`hook_insert_filter` ist `void`; Versiegeln oder Abbrechen dort stoppt
`ap_run_handler` daher nicht. Apache führt bei einem normalen internen Redirect
einen Quick-Handler vor `ap_process_request_internal` und `ap_invoke_handler`
aus; der bisherige Guard konnte Target-Handler-Side-Effects folglich nicht
verhindern.

Die Reparatur ergänzt `APR_HOOK_REALLY_FIRST`-Quick-Handler- und normalen
Handler-Guards, die für einen unsicheren `r->prev`-Redirect `DONE`
zurückgeben. Sie behält die begrenzte core-geformte lokale `ErrorDocument`-
Ausnahme nur bei erfolgreichem Nachweis und speichert diese einmalige Erlaubnis
in der Notes-Tabelle des neuen Requests, sodass verschachtelte Redirects sie
nicht erben. Held-Response-, Terminal-Guard- und Single-Release-Verhalten
bleiben erhalten.

## Akzeptanz, Regression und legitime Controls

- Ein Marker-Deny gibt vor EOS keinen geschützten Marker frei.
- Allow-, log-only-, Empty-, Body-Limit-, ProcessPartial-, Client-Abort-,
  `ErrorDocument`-, Redirect-, H1/H2-, Late-Producer- und Multi-Brigade-
  Controls bewahren ihr dokumentiertes Verhalten.
- `redirect-target-handler-abort-h1` und
  `redirect-target-handler-abort-h2` bewahren die Ablehnung und führen keinen
  Target-Handler aus.
- Die fokussierte statische Suite
  `tests.test_apache_phase4_content_type_synchronized_upstream` zusammen mit
  `tests.test_apache_phase4_response_regression_wiring` bestand 16/16;
  Shell-Syntax, `git diff --check` und ein fokussierter Exact-Header-C17-
  Frontend-Check bestanden ebenfalls.
- Lokale ErrorDocument-Controls bleiben der legitime Control. CRS ist durch
  seinen Framework-Provenance-Guard blockiert, und MRTS besitzt kein aktuelles
  read-only Materialisierungsresultat; keiner wurde umgangen oder als bestanden
  behauptet.

## Abhängigkeiten, Blocker und Restrisiko

Die aktuelle Matrix verwendete eine task-eigene read-only Kopie der vom
Parent-Gitlink referenzierten Framework-Revision
`cdc91a398d6c156eaff927d742b23018a3817fb6` und ließ Framework, MRTS und beide
Gitlinks unverändert. Die relevante MRTS-Revision ist
`13aa91291adea12d5c607fdd165d010fcfb1da78`.

Dieses Finding ist **fixed**, nicht verified. Verbleibende Blocker sind ein
frischer lokaler Codex-Security-Diff-Scan, dann Exact-Pushed-Head-CI, CodeQL,
SonarCloud, Review-/Thread-Evidence, Protected Merge, Resulting-Master-
Validierung und ein Master-Rerun der Original-Reproduktion plus legitimer
Controls. Der lokale ErrorDocument-Nachweis beruht weiterhin auf Apache-Core
`no_local_copy`- und `REDIRECT_STATUS`-Korrelation statt auf einem nicht
fälschbaren Provenance-Primitiv; kein Risiko wird akzeptiert.

Verwandtes Finding: `FND-PARENT-0008` ist eine unabhängige Clang-Baseline-
Warnung und kein Duplikat.

## Historie

- `2026-07-18T14:57:02Z` — historische Native-Evidence zeichnete den Response-
  Bypass auf.
- `2026-07-19T16:50:12Z` — der kanonische Record wurde nach dem Audit der
  historischen Evidence als blockiert erstellt.
- `2026-07-19T18:20:42Z` — die exakte Native-Target-Handler-Reproduktion
  identifizierte den verbleibenden Handler-Side-Effect; fokussierte Parent-
  Remediation bestand H1/H2 und die versiegelte 30-Control-Matrix und setzte
  dieses Finding lokal auf `fixed`.
