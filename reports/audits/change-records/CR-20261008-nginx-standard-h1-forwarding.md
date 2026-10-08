# Change Record: CR-20261008-nginx-standard-h1-forwarding

**Language:** English | [Deutsch](CR-20261008-nginx-standard-h1-forwarding.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-standard-h1-forwarding |
| Date (UTC) | 2026-10-08 |
| Base revision | `e3fcd1c7d5a9ce09abde7c9593a15690d7ed08f0` |

## Motivation and problem statement

The documented harness defaults to HTTP/1, but the Parent native full-lifecycle caller omitted downstream protocol in both Framework selection and initialization. The Framework correctly rejected its default `any` for a NGINX full-lifecycle plan before requests.

## Acceptance criteria

The standard `make full-lifecycle-nginx` caller forwards the existing HTTP/1 default without external injection; explicit compatible H2/H3 selections remain selected in plan-only tests. Invalid/conflicting values fail before selection; generic and other-connector plans remain unchanged.

## Implementation decision and rationale

Resolve the existing NGINX downstream default once, only for the NGINX full-lifecycle profile; validate its compatibility with the existing build profile, export it to the harness and pass it identically to selection and initialization. An enhanced build does not imply a different transport.

## Changed files

`ci/runtime/lifecycle/run-no-crs-baseline.sh`, `tests/test_nginx_full_lifecycle_protocol_wiring.py` and this EN/DE record pair. Framework, MRTS, Gitlinks, dependencies, Required definitions and harness guards are unchanged.

## Commands executed

Dynamic old-code standard-caller regression fails at real Framework selection (exit 1). Focused tests exercise real Make/Framework select/init, stopping before host execution. Existing selection/profile/H1 request tests: 20 PASS, 0 SKIP. Shell syntax and `git diff --check` pass. ShellCheck retains eight existing diagnostics with no new code/severity/message. Dynamic standard/profile matrix: `rtk proxy /root/git/ModSecurity-conector/.venv/bin/python -m unittest -v tests.test_nginx_full_lifecycle_protocol_wiring` with `FRAMEWORK_TEST_PYTHON` pointing to the pinned Framework environment: 9 tests PASS, 0 SKIP, exit 0; initializer sentinel 79 intentionally stops before runtime. Coordinator independently reran the same nine tests (exit 0).

## Security impact

Unsupported downstream/build-profile combinations remain rejected. The plan cannot claim H2/H3 from H1 evidence. No containment, projection freshness, validator or trust boundary is relaxed.

## Runtime evidence

This commit's regression evidence is plan-only, not host runtime. A fresh real standard-caller focus and full lifecycle against the final committed A/B/C head will follow; no external H1 injector will be used.

## Known limitations

Compatible explicit H2/H3 plans are covered, not H2/H3 runtime. This change does not schedule missing Required host/fault/common scenarios or invent events.

## Remaining risks

Independent canonical coverage and Protected prerequisites remain separate obligations; a successful selection does not prove requests or evidence.

## Checks not run and rationale

Fresh standard host focus/full E2E, full lint and published-head CI/Sonar follow the atomic fixes. Ruff is absent; no package installation attempted.

## Final diff and review status

The complete scoped diff and default contract were reviewed. Atomic B commit is separate from binary hashing and S5778; no unrelated protocol work or evidence is included.
