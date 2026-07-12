# Traefik-deaktiviertes Profil

**Sprache:** [English](README.md) | Deutsch

## Verhalten

`disabled/traefik-engine-service.conf` setzt `enabled=off`; forwardAuth wird dadurch nicht zu einem nativen Pfad. Dies unterscheidet sich von `SecRuleEngine Off`, das
bei aktivem Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

## Validierung

Nach dem Anpassen der Hostpfade den im übergeordneten README genannten
Connector-Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1–P4-Verhalten ableiten.
