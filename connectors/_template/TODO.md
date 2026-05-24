# TODO – Neuer Connector auf Basis des Templates

Status: scaffolded

## 1) Grundstruktur

- [ ] Verzeichnis nach `connectors/<name>/` kopieren.
- [ ] Connector-spezifische `README.md` mit **keinen** unbelegten Claims ergänzen.
- [ ] `ORIGIN.md`/Lizenz- und Herkunftsangaben anlegen (noch zu prüfen).
- [ ] Metadaten-Dateien (`metadata.*`) nur mit belegten Feldern ergänzen (noch zu prüfen).

## 2) Server-spezifische Runtime-Fragen (noch zu prüfen)

- [ ] Welche Hook-/Filter-/Middleware-Punkte stellt der Zielserver bereit?
- [ ] Wie wird Request-Body verfügbar gemacht (Buffering/Streaming)?
- [ ] Wie wird Response-Body verfügbar gemacht (falls überhaupt)?
- [ ] Wie werden ModSecurity-Interventions korrekt in Server-Aktionen gemappt?
- [ ] Wie werden Transaktions-IDs serverkonform erzeugt/übernommen?
- [ ] Welche Header-/Body-Normalisierungen sind serverbedingt anders?

## 3) Build-Fragen (noch zu prüfen)

- [ ] Benötigt der Server eigenes Build-System (z. B. Module-API, Plugin-SDK)?
- [ ] Wie werden Build-Artefakte unter `BUILD_ROOT` isoliert?
- [ ] Welche Toolchain-/Dependency-Versionen sind Mindestvoraussetzung?
- [ ] Wie werden reproduzierbare lokale Builds dokumentiert?
- [ ] Welche Makefile-Targets müssen ergänzt werden?

## 4) Test-Fragen (noch zu prüfen)

- [ ] Gibt es einen lauffähigen Start/Stop-Smoke für den echten Serverprozess?
- [ ] Können YAML-Fälle über eine reale HTTP-Kette ausgeführt werden?
- [ ] Sind Interventionen (Allow/Block) nachweisbar?
- [ ] Sind Log-Artefakte (server/connector/audit/access) auswertbar?
- [ ] Wird ein kompatibler Summary-Report erzeugt?

## 5) Offene Risiken

- [ ] Risiko: Struktur wird mit Funktionsfähigkeit verwechselt.
- [ ] Risiko: Runtime-Code aus Apache/NGINX wird unkritisch kopiert.
- [ ] Risiko: Connector-spezifische Semantik (Hooks/Filter) wird unterschätzt.
- [ ] Risiko: CI-Strukturchecks werden als Runtime-Nachweis fehlgedeutet.
- [ ] Risiko: RESPONSE_BODY-/Phase-4-Verhalten wird ohne Evidenz behauptet.
