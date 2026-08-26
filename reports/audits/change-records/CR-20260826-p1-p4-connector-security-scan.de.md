# Change Record CR-20260826: P1–P4-Connector-Parity-Security-Scan-Meilenstein

**Sprache:** [English](CR-20260826-p1-p4-connector-security-scan.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | `CR-20260826-p1-p4-connector-security-scan` |
| Datum (UTC) | `2026-08-26` |
| Basis-Revision | `2bd99f47d61c7dc9d7db847112725d60b49dc1f4` |
| Scope | Parent-only-Security-Scan-Meilensteinbericht, deutscher Begleiter, gepaarter Change Record und bilinguale Archivindizes. Keine Connector-/Common-Source-, Framework/MRTS-Source-, Gitlink-, Dependency-, CI/Workflow-, Branch-Rule-, Required-Check- oder Hosted-Test-Konfigurationsänderung. |

## Motivation und Problemstellung

Der Benutzer forderte ein schrittweises P1–P4-Parity-Programm für zehn
Connectoren mit regelmäßig aktualisiertem task-eigenem Draft-PR. Die Baseline
zeigte, dass diese Arbeit Request/Response-, UDS-, gRPC-, Event-, Lifecycle-
und Ressourcen-Sicherheitsgrenzen berührt. Dieser Meilenstein dokumentiert
einen abgeschlossenen Scoped-Security-Scan, bevor konkurrierende
Source-Implementierung zulässig ist.

## Akzeptanzkriterien

Dieser Meilenstein ist nur akzeptiert, wenn er:

- einen Scoped-Parent-`common/`/`connectors/`-Security-Scan ausführt und
  versiegelt;
- konkrete Evidenz dokumentiert und reproduzierte, validierte und
  source-only Kandidaten-Dispositionen unterscheidet;
- kanonische bilinguale Finding-Records, Index-, Backlog- und
  Remediation-Roadmap-Einträge anlegt oder ergänzt;
- den No-CI-, Parent-only- und No-Framework/MRTS/Gitlink-Scope bewahrt;
- keine konkurrierende Source-Behebung über die Ownership ungemergter
  Draft-PRs hinweg still schreibt; und
- den benutzerautorisierten Draft-PR nur mit wahrheitsgemäßen Ergebnissen
  aktualisiert.

## Implementierungsentscheidung und Begründung

- Der Scan ist im Task-Run
  `20260826T175448Z-p1-p4-connector-parity-20260826-ea15c4bb` versiegelt;
  SHA-256 seiner kanonischen `findings.json` ist
  `18d6248c2d85ce0e1457a62a6682fe8e3abd567af47ed430945ec01788e8c35d`.
- Eine aufbewahrte isolierte Public-API-Reproduktion etablierte
  `FND-PARENT-0958`: Ein nichtleerer Traefik-Native-UDS-Request kann nach
  ungelesenem Downstream-Body HTTP 204 zurückgeben, ohne P2-Callbacks oder
  Request-EOS.
- `FND-PARENT-0959`–`FND-PARENT-0966` bleiben triagierte im Source bestätigte
  Kandidaten, keine Runtime-Exploit-Behauptungen. Die bestehenden
  `FND-PARENT-0007` und `FND-PARENT-0135` wurden ergänzt statt dupliziert.
- Eine Source-Behebung wird absichtlich nicht geschrieben, weil die
  betroffenen Produktpfade die ungemergten Draft-PRs #344, #345 und #346
  überlappen. Der nächste Source-Schritt benötigt eine aktuelle
  Benutzerentscheidung über Integration oder Ablösung.

## Security-Auswirkung

Diese reine Dokumentationsänderung zeichnet einen P0/high lokal
reproduzierten Bypass und verwandte Kandidatengrenzen auf. Sie ändert keine
Produktsicherheitskontrolle. Das P0-Finding blockiert verifizierte Delivery und
Master-Integration, bis eine Behebung vollständig verifiziert, der Befund als
nicht anwendbar bewiesen oder das genaue Restrisiko vom aktuellen Benutzer
ausdrücklich akzeptiert wurde. Kein Kandidat wird als behoben oder als
abgeschlossenes Host-Runtime-Ergebnis dargestellt.

## Geänderte Dateien

- `reports/audits/p1-p4-connector-security-scan.md`
- `reports/audits/p1-p4-connector-security-scan.de.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-security-scan.md`
- `reports/audits/change-records/CR-20260826-p1-p4-connector-security-scan.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Ausgeführte Befehle

### Tests und tatsächliche Ergebnisse

| Check | Tatsächliches Ergebnis |
| --- | --- |
| `go test -count=1 -race ./...` in `connectors/traefik/native_middleware` | Mit task-eigenen Cache- und Tmp-Pfaden bestanden. |
| `go vet ./...` in `connectors/traefik/native_middleware` | Bestanden. |
| `go test -count=1 -race ./...` in `connectors/envoy/ext_proc` | Für Command-, Composite- und Processor-Packages mit task-eigenen Cache-/Module-Cache-/Tmp-Pfaden bestanden. |
| `go vet ./...` in `connectors/envoy/ext_proc` | Bestanden. |
| Isolierter Unread-Body-Public-API-Go-Control | Bestand bei beobachtetem HTTP 204, null P2-Callbacks und `RequestEOS=false`; getrennt als payload-sichere lokale Evidenz aufbewahrt. |
| Standard Scoped Codex Security Scan | Abgeschlossen und versiegelt; 11 Records einschließlich eines lokal reproduzierten P0/high Findings. |
| Finding-JSON-/Backlog-/Roadmap-Konsistenzchecks | Lokal für die elf synchronisierten Records bestanden. |

## Runtime-Evidence

Der isolierte Unread-Body-Control ist eine fokussierte Go-Level-Reproduktion,
kein echter Traefik-Host-Test. Kein ausgewählter Apache-, NGINX-, HAProxy-,
Envoy-, Traefik- oder lighttpd-Host wurde gestartet. Daher wird kein Connector
promotet und keine P1–P4-Real-Host-Akzeptanzzelle behauptet.

## Nicht ausgeführte Prüfungen mit Begründung

- Real-Host-P1–P4-Matrix, ausgewählte Connector-Builds, Host-Konfiguration und
  Protokoll-Controls wurden nicht ausgeführt. Die erforderlichen Host-Binaries
  fehlen, und Produktreparatur wartet auf die Ownership-Entscheidung zu den
  Draft-PRs #344, #345 und #346.
- `make check-bilingual-docs` und `make check-doc-links` bleiben durch
  vorbestehende fehlende Framework-Gitlink-Targets im Parent-only-Worktree
  blockiert. Framework zu initialisieren oder Gitlinks zu ändern ist außerhalb
  des Scopes.

## Bekannte Einschränkungen

Die Scan-Coverage ist teilweise, weil reale Host-Binaries und das ausgewählte
Framework-Material nicht verfügbar sind. Source-Evidenz wird nicht zu einer
Exploit- oder Runtime-Behauptung erhoben. Das kanonische lokale Finding-System
und die aufbewahrte Scan-Evidenz bleiben außerhalb des versionierten
Produktdiffs.

## Verbleibende Risiken

`FND-PARENT-0958` bleibt ein P0/high-Delivery-Blocker.
`FND-PARENT-0959`–`FND-PARENT-0966` benötigen ihre aufgezeichneten
Runtime-Controls. Der Benutzer muss einen sauberen Integrations- oder
Ablösungspfad wählen, bevor eine Behebung ohne Konkurrenz zu den Draft-PRs
#344, #345 und #346 geschrieben werden kann. Kein Merge, direkter
`master`-Push, CI-Änderung, Framework/MRTS-Änderung, Gitlink-Update oder
Hosted-Erfolgsclaim ist autorisiert oder behauptet.

## Finaler Diff- und Review-Status

Der gepaarte Bericht und Change Record dokumentieren nur beobachtete
Scan-/Testergebnisse und das Delivery-Gate. Nach enger Dokumentationsvalidierung
sind sie für das nächste Draft-PR-Update bereit. Das umfassendere P1–P4-
Parity-Programm bleibt aktiv und kann nicht als abgeschlossen gemeldet werden.
