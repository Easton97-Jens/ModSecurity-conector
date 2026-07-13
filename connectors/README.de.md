# Connector-Implementierungen

**Sprache:** [English](README.md) | Deutsch

## Zweck und Evidence-Grenze

Dieses Verzeichnis enthält die repository-eigenen Integrationsschichten für
Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd. Jeder Connector-Baum
verbindet host-spezifischen Code, Metadaten, Harness-Wiring und lokale
Design-Notizen mit den connector-neutralen Schnittstellen in
[Common](../common/README.de.md).

Die Bäume beschreiben Implementierung und deklarierte Capabilities; sie
ersetzen keinen Lauf. Aktuelle Ergebnisse der ausgewählten HTTP/1.1-Kernroute
gehören zur laufbezogenen Evidence und zu den [aktuellen
Reports](../reports/current/). Leiten Sie aus Source-Baum oder erfolgreichem
Build weder Production Readiness, vollständige CRS-Coverage,
HTTP/2-/HTTP/3-Verifikation noch Strict-Verifikation für alle Connectoren ab.

## Struktur und Source of Truth

| Pfad | Zweck | Source of Truth / Wartungsregel |
| --- | --- | --- |
| `_template/` | Scaffold für einen neuen Connector | Nur beim Beginn eines neuen Connectors kopieren; der Template-Baum macht keinen Implementierungs- oder Runtime-Claim. |
| `<connector>/` | Eine Host-Integration | `<connector>` ist ein Dokumentationsplatzhalter für genau `apache`, `nginx`, `haproxy`, `envoy`, `traefik` oder `lighttpd`; beispielsweise `connectors/nginx/`. |
| `<connector>/src/` | Host-spezifischer Source und Adapter | Der eingecheckte Source samt zugehörigen Headern definiert die Implementierung. Host-SDK-Nutzung gehört hierher, nicht nach `common/`. |
| `<connector>/harness/` | Connector-lokales Start- und Beobachtungs-Wiring | Der Harness zusammen mit dem aufrufenden Root-Target definiert den ausführbaren Integrationsvertrag. |
| `<connector>/capabilities.json` und `metadata.*` | Deklarierte Capability und Connector-Metadaten | Diese maschinenlesbaren Dateien sind maßgebliche Deklarationen, aber keine Promotion-Evidence. |
| `<connector>/ORIGIN.md` und `SOURCE_MAP.json` | Herkunft, Lizenz und Import-Provenance | Bei jeder Änderung importierten oder abgeleiteten Materials aktualisieren. |
| `<connector>/README.*`, `ORIGIN.md` und `TODO.md` | Code-nahe Source-, Provenance- und Arbeitsverfolgungsnotizen | Leserorientierte Architektur-, Konfigurations-, Lifecycle-, Einschränkungs- und Validierungs-Guides in [docs/connectors](../docs/connectors/README.de.md) halten. |

Das Root-[Makefile](../Makefile) ist maßgeblich für Target-Namen und Defaults.
Das Framework-Submodule besitzt den wiederverwendbaren Case-Katalog und die
Runner-Schemas. Der connector-spezifische Dokumentationsindex erklärt die
aktuelle unterstützte Route; der Evidence-Index erklärt, welche generierten
Artefakte einen Claim stützen können.

## Einen Connector hinzufügen oder ändern

Beginnen Sie mit `_template/`, erstellen Sie danach
`connectors/<connector>/` mit den dort aufgelisteten Dateien. Ersetzen Sie
`<connector>` nur durch einen der sechs oben genannten Namen; der Text ist kein
literaler Verzeichnisname. Host-spezifischer Source gehört nach `src/`,
Harness-Code nach `harness/`, Herkunfts- und Metadatenänderungen neben den
Source. Einen aktuellen Nutzer-Guide unter
`docs/connectors/<connector>.md` samt deutschem Partner anlegen; bei einem
generierten Guide wird der Generator aktualisiert.

Legen Sie keine ausführbaren Katalog-Cases unter einem Connector-Baum ab:
wiederverwendbare Cases, Normalizer und Runner sind Framework-owned. Speichern
Sie dort keine Build-Verzeichnisse, Download-Caches, Logs, Result-JSON,
Credentials, privaten Schlüssel oder kanonische Evidence. Connector-spezifischer
Server-/Proxy-SDK-Code gehört nicht nach `common/`.

