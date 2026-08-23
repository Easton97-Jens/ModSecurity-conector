# Change Record CR-20260823: PR #309 Lighttpd configuration-reference repair

**Language:** English | [Deutsch](CR-20260823-pr309-lighttpd-config-reference-repair.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260823-pr309-lighttpd-config-reference-repair` |
| Date (UTC) | `2026-08-23` |
| Base revision | `7c403fada21de4547259fef1dc4a1b079cb0cb25` |
| Scope | Parent repository only: closed Lighttpd configuration-reference extraction, one focused regression test, generated English/German reference material and inventory, and paired traceability. No Framework, MRTS, Gitlink, connector-runtime source, workflow, dependency, toolchain, NGINX, or quality-gate configuration change. |

## Motivation and problem statement

After Parent PR [#309](https://github.com/Easton97-Jens/ModSecurity-conector/pull/309)
was squash-merged at the base revision, its shared `test-common` and
`test-apache` paths stopped before a host could start. The first failure came
from `extract_lighttpd()`: its closed expected inventory still listed only two
native plugin directives, while
`connectors/lighttpd/module/mod_msconnector.c` now declares exactly three.

The missing directive is `msconnector.expose-host-transaction-id`. It is an
existing, default-off, server-scoped evidence option. This repair restores the
source-backed documentation contract without broadening the extractor or
changing the native Lighttpd runtime.

## Acceptance criteria

- Require the exact three native Lighttpd directives with their source types
  and server scopes; reject an unexpected key, type, or scope.
- Document the existing transaction-ID evidence option in generated English and
  German configuration references and the machine-readable inventory.
- Preserve its default-off, server-generated, non-request-reflecting semantics.
- Add a focused regression test for the closed inventory and option semantics.
- Preserve Framework/MRTS/Gitlinks, workflows, dependencies, toolchains, and
  quality controls.
- Obtain fresh exact-head hosted validation after this traceability record is
  committed and pushed; no historical check result is treated as evidence for a
  new head.

## Implementation decision and rationale

- `extract_lighttpd()` keeps a closed ordered tuple comparison for
  `msconnector.enabled`, `msconnector.config-file`, and
  `msconnector.expose-host-transaction-id`; it does not use a wildcard or
  permissive parser.
- The new documentation row is generated from the existing native source. Its
  P3 response header carries a server-generated host transaction ID after
  response-header processing and does not alter Common Runtime transaction-ID
  input.
- Repeated Lighttpd metadata literals are named constants only; their values
  and generated output semantics are unchanged.
- The generator, not generated files alone, is the source of the documentation
  update.

## Alternatives

- A permissive extractor or a wildcard inventory was rejected because it would
  hide future native directive drift instead of failing closed.
- Editing generated Markdown and JSON without changing the generator was
  rejected because generation checks would immediately overwrite or reject it.
- Changing native Lighttpd runtime source was unnecessary: the option already
  exists and the defect was solely the stale documentation contract.

## Compatibility impact

The generated reference and inventory now expose an existing default-off
directive. No runtime configuration syntax, default, request behavior,
response behavior, connector ABI, dependency, toolchain, or repository
boundary changes.

## Security impact

The corrected contract is security-relevant because it describes an opt-in
response header. The repair preserves the closed source inventory and documents
that the value is server-generated, default-off, and never reflects a request
header. It changes no request parsing, header emission, privilege, file,
namespace, or runtime decision path. A focused security review found no
reportable regression.

## Changed files

- `ci/checks/documentation/connector_config_reference.py`
- `tests/test_connector_config_reference.py`
- `examples/lighttpd/configuration-reference.md`
- `examples/lighttpd/configuration-reference.de.md`
- `reports/connector-configuration-inventory.json`
- `reports/audits/change-records/CR-20260823-pr309-lighttpd-config-reference-repair.md`
- `reports/audits/change-records/CR-20260823-pr309-lighttpd-config-reference-repair.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

### Tests and actual results

| Check | Actual result |
| --- | --- |
| `python -m unittest -v tests/test_connector_config_reference.py` | Passed: 2 tests. |
| `make check-connector-config-reference` | Passed; source-backed generation and semantic inventory validation completed. |
| `python -m unittest -v connectors.lighttpd.tests.test_patched_host_contract` | Passed: 35 tests, 2 skipped. |
| `make check-doc-links` | Passed. |
| `make check-bilingual-docs` | Passed. |
| `make check-variable-documentation` | Passed. |
| Focused Python compilation | Passed. |
| Focused security diff review | Passed: no reportable finding or security regression. |
| `git diff --check` | Passed on the final delivery diff before staging; rerun is performed for the staged commit. |

## Runtime evidence

This repair changes a source-to-documentation contract, not a connector runtime
path. The original failure happened in shared configuration-reference
validation before Apache or Lighttpd started. The regression tests therefore
provide the relevant evidence: they exercise the closed extractor against the
native source and verify the generated contract metadata.

## Checks not run and rationale

- Full local `make lint` cannot complete in this environment because its
  shared provisioning requires unavailable pinned NGINX/HAProxy inputs. No
  check was weakened and no environment fallback was used.
- The project pins Go `1.26.7`, while only Go `1.26.6` and `1.26.5` were
  locally callable. No toolchain acquisition was performed; hosted Go checks
  are required on the final PR head.
- Fresh hosted, SonarCloud, and master checks for the head created by this
  record were pending when this document was written and are not asserted here.

## Known limitations

This record cannot retroactively change the failed post-merge check history of
PR #309. It documents the corrective PR lifecycle and requires exact-head
success for the successor head and resulting `master` revision.

## Remaining risks

A future native Lighttpd directive change will correctly fail closed until the
source-backed inventory and its regression test are updated together. The
current repair does not create or claim new Lighttpd runtime evidence.

## Final diff and review status

The Parent-only correction is prepared for a fresh normal commit, exact-head
review, and protected PR merge. This Change Record does not itself authorize a
merge, a Framework/MRTS change, a Gitlink update, a direct `master` push, or a
quality-control change.

## Delivery status

This record is committed as a focused continuation of Parent PR #334. Its new
head requires a full fresh hosted and SonarCloud validation round before the
current explicit master authorization may be exercised. No merge result is
asserted in this record.
