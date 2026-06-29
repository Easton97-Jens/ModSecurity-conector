# Reale Connector-Validierung

**Sprache:** [English](real-world-connector-validation.md) | Deutsch

Status: umgesetzt

`real-world-connector-path` bedeutet, dass das Smoke-Ergebnis von diesem Pfad stammt:

```text
HTTP client
  -> real Apache, NGINX, or HAProxy process
  -> real ModSecurity connector module or SPOA/SPOP integration path
  -> libmodsecurity
  -> rule variables
  -> real HTTP response
```

Dies unterscheidet sich von dem dokumentierten Connector-freien libmodsecurity API Smoke
unter
`modules/ModSecurity-test-Framework/docs/testing/v3-api-smoke-test.md`. Die API
Smoke beweist einen öffentlichen libmodsecurity C API Pfad, aber es beweist nicht, dass a
Der Server-Connector füllte dieselben Variablen, pufferte dieselben Körper und schrieb
dieselben Prüfartefakte ausgeführt oder dieselbe Hook-Phase ausgeführt haben.

## Warum das existiert

Direkte API-Tests prüfen kein Server- und Connector-Verhalten. Die
Der reale Connector-Pfad erkennt Probleme wie:

- Serverspezifische Normalisierung des Abfragearguments, bevor `ARGS` erreicht wird
  libmodsecurity;
- Header werden nicht wie erwartet an `REQUEST_HEADERS` übergeben;
- Anforderungstexte werden für Phase:2-Regeln nicht früh genug gelesen;
- roher JSON-Body-Inhalt ist für `REQUEST_BODY` nicht verfügbar;
- Mehrteilige Uploads füllen `FILES`, `FILES_NAMES` nicht aus,
  `FILES_COMBINED_SIZE` oder `MULTIPART_FILENAME`;
- Audit-Log-Artefakte werden von einer Connector-Laufzeit unterschiedlich geschrieben;
- Das Verhalten des Antwortfilters weicht von den direkten API Erwartungen ab.

Wenn der Server startet und das Modul geladen wird, eine erwartete Variable jedoch nicht
Erreiche libmodsecurity und die YAML-Erwartung schlägt fehl, also `fail`, nicht
`blocked`. `blocked` ist für fehlende Quellen, Downloads, Build-Tools,
Modulartefakte, Bibliotheken oder Laufzeitvoraussetzungen.

## Aktuelle Nachweisfälle

Die YAML-Fälle sind die einzige Quelle für Regeln, Wünsche und Erwartungen. Die
Connector-Harnesses materialisieren sie und senden echte HTTP-Anfragen.

Die aktuell generierten Standardlaufzeitzusammenfassungen berichten über den realen Connector
PASS Nachweise für diese Variablenfamilien. Vollständige Matrix- und Force-All-Nachweise
Zeichnen Sie auch FAIL-Klassen für frühere erwartete Fehler, zukünftige Fehler und Verbindungslücken auf.
Laufzeitdifferenz-, Semantik-, Fähigkeits- und Antwortkörperfälle. Nicht lesen
Die folgende Tabelle dient als pauschaler stabiler Status für jeden YAML-Fall.

| Verified variable | Example active cases | Status |
| --- | --- | --- |
| `ARGS` | `phase2_args_block`, `collection_args_get_block`, V2 operator/transform cases | Present in default connector smoke evidence where the case is promoted |
| `REQUEST_HEADERS` | `phase1_header_block` | Present in default connector smoke evidence where the case is promoted |
| `REQUEST_BODY` | `request_body_json_block`, `request_body_raw_text_block`, `json_request_body_block` | Present in default connector smoke evidence where the case is promoted |
| `FILES` | `multipart_files_value_block`, `multipart_files_names_block`, `multipart_files_combined_size`, `multipart_filename_block` | Remaining multipart gaps are classified and non-promoted |
| `XML` | `xml_request_body_block` | Remaining XML processor activation gaps are classified and non-promoted |
| `AUDIT_LOG` | `audit_log_phase1_block` | Explicit `nolog` and audit-evidence gaps are classified; no active `audit_log_evidence` next-fix cluster remains |
| `RESPONSE_HEADERS` | `response_header_basic` | Phase 3 response-header evidence is implemented; remaining MRTS DetectionOnly cases are classification-only |

`RESPONSE_BODY` wird bewusst nicht als verifiziert aufgeführt. Der Aktive
`response_body_pass` Fall beweist Passthrough mit aktiviertem Antworttextzugriff,
Die Blockierung der Antwortkörper-Regelvariablen bleibt jedoch mapped/xfail bestehen, bis beide
Konnektoren geben stabile HTTP 403 für denselben YAML-Fall zurück.
ModSecurity-nginx PR #377 Quelländerungen werden als NGINX Quelle aufgezeichnet
Herkunft, nicht als Connector-Validierung.

