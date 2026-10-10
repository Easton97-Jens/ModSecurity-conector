# Change Record: Native Envoy test boundaries

**Language:** English | [Deutsch](CR-20260923-pr382-envoy-test-boundaries.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260923-pr382-envoy-test-boundaries` |
| Date (UTC) | `2026-09-23` |
| Base revision | `3c29004b060b461649383cdb0db9996feab51b05` |

## Motivation and problem statement

The native Envoy CI run 35847504839, job 107137107263, built Common and
libModSecurity and executed the Go packages. Three tests failed: an unsafe-mode
fixture became private under umask 077; a remove/create fixture could recycle
the owned inode; and the body-limit case expected a successful acknowledgement
on a transaction already made terminal by an invalid host acknowledgement.

## Acceptance criteria

Keep the valid HTTP 413 and payload-redaction controls. Reject an invalid host
acknowledgement permanently, retain the first error, and do not emit duplicate
events or resume request/response processing. Establish unsafe permissions and
a distinct replacement identity independently of runner defaults. Do not weaken
production guards, scanner settings, warning flags or native test selection.

## Implementation decision and rationale

Share only the real body-limit transaction setup between separate positive and
negative cases. The new negative case verifies repeated invalid and corrected
acknowledgements, blocked body/header processing and byte-identical event output
after retries. Preserve the original positive JSONL checks. Explicit chmod creates
the unsafe test file without changing process umask. Rename keeps the original
inode alive while creating the replacement; the existing real-socket ownership
control is unchanged. No production source or dependency is modified.

## Changed files

- `connectors/envoy/ext_proc/internal/processor/common_runtime_engine_test.go`
- `connectors/envoy/ext_proc/internal/processor/body_limit_host_action_test.go`
- `connectors/envoy/ext_proc/internal/processor/jsonl_test.go`
- `connectors/envoy/ext_proc/cmd/msconnector-envoy-response-observer/main_test.go`
- This paired Change Record.

## Commands executed

The changed native test helper and its consumer were formatted with gofmt.
Reconstructing the original consumer produced its exact published Git blob
`540644d88ff07f02bbc8e157497751417edd56a7`, confirming unrelated content was retained.
The existing required native workflow executes the repository build script with
`ENVOY_EXT_PROC_COMMON_TEST=1`, which runs `go test -mod=readonly -tags libmodsecurity -count=1 ./...`.
Fresh execution results for this change are pending at commit preparation.

## Security impact

No accepted finding, exclusion, weaker file mode, permission expansion or new host
capability. The negative host-action test becomes stricter rather than permitting
recovery after a terminal error. Test files and payloads remain temporary fixtures.

## Runtime evidence

The recorded failing run used the actual Common/CGo/native engine integration.
The new tests must pass in a fresh native run before V20 is marked complete.
They do not establish downstream client bytes, real Envoy reset behavior, or all
other connector routes.

## Known limitations

I09 and I10 remain open across other adapters; this repair removes identified
verification blockers, not all implementation gaps. I11 and I12 retain separate
physical-sink and live-host acceptance criteria.

## Remaining risks

Native integration, existing source contracts and exact-head Sonar findings and
duplication must be checked again. The independent secret scan remains unresolved.

## Checks not run and rationale

No full native build was run in the editing container: repository download failed
because GitHub DNS resolution was unavailable there. GitHub APIs remain usable;
remote CI is the native execution path. No pass is inferred from test presence.

## Final diff and review status

Bounded test-only repair on the existing Draft PR #382. Preserve concurrent Apache
and native CI work. No merge, master update, force push or Framework/MRTS edit.
