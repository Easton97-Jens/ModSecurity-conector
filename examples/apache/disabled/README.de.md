# Apache-deaktiviertes Profil

**Sprache:** [English](README.md) | Deutsch

## Verhalten

`disabled/httpd.conf` setzt `modsecurity off`; Apache erzeugt keine Connector-Transaction. Dies unterscheidet sich von `SecRuleEngine Off`, das
bei aktivem Hostconnector die Regelauswertung innerhalb der Engine abschaltet.

## Validierung

Nach dem Anpassen der Hostpfade den im übergeordneten README genannten
Connector-Validierungsbefehl verwenden. Aus einem deaktivierten Profil kein
P1–P4-Verhalten ableiten.
