# HAProxy Integration Decision

## Status

decision_status: undecided
implementation_status: not_started
runtime_verified: false
promoted: false

## Kurzfazit

Mehrere Integrationsoptionen sind aus Repository-Sicht plausibel, aber aktuell ist
keine Option ausreichend belegt, um eine belastbare technische Entscheidung zu
beanspruchen.

## Optionen

1. SPOE / SPOA-Agent
2. HAProxy native Filter / native Extension
3. Lua-basierte Integration
4. Externer HTTP-Service / Sidecar

## Vergleichstabelle

| Option | Im Repo belegt | Abgeleitet | Extern zu verifizieren | Risiken | Empfehlung |
|---|---|---|---|---|---|
| SPOE / SPOA-Agent | In `docs/connectors/future-connectors.md` als erwartetes Modell genannt; im HAProxy-Scaffold als Option erfasst. | Kann als Connector-Komponente in einen Harness-Start/Stop/Request/Log-Flow eingebunden werden. | Vollständige Request-/Response-/Body-Semantik, Fehlerpfade, Lifecycle-Details. | Buffering/Streaming, Response-Inspection, SPOE-Fehlerpfade. | Starker Kandidat aus Repo-Sicht, aber Entscheidung noch nicht belastbar. |
| HAProxy native Filter / native Extension | In `docs/connectors/future-connectors.md` als native extension path erwähnt; im HAProxy-Scaffold als Option erfasst. | Direkte Integration in HAProxy-Lifecycle möglich. | Konkrete Hookpunkte, API-Details, Build-/Packaging-Anforderungen. | Hohe Kopplung an Serverinterna, unklare Body-/Intervention-Semantik. | Starker Kandidat aus Repo-Sicht, aber Entscheidung noch nicht belastbar. |
| Lua-basierte Integration | Im HAProxy-Scaffold als Option genannt. | Kann als schnellere Integrationsspur untersucht werden. | Funktionsumfang für vollständige ModSecurity-Semantik, Body-Verfügbarkeit, Eingriffsmöglichkeiten. | Mögliche Grenzen bei Response-Body/Intervention/Leistung. | Plausibel, aber im Repo schwächer belegt. |
| Externer HTTP-Service / Sidecar | Im HAProxy-Scaffold als Option genannt. | Entkopplung vom HAProxy-Prozess denkbar. | Protokolltreue, Kontextübertragung, Latenz-/Fehlerverhalten, Sicherheitsmodell. | Zusätzliche Betriebs- und Netzwerkabhängigkeiten. | Plausibel, aber im Repo schwächer belegt. |

## Bewertungsfragen pro Option

Für alle untenstehenden Fragen gilt:
- Testdefinition und Testausführung erfolgen ausschließlich im ModSecurity-test-Framework.
- No tests are stored in this connector repository.

### 1) SPOE / SPOA-Agent

#### Request Inspection
- Wie wird der Request an ModSecurity übergeben? **Extern zu verifizieren.**
- Sind Header, URI, Methode und Body verfügbar? **Extern zu verifizieren.**
- Ist Body-Buffering nötig? **Extern zu verifizieren.**
- Was passiert bei großen Requests? **Extern zu verifizieren.**

#### Response Header Inspection
- Können Response Header geprüft werden? **Extern zu verifizieren.**
- Zu welchem Zeitpunkt? **Extern zu verifizieren.**
- Kann danach noch blockiert oder modifiziert werden? **Extern zu verifizieren.**

#### Response Body Inspection
- Ist Response Body verfügbar? **Extern zu verifizieren.**
- Streaming oder Buffering? **Extern zu verifizieren.**
- Welche Größenlimits gelten? **Extern zu verifizieren.**
- Kann nach Body-Prüfung noch eingegriffen werden? **Extern zu verifizieren.**

#### Intervention Mapping
- Wie wird block/allow/log von ModSecurity auf HAProxy gemappt? **Extern zu verifizieren.**
- Gibt es HTTP-Status-Mapping? **Extern zu verifizieren.**
- Gibt es Redirect-/Deny-Mapping? **Extern zu verifizieren.**
- Was passiert bei Fehlern? **Extern zu verifizieren.**

