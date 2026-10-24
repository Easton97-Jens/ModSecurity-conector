# Change Record: native context accounting group

**Language:** English | [Deutsch](CR-20260922-pr382-context-accounting.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260922-pr382-context-accounting` |
| Date (UTC) | `2026-09-22` |
| Base revision | `96c41eb287778e807daeba5b28f97bd5d86fbc0a` |

## Motivation and problem statement

Sonar reported 21 top-level context fields after the request-error work. The
bounded header/body accounting fields form one coherent lifetime-owned group.

## Acceptance criteria

Retain all field names, counter order, zero initialization and independent
request-error/response-terminal state. Do not hide a Sonar finding or remove state.

## Implementation decision and rationale

Use a C17 anonymous value group for the seven contiguous accounting counters.
This follows the existing Common contract style without accessor macros or
additional allocations. Native helpers continue using the same member names.

## Changed files

- `connectors/nginx/src/ngx_http_modsecurity_common.h`
- `tests/test_nginx_context_accounting.py`
- `.github/workflows/lint.yml`
- This record and its German companion.

## Commands executed

The added required CI check is:

```sh
python -m unittest -v tests.test_nginx_context_accounting
```

It compiles the actual context declaration in C17 with warnings as errors and
pedantic checking, both with and without sanity checks. It verifies independent
counter and terminal-state writes. Execution is pending at preparation.

## Security impact

No behavior, bounds, cleanup ownership, compiler warning or scanner rule is
removed. There is no event payload or new external interface.

## Runtime evidence

The declaration test is not a running server. Existing native request and late
error suites remain required, as does fresh exact-head Sonar evidence.

## Known limitations

This targeted structural repair does not complete I09-I12 or the live-host matrix.

## Remaining risks

All native translation units must be rebuilt together after internal layout
changes. No compatibility with previously built module objects is claimed.

## Checks not run and rationale

No local project command was run because the required RTK wrapper is absent.
The independent secret-scan finding remains unresolved.

## Final diff and review status

Prepared for the existing Draft PR only; no merge, master push, force push,
scanner exclusion, issue acceptance or dependency/Framework/MRTS change.
