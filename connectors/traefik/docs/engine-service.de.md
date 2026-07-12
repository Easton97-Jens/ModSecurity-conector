# Persistenter lokaler Engine-Dienst

**Sprache:** [English](engine-service.md) | Deutsch

Dieses Verzeichnis enthält die persistente lokale Engine hinter der ausgewählten
Traefik Native-Middleware-Host-Probe. `traefik-engine-service` ist dauerhaft
Lokaler Unix-Domänen-Socket-Prozess, der eine Common/libmodsecurity-Laufzeit besitzt.
Es existiert, weil der ausgewählte lokale Traefik-Plugin-Pfad das Go ausführt
Middleware durch Yaegi; Es kann die C/C++-Libmodsecurity nicht direkt verknüpfen
Laufzeit.

`native_middleware/` wählt es nur aus, wenn `engineMode: uds` und ein privater
`engineSocketPath` werden vom isolierten Host-Harness versorgt. Die Standardeinstellung
Die Quellkonfiguration bleibt `passthrough`. Die fokussierten lokalen Tests sind es nicht
Traefik-Host-Beweis; Die separate Pinned-Host-Sonde zielt auf No-CRS-Beweise ab
bewirbt ausschließlich und niemals eingecheckte Funktionen, CRS-Unterstützung, Safe/Strict oder
Produktionsbereitschaft.

## Build und lokaler Protokolltest

Der Dienst muss mit einer expliziten lokal erstellten libmodsecurity verknüpft sein:

```sh
MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
make -C connectors/traefik build-engine-service

MODSECURITY_INCLUDE_DIR=/absolute/include \
MODSECURITY_LIB_DIR=/absolute/lib \
make -C connectors/traefik test-engine-service
```

`test-engine-service` erstellt den C17-Dienst, führt seinen Parser/Selbsttest aus und startet
ein echter lokaler Common/libmodsecurity-Dienstprozess und treibt beides sicher an
Transaktion und die gezielte Anforderungsheader-Verweigerungsregel des Repositorys gegenüber Unix
Steckdosen. Es lehnt auch einen übergroßen Teil und ein Ergebnis außerhalb des Staates ab
Anerkennung. Dies ist nur ein fokussierter Dienst-/Protokolltest; das tut es nicht
Starten Sie Traefik oder beweisen Sie eine Host-Aktion.

Der separate Real-Host-Probe erstellt den Dienst unter seiner isolierten Laufzeit
root, startet es einmal und wählt `engineMode: uds` im angehefteten Traefik-Lokal aus
Plugin. Wenn `MSCONNECTOR_RULES_FILE` festgelegt ist, wird genau dieser kanonische Wert geladen
Keine CRS-Regeldatei und erfordert die Regel-IDs `1100001`, `1100101`, `1100201` und
`1100301` für P1 bis P4. Das eingecheckte Zielgerät ist ein eigenständiges Gerät
Nur Fallback. Für die Host-Probe ist erforderlich, dass P1 `200` erlaubt, P1 `403` verweigert und P2 verweigert
`403`, P3 Pre-Commit Deny `403` und P4 Safe/Log-Only mit sichtbarem `200`; P4
strict ist explizit `NOT EXECUTED`.

Die Beispielkonfiguration ist
`config/traefik-engine-service.conf`. Sein Verwandter `rules_file` geht davon aus
Repository-Stammverzeichnis als Arbeitsverzeichnis. Bereitstellungen sollten eine vertrauenswürdige Version verwenden
absoluter Regelpfad und ein privates Laufzeitverzeichnis:

```sh
cd /absolute/ModSecurity-conector
/absolute/traefik-engine-service --check-config \
  --config connectors/traefik/config/traefik-engine-service.conf
/absolute/traefik-engine-service --serve \
  --config connectors/traefik/config/traefik-engine-service.conf \
  --socket /absolute/private-runtime/traefik-engine.sock
```

Der Daemon lehnt einen vorhandenen Socket-Pfad ab, bindet mit dem Modus `0600` und tut dies auch
Die Verknüpfung eines beliebigen, bereits vorhandenen Pfads kann nicht aufgehoben werden. Es serialisiert allgemeine Laufzeitaufrufe
hinter einem Mutex unter Beibehaltung des Transaktionsstatus pro Unix-Verbindung. Es ist
Prozess und Engine bleiben über Verbindungen hinweg bestehen; eine Verbindung stellt genau dar
eine Transaktion.

## Wire-Vertrag

`src/traefik_engine_protocol.h` ist die normative Protokolldeklaration. Rahmen
haben den folgenden 12-Byte-Big-Endian-Header:

| Bytes | Wert |
| --- | --- |
| 0--3 | ASCII `MSE1` |
| 4 | Protokollversion `1` |
| 5 | Opcode |
| 6--7 | null reservierte Flags |
| 8--11 | Nutzlastlänge |

