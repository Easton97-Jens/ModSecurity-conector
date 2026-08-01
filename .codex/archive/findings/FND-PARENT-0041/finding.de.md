# FND-PARENT-0041 — Apache-Phase-4-Harness übergab eine nicht unterstützte Synchronized-Upstream-Option

## Klassifizierung

| Feld | Wert |
| --- | --- |
| Kategorie | test_failure |
| Repository / Ownership | Parent / parent |
| Priorität / Schwere | P1 / not_applicable |
| Konfidenz / Status | validated / fixed |
| Release-Blocker | ja |
| Security-relevant | ja |
| Feasibility | feasible_now |

## Zusammenfassung und Auswirkung

Der Parent-#60-Harness übergab zuvor `--control-root` an den generischen
Framework-Helper `synchronized_upstream.py`. Die vom Parent-Gitlink referenzierte
Framework-Revision `cdc91a398d6c156eaff927d742b23018a3817fb6` implementiert
diese Option nicht. Der Upstream endete daher vor der Adressveröffentlichung,
und erforderliche synchronisierte Phase-4-Controls konnten nicht starten. Dies
ist ein Parent-Testvertragsfehler, keine Autorisierung für Framework-/MRTS-
Änderungen und kein Runtime-Gate-Bypass.

Es wurde kein Leck von Production-Bytes gezeigt, weil der Fehler im Test-
Upstream auftrat. Er verhinderte dennoch den aktuellen Native-Nachweis für das
P0-Response-Body-Enforcement-Finding `FND-PARENT-0038`.

## Beobachtetes Verhalten, Preconditions und Reproduktion

Mit der exakten read-only Framework-Revision und einem synchronisierten
Phase-4-Modus endete das initiale Deny-Control mit `77`; sein stderr zeichnete
ein unbekanntes Argument `--control-root` auf. Der Parent-Harness sendet diese
Option nun nur an den expliziten Parent-eigenen Custom-MIME-Helper, der sie
unterstützt. Der generische gepinnte Framework-Helper erhält nur seine
unterstützten Ready-, Paused-, Release- und Server-Evidence-Dateiargumente.

Der alte Fehler lässt sich durch das initiale exakte Deny-Control mit der
unkonditionalen Option reproduzieren. Die Reparatur lässt sich durch getrennte
Auswahl des unterstützten generischen Helpers und des expliziten Custom-Helpers
sowie den fokussierten Wiring-Test und die exakte Native-Matrix reproduzieren.

## Evidence

| Artefakt | SHA-256 | Ergebnis |
| --- | --- | --- |
| Initiales Deny-Synchronized-Upstream-stderr | `ce80d9e44a44a3d018435ba418db0498a5cd9f4048627d27c0f21a6b81bbdd0b` | Exit `77`, argparse weist `--control-root` ab |
| Initialer Deny-Status | `5f7ce3ab6d8be2a2946edf6669446aec8bb611e755468c11bafc8108304dd354` | Upstream veröffentlichte seine Adresse nicht |
| Post-Fix-Exact-Native-Matrix | `2218e7d5545f6b09dcb43d1b0779889fc778a16d3f3f65e2246598c3b54e4627` | 30 Controls Exit `0` |
| Post-Fix-Manifest | `1f44c2817676ef2952f70573917657d67645d8d85d57e829a47c9d67ee2ea548` | versiegeltes aktuelles Inventar |

Die vollständigen Pfade, Befehlszeilen, Working Directories und Retention-
Daten stehen in `finding.json` im Run
`20260719T162259Z-pr60-exact-head-revalidation-dfba422e`.

## Root Cause und Remediation

PR #60 behandelte den Custom-MIME-Helper und den gepinnten Framework-Helper,
als hätten sie dieselbe CLI. Das ist nicht der Fall. Der fokussierte Parent-
Patch lässt `APACHE_PHASE4_SYNCHRONIZED_UPSTREAM_CONTROL_ROOT=1`
`--control-root` nur für den expliziten Parent-eigenen Custom-Helper auswählen;
der generische Framework-Aufruf lässt ihn weg und erhält alle unterstützten
Control-File-Argumente. Die statische Wiring-Regression bewahrt beide Verträge.

## Akzeptanz, Validierung und legitime Controls

- Der generische gepinnte Framework-Helper erhält Ready-, Paused-, Release- und
  Server-Evidence-Argumente ohne `--control-root`.
- Der explizite Custom-MIME-Helper erhält `--control-root` nur bei Auswahl.
- Die fokussierte Wiring-Suite und Shell-Syntax bestehen.
- Die serielle exakte Native-30-Control-Phase-4-Matrix bestand nach der Reparatur.
- Framework, MRTS und beide Gitlinks bleiben unverändert.

## Abhängigkeiten, Blocker und Restrisiko

Abhängigkeiten sind die obige exakte read-only Framework-Revision und
task-eigene Apache/libModSecurity-Komponenten. Dieses Finding ist **fixed**,
nicht verified: Der finale lokale Codex-Security-Diff-Scan, Exact-Pushed-Head-
CI, CodeQL, SonarCloud, Review-/Thread-Evidence, Protected Merge und
Resulting-Master-Validierung bleiben für PR #60 erforderlich. Kein Runtime-Gate
wurde umgangen und kein Risiko wird akzeptiert.

Verwandtes Finding: `FND-PARENT-0038`; dies ist kein Duplikat, weil es den
Parent-Testvertrag statt der Response-Enforcement-Grenze betrifft.

## Historie

- `2026-07-19T17:06:28Z` — exaktes Native-Deny-Control deckte das nicht
  unterstützte Framework-CLI-Argument auf.
- `2026-07-19T18:20:42Z` — fokussierte Parent-Invocation-Auswahl, Wiring-
  Tests und die versiegelte exakte Native-Matrix bestanden; Finding lokal auf
  `fixed` gesetzt.
