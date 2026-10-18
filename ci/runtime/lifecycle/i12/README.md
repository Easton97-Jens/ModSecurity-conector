# I12 private capture sources

**Language:** English | [Deutsch](README.de.md)

This test-only source contract preserves the exact NGX, HAProxy, Envoy, Apache,
Traefik and lighttpd capture implementations used for I12 review. It neither
changes connector product files nor launches a host. A source application,
configuration load, build or driver exit does not establish runtime qualification.
Root reviews original physical observations and the independently sourced oracle
separately.

`manifest.json` maps logical source names to SHA256 objects. Identical collectors,
clients and backends occur once. Close variants are exact unified deltas against a
shared object. Current `native-lifecycle-observer.c`, its header and the SDK
accessor remain repository references; historical C52/H5, C270/H5 and Ca4/H581
variants are hash-bound deltas, without copied observer trees. The current shared
base is C `0d903fc5…`, H `5b7d8fa7…`, SDK accessor `89ff282b…`; see the manifest
for complete hashes. Historical profile input hashes bind to
`8cc32dceb06121f589150a9794f28878c5e4ba2a`; current-copy revision binding is
separate as described below.
Historical scoped-equivalent revisions and distinct observer ABIs remain explicit.
Stored deltas use zero context; whole-base and result hashes still cover every
byte and native patch application is checked without fuzz. One archived helper
with original trailing whitespace uses transparent JSON-line storage. Export
restores its exact original bytes; source is neither trimmed nor normalized to
pass whitespace checks.

| Source variant | Separate capture scope |
| --- | --- |
| `nginx` | Exact three-TU host overlay, typed host helper, driver/backend and waited client; supported Safe fixture09 |
| `haproxy-direct` | Native HTX binding/filter and SSL-write capture |
| `haproxy-companion-host` | Separate response-companion host variant |
| `haproxy-spop-agent` | Separate diagnostic request-agent/backend variant |
| `envoy` | Shared ext_proc/authz capture source; actual authz backend and distinct ext_proc backend retained separately |
| `apache` | Exact three product-TU overlays and APR/native/host helpers |
| `lighttpd` | Separate stock-sidecar and patched-native fixtures, including original and empty cases |
| `traefik-native` | Actual native-UDS middleware/engine/runtime observation variant |
| `traefik-forwardauth` | Separate authorization/response-observer source variant |

These nine **source variants** are not nine qualified runtime routes. Shared
source never transfers execution, EOS, identity or outcome between logical routes.
Framework and MRTS repositories/gitlinks remain outside this contract. Private
fixture definitions are run-scoped capture inputs, not reusable catalog additions.

## Verify and apply

From the Parent root:

```sh
rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py verify
rtk proxy python3 -B -m unittest discover -s ci/runtime/lifecycle/i12 -p test_capture_sources.py -v
```

Tests write only temporary data below `/var/tmp/codex/ModSecurity-conector`; set
`I12_TEST_ROOT` to an existing authorized external directory when necessary.
The source application uses the external storage root declared in the manifest.

Prepare a **disposable source copy**, without Git metadata, symlinks or hardlinks.
Copy the required base files listed in the selected variant's `source_targets`;
each non-null `before_sha256` must match exactly. Required SDK/upstream sources,
generated headers and toolchains are separate build inputs, not bundled artifacts.
Create `.i12-disposable-source-copy.json` in that external copy with exactly:

```json
{
  "format": "i12-disposable-source-copy-v1",
  "path": "/var/tmp/codex/ModSecurity-conector/disposable-i12-copy",
  "disposable": true,
  "parent_sha": "8cc32dceb06121f589150a9794f28878c5e4ba2a"
}
```

The path must identify the actual physical copy. Then, for example:

```sh
rtk proxy python3 -B ci/runtime/lifecycle/i12/capture_sources.py apply --profile nginx --source-copy /var/tmp/codex/ModSecurity-conector/disposable-i12-copy
```

The tool verifies all bases and objects before writing, applies exact-context
deltas without fuzz, and records resulting hashes in
`i12-source-application-receipt.json`. Capture programs are materialized below
`.i12-capture/<variant>/` and are never imported or executed. A missing marker,
changed base, changed delta, Git checkout/metadata, symlink, hardlink, path escape
or existing capture destination is rejected. Git metadata belonging to the
declared external **storage control plane** is outside the disposable subtree;
it does not authorize a checkout nested within that subtree.

## Current revision and complete export inventory

The v1 marker and its fixed historical input baseline remain supported unchanged.
Current source copies use **v2**. A current revision must never be labelled with
that historical baseline. The trusted source producer exports the complete
committed Parent tree with `git archive`, and records `git ls-tree` file modes,
tree identity and gitlink revisions. Gitlink contents are excluded. The producer
binds these Git commands and their exact revision independently; the capture tool
does not authenticate a commit merely because a marker contains 40 hex digits.

The v2 marker has exactly these fields:

```json
{
  "format": "i12-disposable-source-copy-v2",
  "path": "/var/tmp/codex/ModSecurity-conector/disposable-current-copy",
  "disposable": true,
  "source_revision": "ad510c3b4168ff0e11fc36803e2ce4127a0689ad",
  "snapshot_manifest": ".i12-source-export-manifest.json",
  "snapshot_manifest_sha256": "<complete lowercase SHA256 of the frozen inventory>"
}
```

