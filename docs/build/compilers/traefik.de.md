<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build-, Source- und Paketwege: Traefik

**Sprache:** [English](traefik.md) | Deutsch

## Zweck und aktueller Integrationspfad

Dieser Guide dokumentiert den ausgewählten Integrationspfad
`native-middleware` für Traefik: native Traefik-Middleware mit privatem persistentem UDS-Engine-Service. Der kanonische Kernlauf ist
`make full-lifecycle-traefik-native`. Build-, Konfigurations-, Start- und Kompatibilitäts-
Smokes bleiben davon getrennt.

## Die drei Wege im Vergleich

| Weg | Für wen? | Systemweite Änderungen | Baut Host aus Source? | Kernpfad möglich? | Evidence möglich? |
| --- | --- | --- | --- | --- | --- |
| Repository-Testweg | Entwicklung und CI | Nein | Repository-gesteuert | Ja | Ja, nach Full Lifecycle |
| Lokaler Source-Build | Entwicklung und Integration | Optional | Verifiziertes Binary; Middleware/Service aus Source | Ja | Ja, nur ausgewählter Run |
| Paketweg | Schneller lokaler Einstieg | Ja | Meist nein | Nur mit Source-Anteil | Nur passendes Profil und Run |

Der Paketstatus dieses Connectors lautet exakt
`package-assisted source build`. Pakete liefern Abhängigkeiten und möglicherweise einen Host, während Repository-Connector oder Hostintegration ein Source-Build bleiben. Paketinstallation allein ist keine Evidence des ausgewählten Kerns.

## Gemeinsame Voraussetzungen

Git, ein beschreibbarer externer Stamm, Go- und C/C++-Buildtools, libmodsecurity-Eingaben und das Framework-Submodule. Die Runtime-Vorbereitung liefert das gepinnte Hostbinary über die Provenienzrichtlinie.

Der Test- und Source-Weg brauchen nur Basistools und einen beschreibbaren
externen Stamm, keine globale Installation des ausgewählten Connectors. Vor
einer Paketinstallation die Verfügbarkeit abfragen:

```sh
# Debian / Ubuntu (apt)
apt-cache policy build-essential pkg-config git curl ca-certificates
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
dnf info gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
```

Auf einem Rechner nur die Zeile der passenden Distributionsfamilie ausführen.

`VERIFIED_RUN_PARENT` muss außerhalb des Git-Checkouts liegen. Er enthält
Build-, Cache-, Runtime-, Log- und Evidence-Dateien und darf keine Secrets im
Namen tragen. `CACHE_ROOT` ist Cache-v2 mit wiederverwendbaren Eingaben, nicht
mit kanonischer Evidence. Die vorbereiteten, wirksamen Quellen zeigt:

```sh
make runtime-components-inventory
make runtime-components-sources
```

## Weg 1: Repository-gesteuert testen

Git, ein beschreibbarer externer Stamm, Go- und C/C++-Buildtools, libmodsecurity-Eingaben und das Framework-Submodule. Die Runtime-Vorbereitung liefert das gepinnte Hostbinary über die Provenienzrichtlinie.

Die folgenden Befehle klonen den definierten Branch, initialisieren das
Framework und führen alle getrennten Stufen aus. Sie installieren keinen
Connector systemweit. Fehlen Basistools, zuerst im Paketweg deren Verfügbarkeit
prüfen und nur die dort gezeigten Basispakete installieren.

