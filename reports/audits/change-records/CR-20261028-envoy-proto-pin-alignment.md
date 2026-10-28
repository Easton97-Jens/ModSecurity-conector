# Change Record: CR-20261028-envoy-proto-pin-alignment

**Language:** English | [Deutsch](CR-20261028-envoy-proto-pin-alignment.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261028-envoy-proto-pin-alignment |
| Date (UTC) | 2026-10-28 |
| Base revision | `32b63db8ae38fbec20e5609495171b19373e17d6` |

## Motivation and problem statement

After inventory admission was repaired in PR #429, Envoy contract and CRS runtime jobs reached their build preflight and rejected the pinned Go proto version. The Parent lock still specified v1.37.0 while the already approved go.mod required github.com/envoyproxy/go-control-plane/envoy v1.40.0. Baseline b8f76fd718bf26dd3a4345dd6700534690d8a49d has the same mismatch.

## Acceptance criteria

Align the Parent proto lock with the approved manifest while retaining the exact native build gate and existing security floors. Add a consistency regression, preserve module/dependency files and all inventory selections, and regenerate derived artifacts through their native producer.

## Implementation decision and rationale

Advance ENVOY_GO_PROTO_VERSION to v1.40.0. The existing dependency regression now requires exactly one official module/version assignment and equality to the parsed go.mod requirement. Framework synchronization owns only ENVOY_RELEASE/ENVOY_IMAGE in this contract and therefore preserves the Parent proto pin.

## Changed files

connectors/envoy/config/envoy-ext-proc-versions.env; tests/test_ci_security_workflows.py; config/testing/active-cases.json; reports/testing/test-selection-archive.generated.json; this EN/DE Change Record pair. Only two reviewed source bindings change. Compiler guides were regenerated and remained byte-identical.

## Commands executed

All project shell commands used task-owned RTK v1.0.1 bypass. Three focused workflow/dependency methods passed under Python 3.15.1. The new consistency assertion failed with old v1.37.0 and passed with v1.40.0. The main agent executed the unchanged precompile shell block against the actual go.mod: old pin exit 2 with the hosted diagnostic, corrected pin exit 0. Native compiler-guide generation and git diff --check passed. Native archive regeneration followed the two reviewed binding changes. Complete admission (100 default / 1893 on demand), archive --check, EN/DE documentation, 103 variable references, repository/documentation links and whitespace passed.

## Security impact

The exact proto pin check and existing dependency security floors remain active. No Go module/sum, compiler, sanitizer, native source, permissions, credentials or isolation changes. The regression detects future one-sided manifest/lock drift instead of allowing an unreviewed mismatch.

## Runtime evidence

Contract jobs 122787881979 and 122787859265 and CRS runtime job 122787881189 explicitly report the same precompile mismatch on head cef2ab5ee8fe35e316620acbee5d9eb2f0f73bf3. Native security job 122791600138 reports build_ext_proc.sh exit 2 with hidden inner stderr; association with the same preflight is an inference. Local evidence proves only the exact precompile boundary, not a complete native build or hosted runtime.

## Known limitations

The complete native Envoy build was not run locally: no Go executable on PATH and no local ModSecurity SDK/headers/libraries were available. No packages were installed. Fresh current-head hosted CI remains required.

## Remaining risks

Later independent native build/runtime failures remain possible and must retain their own evidence. Dependabot changes to this proto dependency must carry the paired Parent lock update; the new consistency test makes drift visible.

## Checks not run and rationale

No additional connector matrix, I12 qualification or broad security scan. The existing hosted CI is the full native build/runtime validation boundary; local manifest/precompile success does not substitute for it.

## Final diff and review status

The scoped diff changes one Parent pin and adds ten assertions/setup lines to an existing regression, with derived hash companions and paired traceability. No reader-facing compiler-guide content changed. Final publication/check status remains bound to the actual PR head.