Replace the illustrative path/revision and SHA256 placeholder with the actual
producer-bound values. `.i12-source-export-manifest.json` has exactly `format`
(`i12-source-export-manifest-v1`), `source_revision` (matching the marker),
`git_tree` (complete 40-character lowercase Git tree identity), `files`, and
`gitlinks`. `files` maps **every** exported Parent regular-file path to exactly
`{"mode": 420, "sha256": "<complete lowercase SHA256>"}`; executable Git files
use mode 493 instead of 420. The file hash covers all bytes, including binary
fixtures. `gitlinks` maps each exported gitlink path to its full 40-character
revision; an absent or empty gitlink directory is permitted, its contents are not.
Both mappings use bounded relative paths without Git metadata or path escapes.

Only the marker and inventory themselves are excluded from that complete file
inventory. Duplicate fields, unknown schema fields, revision/hash mismatches,
missing or extra files/directories, wrong file modes, links, special filesystem
objects and gitlink contents are rejected before capture writes. Every selected
profile `before_sha256` is still checked independently; a valid new snapshot
cannot authorize a changed capture base. Validation reads all inventory files and
refuses files that change while being hashed. The full frozen inventory remains
in the copy after capture and describes the **pre-capture** source, not build
outputs. Build in a separate directory after applying capture; a used copy cannot
be submitted as an untouched export again.

The application receipt records `source_revision`, `source_git_tree`, inventory
SHA256, file count and gitlink metadata separately from
`delivery_product_baseline`. This prevents a current build from inheriting the
historical baseline identity. Preserve that receipt, the inventory, producer
commands and source hashes alongside the instrumentation delta and build/load
evidence. The inventory/receipt prove source application only; they do not prove
a complete build, loaded-module identity or a qualified host transaction.

The current shared observer matches the selected public SDK constructor's
`char *` or `const char *` qualification without dropping compiler warnings.
Historical `ad8e5e36…`/`f9f63b62…` objects remain exact reverse deltas from the
current repository bytes. All earlier profile and object result hashes remain
unchanged; native ABI variants still require their own complete build binding.

## Build, ABI and evidence boundaries

Retained prepare/build/driver scripts are exact source records. Some contain
historical run paths; others use the sealed controller ABI `/mnt/src`,
`/mnt/fixtures`, `/mnt/artifacts` and `/task`. Inspect them and review relocation
before a new run. Relocated or edited bytes need a new source/hash binding. This
tool does not recreate, relax or bypass the approved controller's UID, peer,
resource, ownership, filesystem or capability checks. Do not execute archived
launchers directly against a product checkout or old evidence directory.

- NGX binds nginx1.31.6, SDK3.0.14 and the original 33 Parent TUs plus one generated
  registration TU. Fixture09 omits native MIME Clear: SDK3.0.14's merge discards
  same-load MIME additions when Clear is set. Preserved fixture08 remains the
  distinct measured MIME-out case. Native limits and MIME decisions remain SDK
  owned. The driver has a real HTTP backend in a dedicated thread; clients are
  separate waited processes. Connection/URI/header-add APIs remain unwrapped.
- HAProxy binds3.2.25, SDK3.0.14, the declared37 GNU wraps and separate SSL_write
  helper. Direct, companion-host and agent sources are distinct. Public
  `openssl.cnf` files are configuration only; no key or certificate is included.
- Envoy binds the recorded Go1.27.2/native SDK3.0.14 contract. The eight exact
  C/Go/build source changes and two source-copy Go regression files remain
  separate from physical host evidence. Existing strict CL/chunked and gRPC
  terminal-parser controls are retained as source and can run after materialization.
- Apache binds2.4.66/APR1.7.6/SDK3.0.14. The historical C17/F-PIC/no-LTO overlay
  relinks baseline module objects using real APR flags/system Apache headers;
  this is not a claim of a clean full module rebuild.
- lighttpd binds1.4.85/SDK3.0.14. Patched native needs the existing repository patch
  `connectors/lighttpd/patches/0001-lighttpd-msconnector-stream-hooks.patch`, exact
  hash in the manifest, and `LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION=2`.
  Stock modules are incompatible. Use matching generated core headers and the
  existing native build scripts. Borrowed synchronous HTTP/1.x entity callbacks
  occur before transfer framing; HTTP/2 is excluded.
- Traefik native and forwardAuth retain their distinct exact source and observer
  revisions. Their native C/Go/SDK build inputs require the owning native recipe;
  this source export does not establish a fresh build or host version.

Compiler warnings, native pins, SDK-owned body limits, original unknown oracles
and historical observations remain unchanged. The manifest excludes keys,
certificates, binaries, archives, caches, Git metadata and heavy raw evidence.
Any new execution still requires independently bound loaded images, effective
configuration, real clients/backend, native phases/EOS/finish/free, physical logs,
cleanup, neighbor health and Root review.

## Intentional original oracle nulls

The oracle reconciler accepts `intentional_null_fields.visible_status` only for
an original, explicitly present `visible_status: null` without an unresolved
expectation reason. Root must separately interpret that field and supply physical,
versioned primary proof bound to the record's independent sources. The complete
effective oracle must remain byte-semantically identical to the original; this
declaration cannot accompany a correction or replacement expectation. Missing
`native_result`, `phase` or `visible_status` is still rejected. For example, the
original `phase2_over_limit` contract leaves the client status configuration
dependent; its null is distinct from an unknown fixture or missing measurement.

This source-only disposition preserves the original null and awards no lifecycle
qualification. Client/host observations, all applicable lifecycle fields, fresh
execution and separate Root packet review remain mandatory. Other null fields
and unresolved original oracles cannot use this exception.
