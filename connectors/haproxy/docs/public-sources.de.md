# Öffentliche HAProxy-Quellen

**Sprache:** [English](public-sources.md) | Deutsch

Status: aktuelle Referenzen

Externe Quellen dokumentieren die vom Repository verwendeten HAProxy-Mechanismen. Sie
fördern nicht allein das Connector-Verhalten; Werbung kommt nur live
Laufzeitbeweise.

- HAProxy-Dokumentation: https://docs.haproxy.org/
- HAProxy-Konfigurationshandbuch:
  https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/
- HAProxy SPOE/SPOP-Referenz:
  https://raw.githubusercontent.com/haproxy/haproxy/master/doc/SPOE.txt
- HAProxy-Quelle: https://github.com/haproxy/haproxy

Repository-Quell-Pins für Clean-Clone-Builds sind in zentralisiert
`modules/ModSecurity-test-Framework/ci/lib/common.sh`. Die Standardkompilierung und
Der Laufzeitablauf ist in `docs/build/compilers/haproxy.md` dokumentiert. Das Getrennte
Der HTX-Beobachter mit vollem Lebenszyklus wird an HAProxy 3.2.21 angeheftet und in einen kopiert
Einweg-Arbeitsbaum; dass die Auswahl der Quelle den Betrachter nicht in einen verwandelt
Durchsetzungs- oder Fähigkeitsförderungspfad.
