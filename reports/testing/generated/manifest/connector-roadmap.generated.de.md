> Generated file - do not edit manually.
>
> Generated at: `2026-07-11T05:59:47Z`
> Verified run id: `2026-07-11T05-59-47Z-e64adac0`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-connector-roadmap.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `e64adac087abaa8c1bb7e220d16c7f34a0e9bd79`
> Framework SHA: `de0fc5dc0751d3b0e8cb1bd5187e4e3ff558f41f`
> Input status: `complete`

# Archivierte Connector-Roadmap vor dem kanonischen No-CRS-Modell

**Sprache:** [English](connector-roadmap.generated.md) | Deutsch

> Hinweis: Diese deutsche Datei ist eine übersetzte Begleitdatei zur generierten englischen Quelle. Maschinenlesbare Werte, Statusnamen, Pfade und Tabellen bleiben absichtlich unverändert.

## Archivgrenze und maßgeblicher aktueller Status

Dieser Bericht ist `roadmap_only` und bleibt ein historischer Planungsstand vor dem kanonischen Modell.
Für den aktuellen Status gelten `reports/all-connectors-no-crs-baseline.*` und `reports/testing/generated/canonical/connector-capabilities.generated.*`; nur kanonische `result.json`-Evidence darf ein Ergebnis heraufstufen.

| Feld | Wert |
|---|---|
| report_scope | roadmap_only |
| snapshot_kind | historical_precanonical_roadmap |
| evaluates | historical repository structure, skeletons, technical feasibility, first proof steps, and evidence gates |
| does_not_replace | the canonical capability catalog, canonical No-CRS result evidence, or full-matrix evidence |
| current_status_authority | reports/all-connectors-no-crs-baseline.* and reports/testing/generated/canonical/connector-capabilities.generated.* |
| full_matrix_results_created | False |
| runtime_pass_fail_values_created | False |
| merge_readiness_impact | none |

## Aktuelle kanonische Host-Pfade

Diese Tabelle wird bei jeder Erzeugung aus den sechs `connectors/<name>/capabilities.json`-Manifesten gelesen. Die Zustände sind Source-/Capability-Deklarationen und keine PASS-Ergebnisse.

| Connector | Host | Integration | Minimal-Runtime-Deklaration | No-CRS-Deklaration |
|---|---|---|---|---|
| apache | apache | native-httpd-module | implemented_not_asserted | supported_not_verified |
| nginx | nginx | native-nginx-http-module | implemented_not_asserted | supported_not_verified |
| haproxy | haproxy | spoe-spop-agent | implemented_not_asserted | supported_not_verified |
| envoy | envoy | http-ext-authz-service | implemented_not_asserted | supported_not_verified |
| traefik | traefik | http-forwardauth-service | implemented_not_asserted | supported_not_verified |
| lighttpd | lighttpd | native-lighttpd-plugin | implemented_not_asserted | supported_not_verified |

## Archiviertes Planungsmaterial vor dem kanonischen Modell

> Die nachfolgenden Status-, Ranking-, Machbarkeits- und Proof-Aussagen sind ausschließlich historische Planung. Sie dürfen keine aktuellen Capability-, Runtime-, CRS- oder Ergebnisclaims begründen.

## Archivierte Connector-Statusmatrix

| Connector | Verzeichnis | Historischer Snapshot-Status | Warum | Nächster Schritt | Runtime-Evidence? | Full-Matrix? |
|---|---|---|---|---|---|---|
| apache | yes | production_verified | Existing production connector with verified runtime and full-matrix coverage. | Keep in verified runtime/full-matrix maintenance. | yes | yes |
| nginx | yes | production_verified | Existing production connector with verified runtime and full-matrix coverage; OpenResty is NGINX-based. | Keep production coverage and optionally add OpenResty compatibility smoke under nginx later. | yes | yes |
| haproxy | yes | production_verified | Existing production connector with verified runtime and full-matrix coverage; SPOE path is documented. | Keep production coverage and capability notes current. | yes | yes |
| envoy | yes | partial_skeleton | Repository has an Envoy bridge starter and harness entrypoint, but no runtime-verified Envoy integration yet. | Define and run a targeted ext_proc/ext_authz runtime smoke proof; do not start full matrix. | targeted proof required | no |
| lighttpd | yes | partial_skeleton | Repository has a lighttpd bridge starter, but no native module/FastCGI/SCGI runtime integration. | Write a request-blocking feasibility note and select native-module versus sidecar/proxy architecture. | targeted proof required | no |
| traefik | yes | partial_skeleton | Repository has a decision-service starter, but no Traefik Go plugin/middleware or runtime harness. | Prototype forwardAuth/decision-service feasibility before any Go plugin implementation. | targeted proof required | no |
| litespeed | no | planned | No repository directory exists; LiteSpeed/OpenLiteSpeed is only a candidate until install/licensing proof exists. | Run OpenLiteSpeed install/start proof with one CRS/request-blocking smoke if automation allows it. | no | no |
| openresty | no | covered_by_existing_connector | OpenResty is based on the NGINX runtime stack and should not fork connector ownership now. | Treat as nginx runtime variant or compatibility smoke only; no separate reports or full matrix. | no | no |

