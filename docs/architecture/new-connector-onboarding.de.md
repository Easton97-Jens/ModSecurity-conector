# Onboarding neuer Connectors

**Sprache:** [English](new-connector-onboarding.md) | Deutsch

Dieses Dokument definiert die Evidence Gates für zukünftige ModSecurity-Connector-Arbeiten.
Sie ist bewusst strenger als eine Gerüst-Checkliste: Ein Verbinder darf es nicht sein
durch Absicht, Benennung oder erwartete Statusänderungen gefördert. Werbung erfordert Dateien,
Runtimeartefakte und generierte Evidence.

## Umfang

Die Planung neuer Connectors erfolgt nur auf der Roadmap, bis ein Runtimenachweis vorliegt. Nur Roadmap
Das Material kann Architekturoptionen, Risiken und Evidenceschritte beschreiben, muss es aber
keine Runtime-PASS/FAIL-Werte, Vollmatrixzeilen, Zusammenführungsbereitschaftssignale erstellen,
oder Produktionsstatus.

Der aktuelle Roadmap-Bericht wird von `ci/evidence/reports/generate-connector-roadmap.py` und generiert
geschrieben unter `reports/testing/generated/manifest/connector-roadmap.generated.*`.
Es ist als `roadmap_only` registriert und erfordert weder Runtime noch Vollmatrix
Eingänge.

## Connector-Lebenszyklus

| Bühne | Bedeutung | Erforderliche Nachweise | Nicht zulässige Ansprüche |
| --- | --- | --- | --- |
| geplant | Der Kandidat wird verfolgt, es ist jedoch kein Connector-Verzeichnis erforderlich. | Roadmap-Einstieg, Risiken und erster Evidenceschritt. | Runtimeunterstützung, CRS-Unterstützung, Bereitschaft für verifizierte Fälle. |
| Skeleton | Verzeichnis oder Starter vorhanden, aber Runtimeverhalten ist nicht nachgewiesen. | README, metadata/origin-Hinweise, Build-Starter oder Selbsttest, ausdrücklicher Haftungsausschluss außerhalb der Runtime. | Runtime PASS/FAIL, Produktionsbereitschaft, Vollmatrix-Berechtigung. |
| baubar | Starter- oder Adapterkomponente lässt sich reproduzierbar kompilieren. | Build-Befehl, Ausgabe außerhalb des Checkouts, Quellzuordnung, lint/governance-Pass. | Verkehrsabwicklung oder ModSecurity-Semantik ohne RuntimeEvidence. |
| Runtimestartbar | Server/proxy und Sidecar können lokal gestartet werden. | Minimale Konfiguration, start/stop-Skript, Prozessprotokolle, deterministische Bereinigung. | Verifizierte Blockierung oder CRS-Unterstützung ohne result.json/logs. |
| Verifizierter Fall bereit | Es kann ein gezielter realer Runtimefall ausgeführt werden. | result.json, Falllaufdateien, access/error-Protokolle, decision/audit-Evidence, falls zutreffend. | Vollständige Matrixbereitschaft oder breite Phasenabdeckung. |
| Vollmatrix-Kandidat | Vollmatrix-Jobs sind technisch planbar. | Runtimeproduzent, Matrixjobeinträge, Berichtsintegration, Hinweise zu bekannten Einschränkungen. | Vollständiger Matrix-PASS oder Merge-Readiness-Beitrag vor Evidencen. |
| produktionsgeprüft | Die vollständige verifizierte Evidencepipeline wurde durchlaufen. | Verifizierter Runtimenachweis, vollständige Matrix, Governance, Lint, Schnellprüfung, Berichtslayout, Zusammenführungsbereitschaft PASS. | Jeglicher Produktionsanspruch, wenn generierte Evidence blockiert, veraltet oder fehlend sind. |
| wird durch den vorhandenen Connector abgedeckt | Die Runtime wird bewusst als Variante eines vorhandenen Connectors behandelt. | Entscheidung über die Benennung des Datensatzes, der den Connector und den Kompatibilitätsrauchpfad besitzt. | Separate Connector-Identität, separate generierte Berichte, separate vollständige Matrix. |
| blockiert | Externe, Lizenz-, Architektur- oder Evidenceprobleme verhindern den Fortschritt. | Blockerbeschreibung und Entsperrungsnachweis. | Statuserhöhung vor Blocker-Auflösung. |

## Arbeitsphasen

Jeder neue Connector durchläuft explizite Phasen. Eine Phase kann nützlich sein
Designausgabe, ohne eine Statuserhöhung zu genehmigen.

