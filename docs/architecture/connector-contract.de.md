# Connector-Vertrag

**Sprache:** [English](connector-contract.md) | Deutsch

Bei Connector-Implementierungen müssen die Evidence Gates erhalten bleiben
[new connector onboarding](new-connector-onboarding.de.md). Neue Connectoren beginnen als
Nur Roadmap-Kandidaten oder Skelette und werden erst danach zu Runtimekonnektoren
Echte Runtimeartefakte Evidencen das behauptete Verhalten.

Bei diesem Vertrag geht es bewusst um Evidence:

- Connector-neutraler Code bleibt in `common/`;
- Adaptereigener Code bleibt in `connectors/<name>/`;
- Generierte Berichte müssen von Generatoren erstellt und nicht manuell bearbeitet werden.
– Runtimeansprüche erfordern `result.json` plus logs/evidence;
- Full-Matrix-Ansprüche erfordern generierte Full-Matrix-Evidence;
- OpenResty wird von NGINX abgedeckt, es sei denn, eine zukünftige Entscheidung ändert dies ausdrücklich.

## Zweck

Der Connectorvertrag definiert die minimalen, connectorneutralen Pflichten für
die produktiven Apache-, NGINX- und HAProxy-Connectoren. Es ist auch die Grundlinie
für jeden zukünftigen Connector, bevor er von der Planung in die verifizierte Runtime übergehen kann
Evidence.

Der Vertrag hält vier Anliegen getrennt:

- Runtimeverhalten: was der Server, Proxy, Modul oder Sidecar tatsächlich getan hat;
- Evidence nutzen: die vom lokalen oder CI-Läufer geschriebenen Dateien;
- Berichtsklassifizierung: wie generierte Berichte bekannte Lücken beschreiben und
unkritische Grenzen;
- Bereitschaftsansprüche: ob zielgerichtete oder Full-Matrix-Evidence vollständig genug sind
um offizielle Zählungen zu beeinflussen.

Diese Trennung sorgt dafür, dass die Full-Matrix-Bereitschaft ehrlich bleibt. Ein Connector kann vorhanden sein
echte gezielte Evidence, ohne die offiziellen Runtimezählungen zu ändern. Ein Einheimischer
Oracle kann die Semantik von libmodsecurity klären, ohne die Connector-Matrix zu ersetzen
Evidence. Ein lokaler Diagnoserauch kann fehlende Runtimekomponenten aufdecken, ohne dass dies der Fall ist
ein PASS werden.

## Connector-Lebenszyklus

| Zustand | Mindestanforderungen | Erforderliche Artefakte | Zulässige Berichte | Unzulässige Ansprüche |
| --- | --- | --- | --- | --- |
| `skeleton` | Verzeichnis oder Starter vorhanden; Umfang, Quellbesitz und Nicht-Runtimestatus werden dokumentiert. | `README.md`, `ORIGIN.md` oder gleichwertige Herkunft, Metadaten oder Quellzuordnung, wenn Code vorhanden ist. | Nur-Roadmap-Dokumente oder generierte Roadmap-Einträge. | Runtime PASS/FAIL, Bereitschaft für verifizierte Fälle, Bereitschaft für die vollständige Matrix, Produktionsverifizierung. |
| `buildable` | Connectorkomponente, Modul oder Diagnosestarter werden reproduzierbar außerhalb der Kasse erstellt. | Build-Befehl, Build-Protokolle unter dem verifizierten runtime/build-Root, Hinweise zum Quellbesitz. | Build/readiness-Hinweise und Roadmap-Berichte, die kein Runtimeverhalten bestätigen. | Datenverkehrsabwicklung, Requestsblockierung, CRS-Unterstützung oder Funktionsunterstützung ohne Runtimeartefakte. |
| `runtime-startable` | Server/proxy/module/sidecar kann deterministisch in einem sicheren Runtimepfad starten und stoppen. | Minimale Runtimekonfiguration, start/stop-Skript oder Harness-Befehl, Prozessprotokolle, Bereinigungsnachweise. | Bereitschafts- und Diagnosestartberichte des Runtimeproduzenten. | Verifizierte Blockierung, Requestskörperunterstützung, Prüfverhalten oder CRS-Unterstützung ohne `result.json` und Protokolle. |
| `verified-case-ready` | Mindestens ein gezielter realer Runtimefall läuft über den Connector. | `result.json`, `case-run.json`, `case-run.md`, kopierte access/error/audit/decision-Protokolle unter `VERIFIED_RUN_ROOT`. | Gezielte Evidenz und diagnostisch erstellte Zusammenfassungen. | Breite Phasenabdeckung, offizielle Zähländerungen, Full-Matrix PASS, fusionsbereiter Beitrag. |
| `full-matrix-ready` | Alle connector/CRS/MRTS-Matrixjobs sind planbar und können vollständige Jobartefakte erzeugen. | Vervollständigen Sie `job.json`, summary/results JSONL, führen Sie Protokolle aus, erstellen Sie Manifeste und kopieren Sie Protokolle für jeden Matrixjob. | Vollständigkeits- und Nichtübereinstimmungsberichte mit vollständiger Matrix, die aus realen Eingaben generiert werden. | Zeitüberschreitungen, unvollständige Zeilen, leere Zusammenfassungen oder veraltete Berichte werden als neuer Abschluss behandelt. |
| `production-verified` | Die Pipeline für verifizierte Evidence ist vollständig und die Governance-Gates passieren ohne kritische Blocker. | Vollständig generierter Berichtssatz, Analyse kritischer Abweichungen, Dashboard für die Zusammenführungsbereitschaft, Nachweis der Systemumgebung. | Kritisch erstellte Berichte mit vollständigen Eingaben. | Jeder Produktionsanspruch, wenn Eingaben blockiert, veraltet, fehlend, manuell gepatcht oder aktualisiert werden müssen. |

