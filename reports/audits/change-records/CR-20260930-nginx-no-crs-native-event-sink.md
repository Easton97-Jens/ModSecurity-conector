# NGINX no-CRS native event sink

**Language:** English | [Deutsch](CR-20260930-nginx-no-crs-native-event-sink.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-nginx-no-crs-native-event-sink |
| Date (UTC) | 2026-09-30 |
| Base revision | `3de8043c2482b52debc6f6e2d9ca609adf257eab` |
| Framework | `cc36b37d0f6a0fbc3512f3878a691751e91c5fbb` |
| MRTS | `615b13bacbd008562c17408246c41ab27dca3104` |

## Motivation and problem statement

Generic NGINX no-CRS cases produced real HTTP and native-result records but
no native JSONL event: the lifecycle caller did not select a sink scope, and
the direct-harness default emitted no `modsecurity_phase4_log` directive for
those portable cases. With a null module sink, P1/P2/P3 emitters returned
before event construction. A pinned Root-master/`nobody`-worker control with
an explicit existing sink emitted the expected event. The audit-artifact path
is a separate collection defect and is not changed here.

## Acceptance criteria

For each generic no-CRS case, render exactly one case-local native location
sink at `LOG_DIR/phase4.log`; keep connector-specific fixture-owned directives
singular and preserve direct-harness and First-Byte behavior. Real P1/P2/P3
requests must yield their own rule, phase, transaction and message IDs without
body payload. Existing containment, no-follow/private-file, root/worker and
projection checks must remain active. A full canonical PASS is not inferred
from isolated cases.

## Implementation decision and rationale

Only the Parent `nginx:no_crs_baseline` caller selects
`NGINX_PHASE4_LOG_SCOPE=location_if_missing`. After Framework materialization,
the Parent harness checks the generated location include for an existing
directive and otherwise renders one directive into the existing location
placeholder. It reuses the already validated per-case `LOG_DIR/phase4.log`
path, which the collector reads. `server` alone would write to a different
file; unconditional `server_with_location_override` would duplicate the
connector-specific Phase-4 fixture directive. No native C, Common protocol,
Framework, MRTS, schema, rule or canonical expectation changes are made.

## Security impact

The sink is opened by the root NGINX master through the existing no-follow,
regular-file, ownership and mode checks, then used through the inherited
descriptor by the `nobody` worker. In the isolated controls the leaf is
`root:root` mode `0600` under the validated private per-case log root. The
worker does not gain traversal of private config, rules or harness logs.
Path-authority and docroot-projection freshness checks are unchanged; runtime
uses `PrivateNetwork=yes`, no build and no download.

## Changed files

- `ci/runtime/lifecycle/run-connector-stage.sh`
- `connectors/nginx/harness/run_nginx_smoke.sh`
- `tests/test_nginx_no_crs_event_sink.py`
- `connectors/nginx/README.md` and `connectors/nginx/README.de.md`
- This Change Record pair.

## Commands executed

The preserved external RED test reproduced default P1 HTTP `403`, a native
result and zero events; its existing-sink and matched-rule controls passed.
The new dynamic config-render regression was RED before the source fix and
GREEN afterwards. A 19-module Parent run completed 306 tests: 305 passed and
one worker-ownership test could not `chown` in the default sandbox
(`EINVAL`); the exact test passed when repeated with host rights. Shell
syntax passed. ShellCheck retained exactly the base revision's diagnostics,
with no new diagnostics. A final focused five-module run passed 81/81 tests.
Pinned bilingual, repository-path, doc-link and no-CRS consistency checks
passed. `git diff --check` passed before commit.

```sh
rtk run -c 'TMPDIR=/var/tmp/codex/ModSecurity-conector/analysis PYTHONDONTWRITEBYTECODE=1 /root/git/ModSecurity-conector/.venv/bin/python -B -m unittest tests.test_nginx_no_crs_event_sink tests.test_nginx_synchronized_phase4_policy tests.test_nginx_native_security_contract tests.test_nginx_harness_path_authority tests.test_collect_no_crs_source'
rtk run -c 'sh -n connectors/nginx/harness/run_nginx_smoke.sh && sh -n ci/runtime/lifecycle/run-connector-stage.sh'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p1'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p2'
rtk run -c 'bash /var/tmp/codex/ModSecurity-conector/analysis/run-nginx-sink-fix-isolated.sh p3'
rtk run -c 'make FRAMEWORK_ROOT=/var/tmp/codex/worktrees/pr382-nginx-source-map-phase4-header/modules/ModSecurity-test-Framework check-bilingual-docs check-doc-links check-no-crs-doc-consistency'
```

## Runtime evidence

Three fresh cache-only single-case services used separate direct projection
children and real Root-master/`nobody`-worker requests. P1 returned HTTP `403`
and emitted `engine_decision`, `MSCONN_EVENT_ENGINE_DECISION`, rule `1100001`,
`request_headers`, transaction `nginx-deny_header_marker_403-2-1`; P2 returned
HTTP `403` with the same event/message type, rule `1100101`, `request_body`,
transaction `nginx-deny_request_body_marker_403-2-1`. Both harness exits were
`0`. P3 returned HTTP `403` and emitted `phase3_intervention`,
`MSCONN_EVENT_RESPONSE_BLOCKED`, rule `1100201`, `response_headers`, transaction
`nginx-phase3_deny_before_commit-2-1`. Its native case and collector case
passed, but harness exit was `1` because cleanup reported `port=19783
result=still_bound` after the master and workers exited. Each collector saw
one event, and all three collected records passed the pinned Framework event
validator with zero errors. Each isolated collector's broader profile summary
remained `FAIL` because only one case was selected. No isolated result is a
canonical full-lifecycle PASS.

## Checks not run and rationale

The new exact-head full E2E belongs after this separate commit. No new C build,
MRTS matrix, Framework change, remote CI, push, PR or merge is part of this
source fix.

## Known limitations

The independent audit-artifact collection path, P3 cleanup-port observation,
redirect transport and unrelated canonical failures are not repaired here.
An unmatched ordinary allow case has no invented generic allow event.

## Remaining risks

The generated-include check recognizes a standalone location directive used
by the pinned connector-specific fixtures; it does not parse nested includes.
No pinned fixture uses such a nested sink. Full canonical status and any
remaining independent failure classes require the new exact-head run.

## Final diff and review status

The change is Parent-only and has no history rewrite. The pre-commit diff,
documentation checks and separate successor commit must be verified before
the new exact-head run; no overall E2E PASS is claimed in this record.
