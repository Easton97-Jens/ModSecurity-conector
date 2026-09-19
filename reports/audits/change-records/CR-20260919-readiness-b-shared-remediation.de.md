# Change Record CR-20260919-readiness-b-shared-remediation: Gemeinsame Readiness-B-Remediation

**Sprache:** [English](CR-20260919-readiness-b-shared-remediation.md) | Deutsch

## Identität

| Feld | Wert |
| --- | --- |
| Change-ID | CR-20260919-readiness-b-shared-remediation |
| Datum (UTC) | 2026-09-19 |
| Basis-Revision | `e475baabf0787cbc804f176ae998b62156892825` |
| Scope | Ausschließlich gemeinsame Parent-Connector-Remediation, direkt betroffene Tests und gekoppelte Dokumentation. Keine Framework-, MRTS-, Gitlink-, Dependency-, Regelprofil-, Scanner-, Quality-Gate-, Workflow- oder Merge-Änderung ist enthalten. |
| Delivery-Status | Finaler lokaler Kandidat im dedizierten Worktree, bereit für einen aufgabeneigenen ersten Commit und die Einreichung eines Draft-PR. Exakte Commit- und PR-Identität werden erst nach Beobachtung eingetragen; kein Hosted-Check, Review-Ergebnis oder Merge wird hier behauptet. |
| Policy-Auflösung | Die Parent-Traceability-Policy verlangt dieses gekoppelte Record-Paar für die nicht triviale versionierte Arbeit; der etablierte Archivindex wird aktualisiert. |

## Motivation und Problemstellung

Die angeforderte Readiness-Prüfung über zehn Integrationen legte gemeinsam
behebbare Lücken offen, lieferte aber keine ausreichende vollständige Runtime-
Evidenz, um jeden Pfad auf Praxisreife B hochzustufen. Diese Änderung nimmt
enge Parent-eigene Korrekturen vor und bewahrt die Trennung zwischen Source- /
Contract-Evidenz und vollständiger Evidenz zu Host, Protokoll, Regelprofil,
Restart, Lifecycle und Observability.

## Akzeptanzkriterien

1. Die scoped Parent-eigenen Korrektheits- und Provenance-Lücken beheben, ohne
   Fail-Closed-, Ownership- oder Endpoint-Validation-Controls zu schwächen.
2. Unveränderliche Expat-Revisionsauswahl, Archive-Extraction-Ownership,
   Apache-APXS-Output-Platzierung und Peer-/lokale Endpoint-Provenance
   explizit und testbar halten.
3. Vollständige englisch/deutsche Dokumentation und dieses gekoppelte Change-
   Record-Paar pflegen.
4. Den tatsächlichen Reifegrad wahrheitsgemäß berichten: Diese scoped
   Remediation allein weist keine Praxisreife B für alle zehn Pfade nach.

## Implementierungsentscheidung und Begründung

- Der Expat-Component-Resolver verlangt in strikten und nicht strikten Pfaden
  unveränderliche vollständige Git-Objekt-IDs; veränderliche Referenzen und
  die Ersetzung durch das neueste Release gelten nicht als Pin-Evidenz.
- `TAR_OPTIONS="--no-same-owner"` wird für die NGINX-Source-Extraction
  erzwungen, damit Archivmetadaten während eines nicht privilegierten
  Handovers keine Ownership ändern können.
- Der Apache-APXS-Wrapper staged Profile-Registry-Inputs unter einem vom
  Aufrufer bereitgestellten externen Build-Root. Checkout-/Root-Symlinks und
  ein bereits vorhandenes symlinked `connectors`-Stage-Child werden vor dem
  Kopieren erzeugter Inputs abgelehnt.
- Stock-Lighttpd leitet Client-/Server-Endpoint-Metadaten mit `getpeername`
  und `getsockname` aus dem akzeptierten Sidecar-TCP-Socket ab; Unix-Domain-
  Sockets und unbrauchbare Endpoints werden abgewiesen, statt Request-Host-
  Metadaten zu verwenden.
- Das native Traefik leitet den Server-Endpoint aus `http.LocalAddrContextKey`
  ab; Request-`Host` bleibt Request-Metadatum und wird nicht als lokaler
  Engine-Endpoint vertraut.

## Security-Auswirkung

