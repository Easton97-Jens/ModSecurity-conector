# PR #382: Vertrag für native Rückgaben und Ereignisse

**Sprache:** [English](pr-382-event-contract.md) | Deutsch

Stand: Implementierungsreferenz für eine unvollständige Draft-Migration, kein
Nachweis gleichen Verhaltens in allen laufenden Hosts. Die
[Implementierungs- und Verifikationscheckliste](pr-382-checklist.de.md) nennt offene
Routen, fehlgeschlagene Prüfungen und revisionsgebundene Nachweise.

## Native Rückgaben sind operationsspezifisch

Die direkte libModSecurity-API und die Host-Callback-API besitzen unterschiedliche
Rückgabekonventionen. `common/include/msconnector/native_result.h` darf nur an der
dokumentierten nativen Grenze angewendet werden; jede umgebende API behält ihre
eigene Konvention.

| Operation | Akzeptierte native Rückgaben | Erforderliche Folgebehandlung |
| --- | --- | --- |
| Direktes Byte-Append für Request/Response | `0` oder `1` | Bestehenden Phasenablauf fortsetzen und Interventionen an seiner vorgesehenen Grenze abfragen. Null kann das Engine-konfigurierte `ProcessPartial` bedeuten; es beweist nicht, dass der ganze Chunk untersucht wurde. |
| Request-/Response-Phasenauswertung | Nur `1` | Andere Rückgaben als technische Fehler zurückweisen. Eine fehlgeschlagene Phase nicht abschließen oder in eine erfolgreiche Safe-Beobachtung umwandeln. |
| `msc_intervention()` in den geänderten Common-/HAProxy-Pfaden | `0` oder `1` | Keine Intervention von einer abgefragten Intervention unterscheiden; undokumentierte Rückgaben zurückweisen und native Puffer freigeben. |
| `msc_request_body_from_file()` | Eigener API-Vertrag | Byte-Append-Regel nicht wiederverwenden: Null kann auch Datei-I/O- oder Allokationsfehler bedeuten. Verbleibende native Dateipfade sind noch in Prüfung. |
| APR-, NGINX-, HTTP- und Common-Callbacks | Ihre bestehenden Verträge | Host-Erfolgs-/Fehlerzahlen nicht durch den nativen Helfer umdeuten. |

Ein erfolgreicher nativer Aufruf ist keine Allow-Entscheidung. Beispielsweise
kann eine Engine-Limitablehnung eine disruptive Intervention hinterlassen,
obwohl die Append-API eins zurückgibt. Ein Helfer oder Rückgabewerttest beweist
nicht den Zeitpunkt und die Zuständigkeit jeder aufrufenden Interventionsbehandlung.

## Fehlerursache und Hostaktion bleiben getrennt

Die geänderte Common-Fehlerbrücke ordnet `MSCONNECTOR_ERROR_MODSECURITY_FAILURE`
der Klasse `MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE` zu. Timeout,
nicht verfügbare Engine, Connector-, Protokoll- und Body-Limit-Fehler behalten
getrennte Klassen.

Für bekannte technische Fehler verwendet die kanonische Metadatenansicht
`status=error`, `requested_action=error`, einen stabilen Fehlergrund und eine
leere `rule_id`. Der Host muss möglicherweise trotzdem ablehnen oder abbrechen;
diese Aktion macht aus dem technischen Fehler keinen ModSecurity-Regeltreffer.
Body-Limit-Policy-Ereignisse und tatsächliche Regelinterventionen werden nicht
automatisch als technische Fehler umklassifiziert.

## Kanonisches JSONL und fehlende Transportbeobachtungen

`common/include/msconnector/event_protocol.h` liefert dieselbe normalisierte
Ereignisansicht an den Common-JSONL-Writer und die Integritäts-Hash-Berechnung.
Die ursprüngliche Eingabe wird vor der Normalisierung validiert, damit ungültige
oder übergroße Felder nicht durch Ersatzwerte verborgen werden. Query-Redaktion
bleibt aktiv; Body-Nutzdaten werden nicht ergänzt.

| Eingabebedingung | Kanonische Bedeutung |
| --- | --- |
| Bekanntes Regelereignis mit NULL, leerem oder `not_observable`-Transportergebnis | `event=engine_decision`, `message_id=MSCONN_EVENT_ENGINE_DECISION`, leere `actual_action` und eine Meldung, dass keine Hostaktion beobachtet wurde. `action` behält die angeforderte Aktion. |
| Bekannter technischer Fehler ohne Transportbeobachtung | Fehlerursache erhalten, `action=error` verwenden und `actual_action` leer lassen. |
| Beobachtete späte Safe-Regelbehandlung | `actual_action=log_only` und den beobachteten HTTP-Status erhalten. |
| Beobachteter später Strict-Abbruch nach einem anderen Status als 200 | Generisches `MSCONN_EVENT_PHASE4_HARD_ABORT` statt einer Meldung verwenden, die einen vorherigen HTTP 200 behauptet. |
| Unbekanntes Anwendungsereignis | Anwendungseigene Semantik erhalten statt es als WAF-Ereignis zu behandeln. |

