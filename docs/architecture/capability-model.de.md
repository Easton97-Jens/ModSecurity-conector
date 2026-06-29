# Fähigkeitsmodell

**Sprache:** [English](capability-model.md) | Deutsch

Fähigkeiten beschreiben, was ein YAML-Fall ausführt. Es handelt sich nicht um Evidencetiketten
automatische Sprünge. Eine Fähigkeit gilt nur dann als verifiziert, wenn es sich um einen echten Connector handelt
case erzeugt vollständige RuntimeEvidence über Apache, NGINX oder HAProxy.

Fähigkeitsmetadaten allein sind kein Connector-Evidence. Nur API smoked,
Nur zugeordnete Inventareinträge, frühere Tests auf erwartete Fehler, blockierte Fälle und generierte Einträge
Coverage-Zeilen fügen keine verifizierten Variablen hinzu.

Der Connector-Evidencevertrag ist in definiert
[connector contract](connector-contract.de.md). Dieser Vertrag besitzt den Lebenszyklus,
Erforderliche Runtimeartefakte, normalisiertes Entscheidungsmodell und Regeln für den Evidenceumfang
für die produktiven Anschlüsse.

## Fähigkeitsanspruchsebenen

Die Fähigkeitssprache muss präzise sein:

| Anspruchsebene | Bedeutung |
| --- | --- |
| `supported` | Abgedeckt durch vollständige Connector-Runtimenachweise für den genannten Bereich. |
| `bounded` | Nur innerhalb der dokumentierten Grenzen implementiert oder beobachtbar. |
| `evidence-scoped` | Gilt für die zitierten gezielten, Full-Matrix- oder nativen Evidence, aber nicht für eine weitgefasste Behauptung. |
| `not-promoted` | Beobachtetes oder geplantes Verhalten, das ohne weitere Evidence nicht zur offiziellen Unterstützung werden darf. |
| `diagnostic-only` | Nützliche Setup- oder fehlende Runtimenachweise, die nicht als Runtime-PASS gelten können. |

Nur `supported`-Ansprüche, die durch neue Full-Matrix-Evidence gestützt werden, können sich auf Beamte auswirken
Runtime zählt. Gezielte Evidence können eine Lösung rechtfertigen, native Evidence können erklären
Semantik und rein diagnostische Evidence können die lokale Einrichtung erklären, aber nichts davon
Diese Bereiche ersetzen eine Connector-Matrix.

## Zusammenfassung der Funktionen des produktiven Connectors

| Fähigkeit | Apache | NGINX | HAProxy | Evidencegrundlage |
| --- | --- | --- | --- | --- |
| Anfragesperre | unterstützt | unterstützt | unterstützt | Verifizierte Runtimematrix und gezielter `verified-case`-Nachweis, wenn `result.json` und Protokolle vorhanden sind. |
| Anfragetext | für abgedeckte Fälle unterstützt | für abgedeckte Fälle unterstützt | begrenzt für abgedeckte SPOE/SPOP-Fälle | Vollmatrix-Reihen plus Verbindungskabelbaum-Artefakte. |
| XML-Body-Prozessor | evidenzbasiert | evidenzbasiert | evidenzbasiert | XML-Fälle und native/libmodsecurity-Vergleiche; Fördern Sie semantische Kanten nicht ohne Evidence. |
| JSON-Body-Prozessor | evidenzbasiert | evidenzbasiert | evidenzbasiert | JSON/raw-body-Fälle, die vollständige Runtimeartefakte erzeugen. |
| mehrteilig | begrenzt | begrenzt | begrenzt | Verbleibende mehrteilige Überprüfungsarbeiten dürfen nicht durch Bearbeitungen mit dem Status „Erwartet“ verdeckt werden. |
| Response Bodyübereinstimmung | begrenzt | unterstützt für beobachtete match/audit-Evidence | begrenzt | Phase-4-Berichte und Connector-Protokolle; ÜbereinstimmungsEvidence sind nicht dasselbe wie Durchsetzung. |
| Durchsetzung der Reaktionsstelle | ohne Abtreibungsnachweis nicht befördert | begrenzt durch `nginx_phase4_response_body_enforcement_gap` | begrenzt und nicht breit gefördert | Vollständige Matrixklassifizierungen plus gezielte Nachweisanforderungen der Phase 4. |
| Audit-Protokoll | unterstützt, in einigen Fällen mit weniger strukturierten Regeldetails | unterstützt für abgedeckte Prüfungsnachweise | unterstützt mit audit plus `decision.jsonl` | Audit/log meldet und kopierte Runtimeartefakte. |
| CRS | evidenzbasiert | evidenzbasiert | evidenzbasiert | Nur Vollmatrix-CRS-Varianten; gezielte Fälle bedeuten keine breite CRS-Unterstützung. |
| MRTS | evidenzbasiert | evidenzbasiert | evidenzbasiert | Vollmatrix-MRTS-Varianten und generierte Overlay-Klassifizierungen. |
| DetectionOnly-Overlay | als Klassifizierung unterstützt | als Klassifizierung unterstützt | als Klassifizierung unterstützt | `with_mrts_detection_only_overlay` und verwandte DetectionOnly-Klassifizierungen. |
| verifizierter Fall | wird nur mit vollständigen Artefakten unterstützt | wird nur mit vollständigen Artefakten unterstützt | wird nur mit vollständigen Artefakten unterstützt | `result.json`, `case-run.*` und kopierte Protokolle unter `VERIFIED_RUN_ROOT`. |
| Vollmatrix | nur durch generierte MatrixEvidence gestützt | nur durch generierte MatrixEvidence gestützt | nur durch generierte MatrixEvidence gestützt | Vervollständigen Sie `job.json`, Zusammenfassungen, Protokolle und generierte Berichtseingaben. |
| Native Oracle-Relevanz | evidenzbezogen, kein Ersatz | evidenzbezogen, kein Ersatz | evidenzbezogen, kein Ersatz | Native Evidence können die Semantik erklären; Es ersetzt niemals den ConnectorEvidence. |

