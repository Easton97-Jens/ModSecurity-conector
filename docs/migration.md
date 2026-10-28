# Migration and current behavior

**Language:** English | [Deutsch](migration.de.md)

Use this guide when updating an existing checkout or configuration. It explains
what changed since the earlier documentation refresh and where the current
source contracts live. It does not change runtime defaults, select a ruleset,
or claim that an existing deployment has been validated.

## Before updating

Record the deployed connector/host versions and the configuration you actually
use. Update the checkout and its recorded submodules together. Read
[Version pins](reference/version-pins.md), then compare the matching current
[host example](../examples/README.md) with your adapted configuration. Preserve
service identities, private endpoints, rule ownership, and log permissions.

A logical profile is a topology, not just a host name. Do not replace an
authorization/companion profile with a native streaming route while describing
it as a configuration-only update.

## Body limits now belong to the engine

The earlier transitional explanation that connector response limits remain
accepted as compatibility or capacity values is no longer the current contract.
The named connector-owned cumulative request and response options below are
removed. Unknown/removed options fail configuration rather than being ignored.
There is no renamed cumulative connector-size option to substitute for them.

| Layer or integration | Removed settings | Current policy owner |
| --- | --- | --- |
| Common Runtime | `request_body_limit`, `response_body_limit`, `body_limit_action` | Native engine rule configuration |
| Native connector directives | `modsecurity_request_body_limit`, `modsecurity_body_limit_action`, `modsecurity_response_body_limit`, `modsecurity_phase4_body_limit` | Native engine rule configuration |
| HAProxy filter options | `request-body-limit`, `response-body-limit` | Native engine rule configuration |
| Envoy service options | `max_request_body_bytes`, `max_response_body_bytes` | Native engine rule configuration |
| Traefik native middleware option | `maxRequestBodyBytes` | Native engine rule configuration |

For request inspection, review `SecRequestBodyAccess`, `SecRequestBodyLimit`,
`SecRequestBodyNoFilesLimit`, and `SecRequestBodyLimitAction`. For response
inspection, review `SecResponseBodyAccess`, `SecResponseBodyMimeType`,
`SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit`, and
`SecResponseBodyLimitAction`.

Do not mechanically translate an old connector limit into a new engine value:
review the intended application policy. The connector must not infer values
from rule text, inject defaults, select Reject/ProcessPartial, or truncate the
body to its own inspection prefix. Omitted directives keep native
libModSecurity semantics. `DetectionOnly` also keeps actual engine semantics.
The authoritative details are in [Body-limit ownership](phase4-mode-budget.md).

## Phase-4 modes are not size policies

`off`, `safe`, and `strict` select supported late-intervention handling. They
do not select MIME types, a byte budget, or an engine limit action.

`off` does not turn off the engine or response inspection. `safe` is not
permission to ignore native Reject results, transport failures, or processing
errors. `strict` requires the selected profile's supported host action and can
be rejected at startup. Already-sent status, headers, and bytes cannot be taken
back. The `all` example layout is not a fourth phase mode.

The shared source default for Phase-4 mode is `off`, defined by
`MSCONNECTOR_DEFAULT_PHASE4_MODE` in `common/include/msconnector/options.h`.
An example that explicitly selects `safe` or `strict` is not changing that
source default. Use the generated host references for context and inheritance.

## Safety limits that remain

Removing cumulative connector inspection limits does not remove bounded
working memory or validation. Keep individual chunk/frame/message caps,
header/event metadata limits, correlation limits, timeouts, descriptor and
file-range validation, checked reads, pointer checks, and overflow guards.
A reusable working buffer is not a cap on total body size.

Authorization routes still have real host or protocol ceilings:

| Profile boundary | Remaining limitation |
| --- | --- |
| Envoy ext_authz | Host `max_request_bytes` bounds the request body supplied to authorization; the response observer does not make requests incremental |
| Traefik forwardAuth | Host `maxBodySize` buffers and bounds the forwarded request body |
| Composite Traefik authorization response | Host `maxResponseBodySize` limits the authorization response, not the upstream application response |
| HAProxy SPOE/SPOP | A bounded message carries a request sample; an incomplete sample does not prove full P2 inspection |

Do not remove these host settings merely because a similarly named connector
option was removed. Native streaming profiles are separate paths. Review the
[ten-profile matrix](body-inspection-review-matrix.md) and selected host guide
for incomplete samples, framing restrictions, and unproven behavior.

## Test selection is centralized

Normal local, CI, and scheduled functional checks use
[config/testing/active-cases.json](../config/testing/active-cases.json).
The 100-case core and the separately authorized guarded offline Python
exception have distinct accounting. Additional offline cases do not imply
additional connector E2E selection.

```sh
make check-active-inventory
make quick-check
```

The admission check validates the complete inventory without starting tests.
`make test` executes the admitted selection with its actual prerequisites.
Unknown/empty selections and changed source bindings are errors, not reasons
to truncate the selection or bypass the checks. Standard aliases and filters
remain subsets, not full-profile evidence.

Archived assessment suites are not automatic defaults. Specialist execution
requires a separate current request and the documented `ON_DEMAND_TESTS=1`
opt-in. Neither this guide nor that flag authorizes new I12 captures. Use
[Testing and evidence](testing-and-evidence.md), [Test entry points](../tests/README.md),
and the recorded closeout documents to distinguish current selection from
historical coverage.

## Toolchains, generated files, and external origins

`ci/tooling/project-versions.lock.json` owns ordinary project toolchain and
Framework/MRTS revision selection. `.python-version` and `.go-version` are
generated views. Security tools/action pins and protected broker identities
retain their separate reviewed contracts. Do not update one view in isolation
or use a floating source to make a local command pass.

Generated compiler guides, `examples/common/`, host configuration references,
and generated reports must be updated through their generator/source contract.
Manual wording improvements belong in maintained guides unless the generator
is deliberately updated and regenerated too.

The [licenses area](../licenses/README.md) remains a provenance/reference area:
upstream project, recorded revision/license basis, retained notices, and local
differences. It does not relicense imported material or declare one license
for the entire repository.

## Validate the migrated setup

First validate the selected host configuration with its documented checker or
root `check-config` target. Then run only the intended admitted tests. Record
the revision, logical profile, rules, run ID, artifacts, and remaining
limitations for any runtime claim. A passing parser, build, documentation
check, or scanner is not a deployment qualification.

For documentation changes use `make check-bilingual-docs` and
`make check-doc-links`. For operational risk and sensitive data handling read
[Operations and security](operations-and-security.md).