## Archived Connector Candidate Ranking

| Rank | Connector | Difficulty | Risk | Expected Value | Recommendation |
|---|---|---|---|---|---|
| 1 | envoy | high | medium-high | high | Next proof: targeted ext_proc/ext_authz runtime smoke with request blocking and explicit non-goals. |
| 2 | litespeed | medium | high | medium-high | Run OpenLiteSpeed installation/licensing proof before adding a connector directory. |
| 3 | traefik | medium-high | high | medium | Prototype forwardAuth/decision-service feasibility before any Go plugin work. |
| 4 | lighttpd | high | high | medium | Perform hook/proxy architecture spike before implementation. |

## Archived Rationale for Recommending Envoy Next

| Reason | Detail | Evidence Boundary |
|---|---|---|
| Existing repository foothold | The repo already contains an Envoy connector directory, bridge starter, metadata, and smoke entrypoint, so the next step can be a focused proof instead of an unbounded scaffold. | Existing files prove only a skeleton; they do not prove runtime behavior. |
| Clear request-control surfaces | Envoy has documented HTTP extension points such as ext_proc and ext_authz that can return an intervention-style deny before upstream routing. | The roadmap may recommend these surfaces, but support starts only after a targeted case writes result.json and logs. |
| Reusable decision-service pattern | A small external decision service can also inform later Traefik forwardAuth and lighttpd sidecar feasibility work. | Reusable architecture is a planning advantage, not a Full-Matrix or CRS support claim. |
| High value with bounded first proof | A single request-blocking smoke can answer whether Envoy can carry a ModSecurity-style deny decision without touching production connectors. | The first proof is targeted and must keep full_matrix_ready=false. |

## Connector Lifecycle

| Stage | Meaning | Required Evidence | Not Allowed Claims |
|---|---|---|---|
| planned | Candidate is tracked but no connector directory or selected runtime architecture is required yet. | Roadmap entry, rationale, risks, and first proof definition. | No runtime support, no blocking support, no CRS support, no verified-case readiness. |
| skeleton | Connector directory or starter exists with README/metadata/build notes, but no real runtime proof. | Repo-owned scaffold, origin notes, build or self-test starter, and explicit non-runtime disclaimer. | No production readiness, no verified runtime result, no full-matrix eligibility. |
| buildable | Starter or adapter component compiles from clean checkout with documented command. | Build command, artifact path outside checkout, source map, and passing syntax/lint checks. | No traffic handling or ModSecurity semantics unless runtime logs prove them. |
| runtime-startable | Server/proxy and any sidecar can start locally with minimal configuration. | Start/stop or run script, minimal config, process logs, port allocation, and cleanup behavior. | No verified blocking or CRS coverage without a case result and logs. |
| verified-case-ready | A targeted real runtime case can produce result.json and logs under verified runtime root. | result.json, case-run JSON/Markdown, access/error logs or equivalent, decision/audit evidence where applicable. | No full-matrix readiness, no broad phase coverage, no production_verified status. |
| full-matrix-candidate | Full-matrix jobs are technically schedulable for the connector, but may still fail or be incomplete. | Matrix job definitions, runtime result producer, report integration, known limitation notes, and governance/lint pass. | No PASS/Merge Readiness claims until generated full-matrix evidence supports them. |
| production-verified | Connector passed the complete verified evidence pipeline and is included in production status. | Verified runtime evidence, full matrix, governance, lint, quick-check, report layout, and merge-readiness PASS. | Do not claim if any required generated evidence is blocked, stale, or missing. |
| covered-by-existing-connector | Runtime is intentionally covered as a variant of an existing connector rather than a separate connector. | Decision record that names owning connector and allowed future compatibility-smoke path. | No separate full matrix, generated reports, or production connector identity. |
| blocked | Implementation cannot proceed until an external, licensing, architecture, or evidence blocker is resolved. | Blocker description, owner/next proof, and what evidence would unblock it. | No forward status promotion until the blocker is removed and evidenced. |

