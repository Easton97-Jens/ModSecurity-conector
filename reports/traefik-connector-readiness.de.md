# Einsatzreife des Traefik-Connectors

**Sprache:** [English](traefik-connector-readiness.md) | Deutsch

> **Hinweis zum Evidence-Umfang.** Dies ist ein historischer lokaler Snapshot
> eines `minimal_runtime_smoke` vom 10.07.2026, kein kanonisches
> No-CRS-Ergebnis. Er darf weder den aktuellen generierten
> [Traefik-No-CRS-Snapshot](traefik-no-crs-baseline.de.md) noch die
> [kanonische Capability-Matrix](testing/generated/canonical/connector-capabilities.generated.de.md)
> übersteuern. Nur ein kanonisches `result.json` kann den aktuellen
> No-CRS-Status heraufstufen; die lokale Smoke-Evidence unten bleibt bewusst
> enger.

Belegstand: 10.07.2026

## Ergebnis

Der Traefik-Connector hat den Status `minimal_runtime_smoke`, begrenzt auf einen
lokalen, gezielten HTTP-`forwardAuth`-Pfad für Anfrageköpfe. Ein echter
Traefik-3.7.5-Prozess leitete eine erlaubte Anfrage durch den repository-eigenen
Dienst; der nachgelagerte Dienst lieferte HTTP 200. Eine Anfrage mit
`X-Modsec-Smoke: block` wurde durch die libmodsecurity-Regel `1000001` über den
Common-Entscheidungspfad mit HTTP 403 abgewiesen.

Dieser Nachweis umfasst keine Anfragekörper, keine Prüfung der Antwort des
nachgelagerten Dienstes, kein CRS, keine breite Testmatrix, keine
Sicherheitsprüfung und keinen betrieblichen Einsatz.

## Architektur und Host-Integration

Das gewählte Host-Modell ist ein externer HTTP-`forwardAuth`-Dienst. Es handelt
sich weder um ein Traefik-Go-Plugin noch um ein Middleware-Modul oder eine
cgo-Brücke. Traefik ruft den Dienst auf, bevor eine erlaubte Anfrage an den
nachgelagerten Dienst weitergeleitet wird.

- `connectors/traefik/src/traefik_forwardauth_service_main.c` definiert das
  Hostprofil, die bevorzugten Köpfe für die ursprüngliche URI, die
  Mapper-Rückrufe und den Diensteinstieg.
- `connectors/traefik/src/traefik_modsecurity_mapper.c` enthält dünne
  C17-Funktionen, die an die generischen Common-Mapper für Konfiguration,
  Anfrage und Antwort delegieren.
- `common/runtime/http_authorization_service.c` und
  `common/runtime/msconnector_runtime.c` verwalten den neutralen
  HTTP-Lebenszyklus, libmodsecurity-Transaktion, Entscheidung, Intervention und
  Ereignisse.
- Der Laufzeittest gibt nur `X-Modsec-Smoke` und `X-Request-Id` ausdrücklich an
  die Autorisierungsanfrage weiter.
- `forwardAuth` liefert eine Autorisierungsentscheidung, aber keine spätere
  Antwort des nachgelagerten Dienstes an den Connector. Der eingebundene
  Antwort-Mapper belegt keine Prüfung dieser Antwort.

## Common-SDK-Anbindung

Der aktive Connector-Pfad initialisiert Common-Konfiguration über
`msconnector_generic_config_init()`, bildet Anfragen über
`msconnector_generic_map_request()` ab und verwendet Common-Laufzeit-APIs für
Regelladen, Transaktions-IDs, Grenzen, Entscheidungen, Interventionen,
Metadatenereignisse und JSONL-Serialisierung. Traefik-spezifische Profile und
`File Provider`-Daten bleiben unter `connectors/traefik/`.

Die Repository-Prüfungen waren erfolgreich:

```sh
make check-traefik-common-adoption
make check-remaining-connectors-host-integration
```

## Konfiguration

`connectors/traefik/config/traefik-forwardauth.conf` bildet Aktivierung,
Regeldatei, Kopf für die Transaktions-ID, Körpermodi und -grenzen,
Standardstatus für Blockierung und Fehler, Ereignispfad sowie Ressourcenlimits
für Köpfe und Ereignisse auf die Common-Konfiguration ab.
`traefik-forwardauth-dynamic.yaml` stellt die echte `File Provider`-Verdrahtung
von `forwardAuth` und nachgelagertem Dienst für den Starttest bereit.

