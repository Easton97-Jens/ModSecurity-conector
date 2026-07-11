# Einsatzreife des Envoy-Connectors

**Sprache:** [English](envoy-connector-readiness.md) | Deutsch

> **Hinweis zum Evidence-Umfang.** Dies ist ein historischer lokaler Snapshot
> eines `minimal_runtime_smoke` vom 10.07.2026, kein kanonisches
> No-CRS-Ergebnis. Er darf weder den aktuellen generierten
> [Envoy-No-CRS-Snapshot](envoy-no-crs-baseline.de.md) noch die
> [kanonische Capability-Matrix](testing/generated/canonical/connector-capabilities.generated.de.md)
> übersteuern. Nur ein kanonisches `result.json` kann den aktuellen
> No-CRS-Status heraufstufen; die lokale Smoke-Evidence unten bleibt bewusst
> enger.

Belegstand: 10.07.2026

## Ergebnis

Der Envoy-Connector hat den Status `minimal_runtime_smoke`, begrenzt auf einen
lokalen, gezielten HTTP-`ext_authz`-Pfad für Anfrageköpfe. Ein echter
Envoy-1.38.2-Prozess leitete eine erlaubte Anfrage durch den
repository-eigenen Autorisierungsdienst und erhielt HTTP 200. Eine zweite
Anfrage mit `X-Modsec-Smoke: block` wurde durch die libmodsecurity-Regel
`1000001` über den Common-Entscheidungspfad mit HTTP 403 abgewiesen.

Dieser Nachweis umfasst weder die Prüfung von Anfragekörpern noch Antworten des
nachgelagerten Dienstes, CRS, eine breite Testmatrix, eine Sicherheitsprüfung
oder den betrieblichen Einsatz.

## Architektur und Host-Integration

Das gewählte Host-Modell ist ein repository-eigener externer
HTTP-Autorisierungsdienst für Envoys `ext_authz`-Filter. Es handelt sich nicht
um einen nativen Envoy-Filter. Der ältere Selbsttest `envoy_bridge` gehört nicht
zu diesem Nachweis.

- `connectors/envoy/src/envoy_ext_authz_service_main.c` definiert das
  Envoy-Hostprofil, die bevorzugten URI-Köpfe, die Mapper-Rückrufe und den
  Diensteinstieg.
- `connectors/envoy/src/envoy_modsecurity_mapper.c` enthält dünne C17-Funktionen,
  die an die generischen Common-Mapper für Konfiguration, Anfrage und Antwort
  delegieren.
- `common/runtime/http_authorization_service.c` verwaltet den
  connector-neutralen HTTP-Dienstlebenszyklus;
  `common/runtime/msconnector_runtime.c` verwaltet libmodsecurity-Transaktion,
  Entscheidung, Intervention und Ereignis.
- Die Laufzeit verwendet `x-request-id` für die angeforderte Transaktions-ID
  und überträgt eine disruptive Anfrageentscheidung auf den Status der
  Autorisierungsantwort.
- Das gewählte Protokoll kann weder Antwortköpfe noch Antwortkörper des
  nachgelagerten Dienstes sehen. Der eingebundene Antwort-Mapper belegt deshalb
  keinen Envoy-Antwortprüfungspfad.

## Common-SDK-Anbindung

Der aktive Connector-Pfad initialisiert `msconnector_config` über
`msconnector_generic_config_init()`, bildet Anfragen über
`msconnector_generic_map_request()` ab und verwendet Common-Laufzeit-APIs für
Regelladen, Transaktions-IDs, Ressourcenschutz, Entscheidungen, Interventionen,
Metadatenereignisse und JSONL-Serialisierung. Envoy-Typen und -Konfiguration
bleiben unter `connectors/envoy/`; `common/` enthält keinen Envoy-Hosttyp.

Die Repository-Prüfungen waren erfolgreich:

```sh
make check-envoy-common-adoption
make check-remaining-connectors-host-integration
```

## Konfiguration

`connectors/envoy/config/envoy-ext-authz.conf` bildet Aktivierung, Regeldatei,
Kopf für die Transaktions-ID, Körpermodi und -grenzen, Blockierungs- und
Fehlerstatus, Ereignispfad sowie Ressourcenlimits für Köpfe und Ereignisse auf
die Common-Konfiguration ab. Der Starter erzeugt außerhalb des Checkouts eine
konkrete Kopie und ersetzt nur die verwalteten Regel- und Ereignispfade.

Die Vorlage konfiguriert eine gepufferte Anfragekörpergrenze von 4096 Byte. Der
aktuelle Laufzeittest sendet jedoch körperlose GET-Anfragen. Diese Einstellung
ist eine konfigurierte Grenze und kein Laufzeitnachweis für Anfragekörper. Der
Antwortkörpermodus ist `none`. Eingebettete Regeln, entfernte Regeln und breitere
Direktivenkombinationen wurden mit diesem Belegsatz nicht ausgeführt.