#### Build Artefacts
- Welches Artefakt entsteht (Agent/Modul/Lua/Sidecar)? **Nicht belegbar aus dem aktuellen Repository.**
- Wie würde es gestartet? **Extern zu verifizieren.**
- Wie würde es versioniert? **Nicht belegbar aus dem aktuellen Repository.**

#### Harness Requirements
- prepare / start / stop / send_request / collect_logs / cleanup: Im Repo als erwartete Harness-Aufgaben beschrieben, aber ohne HAProxy-Implementierung. **Im Repo belegt (ohne Implementierung).**

#### Framework-seitige Testerwartungen
- haproxy_config_syntax
- haproxy_startup
- spoa_component_startup
- benign_request_allowed
- malicious_request_block_signal
- logs_emitted
- report_generated

Status: **Noch zu prüfen.**

### 2) HAProxy native Filter / native Extension

#### Request Inspection
- Wie wird der Request an ModSecurity übergeben? **Extern zu verifizieren.**
- Sind Header, URI, Methode und Body verfügbar? **Extern zu verifizieren.**
- Ist Body-Buffering nötig? **Extern zu verifizieren.**
- Was passiert bei großen Requests? **Extern zu verifizieren.**

#### Response Header Inspection
- Können Response Header geprüft werden? **Extern zu verifizieren.**
- Zu welchem Zeitpunkt? **Extern zu verifizieren.**
- Kann danach noch blockiert oder modifiziert werden? **Extern zu verifizieren.**

#### Response Body Inspection
- Ist Response Body verfügbar? **Extern zu verifizieren.**
- Streaming oder Buffering? **Extern zu verifizieren.**
- Welche Größenlimits gelten? **Extern zu verifizieren.**
- Kann nach Body-Prüfung noch eingegriffen werden? **Extern zu verifizieren.**

#### Intervention Mapping
- Wie wird block/allow/log von ModSecurity auf HAProxy gemappt? **Extern zu verifizieren.**
- Gibt es HTTP-Status-Mapping? **Extern zu verifizieren.**
- Gibt es Redirect-/Deny-Mapping? **Extern zu verifizieren.**
- Was passiert bei Fehlern? **Extern zu verifizieren.**

#### Build Artefacts
- Welches Artefakt entsteht (Agent/Modul/Lua/Sidecar)? **Nicht belegbar aus dem aktuellen Repository.**
- Wie würde es gestartet? **Extern zu verifizieren.**
- Wie würde es versioniert? **Nicht belegbar aus dem aktuellen Repository.**

#### Harness Requirements
- prepare / start / stop / send_request / collect_logs / cleanup: **Im Repo belegt (als Erwartung), nicht implementiert.**

#### Framework-seitige Testerwartungen
- wie oben, zentral im ModSecurity-test-Framework.
Status: **Noch zu prüfen.**

### 3) Lua-basierte Integration

#### Request Inspection
- Wie wird der Request an ModSecurity übergeben? **Extern zu verifizieren.**
- Sind Header, URI, Methode und Body verfügbar? **Extern zu verifizieren.**
- Ist Body-Buffering nötig? **Extern zu verifizieren.**
- Was passiert bei großen Requests? **Extern zu verifizieren.**

#### Response Header Inspection
- Können Response Header geprüft werden? **Extern zu verifizieren.**
- Zu welchem Zeitpunkt? **Extern zu verifizieren.**
- Kann danach noch blockiert oder modifiziert werden? **Extern zu verifizieren.**

#### Response Body Inspection
- Ist Response Body verfügbar? **Extern zu verifizieren.**
- Streaming oder Buffering? **Extern zu verifizieren.**
- Welche Größenlimits gelten? **Extern zu verifizieren.**
- Kann nach Body-Prüfung noch eingegriffen werden? **Extern zu verifizieren.**

#### Intervention Mapping
- Wie wird block/allow/log von ModSecurity auf HAProxy gemappt? **Extern zu verifizieren.**
- Gibt es HTTP-Status-Mapping? **Extern zu verifizieren.**
- Gibt es Redirect-/Deny-Mapping? **Extern zu verifizieren.**
- Was passiert bei Fehlern? **Extern zu verifizieren.**

