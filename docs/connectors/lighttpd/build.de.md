<!-- Generated from scripts/generate_connector_guides.py; do not edit directly. -->

# lighttpd-Build

**Sprache:** [English](build.md) | Deutsch

## Geltungsbereich

Dieser Leitfaden beschreibt den aktuellen ausgewählten HTTP/1.1-P1–P4-Kern. Er behauptet keine Produktionsreife, vollständige CRS-, HTTP/2- oder HTTP/3-Verifikation und keine Strict-Verifikation für alle Connectoren.

## Buildpfad und Hostversion

`make build-lighttpd` bereitet den gepatchten ausgewählten Host vor; `make check-config-lighttpd` prüft dessen Konfiguration.

Die maßgebliche Hostversion ist die Version der aktuellen vorbereiteten Runtime oder ihres gepinnten Provisionierungsinputs. Eine dokumentierte Version ist keine Aussage über jede Distribution, ABI oder Betriebsumgebung.

## Toolchain und Abhängigkeiten

Benötigt werden der zum Host passende C/C++- bzw. Go-Toolchainpfad, libmodsecurity-Abhängigkeiten und ein beschreibbarer Build-/Cache-Root außerhalb des Checkouts. Compiler, Flags und Hostrevisionen werden als Build-Provenance festgehalten; dieser Leitfaden behauptet keine universelle Compiler- oder Go-Version.

## Cache-v2 und Provenienz

Die Wiederverwendung von Cache-v2 ist identitätsgebunden. Source-URL, Revision oder Digest, Patchset, Architektur, Compiler und Konfiguration bestimmen, ob ein Cache-Eintrag wiederverwendbar ist. Ein Cache-Treffer ist kein Runtime-PASS.

## Build, Config und Runtime

Führen Sie `make build-lighttpd` und danach `make check-config-lighttpd` aus. Start- und Runtime-Smokes existieren nur für die jeweils angebotenen Targetfamilien; der ausgewählte Kernlauf ist `make full-lifecycle-lighttpd`. Erfolgreicher Build oder Config-Check ist kein Rule-Engine-PASS.

## Optionale Profile und Fehlerdiagnose

Kompatibilitäts-, CRS-, erweitertes Matrix-, H2/H3- und Strict-Profile sind getrennt vom ausgewählten Kern. Prüfen Sie bei Fehlern Executable-Pfade, ABI, Modul-/Service-Load, beschreibbare Runtime-Roots sowie gepinnte Source-/Patch-Eingaben, bevor Sie Konfiguration ändern.

## Konfigurationsvariablen und Platzhalter

Die Tabelle enthält nur vorhandene Eingaben oder generierte Pfade. Ein Beispielwert ist kein stiller Default; Details zu Pflicht, Scope, Auswirkung und Sicherheit stehen in der zentralen Referenz.

| Name | Pflicht | Format | Gesetzt durch | Beispielwert |
| --- | --- | --- | --- | --- |
| `LIGHTTPD_SOURCE_URL` | Optional | HTTPS source archive URL | Provisioning/caller | `pinned source URL` |
| `LIGHTTPD_BUILD_ROOT` | Optional | absolute build directory | Provisioning | `<build-root>/lighttpd` |
| `LIGHTTPD_CONFIG` | Generated | absolute host configuration path | Harness | `<build-root>/lighttpd.conf` |
| `NO_CRS_RULES_FILE` | Required for canonical rule runs | absolute rules-file path | Make default or caller | `/etc/modsecurity/no-crs-baseline.conf` |

Siehe die [zentrale Variablenreferenz](../../configuration/variables.de.md).
