# Validation - Connector Template

**Language:** English | [Deutsch](validation.de.md)

## Principle

File structure, generated coverage, or a successful build is not runtime
verification. A connector is runtime-verified only for the exact command,
scope, cases, and result files that were executed and recorded.

## Required runtime evidence

- [ ] command
- [ ] environment
- [ ] exit code
- [ ] connector scope
- [ ] PASS/FAIL/BLOCKED counts
- [ ] summary JSON paths
- [ ] per-case expected and actual statuses for claimed cases
- [ ] relevant logs or audit evidence
- [ ] unresolved FAIL/BLOCKED rows documented

## No-CRS validation

Record the concrete command, for example:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-no-crs
```

No-CRS claims must include counts and summary paths for the claimed connector.

## With-CRS validation

Record the concrete command, for example:

```sh
SOURCE_ROOT=<path> BUILD_ROOT=<path> REFRESH=1 make test-with-crs
```

With-CRS claims must include CRS source path, CRS preamble path, counts, summary
paths, and CRS-specific case evidence. A With-CRS case may need a
variant-specific expectation; do not change a base No-CRS expectation to make a
With-CRS run pass.

## RESPONSE_BODY blocking minimum evidence

RESPONSE_BODY blocking remains `not-verified` until all of the following are
present:

- [ ] repository-backed runtime testcase in the framework
- [ ] expected blocking response-body trigger
- [ ] actual blocking result, such as HTTP 403
- [ ] log/report evidence
- [ ] executed command
- [ ] affected connector
- [ ] Apache and NGINX separately documented if a shared claim is made

Pass-through or log-only response-body evidence does not prove blocking.

## Minimum matrix for more than `partial`

- [ ] `phase1_header_block`
- [ ] request-body blocking
- [ ] response-header blocking, when framework-supported
- [ ] response-body blocking
- [ ] audit/log evidence
- [ ] startup/reload validation
- [ ] negative/pass-through case
- [ ] No-CRS and With-CRS results documented separately
- [ ] no unresolved FAIL/BLOCKED row in the claimed minimum matrix

## Not sufficient

- only file or folder existence
- only static lint
- only generated coverage
- only build success
- No-CRS evidence used as With-CRS evidence
- PASS for one case used as PASS for a whole target
