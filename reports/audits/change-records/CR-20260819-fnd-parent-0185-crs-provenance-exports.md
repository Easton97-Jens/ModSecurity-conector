# CR-20260819 — Preserve optional CRS provenance export presence

**Language:** English | [Deutsch](CR-20260819-fnd-parent-0185-crs-provenance-exports.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260819-fnd-parent-0185-crs-provenance-exports |
| Date (UTC) | 2026-08-19 |
| Base revision | `0edc0dd24fcd16b5fec72c85a7a86e456babfd8b` |
| Finding | `FND-PARENT-0185` |
| Delivery branch | `agent/fix-fnd-parent-0185-crs-export` |
| Framework boundary | Gitlink `bd69ee96e0e7082317d4afe1232bee625665eb9a`; no source or Gitlink change |
| Delivery disposition | Parent Draft PR authorized; no merge authorized |

## Motivation and problem statement

When a caller left an active provenance variable undefined, Parent `make`
exported it as an explicit empty environment value. The Framework correctly
interprets that as an attempted non-canonical override and blocks before the
five HAProxy fixture assertions run. The same presence bug covered the active
CRS, NGINX, HAProxy, HTTPD, APR, APR-util, and PCRE2 pin sets.

## Acceptance criteria

- Undefined optional inputs remain absent at the Framework boundary.
- Explicit empty and altered CRS inputs still fail closed before side effects.
- The five HAProxy tests reach their intended assertions without a Framework,
  Gitlink, or MRTS change.
- Exact-head hosted Actions and the unchanged SonarQube Cloud gate must pass
  before this finding may become verified.

## Implementation decision and rationale

`Makefile` now has a single guarded export list. It forwards an optional pin
only when Make received it, while retaining an explicitly empty or altered
value unchanged. Thus reviewed Framework defaults apply only to genuinely
absent inputs; the existing Framework validation still rejects explicit bad
inputs.

The Parent tests cover that contract for every list member. HAProxy fixtures
now include the binary digest demanded by the current Framework contract, and
the future-pin test asserts the earlier inherited-pin guard rather than a later
runtime-lock failure.

## Security impact

The repair removes accidental empty-value injection only. The Framework guard,
origin validation, CI controls, scanners, and Quality Gate are unchanged.

## Changed files

- `Makefile` and the four focused Parent test modules
- this paired Change Record and its bilingual archive index

## Commands executed

- Five affected HAProxy tests passed directly and through the Parent Make
  boundary.
- `test_prepare_runtime_components` (41), `test_ci_security_workflows` (28),
  `test_all_connectors_no_crs_workflow_contract` (9), and
  `make check-ci-security-contract` (122; 5 expected capability skips) passed.
- Explicit altered and empty `CRS_REPO_URL` controls were rejected before a
  build or download.
- Final independent security review found no bypass or reportable issue.

## Runtime evidence

The retained receipt is
`.codex/runs/20260819T230619Z-fix-fnd-parent-0185-crs-export/evidence/post-remediation-local-validation.md`
with SHA-256 `bf6b0ba026a3135ea7ea4ee10cc977c46f1b63c1252997d694db3a25b6e74235`.

## Checks not run and rationale

`make check-no-crs-source-normalization` reached the repaired tests but has two
unrelated hard-coded catalog-path errors in this deliberately uninitialized
task worktree. Initializing or editing the Framework module would violate the
user-selected boundary, so hosted exact-head checks remain the required broad
evidence.

## Known limitations

The isolated worktree intentionally has no initialized Framework checkout, so
its two static catalog-path cases cannot finish locally.

## Remaining risks

Exact-head hosted CI and SonarQube Cloud evidence are still required; no merge
is authorized.

## Final diff and review status

Only Parent `Makefile`, Parent tests, and this paired traceability material are
changed. The Framework source, its Gitlink, and nested MRTS are unchanged.
`FND-PARENT-0185` is `fixed` locally, not verified or closed. The pending
Draft-PR head must pass the unchanged GitHub Actions and SonarQube Cloud gates;
this record neither requests nor authorizes a merge.
