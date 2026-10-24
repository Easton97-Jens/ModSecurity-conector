# Project version pins

**Language:** English | [Deutsch](version-pins.de.md)

## Canonical Parent configuration

Maintain ordinary Parent revision and toolchain selections in
[`ci/tooling/project-versions.lock.json`](../../ci/tooling/project-versions.lock.json).
The closed schema has exactly five keys:

| Key | Meaning |
| --- | --- |
| `schema_version` | Integer schema identifier |
| `framework_sha` | Exact ordinary Framework revision |
| `mrts_sha` | Exact nested MRTS revision |
| `python_version` | Stable Python 3.14 patch toolchain |
| `go_version` | Stable Go toolchain |

Read the selected values directly from the linked JSON record; this reference
does not maintain another copy of them.
[`.python-version`](../../.python-version) and
[`.go-version`](../../.go-version) are generated views retained for setup actions
and existing consumers. Do not maintain them as independent configuration.
Each Go module retains its separate compatibility floor in `go.mod`;
that floor and the selected build toolchain serve different purposes.

## Revision provenance

The ordinary workflow reader validates bounded, data-only JSON and rejects
duplicate/unknown keys, malformed or non-ASCII values, and symlinked inputs.
It independently requires the lock bytes to match the exact Parent commit's
regular Git blob, the Parent Framework gitlink to match `framework_sha`, and
the Framework MRTS gitlink to match `mrts_sha`. Initialized, independent
Framework/MRTS repositories must have those exact materialized HEADs. Git
replacement objects are disabled for provenance checks. Changing a lock field
alone cannot override a conflicting gitlink or checkout.

The protected NGINX root broker retains its separate reviewed immutable
broker/Framework tuple in its dedicated caller contract. Ordinary lock changes do not
activate or repin that privileged caller. See the
[broker contract](../security/trusted-nginx-root-broker.md).

## Component and security-tool ownership

Component versions, official source URLs, checksums and approved release tuples
remain canonical in the selected Framework's
[`ci/lib/common.sh`](../../modules/ModSecurity-test-Framework/ci/lib/common.sh).
The Parent lock selects that complete immutable Framework source; it does not
copy every component definition into a second authority. Framework component
updates belong to that repository. The reviewed Parent submodule updater then
selects the new Framework gitlink/lock and synchronizes its explicit Parent
projections. No MRTS source change follows implicitly.

Action pins and security-tool release/digest records remain in the distinct
[`ci/tooling/security-tools.lock.yml`](../../ci/tooling/security-tools.lock.yml)
under their constrained workflow/tool updater. Dedicated protected release
contracts retain their own review boundary. Centralizing ordinary selections
does not combine these authorities or expand publisher write permissions.

## Updating and checking

After an authorized toolchain selection change in the JSON lock, regenerate
its two views and check them with the repository-native targets:

```sh
make sync-project-versions
make check-project-versions
```

Local working agreements may require an execution wrapper around these native
command payloads. `ci/tools/sync-project-versions.py --sync` and `--check`
implement these targets. `--check` reports drift and fails instead of silently
repairing it. Exact committed revision provenance is a separate check: the
ordinary workflow reader runs
`ci/tools/read-framework-revisions.py --parent-sha <exact-parent-sha>` after
materializing the selected repositories.

The Python and Go updaters change only their own lock field and corresponding
view; they retain existing metadata, monotonic-version and publication guards.
The Go updater may also synchronize its separately bounded Envoy module bundle.
Publisher guards check the central lock's field scope for existing branches and
new candidates. The Framework updater changes the approved ordinary Framework
selection and its registered projections, preserving toolchain/MRTS fields.

Writers share a `flock` on the `ci/tooling` directory, check file identity and
contents before replacement, and track replacements before directory fsync so
an operational failure can roll them back safely. Rollback preserves unrelated
concurrent edits. Individual file replacement does not make a multi-file
filesystem transaction crash-atomic; a crash can leave detectable view drift.
Rerun the checks before publication and repair only task-owned drift.

## Evidence boundaries

A synchronized view, provenance check or unit-test pass proves its own layer.
Real connector runtime and Sonar results must bind to the delivered exact head.
Framework, Parent and MRTS delivery remain separate; a Parent revision change
neither merges a Framework PR nor authorizes privileged broker activation.
