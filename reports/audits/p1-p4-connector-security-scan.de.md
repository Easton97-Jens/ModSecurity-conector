# P1–P4-Connector-Parity: Scoped-Security-Scan-Meilenstein

**Sprache:** [English](p1-p4-connector-security-scan.md) | Deutsch

## Zweck, Scope und Evidenzgrenze

Dieser Bericht dokumentiert den abgeschlossenen Standard-Security-Scan-
Meilenstein des vom Benutzer angeforderten P1–P4-Connector-Parity-Programms.
Er umfasst Parent `common/` und `connectors/` an der Task-Worktree-Revision
mit Ausgangspunkt `2bd99f47d61c7dc9d7db847112725d60b49dc1f4`; er behauptet
weder finale Connector-Parität noch ein Real-Host-Matrix-Ergebnis.

Der Scan ist im Run
`20260826T175448Z-p1-p4-connector-parity-20260826-ea15c4bb` aufbewahrt und
versiegelt. SHA-256 seiner kanonischen `findings.json` ist
`18d6248c2d85ce0e1457a62a6682fe8e3abd567af47ed430945ec01788e8c35d`.
Framework, MRTS, CI-Workflows, GitHub-Konfiguration, Remote-Deployment und
Hosted-Tests waren ausgeschlossen. Es wurden keine rohen Request- oder
Response-Bodies aufbewahrt.

## Ergebnis und Disposition

Der Scan enthält elf Security-Records. Einer ist lokal reproduziert und
release-blockierend; acht sind im Source bestätigte Kandidaten mit ausstehenden
Host-/Runtime-Controls; zwei ergänzen bestehende kanonische Findings.

| Finding(s) | Disposition | Evidenzgrenze |
| --- | --- | --- |
| `FND-PARENT-0958` | P0/high, lokal reproduziert, `validated`, Release-Blocker | Eine Public-API-Go-Reproduktion zeigt, dass ein nichtleerer Traefik-Native-UDS-Request einen ungelesenen Downstream-Handler erreicht, HTTP 204 zurückgibt und null P2-Body-Callbacks sowie kein Request-EOS erzeugt. |
| `FND-PARENT-0959`, `FND-PARENT-0960` | P1/medium, `triaged` Kandidaten | HAProxy-SPOP-Deadline- und Peer-Disconnect/SIGPIPE-Pfade benötigen ausgewählten Runtime-Nachweis. |
| `FND-PARENT-0961` | P2/medium, `triaged` Kandidat | NGINX-Callback-Logging muss mit `modsecurity_use_error_log` sowohl off als auch on ausgeführt werden. |
| `FND-PARENT-0962`–`FND-PARENT-0964` | P1/P2 Kandidaten | Common-Headersyntax, Host-Action-Event-Zuordnung/Integrität und JSONL-UTF-8 benötigen Parser- und Consumer-Controls. |
| `FND-PARENT-0965`, `FND-PARENT-0966` | P1/medium, `triaged` Kandidaten | Traefik-C-Engine-Ergebnis-Write-Deadline und Envoy-ext_proc-Forced-Shutdown-Drain benötigen kontrollierte Peer-/Stream-Tests. |
| `FND-PARENT-0007`, `FND-PARENT-0135` | Bestehende Records ergänzt | Der Scan ergänzt Source-Evidenz für Traefik-Worker-Admission und die ext_proc-Plaintext-Non-Loopback-Grenze, ohne deren Lifecycle-Disposition zu verstärken. |

Das P0-Finding blockiert verifizierten PR-Status und jede Master-Integration.
Die Kandidatenrecords behaupten weder einen Runtime-Exploit noch eine
abgeschlossene Behebung oder einen vollständig runtime-verifizierten Connector.

## Tatsächlich ausgeführte Validierung

| Check | Tatsächliches Ergebnis |
| --- | --- |
| Traefik Native UDS `go test -count=1 -race ./...` | Mit task-eigenem Go-Cache und temporärem Storage bestanden. |
| Traefik Native UDS `go vet ./...` | Bestanden. |
| Envoy ext_proc `go test -count=1 -race ./...` | Für Command-, Composite- und Processor-Packages mit task-eigenen Cache-/Module-Cache-/Tmp-Pfaden bestanden. |
| Envoy ext_proc `go vet ./...` | Bestanden. |
| Isolierte Unread-Body-Public-API-Reproduktion | Bestand bei beobachtetem HTTP 204, null Request-Body-Callbacks und `RequestEOS=false`; die Evidenz ist getrennt von versionierter Dokumentation aufbewahrt. |
| Standard Scoped Codex Security Scan | Abgeschlossen und versiegelt; Manifest, Coverage, Report, Findings-JSON und SARIF sind lokal aufbewahrt. |

Diese Checks sind Source-Level- oder isolierte Controls. Sie ersetzen keine
Real-Host-Evidenz für Apache, NGINX, HAProxy, Envoy, Traefik oder lighttpd.

## Source-Ownership- und Remediation-Gate

Dieser Meilenstein enthält keine Produkt-Source-Behebung. Die erforderlichen
Common- und Connector-Pfade überlappen die ungemergten Draft-PRs #344, #345
und #346. Die aktuelle Aufgabe darf deren Source-Änderungen nicht kopieren,
rebasen, mergen oder still duplizieren. Vor einer konkurrierenden Behebung ist
eine aktuelle Benutzerentscheidung über Integration oder Ablösung erforderlich.

Nach dieser Entscheidung zuerst `FND-PARENT-0958` reparieren und unabhängig
verifizieren: konfigurierte Body-Inspection muss P2 und genau ein Request-EOS
vor Downstream-Ausführung liefern oder sicher fehlschlagen; Unread-,
Normal-Read-, Empty-Body-, Cancellation-, Later-Request-, echtes
Traefik/UDS- und Cleanup-Controls müssen bestehen. Danach jeden Kandidaten
erst promoten, wenn seine dokumentierten negativen und legitimen Host-Controls
Erreichbarkeit und Auswirkung belegen.

## Bekannte Einschränkungen und nächster Meilenstein

In der aktuellen Umgebung gibt es kein ausgewähltes Apache-, NGINX-, HAProxy-,
Envoy-, Traefik- oder lighttpd-Host-Executable, und der Framework-Gitlink ist
nicht initialisiert. Alle Real-Host-P1–P4-Evidenz bleibt daher unrun, nicht
inapplicable. Die repositoryweiten Bilingual- und Link-Checks bleiben durch
vorbestehende fehlende Framework-Targets blockiert; dieser Meilenstein ändert
weder Framework/MRTS noch CI, Gitlinks, Dependencies, Branch-Protection oder
Required-Checks.

Der Draft-PR wird mit diesem evidenzbegrenzten Dokumentationsmeilenstein
aktualisiert. Er bleibt Draft; es wird weder ein Merge, ein direkter
`master`-Push, ein Hosted-Check-Erfolg noch finale Parität behauptet.