Die Tabelle ist bewusst konservativ gehalten. Eine Zeile mit der Bezeichnung `bounded` oder
`evidence-scoped` ist keine Aufforderung, Tests zu überspringen oder Erwartungen neu zu schreiben. Es ist
eine Erinnerung daran, dass die Fähigkeitsunterstützung zusammen mit den Evidencen gelesen werden muss
Umfang.

## Bekannte Leistungsgrenzen

- Apache ist referenznah und verfügt über eine starke request/request-body-Abdeckung, aber
Die Details der Audit-Log-Regeln sind nicht immer so strukturiert wie bei HAProxy oder NGINX
EntscheidungsEvidence.
– NGINX kann verspätete Phase-4-Reaktionskörper-match/audit-Evidence liefern
Die störende Durchsetzung kann als HTTP `200` für den Client sichtbar bleiben. generiert
Berichte klassifizieren dies als `nginx_phase4_response_body_enforcement_gap`.
- Der primäre strukturierte Evidence von HAProxy ist `decision.jsonl`; `rule_id=0` bedeutet
keine Übereinstimmung, `decision=pass` bedeutet kein Block und `decision=deny` mit
`intervention_status` ist ein BlockEvidence.
- MRTS `with-mrts` kann `ctl:ruleEngine=DetectionOnly` setzen, also nicht blockierend
Störende Zeilen werden eher als `with_mrts_detection_only_overlay` klassifiziert
als Connectorfehler.
- `missing_result` dient immer nur der Diagnose, es sei denn, es handelt sich um einen echten Runtime-`result.json`
existiert für denselben Falllauf.

## Aktive Fähigkeitsnamen

| Fähigkeit | Bedeutung | Verifizierte Variablenzuordnung |
| --- | --- | --- |
| `multipart` | Deterministische multipart/form-data-Requestsgenerierung | keines für sich |
| `files` | `FILES_*` mehrteilige Sammlungen | `FILES` |
| `xml` | Verhalten des XML-Body-Prozessors und der XML-Sammlung | `XML` |
| `json` | JSON- oder unformatiertes JSON-Requestskörperverhalten | `REQUEST_BODY` |
| `response-body` | Verhalten des Response Bodys access/pass-through | nicht `RESPONSE_BODY`, bis die Blockierung vorüber ist |
| `audit-log` | Stabile Audit-Log-Felder werden bestätigt | `AUDIT_LOG` |
| `audit-log-absent` | Erwartete Abwesenheit des Audit-Protokolls; Wird derzeit nur für das frühere expected-failure/probes verwendet | keiner |
| `collections` | Verhalten der ModSecurity-Sammlung | keines für sich |
| `request-cookies` | Cookie-value/name-Sammlungen | `REQUEST_COOKIES` |
| `args-names` | Sammlung von Argumentnamen | `ARGS_NAMES` |
| `request-uri` | Rohe Requests-URI-Variable | `REQUEST_URI` |
| `response-headers` | Verhalten des Antwortheaders phase/filter | `RESPONSE_HEADERS` |
| `request-headers` | Fordern Sie Header-Werte oder -Namen an | `REQUEST_HEADERS` |
| `request-body` | Körperzugriff anfordern | `REQUEST_BODY` |
| `query-args` / `form-urlencoded` | Abfrage- oder URL-codierte Textargumente | `ARGS` |

