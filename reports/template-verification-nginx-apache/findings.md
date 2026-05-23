# Findings

All findings below are based on files, paths, or commands reviewed in this
repository and the local `/src/ModSecurity-conector-build` result tree.

## Template

- `connectors/_template/README.md` defines a generic connector template and is
  not a productive connector implementation.
- `connectors/_template/TODO.md` uses checkbox-style status labels.
- `connectors/_template/docs/coverage-decision-matrix.md` documents the
  generic matrix and runtime-promotion rules.
- `connectors/_template/tests` is absent. Executable Template tests are not
  maintained connector-locally.

## External Tests

- Framework testcases are under `modules/ModSecurity-test-Framework/tests/cases/`.
- Connector-specific framework paths are under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/<connector>/`.
- NGINX-specific YAML files exist under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/nginx/`.
- Apache-specific YAML files were not found under
  `modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache/`;
  only `README.md` was found there.
- New connector scaffolds must not create local `connectors/<name>/tests`
  directories.

## NGINX

- `connectors/nginx/` is present and adapter-owned.
- `connectors/nginx/src/`, `connectors/nginx/config`,
  `connectors/nginx/metadata.c`, and `connectors/nginx/ORIGIN.md` are present.
- `connectors/nginx/tests` is absent.
- `common/include/msconnector/rule_load_stats.h` exists.
- The NGINX build contract uses
  `MSCONNECTOR_COMMON_INC=$CONNECTOR_ROOT/common/include`.
- The current parent runtime contract uses
  `NGINX_HARNESS_PARENT=$(BUILD_ROOT)`.
- `connectors/nginx/harness/nginx_smoke.conf` uses the generated `DOCROOT` as
  the NGINX `root`.
- `modules/ModSecurity-test-Framework/tests/runners/runner_core.py` writes
  `index.html` into the generated docroot during materialization.
- `/tmp` is `drwx------ root root` in this workspace, so a root-owned NGINX
  runtime work root below `/tmp` is not traversable by the `nobody` worker.
- Current `/src` NGINX all-scope smoke passed: 60 PASS, 0 FAIL, 0 BLOCKED.
- Current `/src` NGINX common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- The historical 11 NGINX BLOCKED rows are documented in
  `nginx-blocked-runtime-cases.md` and classified as an environment/docroot
  permission blocker.
- RESPONSE_BODY blocking remains not verified for NGINX. `response_body_pass`
  is pass-through evidence only.

## Apache

- `connectors/apache/` is present and adapter-owned.
- `connectors/apache/src/`, `connectors/apache/Makefile.am`,
  `connectors/apache/configure.ac`, `connectors/apache/metadata.c`, and
  `connectors/apache/ORIGIN.md` are present.
- `connectors/apache/tests` is absent.
- `connectors/apache/build/apxs-wrapper.in` contains a common include fallback
  based on `CONNECTOR_ROOT`.
- Current `/src` Apache common smoke passed: 54 PASS, 0 FAIL, 0 BLOCKED.
- RESPONSE_BODY blocking remains not verified for Apache. `response_body_pass`
  is pass-through evidence only.

## Similar Connectors

- `connectors/haproxy/README.md` identifies HAProxy as scaffolded and not
  implemented.
- `connectors/envoy/README.md` identifies Envoy as scaffolded and not
  implemented.
- `connectors/traefik/README.md` identifies Traefik as scaffolded and not
  implemented.
- `connectors/lighttpd/README.md` identifies Lighttpd as scaffolded and not
  implemented.

## Current Commands And Results

| Command | Result | Evidence |
| --- | --- | --- |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-nginx` | PASS | NGINX 60 PASS, 0 FAIL, 0 BLOCKED. |
| `SOURCE_ROOT=/src BUILD_ROOT=/src/ModSecurity-conector-build REFRESH=1 make smoke-common` | PASS | Apache 54 PASS; NGINX 54 PASS; both 0 FAIL and 0 BLOCKED. |
| `test ! -d connectors/_template/tests` | PASS | Local Template test folder absent. |
| `test ! -d connectors/apache/tests` | PASS | Local Apache test folder absent. |
| `test ! -d connectors/nginx/tests` | PASS | Local NGINX test folder absent. |

Final static checks are recorded in `summary.md` after rerun.

## Decisions

- `connectors/_template`: partially suitable.
- `connectors/apache`: partial.
- `connectors/nginx`: partial.
- RESPONSE_BODY blocking: not verified.
- Full runtime verification: no.
