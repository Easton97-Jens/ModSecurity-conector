# Change Record: native intervention test linkage

**Language:** English | [Deutsch](CR-20260922-pr382-chain-link.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-chain-link` |
| Date (UTC) | `2026-09-22` |
| Base revision | `3730eaa03b2f76ccac3baebfc862d8a8417c99ef` |

## Motivation and problem statement

The native intervention-chain suite failed during linking before any of its ten
behavior tests could run. The fixture linked `block_statuses.c` but omitted its
real `http_status.c` dependency. This failure already exists at `7fe606c5` in
[CI job 106698812691](https://github.com/Easton97-Jens/ModSecurity-conector/actions/runs/35713306728/job/106698812691).

## Acceptance criteria

Link the actual missing dependency and execute the existing ten tests without
stubs, removed assertions or relaxed compiler flags. Preserve all native/host
failure, legitimate rule, cleanup and Safe/Strict/Off controls.

## Implementation decision and rationale

Add only `http_status.c` to the existing fixture source list. Production source
is unchanged. The linker diagnostics explicitly identify that dependency.

## Changed files

- `tests/test_nginx_native_intervention_chain.py`
- This record and its German companion.

## Commands executed

The existing CI entry point is:

```sh
python -m unittest -v tests.test_nginx_native_intervention_chain
```

Execution after this correction is pending at preparation. The preceding CI
failure was an unresolved-symbol error, not a failed behavioral assertion.

## Security impact

Restore execution of the original security regressions rather than bypassing
their failing setup. No production logic, flags, scanner rules or permissions
change.

## Runtime evidence

The fixture compiles the real collector, dispatcher, P4 caller and Common
lifecycle with controlled native and final host I/O seams. It is not a live host.

## Known limitations

This does not complete all I09-I12 criteria. Any behavioral failure revealed
once the fixture links must be investigated independently.

## Remaining risks

Passing controlled call-chain tests cannot establish client transport outcomes.

## Checks not run and rationale

Local commands were not run because the required RTK wrapper is absent.
Fresh CI and exact-head Sonar evidence remain required.

## Final diff and review status

Single-line test-build repair plus bilingual traceability, on the existing Draft
PR only. No merge, master push, force push or dependency version change.
