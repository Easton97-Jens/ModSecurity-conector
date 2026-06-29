# Open Connectors CI Evidence Status

**Sprache:** [English](open-connectors-ci-evidence-status.md) | Deutsch

## Zusammenfassung

Der finale manuelle `workflow_dispatch`-Lauf fuer
`Open Connector Runtime Smokes` wurde auf `master` erfolgreich abgeschlossen.

Envoy, Traefik und Lighttpd haben jetzt CI-Evidence fuer:

- einfachen Runtime-Smoke
- gezielten ModSecurity-Smoke
- Minimal-CRS-Smoke
- sekundaeren CRS-Smoke

Request-Body-Smoke-Unterstuetzung wurde nach diesem dokumentierten Lauf als
separate Evidence-Stufe ergaenzt. Ein neuer `workflow_dispatch`-Lauf ist
erforderlich, bevor dieser Report beobachtete Request-Body-PASS-Evidence
ausweisen kann.

Lighttpd hat zusaetzlich CI-Evidence fuer:

- lokalen Source-Build

Dieser Report fasst nur beobachtete Smoke-Evidence zusammen. Er bewirbt keine
Production-Readiness, keine Full-Matrix-Readiness, keine CRS-Vollstaendigkeit
und keine Response-Body-Verifikation.

## Workflow-Lauf

- Workflow-Name: `Open Connector Runtime Smokes`
- Workflow-Datei: `.github/workflows/open-connectors-smoke.yml`
- Event: `workflow_dispatch`
- Branch: `master`
- Commit: `b48506c72351b5ea1552c98a144c413fab7fa1e4`
- Run-ID: `28376822599`
- Run-Status: `success`
- Dauer: `13m 20s`
- Artefakte: `2`
- Artefaktnamen:
  - `open-connectors-smoke-evidence`
  - `open-connectors-final-checks`

Artefakt-Metadaten:

| Artefakt | Groesse | Digest |
| --- | --- | --- |
| `open-connectors-smoke-evidence` | `907555153` Bytes | `sha256:1f973bc6b0e8a393fe6a3be7f9b5b78518ff23df072f387d0a93a19544382da8` |
| `open-connectors-final-checks` | `3181` Bytes | `sha256:dd978f0e1996f30a04b99b987b00199611292ab0ed6c895ef922a50c54439782` |

## Statusmatrix

| Connector | Build | Simple Runtime | Targeted ModSecurity | Minimal CRS | Secondary CRS | Integration Mode |
| --------- | ----- | -------------- | -------------------- | ----------- | ------------- | ---------------- |
| Envoy | n/a | PASS 200/403 | PASS 200/403 | PASS 200/403 | PASS 200/403 | ext_authz |
| Traefik | n/a | PASS 200/403 | PASS 200/403 | PASS 200/403 | PASS 200/403 | forwardAuth |
| Lighttpd | PASS | PASS 200/403 | PASS 200/403 | PASS 200/403 | PASS 200/403 | sidecar_proxy |

## Evidence-Artefakte

`open-connectors-smoke-evidence` enthaelt das Runtime-Evidence-Buendel, das aus
`ci-artifacts/open-connectors/` hochgeladen wurde. Der Workflow kopiert
`/tmp/ModSecurity-conector-verified/` nach `verified-root/`; dadurch enthaelt
das Artefakt die Result-Dateien, Logs, Audit-Logs, Decision-Logs,
Request-Transcripts, soweit vom jeweiligen Connector-Smoke erzeugt, und
Runtime-Inventory-Ausgaben des Laufs.

`open-connectors-final-checks` enthaelt Final-Check-Diagnosen fuer:

- `lint.log`
- `quick-check.log`
- `git-diff-check.log`
- finalen Git-Status und Git-Diff-Zusammenfassungen

Die Final Checks waren erfolgreich:

- `make lint`
- `make quick-check`
- `git diff --check`

## CRS-Evidence

Minimal-CRS-Smoke:

- Probe-Typ: SQLi-Probe
- Erwartete beobachtete Regel: `949110`
- Erwartete Message: `Inbound Anomaly Score Exceeded`
- Scope: nur beobachtete Smoke-Evidence

Sekundaerer CRS-Smoke:

- Probe-Typ: XSS-Probe
- Erwartete beobachtete Regel: `941100`
- Erwartete Message: `XSS Attack Detected via libinjection`
- Scope: nur beobachtete Smoke-Evidence

Diese CRS-Smokes sind keine CRS-Complete-Evidence.

## Nach diesem Lauf ergaenzte Request-Body-Evidence

Workflow und Make-Targets enthalten jetzt einen gezielten Request-Body-Smoke
fuer Envoy, Traefik und Lighttpd:

- `make smoke-envoy-request-body`
- `make smoke-traefik-request-body`
- `make smoke-lighttpd-request-body`
- `make smoke-open-connectors-request-body`

Erwartete Request-Body-Evidence-Dateien:

- `$<CONNECTOR>_RESULT_ROOT/request-body-result.json`
- `$<CONNECTOR>_LOG_ROOT/request-body-decision.log`
- `$<CONNECTOR>_LOG_ROOT/request-body-request-transcript.jsonl`

Der Smoke verwendet `common/rules/modsecurity_request_body_smoke.conf`,
POST-Bodies und Regel `1000002`. Er darf `request_body_smoke_verified=true`
nur setzen, wenn der erlaubte POST 200 liefert und der geblockte Body-Marker
`modsec-request-body-block` via libmodsecurity 403 liefert. Das ist keine
Response-Body-Verifikation.

## Connector-Scope

Envoy:

- Integration mode: `ext_authz`
- Runtime-Komponente: gepinnte Envoy-Binary
- Kein Source-Compile

Traefik:

- Integration mode: `forwardAuth`
- Runtime-Komponente: gepinntes Traefik-Release-Archiv
- Kein Source-Compile

Lighttpd:

- Integration mode: `sidecar_proxy`
- Lokaler Source-Build
- Phase-1-Sidecar-Proof
- Kein nativer Lighttpd-ModSecurity-Connector

## Explizit nicht gesetzte Claims

Die folgenden Claims bleiben verboten und werden durch diese Evidence nicht
gesetzt:

- `production_ready=true`
- `full_matrix_ready=true`
- `crs_complete=true`
- `response_body_verified=true`

## Verbleibende Arbeit

1. SonarCloud-Triage bleibt ein separater Track.
2. `Open Connector Runtime Smokes` erneut manuell laufen lassen, um
   Request-Body-CI-Artefakt-Evidence zu sammeln.
3. Audit-Log-Schema-Validierung sollte als eigene Evidence-Stufe ergaenzt werden.
4. Weitere CRS-Kategorien koennen ohne CRS-Complete-Claim ergaenzt werden.
5. Response-Body-Evidence sollte getrennt bleiben, bis sie explizit verifiziert ist.
