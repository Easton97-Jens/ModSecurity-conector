# Compile HAProxy


**Sprache:** [English](COMPILE_HAPROXY.md) | Deutsch

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

Dieser Guide beschreibt den Einsatz des HAProxy-SPOE/SPOP-ModSecurity-Pfads
außerhalb dieses Repositorys: HAProxy bereitstellen,
`haproxy-modsecurity-spoa` bauen, HAProxy-SPOE-Konfiguration verdrahten, den
SPOA-Prozess mit einem betreiberseitigen Process Manager starten und den ersten
Config-Check oder Start ausführen.

## Status und Grenzen

HAProxy selbst kann von der Distribution bereitgestellt oder lokal gebaut
werden. Dieses Repository baut den Prozess `haproxy-modsecurity-spoa` und
libmodsecurity-Binding-Checks. Der ausgewählte SPOE/SPOP-Pfad unterstützt nur
Requests und Response-Header; RESPONSE_BODY / Phase 4 ist
`not_implemented`, und das ausgemusterte Sample ist kein Laufzeitnachweis.

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
make smoke-haproxy
```

Optionale HAProxy-Repository-Validierung:

```sh
make test-haproxy-no-crs
make test-haproxy-with-crs
```

## Pfad 2: Externer Einsatz mit Distribution-Paketen

1. Installieren Sie HAProxy mit SPOE/SPOP-Unterstützung, Build-Werkzeuge und
   libmodsecurity-Header/-Libraries. Paketnamen unterscheiden sich je
   Distribution.
2. Pakete können HAProxy und libmodsecurity bereitstellen.
   `haproxy-modsecurity-spoa` muss weiterhin aus `connectors/haproxy` gebaut
   werden.
3. Holen Sie den Connector-Quellcode dieses Repositorys:

   ```sh
   git clone <modsecurity-conector-repo-url> ModSecurity-conector
   cd ModSecurity-conector
   ```

4. Bauen Sie Binding und SPOA-Prozess:

   ```sh
   make prepare-runtime-components
   make -C connectors/haproxy build-modsecurity-binding
   make -C connectors/haproxy build-spoa-runtime
   make -C connectors/haproxy self-test-modsecurity-binding
   make -C connectors/haproxy self-test-spoa-runtime
   ```

5. Kopieren Sie das gebaute SPOA-Binary und angepasste Konfigurationen in
   externe Runtime-/Config-/Log-Verzeichnisse:

   > Hinweis: `install` ist hier kein Paketmanager-Befehl. Er kopiert Dateien
   > und kann Berechtigungen setzen. Zum Beispiel ist
   > `sudo install -m 0755 file.so /target/file.so` ähnlich zu
   > `sudo cp file.so /target/file.so` gefolgt von
   > `sudo chmod 0755 /target/file.so`.

   ```sh
   sudo install -d -m 0755 <haproxy-config-dir> <modsecurity-config-dir> <haproxy-modsecurity-log-dir>
   sudo install -m 0755 <built-haproxy-modsecurity-spoa> <runtime-binary-dir>/haproxy-modsecurity-spoa
   sudo install -m 0644 examples/haproxy/spoe-modsecurity.conf <haproxy-config-dir>/spoe-modsecurity.conf
   sudo install -m 0644 examples/haproxy/modsecurity-agent.conf <haproxy-config-dir>/modsecurity-agent.conf
   sudo install -m 0644 examples/haproxy/haproxy-request-only.cfg <haproxy-config-dir>/haproxy.cfg
   sudo haproxy -c -f <haproxy-config-dir>/haproxy.cfg
   sudo systemctl reload <haproxy-service-name>
   ```

HAProxy verbindet sich über SPOE/SPOP mit dem SPOA-Prozess. Starten/restarten
Sie den SPOA mit einer betreiberseitigen Service Unit oder einem Process
Manager; dieses Repository installiert keine solche Unit.

## Pfad 3: Externer Einsatz aus Source

1. Installieren Sie Compiler-/Build-Voraussetzungen und HAProxy, falls Sie kein
   Paket verwenden.
2. Bauen Sie libmodsecurity v3 aus Source, falls Pakete nicht geeignet sind:

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

3. Klonen Sie dieses Repository und bauen Sie Binding/SPOA-Prozess mit den in
   Pfad 2 gezeigten `make -C connectors/haproxy ...`-Befehlen.
4. Installieren/kopieren Sie SPOA-Binary und Konfigurationen mit dem
   Platzhalter-Installationsmuster aus Pfad 2.
5. Validieren Sie HAProxy mit `haproxy -c -f <haproxy-config>`. Starten Sie das
   SPOA-Binary mit der vom gebauten Binary unterstützten Konfigurationsmethode.
   Die Source unterstützt `--config PATH`, daher kann ein betreiberartiger
   Aufruf so aussehen:

   ```sh
   <runtime-binary-dir>/haproxy-modsecurity-spoa --config <haproxy-config-dir>/modsecurity-agent.conf
   ```

## Config Snippets

```haproxy
filter spoe engine modsecurity config <spoe-config>