## Archived New-Connector Work Phases

| Phase | Name | Entry Condition | Work | Exit Evidence | Promotion Gate |
|---|---|---|---|---|---|
| 0 | Roadmap triage | Candidate appears in repository skeletons, backlog, or architecture discussion. | Record status, rationale, risks, first proof, and forbidden claims. | Roadmap-only generated report and optional architecture/onboarding docs. | No runtime promotion; this phase only authorizes a proof plan. |
| 1 | Architecture proof specification | Candidate has enough technical surface to compare integration options. | Choose one minimal control point, name alternatives, define logs, result schema, and non-goals. | Documented proof spec with acceptance criteria and rollback/cleanup expectations. | A proof may be implemented, but no Full-Matrix job may be added yet. |
| 2 | Targeted runtime smoke | Proof spec is accepted and can run without production connector changes. | Create minimal config, launcher, upstream, decision service, and one blocking smoke. | result.json, case-run files, access/error logs or equivalent, and decision/audit logs where applicable. | The smoke proves only the named case and must keep full_matrix_ready=false. |
| 3 | Verified-case readiness | Targeted smoke is deterministic and uses verified runtime paths. | Wire the connector into the verified-case runner shape with documented capabilities and limitations. | A real verified-case run for one case, with rerun command and artifact locations. | May become a full-matrix candidate only after governance, lint, quick-check, and evidence layout pass. |
| 4 | Full-Matrix candidacy | Verified-case evidence exists and missing capability claims are explicitly documented. | Add matrix job plumbing and generated-report integration without altering expected statuses. | Full-Matrix jobs are schedulable and report completeness can describe generated evidence honestly. | No PASS, readiness, or production claim until complete generated Full-Matrix evidence exists. |
| 5 | Production verification | Full-Matrix evidence is complete and critical reports are generated from verified inputs. | Run the complete verified evidence pipeline and resolve mismatches through real fixes only. | Merge Readiness PASS, critical mismatches 0, governance/lint/quick-check/layout PASS. | Only now may the connector be described as production_verified. |

## New Connector Acceptance Criteria

| Requirement | Required for Skeleton | Required for Verified-Case | Required for Full-Matrix |
|---|---|---|---|
| connectors/<name>/README.md | yes | yes | yes |
| build/start/stop or run script | build starter allowed | yes | yes |
| minimal config | recommended | yes | yes |
| verified-case support | no | yes | yes |
| result.json | no | yes | yes |
| access/error logs or equivalent | no | yes | yes |
| audit evidence if supported | document support | yes if supported | yes if supported |
| decision evidence if applicable | document support | yes | yes |
| capability notes | yes | yes | yes |
| request blocking smoke | no | yes | yes |
| request body smoke or documented not-supported reason | no | yes | yes |
| clean report-governance/lint/quick-check | yes | yes | yes |

## Future Files, Targets, and Reports

| Item | Stage | Purpose | Evidence Rule |
|---|---|---|---|
| connectors/<name>/README.md | skeleton | Describe connector scope, current lifecycle stage, build/runtime commands, and explicit non-claims. | Required before any connector is listed as more than planned. |
| connectors/<name>/ORIGIN.md and SOURCE_MAP.json | skeleton | Track source ownership, upstream references, and which files are repo-owned. | Must not imply runtime support. |
| connectors/<name>/config/ or harness config | runtime-startable | Provide minimal deterministic proxy/server configuration for local smoke runs. | Config presence is not runtime evidence until a run writes logs and result.json. |
| connectors/<name>/harness/ or scripts/run-smoke.sh | runtime-startable | Start, exercise, and clean up the minimal proof harness. | Must write artifacts under verified runtime roots, not inside the checkout. |
| make smoke-<name> or equivalent launcher | runtime-startable | Expose a small local smoke for developers and CI feasibility. | A smoke target alone is not Full-Matrix integration. |
| make verified-case CONNECTOR=<name> CASE=<case> | verified-case-ready | Run one real case through the verified-case evidence shape. | Requires result.json, logs, case-run files, and truthful expected/actual status. |
| reports/testing/generated/runtime/<name>-runtime-results.generated.md | verified-case-ready | Summarize real runtime evidence once a generator consumes verified inputs. | Must be generated, never hand-edited, and must not be present for roadmap-only candidates. |
| make verified-full-matrix-job CONNECTOR=<name> CRS=<variant> MRTS=<variant> | full-matrix-candidate | Run a schedulable connector/CRS/MRTS matrix job. | Schedulable is not PASS; report actual status only after real execution. |
| reports/testing/generated/manifest/full-matrix-job-completeness.generated.* | full-matrix-candidate | Record which jobs exist, completed, failed, or are missing. | Do not fabricate job rows for connectors that are not integrated. |
| reports/testing/generated/manifest/merge-readiness-dashboard.generated.* | production-verified | Expose final readiness only after critical generated evidence is complete. | Roadmap-only reports must not influence readiness. |

