> Status: Historisch
> Ersetzt durch: [../../current/six-connector-core-completion.de.md](../../current/six-connector-core-completion.de.md)
> Datum: Als historischer Bericht bei der Repository-Reorganisation am 2026-07-12 beibehalten
> Evidenzgrenze: Historische Planung, Bewertung oder Momentaufnahme; keine aktuelle kanonische Evidence.

# Vorlagenbewertung

**Sprache:** [English](template-evaluation.md) | Deutsch

Status: überprüft

Vorlagenstatus: geeignetes Gerüst, nicht laufzeitverifiziert

`connectors/_template` wird als Gerüst für zukünftige Konnektoren bewertet, nicht als
ein fertiger Connector. Es enthält absichtlich keine produktive Adapterquelle,
keine lokal ausführbare Testsuite und kein Laufzeitanspruch. Runtime-Nachweise gehören dazu
an konkreten Connectors und müssen mit Befehlen, Zählungen, Summary-JSON, aufgezeichnet werden
Protokolle und fallbezogener expected/actual-Status.

## Urteil

- [x] Als Verbindungsgerüst geeignet.
- [x] Erhebt keinen Anspruch auf Apache, NGINX, HAProxy oder ein anderes Laufzeitverhalten.
- [x] Dokumentiert, dass ausführbare Tests Eigentum des Frameworks sind.
- [x] Hält `connectors/_template/tests` fern.
- [x] Definiert Pro-Connector-Gates für Ursprung, Metadaten, Build, No-CRS,
  With-CRS, Abdeckungsmatrix, RESPONSE_BODY und Promotion.
- [ ] Laufzeit überprüft: nicht anwendbar auf die Vorlage.
- [ ] Build überprüft: nicht anwendbar auf die Vorlage.
- [ ] RESPONSE_BODY überprüft: nicht anwendbar auf die Vorlage.

## Checklisten-Nachweise

| Area | Result | Evidence | Notes |
| --- | --- | --- | --- |
| README | [x] Present | `connectors/_template/README.md` | Describes purpose, required files, non-claims, and per-connector evidence. |
| TODO | [x] Present | `connectors/_template/TODO.md` | Phase checklist exists for future connector work. |
| Architecture docs | [x] Present | `connectors/_template/docs/architecture.md` | Requires connector-specific architecture proof. |
| Build docs | [x] Present | `connectors/_template/docs/build.md` | Treats build evidence as per-connector. |
| Validation docs | [x] Present | `connectors/_template/docs/validation.md` | Requires executed runtime commands and result files. |
| Coverage matrix docs | [x] Present | `connectors/_template/docs/coverage-decision-matrix.md` | Separates framework coverage from runtime verification. |
| Harness contract | [x] Present | `connectors/_template/harness/README.md` | Harness implementation remains per-connector. |
| Source placeholder | [x] Present | `connectors/_template/src/README.md` | No productive source claim. |
| Local tests folder | [x] Absent | `test ! -d connectors/_template/tests` | Executable tests stay in `modules/ModSecurity-test-Framework/tests/cases/`. |
| Runtime proof | [ ] Not applicable | This report | A Template cannot be runtime-verified. |

## Phasenmatrix

| Phase | Gate | Template status | Promotion meaning |
| --- | --- | --- | --- |
| Phase 0 | Scaffold files | [x] Complete | Suitable scaffold. |
| Phase 1 | Origin/license | [ ] Per-connector gate | Future connector must provide `ORIGIN.md` and provenance. |
| Phase 2 | Metadata | [ ] Per-connector gate | Future connector must provide metadata in the repo's expected form. |
| Phase 3 | Build | [ ] Per-connector gate | Future connector must provide command, result, artifact, and log path. |
| Phase 4 | Harness | [ ] Per-connector gate | Future connector must implement the harness contract. |
| Phase 5 | No-CRS runtime | [ ] Per-connector gate | No-CRS evidence cannot be inherited from the Template. |
| Phase 6 | With-CRS runtime | [ ] Per-connector gate | CRS evidence must be scoped to executed With-CRS cases. |
| Phase 7 | Coverage matrix | [x] Scaffold rule | Matrix shape is documented; rows must be filled by each connector. |
| Phase 8 | RESPONSE_BODY | [ ] Runtime promotion gate | Blocking RESPONSE_BODY evidence is required before any verified claim. |
| Phase 9 | Negative/pass-through | [ ] Per-connector gate | Required before promotion beyond partial. |
| Phase 10 | Audit/log | [ ] Per-connector gate | Required before promotion beyond partial. |
| Phase 11 | More than partial | [ ] Blocked by design | Requires a concrete connector and complete runtime evidence. |

## Keine Ansprüche

- Die Vorlage ist kein Apache, NGINX, HAProxy, Envoy, lighttpd oder Traefik
Laufzeitimplementierung.
- Generierte Abdeckungsberichte sind planning/reporting Hilfsmittel, kein Laufzeitnachweis.
- Ein PASS für einen konkreten Konnektor wird nicht in die Vorlage oder auf einen übertragen
  anderer Connector.
- Die Vorlage beansprucht keine RESPONSE_BODY-Blockierungsunterstützung.
- Es ist kein lokales `connectors/_template/tests`-Verzeichnis erforderlich oder zulässig
  ausführbare Fälle.

## Pro-Connector-Gates

konkrete Connectors müssen Folgendes bieten:

- [ ] `ORIGIN.md`, Lizenz, Quellzuordnung, importierte Dateien und lokale Änderungen.
- [ ] Metadatenquelle oder das entsprechende Metadatenformular des Repositorys.
- [ ] Build-Befehl, Exit-Status, Artefaktpfad, include/library-Pfade und Protokoll.
- [ ] Harness-Befehl und Summary-JSON Pfad.
- [ ] No-CRS- und With-CRS-Ergebnisse separat dokumentiert.
- [ ] PASS/FAIL/BLOCKED/NOT_EXECUTABLE zählt pro Fall, wenn eine Matrix ausgeführt wird.
- [ ] Die CRS-Überprüfung gilt nur für ausgeführte CRS-Fälle.
- [ ] RESPONSE_BODY Sperren von Nachweisen vor verifizierten RESPONSE_BODY Ansprüchen.
- [ ] Negative/pass-through und audit/log Nachweis vor Promotion darüber hinaus
  teilweise.

## Entscheidung

Das Template eignet sich als Gerüst und bleibt nicht laufzeitverifiziert. Fehlt
Ursprung, Metadaten, Build, No-CRS, With-CRS, RESPONSE_BODY, audit/log und Laufzeit
Nachweise sind Pro-Connector-Gates, keine Template-Defekte.