Die Common-Vorlage verwendet `request_body_mode=none`, weil der gewählte
`forwardAuth`-Pfad den ursprünglichen Anfragekörper nicht an den Dienst liefert.
Die numerische Anfragekörpergrenze von 4096 Byte bleibt eine Einstellung für
Parser und Ressourcenschutz, keine Host-Fähigkeit; das erzeugte Ergebnis setzt
`request_body_verified` ausdrücklich auf false. Der Antwortkörpermodus ist
ebenfalls `none`. Eingebettete Regeln, entfernte Regeln und breitere
Direktivenkombinationen wurden nicht ausgeführt.

## Belege für Bauvorgang, Konfiguration, Start und Laufzeit

| Stufe | Reproduktionsbefehl | Beobachteter Nachweis | Grenze |
|---|---|---|---|
| Bauvorgang | `make build-traefik-connector` | C17-Kompilierung mit `-Wall -Wextra -Werror`; Dienst gegen lokale libmodsecurity mit lokalem `RUNPATH` gelinkt | Nur Kompilierung und Linken; kein Dienstselbsttest und keine Anfrage |
| Konfiguration | `make check-traefik-config` | Gebauter Dienst akzeptierte die Common-Konfiguration mit `--check-config` | Startet Traefik nicht |
| Start | `make start-smoke-traefik` | Dienst und echtes Traefik blieben mit erzeugter `File Provider`-Konfiguration aktiv und wurden ohne Anfrage beendet | Nur Prozesslebenszyklus |
| Laufzeit | `make runtime-smoke-traefik` | Echter Pfad Traefik -> `forwardAuth` -> Common/libmodsecurity lieferte 200 und regelgestütztes 403; erwartetes Ereignis gefunden; Prozesse beendet | Nur zwei gezielte GET-Fälle mit Köpfen |

Die beobachteten lokalen Laufzeitbelege liegen außerhalb des Checkouts:

- Bauartefakt:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/traefik-forwardauth`
- Laufzeitergebnis:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/runtime-smoke/result.json`
- Laufzeitereignis:
  `/var/tmp/ModSecurity-conector-verified/build/traefik-connector/runtime-smoke/logs/events.jsonl`

Das Ergebnis enthält erlaubten Status 200, blockierten Status 403, den
Common-Laufzeitpfad, Regel `1000001` sowie false für Anfragekörper,
Antwortkörper, Verarbeitung der nachgelagerten Antwort, CRS-Vollständigkeit und
breite Matrixreife. Das Ereignis nennt die Transaktion
`traefik-forwardauth-block` und enthält kein Körpernutzdatenfeld. Diese lokalen
Artefakte sind kein aufbewahrter, plattformübergreifender CI-Lauf.

Fehlende lokale Programme werden als BLOCKED mit Rückgabecode 77 gemeldet. Sind
die Eingaben vorhanden, gelten Fehler bei Konfiguration, Start, Abbildung,
HTTP-Status oder Ereignis als Fehlschlag.

## Bekannte Grenzen und verbleibende technische Lücken

- Der gewählte echte `forwardAuth`-Pfad hat keinen Laufzeitnachweis für
  Anfragekörper.
- In diesem Modell vor der Anfrage kann der Connector Antwortköpfe,
  Antwortmetadaten oder Antwortkörper des nachgelagerten Dienstes nicht prüfen.
- Auf dem getesteten Pfad gibt es keine Antwortphase oder späte Intervention.
- Eingebettete oder entfernte Regelquellen, Inhaltstyp-Richtlinien,
  Abschneidungsfälle, Umleitungen, Verbindungsabbruch, Parallelität,
  Langzeitstabilität und Leistung sind offen.
- Es erfolgten weder eine CRS-Ausführung noch eine vollständige Matrix mit oder
  ohne CRS, eine Sicherheitsprüfung oder eine betriebliche Härtung.
- Der Nachweis gilt für eine lokale Traefik-Version und eine gezielte Regel.

## Durch die Belege gestützte Aussagen

- Es gibt einen echten repository-eigenen Traefik-`forwardAuth`-Pfad, der das
  Common SDK und die Common-Laufzeit verwendet.
- Der Connector-Dienst lässt sich gegen lokale libmodsecurity bauen und linken.
- Konfigurationsprüfung sowie anfragefreier Start und Stopp von Dienst und
  Traefik sind lokal erfolgreich.
- Der gezielte Anfragekopfpfad hat `minimal_runtime_smoke`-Belege für erlaubtes
  HTTP 200, regelgestütztes HTTP 403 und ein reines Metadatenereignis.

## Bewusst nicht erhobene Claims

- Produktionsreife oder Produktionshärtung
- sichere Laufzeit oder bestätigte Sicherheit
- CRS-Bestätigung oder CRS-Vollständigkeit
- Bestätigung einer vollständigen Testmatrix
- Bestätigung von Anfragekörpern, nachgelagerten Antworten oder Antwortkörpern
- breite Kompatibilität mit Traefik-Versionen oder Plattformen
- Bestätigung aller Connectoren
