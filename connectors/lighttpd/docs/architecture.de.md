# lighttpd-Architektur

**Sprache:** [English](architecture.md) | Deutsch

Status: natives Modul, `minimal_runtime_smoke` für eine Phase-1-Header-Regel

## Laufzeitablauf

```text
lighttpd handle_uri_clean
  -> lighttpd request mapper
  -> Common request contract and resource limits
  -> Common/libmodsecurity transaction begin
  -> allow or http_status_set_err(...)

lighttpd handle_response_start
  -> lighttpd response mapper
  -> Common response contract and resource limits
  -> Common/libmodsecurity response processing

lighttpd handle_request_reset
  -> transaction finish and destroy
  -> mapped header storage release
```

`module/mod_msconnector.c` ist die einzige Plugin-Lebenszyklusschicht.
`src/lighttpd_modsecurity_mapper.c` ist die einzige Host-Mapping-Schicht. Das Gemeinsame
Laufzeit und alle gängigen SDK-Typen bleiben frei von Lighttpd-Headern und Callbacks
Typen.

## Plugin-Lebenszyklus

Das Modul exportiert `mod_msconnector_plugin_init` für den Lighttpd-Loader und
registriert:

- `init` zum Zuweisen des Plugin-Status;
- `set_defaults` zum Registrieren von Host-Anweisungen und Validieren der Common Runtime
  config, Regeln laden und die gemeinsame Laufzeit erstellen;
- `handle_uri_clean` für Anforderungsmetadaten und Anforderungsheader;
- `handle_response_start` für Antwortmetadaten und Antwortheader;
- `handle_request_reset` für den Transaktionsabschluss und die Bereinigung;
- `cleanup`, um die Common Runtime zu zerstören.

Die Anweisungen gelten serverweit. Eine einzelne Laufzeit wird daraus erstellt
`msconnector.config-file`; Jede Anfrage erhält eine eigene Transaktion und einen eigenen Mapper
Speicherung in `r->plugin_ctx`.

## Zuordnung und Eigentum

Der Request Mapper stellt Methode, ursprüngliches Ziel, HTTP-Version, Hostnamen usw. bereit.
Clientadresse/-port, Servername/-port und jeder Lighttpd-String-Header als
längenbegrenzter gemeinsamer Header. Der Antwort-Mapper stellt den Status HTTP bereit
Version und Antwortheader.

Die Anzahl der Header und die Gesamtbyte-Grenzwerte werden vor dem Laufzeiteintrag überprüft. Das Gemeinsame
DoS/Ressourcenschutz wendet die konfigurierten Werte pro Name, Wert, Text usw. an
Grenzen. Header-Werte bleiben Slices und werden niemals als nicht validiertes C behandelt
Saiten.

Die Common Runtime übernimmt die zugeordnete Anfrage und Antwort. Daher die
Der Handler-Kontext besitzt die zugeordneten Header-Arrays bis `handle_request_reset`.
Alle Mapper-Error- und Transaction-Begin-Fehlerpfade geben ihren eigenen Status frei.

## Entscheidungen und Ereignisse

Eine störende Anfrage-Header-Entscheidung wird mithilfe von in eine Fehlerantwort umgewandelt
lighttpds `http_status_set_err()`. Die überprüfte Regel fordert den Status 403 an.
Laufzeit- oder Mapper-Fehler verwenden die Common-Error-zu-HTTP-Zuordnung. Umleiten, löschen,
Verbindungsabbruch und Spätinterventionssemantik wurden nicht getrennt betrachtet
bestätigt durch diesen schmalen Smoke-Test.

Die Common Runtime verfügt über das Laden von Regeln, Transaktions-IDs, Flow Guards,
libmodsecurity-Aufrufe, Entscheidungen, Ereigniskonstruktion, Integritätsmetadaten und
JSONL-Serialisierung. Der Standard-Connector-Modus leitet keine Anfrage oder Antwort weiter
Körpernutzlast zu diesem Ereignispfad hinzufügen.

## Körpergrenze

Der Aktienmodus überschreibt beide Mapper-Verträge
`MSCONNECTOR_MAPPER_UNSUPPORTED` und bildet einen Körper mit der Länge Null ab. Der einheimische Smoke-Test
Konfigurationssätze `request_body_mode=none` und `response_body_mode=none`.Der separate, über den gesamten Lebenszyklus ausgewählte Lighttpd 1.4.84-Patch fügt eine versionierte Version hinzu
ABI für ausgeliehene HTTP/1.x-Anfragetextbereiche und Identitätsentitätsantworten
Bereiche. Der Antwortrückruf wird in `http_chunk_append_mem()` und aufgerufen
`http_chunk_append_buffer()`, bevor dieser Kern HTTP/1-Transfer-Framing anwendet;
Es handelt sich nicht um einen Socket-Queue-Rückruf. Die ausgewählte Filterreihenfolge ist
Anwendung/Backend → ausgewählter Identitätsentitätsbereich → msconnector-Rückruf →
HTTP/1-Transfer-Framing → Socket. Der Rückruf erhält nur einen synchronen
geliehener Zeiger und Länge, verschiebt einen monotonen Entitätsoffset und signalisiert
Einmal EOS. Es wird keine Körperwarteschlange im Besitz des Connectors beibehalten.

Die gepatchte Bindung kann inkrementell Anforderungs- und Antwortbereiche an übergeben
Common Runtime, wenn der entsprechende Modus `streaming` ist. Gepufferte Anfrage
Der Modus bleibt abgelehnt. Der ausgewählte Antwortbereich ist nur Identität: gzip/br,
HTTP/2- und ungeprüfte Datei-/Zero-Copy-Ausgaberouten werden nicht als Text geltend gemacht
Inspektionswege. Nach dem einmaligen Anhängen treten kurze Schreibvorgänge und `EAGAIN` auf
Rückruf, sodass der Strukturvertrag die Entitätsaufnahme nicht auf einem duplizieren kann
Socket-Wiederholung; diesem Verhalten fehlt immer noch ein Fehlerinjektionslauf auf einem echten Host.

Der gepatchte Host hat einen schmalen echten Phase-1 200/403-Smoke-Test, aber das ist kein P4
Laufzeitbeweise. Es erweist sich noch nicht als sicher, dass eine vom Kunden beachtete Phase-4-Regel sicher ist
Ergebnis, strikter Abbruch, Kürzung, erstes Byte oder Ergebnis ohne vollständigen Puffer.
Sichere/minimale Quellverhaltensdatensätze `log_only`; streng bleibt bewusst bestehen
`NOT EXECUTED`, da kein vom Client validiertes Lighttpd-Abbruchprimitiv vorhanden ist.

## Alternative Wege

Der Legacy-Brückenstarter und das Framework `sidecar_proxy` Smoke bleiben getrennt
Artefakte. Der primäre Connector-Pfad ist jetzt das native Modul. FastCGI, SCGI,
und mod_magnet/Lua werden von diesem Modul nicht implementiert.

## Aktuelle Anspruchsgrenze

Der verifizierte 200/403-Smoke-Test unterstützt `minimal_runtime_smoke` und
Nur `partial_runtime_path`. Es unterstützt keine produktionsbereite Sicherheit
verifiziert, CRS-verifiziert, Response-Body-verifiziert oder Full-Matrix-Ansprüche.