Der Lebenszyklus ist nur dann monoton, wenn die Evidence aktuell sind. Ein Connector kann sich zurückbilden
von `full-matrix-ready` in einen Diagnosezustand, wenn erforderliche Eingänge fehlen,
veraltet, blockiert oder aus einem unsicheren Runtimepfad erstellt.

## Erforderliches Verzeichnislayout

Das Ziellayout für produktive und zukünftige Connectoren ist:

```text
connectors/<name>/
  README.md
  config/
  scripts/
  harness/
  logs/
  examples/
```

Der aktuelle produktive Connector-Baum entspricht nicht genau dieser Idealform.
und dieses Dokument gestattet nicht das Verschieben von Dateien nur aus kosmetischen Gründen
Layout:

| Connector | Aktuelles Layout | Vertragsdelta | Roadmap-Bereinigung |
| --- | --- | --- | --- |
| Apache | `README.md`, `build/`, `docs/`, `harness/`, `src/`, Autotools-Dateien. | Kein separates Verzeichnis `config/`, `scripts/`, `logs/` oder `examples/`. Runtimeprotokolle werden unter `VERIFIED_RUN_ROOT` kopiert und nicht im Checkout gespeichert. | Dokumentieren Sie jede zukünftige harness/config-Aufteilung, bevor Sie buildempfindliche Autotools-Dateien verschieben. |
| NGINX | `README.md`, `config`-Datei für dynamische Module auf Root-Ebene, `docs/`, `harness/`, `src/`. | `config` ist eine Build-Metadatendatei, kein `config/`-Verzeichnis. kein separates `scripts/`-, `logs/`- oder `examples/`-Verzeichnis. | Wenn Beispiele oder Runtimekonfigurationen später aufgeteilt werden, behalten Sie den Modul-`config`-Pfadvertrag und die Quellzuordnung bei. |
| HAProxy | `README.md`, `docs/`, `harness/`, `poc/`, `src/`. | Kein separates Verzeichnis `config/`, `scripts/`, `logs/` oder `examples/`. Beispiele und Diagnosen für SPOE/SPOP sind derzeit unter `docs/` und `poc/` dokumentiert. | Verschieben oder teilen Sie Beispiele nur, nachdem Sie die vorhandenen SPOA/SPOP-Evidencereferenzen stabil gehalten haben. |

Generierte Protokolle und Runtimeausgaben dürfen nicht unter dem Connector festgeschrieben werden
Verzeichnisse. Sie gehören unter `VERIFIED_RUN_ROOT`.

## Erforderliche Runtimeartefakte

Ein vollständig verifizierter Connector-Runtimefall muss mindestens Folgendes schreiben oder kopieren:

