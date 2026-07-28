# Change Record: Parent Traefik transport-hardening diagnostic assertion order for SonarQube Cloud S3415

**Language:** English | [Deutsch](CR-20260728-sonar-traefik-transport-hardening-s3415.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260728-sonar-traefik-transport-hardening-s3415 |
| Date (UTC) | 2026-07-28 |
| Base revision | 1b0f8825f3510b99b603bb6cd6f0777e1710358e |
| Tracking | Current Parent `python:S3415` receipts AZ-KYVOWfYmbqbBXVNCg through AZ-KYVOWfYmbqbBXVNC0 at lines 73, 74, 122, 123, 165–172, 188, 189, 248–251, 256, 257, and 270 in `tests/test_traefik_transport_hardening_contract.py`. |
| Boundary | Parent test diagnostics and this English/German Change Record pair plus indexes. Traefik middleware, transport behavior, protocol controls, fixtures, Framework/MRTS source, Gitlinks, scanner configuration, Quality Gates, suppressions, and hosted SonarQube Cloud issue state remain unchanged. |
| Delivery status | At record authoring, this was a locally validated candidate for the authorized normal commit/Draft-PR cycle. This record claims no commit, push, pull request, hosted SonarQube Cloud analysis, Ready-for-review transition, or merge; later exact-head evidence is required for any delivery claim. |

## Motivation and problem statement

The 21 selected `unittest` assertions put expected values before observed
values. Reversing only the first two `assertEqual` arguments makes failure
reports identify observed values first while preserving the same equality
predicate, values, messages, test behavior, and coverage. This is a
diagnostic-only change, not a Traefik behavior change or security fix.

## Acceptance criteria

- The exact 21 tracked calls use `assertEqual(actual, expected)` with their
  original values and messages.
- All existing transport-hardening, HTTP/1.1 connection reuse, first-byte,
  end-of-stream, P1/P4 evidence, and negative controls remain unchanged.
- The complete focused Parent contract module passes after read-only
  initialization of the Parent-pinned Framework at
  `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`.
- This English/German Change Record pair is indexed and documentation checks
  record their observed result.

## Implementation decision and rationale

The source candidate changes only the first two operands of each of the 21
existing `assertEqual` calls. Actual status, runtime-rule ID, event, barrier,
and protocol-error values are now first; the same literals, lists, and other
expected values remain second. No assertion was removed or converted to a
different predicate.

The test imports existing runtime helpers but performs its covered behavior
through local loopback HTTP servers on `127.0.0.1` and ephemeral ports. No
Traefik binary, ModSecurity build, external network request, or product
subprocess was introduced. The Parent-pinned Framework was initialized
read-only only to satisfy existing test prerequisites; Framework and MRTS
source and Parent/Framework Gitlinks did not change.

## Security impact

This test module covers transport-hardening invariants, including HTTP/1.1
connection reuse, upstream end-of-stream visibility, no full response
buffering, payload-free P1 evidence, causal P4 barriers, and negative
`assertRaisesRegex` controls. The edits only change symmetric equality operand
order; all security-related predicates, values, fixtures, loopback server
behavior, and negative controls are unchanged. This is not a security fix and
does not create, close, or claim a security finding.

## Changed files

- `tests/test_traefik_transport_hardening_contract.py` — 21 S3415 diagnostic
  assertion-order updates only.
- `reports/audits/change-records/CR-20260728-sonar-traefik-transport-hardening-s3415.md`
  and `CR-20260728-sonar-traefik-transport-hardening-s3415.de.md`.
- `reports/audits/change-records/README.md` and `README.de.md`.

No generated artifacts, product source, Framework files, MRTS files, or
Gitlinks changed.

## Commands executed

- `/root/git/ModSecurity-conector/.venv/bin/python tests/test_traefik_transport_hardening_contract.py`
  with `PYTHONDONTWRITEBYTECODE=1`
- `make check-bilingual-docs check-doc-links`
- `git diff --check`

## Tests and actual results

| Command or check | Result |
| --- | --- |
| Focused Parent module `tests.test_traefik_transport_hardening_contract` | initial source validation passed: 7 tests in 1.182s; independent delivery preflight rerun passed: 7 tests in 1.164s with bytecode disabled after read-only initialization of Parent-pinned Framework `47e50e7bc43ba7a3b5bad1a9448111794f664cc0`. |
| Assertion AST review | passed: 21 `assertEqual` calls, zero constant-first calls, and all 21 expected values second. |
| `make check-bilingual-docs check-doc-links` | passed: bilingual documentation, repository path references, and documentation links passed. |
| `git diff --check` | passed with no output. |

## Runtime evidence

The passing seven-test module is focused Parent contract evidence. It does not
claim production Traefik runtime coverage, a complete connector matrix, or a
hosted SonarQube Cloud analysis.

## Checks not run and rationale

- Product builds, connector-runtime smokes, a full matrix, Framework tests,
  and MRTS tests are not run because no product, Framework, or MRTS behavior
  changed.
- Hosted SonarQube Cloud analysis, GitHub CI, commit, push, pull request, and
  merge are not run or asserted by this local Change Record. The receipt keys
  are not claimed closed without a later exact-head analysis.

## Known limitations

The focused seven-test result proves only the exercised contract scope. It does
not establish hosted SonarQube Cloud issue closure, broader connector coverage,
or delivery verification.

## Remaining risks

A future unrelated edit could accidentally change an expected value, message,
or assertion evaluation order. The narrow 21-call diff, assertion AST review,
unchanged security controls, and focused module result reduce that diagnostic
risk. No product-security remediation conclusion follows from this change.

## Final diff and review status

At record authoring, the source candidate is limited to the 21 diagnostic
operand swaps and the paired Change Record/index update. The focused module,
documentation/link validation, and whitespace check passed. No commit, push,
pull request, hosted analysis, Ready-for-review transition, or merge is
asserted.
