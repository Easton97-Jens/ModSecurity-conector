# Engine-eigene Response-Inspection-Limits

**Sprache:** [English](CR-20261004-engine-owned-response-limits.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20261004-engine-owned-response-limits` |
| Datum (UTC) | 2026-10-04 |
| Basis-Revision | `9d18eebf6f01e0f370ffa9555e50101612cba11e` |

## Motivation und Problemstellung

Connector-eigene kumulierte Phase-4-Response-Budgets duplizierten die libModSecurity-Policy und konnten Responses abweisen, die die Engine gar nicht inspizieren würde, einschließlich über MIME ausgeschlossener Responses oder Konfigurationen mit `SecResponseBodyLimitAction ProcessPartial`. Das repositoryweite Ziel ist eine einheitliche Eigentümerschaft für Apache, NGINX, HAProxy, Envoy, Traefik und lighttpd: libModSecurity besitzt Auswahl und Byte-Limits der WAF-Response-Inspection; Connectoren behalten nur echte Host-/Transport-/Ressourcen-Sicherheitslimits.

## Akzeptanzkriterien

- Jeder gültige Phase-4-Modus löst die alte kumulierte Connector-Response-Inspection-Grenze auf ein reines Accounting-Maximum statt auf ein konfiguriertes WAF-Byte-Budget auf.
- NGINX wendet sein getrenntes kumuliertes Safe-/Strict-Response-Limit nicht mehr an.
- Envoy deaktiviert beim Common-Runtime-Mode-Readback den kumulierten Response-Precheck für off, safe und strict, während Per-Chunk- und Überlaufprüfungen erhalten bleiben.
- Apache, HAProxy, Common Runtime, Traefik und lighttpd übernehmen dieselbe Eigentümerschaft über gemeinsame Runtime-/Helper-Pfade.
- Unabhängige Allokations-, Speicherkapazitäts-, Chunk-/Frame-, Timeout-, Datei-Read- und arithmetische Überlaufprüfungen bleiben aktiv.
- Das Ziel ist in `.codex/context/phase4-target-semantics.md` und zweisprachiger Leserdokumentation festgehalten.

## Implementierungsentscheidung und Begründung

Die bestehende API `msconnector_phase4_effective_body_limit` bleibt als Kompatibilitäts-Shim erhalten. Gültige Modi liefern `SIZE_MAX` ausschließlich als arithmetische/Accounting-Grenze; nicht gesetzte oder unbekannte Modi liefern weiterhin null und schlagen fail-closed fehl. NGINX verwendet nun den gemeinsamen Helper statt einer eigenen Safe-/Strict-Budget-Verzweigung. Die Common Runtime erzwingt Reject-Semantik nur bei unmöglichem Response-Zählerüberlauf, damit `ProcessPartial` keinen arithmetischen Überlauf in einen erfolgreichen Append umwandelt.

Das Parsen von `modsecurity_phase4_body_limit` bleibt vorerst erhalten, um keinen sofortigen Konfigurationsbruch zu erzeugen. In den quellenbasierten Konfigurationsmetadaten ist der Wert als deprecated/compatibility-only markiert. Eine Entfernung aus der öffentlichen Konfiguration kann getrennt als Breaking Migration erfolgen.

## Geänderte Dateien

- `.codex/context/phase4-target-semantics.md`
- `ci/checks/documentation/connector_config_reference.py`
- `common/include/msconnector/phase4_budget.h`
- `common/runtime/msconnector_runtime.c`
- `common/src/directive_spec.c`
- `connectors/apache/README.de.md`
- `connectors/apache/README.md`
- `connectors/apache/src/msc_filters.c`
- `connectors/envoy/README.de.md`
- `connectors/envoy/README.md`
- `connectors/envoy/ext_proc/internal/processor/common_runtime_budget.go`
- `connectors/envoy/ext_proc/internal/processor/phase4_budget_test.go`
- `connectors/haproxy/README.de.md`
- `connectors/haproxy/README.md`
- `connectors/lighttpd/README.de.md`
- `connectors/lighttpd/README.md`
- `connectors/nginx/README.de.md`
- `connectors/nginx/README.md`
- `connectors/nginx/src/ngx_http_modsecurity_body_filter.c`
- `connectors/nginx/src/ngx_http_modsecurity_header_filter.c`
- `connectors/traefik/README.de.md`
- `connectors/traefik/README.md`
- `docs/phase4-mode-budget.de.md`
- `docs/phase4-mode-budget.md`
- `examples/apache/README.de.md`
- `examples/apache/README.md`
- `examples/apache/configuration-reference.de.md`
- `examples/apache/configuration-reference.md`
- `examples/common/common-connector-configuration.de.md`
- `examples/common/common-connector-configuration.md`
- `examples/nginx/README.de.md`
- `examples/nginx/README.md`
- `examples/nginx/configuration-reference.de.md`
- `examples/nginx/configuration-reference.md`
- `reports/connector-configuration-inventory.json`
- `tests/test_nginx_phase4_mode_budget.py`
- `tests/test_phase4_all_connector_budget.py`
- `tests/test_phase4_envoy_budget.py`
- `reports/audits/change-records/CR-20261004-engine-owned-response-limits.md`
- `reports/audits/change-records/CR-20261004-engine-owned-response-limits.de.md`

## Ausgeführte Befehle

Es wurde kein repository-nativer Build-/Test-/Dokumentationsbefehl ausgeführt. Die Repository-Policy verlangt RTK für Projekt-Shellbefehle; ein Umgebungscheck fand kein installiertes `rtk`, daher wurde nicht stillschweigend auf unwrapped Befehle zurückgefallen. GitHub-Connector-Reads/-Writes und Source-Level-Exact-Match-Prüfungen wurden zur Vorbereitung des Branches verwendet.

## Security-Auswirkung

Die Änderung entfernt einen Connector-Ablehnungspfad, der ansonsten legitime große oder MIME-ausgeschlossene Responses beenden konnte. Sie deaktiviert weder die libModSecurity-Response-Inspection noch deren `SecResponseBodyLimit`-Policy. Unabhängige Host- und Transport-Ressourcencontrols bleiben verpflichtend. Pfade, die Responses puffern, dürfen weiterhin explizite begrenzte Speicherkapazität erzwingen.

## Runtime-Evidence

Es wurde keine Runtime-Evidence erhoben oder beansprucht.

## Bekannte Einschränkungen

Alte Budget-Konfiguration bleibt parsebar und kann deshalb für ältere Automation aktiv aussehen, obwohl sie die WAF-Response-Inspection nicht mehr steuert. Der Branch enthält Source-Level- und Dokumentationsregressionen, aber kein lokal ausgeführtes Projekt-Testergebnis, weil der verpflichtende RTK-Wrapper nicht verfügbar ist.

## Verbleibende Risiken

Native Host-Regressionen sind weiterhin nötig, um zu beweisen, dass große Responses streamend/begrenzt bleiben und kein hostspezifischer Bufferpfad ausschließlich vom entfernten kumulierten Inspection-Budget abhing. Das Live-Verhalten später Interventionen wird durch diese Source-Level-Migration weder verändert noch bewiesen.

## Nicht ausgeführte Prüfungen mit Begründung

`tests.test_nginx_phase4_mode_budget`, `tests.test_phase4_all_connector_budget`, `tests.test_phase4_envoy_budget`, Konfigurationsreferenz-Generierungschecks, Bilingual-/Link-Checks, native Connector-Builds, Host-Runtime-Regressionen, Sanitizer, SonarQube und `git diff --check` wurden nicht ausgeführt, weil der repository-verpflichtende RTK-Wrapper in dieser Umgebung nicht verfügbar ist. CI und Review für den aktuellen Head müssen diese Ergebnisse liefern.

## Finaler Diff- und Review-Status

Die Änderung ist auf einem Task-Branch von der dokumentierten Basis-Revision vorbereitet und für einen Draft-Pull-Request vorgesehen. Es ist kein Merge nach `master` autorisiert oder beansprucht. CI, Review und Quality Gate für den aktuellen Head stehen aus.