- `result.json`;
- Zugriffsprotokoll oder gleichwertiges Requestsprotokoll;
- Fehlerprotokoll oder gleichwertiges server/proxy-Diagnoseprotokoll;
- Audit-Log, sofern vom Connector und Gehäuse unterstützt;
- Entscheidungsstrom, wenn der Connector einen hat;
- `case-run.json`;
- `case-run.md`;
- Protokolle unter `VERIFIED_RUN_ROOT` kopiert.

`missing_result` ist eine nützliche Diagnose, aber kein vollständiger Runtimefehler.
Ein Fall ohne echte Runtime `result.json` muss als klassifiziert werden
`diagnostic_only_missing_runtime_components` oder der nächstgelegene Nur-Diagnose-Typ
Grund. Es darf niemals als Runtime PASS gezählt werden.

### HAProxy-Runtimeartefakte

HAProxy verfügt über einen zusätzlichen SPOE/SPOP-Evidencevertrag:

- `decision.jsonl` ist der primäre strukturierte Entscheidungsstrom;
- HAProxy-Protokolle und SPOA/SPOP-Protokolle müssen kopiert werden, sofern vorhanden;
- `intervention_status` zeichnet den ModSecurity-Eingriffsstatus auf;
- `decision=pass` bedeutet, dass die Anfrage nicht blockiert wurde;
- `decision=deny` plus `intervention_status` blockiert Evidence;
- `rule_id=0` bedeutet, dass keine Übereinstimmung mit den ModSecurity-Regeln festgestellt wurde.

### NGINX-Runtimeartefakte

Der NGINX-Runtimenachweis muss Folgendes umfassen:

- NGINX-Fehlerprotokoll;
- ModSecurity-Auditnachweise, wenn der Fall dies erwartet;
- Antwort-Körper-Übereinstimmungsnotizen der Phase 4, wenn der Fall Response Body ausübt.

NGINX kann im Spätherbst eine rule-match/audit-Erkennung des Reaktionskörpers zeigen
Die Durchsetzung des Response Bodys in Phase 4 bleibt begrenzt und kann den HTTP-Status verlassen
bei `200`.

### Apache-Runtimeartefakte

Der Apache-Runtimenachweis muss Folgendes umfassen:

- Apache-Fehlerprotokoll;
- ModSecurity-Audit-Protokoll, wenn erwartet;
- Hinweise für Fälle, in denen die Regelübereinstimmungsdetails weniger strukturiert sind als die
HAProxy/NGINX Entscheidungsströme.

Apache ist für dieses Repository referenznah, aber es ist kein automatisches Orakel
für jede semantische Kante von libmodsecurity.

## Normalisiertes Entscheidungsmodell

Jeder generierte Runtimebericht sollte konnektorspezifische Beobachtungen normalisieren
in die gleichen Felder:

| Feld | Bedeutung |
| --- | --- |
| `expected_status` | Vom Testfall erwarteter HTTP-Status. |
| `actual_status` | Von der Connector-Runtime beobachteter HTTP-Status. |
| `status` | Runtimeergebnis wie `PASS`, `FAIL`, `BLOCKED` oder `MISSING_RESULT`. |
| `rule_id` | Übereinstimmende ModSecurity-Regel-ID, sofern bekannt; Connectorspezifische Unbekannte müssen explizit bleiben. |
| `decision` | Normalisierte Entscheidung: `pass`, `deny` oder `unknown`. |
| `intervention_status` | ModSecurity-Eingriffsstatus, wenn der Connector ihn verfügbar macht. |
| `classification` | Generierte Berichtsklassifizierung für bekannte Lücken, Überlagerungen oder Semantik. |
| `critical` | Ob die Zeile die Zusammenführungsbereitschaft blockiert. |
| `evidence_scope` | Evidencequelle: `targeted`, `full-matrix`, `native` oder `diagnostic`. |

Connectorspezifische Felder können beibehalten werden, es müssen jedoch Berichtsentscheidungen getroffen werden
aus dem normalisierten Modell oben.

## Regeln zum Nachweisumfang

