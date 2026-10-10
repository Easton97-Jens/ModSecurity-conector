# Change Record: CR-20261009-nginx-fresh-raw-run-mode

**Sprache:** [English](CR-20261009-nginx-fresh-raw-run-mode.md) | Deutsch

Dateisystem-Vertragsfix; Host-Integration steht aus.

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20261009-nginx-fresh-raw-run-mode |
| Datum (UTC) | 2026-10-09 |
| Basis-Revision | `dcbefad1144b38f1545399a9f72967fbb1b3d424` |

## Motivation und Problemstellung

Die Umask 077 des Aufrufers erzeugte den NGINX-Raw-Run mit 0700 und blockierte den nobody-Worker. Das Voraberstellen des exakten Runs scheitert korrekt an Freshness.

## Akzeptanzkriterien

Das frische NGINX-full_lifecycle-Raw-Kind erhält 0711. Vorhandene/Symlink-Kinder bleiben abgelehnt, Logs/Results privat und andere Routen unverändert.

## Implementierungsentscheidung und Begründung

Nach bestehenden Prüfungen erstellt mkdir -p nur den Parent; exklusives mkdir -m 0711 erstellt das exakte Raw-Kind. Kein vorhandenes Kind wird per chmod verändert oder wiederverwendet. Der Aufrufer stellt traversierbare Vorfahren bereit.

## Geänderte Dateien

`ci/runtime/lifecycle/run-no-crs-baseline.sh`; `tests/test_nginx_raw_run_creation.py`; dieses EN/DE-Change-Record-Paar.

## Ausgeführte Befehle

Alle Shell-Befehle verwendeten RTK. Erste Regression: fünf Tests, ein Fehler (0700 statt 0711). Gespeicherte Regression gegen die alte Source: sechs Tests, drei erwartete Fehler (Modus und spät erstelltes Verzeichnis/Symlink). Finaler Befehl: python3 -m unittest -v tests.test_nginx_raw_run_creation tests.test_no_crs_baseline_shell_environment tests.test_runtime_path_security tests.test_runtime_path_utils tests.test_resolve_runtime_paths, mit neutralem externem TMPDIR: 43 Tests, Exit 0, keine SKIPs, 6.690s. sh -n, shellcheck -S warning, Change-Record-Struktur und git diff --check bestanden. Anfängliche Sandbox-chown-Fehler bestanden bei privilegierter Wiederholung. Ein breiterer Lauf mit nginx im TMPDIR löste korrekt die Foreign-Connector-Ablehnung aus; die Wiederholung mit neutralem TMPDIR bestand. Logs: raw-run-mode-red.log und raw-run-mode-green-neutral.log unter /var/tmp/codex/ModSecurity-conector/analysis/nginx-all-required-20261008T124555Z.

## Security-Auswirkung

Das Raw-Kind erhält nur Traversierungsrechte, keine Lese- oder Schreibrechte für Gruppe/Andere. Bei umask 077 bleiben Logs/Results 0700. Exklusives mkdir lehnt ein nach Preflight erstelltes Kind ab. Bestehende Pfadprüfungen bleiben aktiv.

## Runtime-Evidence

Nur Dateisystem-Regressions-Evidence; kein HTTP-, Canonical-Ergebnis, Build oder E2E-PASS wird behauptet.

## Bekannte Einschränkungen

Der Aufrufer muss sichere traversierbare Vorfahren bereitstellen. Canonical-Evidence-Rechte sind unverändert; die fokussierte Grenze beweist nur, dass Canonical-RUN_DIR dort nicht erstellt wird, nicht dessen späteren Modus. Der Root-Testlauf beweist Erstellung durch EUID 0; ein separater Host-Lauf muss Root/Worker-Identitäten beweisen.

## Verbleibende Risiken

Nach Integration bleibt die Host-Lifecycle-Verifikation erforderlich.

## Nicht ausgeführte Prüfungen mit Begründung

Kein Build oder E2E in diesem isolierten Worker-Worktree. Vollständige Dokumentationslinks benötigen den befüllten Framework-Checkout und verbleiben bei der Integration.

## Finaler Diff- und Review-Status

Nur fokussierter Diff. Kein Commit/Push oder Framework/MRTS-Eingriff. Integrationsreview steht aus.