```sh
git clone --recurse-submodules https://github.com/Easton97-Jens/ModSecurity-conector.git
cd ModSecurity-conector
git switch feature/all-connectors-no-crs-baseline
git submodule update --init --recursive
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build"
make check-framework
make prepare-runtime-components
make prepare-traefik-runtime
make build-traefik
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
run_id="traefik-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

| Befehl | Zweck | Voraussetzung | Ergebnis/Ort | Exit- und Evidence-Grenze |
| --- | --- | --- | --- | --- |
| `git clone` / `git switch` / `git submodule update` | definierter Checkout | Netzwerkzugang und Git | Checkout mit Framework-Submodule | Git-Fehler sind keine Build- oder Runtime-Evidence. |
| `make check-framework` | Framework-Vertrag prüfen | initialisiertes Submodule | bestätigter Framework-Pfad | `77` kann ein fehlendes Framework als BLOCKED melden; kein Connector-Test. |
| `make prepare-runtime-components` + `make prepare-traefik-runtime` | Cache-v2 und Host-/Source-Eingaben vorbereiten | beschreibbarer externer Run-Root | Provenienz, Cache und vorbereitete Eingaben | `77` bedeutet bewusst blockierte Voraussetzung; Cache ist keine Evidence. |
| `make build-traefik` | Buildstufe | Vorbereitung und Toolchain | `$BUILD_ROOT/stages/traefik/build/results` | `0` ist Stufenerfolg, kein Config- oder Trafficnachweis. |
| `make check-config-traefik` | Konfiguration laden/prüfen | erzeugter Host/Connector | `$BUILD_ROOT/stages/traefik/config_load/results` | `0` ist kein gesendeter HTTP-Request. |
| `make start-smoke-traefik` | Host ohne Volltraffic starten | lesbare Konfiguration und freie lokale Ressourcen | `$BUILD_ROOT/stages/traefik/start_smoke/results` | `0` ist keine Full-Lifecycle-Evidence. |
| `make runtime-smoke-traefik` | begrenzten repository-eigenen Runtime-Smoke ausführen | vorbereiteter Host und lokale Ports | `$BUILD_ROOT/stages/traefik/minimal_runtime_smoke/results` | `0` gilt nur für diesen Smoke. |
| `make full-lifecycle-traefik-native` | ausgewählten No-CRS-Kernlauf ausführen | sicherer Run-Identifier | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/traefik/$run_id` | Kanonische Artefakte erst nach anschließendem Evidence-Check bewerten. |
| `make evidence-check-traefik` | bereits erzeugte kanonische Artefakte validieren | derselbe Run-Identifier und vollständige Artefakte | `$VERIFIED_RUN_ROOT/evidence/no-crs-evidence/traefik/$run_id` | validiert vorhandene Evidence; erzeugt keine neuen Logs oder Runtime-Dateien. |

`0` bedeutet Erfolg der jeweiligen Stufe. `77` steht für eine bewusst
blockierte Voraussetzung, etwa fehlendes Framework oder einen ungeeigneten
externen Root. `2` kann bei ungültiger Stage-, Connector- oder
Eingabeauswahl auftreten. Andere Nichtnullwerte sind fehlgeschlagene oder
weitergereichte Checks; sie sind nicht als stärkere Aussage zu interpretieren.

### Validierung

Der vorherige Block führt mit demselben `run_id` Config-, Start- und
HTTP/1.1-Smoke sowie den ausgewählten P1–P4-Kernlauf aus. Die folgenden Befehle
prüfen Host, Artefakt und dynamische Library erneut, wiederholen die
repository-gesteuerten Config-/Start-/Runtime-Checks und validieren die bereits
erzeugte Evidence. Der Evidence-Check startet keinen neuen Kernlauf.

```sh
test -x "$CACHE_ROOT/shared/traefik/bin/traefik"
"$CACHE_ROOT/shared/traefik/bin/traefik" version
test -x "$VERIFIED_RUN_ROOT/runs/traefik/$run_id/traefik-runtime/engine-build/traefik-engine-service"
ldd "$VERIFIED_RUN_ROOT/runs/traefik/$run_id/traefik-runtime/engine-build/traefik-engine-service" | grep -F libmodsecurity
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
make runtime-components-inventory
make runtime-components-sources
```

## Weg 2: Lokal aus Source bauen

Die native Middleware und der private UDS-Engine-Service sind Repository-Source-Builds mit Go, CGo/Common und libmodsecurity. Der ausgewählte Traefik-Host ist ein verifiziertes Releasebinary und wird nicht als gepflegter vollständiger Host-Source-Build dargestellt.

Das Go-Modul `connectors/traefik/native_middleware/go.mod` deklariert `go 1.24.0`. Vor dem Build `go version` prüfen; der Paketname allein verspricht keine passende Go-Version.

