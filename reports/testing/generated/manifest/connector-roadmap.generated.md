> Generated file - do not edit manually.
>
> Generated at: `2026-06-19T17:36:41Z`
> Verified run id: `2026-06-19T17-36-41Z-983ce2a2`
> Data source policy: `verified-inputs-only`
> Generator: `ci/generate-connector-roadmap.py`
> Make target: `refresh-connector-reports`
> Owner: `manifest`
> Severity: `informational`
> Connector SHA: `983ce2a2918c3a3c649cd84364b6dcfdc9e53506`
> Framework SHA: `dc19582d89bd8ef50463c5a9c5a0271cc37bb958`
> Input status: `complete`

# Connector Roadmap

Roadmap-only generated report. It does not create runtime PASS/FAIL values and does not add full-matrix rows for unimplemented connectors.

## Connector Status Matrix

| Connector | Directory | Status | Build Target | Verified Case | Full Matrix | Notes |
|---|---|---|---|---|---|---|
| apache | yes | production_verified | yes | yes | yes | production verified runtime connector; framework runtime and full-matrix evidence present |
| nginx | yes | production_verified | yes | yes | yes | production verified runtime connector; OpenResty is initially covered as an nginx runtime variant |
| haproxy | yes | production_verified | yes | yes | yes | production verified runtime connector; SPOE-sidecar integration path is documented |
| envoy | yes | partial_skeleton | yes | no | no | partial bridge starter only; no runtime-verified Envoy adapter; most realistic proof path is ext_proc or ext_authz sidecar before considering native/WASM work; request/response body coverage depends on Envoy buffering/streaming mode limits |
| lighttpd | yes | partial_skeleton | yes | no | no | partial bridge starter only; no native lighttpd module, FastCGI, or SCGI bridge; blocking is plausible only after a selected hook/proxy architecture is proven |
| traefik | yes | partial_skeleton | yes | no | no | partial decision-service starter only; no Go plugin/middleware or runtime harness; direct libmodsecurity embedding is not proven; reverse-proxy/decision-service harness is lower-risk |
| litespeed | no | planned | no | no | no | planned candidate; no repository directory yet; OpenLiteSpeed/LiteSpeed ModSecurity compatibility needs license/download/automation proof before implementation |
| openresty | no | covered_by_existing_connector | no | no | no | covered_by_nginx; do not create a separate connector at this stage |

## Connector Candidate Ranking

| Rank | Connector | Difficulty | Risk | Expected Value | Recommendation |
|---:|---|---|---|---|---|
| 1 | envoy | high | medium-high | high | Next proof: ext_proc/ext_authz sidecar runtime smoke with request blocking and explicit body-mode evidence. |
| 2 | litespeed | medium | high | medium-high | Run installation/licensing proof for OpenLiteSpeed first; do not implement until automation is proven. |
| 3 | traefik | medium-high | high | medium | Prototype a decision-service/forwardAuth harness before any Go plugin work. |
| 4 | lighttpd | high | high | medium | Perform hook/proxy architecture spike before implementation. |

## OpenResty Decision

| Field | Value |
|---|---|
| Decision | covered_by_nginx |
| Separate connector | no |
| Reason | NGINX-based runtime |

## LiteSpeed Candidate

| Field | Value |
|---|---|
| Candidate | LiteSpeed / OpenLiteSpeed |
| Status | planned |
| Key risks | license/download automation, edition differences, ModSecurity-engine compatibility, CI installability |
| Next proof step | OpenLiteSpeed package/container install proof with one CRS blocking fixture and captured evidence |

## Technical Feasibility

### envoy

| Field | Assessment |
|---|---|
| integration | realistic via ext_proc gRPC sidecar or ext_authz decision service; WASM/Lua are possible but not currently represented in the repo |
| blocking | realistic for request blocking with ext_authz/ext_proc; response-body disruptive semantics require explicit filter-mode proof |
| phases | request headers/body and response headers/body are conceptually mappable through Envoy HTTP filters, subject to configured processing modes |
| limits | body coverage is governed by Envoy buffering/streaming settings and partial-body behavior; must be evidenced per case |

### lighttpd

| Field | Assessment |
|---|---|
| integration | no native ModSecurity adapter is present; needs either a native module study or proxy/sidecar bridge |
| blocking | realistic only after the chosen hook can stop forwarding before upstream commit |
| phases | request headers/body are more likely first; response phases need separate hook proof |
| limits | unknown until module/proxy architecture and buffering behavior are selected |

### traefik

| Field | Assessment |
|---|---|
| integration | plugin/middleware or forwardAuth-style decision service are the likely paths; direct libmodsecurity integration is not proven |
| blocking | request blocking is realistic through middleware/decision service; response-body blocking is higher risk |
| phases | request header/body first; response phases require Go middleware/harness evidence |
| limits | depends on plugin/middleware body buffering and Yaegi/Go runtime constraints |

### litespeed

| Field | Assessment |
|---|---|
| integration | OpenLiteSpeed and LiteSpeed Enterprise advertise ModSecurity-compatible rule support, but this repo has no connector or harness |
| blocking | plausible if the server's own ModSecurity engine can be driven in CI with CRS fixtures |
| phases | must be mapped empirically from server logs/results rather than assumed equivalent to libmodsecurity v3 connectors |
| limits | license, package availability, edition differences, and non-libmodsecurity engine compatibility are the main risks |

## Recommended Next Connector

envoy

## Data Sources

| Value | Source | Source Hash | Verified Run ID | Status |
|---|---|---|---|---|
| Declared input | `connectors` | `1627bb92c5756d6f37fe7f678a30211b2ad2a694b3bf2c269f32f6d7523a44cd` | `2026-06-19T17-36-41Z-983ce2a2` | present |
| Declared input | `Makefile` | `22368c84b5502b69ed3ea9c6ecaac7e3f82bb6a3ea661a78c0f8bee7f6015d20` | `2026-06-19T17-36-41Z-983ce2a2` | present |
| Declared input | `ci` | `f1e134e757036b53da0197a46cdc0db2298a63bb23af16cc1e6ea24561dcf085` | `2026-06-19T17-36-41Z-983ce2a2` | present |
| Declared input | `config` | `ae2f671756d889c00872b67962e0112910de7a0a00bb8cf6ebe9d490723cccbb` | `2026-06-19T17-36-41Z-983ce2a2` | present |
| Declared input | `docs` | `7c0eab4174dcf7c2a752a9a8481ad3bc69a6757917ff9a52b0375acff7b892ee` | `2026-06-19T17-36-41Z-983ce2a2` | present |
| Declared input | `reports/testing/generated` | `890788099601d1d6f311a8ae95e0f3f8d55ccfa4732eaffbb53ddd1213786a04` | `2026-06-19T17-36-41Z-983ce2a2` | present |

## Data Availability / Missing Information

| Input | Status | Notes |
|---|---|---|
| `connectors` | present | input directory available |
| `Makefile` | present | input file available |
| `ci` | present | input directory available |
| `config` | present | input directory available |
| `docs` | present | input directory available |
| `reports/testing/generated` | present | input directory available |
