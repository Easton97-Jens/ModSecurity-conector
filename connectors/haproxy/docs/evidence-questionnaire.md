# HAProxy Integration Evidence Questionnaire

## Status
questionnaire_status: draft
implementation_status: not_started
runtime_verified: false
decision_status: undecided

## Zweck
Dieser Fragebogen dient dazu, externe HAProxy-Fakten strukturiert zu prüfen,
bevor eine Integrationsentscheidung oder Implementierung erfolgt.

## Regeln für Evidenz
Jede Antwort muss eine der folgenden Markierungen enthalten:
- Belegt durch Repository
- Extern belegt
- Abgeleitet
- Nicht belegbar
- Noch zu prüfen

Jede technische Aussage braucht:
- Quelle
- Datum der Prüfung
- getestete HAProxy-Version, falls relevant
- kurze Begründung
- Risiko-Einschätzung

Wenn eine Aussage nicht mit dem aktuellen Repository belegt werden kann:
- "Nicht belegbar aus dem aktuellen Repository."

Wenn eine Aussage nur über externe Dokumentation/Tests verifiziert werden kann:
- "Extern zu verifizieren."

## Optionen
Für jede Option gilt derselbe Fragenkatalog. Es wird hier keine Option ausgewählt.

### Option: SPOE / SPOA-Agent

#### 1. Request Inspection
- Können Methode, URI, Pfad, Query, Header und Body geprüft werden?
- Sind große Request Bodies möglich?
- Ist Body-Buffering nötig?
- Gibt es Größenlimits?
- Was passiert bei Chunked/Streaming Requests?
- Kann vor Weiterleitung an Backend blockiert werden?
Status: Extern zu verifizieren.

#### 2. Response Header Inspection
- Können Response Header geprüft werden?
- Zu welchem Zeitpunkt?
- Kann nach Header-Prüfung noch blockiert/geändert werden?
- Welche Einschränkungen gibt es?
Status: Extern zu verifizieren.

#### 3. Response Body Inspection
- Kann der Response Body geprüft werden?
- Streaming oder Buffering?
- Gibt es Größenlimits?
- Kann nach Body-Prüfung noch blockiert/geändert werden?
- Welche Latenz-/Speicherfolgen entstehen?
Status: Extern zu verifizieren.

#### 4. Intervention Mapping
- Wie wird ModSecurity allow gemappt?
- Wie wird deny/block gemappt?
- Wie werden Statuscodes gemappt?
- Wie werden Redirects gemappt?
- Wie werden Fehler im Connector gemappt?
- Was ist das Fail-open/Fail-closed-Verhalten?
Status: Extern zu verifizieren.

#### 5. Build Artefacts
- Welches Artefakt entsteht?
  - Binary?
  - Agent?
  - Modul?
  - Lua-Script?
  - Container?
- Wie wird es gebaut?
- Wie wird es versioniert?
- Wie wird es deployed?
- Ist HAProxy-Neukompilierung nötig?
Status: Nicht belegbar aus dem aktuellen Repository.

#### 6. Runtime Lifecycle
- Wie startet die Connector-Komponente?
- Wie stoppt sie?
- Wie wird Health geprüft?
- Wie werden Timeouts behandelt?
- Wie werden Verbindungsfehler behandelt?
- Wie wird Reload/Restart behandelt?
Status: Extern zu verifizieren.

#### 7. Logging & Observability
- Welche Logs entstehen?
- Wo entstehen sie?
- Gibt es Audit Logs?
- Gibt es Debug Logs?
- Wie wird ein Request eindeutig korreliert?
- Welche Metriken wären nötig?
Status: Extern zu verifizieren.

#### 8. Harness Requirements
- prepare
- start
- stop
- send_request
- collect_logs
- cleanup
- report generation

Für jeden Hook:
- Was muss der Hook konkret tun?
- Welche Artefakte braucht er?
- Welche Exit-Kriterien gibt es?

Status:
- Hook-Namen und allgemeine Verantwortung: Belegt durch Repository.
- HAProxy-spezifische Umsetzung: Extern zu verifizieren.

