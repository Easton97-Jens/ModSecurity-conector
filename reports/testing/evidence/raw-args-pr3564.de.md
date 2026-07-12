# RAW Nachweise für Argumentsammlungen

**Sprache:** [English](raw-args-pr3564.md) | Deutsch

Status: Nur zugeordnet

Upstream PR: https://github.com/owasp-modsecurity/ModSecurity/pull/3564
Upstream-Repository: https://github.com/owasp-modsecurity/ModSecurity

PR #3564 führt RAW Argumentsammlungsunterstützung in ModSecurity ein:

- `ARGS_RAW`
- `ARGS_GET_RAW`
- `ARGS_POST_RAW`
- `ARGS_NAMES_RAW`
- `ARGS_GET_NAMES_RAW`
- `ARGS_POST_NAMES_RAW`

## Aktuelle Klassifizierung

Die lokal beobachtete ModSecurity v3-Referenz lautet:

| Repository | Local reference | Upstream | Observed commit | Observed version/tag |
| --- | --- | --- | --- | --- |
| ModSecurity v3 | `<external-source-root>/ModSecurity_V3` | https://github.com/owasp-modsecurity/ModSecurity | `0fb4aff98b4980cf6426697d5605c424e3d5bb60` | `v3.0.15` |

Diese Quelle wird als schreibgeschützt behandelt. RAW Argumentsammlungen werden nicht gezählt
aktiver allgemeiner PASS in diesem Repository, es sei denn, die lokale v3-Quelle ist konfiguriert
enthält die Funktion und sowohl Apache als auch NGINX geben den erwarteten echten HTTP zurück
Verhalten durch das gemeinsame Smoke-Harness.

## Regel importieren

Zukünftige RAW-ARGS YAML-Fälle können erst dann aktiv werden, wenn alle folgenden Punkte zutreffen:

- Quellbeweise deuten auf einen konfigurierten ModSecurity v3-Checkout mit PR #3564 hin
  Verhalten vorhanden;
- Apache und NGINX bauen auf dieser Quelle unter `BUILD_ROOT` auf;
- beide Connector-Smokes geben den erwarteten HTTP-Status für denselben YAML-Fall zurück;
- `verified_variables` wird nur durch das Bestehen aktiver Fälle aktualisiert.

Bis dahin bleibt RAW-ARGS mapped-only/evidence-only.
