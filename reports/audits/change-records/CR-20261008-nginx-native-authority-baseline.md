# Change Record: CR-20261008-nginx-native-authority-baseline

**Language:** English | [Deutsch](CR-20261008-nginx-native-authority-baseline.de.md)

Explicit baseline authority wiring; unit evidence only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-authority-baseline |
| Date (UTC) | 2026-10-08 |
| Base revision | `6b069af4c2c87cdbddd7efc8867f642b1dd03098` |

## Motivation and problem statement

The baseline must provide explicit native artifact authority to the collector and finalizer without promoting the raw evidence root or redefining global build roots.

## Acceptance criteria

For NGINX full-lifecycle selected closed native cases, preserve required initialized records, require actual prepared prefix and all five explicit fault libraries, create a fresh private authority child, and reject subsequent snapshot prefix mismatch.

## Implementation decision and rationale

prepare_nginx_native_authority runs after canonical init and before stage execution. Actual catalog selection intersects the Framework reader closed CASE_IDS and requires selected descriptors. Explicit NGINX_PREFIX supplies the same sbin/nginx and modules/ngx_http_modsecurity_module.so paths used by the native dispatcher. The producer receives current Parent/Framework roots and Framework/tools/MRTS, run identity, five original library inputs and artifact_root=STAGE_BUILD_ROOT. An exclusive 0700 host-runtime/native-authority-<run> directory receives the original authority. Collector gets --allowed-native-operation-root STAGE_BUILD_ROOT; finalizer gets --native-operation-authority with the original path. The later validated runtime snapshot must match the sealed prefix.

## Changed files

Only ci/runtime/lifecycle/run-no-crs-baseline.sh, new tests/test_no_crs_native_authority_wiring.py and this paired record.

## Commands executed

RTK-wrapped unittest first showed five missing-helper errors (RED). The new eight extracted-shell controls then passed in the combined wiring run. sh -n passed. Combined existing/new wiring: 48 tests, two missing Apache fixture failures and 26 existing dependency skips. The repository generator created the pair; archive and final whitespace checks are recorded in the handoff.

## Security impact

Missing prefix or any fixture blocks with nonzero exit after initialization; no selected required case is excluded. No legacy library fallback, shell-evaluated catalog data or native event fabrication. Fresh directory creation is descriptor anchored using existing Parent safe-directory checks. Producer performs independent strict source/path/digest validation; unit doubles prove wiring only.

## Runtime evidence

None. The new tests use bounded selection and producer doubles; they invoke no native binary, compilation or full baseline. They do not establish Root host roles, runtime provenance or canonical PASS.

## Known limitations

The authority producer requires clean current pinned source roots and prebuilt explicit artifacts. The actual invocation snapshot exists only after stage provisioning, so native callers must pass the prepared prefix before execution. Existing broad tests cannot fully execute in this isolated worktree because Framework fixtures are absent.

## Remaining risks

The coordinator must rerun integrated wiring against actual Framework and collector/finalizer commits, verify prepared build readiness, and perform fresh authorized native capture. Hashing alone does not verify the build.

## Checks not run and rationale

Full baseline capture, native compilation/runtime and canonical retention were outside this slice. Two existing Apache phase4 YAML fixtures are absent and 26 existing dependency-gated tests skipped; these are not new passing evidence. No packages installed.

## Final diff and review status

Focused shell/test/paired-record changes reviewed. Existing warning/capability/payload/event handling, global BUILD_ROOT and RAW_DIR collector boundary remain unchanged. No Root worktree, central validator, catalog, schema, Gitlink or MRTS writes.