| Phase | Name | Evidence verlassen | Promotion-Tor |
| --- | --- | --- | --- |
| 0 | Roadmap-Triage | Nur auf der Roadmap erstellter Bericht und optionale Architekturhinweise. | Keine Runtimeförderung. |
| 1 | ArchitekturEvidencespezifikation | Ausgewählter Kontrollpunkt, Alternativen, Protokolle, Ergebnisschema und Nichtziele. | Es kann ein Proof implementiert, aber noch kein Full-Matrix-Job hinzugefügt werden. |
| 2 | Gezielter Runtimerauch | Minimale Konfiguration, Launcher, Upstream, Entscheidungsdienst, result.json und Protokolle. | Der Evidence deckt nur den genannten Fall ab und muss `full_matrix_ready=false` einhalten. |
| 3 | Bereitschaft für verifizierte Fälle | Ein echter verifizierter Falllauf mit Wiederholungsbefehlen und Artefaktpositionen. | Kann erst dann zum Full-Matrix-Kandidaten ernannt werden, wenn Governance, Lint, Schnellprüfung und Layout bestanden wurden. |
| 4 | Full-Matrix-Kandidatur | Matrix-Jobs sind planbar und generierte Berichte beschreiben die tatsächliche Vollständigkeit. | Kein PASS-, Bereitschafts- oder Produktionsanspruch, bis ein vollständig generierter Full-Matrix-Nachweis vorliegt. |
| 5 | Produktionsüberprüfung | Vervollständigen Sie verifizierte Evidencepipeline-Pässe mit Merge Readiness PASS. | Erst jetzt darf der Connector `production_verified` heißen. |

## Akzeptanzkriterien

Ein neuer Connector bewegt sich möglicherweise nicht in Richtung Full-Matrix, bis er mindestens Folgendes nachweisen kann:

- `connectors/<name>/README.md`
- build/start/stop oder Skript ausführen
- minimale Runtimekonfiguration
- Unterstützung bei verifizierten Fällen
- `result.json`
- access/error-Protokolle oder gleichwertig
- Prüfungsnachweise, sofern unterstützt
- gegebenenfalls Entscheidungsnachweise
- Hinweise zur Leistungsfähigkeit
- Requestsblockierender Smoke
- Körperrauch oder ein dokumentierter, nicht unterstützter Grund anfordern
- Bereinigen Sie `make report-governance`, `make lint` und `make quick-check`

## Zukünftige Dateien, Ziele und Berichte

Dies sind spätere Lieferungen für echte Connectoren. Nur Roadmap-Kandidaten müssen
Fügen Sie keine generierten Runtimeberichte oder Vollmatrixzeilen hinzu.

| Artikel | Bühne | Evidenceregel |
| --- | --- | --- |
| `connectors/<name>/README.md` | Skeleton | Erforderlich, bevor ein Kandidat größer als `planned` ist; Es müssen Nichtansprüche angegeben werden. |
| `connectors/<name>/ORIGIN.md` und `SOURCE_MAP.json` | Skeleton | Verfolgen Sie den Besitz und die Quellenzuordnung, bedeuten Sie jedoch keine Runtimeunterstützung. |
| `connectors/<name>/config/` oder Harnesskonfiguration | Runtimestartbar | Die Konfiguration ist kein Evidence, bis ein Lauf Protokolle schreibt und `result.json`. |
| `connectors/<name>/harness/` oder `scripts/run-smoke.sh` | Runtimestartbar | Runtimeartefakte müssen unter verifizierten Runtimewurzeln geschrieben werden. |
| `make smoke-<name>` oder gleichwertig | Runtimestartbar | Nur lokaler Smoke; keine Vollmatrix-Integration. |
| `make verified-case CONNECTOR=<name> CASE=<case>` | Verifizierter Fall bereit | Erfordert echte Ergebnisse, Protokolle, Fallakten und einen wahrheitsgetreuen Status. |
| `reports/testing/generated/runtime/<name>-runtime-results.generated.md` | Verifizierter Fall bereit | Nur aus verifizierten Eingaben generiert, niemals manuell bearbeitet. |
| `make verified-full-matrix-job CONNECTOR=<name> CRS=<variant> MRTS=<variant>` | Vollmatrix-Kandidat | Planbar ist nicht PASS; Melden Sie nur den tatsächlichen Ausführungsstatus. |
| `reports/testing/generated/manifest/full-matrix-job-completeness.generated.*` | Vollmatrix-Kandidat | Erstellen Sie keine Jobreihen für nicht integrierte Anschlüsse. |
| `reports/testing/generated/manifest/merge-readiness-dashboard.generated.*` | produktionsgeprüft | Nur-Roadmap-Berichte dürfen die Bereitschaft nicht beeinflussen. |

