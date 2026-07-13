# Ursprung des lighttpd-Connectors

**Sprache:** [English](ORIGIN.md) | Deutsch

Status: repository-owned native module; stock `minimal_runtime_smoke` plus a
non-promoted patched-host full-lifecycle probe

In dieses Verzeichnis wurde keine Upstream-Connector-Implementierung
importiert. Das Modul, der Mapper, die Build-Skripte und das native Harness
sind repository-eigener Quellcode.

Die Host-ABI wird gegen den gepinnten lighttpd-1.4.84-Release-Quellcode und
sein generiertes `config.h` kompiliert. Das Test-Framework lädt und baut diesen
Release in einem verwalteten Component-Cache; der Upstream-Quellcode und die
generierten Header werden nicht in diesem Connector-Baum eingecheckt. Das
Modul verlinkt gegen eine lokal verwaltete libmodsecurity-Installation.

| Element | Wert |
| --- | --- |
| Connector-Quellcode | repository-eigene Dateien unter `connectors/lighttpd/` |
| Importierter Upstream-Connector-Quellcode | none |
| Host-Quellcode | lighttpd-1.4.84-Release-Tarball |
| Host-Quellcode-URL | `https://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-1.4.84.tar.xz` |
| Host-Commit | release tarball; no Git commit selected |
| Generierte Host-ABI-Eingabe | Datei `config.h` aus dem lighttpd-Build-Tree |
| Native Ausgabe | `mod_msconnector.so` |
| Runtime-Status | stock `minimal_runtime_smoke` plus a full-lifecycle-selected patched Phase-1 host probe |

Das Full-Lifecycle-Profil wählt `patched-native` über
`full-lifecycle-lighttpd-patched`. Dieses Target erstellt einen kopierten
1.4.84-Quellbaum, einen Out-of-Source-Core-Build, eine gestagte Binärdatei und
ein gestagtes ABI-passendes Modul unter dem verwalteten Build-Root. Es zeichnet
den lokalen Patch-SHA-256 sowie Binär-/Modul-Hashes vor einem echten
`lighttpd -tt`-Load auf. Dies ist weiterhin nur ein schmaler
Phase-1-Build-/Load-/Runtime-Pfad: Der Host-Smoke verwendet beide Body-Modi
als `none`. Der Response-Callback des Patches erhält einen geliehenen
HTTP/1.1-Identity-Entity-Range vor Transfer-Framing statt Socket-Wire-Output,
doch dieser Source-/Build-Vertrag bleibt ohne einen Streaming-Host-Run nicht
hochgestuft.

Der eingecheckte Connector-Quellcode kopiert weder lighttpd-
Implementierungscode noch Header. Öffentliche Host-API- und Build-Grenzen sind
im [kanonischen lighttpd-Leitfaden](../../docs/connectors/lighttpd.de.md)
zusammengefasst. Jeder künftige Source-Import muss diese Datei,
`SOURCE_MAP.json` und die repositoryweite Attribution aktualisieren, bevor ein
weitergehender Claim erhoben wird.