## Variablen und Dokumentationsplatzhalter

Die folgenden Werte sind Eingaben für Root-Targets, keine Werte, die eine
Connector-Source-Datei stillschweigend liest. Die vollständige Vereinbarung
steht in der zentralen [Variablen- und Platzhalterreferenz](../docs/reference/variables.de.md)
und im [Glossar](../docs/reference/glossary.de.md).

| Name | Lokale Bedeutung | Pflicht, Format und Beispiel |
| --- | --- | --- |
| `FRAMEWORK_ROOT` | Ort des Framework-Submodules für delegierte Targets | Für Targets erforderlich, die an das Framework delegieren. Der Repository-Default ist `modules/ModSecurity-test-Framework`; einen vorhandenen vertrauenswürdigen Checkout wie `/srv/src/ModSecurity-test-Framework` nur bewusst als Override verwenden. Kein Build- oder Evidence-Pfad. |
| `BUILD_ROOT` | Elternpfad für generierte Build- und Runtime-Arbeit | Optional. Das Root-Makefile leitet ihn unterhalb seines Verified-Run-Roots ab; ein Override muss ein absolutes beschreibbares Verzeichnis außerhalb des Checkouts sein, etwa `/srv/modsecurity-work/build`. Ein falscher Pfad kann zu `BLOCKED` oder Exit `77` führen. |
| `NO_CRS_RUN_ID` | Kennung, die einen aggregierten No-CRS-Evidence-Lauf zusammenfasst | Für aggregierte Evidence-Kommandos erforderlich. Kein Default; dateisystemsicheres Token wie `six-core-20260712T120000Z`. Niemals Secrets, Benutzernamen oder Tickettext verwenden. |
| `<repository-root>` | Reiner Dokumentationsplatzhalter für den absoluten Root dieses Checkouts | Enthält `Makefile` und `docs/`; wenn ein Kommando ihn ausdrücklich verlangt, einen realen Pfad wie `/srv/src/ModSecurity-conector` verwenden. Winkelklammern nicht in ein Kommando kopieren. |
| `<external-source-root>` | Reiner Dokumentationsplatzhalter für einen vertrauenswürdigen Source-Checkout außerhalb dieses Repositorys | Optional, soweit ein Kommando nichts anderes verlangt; `/srv/src/ModSecurity-test-Framework` ist ein Beispiel. Weder Cache-/Output-Ort noch Evidence, dass der externe Checkout bestanden hat. |

Keiner dieser Werte ist ein Secret. Credentials und privates Material bleiben
aus Connector-Konfiguration, Kommandozeilen, Logs und Evidence heraus.

## Relevante Targets

Verwenden Sie im Target einen literalen Connector-Namen. So ist
`make check-nginx-common-adoption` eine Instanz des dokumentierten Musters
`check-<connector>-common-adoption`; `<connector>` besitzt die sechs oben
genannten erlaubten Werte.

| Target | Zweck und Ergebnisgrenze |
| --- | --- |
| `make check-<connector>-common-adoption` | Prüft die Verwendung der Common-Contracts eines Connectors. Es ist ein Strukturcheck, kein Host-Runtime-Nachweis. |
| `make build-<connector>` und `make check-config-<connector>` | Baut bzw. validiert die ausgewählte Connector-Konfiguration, soweit das Target existiert. Ein erfolgreicher Prozess-Exit erfüllt nur den Vertrag dieses Targets. |
| `make full-lifecycle-<connector>` | Führt das ausgewählte native HTTP/1.1-Kernprofil für einen Connector aus und schreibt laufbezogene Artefakte. |
| `make full-lifecycle-all-connectors` | Führt alle sechs ausgewählten Profile aus; für einen kanonischen aggregierten Kandidaten eine sichere `NO_CRS_RUN_ID` angeben. |
| `make check-six-connector-core-completion` | Validiert das Evidence-Gate für den ausgewählten Six-Connector-Core; erweitert weder Protokoll- noch Lifecycle-Grenze. |
| `make lint` | Führt Repository-Contracts, Dokumentationschecks und Syntaxchecks aus. Es erzeugt nicht selbst kanonische Runtime-Evidence. |

Details zu Compiler, Konfiguration, Testebene und Evidence stehen unter
[Build](../docs/build/README.de.md), [Testing](../docs/testing-and-evidence.de.md)
und [Evidence](../docs/testing-and-evidence.de.md).
