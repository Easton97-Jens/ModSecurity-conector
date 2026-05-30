# HAProxy Integration Decision Record

## Kurzfazit
Es gibt mehrere plausible Optionen, aber keine ist ausreichend belegt.

## Vergleichstabelle
| Option | Repo-Belege | Vorteile | Risiken | Fehlende Informationen | Empfehlung |
|---|---|---|---|---|---|
| SPOE / SPOA-Agent | In `future-connectors.md` als erwartetes Modell erwähnt; im HAProxy-Scaffold als offene Option genannt. | Abgeleitet: passt zur Repo-Aussage „SPOE oder native extension“. | Buffering/Streaming, Response-Inspection und Fehlerpfade sind schwierig. | Protokoll-/Lifecycle-Details, Artefakte, Mapping-Regeln (Extern zu verifizieren). | Kandidat, aber noch nicht entscheidbar. |
| HAProxy Filter | In `future-connectors.md` als „native extension path“ indirekt genannt; im Scaffold als Option. | Abgeleitet: potenziell direkter Integrationspfad. | Hohe Kopplung an HAProxy-Lifecycle/API. | API-Stabilität, Hookpunkte, Build-Mechanik (Extern zu verifizieren). | Plausibel, aber unbelegt im Repo. |
| Lua-basierte Integration | Nur als offene Option im Scaffold. | Abgeleitet: könnte schnelleres Prototyping erlauben. | Leistungs-/Body-/Interventionseinschränkungen. | Machbarkeit mit libmodsecurity (Extern zu verifizieren). | Niedrige Belegstärke; nur explorativ. |
| Externer HTTP-Service / Sidecar | Im Scaffold als „Externer Service/Prüfservice“ genannt. | Abgeleitet: Prozessentkopplung. | Latenz, Fehlerpfade, Kontextkonsistenz. | Protokollvertrag, Action-Mapping, Betriebsmodell (Extern zu verifizieren). | Plausibel, aber nicht priorisierbar. |

## Belege aus dem Repository
- `connectors/haproxy/README.md`: HAProxy ist Scaffold, nicht implementiert/validiert/promoted.
- `connectors/haproxy/TODO.md`: Integrationsstrategie, Request/Response, Intervention-Mapping, Logging, Streaming/Buffering sind offen.
- `connectors/haproxy/docs/architecture.md`: Optionen sind offen, keine Entscheidung.
- `connectors/haproxy/docs/build.md`: Build-Fragen offen.
- `connectors/haproxy/docs/validation.md`: Mindestanforderungen für Runtime-Evidence.
- `docs/connectors/future-connectors.md`: HAProxy expected model „SPOE or native extension path“.
- `docs/architecture/connector-adapter-interface.md`: Required Hooks und Boundary-Regeln.
- `Makefile`: keine HAProxy smoke/build targets.
- `.github/workflows/test-haproxy.yml`: nur Strukturcheck.
- `reports/testing/test-coverage-overview.md`: Runtime-Snapshot bezieht sich auf Apache/NGINX, nicht HAProxy.

## Bewertung der Optionen

### 1. SPOE / SPOA-Agent
- Belegt im Repo: als expected model und TODO-Option erwähnt.
- Abgeleitet: Request-Prüfpfad über separate Connector-Komponente denkbar.
- Extern zu verifizieren: vollständige Request/Response/Body-Semantik, Mapping auf HAProxy-Actions.
- Nicht belegbar: exakter Artefakt-Satz im Build.
- Risiko: schwierige Buffering/Streaming- und Fehlerpfade.
- Empfehlung: technisch plausibler Kandidat, aber nicht entscheidungsreif.

### 2. HAProxy Filter
- Belegt im Repo: native extension path + Filteroption genannt.
- Abgeleitet: direkter Lifecycle-Zugriff möglich.
- Extern zu verifizieren: verfügbare Hookpunkte und Semantik.
- Nicht belegbar: konkrete Implementierbarkeit im aktuellen Repo.
- Risiko: hohe Kopplung an Serverinterna.
- Empfehlung: plausibel, ohne Zusatzbelege nicht vorziehbar.

### 3. Lua
- Belegt im Repo: als Option genannt.
- Abgeleitet: möglicher Prototypingpfad.
- Extern zu verifizieren: Leistungsfähigkeit für Body/Intervention.
- Nicht belegbar: ausreichende ModSecurity-Semantik.
- Risiko: unklare Feature-Abdeckung.
- Empfehlung: nur explorativ.

### 4. Externer HTTP-Service / Sidecar
- Belegt im Repo: als Option genannt.
- Abgeleitet: Entkopplung der Prozesse.
- Extern zu verifizieren: Protokolltreue, Latenz, Security, Fehlerpfade.
- Nicht belegbar: Eignung für vollständige ModSecurity-Semantik.
- Risiko: zusätzliche Betriebsabhängigkeiten.
- Empfehlung: plausibel, aber nicht priorisierbar.

## Empfohlener nächster Schritt
Einen einheitlichen evidenzbasierten Vergleichsfragebogen erstellen, der pro Option dieselben Nachweispunkte abfragt (Request, Response-Header, Response-Body, Intervention-Mapping, Build-Artefakte, Harness-Hooks, Minimaltests).

## Nicht beantwortbar aus dem aktuellen Repository
- Welche Option technisch/funktional überlegen ist.
- Konkrete Umsetzbarkeit von Response-Header-/Body-Inspection je Option.
- Vollständiges Intervention→HAProxy-Action-Mapping.
- Konkrete Build-Artefakte je Option.
- HAProxy-spezifische Hook-/Lifecycle-Garantien.
- Last-/Latenzverhalten der Optionen.
