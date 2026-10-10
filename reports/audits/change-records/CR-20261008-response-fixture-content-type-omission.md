# Change Record: CR-20261008-response-fixture-content-type-omission

**Language:** English | [Deutsch](CR-20261008-response-fixture-content-type-omission.de.md)


## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-response-fixture-content-type-omission |
| Date (UTC) | 2026-10-08 |
| Base revision | `b7403e30111688da00d8e7ce376ea91ced1c6145` |

## Motivation and problem statement

Explicit missing Content-Type was converted into an empty header or a backend default.

## Acceptance criteria

Real HTTP must omit Content-Type entirely; default responses remain unchanged; framing/unknown/conflicting omissions fail closed.

## Implementation decision and rationale

Validate optional omit_headers=['Content-Type'] through a closed helper and apply only that explicit omission in the existing backend.

## Changed files

ci/runtime/common/response_fixture_omission.py; ci/runtime/common/response-header-test-backend.py; tests/test_response_fixture_omission.py; EN/DE record pair.

## Commands executed

RTK-wrapped Parent Python: missing-helper RED1; real-wire RED1/default header; GREEN6 tests0; existing backend10 tests0/no SKIPs with trusted Framework and external TMPDIR. Native record archive check0. Bilingual/doc-link target2: uninitialized nested Framework links in this isolated worktree; no check weakened.

## Security impact

No framing/security header suppression or product semantics changes; omission/configured-header conflicts rejected, including empty values.

## Runtime evidence

Real bounded loopback HTTP unit operation received200/body with Content-Length15 and no Content-Type field. Not Root/nobody connector or Canonical evidence.

## Known limitations

Coordinator must propagate explicit omit_headers in shared metadata; native NGINX missing-header focus remains pending.

## Remaining risks

Integrated wire/NATIVE evidence must match the contract; no PASS from fixtures or absence alone.

## Checks not run and rationale

Full Parent lint, integrated native requests and remote checks pending coordinator integration. Full bilingual/doc-link checks require the actual nested Framework checkout; current isolated worktree leaves it uninitialized.

## Final diff and review status

Task-owned explicit files only; no push/merge/gitlink update. Unit and existing backend checks pass; final integration remains open.
