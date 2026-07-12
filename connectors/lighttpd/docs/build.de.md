# lighttpd Build

**Sprache:** [English](build.md) | Deutsch


Status: Kompilierung/Link des nativen Moduls überprüft; Patched-Host-Ziel erstellt a
abgeglichener Lighttpd 1.4.84-Kern und -Modul unter einem isolierten Build-Root

## Eingaben

`build/build_module.sh` erfordert absolute Pfade:

- `LIGHTTPD_SOURCE_DIR`: angehefteter Lighttpd-Quellenstamm, der `src/plugin.h` enthält;
- `MODSECURITY_INCLUDE_DIR`: Präfix, das `modsecurity/modsecurity.h` enthält;
- `MODSECURITY_LIB_DIR`: Verzeichnis, das `libmodsecurity.so` enthält.

Die genaue Lighttpd-ABI-Version stammt aus einem generierten `config.h`. Das Drehbuch
sucht `LIGHTTPD_CONFIG_DIR`, `LIGHTTPD_BUILD_DIR`,
`LIGHTTPD_BUILD_ROOT` und der Quellbaum in dieser Reihenfolge. Es erfindet kein
`LIGHTTPD_VERSION_ID` aus einem Dateinamen.

Alle Artefakte werden außerhalb der Kasse unter einem absoluten `BUILD_ROOT` geschrieben.
Das Modul ist standardmäßig auf:

```text
$BUILD_ROOT/lighttpd-connector/modules/mod_msconnector.so
```

`LIGHTTPD_MODULE_DIR` kann ein anderes absolut verwaltetes Ausgabeverzeichnis auswählen.

## Nativer Build

```sh
make -C connectors/lighttpd build-lighttpd-connector
```

Das Skript kompiliert alle `common/src/*.c`,
`common/runtime/msconnector_runtime.c`, der Lighttpd-Mapper und das Modul as
PIC und verknüpft sie dann mit libmodsecurity in das gemeinsame Objekt. Erforderliches C
Zu den Flaggen gehören:

```text
-std=c17 -fPIC -Wall -Wextra -Werror
```

Die hostspezifischen Objekte nutzen zusätzlich die angehefteten Quellheader,
generiert `config.h` und `MSCONNECTOR_LIGHTTPD_HOST_API`. Ungelöster Lighttpd
Hostsymbole im gemeinsam genutzten Objekt sind beabsichtigt und werden bei lighttpd aufgelöst
lädt das Modul.

Der Build kann nur kompiliert/verlinkt werden. Das Ergebnis wird niemals geladen oder ausgeführt
Modul.

## Gepatchter 1.4.84-Kern und passendes Modul

Der Standardmodus bleibt der Standardmodus und wird weiterhin nur gegen einen kompiliert
unveränderter Lighttpd ABI:

```sh
make -C connectors/lighttpd build-lighttpd-connector
```

Das Repository enthält einen versionierten 1.4.84-Patch für einen lokalen Streaming-Hook
ABI. Der bereitgestellte Quellbaum wird niemals bearbeitet. `build-lighttpd-patched-core`
kopiert die Quelle nach `BUILD_ROOT/lighttpd-core-patched/lighttpd-1.4.84`,
zeichnet den Patch SHA-256 auf, konfiguriert einen Out-of-Source-Build, führt `make` aus und
`make install` und stellt die Binärdatei unter `stage/bin/lighttpd` bereit.

```sh
make -C connectors/lighttpd check-lighttpd-core-patch
make -C connectors/lighttpd apply-lighttpd-core-patch
make -C connectors/lighttpd build-lighttpd-patched-core
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
```

Der Matched-Host-Build ruft `build_module.sh` mit dem generierten `config.h` auf.
die kopierten gepatchten Header und dann `LIGHTTPD_MSCONNECTOR_CORE_MODE=patched`
Stufen `mod_msconnector.so` in `stage/modules`. Der Kern und der Wirt manifestieren sich
enthalten die Patch-SHA-256- und Binär-/Modul-SHA-256-Werte. Das Prüfziel
erfordert, dass die bereitgestellte Binärdatei 1.4.84 meldet, überprüft beide Hook-Symbole mit
`nm -D` und führt einen echten `lighttpd -tt`-Modulladevorgang aus dem isolierten Bereich durch
Modulverzeichnis.

Das ABI-Tag lehnt eine versehentliche Vermischung von Standard- und gepatchten dynamischen Modulen ab. Der Patch
macht geliehene HTTP/1.x-Anforderungsbereiche und Identitätsentitäts-Antwortbereiche verfügbar in
`http_chunk.c`, vor HTTP/1-Transfer-Framing und vor einem Socket-Schreibvorgang. Es
überprüft weder `connections.c` noch eine Verbindungswarteschlange. HTTP/2 ist bewusst
ausgeschlossen und gzip/br liegen außerhalb des ausgewählten Nur-Identitäts-Vertrags. Die
Das Full-Lifecycle-Profil wählt diesen gepatchten Host für eine isolierte Phase-1 aus
Laufzeitsonde. Es bleibt ein nicht hochgestufter Build-/Ladepfad und wird nicht eingerichtet
Für den Kunden sichtbarer Reaktionskörper, Phase-4- oder Spätinterventionsnachweise.

## Separate Vorgänge

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

- Bridge Build kompiliert nur die historische Bridge-Binärdatei.
- Der Bridge-Selbsttest führt diese Binärdatei explizit mit `--self-test` aus.
- Nativer Build kompiliert und verlinkt nur.
- Bei der Konfigurationsprüfung wird das echte `LIGHTTPD_BIN -tt` ausgeführt und das echte Modul geladen.
- Start Smoke startet und stoppt Lighttpd ohne Netzwerkanfragen.
- Runtime-Smoke allein sendet zwei echte Host-Anfragen.

`runtime-smoke-lighttpd-patched` ist ein separater, isolierter Phase-1-Smoke-Test
durch das Full-Lifecycle-Profil. Der eingecheckte Aufruf lädt nur die bereitgestellte Datei
gepatchtes Modul, verwendet `request_body_mode=none` und `response_body_mode=none`,
und prüft die Basislinie 200 plus die regelgestützte 403. Der Ersteller erlaubt Streaming
nur mit der gepatchten Entität ABI und `LIGHTTPD_PATCHED_ENTITY_ENCODING=identity`;
Das ist eine Vertragskonfiguration, kein P4-Laufzeitanspruch. Es ruft niemals das auf
generischer Bestand No-CRS Selected-Case-Consumer und seine PASS-Ausgabezustände
`phase4=not-executed`.

## Verifiziertes lokales Ergebnis

Unter Verwendung des vom Framework verwalteten Lighttpd 1.4.84-Builds und der lokalen libmodsecurity kann die
natives Modul kompiliert und verknüpft mit C17 und `-Werror`; Der Lader akzeptierte
sein ABI und seine Konfiguration. Dadurch werden Link-/Konfigurationsladenachweise für die erstellt
Nur angehefteter Build, keine Portabilität über beliebige Lighttpd-Releases hinweg.

## Nicht überprüfter Build-/Laufzeitbereich

Kein Build-Ergebnis legt die Verarbeitung des Körpers, die CRS-Vollständigkeit und die Produktion fest
Härtung, Sicherheitsüberprüfung oder vollständige Matrixkompatibilität. C23 und neuer
Standards können als optionale Repository-Kompilierungsspuren überprüft werden, aber C17 ist dies
erforderlicher Modulstandard.