Die folgenden Pins sind Eingaben des unterstützten Vorbereiters. Bei einem
geänderten Pin sind `runtime-components-inventory` und
`runtime-components-sources` maßgeblich; besonders bei beweglichen
libmodsecurity-Referenzen wird der aufgelöste Commit dort dokumentiert.

| Komponente | Pin/Version | Quelle | Integrität/Commit |
| --- | --- | --- | --- |
| Traefik host binary | 3.7.5 (`TRAEFIK_VERSION`) | https://github.com/traefik/traefik/releases/download/v3.7.5/traefik_v3.7.5_linux_amd64.tar.gz | SHA256 `9da81a928fde965c2c4678698bbc28bc3f600223b14c32b35bd480bf5ec863dc` |
| native middleware and engine service | current checkout commit | connectors/traefik | Git commit plus external build provenance |
| libmodsecurity | configured `MODSECURITY_GIT_REF` (default `v3/master`) | https://github.com/owasp-modsecurity/ModSecurity.git | resolved commit is recorded in Cache-v2 provenance |

`-O2 -g` ist ein nachvollziehbarer Entwicklungswert, kein Repository-Default
und keine Vorgabe für ein Deployment. `jobs` ist die Anzahl paralleler
Compilerprozesse; bei wenig RAM beispielsweise `2` wählen. `CPPFLAGS`,
`LDFLAGS`, `PKG_CONFIG_PATH` und `LD_LIBRARY_PATH` nur für bewusst gewählte
Header-, Bibliotheks- oder Stagingpfade setzen.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/traefik-source"
export CC=gcc
export CXX=g++
export CFLAGS="-O2 -g"
export CXXFLAGS="-O2 -g"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-traefik-runtime
make runtime-components-inventory
make runtime-components-sources
run_id="traefik-source-$(date -u +%Y%m%dT%H%M%SZ)"
MAKE_JOBS="$jobs" make -C connectors/traefik build-native-middleware
MAKE_JOBS="$jobs" make -C connectors/traefik test-native-middleware
MAKE_JOBS="$jobs" make -C connectors/traefik build-engine-service
MAKE_JOBS="$jobs" make -C connectors/traefik test-engine-service
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
```

Die fokussierten Befehle bauen die lokale native Middleware und ihren privaten UDS-Engine-Service. Der ausgewählte Host bleibt das verifizierte Traefik-Binary aus der Vorbereitung; ForwardAuth-Kompatibilität ist nicht der ausgewählte Weg.

| Befehlsgruppe | Zweck | Voraussetzung | Ergebnis und Grenze |
| --- | --- | --- | --- |
| Source-Buildbefehle oben | ausgewählten Host, Modul oder Service aus Source bauen | vorbereitete Provenienz, Toolchain und externer Buildroot | Artefakte und Command-/Source-Info-Records unter `$BUILD_ROOT`; Exit `0` ist nur Build-Erfolg. |
| gezeigte Config-/Test-/Runtime-Targets | Artefakt, ABI und Loader im selben Staging prüfen | passende Header, Bibliotheken und lesbare Konfiguration | Die Targets prüfen das erzeugte Modul bzw. den Service und dessen Library-Auflösung; `77` kann eine fehlende Voraussetzung melden. |
| `make full-lifecycle-traefik-native` + Evidence-Check | ausgewählten Kernpfad ausführen und Artefakte validieren | sicherer `run_id` und vollständige Runtime | Evidence unter `evidence/no-crs-evidence/traefik/$run_id`; `2` steht für ungültige Eingabe/Stufe, andere Fehler bleiben Fehler. |

Der unterstützte Build wird dabei durch `connectors/traefik/build/build-native-middleware.sh`, `connectors/traefik/build/build-engine-service.sh` umgesetzt; die
Root-Stufen dispatchen über
`ci/runtime/lifecycle/run-connector-stage.sh`, der Full Lifecycle über
`ci/runtime/lifecycle/run-no-crs-baseline.sh`. Diese Skripte sind die
Implementierung hinter den gezeigten Make-Targets, nicht eine zweite,
eigenständig zu kopierende Handbauanleitung.

Hostbinary, lokales Plugin, File-Provider-Konfiguration, UDS-Berechtigungen, Engine-Service und libmodsecurity-Laufzeitbibliothek sind ein invocation-lokaler Satz. Ein Standardhostpaket enthält weder native Middleware noch ihren Engine-Service.

### Prefix und Staging

| Ort | Verwendung | Grenze |
| --- | --- | --- |
| `/usr` | vom Distributionspaket verwaltet | nicht als manueller Default überschreiben |
| `/usr/local` | bewusste lokale Installation | vorher Dateien inventarisieren |
| `/opt/modsecurity-connector` | bewusst gewählter isolierter Prefix | `PKG_CONFIG_PATH` und Loaderpfad gezielt setzen |
| `$HOME/.local` | benutzerlokale Installation | kein gemeinsam genutzter Systemhost |
| unter `VERIFIED_RUN_PARENT` | empfohlenes externes Staging | Standard für diesen Entwicklungsweg; außerhalb des Checkouts |

Der unterstützte Vorbereiter besitzt den exakten Upstream-Configure- und
Installationsaufruf. Seine erzeugten Command-, Source-Info- und
Artifact-Records im externen Buildroot sind der nachvollziehbare
Konfigurations- und Kompilierungsnachweis; diese Anleitung erfindet keinen
zweiten Handaufruf.

### Validierung

Die folgenden Befehle prüfen das aufgelöste Hostbinary an seinem dokumentierten
externen Staging- oder Cachepfad nach Vorbereitung beziehungsweise Source-Build.
Danach prüfen die Artefaktbefehle, dass das erzeugte Modul oder der Service
vorhanden ist und `ldd` `libmodsecurity` auflöst. Die unterstützten Targets
prüfen anschließend Link, Konfiguration, Start oder den ausgewählten Lifecycle.

```sh
test -x "$CACHE_ROOT/shared/traefik/bin/traefik"
"$CACHE_ROOT/shared/traefik/bin/traefik" version
test -x "$BUILD_ROOT/traefik-engine-service/traefik-engine-service"
ldd "$BUILD_ROOT/traefik-engine-service/traefik-engine-service" | grep -F libmodsecurity
go version
grep -Fx 'go 1.24.0' connectors/traefik/native_middleware/go.mod
make -C connectors/traefik test-engine-service
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

