# Change Record: CR-20261008-nginx-cleanup-observation

**Language:** English | [Deutsch](CR-20261008-nginx-cleanup-observation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-cleanup-observation |
| Date (UTC) | 2026-10-08 |
| Base revision | 201c6194a0061efe49e854a02f8626170ddee3b1 |

## Motivation and problem statement

Native framing evidence needs an actual cleanup observation, not a fixture-created
cleanup claim. This bounded constructor prepares metadata from actual Common facts.

## Acceptance criteria

Preserve actual cleanup return/completion/taxonomy and native completion boolean.
Reject NULL and truncated output. Emit LOGGING metadata without fabricated source,
rule or transaction identity. Compile and execute real Common transition tests.

## Implementation decision and rationale

ngx_http_modsecurity_cleanup_observation accepts event, caller-owned reason buffer
and capacity, actual Common return, const contract and native completion boolean.
It returns 1 on construction, 0 on invalid/truncated input, leaving event unchanged
on rejection. The reason buffer must remain alive through serialization.

Call only after actual Common cleanup and native void cleanup have returned.
Native completion is true only when a transaction existed before cleanup and
cleanup returned. No native getter runs after free. The coordinator binds actual
request, transaction, host and protocol separately.

## Changed files

New connectors/nginx/src/ngx_http_modsecurity_cleanup_observation.h,
tests/test_nginx_cleanup_observation.c and this paired record only.
Module/Common/source-map wiring is coordinator-owned and unchanged here.

## Commands executed

RTK-wrapped cc -std=c17 -Wall -Wextra -Werror -Icommon/include compiled the test
with common/src/transaction_state.c to an external task binary, exit 0.
The binary executed normal complete phases/finish/cleanup, premature cleanup,
second cleanup, incomplete observation, preserved timeout, native0 and NULL/
truncation controls, exit 0.
Recompilation with -fsanitize=undefined and execution passed, exit 0, including
exact-fit reason capacity and unchanged contract. Direct EN/DE record validation
passed after correcting its required German heading/identity labels, exit 0.

## Security impact

Payload-free bounded formatting; no weakening, invented API return or synthetic
source identity. Empty rule metadata. LOGGING/allow reports cleanup success only,
not permission for a request. The constructor does not mutate the contract.

## Runtime evidence

No native NGINX build/runtime executed. Common state unit execution is not native
cleanup or host runtime evidence.

## Known limitations

The caller must supply actual facts and stable borrowed metadata. A native void
cleanup completion has no invented numeric API return. Native0 remains explicit.

## Remaining risks

Integrated source binding, serializer behavior and canonical runtime require the
coordinator's module hook and fresh evidence.

## Checks not run and rationale

Native NGINX runtime/build was outside this authorized slice. Full bilingual
repository validation has previously been blocked by 22 absent submodule link
targets; the new pair is checked directly. Ruff is unavailable; no installation.

## Final diff and review status

Focused source/test/record diff reviewed. Separate commit contains only owned new
files. No existing commits, module hooks, Common files or Gitlinks are changed.
