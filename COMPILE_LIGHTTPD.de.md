# Compile Lighttpd


**Sprache:** [English](COMPILE_LIGHTTPD.md) | Deutsch

## Inhaltsverzeichnis

- [Zweck](#zweck)
- [Status und Grenzen](#status-und-grenzen)
- [Überblick: Drei Pfade](#überblick-drei-pfade)
- [Pfad 1: Repository-Smoke / Validierung](#pfad-1-repository-smoke--validierung)
- [Pfad 2: Externer Einsatz mit Distribution-Paketen](#pfad-2-externer-einsatz-mit-distribution-paketen)
- [Pfad 3: Externer Einsatz aus Source](#pfad-3-externer-einsatz-aus-source)
- [Config Snippets](#config-snippets)
- [Beispiel-Konfigurationen](#beispiel-konfigurationen)
- [Logs](#logs)
- [Troubleshooting](#troubleshooting)
- [Nicht-Claims](#nicht-claims)
- [Verwandte Dokumente](#verwandte-dokumente)

## Zweck

Dieser Guide beschreibt den Einsatz des Lighttpd-Runtime-Pfads außerhalb dieses
Repositorys mit einem betreiberseitig bereitgestellten sidecar_proxy-
Decision-Service/Sidecar und externer Konfiguration.

## Status und Grenzen

Lighttpd kann betreiberseitig bereitgestellt oder über den Repository-Helper
gebaut werden. Hier gibt es kein natives Lighttpd-ModSecurity-Modul; externer
Einsatz ist `sidecar_proxy` / Phase 1.

## Überblick: Drei Pfade

| Pfad | Zweck | Haupteinsatz |
| --- | --- | --- |
| Pfad 1: Repository-Smoke | Repository-Evidence validieren | Entwickler / Reviewer |
| Pfad 2: Externer Einsatz mit Paketen | Distro-Pakete nutzen, wo kompatibel | Betreiber mit Systempaketen |
| Pfad 3: Externer Einsatz aus Source | ModSecurity und/oder Connector-Teile manuell bauen | Betreiber mit genauer Versionskontrolle |

## Pfad 1: Repository-Smoke / Validierung

Diese Befehle validieren Repository-Evidence. Sie sind nicht die externe
Installationsprozedur.

```sh
git submodule update --init --recursive
make setup-dev
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
```

Optionale Repository-Evidence:

```sh
make smoke-lighttpd-modsecurity
make smoke-lighttpd-crs
```

## Pfad 2: Externer Einsatz mit Distribution-Paketen

1. Installieren oder stellen Sie das Lighttpd-Runtime-Binary über Ihre
   Distribution, ein Vendor-Paket, Container-Image oder Deployment-Tooling
   bereit. Paketnamen und Servicenamen unterscheiden sich je Distribution.
2. Stellen Sie einen erreichbaren sidecar_proxy-Decision-Service/Sidecar
   bereit. Falls der Service libmodsecurity verwendet, installieren Sie
   kompatible libmodsecurity-Header/-Libraries oder Runtime-Pakete.
3. Holen Sie dieses Repository für Beispielkonfigurationen und Smoke-Referenzen:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Passen Sie die Beispielkonfiguration an Listener, Backend,
   Decision-Service-URL/-Adresse, Regelverzeichnis, CRS-Verzeichnis,
   Runtime-Verzeichnis und Log-Verzeichnis an.
5. Führen Sie den ersten Syntax-Check/Start mit betreibergewählten
   Binary-Platzhaltern aus:

   ```sh
   <lighttpd-bin> -tt -f examples/lighttpd/lighttpd-sidecar-proxy.conf
   <lighttpd-bin> -D -f examples/lighttpd/lighttpd-sidecar-proxy.conf
   ```

6. Prüfen Sie Runtime-Logs, Decision-Service-Logs und ModSecurity-Audit-/
   Decision-Logs, wenn das Backend sie unterstützt.

## Pfad 3: Externer Einsatz aus Source

Source-basierter externer Einsatz kann den gepinnten Lighttpd-Runtime-Build-
Helper aus Pfad 1/2 oder einen betreiberseitig gebauten kompatiblen Lighttpd
verwenden. Es bleibt ein sidecar_proxy-Pfad, kein nativer Connector. Wenn das
Sidecar-Backend libmodsecurity verwendet, bauen Sie libmodsecurity nach Bedarf.

Falls Ihr Decision-Backend libmodsecurity verwendet und Pakete nicht geeignet
sind, bauen Sie libmodsecurity v3 aus Source:

Installieren Sie zuerst die Build-Voraussetzungen für Ihr Betriebssystem.
Verwenden Sie dann entweder den von Ihrem Deployment ausgewählten
libmodsecurity-Ref oder ermitteln Sie vor dem Build den Repository-/Framework-
Pin. Das folgende Beispiel ist ein Upstream-Style-Beispiel, keine
repository-eigene Build-Garantie:

```sh
git clone --depth 1 -b <modsecurity-v3-ref> https://github.com/owasp-modsecurity/ModSecurity.git ModSecurity-v3
cd ModSecurity-v3
git submodule update --init --recursive
./build.sh
./configure --prefix=<libmodsecurity-prefix>
make -j"$(nproc)"
sudo make install
```

Ersetzen Sie `<modsecurity-v3-ref>` und `<libmodsecurity-prefix>` durch vom
Betreiber gewählte Werte. Prüfen Sie Upstream-Voraussetzungen und Flags für Ihr
Betriebssystem.

Danach bauen oder starten Sie Ihren betreiberseitig bereitgestellten
Decision-Service/Sidecar, passen die Beispielkonfiguration an, führen den ersten
Syntax-Check/Start aus Pfad 2 aus und prüfen Logs.

## Config Snippets

```yaml
server.modules += ("mod_proxy")
proxy.server = (
  "" => (("host" => "<sidecar-or-backend-host>", "port" => <port>))
)
```

Siehe [examples/lighttpd/README.de.md](examples/lighttpd/README.de.md) für die
Erklärung dieser Direktiven, Platzhalter, Logs und Grenzen.

## Beispiel-Konfigurationen

Verwenden Sie die Dateien in
[examples/lighttpd/](examples/lighttpd/README.de.md) als Startpunkte für externe
Konfiguration. Sie werden vom Repository nicht automatisch installiert und sind
keine universellen Produktionsdefaults.

## Logs

Prüfen Sie die relevanten Deployment-Logs; behandeln Sie die Pfade in den
Beispielen nicht als universelle Anforderungen.

- Webserver-/Proxy-Access-Logs.
- Webserver-/Proxy-Error-Logs.
- ModSecurity-Audit-Log, wenn aktiviert.
- Connector-Decision-Log, falls dieser Connector/Pfad eines hat.
- Sidecar-/Agent-Log, falls dieser Connector/Pfad eines hat.

## Troubleshooting

Prüfen Sie fehlendes Runtime-Binary, fehlenden Sidecar-/Auth-/Decision-Service,
falsche Backend-Adresse, fehlende Shared Libraries, falschen Regelpfad,
fehlendes schreibbares Log-Verzeichnis und Response-Body-Annahmen außerhalb
belegter Evidence.

## Nicht-Claims

- Lighttpd ist hier kein Production-Ready-Nachweis.
- Dieses Repository stellt hier keine native Lighttpd-ModSecurity-Integration
  bereit.
- Der aktuelle Pfad ist `sidecar_proxy` / Phase 1.
- FastCGI/SCGI/mod_magnet/Lua sind hier nicht implementiert.
- RESPONSE_BODY / Phase 4 ist nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.

## Verwandte Dokumente

- [examples/lighttpd/README.de.md](examples/lighttpd/README.de.md)
- `connectors/lighttpd/docs/build.md`
- `connectors/lighttpd/docs/validation.md`