## Weg 3: Über Pakete beziehungsweise paketgestützt installieren

Status: `package-assisted source build`. Pakete liefern Abhängigkeiten und möglicherweise einen Host, während Repository-Connector oder Hostintegration ein Source-Build bleiben. Paketinstallation allein ist keine Evidence des ausgewählten Kerns.

Pakete liefern nur Buildabhängigkeiten. Ein Standard-Traefik-Paket oder unabhängiges Releasebinary enthält nicht die repository-native Middleware oder den persistenten UDS-Engine-Service.

Paketnamen sind releaseabhängig. Diese Abfrage erfolgt vor jeder Installation;
Fedora `mod_security` ist ModSecurity v2 und kein Ersatz für
`libmodsecurity-devel` aus dem v3-Pfad.

Die ersten Befehle sind für **Debian / Ubuntu (apt)**, die folgenden für
**Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)**. Nur die passende Familie
verwenden.

```sh
# Debian / Ubuntu (apt)
apt-cache policy build-essential pkg-config git curl ca-certificates
apt-cache policy golang-go libmodsecurity-dev
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
dnf info gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
dnf info golang libmodsecurity-devel
# Host-package availability inquiry only; no package is selected by this query
apt-cache search '^traefik$'
dnf search traefik
```

Die letzten Abfragezeilen ermitteln nur, ob eine Distribution ein Traefik-Hostpaket anbietet; kein Ergebnis gilt als ausgewählter Host, weil das Repository sein verifiziertes Binary samt Source-gebauter nativer Middleware und Engine-Service nutzt.

Nur nach erfolgreicher Prüfung und nach eigener Kontrolle der Liste installieren:

```sh
# Debian / Ubuntu (apt)
sudo apt update
sudo apt install --yes build-essential pkg-config git curl ca-certificates
sudo apt install --yes golang-go libmodsecurity-dev
# Fedora / RHEL / Rocky Linux / AlmaLinux (dnf)
sudo dnf install -y gcc gcc-c++ make pkgconf-pkg-config git curl ca-certificates
sudo dnf install -y golang libmodsecurity-devel
```

`sudo` wird verwendet, weil Paketdatenbank und Systempfade gewöhnlich
Administratorrechte benötigen. In CI oder einem Container ist der Prozess oft
bereits root; dann `sudo` weglassen statt die Paketliste zu ändern.

Pakete liefern nur den Abhängigkeits-/Hostanteil. Anschließend diesen unterstützten Source-Follow-up ausführen; die Paketinstallation baut weder den ausgewählten Connector noch die Hostintegration allein.

```sh
export VERIFIED_RUN_PARENT="$HOME/modsecurity-connector-work"
export VERIFIED_RUN_ROOT="$VERIFIED_RUN_PARENT/ModSecurity-conector-verified"
export CACHE_ROOT="$VERIFIED_RUN_ROOT/cache-v2"
export BUILD_ROOT="$VERIFIED_RUN_ROOT/build/traefik-package"
jobs="$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf '2')"
make check-framework
make prepare-runtime-components
make prepare-traefik-runtime
make runtime-components-inventory
make runtime-components-sources
run_id="traefik-package-$(date -u +%Y%m%dT%H%M%SZ)"
MAKE_JOBS="$jobs" make -C connectors/traefik build-native-middleware
MAKE_JOBS="$jobs" make -C connectors/traefik test-native-middleware
MAKE_JOBS="$jobs" make -C connectors/traefik build-engine-service
MAKE_JOBS="$jobs" make -C connectors/traefik test-engine-service
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
```

| Befehlsgruppe | Zweck | Voraussetzung | Ergebnis und Grenze |
| --- | --- | --- | --- |
| Source-Buildbefehle oben | ausgewählten Host, Modul oder Service aus Source bauen | vorbereitete Provenienz, Toolchain und externer Buildroot | Artefakte und Command-/Source-Info-Records unter `$BUILD_ROOT`; Exit `0` ist nur Build-Erfolg. |
| gezeigte Config-/Test-/Runtime-Targets | Artefakt, ABI und Loader im selben Staging prüfen | passende Header, Bibliotheken und lesbare Konfiguration | Die Targets prüfen das erzeugte Modul bzw. den Service und dessen Library-Auflösung; `77` kann eine fehlende Voraussetzung melden. |
| `make full-lifecycle-traefik-native` + Evidence-Check | ausgewählten Kernpfad ausführen und Artefakte validieren | sicherer `run_id` und vollständige Runtime | Evidence unter `evidence/no-crs-evidence/traefik/$run_id`; `2` steht für ungültige Eingabe/Stufe, andere Fehler bleiben Fehler. |

### Validierung

`libmodsecurity` muss als v3-Entwicklungsabhängigkeit Header und
pkg-config-Metadaten liefern. Fehlt einer dieser Befehle, zum
repository-gesteuerten Source-Build zurückkehren; kein ModSecurity-v2-Paket
stillschweigend einsetzen.