#### Build Artefacts
- Welches Artefakt entsteht (Agent/Modul/Lua/Sidecar)? **Nicht belegbar aus dem aktuellen Repository.**
- Wie würde es gestartet? **Extern zu verifizieren.**
- Wie würde es versioniert? **Nicht belegbar aus dem aktuellen Repository.**

#### Harness Requirements
- prepare / start / stop / send_request / collect_logs / cleanup: **Im Repo belegt (als Erwartung), nicht implementiert.**

#### Framework-seitige Testerwartungen
- wie oben, zentral im ModSecurity-test-Framework.
Status: **Noch zu prüfen.**

### 4) Externer HTTP-Service / Sidecar

#### Request Inspection
- Wie wird der Request an ModSecurity übergeben? **Extern zu verifizieren.**
- Sind Header, URI, Methode und Body verfügbar? **Extern zu verifizieren.**
- Ist Body-Buffering nötig? **Extern zu verifizieren.**
- Was passiert bei großen Requests? **Extern zu verifizieren.**

#### Response Header Inspection
- Können Response Header geprüft werden? **Extern zu verifizieren.**
- Zu welchem Zeitpunkt? **Extern zu verifizieren.**
- Kann danach noch blockiert oder modifiziert werden? **Extern zu verifizieren.**

#### Response Body Inspection
- Ist Response Body verfügbar? **Extern zu verifizieren.**
- Streaming oder Buffering? **Extern zu verifizieren.**
- Welche Größenlimits gelten? **Extern zu verifizieren.**
- Kann nach Body-Prüfung noch eingegriffen werden? **Extern zu verifizieren.**

#### Intervention Mapping
- Wie wird block/allow/log von ModSecurity auf HAProxy gemappt? **Extern zu verifizieren.**
- Gibt es HTTP-Status-Mapping? **Extern zu verifizieren.**
- Gibt es Redirect-/Deny-Mapping? **Extern zu verifizieren.**
- Was passiert bei Fehlern? **Extern zu verifizieren.**

#### Build Artefacts
- Welches Artefakt entsteht (Agent/Modul/Lua/Sidecar)? **Nicht belegbar aus dem aktuellen Repository.**
- Wie würde es gestartet? **Extern zu verifizieren.**
- Wie würde es versioniert? **Nicht belegbar aus dem aktuellen Repository.**

#### Harness Requirements
- prepare / start / stop / send_request / collect_logs / cleanup: **Im Repo belegt (als Erwartung), nicht implementiert.**

#### Framework-seitige Testerwartungen
- wie oben, zentral im ModSecurity-test-Framework.
Status: **Noch zu prüfen.**

## Aktueller Stand aus dem Repository

- `connectors/haproxy/README.md`: HAProxy ist Scaffold, nicht implementiert, nicht runtime-verifiziert, nicht promoted.
- `connectors/haproxy/TODO.md`: Integrationsstrategie, Request/Response-Pfad, Intervention-Mapping, Logging, Build/Betrieb sind offen.
- `connectors/haproxy/docs/architecture.md`: Optionen genannt, keine Entscheidung getroffen.
- `connectors/haproxy/docs/build.md`: Build-Fragen offen, keine funktionierende Pipeline behauptet.
- `connectors/haproxy/docs/validation.md`: Mindestanforderungen an Runtime-Evidence dokumentiert (framework-seitig).
- `docs/connectors/future-connectors.md`: HAProxy erwartet SPOE oder native extension; schwierige Bereiche benannt.
- `docs/architecture/connector-adapter-interface.md`: Required Hooks und Connector-/Runner-Grenzen definiert.

## Vorläufige Empfehlung

SPOE/SPOA-Agent und native Filter/native Extension sind die stärksten Kandidaten
aus Repository-Sicht. Aber: Die Entscheidung ist noch nicht belastbar, solange
HAProxy-Lifecycle, Response-Body-Verhalten, Intervention-Mapping und
Build-Artefakte nicht extern geprüft wurden.

## Nicht beantwortbar aus dem aktuellen Repository

- Welche Option technisch überlegen ist.
- Ob Response Body Inspection vollständig möglich ist.
- Wie Interventions vollständig gemappt werden.
- Welche Build-Artefakte konkret entstehen.
- Welche Performance-/Latenz-Auswirkungen entstehen.