## Ergebnismetadaten

Jede Connector-Zusammenfassung unter `$BUILD_ROOT/results/` zeichnet Folgendes auf:

```json
{
  "status_model": "msconnector_status",
  "origin_model": "msconnector_origin",
  "intervention_model": "msconnector_intervention",
  "connector_path": "real-world",
  "validation_mode": "real-world-connector-path",
  "server": "apache",
  "server_binary": "...",
  "module": "...",
  "libmodsecurity": "...",
  "origin": {
    "source": "adapter-owned|monorepo-upstream|external",
    "source_repo": "ModSecurity-apache",
    "source_commit": "...",
    "source_version": "...",
    "license": "Apache-2.0",
    "imported_path": "..."
  },
  "verified_variables": ["ARGS", "REQUEST_BODY"]
}
```

`verified_variables` wird nur aus aktiven Fällen berechnet, deren Ergebnis ist
`pass`. Nur zugeordnete, xfail-, blockierte und fehlgeschlagene Fälle fügen keine Variablen hinzu.

## Laufzeitport und PID Sicherheit

Die Kabelbäume wählen Ports deterministisch aus dem angeforderten Basisport und aus
Suchen Sie vorwärts nach einem freien `127.0.0.1` Listener-Slot. Wenn eine generierte Laufzeit-PID
Wenn die Datei von einem früheren Lauf übrig bleibt, stoppt der Harness diesen Prozess erst, wenn die
Die PID-Datei befindet sich unter `BUILD_ROOT` und die Prozessbefehlszeile verweist auf die
dasselbe generierte Laufzeitverzeichnis.

Die Kabelbäume töten keine unabhängigen Apache-, NGINX- oder Systemprozesse. Ein Pid
Eine Datei, die außerhalb der generierten Laufzeit zeigt, wird als `blocked` gemeldet. Wenn ein
Wenn der Bindungskonflikt nach der Preflight-Portprüfung immer noch auftritt, wird der Fall einmal wiederholt
auf dem nächsten freien Port und behält die normale Unterscheidung `fail`/`blocked` bei
Der Server kann immer noch nicht ausgeführt werden.

## Aktueller Connector-Status

Aktuell generierter Standard-Laufzeitnachweis:

| Connector | Runtime path | Integration path | Default summary |
| --- | --- | --- | --- |
| Apache | real Apache process | Apache module | 54 PASS / 0 FAIL / 0 BLOCKED |
| NGINX | real NGINX process | NGINX module | 60 PASS / 0 FAIL / 0 BLOCKED |
| HAProxy | real HAProxy process | SPOA/SPOP agent | 55 PASS / 0 FAIL / 0 BLOCKED |

Diese lokalen Ergebnisse fördern keine Force-All-Fehler, xfail-Prüfungen,
Nur zugeordnetes Inventar, zukünftige Fälle, Connector-Gap-Fälle, Laufzeitunterschiede
Fälle, API-only-Smokes oder `RESPONSE_BODY`-Blockierung.

Aktuelle Force-All- und Full-Matrix-Nachweise:

| Scope | Result |
| --- | --- |
| Apache force-all | 100 PASS / 27 FAIL / 0 BLOCKED |
| NGINX force-all | 95 PASS / 39 FAIL / 0 BLOCKED |
| HAProxy force-all | 104 PASS / 23 FAIL / 0 BLOCKED |
| Full-Matrix | 3074 PASS / 782 FAIL / 0 BLOCKED |

In anderen Umgebungen müssen die gleichen Smoke-Ziele verwendet werden, bevor die Prüfung bestanden werden kann. Die
Vollmatrix-FAIL-Zeilen werden in den generierten Berichten und im Finale klassifiziert
Die Konsistenzprüfung empfiehlt derzeit keinen nächsten zur Laufzeit reparierbaren Connector
Cluster.

## Zukünftige Connector

Envoy, Lighttpd und Traefik benötigen einen analogen Nachweis, bevor ein Laufzeitanspruch besteht
gemacht:

- echter server/proxy Prozess;
- echtes Integrationsmodul, Plugin, Filter, SPOE-Dienst oder Middleware;
- libmodsecurity oder dokumentierter gleichwertiger Integrationspfad;
- aktive YAML-Fälle, die als HTTP-Verkehr gesendet werden;
- Ergebniszusammenfassung mit echten Server-binary/module-Metadaten und verifiziert
  Variablen, die nur aus vorübergehenden Fällen abgeleitet sind.

HAProxy verfügt über einen evidenzbasierten SPOA/SPOP-Laufzeitpfad. Die größeren Lücken bleiben bestehen
gemeldet und nicht hochgestuft, bis Runtime-Nachweise eine engere oder weitere Einschränkung rechtfertigen
Unterhaltsanspruch.