```sh
pkg-config --exists libmodsecurity
pkg-config --atleast-version=3.0 libmodsecurity
pkg-config --modversion libmodsecurity
pkg_version="$(pkg-config --modversion libmodsecurity)"
case "$pkg_version" in 3.*) ;; *) printf '%s\n' "libmodsecurity major version must be 3: $pkg_version" >&2; exit 1 ;; esac
pkg-config --cflags libmodsecurity
pkg-config --libs libmodsecurity
make check-config-traefik
test -x "$CACHE_ROOT/shared/traefik/bin/traefik"
"$CACHE_ROOT/shared/traefik/bin/traefik" version
test -x "$BUILD_ROOT/traefik-engine-service/traefik-engine-service"
ldd "$BUILD_ROOT/traefik-engine-service/traefik-engine-service" | grep -F libmodsecurity
go version
grep -Fx 'go 1.24.0' connectors/traefik/native_middleware/go.mod
make -C connectors/traefik test-engine-service
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

## Nach dem Build konfigurieren

Das Config-Target prüft die Repository-Connectorkonfiguration. Der ausgewählte native Full-Lifecycle startet den gepinnten Host getrennt mit lokalem Plugin und UDS-Engine; ForwardAuth-Kompatibilität ist kein Ersatz.

Die gewählte Konfiguration, Regeln und Modulpfade werden durch die
repository-eigenen Targets erzeugt oder geprüft. Konfigurationsdateien müssen
lesbar sein; keine Cookies, Autorisierungswerte, Tokens, privaten Schlüssel
oder Rohlogs in Konfiguration oder Evidence ablegen.

```sh
make check-config-traefik
```

## Build und Installation validieren

Für alle Wege gilt: Hostbinary und Version prüfen, Connectorartefakt und
Shared Libraries im ausgewählten Staging betrachten, dann Config- und
Start-Smoke ausführen. Die Source- und Paketwege enden deshalb jeweils mit
ihrem Validierungsblock; ein einzelner Compile oder Link reicht nicht.

```sh
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
```

## Realen HTTP/1.1-Test ausführen

`make runtime-smoke-traefik` ist der unterstützte repository-eigene
Minimal-Smoke mit realem HTTP/1.1-Traffic für seine dokumentierte Route. Die
konkreten lokalen Ports, URLs und Requests werden aus der erzeugten
Konfiguration abgeleitet; keinen zweiten `curl`-Endpoint erfinden. Für den
ausgewählten P1–P4-Kernpfad, soweit anwendbar, folgt der Full Lifecycle:

```sh
run_id="traefik-http11-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

Der Minimal-Smoke und der Full Lifecycle haben unterschiedliche Grenzen. Ein
P1-Deny, P2/P3/P4-Beobachtungen oder ein PASS gelten nur für den tatsächlich
ausgeführten repository-definierten Fall und werden hier nicht zu einer
allgemeinen Capability-Aussage ausgeweitet.

## Evidence und Logs prüfen

Nach einem Full Lifecycle liegen abgeleitete, run-gebundene Verzeichnisse unter
`$VERIFIED_RUN_ROOT`: Evidence in
`evidence/no-crs-evidence/traefik/$run_id`, Builddateien in
`build/traefik/$run_id`, Runtime-Dateien in `runs/traefik/$run_id` und
sanitisierte Logs in `run-logs/traefik/$run_id`. Allgemeine Stufenresultate
liegen unter `$BUILD_ROOT/stages/traefik`. Pfade sind abgeleitet, nicht feste
Systempfade.

```sh
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
make runtime-components-inventory
make runtime-components-sources
```

Evidence erst nach dem Check teilen und sensible Werte vorher entfernen. Cache
und Downloads sind wiederverwendbare Eingaben, keine Evidence.

## Aktualisieren und neu bauen

Den Checkout nur kontrolliert aktualisieren, danach Submodule und Provenienz
erneut prüfen. Einen alten Cache nicht als Beleg für neue Pins behandeln.

```sh
git pull --ff-only
git submodule update --init --recursive
make runtime-components-inventory
make runtime-components-sources
make check-framework
make prepare-runtime-components
make prepare-traefik-runtime
make build-traefik
```

## Deinstallieren und bereinigen

Repository-Testweg: Den externen `VERIFIED_RUN_PARENT` erst nach Inspektion
oder Archivierung der gewünschten Evidence leeren; der Git-Checkout bleibt
unverändert. `rmdir` entfernt nur leere Verzeichnisse und ist deshalb der
sichere Abschluss statt eines unkontrollierten rekursiven Löschbefehls.

```sh
find "$VERIFIED_RUN_PARENT" -maxdepth 1 -mindepth 1 -print
rmdir "$VERIFIED_RUN_PARENT"
```

Source-Build: Externes Staging oder einen bewusst gewählten Prefix erst nach
Inventarisierung entfernen. Eine Installation unter `/usr` oder `/usr/local`
nicht pauschal löschen. Paketweg: Nur tatsächlich selbst installierte
Connectorpakete entfernen; Benutzerdaten und Evidence nicht ungefragt löschen.