## Archived Envoy Architecture Options

| Option | Description | Pros | Cons | Proof Difficulty | Recommendation |
|---|---|---|---|---|---|
| ext_proc sidecar | Envoy External Processing gRPC service that can inspect configured request/response processing points. | Best fit for staged request/body/response experiments; external process can own ModSecurity lifecycle and evidence logs. | Requires protobuf/gRPC service and careful body processing-mode limits; response-body intervention semantics need proof. | medium-high | primary proof path together with a minimal request-blocking case |
| ext_authz service | Envoy authorization service that returns allow/deny before routing to upstream. | Simple request blocking proof; easy to reason about 403 decisions and logs. | Primarily authorization-oriented; request body/response body coverage is limited and not a full ModSecurity phase mapping. | medium | acceptable first smoke if ext_proc is too heavy; pair with clear body/response non-goals |
| WASM filter | Proxy-Wasm HTTP filter embedded in Envoy filter chain. | Native filter-chain placement and possible phase visibility. | Higher toolchain complexity; embedding libmodsecurity or a robust bridge is risky; evidence and debugging are harder. | high | defer until sidecar proof confirms required semantics |
| Lua filter | Envoy Lua HTTP filter that calls or models an external decision service. | Fast prototype for header/path decisions. | Not a strong long-term ModSecurity integration; body and response handling are constrained. | medium | use only as fallback feasibility spike, not preferred connector path |
| reverse-proxy chain with existing connector | Envoy fronts an existing verified connector such as nginx or apache. | Fast compatibility smoke and infrastructure proof. | Does not prove an Envoy connector; ModSecurity decision belongs to downstream connector. | low-medium | allowed only as infrastructure smoke, not as Envoy connector evidence |
| external ModSecurity decision service | Standalone service owns ModSecurity transaction evaluation; Envoy calls it through ext_proc/ext_authz or another control point. | Clear separation of Envoy harness and ModSecurity lifecycle; reusable for Traefik/lighttpd sidecar studies. | Protocol mapping and body buffering still must be proven; not a connector by itself. | medium-high | use as shared service behind ext_proc/ext_authz proof |

### Archived Envoy Option Capability Checks

| Option | Request Blocking | Request Body | Response Body | Intervention Status | Evidence | CI Testability | Risk |
|---|---|---|---|---|---|---|---|
| ext_proc sidecar | yes, if the processor returns a denied/modified response before upstream forwarding | possible, subject to Envoy processing mode and buffering settings | possible in concept, but not claimed until explicitly evidenced | map ModSecurity disruptive intervention to Envoy processor response/denied status | Envoy logs, processor logs, decision log, result.json, case-run files | good after pinned Envoy binary/container and deterministic ports | medium-high |
| ext_authz service | yes | limited/config-dependent; do not claim broad request-body support in first proof | no practical response-body claim for first proof | map deny decision to ext_authz denied response status 403 | Envoy logs, authz service logs, decision log, result.json, case-run files | good | medium |
| WASM filter | possible but not proven | possible but SDK/runtime constrained | possible but high risk | filter must translate decisions into local responses/stream actions | Envoy logs plus WASM module logs; more complex CI artifacts | moderate to poor for first proof | high |
| Lua filter | yes for simple cases | limited | not a first-proof claim | Lua script returns local 403 or delegates to sidecar | Envoy logs, Lua log messages, sidecar logs if used | good for a smoke, weak for connector semantics | medium-high |
| reverse-proxy chain with existing connector | yes, but by the existing connector rather than Envoy | covered by existing connector only | covered by existing connector only | downstream connector returns status; Envoy only forwards it | Envoy forwarding logs plus existing connector logs | good | low for smoke, high if misrepresented |
| external ModSecurity decision service | yes through caller integration | depends on caller body delivery | depends on caller response delivery | service returns intervention_status and decision fields consumed by Envoy adapter layer | service decision log, ModSecurity audit/decision log, Envoy logs, result.json | good if implemented as deterministic local process | medium |

