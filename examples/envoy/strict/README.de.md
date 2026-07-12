# Envoy-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

Der ext_proc-Service akzeptiert `late_action_policy: strict`, zeichnet nach
der Commit-Grenze aber aktuell `strict_abort_not_attempted` auf. Strict ist
optional und es wird keine Late-Reset-Konfiguration behauptet.

## Verwendung

Safe-ext_proc-Template und Service-Vertrag verwenden, generiertes YAML und
Service-JSON validieren und Host-Evidenz ergänzen, bevor auf ein striktes
Transportergebnis vertraut wird.