| Evidenceumfang | Definition | Kann die offizielle Runtimeanzahl geändert werden? |
| --- | --- | --- |
| `full-matrix evidence` | Vollständig generierte Evidence aus allen geplanten connector/CRS/MRTS-Matrixjobs, einschließlich vollständiger `job.json`- und Runtimezusammenfassungen. | Ja. |
| `targeted evidence` | Ein oder mehrere explizit ausgewählte verifizierte Fälle, die zum Evidence oder zur Widerlegung einer gezielten Lösung dienen. | Nein, außer als unterstützender Evidence für eine spätere Aktualisierung der Vollmatrix. |
| `native evidence` | Native ModSecurity, nativer Connector oder Vergleich im Oracle-Stil zum Verständnis der Semantik. | Nein. Es kann die Semantik erklären, ersetzt jedoch nicht den ConnectormatrixEvidence. |
| `diagnostic-only evidence` | Lokale Smoke-, Start- oder fehlende Runtimeausgabe, die bei der Diagnose des Setups hilft, aber keine vollständigen Runtimeartefakte enthält. | NEIN. |
| `stale evidence` | Evidence für alten Code, alte Framework-Eingaben oder veraltete Runtimeartefakte. | NEIN. |
| `refresh-needed evidence` | Hinweise, die `full_matrix_refresh_needed=true` nach realen Runtime- oder Eingabeänderungen anzeigen. | Nein, bis neue Full-Matrix-Evidence es wieder auf `false` zurückführen. |

Strenge Regeln:

- Nur Full-Matrix-Evidence können die offiziellen Runtimezählungen ändern.
- Gezielte Evidence können eine Korrektur rechtfertigen, führen sie aber nicht automatisch durch
offiziell erstellte Berichte grün;
- Native Evidence können semantische Erwartungen bestätigen, ersetzen jedoch nicht a
Connectormatrix;
- Nur diagnostische Evidence, einschließlich `missing_result`, dürfen niemals als solche gelten
Runtime PASS;
- `full_matrix_refresh_needed=true` darf nur durch einen echten Neudurchlauf gelöscht werden,
nicht durch Bearbeitung von Berichten oder Dokumentationen.

## Fähigkeitsgrenzmodell

### Apache

Apache ist der referenznahe Steuerungskonnektor in diesem Repository. Es hat stark
Requests- und Requestskörperabdeckung und unterstützt die Audit-Logierung für die abgedeckten Personen
Fälle. Seine bekannte Grenze ist die Evidenceform: Audit-Loge sind vorhanden, aber
Regelübereinstimmungsdetails sind nicht immer so strukturiert wie HAProxy `decision.jsonl` oder
Hinweise zu NGINX Phase 4. Apache darf nicht als perfektes Orakel für jedermann angepriesen werden
Semantischer Rand von libmodsecurity.

### NGINX

Die NGINX-Anfrageblockierung ist für die abgedeckten anfrageseitigen Fälle evidenzbasiert.
Das Verhalten des Requestshauptteils wird für die überprüften Fälle unterstützt. Response Body der Phase 4
Regelübereinstimmung kann durch audit/log-Evidence beobachtet werden.

Bei der begrenzten Lücke handelt es sich um eine verspätete, störende Phase-4-Durchsetzung der Reaktionsorgane: a
Die Response Bodyregel kann übereinstimmen, während der für den Client sichtbare HTTP-Status bestehen bleibt
`200`. Dies wird klassifiziert als:

```text
nginx_phase4_response_body_enforcement_gap
```

Möglicherweise sind noch Audit-Loge und Regelnachweise vorhanden. Die Lücke ist dabei unkritisch
es bleibt evidenzbasiert, generiert und wird nicht zu einer falschen Blockierung befördert
beanspruchen.

### HAProxy

HAProxy verwendet ein SPOE/SPOP-based-Modell. `decision.jsonl` ist die primäre Struktur
Evidencestrom und muss zusammen mit HAProxy-Protokollen, SPOA/SPOP-Protokollen und Audits gelesen werden
Protokolle und normalisiertes `result.json`.

Entscheidungssemantik:

- `rule_id=0` bedeutet keine Regelübereinstimmung;
- `decision=pass` bedeutet kein Block;
- `decision=deny` mit `intervention_status` ist BlockEvidence;
- Die Unterstützung durch die Reaktionsorgane ist begrenzt und darf ohne diese nicht breit gefördert werden
gezielte before/after-Evidence und Full-Matrix-Bestätigung.

### MRTS

MRTS ist ein connectorübergreifendes Overlay-Verhalten. Die Variante `with-mrts` kann Folgendes festlegen:

```text
ctl:ruleEngine=DetectionOnly
```

Wenn diese Überlagerung angewendet wird, werden störende Aktionen absichtlich nicht blockierend.
Die generierte Klassifizierung lautet:

```text
with_mrts_detection_only_overlay
```

Das ist kein Connector-Fehler. Es handelt sich um eine Berichtsklassifizierung für die ausgewählten
MRTS-Modus und darf nicht durch Änderungen des erwarteten Status behoben werden.

## Vollmatrix-Bereitschaftskriterien

Ein Connector ist nur dann für die vollständige Matrix geeignet, wenn alle folgenden Bedingungen zutreffen:

– Der Runtimestart ist in sicheren Runtimepfaden deterministisch.
- `verified-case` kann zumindest Diagnoseartefakte schreiben und Fälle abschließen
schreibe echtes `result.json`;
- Jeder geplante Full-Matrix-Job schreibt vollständige Artefakte.
- `job.json` ist für jeden Job vollständig;
- Kein Timeout wird als erneuter Abschluss gewertet.
- Protokolle werden unter `VERIFIED_RUN_ROOT` kopiert;
- Berichte werden aus realen Stromeingängen generiert;
- `check-generated-report-layout` besteht immer noch;
- Veraltete, blockierte, teilweise oder `missing_result`-Zeilen werden ehrlich klassifiziert.

Die Full-Matrix-Bereitschaft ist kein Anspruch auf Dokumentation. Es handelt sich um einen generierten Evidence
beanspruchen.

## Akzeptanzkriterien für neue Connectoren

Bevor ein neuer Connectoren in die Vollmatrix aufgenommen werden kann, muss er mindestens Folgendes nachweisen:

```text
build target exists
runtime start target exists
verified-case works
result.json produced
logs copied
request blocking smoke passes
request-body smoke evaluated
capability notes documented
```

Bevor echte Full-Matrix-Evidence vorliegen, sind die folgenden Behauptungen verboten:

```text
production_verified
full_matrix_ready
merge_ready
critical_free
```

Informationen zu zukünftigen Anschlüssen finden Sie unter [new connector onboarding](new-connector-onboarding.de.md)
Planungs- und Erstnachweisbeschränkungen.

## Zukünftig generierter Bericht

Ein zusammenfassender Bericht zur Connector-Fähigkeit kann später nützlich sein:

```text
reports/testing/generated/manifest/connector-capability-summary.generated.md
reports/testing/generated/manifest/connector-capability-summary.generated.json
```

Erstellen oder übertragen Sie diesen Bericht erst, wenn die Runtimeeingaben vollständig verifiziert sind
verfügbar und der Generator kann es aus dem aktuellen manifests/reports ohne ableiten
Blockieren der Berichtsgovernance. Wenn lokale Runtimekomponenten fehlen, behalten Sie diese bei
Befolgen Sie die hier dokumentierte Arbeit und schreiben Sie keinen blockierten generierten Bericht fest.

Der zukünftige Bericht sollte nur evidenzbasierte Fähigkeiten zusammenfassen:

| Connector | Sperrung anfordern | Requeststext | Response Body-Übereinstimmung | Durchsetzung der Reaktionsstelle | Audit-Protokoll | CRS | MRTS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Apache | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert |
| NGINX | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert |
| HAProxy | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert | aus Evidencen generiert |

## Kleine Roadmap zur Härtung

Zukünftige Verhärtungen sollten klein und evidenzbasiert bleiben:

1. Fügen Sie erst nach Abschluss eine Zusammenfassung der Generator-gestützten Connectorenfunktionen hinzu
RuntimeEvidence liegen vor.
2. Teilen Sie den Connector examples/configs nur, wenn dabei der vorhandene Build erhalten bleibt
und Kabelbäume.
3. Verbessern Sie die Extraktion von Apache-Regeldetails, ohne das Runtimeverhalten zu ändern.
4. Halten Sie die Durchsetzung der NGINX-Phase-4-Reaktionsstellen geheim, bis die Maßnahmen ergriffen werden
before/after-Evidence belegen eine echte Durchsetzungsänderung.
5. Halten Sie die HAProxy-Response-Body-Unterstützung begrenzt, bis `decision.jsonl`,
Intervention, Prüfung und HTTP-Evidence stimmen überein.
6. Bewerten Sie jeden neuen Connector-Kandidaten separat und überarbeiten Sie die drei nicht
produktive Connectoren, während die Evidenzbasis stabil ist.
