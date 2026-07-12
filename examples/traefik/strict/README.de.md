# Traefik-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

Common Runtime akzeptiert `phase4_mode=strict`, aber die native Go-Middleware
stuft disruptive P4-Entscheidungen nach Commit zu log-only herab. Strict ist
optional und es wird kein Abbruchprofil behauptet.

## Verwendung

Das Safe-UDS-Setup beibehalten, statische/dynamische Konfiguration und den
Engine-Service validieren und neue Host-Evidenz verlangen, bevor ein strikter
Transportanspruch erhoben wird.
