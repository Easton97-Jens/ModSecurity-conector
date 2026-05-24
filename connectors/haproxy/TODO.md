# HAProxy Connector TODO

Status: scaffolded

Alle Punkte in diesem Dokument sind **noch zu prüfen**, sofern nicht separat
mit Runtime-/Build-Evidenz im Repository belegt.

## Integrationsstrategie (noch zu prüfen)

- [ ] Welche Integrationsstrategie wird verwendet?
- [ ] SPOE?
- [ ] Native HAProxy-Filter?
- [ ] Lua?
- [ ] Externer Service?
- [ ] Anderer Ansatz?
- [ ] Welche Entscheidungskriterien gelten (Sicherheit, Performance,
      Wartbarkeit, Betrieb)?

## Request-/Response-Pfad (noch zu prüfen)

- [ ] Wie werden Requests an die Connector-Komponente übergeben?
- [ ] Welche Header-/Body-Daten sind in welcher Phase verfügbar?
- [ ] Wie werden Response Headers behandelt?
- [ ] Wie werden Response Bodies behandelt?
- [ ] Wie werden Streaming- und Buffering-Grenzen umgesetzt?

## Intervention und Action-Mapping (noch zu prüfen)

- [ ] Wie werden ModSecurity-Interventions auf HAProxy-Actions gemappt?
- [ ] Welche Block-/Allow-Semantik ist technisch sauber abbildbar?
- [ ] Wie werden Fehlerpfade (z. B. Connector nicht erreichbar) behandelt?

## Logging und Nachweis (noch zu prüfen)

- [ ] Welche Logs gelten als Mindestnachweis (HAProxy/Connector/Audit)?
- [ ] Wie wird die Korrelation zwischen Request, Entscheidung und Log sichergestellt?
- [ ] Wie wird Logging-Validierung automatisiert?

## Build und Betrieb (noch zu prüfen)

- [ ] Wird ein kompilierter Bestandteil benötigt?
- [ ] Wird ein SPOA-Agent gebaut?
- [ ] Welche Laufzeitumgebung ist erforderlich?
- [ ] Wie werden Build-/Runtime-Artefakte strikt unter `BUILD_ROOT` isoliert?