http-request send-spoe-group modsecurity request-check
http-request deny if { var(txn.modsec.blocked) -m bool }

backend <spoa-backend>
    mode spop
    server spoa <spoa-host>:<spoa-port>
```

Agent-Config-Form:

```text
listen <spoa-host>:<spoa-port>
rules-file <modsecurity-rules-file>
decision-log <decision-log-path>
audit-log <audit-log-path>
```

Siehe [examples/haproxy/README.de.md](examples/haproxy/README.de.md) für die
Erklärung dieser Direktiven, Platzhalter, Logs und Grenzen.

## Beispiel-Konfigurationen

Verwenden Sie die Dateien in [examples/haproxy/](examples/haproxy/README.de.md)
als Startpunkte für externe Konfiguration. Sie werden vom Repository nicht
automatisch installiert und sind keine universellen Produktionsdefaults.

## Logs

Prüfen Sie die relevanten Deployment-Logs; behandeln Sie die Pfade in den
Beispielen nicht als universelle Anforderungen.

- Webserver-/Proxy-Access-Logs.
- Webserver-/Proxy-Error-Logs.
- ModSecurity-Audit-Log, wenn aktiviert.
- Connector-Decision-Log, falls dieser Connector/Pfad eines hat.
- Sidecar-/Agent-Log, falls dieser Connector/Pfad eines hat.

## Troubleshooting

Prüfen Sie fehlende Header, fehlende Shared Libraries, falsche HAProxy-
SPOE-Konfiguration, falsche SPOP-Backend-Adresse, fehlenden Sidecar-/SPOA-
Prozess, falschen Regelpfad, fehlendes schreibbares Log-Verzeichnis und
RESPONSE_BODY-Annahmen außerhalb belegter Evidence.

## Nicht-Claims

- RESPONSE_BODY / Phase 4 ist nicht promoted.
- Force-all-FAIL-Zeilen sind kein Produktionssupport.
- Dieses Repository stellt keine systemd-Service-Unit für den SPOA-Prozess
  bereit.

## Verwandte Dokumente

- [examples/haproxy/README.de.md](examples/haproxy/README.de.md)
- `connectors/haproxy/docs/build.md`
- `connectors/haproxy/docs/validation.md`

## Common-SDK-Adoption-C-Prüfungen

HAProxy führt Config-, Direktiven-/Optionssemantik, Request-/Response-Mapper-Contracts, Event-JSONL-Helfer und globale Limits jetzt über das Common SDK, soweit diese Adoption-Schicht diese Pfade umsetzt. HAProxy-spezifisch bleiben SPOE/SPOP, generierte HAProxy-Konfigurationsfragmente, Prozess-Lifecycle, Frame-Parsing, Socket-Handling und Build-Glue.

`make check-haproxy-c17` ist die harte C17-Compile-Prüfung. `make check-haproxy-c23` und `make check-haproxy-future-c` sind optionale, compilerabhängige Prüfungen. Fehlen HAProxy- oder libmodsecurity-Header, meldet der direkte Check `BLOCKED` und beendet sich mit 77; der Lint-Wrapper behandelt dies als Skip. Dies ist nur Compile-/Struktur-Evidence und keine Production-, CRS-, Full-Matrix- oder Runtime-Verification.
