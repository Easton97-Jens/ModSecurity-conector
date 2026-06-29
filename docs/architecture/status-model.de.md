# Statusmodell

**Sprache:** [English](status-model.md) | Deutsch

Das Framework trennt Runtimeergebnisse vom import/classification-Status.

## Runtimestatus

| Status | Bedeutung | Exit-Effekt |
| --- | --- | --- |
| `pass` | Das tatsächliche HTTP-Verhalten entsprach den YAML-Erwartungen | Erfolg |
| `fail` | Der Server wurde ausgeführt, aber das Verhalten wich von den YAML-Erwartungen ab | Ausgang 1 |
| `blocked` | Quelle, Download, Build oder Runtimevoraussetzung fehlten | Ausfahrt 77 |
| `not_executable` | Der Fall konnte für den connector/runtime-Modus strukturell nicht realisiert werden | Ausfahrt 78 |
| `skipped` | Reserviert für explizites zukünftiges Sprungverhalten | nicht stillschweigend verwendet |

`fail` wird verwendet, wenn eine Regelvariable libmodsecurity oder das nicht erreicht
Connector gibt den falschen HTTP-Status zurück. `blocked` gilt nur für Voraussetzungen.

## Allgemeiner Betriebsstatus

Der gemeinsame C-First-Header `common/include/msconnector/status.h` und der Helfer
Die Implementierung `common/src/status.c` definiert den connectorneutralen Betrieb
Ergebnisse. Harness-Zusammenfassungen stellen diese Konzepte als JSON-Metadaten dar, die nur angehängt werden können.
Sie ersetzen nicht die oben genannten Runtimestatus.

| Runtimestatus | `operation_status` | `msconnector_status`-Äquivalent |
| --- | --- | --- |
| `pass` | `ok` | `MSCONNECTOR_STATUS_OK` |
| `fail` | `error` | `MSCONNECTOR_STATUS_ERROR` |
| `blocked` | `blocked` | `MSCONNECTOR_STATUS_BLOCKED` |
| `not_executable` | `unsupported` | `MSCONNECTOR_STATUS_UNSUPPORTED` |
| `skipped` | `unsupported` | `MSCONNECTOR_STATUS_UNSUPPORTED` |

Die Zuordnung erfolgt bewusst einseitig. Vorhandene Smoke-Semantik und Exit-Codes
bleiben unverändert. Python/Shell-Läufer spiegeln diese Zuordnung wider
`modules/ModSecurity-test-Framework/tests/runners/msconnector_models.py`; Sie laden den C-Helfer nicht durch
FFI.

Standardmäßige Smoke-Zusammenfassungen, Force-All-Runtimematrix-Snapshots und kombiniert
`make smoke-all`-Ergebnisse sind separate Evidenzklassen. Ein PASS in einem Ergebnis
Die Datei darf nicht auf „mapped-only“, „future“, „connector-gap“ oder „connector-gap“ verallgemeinert werden.
Runtimedifferenz-, blockierte oder ehemalige-XFAIL-Fälle.

## Importstatus

| Status | Bedeutung |
| --- | --- |
| `fully-imported-common` | Von der Quelle abgeleiteter Fall, der über echte Apache- und NGINX-Connector-Pfade weitergegeben wird |
| `connector-specific` | Gilt nur für einen benannten Connector |
| `mapped-only` | Die Quelle ist dokumentiert, aber nicht als aktiver Smoke ausführbar |
| `blocked` | Die relevante Quelle ist vorhanden, aber der aktuelle Harness kann sie nicht ausführen |
| `former_xfail` | Historische Migrationsmetadaten für Fälle, die jetzt durch normale RuntimeEvidence ausgewertet werden |

`config/testing/import-status.json` ist das maschinenlesbare Manifest für den Importstatus
zählt. Connector-Zusammenfassungen kopieren diese Zählungen in `import_status`.

## Ergebnismetadaten

Jede JSON-Connector-Zusammenfassung enthält:

- `status_model: "msconnector_status"`
- `origin_model: "msconnector_origin"`
- `intervention_model: "msconnector_intervention"`
- `connector_path: "real-world"`
- `validation_mode: "real-world-connector-path"`
- `environment`: `SMOKE_ENVIRONMENT`, sonst `github-actions` oder `local`
- `audit_behavior`: `stable`, `unstable` oder `unexpected`
- `verified_variables`: Wird nur aus der Weitergabe aktiver Fälle abgeleitet

Jeder Case-Eintrag enthält außerdem ein `intervention`-Objekt mit der Neutralität
`msconnector_intervention`-Form: `disruptive`, `status` und `log_message`.
Für nicht störende Erwartungen lautet der Interventionsstatus `0`; das erwartete
Die HTTP-Antwort bleibt als `expected_status` verfügbar.

Frühere XFAIL-Fälle behalten Migrationsmetadaten bei, PASS/FAIL/BLOCKED/NOT_EXECUTABLE
kommt jetzt nur noch aus Live-RuntimeEvidencen.

`RESPONSE_BODY`-Pass-Through-Evidence sind keine Unterstützung für die Blockierung von Response Bodyn.
RAW-Argumentsammlungen bleiben nur zugeordnet, bis lokale PR #3564-Unterstützung und
Apache/NGINX Real-World-Connector-Pässe sind vorhanden.
