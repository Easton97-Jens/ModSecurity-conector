# HAProxy Validation

Status: partial; historical SPOA runtime material is evidence-scoped and does
not promote canonical Phase-4 facets.

`make smoke-haproxy` verifies framework YAML cases by materializing each case,
starting HAProxy, starting `haproxy-modsecurity-spoa`, starting a backend,
sending the case request through HAProxy, and asserting the observed status.

`make runtime-matrix-haproxy` records rows from live summary evidence. PASS and
FAIL are used only for live HAProxy execution. Generated artifacts may differ by
environment and case inventory, but no HAProxy PASS/FAIL may be fabricated from
synthetic matrix rows.

## Commands

```bash
git submodule update --init --recursive
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
HAPROXY_HTX_SOURCE_DIR=/absolute/path/to/haproxy-3.2.21 \
  MODSECURITY_INCLUDE_DIR=/absolute/path/to/include \
  MODSECURITY_LIB_DIR=/absolute/path/to/lib \
  BUILD_ROOT=/var/tmp/haproxy-htx-smoke \
  make -C connectors/haproxy runtime-smoke-haproxy-htx
make smoke-haproxy
make runtime-matrix-haproxy
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

## Historical Evidence

These snapshots are not current canonical Phase-4 facet evidence.

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke (historical) | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all (historical) | 133 | 104 | 23 | 0 | 6 |

Evidence is recorded in:

- `/src/ModSecurity-conector-build/results/with-crs/haproxy-summary.json`
- `/src/ModSecurity-conector-build/results/force-all/haproxy-summary.json`
- `reports/testing/generated/haproxy-runtime-results.generated.md`
- `reports/testing/haproxy-poc.md`
- `reports/testing/runtime-validation-snapshot.json`

## Not Claimed

- Force-all FAIL rows are not hidden by default smoke.
- Full-body RESPONSE_BODY support is not promoted.
- A build self-test alone is not runtime verification.
- There is no synthetic matrix writer.

Phase 4 / RESPONSE_BODY remains non-promoted. The old bounded sample branch
is disabled because it required `http-response wait-for-body`; it is not a
real host-side response stream or strict-abort proof.

## Canonical Phase-4 validation

The selected SPOA/SPOP configuration has no response-body path: the former
bounded branch is disabled. The separate `full-lifecycle-haproxy-htx` profile
selects a HAProxy 3.2.21 HTX observer with a real-host P1–P4 transport smoke.
It is observer-only after forwarding and is not an SPOP response path. Its
observer evidence explicitly records upstream 200 for
precommit decisions and `host_action=not_attempted` for the P4 safe policy.
`response_body_buffered`, `phase4`, and `phase4_rule_evaluation` are
`not_implemented`. The current runner has no host-observed client status or
commitment timing and no post-commit response point. Therefore pre-commit
deny, all late-intervention actions, and semantic status metadata are
`not_implemented`, not pending PASS assertions.

| Case | Required evidence | Excluded substitute |
| --- | --- | --- |
| `phase4_rule_observed` | Rule `1100301` observed through the real response path | a self-test or agent-only log |
| `phase4_deny_before_commit` | `NOT_EXECUTED`: implement host-observed client status and commitment timing first | policy-derived agent fields |
| `phase4_deny_after_commit_log_only` | `NOT_EXECUTED`: implement a post-commit host point and safe action first | a bare response status or response-preserving policy value |
| `phase4_deny_after_commit_abort` | `NOT_EXECUTED`: implement controlled post-commit `abort_connection` first | timeout, agent failure, or generic disconnect |
| status/action metadata | `NOT_EXECUTED`: implement host-observed original/visible status and timing first | one status field, a rule ID, or policy-derived values |

No canonical run means `NOT_EXECUTED`, not a synthetic 403 `PASS`.  Event and
report artifacts are metadata-only and must never include response-body data.