#### 9. Minimal Runtime Tests
- HAProxy config syntax valid
- HAProxy starts
- Connector component starts
- benign request allowed
- malicious request blocked
- response header case covered
- response body case covered
- logs emitted
- report generated

Für jeden Test:
- Eingangsdaten
- erwartetes Ergebnis
- Belegart
- offen/erfüllt

Status: Noch zu prüfen.

#### 10. Risiken
- technische Risiken
- Performance-Risiken
- Sicherheitsrisiken
- Betriebsrisiken
- Testbarkeitsrisiken
Status: Noch zu prüfen.

### Option: HAProxy native Filter / native Extension

#### 1. Request Inspection
- Können Methode, URI, Pfad, Query, Header und Body geprüft werden?
- Sind große Request Bodies möglich?
- Ist Body-Buffering nötig?
- Gibt es Größenlimits?
- Was passiert bei Chunked/Streaming Requests?
- Kann vor Weiterleitung an Backend blockiert werden?
Status: Extern zu verifizieren.

#### 2. Response Header Inspection
- Können Response Header geprüft werden?
- Zu welchem Zeitpunkt?
- Kann nach Header-Prüfung noch blockiert/geändert werden?
- Welche Einschränkungen gibt es?
Status: Extern zu verifizieren.

#### 3. Response Body Inspection
- Kann der Response Body geprüft werden?
- Streaming oder Buffering?
- Gibt es Größenlimits?
- Kann nach Body-Prüfung noch blockiert/geändert werden?
- Welche Latenz-/Speicherfolgen entstehen?
Status: Extern zu verifizieren.

#### 4. Intervention Mapping
- Wie wird ModSecurity allow gemappt?
- Wie wird deny/block gemappt?
- Wie werden Statuscodes gemappt?
- Wie werden Redirects gemappt?
- Wie werden Fehler im Connector gemappt?
- Was ist das Fail-open/Fail-closed-Verhalten?
Status: Extern zu verifizieren.

#### 5. Build Artefacts
- Welches Artefakt entsteht?
  - Binary?
  - Agent?
  - Modul?
  - Lua-Script?
  - Container?
- Wie wird es gebaut?
- Wie wird es versioniert?
- Wie wird es deployed?
- Ist HAProxy-Neukompilierung nötig?
Status: Nicht belegbar aus dem aktuellen Repository.

#### 6. Runtime Lifecycle
- Wie startet die Connector-Komponente?
- Wie stoppt sie?
- Wie wird Health geprüft?
- Wie werden Timeouts behandelt?
- Wie werden Verbindungsfehler behandelt?
- Wie wird Reload/Restart behandelt?
Status: Extern zu verifizieren.

#### 7. Logging & Observability
- Welche Logs entstehen?
- Wo entstehen sie?
- Gibt es Audit Logs?
- Gibt es Debug Logs?
- Wie wird ein Request eindeutig korreliert?
- Welche Metriken wären nötig?
Status: Extern zu verifizieren.

#### 8. Harness Requirements
- prepare
- start
- stop
- send_request
- collect_logs
- cleanup
- report generation

Für jeden Hook:
- Was muss der Hook konkret tun?
- Welche Artefakte braucht er?
- Welche Exit-Kriterien gibt es?

Status:
- Hook-Namen und allgemeine Verantwortung: Belegt durch Repository.
- HAProxy-spezifische Umsetzung: Extern zu verifizieren.

#### 9. Minimal Runtime Tests
- HAProxy config syntax valid
- HAProxy starts
- Connector component starts
- benign request allowed
- malicious request blocked
- response header case covered
- response body case covered
- logs emitted
- report generated

Für jeden Test:
- Eingangsdaten
- erwartetes Ergebnis
- Belegart
- offen/erfüllt

Status: Noch zu prüfen.

#### 10. Risiken
- technische Risiken
- Performance-Risiken
- Sicherheitsrisiken
- Betriebsrisiken
- Testbarkeitsrisiken
Status: Noch zu prüfen.

### Option: Lua-basierte Integration

