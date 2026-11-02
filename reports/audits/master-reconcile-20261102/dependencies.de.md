# Build-Komponenteninventar und Advisory-Bewertung

**Sprache:** [English](dependencies.md) | Deutsch

Am 2026-11-02 gegen Connector430d3194fa04ca4aafcdaef6aeb256d21dc18f0c und Framework 91145b7ba721bdec4e89af754cf40bf496fd2a08 geprüft. Das [maschinenlesbare Inventar](component-inventory.json) enthält 17 native/Runtime-/Toolchain-Komponenten, vier direkte und sechs indirekte Envoy-Go-Abhängigkeiten, drei reine go.sum-Einträge und 11 beobachtete installierte Entwicklungspakete. Dies ist ein Quellen-/Build-Inventar, keine vollständige Binär- oder Container-SBOM. Eine Prüfsummendatei beweist keine Verlinkung.

## Befunde mit weiterem Arbeitsbedarf

| Komponente | Ausgewählter / geprüfter Stand | Einordnung |
| --- | --- | --- |
| NGINX | release-1.31.6 / behobene Mainline mindestens 1.31.7, beobachtet 1.31.8 | Upstream-Version liegt in fünf veröffentlichten Bereichen. HTTP/3 ist ein tatsächlicher optionaler Build-/Konfigurationspfad. Der ausgewählte H1-Fixture fehlen mehrere Advisory-Voraussetzungen; beliebige Nutzerkonfigurationen bleiben ungeklärt. Kein Exploit und kein gepatchter Build nachgewiesen. |
| Envoy | 1.39.1 / behoben 1.39.2, beobachtet 1.39.6 | BoringSSL-Korrektur für Zertifikat-Speicherverbrauch ist neuer. Das ausgewählte TLS-Template prüft eine vorgegebene CA; Angreiferkontrolle über ein zugelassenes Zertifikat wurde nicht belegt. Gepatchtes Tupel/Build und lokale Erreichbarkeit bleiben offen. |
| Parent Python | 3.15.1 / Security3.15.2 | Sicherheitsrelease korrigiert CA-Misstrauen und tar_filter-Linkersetzung. Exakte geprüfte Runner-Bereitschaft und erreichbare Archiv-/TLS-Voraussetzungen bleiben ungeprüft. Bestehende Python-/Bootstrap-PRs behalten ihre getrennte Zuständigkeit. |

Offizielle Nachweise: [NGINX-Advisories](https://nginx.org/en/security_advisories.html), [NGINX-Releases](https://nginx.org/news.html), [Envoy1.39.2](https://www.envoyproxy.io/docs/envoy/v1.39.2/version_history/v1.39/v1.39.2), [Python 3.15.2](https://www.python.org/downloads/release/python-3152/).

Diese offenen Punkte werden durch allgemeine CI nicht geschlossen. Kein Runtime-Tupel wurde ohne geprüfte Herkunft, Generator und passende Build-/Regressionsnachweise geändert. Als nächster Schritt bleiben ein gezieltes geprüftes Tupelupdate und passende Build-Prüfungen unter Erhalt der geschützten NGINX-Zulassung und bestehenden Wartungszuständigkeit.

## Durch Nachweise ausgeschlossene Bedingungen

Traefik 3.7.13 wird als hashgeprüftes offizielles Release geladen. Das [SNI-Advisory](https://github.com/traefik/traefik/security/advisories/GHSA-fh26-gfpp-7xxx) nimmt offizielle Go1.26-Binärdateien ausdrücklich aus; Parent-Go1.27.3 beweist keinen Neubau des offiziellen Hosts. Ausgewählte ForwardAuth-Templates konfigurieren keine verbindungsgebundene NTLM-/Negotiate-Authentifizierung. [ForwardAuth](https://github.com/traefik/traefik/security/advisories/GHSA-hrpp-p4fc-wwf8)- und [FastProxy](https://github.com/traefik/traefik/security/advisories/GHSA-53qr-784g-cj35)-Bedingungen bleiben für eigene Deployments relevant; diese wurden nicht qualifiziert. Neuester beobachteter Traefik-Stand ist 3.7.17.

Der tatsächliche Envoy-Paketgraph des Standard-Builds mit go1.27.3 enthält x/net-HTTP2/HPACK-, IDNA-, Trace- und interne Hilfspakete, aber kein golang.org/x/net/html. Deshalb sind [GO-2026-6866](https://pkg.go.dev/vuln/GO-2026-6866) und [GO-2026-6860](https://pkg.go.dev/vuln/GO-2026-6860), deren Modulbereich x/net v0.61.0 einschließt und deren Fix v0.62.0 ist, über diesen beobachteten Graphen nicht erreichbar. Neue Tags/eigene Builds erneut prüfen. Daraus folgt keine pauschale Sicherheitsbewertung für x/net oder übrige Module.

Framework-Python 3.14.10, OpenSSL 4.0.3, ModSecurity v3.0.17 und PCRE2 10.49 enthalten die ausgewählten veröffentlichten Korrekturen im Inventar. Apache 2.4.69, APR 1.7.6, APR-util 1.6.5, HAProxy 3.2.25, lighttpd 1.4.85 und PyYAML 6.0.3 entsprechen beobachteten Upstream-Versionen; Aktualität allein beweist keine Befundfreiheit. AWS-LC v5.11.0 ist ausdrücklich ein ungenutzter Zukunftskandidat und benötigt kein Runtime-Update allein wegen 5.12.0.

## Inventargrenzen

Installierte Ubuntu-Entwicklungsmetadaten für GCC/G++, APR/APR-util, curl, LMDB, PCRE2, OpenSSL, libxml2, YAJL und zlib wurden abgefragt. Mehrere installierte Versionen unterscheiden sich von kanonischen Quelltupeln. Sie sind getrennt erfasst; eine Verlinkung ausgewählter Produktartefakte oder Advisory-Bewertung distributionsgepatchter Pakete wurde nicht abgeleitet. Vollständige native transitive Features, eingebundene Submodule, Verlinkung geladener Artefakte, OS-/Container-Paketgraphen und vollständige Advisory-Abdeckung übriger Module bleiben ungeklärt.

Durch diesen Inventardurchlauf wurden keine Pakete oder Quellversionen aktualisiert. Die reine Coverage-Taskumgebung nutzt die bestehende hashgebundene coverage 7.17.0-Anforderung; keine globale Umgebung und kein Dependency-Lock wurden geändert.

Lokale Sonar-Secrets-Prüfung aufgrund ausdrücklicher Benutzeranweisung nicht ausgeführt.