Diese Arbeit betrifft Supply-Chain-Pinning, Archive-Ownership, externe
Build-Output-Grenzen und Provenance von nicht vertrauenswürdigen HTTP-
Endpoints. Die Korrekturen bewahren Fail-Closed-Verhalten bei fehlenden oder
fehlerhaften Endpoints und verhindern, dass request-kontrollierte Host-
Metadaten zu einem lokalen UDS-/Engine-Endpoint werden. Sie schließen weder
das separat verfolgte Same-UID-UDS-Pathname-Replacement-Risiko
(`FND-PARENT-0015`) noch weisen sie eine wirksame Regelprofilabdeckung für die
2026-`t:hexDecode`-Advisory-Bedingung nach.

## Geänderte Dateien

- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `ci/provisioning/components/prepare-runtime-components.py`
- `connectors/apache/build/apxs-wrapper.in`
- `connectors/apache/README.md`
- `connectors/apache/README.de.md`
- `connectors/lighttpd/stock_sidecar/stock_sidecar.c`
- `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
- `connectors/lighttpd/README.md`
- `connectors/lighttpd/README.de.md`
- `connectors/traefik/native_middleware/middleware.go`
- `connectors/traefik/native_middleware/engine_uds_test.go`
- `connectors/traefik/native_middleware/middleware_test.go`
- `connectors/traefik/native_middleware/README.md`
- `connectors/traefik/native_middleware/README.de.md`
- `docs/reference/variables.md`
- `docs/reference/variables.de.md`
- `tests/test_prepare_runtime_components.py`
- `tests/test_apache_request_transaction_cleanup.py`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.md`
- `reports/audits/change-records/CR-20260919-readiness-b-shared-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Tests und tatsächliche lokale Ergebnisse

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| `tests.test_prepare_runtime_components` | Bestanden: 90 Tests; fünf Framework-HEAD-Mismatch-Fälle wurden übersprungen. |
| `tests.test_apache_request_transaction_cleanup` | Bestanden. |
| `tests.test_apache_apxs_profile_registry_staging` | Bestanden: 5 Fälle. |
| Finaler Apache-Autotools-Host-Lauf nach Hardening mit den gecachten nicht privilegierten Apache-/libModSecurity-Inputs | Lokal bestanden: Modul-Laden, Allow-/Block-Verhalten und die dokumentierten Transaction-ID-Controls wurden abgeschlossen. Dies ist begrenzte lokale Host-Evidenz, keine Evidenz für jeden Connector- oder Protokollpfad. |
| HAProxy-SPOP-zu-HTX-Combined-bounded-Host-Lauf | Lokal als nicht privilegierter isolierter Pfad mit dem source-gebauten aktuellen SPOP-Adapter und HAProxy HTX bestanden. Dies ist begrenzte Evidenz für diesen Combined-Pfad, keine Standalone-HTX-Evidenz und keine vollständige B-Klassen-G2–G6-/54-Fälle-Evidenz. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` mit `CC=clang` | Bestanden: 18 Tests. |
| `connectors/lighttpd/tests/test_stock_sidecar_contract.py` mit `CC=cc` | Bestanden: 18 Tests. |
| Natives Traefik-Go-Modul `go test -mod=readonly ./...` | Bestanden. |
| Natives Traefik `go vet ./...` und `gofmt -d`-Review | Bestanden; `gofmt -d` erzeugte keinen Diff. |
| Natives Traefik `FuzzUDSFrameAndResult` für 15 Sekunden | Bestanden. |
| `git diff --check` während der scoped Implementierung | Bestanden. |
| `make check-variable-documentation` | Bestanden: 100 dokumentierte Variablenreferenzen gescannt. |
| `make check-bilingual-docs` und `make check-doc-links` | Ausschließlich durch den nicht materialisierten Framework-Gitlink blockiert; jedes ausgegebene Ziel liegt unter `modules/ModSecurity-test-Framework`. |

## Ausgeführte Befehle

Alle Befehle wurden über den Repository-RTK-Proxy ausgeführt. Die beobachtete
lokale Validierung umfasste die fokussierten Python-Auswahlen
`tests.test_prepare_runtime_components`,
`tests.test_apache_request_transaction_cleanup` und
`tests.test_apache_apxs_profile_registry_staging`; den Apache-Autotools-
Bootstrap-Check; `connectors/lighttpd/tests/test_stock_sidecar_contract.py`
mit `CC=clang` und `CC=cc`; sowie die nativen Traefik-Befehle
`go test -mod=readonly ./...`, `go vet ./...`, `gofmt -d` und den
15-sekündigen `FuzzUDSFrameAndResult`-Lauf. Der ausgeführte HAProxy-Host-
Control war `connectors/haproxy/harness/combined_spop_htx/run_combined_spop_htx.sh`
mit einem isolierten nicht privilegierten Runtime-Root und dem aktuellen
Combined-SPOP-zu-HTX-Pfad. `git diff --check` und
`make check-variable-documentation` bestanden während der scoped Arbeit. Die
repositoryweiten Bilingual-/Link-Targets wurden ausgeführt, sind aber
ausschließlich durch den separat besessenen, nicht materialisierten Framework-
Gitlink blockiert. Die obige Tabelle hält die tatsächlich beobachteten
Ergebnisse fest; kein unbeobachteter Hosted- oder Produktionsbefehl wird als
ausgeführt dargestellt.

