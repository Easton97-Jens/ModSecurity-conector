# Change Record: Parent-HAProxy-Runtime-Maintainability-Behebung

**Sprache:** [English](CR-20260730-sonar-haproxy-runtime-maintenance.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260730-sonar-haproxy-runtime-maintenance |
| Datum (UTC) | 2026-07-30 |
| Basis-Revision | `4e5d45072bf32ff822f4b1039517026416259493` |
| Tracking | Aktuelle HAProxy-SonarQube-Cloud-Maintainability-Behebung und initiale Draft-PR-Delivery. |
| Grenze | Parent `connectors/haproxy/`, dessen direkter Contract-Check sowie dieses bilinguale Change-Record-/Index-Paar. Framework, MRTS, Gitlinks, Workflows, Sonar-Konfiguration, Suppressions und `master` bleiben unverändert. |

## Motivation und Problemstellung

Das aktuelle Master-Inventar enthält 55 HAProxy-Maintainability-Zeilen plus ein
`python:S5332`-Loopback-Helper-Signal. Dieses fokussierte Inkrement extrahiert
wiederholtes SPOP-Argument-Parsing, trennt HTX-Request-/Response-End-of-Stream-
Behandlung, zentralisiert Build-Artefakt-Hashing und isoliert CRS-
Konfigurationsladen. Es beansprucht nicht, dass der Draft-PR jeden historischen
Baseline-Befund schließt.

## Akzeptanzkriterien

- Exaktes begrenztes SPOP-Key-Matching, typed-Value-Consumption, Owned-
  Header-/Body-Handling und Request-/Response-Lifecycle-State bleiben erhalten.
- HTX-Phase-2-Pre-Commit- und Phase-4-Late-Intervention-Verhalten bleiben mit
  genau einem Binding-Finalization-Callsite je Phase erhalten.
- Die SHA-256-Build-Evidence des Builders bleibt deterministisch und
  POSIX-Shell-sauber.
- CRS-Setup-File-Precedence, Example-Fallback, Rules-Directory-Laden und
  Cleanup-Verhalten bleiben erhalten.
- Alle Änderungen bleiben Parent-only und bei geändertem C C17-kompatibel.

## Implementierungsentscheidung und Begründung

Die SPOP-Runtime verwendet Tabellen und einen längenbewussten C-String-
Comparator für bekannte String-, Integer- und Response-Header-Argumente; das
literal-only Makro bleibt nur für echte Literale. Eigene variadische File-
Writer entfallen, unterbrochenes I/O wird ohne verschachtelte `continue`-Pfade
wiederholt. HTX-Lifecycle-Code ist in Request- und Response-Helper getrennt;
der direkte Contract-Checker folgt diesen Helfern. Der Builder besitzt eine
`sha256_of`-Pipeline. CRS-Laden im Binding hat jetzt einen gemeinsamen
Allocation-Cleanup-Pfad.

## Security-Auswirkung

Der geänderte Code verarbeitet peer-kontrollierte SPOP-Felder und nativen HTTP-
Lifecycle-State. Die Security-Invariante bleibt unverändert: Nur begrenzte,
erkannte typed Inputs dürfen den geparsten Request ändern, unbekannte Inputs
verwenden den bestehenden Skip-Pfad, und Phase-2-/Phase-4-Kontrollen dürfen
nicht durch Callback-Reihenfolge umgangen werden. Das aktuelle `python:S5332`-
Signal ist ein `already_safe` lokaler Testserver: Er bindet an das Literal
`127.0.0.1`, und Probe-URLs werden vor Verwendung als credential-free
`https://127.0.0.1` geprüft. Es wurde keine Suppression, Scanner-Exclusion
oder Kontrollschwächung genutzt.

## Geänderte Dateien

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`
- `connectors/haproxy/src/haproxy_modsecurity_binding.c`
- `connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c`
- `connectors/haproxy/htx-overlay/build-overlay.sh`
- `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`
- Dieses englisch/deutsche Change-Record-Paar und beide Indizes.

## Ausgeführte Befehle

| Kontrolle | Ergebnis |
| --- | --- |
| `cc -std=c17 -Wall -Wextra -Werror -fsyntax-only -Icommon/include -Iconnectors/haproxy/src connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` | bestanden |
| `python3 ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | bestanden: 26 Contracts |
| `shellcheck --severity=warning connectors/haproxy/htx-overlay/build-overlay.sh` | bestanden |
| `PYTHONDONTWRITEBYTECODE=1 python3 connectors/haproxy/harness/test_haproxy_htx_smoke_helper.py` im autoritativen Parent-Checkout | bestanden: 9 Tests |
| `git diff --check` | bestanden |

## Runtime-Evidence

Die fokussierte Python-Helper-Suite bestätigt ihre Local-Loopback-Kontrollen.
Der HTX-Checker verifiziert Source-Level-Lifecycle-Invarianten. Keines der
Ergebnisse beansprucht einen Live-HAProxy-plus-libmodsecurity-Enforcement-Run.

## Nicht ausgeführte Prüfungen mit Begründung

`make -C connectors/haproxy test-htx-overlay` hat seine 26 statischen Checks
abgeschlossen, konnte danach aber den bewusst nicht initialisierten Framework-
Helper in diesem isolierten Task-Worktree nicht importieren. `make -C
connectors/haproxy build-modsecurity-binding` endete mit 77, weil
libmodsecurity-Header und -Bibliothek unter `/src` und im registrierten
temporären Build-Root fehlen. Kein vollständiger Runtime-/Connector-Matrix-/
Codex-Security-Diff-Scan oder Hosted-Exact-Head-Check lief bisher.

## Bekannte Einschränkungen

Der Draft-PR behält bewusst unbearbeitete historische HAProxy-SonarQube-Cloud-
Baseline-Zeilen. Fehlende libmodsecurity-Development-Artefakte verhindern
lokale native Binding-/Link-/Runtime-Evidence.

## Verbleibende Risiken

Ein frisches Exact-Head-SonarQube-Cloud-Ergebnis kann verbleibende Baseline-
oder neu eingeführte Befunde zeigen; es ist erforderlich, bevor der PR als
verifiziert oder mergebar gelten kann.

## Finaler Diff- und Review-Status

Der lokale Diff ist Parent-only, hat seine verfügbaren fokussierten Checks
bestanden und ist für einen Draft-PR vorbereitet. Push, PR-Nummer, Exact Head,
Hosted-Checks, Review und SonarQube-Cloud-Ergebnisse werden absichtlich erst
nach ihrem tatsächlichen Eintritt dokumentiert.