Das folgende Beispiel ist ein erläuternder Feldauszug, kein vollständiges
serialisiertes Ereignis und kein aufgezeichnetes Laufzeitergebnis:

```json
{
  "event": "engine_decision",
  "message_id": "MSCONN_EVENT_ENGINE_DECISION",
  "status": "blocked",
  "action": "deny",
  "requested_action": "deny",
  "actual_action": "",
  "http_status": 403,
  "original_http_status": 201,
  "visible_http_status": 201,
  "transport_result": "not_observable"
}
```

Hier klassifiziert `status=blocked` die Regelentscheidung der Engine; es behauptet
nicht, dass eine Blockierung beim Client ankam. Clientseitige Durchsetzung nicht
allein aus `status`, `action` oder dem angeforderten HTTP-Status ableiten.

Die Normalisierung erfindet oder überschreibt keine Zeitstempel, Bytezähler,
EOS-, Commit-, HTTP-Beobachtungen, Abbruch-/Resetflags oder Transportnachweise.
Ereigniserzeuger müssen wahrheitsgemäße, untereinander konsistente Metadaten
liefern; der verbleibende Vergleich bis zur Ausgabe wird getrennt verfolgt.
Insbesondere korrigiert diese Änderung nicht pauschal jedes Body-Limit-,
Abbruch- oder anwendungseigene Ereignis.

## Migration für Log-Auswerter

Auswerter müssen die neue Engine-Decision-Kennung erkennen, leere
`actual_action` akzeptieren und angeforderte Aktionen von beobachteten Ergebnissen
trennen. Durchsetzung nicht aus einem alten Phasenereignisnamen oder einer
früheren Standardmeldung ableiten. Relevante Metadatenfelder vergleichen statt
identische Transaktions-IDs, Zeitstempel, Hostnamen, Bytezähler oder native
Log-Präfixe zu erwarten.

Die normalisierte Darstellung betrifft auch die Integritäts-Hash-Berechnung.
Erzeuger und Prüfer müssen kompatible Vertragsversionen verwenden; aufbewahrte
Datensätze sind mit der erzeugenden Implementierung zu validieren. Vor einer
Freigabe bleibt eine Kompatibilitäts-/Versionierungsprüfung für historische
Auswerter erforderlich. ModSecurity-Auditlog und native Hostdiagnosen bleiben
vom Common-Metadaten-JSONL getrennt.

## Sonar-Verifikation ohne neue Befunde

Der Nutzer verlangt null neue PR-Issues und null neue Security Hotspots, nicht
nur ein bestandenes Sonar Quality Gate. `ci/checks/common/check-sonar-zero.py`
liest den Sonar-GitHub-Check des exakten PR-Heads und verlangt explizit null
Issues, Hotspots und Annotationen sowie ein erfolgreiches Ergebnis.

Fehlende Analyse, ältere SHA, falscher Anbieter, fehlende oder mehrdeutige Zähler,
eine neuere unfertige Analyse oder jeder positive Befundzähler lassen die
Verifikation fehlschlagen. Begrenztes Polling wartet nur auf den Analyseabschluss;
es sind keine Wiederholungen zum Verbergen von Befunden. Die Prüfung akzeptiert
keine Issues und ändert keine Scanner-Ausnahmen. Sie liest GitHub Checks mit
jobbezogenen Leserechten; ein Sonar-Token wird weder benötigt noch offengelegt.
Sie beweist nicht, dass der gesamte historische Issue-Bestand des Projekts null
ist, und ersetzt keine Code- oder Host-Integrationstests.

## Nachweisgrenzen und verbleibende Arbeit

Kompilierte Common-Tests prüfen native Rückgabeklassifizierung, echten
JSONL-/Hash-Code, Redaktion und fehlende Beobachtungen. Extrahierte HAProxy-
Auswertungstests prüfen Phasenreihenfolge, jeden injizierten nativen Aufruffehler,
teilweisen Ressourcenbesitz und Freigabereihenfolge sowie begrenzte Rule-ID-
Dekodierung. Separate Kompatibilitätstests kompilieren und linken das tatsächliche
HAProxy-Binding gegen kontrollierte native API-Testgrenzen.

Diese Ebenen beweisen kein echtes HTTP-Verhalten, keine `strict`-Reset-/
Abbruchunterstützung, kein Überleben benachbarter Streams und keine gleichen Logs
aller direkten/Companion-/Middleware-/Sidecar-Routen. Nicht unterstützte Profile
bleiben nicht unterstützt. Modusstandards, Engine-eigene MIME-Auswahl, unabhängige
Transport-/Ressourcengrenzen und bestehende Sicherheitsprüfungen werden nicht
geschwächt. Ein später Abbruch kann gesendete Bytes nicht zurückholen.

Vor der Freigabe bleiben die offenen Checklistenpunkte abzuschließen, darunter
NGINX-Adoption-/Mutationstests, native Request-/Datei- und späte Fehlerpfade,
Erzeuger-/Ausgabefehlerbehandlung, Connector-Anleitungen und echte Host-Matrizen.