## Runtime-Evidence

Der finale Apache-Bootstrap- und der HAProxy-SPOP-zu-HTX-Combined-Lauf sind
tatsächliche lokale nicht privilegierte Host-Evidenz innerhalb ihrer begrenzten
Fixtures. Der HAProxy-Lauf startet Standalone-HTX nicht erneut und deckt weder
die vollständigen B-Klassen-G2–G6 noch die 54-Fälle-Matrix ab. Die Lighttpd-
und Traefik-Ergebnisse sind Source-, Contract- und Go-Modul-Evidenz; sie
ersetzen keinen unabhängig gestarteten Produktivhost mit den erforderlichen
Regeln, Lifecycle-Controls, Logs, Metriken, Restart-, HTTP/1.1-, HTTP/2- und
HTTP/3-Evidenz. Es wird nicht behauptet, dass nun alle zehn Integrationspfade
B-Klassen-Runtime-Evidenz besitzen.

## Nicht ausgeführte Prüfungen mit Begründung

- Eine vollständige Evidenzmatrix für zehn Pfade, einschließlich aller
  erforderlichen Protokoll- und Lifecycle-Dimensionen, ist bei diesem Record-
  Snapshot nicht abgeschlossen.
- Wirksames externes Regelprofil-Testing für die `t:hexDecode`-Advisory-
  Bedingung ist nicht gelaufen; Checked-in-Source-Inspektion kann die
  verwendeten Regeln eines Deployments nicht beweisen.
- Vollständige Host-Evidenz für NGINX, beide Envoy-Pfade, Standalone-HAProxy-
  HTX, Traefik-forwardAuth, Stock-Lighttpd und gepatchtes Lighttpd wird hier
  nicht behauptet. Der Combined-HAProxy-SPOP-zu-HTX-Lauf bleibt unterhalb
  vollständiger B-Klassen-G2–G6- und 54-Fälle-Evidenz.
- Exact-Head-Hosted-CI, SonarQube Cloud, Review, Mergeability und PR-
  Ergebnisse liegen noch nicht vor und dürfen nicht aus lokalen Checks
  abgeleitet werden. Die Voraussetzungen der repositoryweiten Bilingual-/Link-
  Targets sind ebenso durch den separat besessenen nicht materialisierten
  Framework-Gitlink blockiert.

## Bekannte Einschränkungen

Das angeforderte Ergebnis — nachgewiesene B-Reife für alle zehn
Integrationspfade — ist bei diesem Snapshot nicht erreicht. Die Korrekturen
beheben nur die aufgeführten gemeinsamen Lücken. FND-PARENT-0015 bleibt offen,
Host-/Runtime-Voraussetzungen sind für mehrere Pfade blockiert oder nicht
verifiziert, und das wirksame Regelprofil zur Bewertung der `t:hexDecode`-
Bedingung wurde nicht bereitgestellt.

## Verbleibende Risiken

Die korrigierte Endpoint-Behandlung kann nicht selbst beweisen, dass jeder
Embedding-Host eine vertrauenswürdige lokale Adresse liefert. Die Local-
Address-Validierung schlägt daher fail-closed fehl. Archive- und APXS-
Korrekturen ersetzen keinen frischen Host-Build für jede unterstützte
Deployment-Konfiguration. Für die Advisory-Bedingung wird ohne das tatsächlich
aktivierte Regelprofil weder ein verwundbarer noch ein betroffener Status
behauptet.

## Finaler Diff- und Review-Status

Dies ist ein partieller Parent-only-Remediation-Record. Er beschreibt
beobachtete lokale Evidenz und bekannte Grenzen, zertifiziert aber weder das
Zehn-Pfad-B-Ziel noch ein Release, ein Hosted-Qualitätsergebnis, einen Pull
Request oder einen Merge. Finaler Scoped-Diff und source-lokale
Dokumentationschecks sind abgeglichen; repositoryweite Dokumentations-Targets
sind wahrheitsgemäß durch den fehlenden Framework-Gitlink blockiert. Exakte
Commit-/PR-Fakten werden nach ihrer Beobachtung ergänzt; die verbleibende
Runtime-Evidenz bleibt Follow-up-Pflicht.
