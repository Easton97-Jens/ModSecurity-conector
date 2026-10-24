# Change Record: CR-20261008-nginx-native-authority-producer

**Language:** English | [Deutsch](CR-20261008-nginx-native-authority-producer.de.md)

Explicit authority producer; unit evidence only.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261008-nginx-native-authority-producer |
| Date (UTC) | 2026-10-08 |
| Base revision | `9ecd63fce94d424526fe6a70da1021c8f0d02681` |

## Motivation and problem statement

Explicit authority must bind actual current clean Parent, Framework and MRTS identities and actual supplied artifact bytes without trusting a receipt.

## Acceptance criteria

Require distinct explicit source roots, exact current HEAD40 and both current Gitlinks; reject dirty sources, unsafe paths, mutable observations and existing output.

## Implementation decision and rationale

produce_native_authority checks the actual Git tuple before and after stable bounded hashes, then writes the closed schema_version 1 original exclusively as native-operation-authority.json, mode 0400. All CLI roots, run ID, binary/module paths and five fault libraries are mandatory. Output is beneath the explicit external artifact root in an existing private 0700 directory. Eight case digests derive from the closed input/begin/finish/write/budget mapping.

## Changed files

Only the new ci/runtime/lifecycle/nginx_native_authority.py, tests/test_nginx_native_authority.py and this paired record.

## Commands executed

RTK-wrapped unittest first failed for the missing producer, then the initial five actual-Git tests passed. Expanded producer/configtest checks passed 30 tests; runtime-path security passed 21 tests. Owner rejection uses explicitly injected foreign fstat metadata because this container rejects chown65534 with EINVAL. The repository generator created this thirteen-heading pair; its archive checker passed and git diff --check reported no whitespace errors.

## Security impact

NOFOLLOW traversal includes every component; artifact files must be current-user-owned, non022, bounded nonempty single-link regular files with stable metadata and bytes. FIFO opening is nonblocking. Root-owned sticky shared ancestors are allowed but final directories remain owned/non022. Git environment overrides are removed. No receipt supplies trusted digests.

## Runtime evidence

None. Controlled temporary Git repositories and dummy artifact bytes are unit evidence only. No build, compile, native invocation or host runtime occurred.

## Known limitations

Each artifact is bounded to 64 MiB and JSON to 16 KiB. Git snapshots and repeated hashes detect observed changes, not an atomic snapshot of all repositories. File modes are not protection against a privileged owner. Artifact hashes do not establish compiler, Engine library, release or native behavior.

## Remaining risks

The coordinator must independently verify actual build readiness and bind the returned current tuple to its selected run context. Retention must preserve original bytes and digest; canonical PASS remains outside this producer.

## Checks not run and rationale

Native build/runtime, Engine/archive readiness and integrated canonical retention were outside this slice. Three existing test_runtime_path_utils execute-only tests could not run through setup because chown65534 returns EINVAL. An initially mistyped runtime-path test module did not import; the correct test_runtime_path_security then passed. No package installation or remote analysis.

## Final diff and review status

Focused owned files reviewed; existing source, Gitlinks and commits preserved. The producer never updates Gitlinks or discovers replacement trusted roots.
