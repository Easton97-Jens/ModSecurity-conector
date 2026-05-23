# TODO - Neuer Connector auf Basis des Templates

Status: teilweise geeignet

Template-Bewertung: teilweise geeignet

Begründung: Die Grundstruktur, vorsichtige Warnungen und Planungsdokumente
sind im Template vorhanden. Das Template ist aber nur teilweise geeignet, weil
konkrete Herkunfts-/Metadatenfelder, Build-Nachweise und Runtime-Nachweise
nicht im Template selbst belegt sind. Der lokale `tests`-Ordner wurde entfernt;
ausführbare Template-Tests werden nicht connector-lokal gepflegt.

Legende:

- [x] erledigt / durch Template-Dateien belegt
- [ ] offen / fuer konkrete Connectoren noch zu klaeren
- [ ] blockiert / ohne konkrete Quellen, Build-Artefakte oder Runtime-Setup
      nicht pruefbar
- [ ] nicht verifiziert / keine ausreichende Repo-Evidenz gefunden

Status-Vokabular:

- `template`: generische Vorlage, keine Implementierung.
- `scaffolded`: Struktur vorhanden, keine belegte Adapter-Implementierung.
- `adapter-owned`: produktiver Connector-Code liegt im Connector-Baum mit
  Herkunft und Metadaten.
- `runtime-smoke-verified`: nur konkret gelaufene Smoke-Fälle mit Command und
  Ergebnis.
- `partial`: Struktur oder Teilruntime ist belegt, aber keine vollständige
  Verifikation.
- `not-verified`: keine ausreichende Runtime-Evidenz.

## 1) Template-Grundstruktur

- [x] Status: erledigt - `README.md` vorhanden.
- [x] Status: erledigt - `TODO.md` vorhanden.
- [x] Status: erledigt - `docs/architecture.md` vorhanden.
- [x] Status: erledigt - `docs/build.md` vorhanden.
- [x] Status: erledigt - `docs/validation.md` vorhanden.
- [x] Status: erledigt - `harness/README.md` vorhanden.
- [x] Status: erledigt - `src/README.md` vorhanden.
- [x] Status: erledigt - Lokaler Template-Tests-Ordner wurde entfernt.
- [x] Status: erledigt - Template warnt, dass es keine produktive
      Implementierung ist.

## 2) Template-Eignung

- [x] Status: erledigt - Grundstruktur fuer neue Connector-Verzeichnisse ist
      beschrieben.
- [x] Status: erledigt - Architektur-, Build-, Harness-, Source- und
      Testbereiche werden als Planungsbereiche benannt.
- [x] Status: erledigt - `docs/validation.md` stellt klar, dass Strukturchecks
      keine Runtime-Evidenz ersetzen.
- [x] Status: erledigt - Das Template enthaelt keinen lokalen Testordner mehr.
- [x] Status: erledigt - Neue Connectoren duerfen keinen lokalen
      `connectors/<name>/tests`-Ordner anlegen.
- [x] Status: erledigt - Externe Framework-Testpfade sind im Repository
      belegt: `modules/ModSecurity-test-Framework/tests/cases/`,
      `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`
      und `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`.
- [ ] Status: offen - `ORIGIN.md`/Lizenz- und Herkunftsangaben muessen fuer
      konkrete Connectoren separat belegt werden.
- [ ] Status: offen - Metadaten-Dateien (`metadata.*`) muessen fuer konkrete
      Connectoren separat belegt werden.
- [ ] Status: teilweise - Das Template ist als vorsichtiger Scaffold geeignet,
      aber nicht als vollstaendige Connector-Implementierungsgrundlage ohne
      weitere Repo-spezifische Bewertung.

## 3) Server-spezifische Runtime-Fragen

- [ ] Status: offen - Welche Hook-/Filter-/Middleware-Punkte stellt der
      Zielserver bereit?
- [ ] Status: offen - Wie wird Request-Body verfuegbar gemacht
      (Buffering/Streaming)?
- [ ] Status: offen - Wie wird Response-Body verfuegbar gemacht, falls
      ueberhaupt?
- [ ] Status: offen - Wie werden ModSecurity-Interventions korrekt in
      Server-Aktionen gemappt?
- [ ] Status: offen - Wie werden Transaktions-IDs serverkonform
      erzeugt/uebernommen?
- [ ] Status: offen - Welche Header-/Body-Normalisierungen sind serverbedingt
      anders?