## Archived Recommended Envoy Proof

| Field | Value |
|---|---|
| name | Minimal Envoy ext_proc/ext_authz runtime smoke |
| scope | targeted proof only; not a full connector and not a full-matrix producer |
| runtime_root | $VERIFIED_RUN_ROOT/envoy-smoke/ |
| goals | Envoy starts locally with a deterministic minimal config.<br>A simple upstream responds through Envoy.<br>A ModSecurity-like decision service or sidecar can emit a deny decision.<br>A case such as action_deny_phase1 or envoy_request_blocking_smoke returns HTTP 403.<br>Logs and decision evidence are written under the verified runtime root.<br>No full-matrix integration is added for this proof. |
| artifacts | connectors/envoy/README.md<br>connectors/envoy/config/envoy.yaml<br>connectors/envoy/harness/<br>connectors/envoy/scripts/run-smoke.sh<br>connectors/envoy/examples/ |
| evidence | result.json<br>envoy access log<br>envoy error log<br>decision-service log<br>modsecurity decision log, if present<br>case-run.md<br>case-run.json |

### Archived Envoy Proof Exit Criteria

| Criterion | Required Evidence | Failure Mode |
|---|---|---|
| Local startup | Envoy, upstream, and decision service start from a deterministic script and clean up ports/processes. | If startup is flaky, the proof remains skeleton/runtime-startable work only. |
| Upstream pass-through | A benign request reaches the upstream through Envoy and logs the route. | If upstream pass-through fails, no ModSecurity-style decision claim is allowed. |
| Request blocking | A known malicious smoke request returns HTTP 403 via the selected ext_proc/ext_authz path. | If only the upstream blocks, the result is an infrastructure smoke, not Envoy connector proof. |
| Decision evidence | Decision-service log records deny, intervention_status=403, case id, and request correlation id. | If decision evidence is missing, the HTTP status is insufficient for verified-case readiness. |
| Runtime evidence package | result.json, case-run.md, case-run.json, Envoy logs, and decision logs under $VERIFIED_RUN_ROOT/envoy-smoke/. | If artifacts live only in the checkout or are incomplete, do not promote the proof. |
| Scope guard | result.json declares evidence_scope=targeted and full_matrix_ready=false. | Any Full-Matrix or production claim invalidates the first-proof boundary. |

### Archived Envoy Minimal Result Schema

```json
{
  "connector": "envoy",
  "case": "envoy_request_blocking_smoke",
  "expected_status": 403,
  "actual_status": 403,
  "status": "pass",
  "decision": "deny",
  "intervention_status": 403,
  "evidence_scope": "targeted",
  "full_matrix_ready": false
}
```

### Envoy Non-Goals

- No CRS support in first proof.
- No MRTS support in first proof.
- No full matrix.
- No response-body support claim.
- No production_verified claim.
- No merge-readiness impact.

## LiteSpeed / OpenLiteSpeed Candidate

| Field | Value |
|---|---|
| candidate | LiteSpeed / OpenLiteSpeed |
| status | planned |
| edition_note | OpenLiteSpeed is likely more CI-friendly; LiteSpeed Enterprise may add license/download automation risk. |
| install_path | Prefer package/container proof if license and automation permit it. |
| modsecurity_crs_support | Must be proven with the selected edition; do not assume libmodsecurity-v3 connector parity. |
| first_proof | OpenLiteSpeed install/start proof plus one CRS/request-blocking smoke, if automation and licensing allow it. |
| main_risk | License/download automation, edition differences, ModSecurity-engine compatibility, package availability, and CI reproducibility. |
| evidence_required | install log, start log, minimal config, request/response transcript, result.json, access/error/audit logs if available. |
| not_allowed_claims | No production status, no full matrix, no CRS compatibility claim, and no phase coverage claim before evidence exists. |

## Archived Lighttpd and Traefik Feasibility