## Belege für Bauvorgang, Konfiguration, Start und Laufzeit

| Stufe | Reproduktionsbefehl | Beobachteter Nachweis | Grenze |
|---|---|---|---|
| Bauvorgang | `make build-envoy-connector` | C17-Kompilierung mit `-Wall -Wextra -Werror`; Dienst gegen lokale libmodsecurity mit lokalem `RUNPATH` gelinkt | Nur Kompilierung und Linken; kein Prozess und keine Anfrage |
| Konfiguration | `make check-envoy-config` | Konkrete Common-Konfiguration akzeptiert und gezielte Regeln geladen | Startet Envoy nicht |
| Start | `make start-smoke-envoy` | Erzeugte Envoy-YAML validiert; Dienst und Envoy blieben aktiv; beide beendet; `requests_sent=no` | Nur Prozesslebenszyklus |
| Laufzeit | `make runtime-smoke-envoy` | Echter Pfad Envoy -> `ext_authz` -> Common/libmodsecurity lieferte 200 und regelgestütztes 403; Metadatenereignis gefunden; Prozesse beendet | Nur zwei gezielte Fälle mit Anfrageköpfen |

Die beobachteten lokalen Belege liegen außerhalb des Checkouts:

- Bauartefakt:
  `/var/tmp/ModSecurity-conector-verified/build/envoy-connector/msconnector_envoy_ext_authz`
- Startzusammenfassung:
  `/var/tmp/ModSecurity-conector-verified/build/envoy-connector/start-smoke/start-summary.txt`
- Laufzeitzusammenfassung:
  `/var/tmp/ModSecurity-conector-verified/build/envoy-connector/runtime-smoke/runtime-summary.txt`
- Laufzeitereignis:
  `/var/tmp/ModSecurity-conector-verified/build/envoy-connector/runtime-smoke/events.jsonl`

Das Laufzeitereignis nennt Connector `envoy`, Transaktion `envoy-block-1`, die
Anfragekopfphase, Regel `1000001` und HTTP 403. Es enthält Metadaten statt
Nutzdaten aus Anfrage- oder Antwortkörpern. Diese lokalen Artefakte sind
reproduzierbare Belege, aber kein aufbewahrter, plattformübergreifender CI-Lauf.

Fehlende lokale Voraussetzungen werden als BLOCKED mit Rückgabecode 77
gemeldet. Sind die benötigten Programme und Eingaben vorhanden, gelten Fehler
bei Konfiguration, Start, Abbildung, Status oder Ereignis als Fehlschlag und
nicht als übersprungene Prüfung.

## Bekannte Grenzen und verbleibende technische Lücken

- Es wurde keine Anfrage mit Körper durch Envoy und den Connector getestet.
- Antwortköpfe, Antwortmetadaten und Antwortkörper des nachgelagerten Dienstes
  stehen diesem `ext_authz`-Dienst nicht zur Verfügung.
- Antwortphasen und späte Interventionen wurden nicht getestet.
- Eingebettete oder entfernte Regelquellen, Inhaltstyp-Richtlinien,
  Abschneidungsfälle, Umleitungen, Verbindungsabbruch, Parallelität,
  Langzeitstabilität und Leistung sind offen.
- Es erfolgten weder eine CRS-Ausführung noch eine vollständige Matrix mit oder
  ohne CRS, eine Sicherheitsprüfung oder eine betriebliche Härtung.
- Der Nachweis gilt für eine lokale Envoy-Version und eine gezielte Regel.

## Durch die Belege gestützte Aussagen

- Es gibt einen echten repository-eigenen Envoy-`ext_authz`-Host-Pfad, der das
  Common SDK und die Common-Laufzeit verwendet.
- Der Connector lässt sich in der verwalteten Umgebung gegen lokale
  libmodsecurity bauen und linken.
- Konfigurationsprüfung sowie anfragefreier Start und Stopp von echtem Envoy
  sind lokal erfolgreich.
- Der gezielte Anfragekopfpfad hat `minimal_runtime_smoke`-Belege für erlaubtes
  HTTP 200, regelgestütztes HTTP 403 und ein reines Metadatenereignis.

## Bewusst nicht erhobene Claims

- Produktionsreife oder Produktionshärtung
- sichere Laufzeit oder bestätigte Sicherheit
- CRS-Bestätigung oder CRS-Vollständigkeit
- Bestätigung einer vollständigen Testmatrix
- Bestätigung von Anfragekörpern, Antwortköpfen oder Antwortkörpern
- breite Kompatibilität mit Envoy-Versionen oder Plattformen
- Bestätigung aller Connectoren
