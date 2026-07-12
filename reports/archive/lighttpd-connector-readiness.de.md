> Status: Historisch
> Ersetzt durch: [../current/six-connector-core-completion.de.md](../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Einsatzreife des lighttpd-Connectors

**Sprache:** [English](lighttpd-connector-readiness.md) | Deutsch

> **Hinweis zum Evidence-Umfang.** Dies ist ein historischer lokaler Snapshot
> eines `minimal_runtime_smoke` vom 10.07.2026, kein kanonisches
> No-CRS-Ergebnis. Er darf weder den aktuellen generierten
> [lighttpd-No-CRS-Snapshot](../evidence/lighttpd-no-crs-baseline.de.md) noch die
> [kanonische Capability-Matrix](../testing/generated/canonical/connector-capabilities.generated.de.md)
> übersteuern. Nur ein kanonisches `result.json` kann den aktuellen
> No-CRS-Status heraufstufen; die lokale Smoke-Evidence unten bleibt bewusst
> enger.

Belegstand: 10.07.2026

## Ergebnis

Der lighttpd-Connector hat den Status `minimal_runtime_smoke`, begrenzt auf
einen lokalen, gezielten Anfragekopfpfad durch das native Modul. Ein echter
lighttpd-1.4.84-Prozess lud `mod_msconnector.so`; die unveränderte Anfrage
`OPTIONS *` lieferte HTTP 200, und derselbe Host-Pfad mit
`X-Modsec-Smoke: block` lieferte HTTP 403 aus der libmodsecurity-Regel `1000001`
über den Common-Entscheidungspfad.

Das native Modul unterstützt bewusst weder Anfrage- noch Antwortkörper. Der
Nachweis umfasst kein Antwortverhalten über den implementierten Kopf-Rückruf
hinaus, kein CRS, keine breite Testmatrix, keine Sicherheitsprüfung und keinen
betrieblichen Einsatz.

## Architektur und Host-Integration

Die primäre Integration ist ein repository-eigenes natives lighttpd-Modul,
nicht der ältere Brücken-Starter oder der alternative Framework-Dienstpfad.

- `connectors/lighttpd/module/mod_msconnector.c` implementiert
  Plugin-Initialisierung, serverweite Konfiguration, Anfragelebenszyklus und
  Aufräumen.
- `handle_uri_clean` bildet Anfragemetadaten und -köpfe ab, beginnt die
  Common-Transaktion, verarbeitet die Anfragephase und überträgt eine disruptive
  Entscheidung mit `http_status_set_err()`.
- `handle_response_start` bildet Antwortmetadaten und -köpfe auf die
  Common-Antwort-API ab; der gezielte Laufzeittest prüft keine
  antwortspezifische Regel oder Intervention.
- `handle_request_reset` beendet und zerstört die Transaktion und gibt die vom
  Connector besessenen abgebildeten Felder frei.
- `connectors/lighttpd/src/lighttpd_modsecurity_mapper.c` verwaltet die
  hostspezifische Abbildung und hält lighttpd-Typen außerhalb von `common/`.

## Common-SDK-Anbindung

Das Modul initialisiert Konfiguration über
`msconnector_generic_config_init()`, ruft die generischen Common-Mapper für
Anfrage und Antwort auf und verwendet Common-Laufzeit-APIs für Regelladen,
Transaktionszustand und -IDs, Grenzen, Entscheidungen, Interventionen,
Ablauf-/Integritätsmetadaten, Ereignisse und JSONL-Serialisierung. Die
Kopf-Felder bleiben während der Transaktion Eigentum des Connectors.

Die Repository-Prüfungen waren erfolgreich:

```sh
make check-lighttpd-common-adoption
make check-remaining-connectors-host-integration
```

## Konfiguration

Die lighttpd-Hostkonfiguration registriert `msconnector.enabled` und
`msconnector.config-file`. Die referenzierte Common-Datei im Format
`key=value` bildet Regeldatei, Kopf für die Transaktions-ID, Körperrichtlinien
und -grenzen, Blockierungs- und Fehlerstatus, Ereignispfad sowie Grenzen für
Köpfe und Ereignisse ab.

Das native Modul verlangt für beide Körpermodi `none`. Eine negative
Konfigurationsprüfung bestätigte, dass `request_body_mode=buffered` beim Laden
des Moduls abgelehnt wird. Die numerischen Körpergrenzen sind Einstellungen des
Parsers und Ressourcenschutzes, keine Fähigkeit zur Körperverarbeitung.
Eingebettete Regeln, entfernte Regeln, Inhaltstyp-Richtlinien und breitere
Direktivenkombinationen wurden nicht ausgeführt.

## Belege für Bauvorgang, Konfiguration, Start und Laufzeit

| Stufe | Reproduktionsbefehl | Beobachteter Nachweis | Grenze |
|---|---|---|---|
| Bauvorgang | `make build-lighttpd-connector` | C17-PIC-Kompilierung mit `-Wall -Wextra -Werror`; natives dynamisch ladbares Modul gegen lokale libmodsecurity mit lokalem `RUNPATH` gelinkt | Nur Kompilierung und Linken; kein impliziter Selbsttest |
| Konfiguration | `make check-lighttpd-config` | Echtes lighttpd lud mit `-tt` `mod_msconnector.so`, akzeptierte Host-/Common-Konfiguration, initialisierte libmodsecurity und lud die gezielte Regel | Startet keinen Anfrageverkehr |
| Start | `make start-smoke-lighttpd` | Echter Vordergrundprozess blieb aktiv und wurde beendet; Ausgabe enthält `requests=0` | Nur Prozesslebenszyklus |
| Laufzeit | `make runtime-smoke-lighttpd` | Echter lighttpd-/Modulpfad lieferte unverändert 200 und regelgestützt 403; erwartetes Ereignis gefunden; Prozess beendet | Nur zwei gezielte `OPTIONS *`-Fälle mit Anfrageköpfen |

Auch die vier übergeordneten Ziele waren gemeinsam erfolgreich:

```sh
make build-lighttpd-connector check-lighttpd-config \
  start-smoke-lighttpd runtime-smoke-lighttpd
```

Die beobachteten lokalen Artefakte liegen außerhalb des Checkouts:

- Natives Modul:
  `<verified-run-root>/build/lighttpd-connector/modules/mod_msconnector.so`
- Bauinventar:
  `<verified-run-root>/build/lighttpd-connector/build-info.txt`
- Erzeugte Testkonfiguration und Protokolle:
  `<verified-run-root>/build/lighttpd-connector/smoke/`
- Laufzeitereignis:
  `<verified-run-root>/build/lighttpd-connector/smoke/events.jsonl`

Das Laufzeitereignis nennt Connector `lighttpd`, die Anfragekopfphase, Regel
`1000001` und HTTP 403 und enthält kein Nutzdatenfeld aus Anfrage- oder
Antwortkörpern. Diese lokalen Artefakte sind kein aufbewahrter,
plattformübergreifender CI-Lauf.

Die historischen Ziele `build-lighttpd-bridge` und
`self-test-lighttpd-bridge` sind getrennt. Das native Bauziel führt keinen dieser
Selbsttests aus, und das Ergebnis des Brücken-Selbsttests zählt nicht als
Laufzeitnachweis des nativen Host-Pfads.

## Bekannte Grenzen und verbleibende technische Lücken

- Erfassung des Anfragekörpers, Phase 2, Abschneidungsverhalten und Verarbeitung
  nach Inhaltstyp werden nicht unterstützt.
- Erfassung des Antwortkörpers, Phase 4 und späte Intervention werden nicht
  unterstützt.
- Der Antwortkopf-Rückruf ist implementiert und wird geladen; der gezielte
  Laufzeittest prüft jedoch weder die Abbildung von Antwortköpfen noch eine
  Entscheidung in der Antwortphase.
- Umleitung, Verbindungsabbruch, Paralleltests mit mehreren Arbeitern oder
  Threads, Langzeitstabilität und Leistung sind offen.
- Es erfolgten weder eine CRS-Ausführung noch eine vollständige Matrix mit oder
  ohne CRS, eine Sicherheitsprüfung oder eine betriebliche Härtung.
- Der Nachweis gilt für eine lokale lighttpd-Version und eine gezielte Regel.

## Durch die Belege gestützte Aussagen

- Es gibt ein echtes repository-eigenes natives lighttpd-Modul, das das Common
  SDK und die Common-Laufzeit verwendet.
- Das native Modul lässt sich lokal bauen, linken und in echtem lighttpd 1.4.84
  laden.
- Konfigurationsprüfung sowie anfragefreier Start und Stopp von echtem lighttpd
  sind erfolgreich.
- Der gezielte Anfragekopfpfad hat `minimal_runtime_smoke`-Belege für
  unverändertes HTTP 200, regelgestütztes HTTP 403 und ein reines
  Metadatenereignis.
- Nativer Bauvorgang, Brücken-Selbsttest, Starttest und Laufzeittest sind getrennte
  Belegstufen.

## Bewusst nicht erhobene Claims

- Produktionsreife oder Produktionshärtung
- sichere Laufzeit oder bestätigte Sicherheit
- CRS-Bestätigung oder CRS-Vollständigkeit
- Bestätigung einer vollständigen Testmatrix
- Bestätigung von Anfragekörpern, Antwortköpfen oder Antwortkörpern
- breite Kompatibilität mit lighttpd-Versionen oder Plattformen
- Bestätigung aller Connectoren
