# HAProxy-Strict-Profilgrenze

**Sprache:** [English](README.md) | Deutsch

## Status

Der native HTX-Parser akzeptiert `phase4-mode strict`, aber der aktuelle
Hostpfad zeichnet den gewünschten Abbruch als `not_attempted` auf. Strict ist
optional und hier wird kein ausführbares Profil behauptet.

## Verwendung

Das optionale Argument am nativen Filter setzen, mit `haproxy -c -f <config>`
validieren und es ohne neue Host-Evidenz nicht als client-sichtbaren Abbruch
darstellen.