#### 1. Request Inspection
- Können Methode, URI, Pfad, Query, Header und Body geprüft werden?
- Sind große Request Bodies möglich?
- Ist Body-Buffering nötig?
- Gibt es Größenlimits?
- Was passiert bei Chunked/Streaming Requests?
- Kann vor Weiterleitung an Backend blockiert werden?
Status: Extern zu verifizieren.

#### 2. Response Header Inspection
- Können Response Header geprüft werden?
- Zu welchem Zeitpunkt?
- Kann nach Header-Prüfung noch blockiert/geändert werden?
- Welche Einschränkungen gibt es?
Status: Extern zu verifizieren.

#### 3. Response Body Inspection
- Kann der Response Body geprüft werden?
- Streaming oder Buffering?
- Gibt es Größenlimits?
- Kann nach Body-Prüfung noch blockiert/geändert werden?
- Welche Latenz-/Speicherfolgen entstehen?
Status: Extern zu verifizieren.

#### 4. Intervention Mapping
- Wie wird ModSecurity allow gemappt?
- Wie wird deny/block gemappt?
- Wie werden Statuscodes gemappt?
- Wie werden Redirects gemappt?
- Wie werden Fehler im Connector gemappt?
- Was ist das Fail-open/Fail-closed-Verhalten?
Status: Extern zu verifizieren.

#### 5. Build Artefacts
- Welches Artefakt entsteht?
  - Binary?
  - Agent?
  - Modul?
  - Lua-Script?
  - Container?
- Wie wird es gebaut?
- Wie wird es versioniert?
- Wie wird es deployed?
- Ist HAProxy-Neukompilierung nötig?
Status: Nicht belegbar aus dem aktuellen Repository.

#### 6. Runtime Lifecycle
- Wie startet die Connector-Komponente?
- Wie stoppt sie?
- Wie wird Health geprüft?
- Wie werden Timeouts behandelt?
- Wie werden Verbindungsfehler behandelt?
- Wie wird Reload/Restart behandelt?
Status: Extern zu verifizieren.

#### 7. Logging & Observability
- Welche Logs entstehen?
- Wo entstehen sie?
- Gibt es Audit Logs?
- Gibt es Debug Logs?
- Wie wird ein Request eindeutig korreliert?
- Welche Metriken wären nötig?
Status: Extern zu verifizieren.

#### 8. Harness Requirements
- prepare
- start
- stop
- send_request
- collect_logs
- cleanup
- report generation

Für jeden Hook:
- Was muss der Hook konkret tun?
- Welche Artefakte braucht er?
- Welche Exit-Kriterien gibt es?

Status:
- Hook-Namen und allgemeine Verantwortung: Belegt durch Repository.
- HAProxy-spezifische Umsetzung: Extern zu verifizieren.

#### 9. Minimal Runtime Tests
- HAProxy config syntax valid
- HAProxy starts
- Connector component starts
- benign request allowed
- malicious request blocked
- response header case covered
- response body case covered
- logs emitted
- report generated

Für jeden Test:
- Eingangsdaten
- erwartetes Ergebnis
- Belegart
- offen/erfüllt

Status: Noch zu prüfen.

#### 10. Risiken
- technische Risiken
- Performance-Risiken
- Sicherheitsrisiken
- Betriebsrisiken
- Testbarkeitsrisiken
Status: Noch zu prüfen.

### Option: Externer HTTP-Service / Sidecar

#### 1. Request Inspection
- Können Methode, URI, Pfad, Query, Header und Body geprüft werden?
- Sind große Request Bodies möglich?
- Ist Body-Buffering nötig?
- Gibt es Größenlimits?
- Was passiert bei Chunked/Streaming Requests?
- Kann vor Weiterleitung an Backend blockiert werden?
Status: Extern zu verifizieren.

#### 2. Response Header Inspection
- Können Response Header geprüft werden?
- Zu welchem Zeitpunkt?
- Kann nach Header-Prüfung noch blockiert/geändert werden?
- Welche Einschränkungen gibt es?
Status: Extern zu verifizieren.