## Evidenceregeln

- Patchen Sie generierte Berichte nicht manuell.
- Ändern Sie die erwarteten Status nicht, damit ein neuer Connector grün aussieht.
- Erfinden Sie keine PASS/FAIL-Werte oder Vollmatrixzeilen für nicht implementierte Connectoren.
- Übertragen Sie keine blockierten generierten Berichte aus einer lokalen Umgebung, in denen verifizierte Runtimeeingaben fehlen.
– Speichern Sie Runtimeartefakte im verifizierten Runtimestammverzeichnis, nicht im Checkout.
- Behalten Sie die Roadmap für neue Connector-Berichte bei, bis echte Runtimenachweise vorliegen.

## Envoy Erster Evidence

Envoy ist der nächste empfohlene Connector, da das Repository bereits Folgendes enthält
Ein Envoy-Starter und Envoy verfügt über realistische HTTP-Filterkontrollpunkte für a
Sidecar-basierter Evidence. Der erste Schritt ist kein vollständiger Connector. Es handelt sich um eine gezielte
Runtimerauch, der einen minimalen Requestsblockierungspfad Evidencet.

Die Empfehlung ist an Evidence gebunden:

- Vorhandene Envoy-Dateien erweisen sich als Skelett und nicht als Runtimeunterstützung.
- `ext_proc` und `ext_authz` sind Proof-Kandidaten, keine verifizierte Unterstützung;
- Ein wiederverwendbarer Entscheidungsdienst ist für spätere Traefik/lighttpd-Studien nützlich, aber
es ist kein eigenständiger Connector;
- Das erste Envoy-Ergebnis muss gezielt bleiben und deklariert werden
`full_matrix_ready=false`.

Vor der Implementierung zu vergleichende Architekturoptionen:

| Option | Erstmalige Verwendung | Hauptrisiko |
| --- | --- | --- |
| `ext_proc` Beiwagen | Bevorzugter Pfad für request/body/response-Verarbeitungsexperimente. | Grenzen der gRPC/protobuf-Komplexität und des Körperverarbeitungsmodus. |
| `ext_authz`-Dienst | Einfacherer Smoke zur Requestsblockierung, wenn `ext_proc` zu schwer ist. | Eingeschränkter Requeststext und kein Anspruch auf den ersten Response Body. |
| WASM-Filter | Zukünftige native Filterkettenoption. | Hohe Toolchain-, Debugging- und ModSecurity-Lebenszykluskomplexität. |
| Lua-Filter | Fallback-Machbarkeitsspitze für einfache Entscheidungen. | Schwache langfristige Connectorsemantik. |
| Reverse-Proxy-Kette mit vorhandenem Connector | Nur Infrastrukturrauch. | Die Blockierung würde dem Downstream-Anschluss zufallen, nicht Envoy. |
| Externer ModSecurity-Entscheidungsdienst | Gemeinsamer Dienst hinter `ext_proc` oder `ext_authz`. | Die Protocol/body-Zuordnung muss noch nachgewiesen werden. |

Empfohlener Evidence:

- Minimaler Envoy `ext_proc`- oder `ext_authz`-Runtimerauch.
– Envoy startet lokal mit einer deterministischen Minimalkonfiguration.
– Ein einfacher Upstream antwortet über Envoy.
– Ein ModSecurity-ähnlicher Entscheidungsdienst oder Sidecar gibt eine Ablehnungsentscheidung zurück.
– Ein Smoke-Fall wie `envoy_request_blocking_smoke` gibt HTTP 403 zurück.
- `result.json`, Envoy-Protokolle, Entscheidungsdienstprotokolle und Case-Run-Dateien sind
geschrieben unter `$VERIFIED_RUN_ROOT/envoy-smoke/`.

Ausstiegskriterien:

