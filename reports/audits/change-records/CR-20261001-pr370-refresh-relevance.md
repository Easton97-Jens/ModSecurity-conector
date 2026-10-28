# Change Record: CR-20261001-pr370-refresh-relevance

**Language:** English | [Deutsch](CR-20261001-pr370-refresh-relevance.de.md)

Current-master maintenance of PR #370; no readiness promotion.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261001-pr370-refresh-relevance |
| Date (UTC) | 2026-10-28 |
| Base revision | `15cea9e4d778fa1ec6e27e6fe084b347010f1367` |

## Motivation and problem statement

The user requested that existing Draft PR [#370](https://github.com/Easton97-Jens/ModSecurity-conector/pull/370) be updated to current `master`, with `master` authoritative for Phase-4 processing. The published branch was 13 commits behind and its retained qualification code referenced removed Common and connector-limit APIs. Sonar new-code duplication must be exactly zero before completion. NGINX may follow `master`, but remains excluded from readiness-B qualification and runtime credit.

## Acceptance criteria

Normally merge the observed base revision, leave no conflict, preserve current-master Phase-4 and technical-error semantics, retain only relevant additive corrections, keep the active inventory at no more than 100 cases, pass focused local validation, update this bilingual traceability, publish through the existing PR branch without force, and obtain exact-head CI and Sonar duplication density/lines/blocks of zero. No direct `master` push or merge is authorized.

## Implementation decision and rationale

The normal merge exposed 43 textual conflicts. Every conflicted product, Common, documentation, and workflow path was first restored to the exact `master` version. The remaining PR delta was then audited by connector. Obsolete qualification harnesses, removed body-limit configuration, orphaned composite APIs, stale lighttpd keepalive claims, and old technical-error oracles were removed from the net diff instead of restoring pre-master behavior.

The retained changes are narrow: fresh external APXS profile-registry staging for retries; Envoy authorization-Path authority and response-companion smoke-rule selection; a forward-declaration-safe HAProxy source checker; stricter Traefik fixture framing, bounded reads/writes, and payload-digest verification; and two small deterministic test corrections. Reviewed source hashes and the generated specialist archive were updated without changing selectors or case counts.

## Changed files

- Apache build containment and EN/DE documentation: `connectors/apache/build/apxs-wrapper.in`, `connectors/apache/README.md`, `connectors/apache/README.de.md`, and `tests/test_apache_apxs_profile_registry_staging.py`.
- Envoy protected-URI and response-companion smoke path plus EN/DE documentation and tests: `connectors/envoy/src/envoy_ext_authz_service_main.c`, `connectors/envoy/config/envoy-ext-authz-smoke.yaml.in`, `connectors/envoy/harness/run_envoy_connector_runtime.sh`, `common/rules/modsecurity_response_companion_smoke.conf`, `connectors/envoy/README.md`, `connectors/envoy/README.de.md`, and `tests/test_envoy_transport_hardening_contract.py`.
- HAProxy and Traefik verification: `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`, `connectors/traefik/scripts/runtime_native_smoke.py`, and `tests/test_traefik_transport_hardening_contract.py`.
- Deterministic test corrections: `tests/test_bounded_nginx_cases.py` and `tests/test_logical_connector_example_matrix.py`.
- Inventory and generated companion: `config/testing/active-cases.json` and `reports/testing/test-selection-archive.generated.json`.
- This EN/DE record pair and the EN/DE archive indexes.

## Commands executed

All project shell commands were RTK-wrapped. Heavy output and Go caches used private paths below `/var/tmp/codex/ModSecurity-conector`.

| Check | Observed local result |
| --- | --- |
| APXS focused module | 7/7 passed. |
| Envoy focused transport module | 3/3 passed. |
| Traefik focused transport module | 6/6 passed. |
| NGINX umask plus logical-example regressions | 3/3 passed; no NGINX runtime or B qualification was run. |
| `make check-haproxy-htx-overlay` | Passed. |
| `python3 ci/tools/update-test-archive.py --check` | Passed. |
| `make check-active-inventory` | Passed: 100 core cases, hard limit 100, 1,893 on-demand cases. |
| Six-group active selection check | Passed: 22 executions and 26 expanded cases. |
| Six-group active execution with `--strict-skips` | Final run passed all 26 cases with no skip. The first attempt lacked explicit libmodsecurity paths; the second exposed a read-only default Go cache. The successful rerun used existing system libmodsecurity and private external Go caches. |
| Independent narrowed-diff security review | No validated new security vulnerability; `git diff --check origin/master` passed. |
| Common/adapter static contract targets | All six selected targets passed. |
| EN/DE, link, variable and generated connector-reference checks | Passed after read-only materialization of the exact Framework Gitlink. |
| Direct repository Envoy connector build script | Passed against the existing system libmodsecurity and produced both service binaries. The Root lifecycle wrapper was separately interrupted after making no observable progress during preparation; no wrapper-build pass is claimed. |
| `sh -n` for both changed shell paths | Passed. Direct ShellCheck also ran, but reported existing template shebang, `CDPATH`, dynamic-source, and intentional splitting findings outside the changed lines; no suppression was added. |
| Change-Record structure and final whitespace checks | Passed locally. |

## Security impact

Envoy no longer treats downstream original-URI hint headers as policy-selection authority; the authorization request Path is authoritative. Traefik evidence readers reject ambiguous Content-Length/Transfer-Encoding framing, noncanonical or oversized fixture lengths, truncated input, short output, and same-length payload substitution. APXS rebuilds avoid trusting or overwriting an earlier staged child. The HAProxy checker no longer mistakes a forward declaration for a function body. No suppression, Quality-Gate relaxation, dependency change, permission expansion, or compiler-warning reduction is introduced.

## Runtime evidence

The selected active run exercised 26 reviewed cases across Common, Apache, HAProxy, Envoy, Traefik, and lighttpd, including the real Stock-lighttpd loopback allow case. These are bounded contract and component/runtime checks for the selected inventory only. They do not establish three fresh starts, every G1–G9 gate, production readiness, or readiness B for every non-NGINX profile. NGINX was updated only through incoming `master` and received no readiness credit.

## Known limitations

The APXS wrapper continues to assume a trusted external build-root ancestry; the patch narrows reuse below that boundary but does not claim protection from a hostile same-host writer controlling an ancestor. The retained Traefik changes harden the local evidence harness and do not expand connector capability claims. The selected active inventory is not the historical full I12 or all-profile qualification matrix.

## Remaining risks

Hosted checks and Sonar must bind to the final delivered SHA. Local success does not prove hosted workflow permissions, external service availability, or zero new-code duplication. The Root Envoy lifecycle wrapper did not complete locally, although the underlying repository build script passed. The larger readiness-B objective remains unproven until its required host/profile/run evidence exists.

## Checks not run and rationale

No historical full-matrix/I12 restart, all-profile G1–G9 campaign, Framework/MRTS source write, dependency installation, direct `master` push, force push, or merge was performed. Exact-head CI and Sonar are available only after publishing the successor commit and remain pending at this stage.

## Final diff and review status

Master-first relevance and Phase-4 audits are complete. The narrowed diff received independent security, test-selection, and documentation review, and the selected local static, documentation, build, focused, and 26-case active checks passed as qualified above. Delivery SHA reconciliation and hosted CI/Sonar results are recorded only after they are actually observed.