| Connector | Historical State | Blocker | First Proof Step | Risk |
|---|---|---|---|---|
| lighttpd | partial_skeleton | No selected native ModSecurity integration, FastCGI/SCGI bridge, or runtime harness. | Request-blocking feasibility proof that selects native module versus proxy/sidecar architecture. | high |
| traefik | partial_skeleton | No Go plugin/middleware, no forwardAuth runtime harness, and no libmodsecurity lifecycle proof. | forwardAuth/decision-service returns 403 for a known malicious request with logs and result.json. | high |

## OpenResty Decision

| Field | Value |
|---|---|
| decision | covered_by_nginx |
| separate_connector | no |
| future_option | nginx runtime variant / compatibility smoke |
| reason | NGINX-based stack |
| full_matrix | no separate full matrix |
| reports | no separate generated reports |

## Archived New-Connector Work Items

| Priority | Work Item | Connector | Output | Acceptance Criteria |
|---|---|---|---|---|
| 1 | Envoy architecture proof spec | envoy | documented ext_proc/ext_authz choice and non-goals | Roadmap and onboarding docs name protocol, evidence, and blocked claims. |
| 2 | Envoy minimal smoke harness skeleton | envoy | envoy.yaml, run-smoke.sh, upstream/decision-service launcher plan | Can start Envoy and upstream locally without full-matrix integration. |
| 3 | Envoy result/evidence schema | envoy | targeted result.json and case-run schema | Schema includes connector, case, expected/actual status, decision, intervention_status, evidence_scope, and full_matrix_ready=false. |
| 4 | LiteSpeed install feasibility proof | litespeed | OpenLiteSpeed install/start feasibility notes | Documents license/download path, automation risk, and one request-blocking proof fixture. |
| 5 | OpenResty compatibility-smoke decision | openresty | nginx-owned compatibility-smoke decision | No separate connector, no separate full matrix, no separate generated reports. |
| 6 | Lighttpd feasibility note | lighttpd | native-module versus sidecar/proxy feasibility note | Identifies first request-blocking hook and evidence that would prove it. |
| 7 | Traefik forwardAuth feasibility note | traefik | decision-service/forwardAuth proof note | Known malicious request returns 403 with decision logs in targeted proof. |

## Claims Not Allowed Before Full-Matrix Evidence

- production_verified status
- merge-readiness contribution
- full-matrix PASS/FAIL counts
- CRS support across variants
- MRTS support
- response-body blocking support
- phase coverage parity with apache/nginx/haproxy
- runtime capability claims without result.json and logs

## Archived Recommended Next Connector

| Field | Value |
|---|---|
| Connector | envoy |
| First proof | Minimal Envoy ext_proc/ext_authz runtime smoke |
| Why | Repository has an Envoy bridge starter and harness entrypoint, but no runtime-verified Envoy integration yet. |
| Non-goals | No CRS support in first proof.<br>No MRTS support in first proof.<br>No full matrix.<br>No response-body support claim.<br>No production_verified claim.<br>No merge-readiness impact. |

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `connectors` | `7718dd37b45e90a90f4c57fd6a495f1c84b6d56a89a3fef9b3114c17925f0966` | `2026-07-11T05-59-47Z-e64adac0` | present |
| Declared input | `Makefile` | `ab39c7c7584d499a66cf0700273f0d51336c0a1e9e24954c3485027652a0b640` | `2026-07-11T05-59-47Z-e64adac0` | present |
| Declared input | `ci` | `6aab3274a0b20f63f0e72af48f0e92ee2281b1a4fc796692f5f580131d31d63a` | `2026-07-11T05-59-47Z-e64adac0` | present |
| Declared input | `config` | `b290b708415c6ee91cdbdf69c16f360a0a4c7311494b9ffdef8c5cafebf4cd03` | `2026-07-11T05-59-47Z-e64adac0` | present |
| Declared input | `docs` | `de53518df73f2fa90b47f5cdb2d11c0da608536389b1617ccb37dcb172b5bd7c` | `2026-07-11T05-59-47Z-e64adac0` | present |
| Declared input | `reports/testing/generated` | `93fcfe119a10479f7cec5a24cc7c08e244a432ab984d57f30347ce351dffcd34` | `2026-07-11T05-59-47Z-e64adac0` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `connectors` | present | input directory available |
| `Makefile` | present | input file available |
| `ci` | present | input directory available |
| `config` | present | input directory available |
| `docs` | present | input directory available |
| `reports/testing/generated` | present | input directory available |
