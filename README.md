# ModSecurity Connector Monorepo

Status: scaffolded

This repository is a monorepo scaffold for future libmodsecurity v3 based
connectors.

Implemented now:

- Connector-neutral headers under `common/include/msconnector/`.
- Documentation that separates local v3/libmodsecurity facts from v2 historical
  and regression-test material.
- Connector directories for Apache, NGINX, HAProxy, Envoy, Lighttpd, and
  Traefik.
- Test layout, normalizer skeletons, runner skeletons, and CI structure checks.

Not implemented:

- No complete connector runtime.
- No server/proxy module build.
- No claim that any connector can load, run, block, log, or reload rules.

Primary local references:

- `/root/conecter/ModSecurity_V3`: `v3/master`, observed `v3.0.15`
- `/root/conecter/ModSecurity_V2`: `v2/master`, observed `v2.9.13`
- `/root/conecter/ModSecurity-apache`: observed `v0.0.9-beta1-26-g0488c77`
- `/root/conecter/ModSecurity-nginx`: observed `v1.0.4-14-g9eb44fd`

Boundary rule:

- `common/` contains connector-neutral code only.
- `connectors/<name>/` contains server/proxy-specific integration only.
- `tests/common/` contains only portable engine/rule/behavior tests.
- `tests/<connector>/` contains connector-specific behavior tests.

See `docs/architecture.md`, `docs/compatibility.md`, and `docs/roadmap.md`.