`RESPONSE_BODY` wird in `verified_variables` währenddessen absichtlich nicht ausgegeben
`response_body_basic_block` bleibt der ehemalige expected-failure/mapped-only.

## Sammlungssemantikentscheidungen

`ARGS_NAMES` wird durch aktive Kontrollfälle überprüft, z
`v3_args_names_get_block`, wohin eine normale, durch kaufmännische Und-Zeichen getrennte Abfrage gelangt
libmodsecurity und erzeugt einen störenden Eingriff durch das Reale
Verbindungspfad.

Semikolon-Abfragetrennzeichenproben werden separat verfolgt. Wenn Apache, NGINX,
und HAProxy führen alle die Semikolon-Sammelprüfungen mit den erwarteten `403` und aus
tatsächliches `200`, während der Kontrollfall `ARGS_NAMES` im No-MRTS durchläuft
Varianten, die Nichtübereinstimmung wird klassifiziert als
`libmodsecurity_collection_semantics`. Diese Klassifizierung ist nur berichtspflichtig: it
ändert weder die YAML-Erwartungen noch die PASS/FAIL-Werte und zählt nicht als solche
eine konnektorspezifische Runtimeregression, es sei denn, neue Erkenntnisse weisen auf einen Connector hin
weicht vom gemeinsamen libmodsecurity-Verhalten ab.

## Validierungsregeln

YAML-Fälle können Funktionen als Liste oder als Zuordnung boolescher Werte ausdrücken.
Unterstrich-Aliase wie `request_body` werden zu Bindestrichnamen wie z. B. normalisiert
`request-body`. Unbekannte Funktionsnamen können nicht materialisiert werden.

Fähigkeiten entscheiden nicht darüber, ob ein Fall aktiv ist. Entdeckung ist Weg und
Statusbasiert:

- `modules/ModSecurity-test-Framework/tests/cases/minimal`, `imported`, `v2-imported` und `v3-imported`
sind aktive gemeinsame Bereiche.
– `modules/ModSecurity-test-Framework/tests/cases/former expected-failure` ist von der normalen Erkennung ausgeschlossen und muss es sein
explizit mit `SMOKE_CASES` ausgewählt.
- Connectorspezifische Fälle sind nur für den entsprechenden Connector aktiv.

## Zusammenfassende Darstellung

Connector-Zusammenfassungen legen allgemeine Metadaten nach Namen offen, nicht nach C/Python FFI. Der
Kabelbäume verwenden weiterhin Shell und Python, aber ihre JSON-Datensätze deklarieren Folgendes:

- `status_model: "msconnector_status"`
- `origin_model: "msconnector_origin"`
- `intervention_model: "msconnector_intervention"`

Dadurch wird die Evidenceform bei Beibehaltung mit den C-First-Headern ausgerichtet
die Runtimeumgebung unabhängig vom kompilierten Adaptercode.

`common/src/capabilities.c` bietet C-First-Deskriptor-Helfer für die Zukunft
Connectorcode. Die aktiven Python/Shell-Läufer spiegeln dieselben Metadatennamen wider
ohne FFI.

## Neue Connector-Fähigkeitsansprüche

Zukünftige Connectoren müssen den Lebenszyklus- und Nachweisregeln in folgen
[new connector onboarding](new-connector-onboarding.de.md) vor dem Hinzufügen der Funktion
Ansprüche. Ein Skelett- oder Roadmap-Only-Connector kann beabsichtigte Funktionen beschreiben,
aber diese Beschreibungen sind keine verifizierten Variablen, Runtimeunterstützung, CRS-Unterstützung,
oder Full-Matrix-Abdeckung. Die Funktionsunterstützung beginnt erst, wenn eine angestrebte Runtime erreicht ist
Fall produziert `result.json` plus logs/evidence und Produktionsfähigkeitsstatus
erfordert Full-Matrix-Evidence.