- [ ] Status: nicht verifiziert - RESPONSE_BODY blocking ist durch das
      Template nicht verifiziert. Benötigt werden belegbarer Runtime-Testcase,
      blockierender Response-Body-Trigger, tatsächliches blockierendes Ergebnis
      wie HTTP 403, Log-/Report-Evidence, ausgeführter Command und betroffener
      Connector.

## 4) Build-Fragen

- [ ] Status: offen - Benötigt der Server eigenes Build-System, zum Beispiel
      Module-API oder Plugin-SDK?
- [ ] Status: offen - Wie werden Build-Artefakte unter `BUILD_ROOT` isoliert?
- [ ] Status: offen - Welche Toolchain-/Dependency-Versionen sind
      Mindestvoraussetzung?
- [ ] Status: offen - Wie werden reproduzierbare lokale Builds dokumentiert?
- [ ] Status: offen - Welche Makefile-Targets muessen ergaenzt werden?
- [ ] Status: blockiert - Build-Verifikation fuer einen neuen Connector ist
      ohne konkrete Connector-Quellen und Abhaengigkeiten nicht pruefbar.

## 5) Test-Fragen

- [ ] Status: offen - Gibt es einen lauffaehigen Start/Stop-Smoke fuer den
      echten Serverprozess?
- [ ] Status: offen - Koennen YAML-Faelle ueber eine reale HTTP-Kette
      ausgefuehrt werden?
- [ ] Status: offen - Sind Interventionen (Allow/Block) nachweisbar?
- [ ] Status: offen - Sind Log-Artefakte (server/connector/audit/access)
      auswertbar?
- [ ] Status: offen - Wird ein kompatibler Summary-Report erzeugt?
- [x] Status: erledigt - Der lokale Template-Tests-Ordner wurde entfernt.
- [x] Status: erledigt - Ausfuehrbare Connector-Tests werden nicht
      connector-lokal gepflegt; neue Connectoren referenzieren die externen
      Framework-Pfade.
- [ ] Status: offen - Fuer einen konkreten neuen Connector muss der passende
      `smoke-<name>` oder ein dokumentierter Runtime-Command belegt werden.
- [ ] Status: offen - Mehr als `partial` ist erst nach dokumentierter
      Mindestmatrix belegbar: `phase1_header_block`, Request-Body blocking,
      Response-Header blocking falls vom Framework unterstuetzt, Response-Body
      blocking, Audit-/Log-Evidence, Startup/Reload-Validation und
      Negative/Pass-through-Fall.
- [x] Status: erledigt - Coverage decision matrix reviewed.
- [ ] Status: nicht verifiziert - Phase 1 runtime evidence documented.
- [ ] Status: nicht verifiziert - Phase 2 request-body runtime evidence
      documented.
- [ ] Status: nicht verifiziert - Phase 3 response-header runtime evidence
      documented.
- [ ] Status: nicht verifiziert - Phase 4 response-body runtime evidence
      documented.
- [ ] Status: nicht verifiziert - RESPONSE_BODY blocking verified.
- [ ] Status: nicht verifiziert - Audit/log evidence documented.
- [ ] Status: nicht verifiziert - Negative/pass-through case documented.
- [x] Status: teilweise - Connector status remains `partial` until matrix is
      complete.

## 6) Risiken

- [ ] Status: offen - Risiko: Struktur wird mit Funktionsfaehigkeit
      verwechselt.
- [ ] Status: offen - Risiko: Runtime-Code aus Apache/NGINX wird unkritisch
      kopiert.
- [ ] Status: offen - Risiko: Connector-spezifische Semantik
      (Hooks/Filter) wird unterschaetzt.
- [ ] Status: offen - Risiko: CI-Strukturchecks werden als Runtime-Nachweis
      fehlgedeutet.
- [ ] Status: nicht verifiziert - Risiko: RESPONSE_BODY-/Phase-4-Verhalten
      wird ohne Evidenz behauptet.

## 7) Scaffold-Entscheidungen

Die verbindlichen Scaffold-Entscheidungen fuer neue Connectoren stehen in:

```text
reports/template-verification-nginx-apache/connector-scaffold-decisions.md
```

## 8) Vollstaendige Bewertung

Die vollstaendige Template-Bewertung steht in:

```text
reports/template-verification-nginx-apache/template-evaluation.md
```