Die maximale Nutzlast beträgt 65.536 Byte. Jeder rohe Anforderungs- oder Antwortblock ist
einzeln auf 32.768 Bytes begrenzt. Metadaten haben separate Obergrenzen: höchstens 128
Header, 256-Byte-Header-Namen, 8.192-Byte-Header-Werte, ein 4.096-Byte-URI,
und begrenzte IDs/Adressen. Eingebettete NUL-Bytes, nachgestellte Metadaten, ungültig
Frame-Flags, ungültige Reihenfolge und doppelte EOS-Vorgänge werden abgelehnt.

Der Client sendet diesen geordneten Lebenszyklus:

1. `BEGIN` überträgt begrenzte Anforderungsmetadaten und Header. Es ruft Common auf
   Verbindungs-/URI-/Request-Header-Verarbeitung und gibt die erste Entscheidung zurück.
2. Null oder mehr `REQUEST_CHUNK`-Frames, gefolgt von genau einmal
   `REQUEST_EOS`, hängen Sie den Anforderungstext an und beenden Sie ihn.
3. `RESPONSE_HEADERS`, null oder mehr `RESPONSE_CHUNK`-Frames und genau einer
   `RESPONSE_EOS` verarbeitet den Antwortlebenszyklus. `RESPONSE_COMMIT`-Datensätze
   die beiden Host-Metadaten-Booleans (`headers_sent`, `body_started`) sofort
   bevor oder nachdem der Host Bytes weiterleitet; Es puffert niemals Bytes.
4. `FINISH` ruft die allgemeine Protokollierung/Finalisierung erst nach dem erforderlichen EOS auf
   Anrufe (oder nach einer Terminal-Engine-Entscheidung).
5. `DESTROY` ist nach einem erfolgreichen `FINISH` erforderlich und gibt das Common frei
   Transaktion. EOF, fehlerhafte Eingaben oder ein Socket-Timeout zerstören ebenfalls eine
   In-Flight-Transaktion ohne Synthese eines Host-Ergebnisses.

`RESPONSE_HEADERS` ist `u16 status`, eine HTTP-Version mit begrenzter Länge und Präfix.
dann eine begrenzte Header-Liste. `BEGIN` verwendet die Methode mit Längenpräfix, URI und HTTP
Version, Hostname, Client-Adresse/Port, Server-Adresse/Port, Host-Anfrage-ID,
und Header in der genauen Reihenfolge, die im Header dokumentiert ist.

Jeder Befehl erhält einen `RESULT`-Frame. Seine Nutzlast beginnt mit Befehl, Ergebnis
Code, angeforderte Entscheidungsaktion, Phase, HTTP-Status und Lebenszyklus-Flags;
Es dürfen nur eine begrenzte Transaktions-ID, Regel-ID und Weiterleitungs-URL folgen. Es nie
Enthält Anforderungs-/Antworttextbytes, Header, URI-Werte, Regelnachrichten usw
Protokollnachrichten.

## Ergebnisgrenze

`OUTCOME` wird erst gesendet, nachdem der Go `ResponseWriter` tatsächlich geschrieben hat
ausgewählte Host-Aktion. Ein fehlgeschlagener oder kurzer Antworttext-Schreibvorgang führt zu einem Commit
Nur Metadaten und niemals ein vom Host bestätigtes Ergebnis. Bevor Sie antworten, schreiben Sie es fest
akzeptiert nur eine übereinstimmende angeforderte Störaktion mit einer expliziten Anforderung
`HOST_ACTION_APPLIED`-Flag und entsprechender sichtbarer Status. Mit einem Run-Local
`event_path`, der Dienst ruft dann die Common Host-Outcome-API auf: Common
behält das rohe Engine-Decision-Ereignis bei und schreibt ein zweites Ereignis mit Canonical
`transport_result=http_status`.

Nachdem Antwortheader/-text festgeschrieben wurden, wird ein Antworttext unterbrochen
Die Entscheidung kann nur als `LOG_ONLY` bestätigt werden, ohne Flag für angewandte Aktion
und der tatsächlich bereits sichtbare HTTP-Status. Der Dienst kann einen Traefik nicht zurücksetzen
Antwort oder ein verspäteter Abbruch beweisen, so verweigert es alle stärkeren Post-Commits
Danksagungen. Seine vom Gastgeber bestätigten Veranstaltungsverwendungen
`transport_result=log_only`. Das Pinned-Host-Probe zeichnet dies nur als auf
gezieltes P4-sicheres/nur-Protokollieren-Verhalten; strikte Spätintervention ist `NOT EXECUTED`.

Der Host-Harness hält `event_path` unter seinem connector-spezifischen Laufzeitstamm,
setzt den allgemeinen Integrationsmodus auf `native-traefik-middleware` und leitet die Rohdaten weiter
JSONL-Artefakt und filtert vom Host bestätigte Ergebnisereignisse nach
kanonische `transport_result`-Werte. Es behandelt nicht das Rohe
„Requested-Decision“-Ereignis als Host-Aktion. Stornierungs-/Trennungsschutz und
Fähigkeitsförderung bleiben separate Arbeiten.
