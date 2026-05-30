# HAProxy SPOE/SPOA PoC Scaffold

documentation only

## Status
- documentation_only: true
- implementation_status: not_started
- runtime_verified: false
- decision_status: undecided
- promoted: false

## Zweck
Dieses Verzeichnis dient ausschließlich als dokumentarischer Platzhalter für
einen späteren HAProxy-SPOE/SPOA-PoC im Rahmen der bestehenden
Evidenzdokumente.

This directory does not contain a runnable HAProxy SPOE/SPOA PoC.

## Geplante, aber nicht erstellte Artefakte (planned only)
- `connectors/haproxy/poc/spoe/haproxy.cfg.example` (planned only)
- `connectors/haproxy/poc/spoe/spoe-agent.conf.example` (planned only)
- Framework-side tests: planned in ModSecurity-test-Framework, not in this repository.
- Framework-side report outputs: planned in ModSecurity-test-Framework, not in this repository.

The example configuration files are illustrative only and not runtime verified.

## Test- und Report-Ownership
No tests are stored in this connector repository.

All test definitions, test execution, runners, and generated reports belong to
Easton97-Jens/ModSecurity-test-Framework.

runtime_verified must remain false in this repository until external framework
evidence is produced.

## Nicht-Ziele
- Keine Runtime-Implementierung.
- Kein C-Code.
- Keine Python-/Shell-Skripte.
- Keine HAProxy-Konfiguration in diesem Verzeichnis.
- Keine SPOE-Agent-Konfiguration in diesem Verzeichnis.
- Keine Aussage, dass SPOE/SPOA funktionsfähig ist.

## Offene Punkte
- Exakte SPOE/SPOP-Konfigurationsdetails: Extern zu verifizieren.
- Vollständige ModSecurity-Semantik: Nicht belegbar aus dem aktuellen Repository.
- Request-/Response-/Intervention-Details: Noch zu prüfen.