#### 3. Response Body Inspection
- Kann der Response Body geprüft werden?
- Streaming oder Buffering?
- Gibt es Größenlimits?
- Kann nach Body-Prüfung noch blockiert/geändert werden?
- Welche Latenz-/Speicherfolgen entstehen?
Status: Extern zu verifizieren.

#### 4. Intervention Mapping
- Wie wird ModSecurity allow gemappt?
- Wie wird deny/block gemappt?
- Wie werden Statuscodes gemappt?
- Wie werden Redirects gemappt?
- Wie werden Fehler im Connector gemappt?
- Was ist das Fail-open/Fail-closed-Verhalten?
Status: Extern zu verifizieren.

#### 5. Build Artefacts
- Welches Artefakt entsteht?
  - Binary?
  - Agent?
  - Modul?
  - Lua-Script?
  - Container?
- Wie wird es gebaut?
- Wie wird es versioniert?
- Wie wird es deployed?
- Ist HAProxy-Neukompilierung nötig?
Status: Nicht belegbar aus dem aktuellen Repository.

#### 6. Runtime Lifecycle
- Wie startet die Connector-Komponente?
- Wie stoppt sie?
- Wie wird Health geprüft?
- Wie werden Timeouts behandelt?
- Wie werden Verbindungsfehler behandelt?
- Wie wird Reload/Restart behandelt?
Status: Extern zu verifizieren.

#### 7. Logging & Observability
- Welche Logs entstehen?
- Wo entstehen sie?
- Gibt es Audit Logs?
- Gibt es Debug Logs?
- Wie wird ein Request eindeutig korreliert?
- Welche Metriken wären nötig?
Status: Extern zu verifizieren.

#### 8. Harness Requirements
- prepare
- start
- stop
- send_request
- collect_logs
- cleanup
- report generation

Für jeden Hook:
- Was muss der Hook konkret tun?
- Welche Artefakte braucht er?
- Welche Exit-Kriterien gibt es?

Status:
- Hook-Namen und allgemeine Verantwortung: Belegt durch Repository.
- HAProxy-spezifische Umsetzung: Extern zu verifizieren.

#### 9. Minimal Runtime Tests
- HAProxy config syntax valid
- HAProxy starts
- Connector component starts
- benign request allowed
- malicious request blocked
- response header case covered
- response body case covered
- logs emitted
- report generated

Für jeden Test:
- Eingangsdaten
- erwartetes Ergebnis
- Belegart
- offen/erfüllt

Status: Noch zu prüfen.

#### 10. Risiken
- technische Risiken
- Performance-Risiken
- Sicherheitsrisiken
- Betriebsrisiken
- Testbarkeitsrisiken
Status: Noch zu prüfen.

## Vergleichsmatrix

| Option | Request | Response Header | Response Body | Intervention Mapping | Build | Lifecycle | Logging | Tests | Gesamtstatus |
|---|---|---|---|---|---|---|---|---|---|
| SPOE / SPOA-Agent | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. |
| HAProxy native Filter / native Extension | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. |
| Lua-basierte Integration | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. |
| Externer HTTP-Service / Sidecar | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. | Noch zu prüfen. |

## Entscheidungskriterien
Eine Option darf erst empfohlen werden, wenn mindestens diese Punkte extern
belegt sind:
- Request Inspection möglich
- Block/Allow vor Backend möglich
- Logging möglich
- Harness start/stop/send_request/collect_logs möglich
- Minimaler Smoke-Test realistisch
- Build-/Deployment-Modell bekannt

Response Body Inspection darf entweder:
- belegt unterstützt sein
oder
- klar als nicht unterstützt / späterer Scope dokumentiert sein

## Nicht-Ziele
- Keine Implementierung.
- Keine Codeänderung.
- Keine Entscheidung.
- Kein Performance-Versprechen.
- Keine Produktionsreife-Behauptung.

## Nächster Schritt nach diesem Dokument
Die HAProxy-Dokumentation und/oder kleine externe Proofs gegen diesen
Fragebogen prüfen und die Antworten dokumentieren.