```sh
sudo apt remove golang-go
sudo dnf remove golang
```

## Troubleshooting

### Testweg

Bei Exit `77` zuerst Framework-Submodule, absoluten externen Root, fehlende
Basistools und Cache-Provenienz prüfen. Bei Exit `2` Connector-, Stage- und
Run-ID-Eingaben prüfen. Ist ein Port belegt, den vorherigen lokalen Prozess
geordnet beenden und den Run mit neuer Run-ID wiederholen; Cache-Einträge nicht
blind mischen oder umbenennen.

### Source-Build

Fehlender Compiler oder Header: die Source-Voraussetzungen und die gewählte
Toolchain prüfen. Findet `pkg-config` libmodsecurity nicht, Header- und
Library-Root sowie `PKG_CONFIG_PATH` prüfen. Bei ABI- oder Modulfehlern Host,
Header, Modul, Prefix und Connector gemeinsam aus derselben vorbereiteten
Quelle bauen. Bei fehlender Shared Library nur den bewussten Stagingpfad und
`LD_LIBRARY_PATH` prüfen, nicht global Dateien kopieren.

### Paketweg

Vor Installation Release-Verfügbarkeit erneut abfragen. Bei fehlenden v3-
Headern oder pkg-config-Metadaten den Source-Build verwenden. Eine nicht
lesbare Konfiguration, falsche Dateiberechtigung oder ein belegter Port ist
kein Paketbeweis. Ein Paket-Host mit nicht passender ABI darf nicht mit einem
Source-Modul kombiniert werden.

## Variablen und Platzhalter

| Variable/Platzhalter | Pflicht | Standard | Beispiel | Bedeutung |
| --- | --- | --- | --- | --- |
| VERIFIED_RUN_PARENT | ja | vom Makefile gewählt, wenn nicht gesetzt | $HOME/modsecurity-connector-work | Beschreibbarer externer Stamm für Build, Cache, Runtime, Logs und Evidence; außerhalb des Checkouts und ohne Secrets im Namen. |
| VERIFIED_RUN_ROOT | nein | unter VERIFIED_RUN_PARENT abgeleitet | $HOME/modsecurity-connector-work/ModSecurity-conector-verified | Run-gebundener externer Stamm; enthält abgeleitete Build-, Run-, Log- und Evidence-Pfade. |
| BUILD_ROOT | nein | unter dem verifizierten Run abgeleitet | externes Build-Unterverzeichnis | Staging- und Buildausgabe; nicht in den Git-Checkout legen. |
| CACHE_ROOT | nein | als Cache-v2 unter dem verifizierten Run abgeleitet | externes Cache-v2-Unterverzeichnis | Wiederverwendbare Eingaben; kein PASS und keine kanonische Evidence. |
| NO_CRS_RUN_ID | für Full Lifecycle | leer | nginx-core-20260712T120000Z | Dateisicherer Name eines Evidence-Runs; denselben Wert für Full Lifecycle und Evidence-Check verwenden. |
| CC | nein | Toolchain-Default | gcc | C-Compiler für C- und CGo-nahe Buildschritte. |
| CXX | nein | Toolchain-Default | g++ | C++-Compiler für Abhängigkeiten, die ihn benötigen. |
| CFLAGS | nein | Toolchain-Default | -O2 -g | Zusätzliche C-Flags; Beispiel ist Entwicklungswert, kein Repository- oder Produktionsdefault. |
| CXXFLAGS | nein | Toolchain-Default | -O2 -g | Zusätzliche C++-Flags; kein Produktionsprofil. |
| CPPFLAGS | nein | leer oder Toolchain-Default | -I/opt/modsecurity-connector/include | Zusätzliche Include-Flags für bewusst gewählte Headerpfade. |
| LDFLAGS | nein | leer oder Toolchain-Default | -L/opt/modsecurity-connector/lib | Zusätzliche Linkerflags für bewusst gewählte Bibliothekspfade. |
| PKG_CONFIG_PATH | nein | Paketmanager-/Toolchain-Default | /opt/modsecurity-connector/lib/pkgconfig | Zusätzlicher Suchpfad für pkg-config-Metadaten; kein ABI-Ersatz. |
| LD_LIBRARY_PATH | nein | Loader-Default | /opt/modsecurity-connector/lib | Temporärer Suchpfad für Shared Libraries; keine globale Installation. |
| MAKE_JOBS | nein | vom Framework ermittelt | 2 | Anzahl paralleler Compilerprozesse; bei wenig RAM kleiner wählen. |
| HOME | nein | Anmeldeverzeichnis | $HOME | Shellwert für das Benutzerverzeichnis; keine lokale Entwicklerpfadangabe. |
| jobs | nein | nicht gesetzt | 2 | Lokale Shellvariable aus `getconf`, die an `MAKE_JOBS` übergeben wird. |
| run_id | nein | nicht gesetzt | apache-core-20260712T120000Z | Lokale Shellvariable, aus der `NO_CRS_RUN_ID` gesetzt wird. |
| TRAEFIK_BIN | nein | generated external cache binary | verified external Traefik binary | Aufgelöstes gepinntes Traefik-Hostbinary. |
| TRAEFIK_NATIVE_RUNTIME_ROOT | nein | derived under BUILD_ROOT | external native runtime directory | Invocationslokale Native-Middleware-Dateien. |
| TRAEFIK_CONNECTOR_CONFIG | nein | connector configuration file | connector configuration file | Repository-Connectorkonfiguration. |
| TRAEFIK_ENGINE_SERVICE_BIN | nein | derived external executable | external engine-service executable | Repository-gebauter privater UDS-Engine-Service. |
| MSCONNECTOR_RULES_FILE | nein | unset | absolute no-CRS rules file | Kanonische Regeleingabe für die ausgewählte native Runtime, wenn der Dispatcher sie exportiert. |
| TRAEFIK_ENGINE_SERVICE_CFLAGS | nein | unset | -O2 -g | Optionale C-Flags nur für den C/C++-Engine-Service-Build. |
| TRAEFIK_ENGINE_SERVICE_LDFLAGS | nein | unset | -L/opt/modsecurity-connector/lib | Optionale Linkerflags nur für den Engine-Service. |