| Kriterium | Erforderliche Nachweise |
| --- | --- |
| Lokaler Start | Envoy, Upstream und Decision Service beginnen mit einem deterministischen Skript und bereinigen ports/processes. |
| Upstream-Pass-Through | Eine harmlose Anfrage erreicht den Upstream über Envoy und protokolliert die Route. |
| Sperrung anfordern | Eine bekannte böswillige Anfrage gibt HTTP 403 über den ausgewählten Envoy-Erweiterungspfad zurück. |
| EntscheidungsEvidence | Entscheidungsprotokolldatensätze verweigern, `intervention_status=403`, Fall-ID und Requestskorrelations-ID. |
| RuntimeEvidencepaket | `result.json`, `case-run.md`, `case-run.json`, Envoy-Protokolle und Entscheidungsprotokolle unter `$VERIFIED_RUN_ROOT/envoy-smoke/`. |
| Zielfernrohrschutz | `result.json` deklariert `evidence_scope=targeted` und `full_matrix_ready=false`. |

Envoy First-Proof-Non-Goals:

- Keine CRS-Unterstützung.
- Keine MRTS-Unterstützung.
- Keine vollständige Matrix.
- Kein Anspruch auf Unterstützung durch die Antwortstelle.
- Kein `production_verified`-Anspruch.
– Keine Auswirkung auf die Zusammenführungsbereitschaft.

## LiteSpeed ​​geplanter Evidence

LiteSpeed ​​ist nur ein geplanter Kandidat. OpenLiteSpeed ​​ist wahrscheinlich die erste Variante
zu studieren, weil es wahrscheinlicher ist, dass es CI-freundlich ist als LiteSpeed ​​Enterprise,
aber Verpackung, Lizenzierung, Download-Automatisierung und ModSecurity/CRS-Kompatibilität
muss nachgewiesen werden, bevor ein Connector-Verzeichnis hinzugefügt wird.

Erster Proof: OpenLiteSpeed ​​install/start-Proof plus ein CRS/request-blocking
rauchen, wenn Automatisierung und Lizenzierung dies zulassen.

| Feld | Wert |
| --- | --- |
| Kandidat | LiteSpeed ​​/ OpenLiteSpeed |
| Status | geplant |
| Erster Evidence | OpenLiteSpeed ​​install/start Proof plus ein CRS/request-blocking Smoke, sofern Automatisierung und Lizenzierung dies zulassen. |
| Hauptrisiken | License/download-Automatisierung, Editionsunterschiede, Paketverfügbarkeit, CI-Reproduzierbarkeit und ModSecurity/CRS-Kompatibilität. |
| Nachweis erforderlich | Installationsprotokoll, Startup-Log, Minimalkonfiguration, Requeststranskript, `result.json`- und access/error/audit-Protokolle, falls verfügbar. |

## Lighttpd und Traefik

Lighttpd und Traefik bleiben `partial_skeleton`-Kandidaten. Sie sollten sich nicht bewegen
in Richtung Full-Matrix, bis ein gezielter Requestsblockierungsnachweis eine Machbarkeit ergibt
Runtimekontrollpunkt.

| Connector | Aktueller Stand | Erster Evidenceschritt | Hauptrisiko |
| --- | --- | --- | --- |
| lighttpd | partielles_Skelett | Machbarkeitsnachweis zur Requestsblockierung, der das native Modul gegenüber der proxy/sidecar-Architektur auswählt. | Unklare native ModSecurity-Integration und wahrscheinlicher Bedarf an sidecar/proxy. |
| traefik | partielles_Skelett | forwardAuth/decision-service gibt 403 für eine bekannte böswillige Anfrage mit Protokollen und `result.json` zurück. | Wenn man zu früh mit einem Go-Plugin beginnt, könnte die einfachere Frage des Entscheidungsdienstnachweises verdeckt werden. |

## OpenResty-Entscheidung

OpenResty wird vom bestehenden NGINX-Connector abgedeckt, da es NGINX-basiert ist.
Zu diesem Zeitpunkt darf es noch kein separater Anschluss sein. Eine zukünftige Kompatibilität
Smoke kann als NGINX-Runtimevariante hinzugefügt werden, es darf jedoch keine separate Variante erstellt werden
Vollständige Matrixzeilen oder separat generierte Connector-Berichte.

## Was Sie vor dem vollständigen MatrixEvidence nicht behaupten sollten

Bevor vollständige Evidence vorliegen, behaupten Sie nicht:

- Produktionsgeprüfter Status
- Beitrag zur Merge-Readiness
- Vollmatrix-PASS/FAIL-Zählungen
- Variantenübergreifende CRS-Unterstützung
- MRTS-Unterstützung
- Unterstützung für die Blockierung des Response Bodys
- Phasenabdeckungsparität mit Apache, NGINX oder HAProxy
- Unterstützung der Runtimefähigkeit ohne `result.json` und Protokolle