| Dokumentierter Wert | Beispiel | Bedeutung |
| --- | --- | --- |
| Connectorname | traefik | Make- und Evidence-Name dieses Guides; kein Platzhalter in den gezeigten Befehlen. |
| Source-Verzeichnis | unter `$BUILD_ROOT` oder vorbereiteter Provenienz | Vom unterstützten Vorbereiter erzeugte Quelle; keinen zweiten Hand-Checkout als Ersatz verwenden. |
| Build-Verzeichnis | `$BUILD_ROOT/stages/traefik` | Staging- und Stufenergebnisse außerhalb des Checkouts. |
| Installationsprefix | externes Staging unter `VERIFIED_RUN_PARENT` | Bevorzugter Entwicklungsort statt systemweiter Installation. |
| Rules-Datei | vom Full-Lifecycle-Dispatcher | Kanonische Regeldatei wird vom ausgewählten Lauf geliefert; keine lokale Datei als gleichwertig ausgeben. |
| Modul-/Hostbinary | von Vorbereitung oder Source-Build aufgelöst | Pfad, Header und ABI gehören zum selben ausgewählten Host. |

## Einschränkungen und nicht erhobene Claims

Die Anweisungen beschreiben reproduzierbare Entwicklungs-, Test- und
Buildwege. Sie sind keine Bewertung als produktionsreifes Paket oder gehärtete
Deployment-Anleitung. Sie behaupten keine vollständige CRS-Abdeckung,
keine vollständige Protokoll- oder Plattformmatrix und keine über den
dokumentierten Run hinausgehende Sicherheitseigenschaft. Ein Paketweg ist nur
dann gleichwertig, wenn der ausgewählte Host-, Modul-, Middleware-, Service-
oder Patchpfad tatsächlich durch den dokumentierten Full Lifecycle ausgeführt
und geprüft wurde.
