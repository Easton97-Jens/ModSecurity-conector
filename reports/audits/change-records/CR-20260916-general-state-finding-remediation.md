# Change Record: validated general-state finding remediation

**Language:** English | [Deutsch](CR-20260916-general-state-finding-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260916-general-state-finding-remediation |
| Date (UTC) | 2026-09-16 |
| Base revision | `e475baabf0787cbc804f176ae998b62156892825` |
| User authorization | “kümmere dich in dem bestehenden pr um die sichere behebung der sachen” |
| Delivery status | Extends Parent Draft PR #369 only. A normal commit and push to its existing branch are in scope; no merge, auto-merge, direct `master` write, Framework/MRTS/Gitlink change, or branch deletion is authorized. |

## Motivation and problem statement

The retained general-state run `20260913T142629Z-e475baa` mixed confirmed
Parent defects with runtime evidence gaps and Framework-owned observations.
This change repairs only the three confirmed, Parent-owned boundaries that have
a focused regression route:

- `FND-PARENT-1093`: Expat provenance is immutable in every preparation mode.
- `FND-PARENT-1096`: the opt-in Envoy response-phase smoke selects matching
  P1/P3/P4 rules and rejects duplicate evidence records.
- `FND-PARENT-1097`: Apache APXS receives a staged profile registry outside
  the canonical Parent checkout, including through the fresh-source Autotools
  bootstrap.

The existing PR's separately recorded lighttpd endpoint-metadata repair remains
unchanged. This record does not turn a blocked runtime observation into a
product diagnosis and does not change the Framework or MRTS.

## Acceptance criteria

- `EXPAT_GIT_REF` accepts exactly a 40- or 64-character hexadecimal object ID
  and Expat never resolves a mutable latest release.
- The default Envoy P1 smoke remains unchanged; a separate response target
  selects `modsecurity_response_companion_smoke.conf`, enables its response
  assertions, and exposes only its path-scoped P3/P4 fixture data.
- Response-phase evidence requires exactly one correlated P3 deny record and
  exactly one correlated P4 safe record, without response payload fields.
- APXS compiles a staged `connectors/profile_registry.c` and receives a staged
  include root. A direct or symlink-resolved staging location inside the
  canonical checkout fails before profile-registry artifacts are created.
- Focused regression tests and same-boundary negative controls pass without
  starting a native Envoy service. The local fresh-source Apache build reaches
  its module-output check, while its later runtime phase is blocked by a host
  filesystem that rejects `chown(...)=EINVAL`.

## Implementation decision and rationale

### Immutable Expat provenance

`prepare_expat_git_component` now always delegates to
`prepare_immutable_git_component`; `strict` continues to govern the shared
cache/fsck policy only. `required_runtime_component_sources` validates
`EXPAT_GIT_REF` before either mode can reach a Git or release-resolution sink.
The full-object predicate now accepts only exactly 40 or exactly 64 hexadecimal
characters. The Framework-provided default is the full 40-character commit
`92810461043fce37e70079b37ab1f04490a8f039`. The generic `go-ftw` and `albedo`
release-resolution paths are deliberately unchanged.

This removes a mutable upstream `releases/latest` selection from the Expat
build-input boundary. A mutable Expat reference now fails closed before Git or
release lookup.

## Security impact

The repair narrows source provenance, preserves the default Envoy test mode,
and prevents APXS from placing profile-registry build artifacts in a canonical
source checkout. It does not weaken a host, file-permission, UDS, URI, or
response-payload control. Unproven runtime observations remain unpatched.

### Envoy response-phase smoke evidence

`response-phase-smoke-envoy` is an opt-in Make target. It selects
`common/rules/modsecurity_response_companion_smoke.conf` and exports
`MSCONNECTOR_RESPONSE_PHASE_SMOKE=1`; normal `runtime-smoke-envoy` keeps its
P1 default rule fixture. Target-specific `override` assignments make a
command-line `RULES_FILE` or `MSCONNECTOR_RESPONSE_PHASE_SMOKE=0` unable to
reduce this target to P1-only coverage. The upstream helper emits
`X-Modsec-Upstream: block` only for `/phase3-block` and the response-body
marker only for `/phase4-marker`.

The event verifier now rejects zero, missing, or duplicate matching P3/P4
records. It does not retain response payload data. This corrects test evidence
selection; it does not claim native Envoy response-phase or original-URI
correlation evidence.

### Apache profile-registry staging

APXS/libtool can write object artifacts beside a C input. The wrapper now
resolves the canonical checkout and requested staging parent before creating
the staging directory, rejects paths inside the checkout (including through a
symlink), resolves the final root again, then copies
`connectors/profile_registry.c` and `.h` there. APXS receives only the staged
source and staged include root.

Normal out-of-tree builds remain supported. An in-checkout profile-registry
staging root now fails closed instead of allowing `.o`, `.lo`, `.slo`, or
`.libs/*.o` artifacts to dirty the source checkout.

The Autotools bootstrap extracts its synthetic checkout at
`$WORK_ROOT/source`, then supplies the sibling
`$WORK_ROOT/profile-registry` only to its `make` invocation. `WORK_ROOT` is a
private `mktemp` directory created after `umask 077` under the configured test
parent and removed by the existing bounded cleanup. This supplies the wrapper
an external stage for that synthetic checkout without weakening its
canonical-path or symlink rejection.

## Changed files

- `ci/provisioning/components/prepare-runtime-components.py`
- `tests/test_prepare_runtime_components.py`
- `connectors/envoy/Makefile`
- `connectors/envoy/harness/envoy_smoke_helper.py`
- `tests/test_envoy_transport_hardening_contract.py`
- `connectors/apache/build/apxs-wrapper.in`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.md`
- `reports/audits/change-records/CR-20260916-lighttpd-stock-sidecar-endpoint-metadata.de.md`
- `reports/audits/change-records/CR-20260916-general-state-finding-remediation.md`
- `reports/audits/change-records/CR-20260916-general-state-finding-remediation.de.md`
- `reports/audits/change-records/README.md`
- `reports/audits/change-records/README.de.md`

## Commands executed

| Command or check | Result | Observed result |
| --- | --- | --- |
| Verified project venv: `python -m unittest -v tests.test_prepare_runtime_components tests.test_envoy_transport_hardening_contract tests.test_apache_apxs_profile_registry_staging tests.test_apache_common_adoption` with bytecode and temporary output outside the checkout | passed | 134 tests passed; 5 existing Framework-dependent tests were skipped because the Framework test root did not match the Parent gitlink. |
| `sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh` and `sh -n connectors/apache/build/apxs-wrapper.in` | passed | Shell syntax accepted. |
| `sh -n connectors/envoy/harness/run_envoy_connector_runtime.sh` | passed | Shell syntax accepted. |
| `make -n -C connectors/envoy response-phase-smoke-envoy` | passed | Dry-run shows the companion rule file and `MSCONNECTOR_RESPONSE_PHASE_SMOKE=1`; no build or service ran. |
| `APACHE_AUTOTOOLS_TEST_PARENT=... APACHE_AUTOTOOLS_RUNTIME_PARENT=... make check-apache-autotools-bootstrap` | blocked_environment (make exit 2) | The fresh source snapshot completed Autotools configuration, `make`, and the module-output check; a later runtime `chown` on the controlled `/var/tmp` root failed with `EINVAL`. |
| `make check-bilingual-docs` | blocked_environment | The checker reported no error for either current Change Record, but failed on 20 pre-existing links whose Framework-Gitlink targets are absent from this worktree. |
| `git diff --check` | passed | No whitespace errors before delivery preparation. |

The Apache fake-APXS control proves that generated profile-registry artifacts
exist only under the external stage root. Its negative controls reject a direct
in-checkout root and a symlink resolving into the checkout. The Bootstrap
contract preserves its one private sibling stage assignment, while the partial
native bootstrap run proves that the build progressed beyond the original CI
failure point: it reached the module-output check before the unrelated host
ownership operation. The Expat controls reject mutable, abbreviated,
41-character, and 63-character references before Git/release lookup; 40- and
64-character references remain accepted. The Envoy controls preserve the
default P1 target and reject duplicate P3/P4 evidence.

## Runtime evidence

The Envoy helper fixture was exercised by the focused Python contract test,
not by a native Envoy process. The Apache fake-APXS test exercised the wrapper
argument and artifact boundary. The local Apache bootstrap additionally
exercised its real Autotools/APXS module build, but not its completed server
runtime because the controlled host filesystem rejected a later ownership
change. These are bounded local evidence routes only.

## Checks not run and rationale

No native Envoy build or service, completed Apache server-runtime check, full
connector matrix, SonarQube Cloud analysis, or hosted PR check has been run at
this follow-up's exact head. A native Envoy runtime run requires the separate
runtime preflight and a short, private absolute runtime root suitable for its
UDS; neither is implied by the static contract tests. The local Apache
bootstrap's post-build ownership failure is a host filesystem constraint, not
evidence that permits weakening the ownership logic. No Framework source or
externally prepared CRS content was changed or tested.

## Known limitations

- `FND-PARENT-1091` remains covered by its own lighttpd Change Record. Its
  immediate-client-reset test is a demonstrated scheduler race; a deterministic
  broken-peer harness belongs in a separate narrowly scoped test-stability
  change.
- `FND-PARENT-1092` (Traefik) remains `blocked_missing_evidence`: the proposed
  empty-body P2 root cause is contradicted by the Common finish path. A
  targeted runtime body A/B matrix is required before altering lifecycle code.
- `FND-PARENT-1096` is locally repaired only for rule/fixture/evidence
  selection. Native response-phase execution and original-URI correlation
  remain unverified.
- The five skipped tests in the combined suite require a Framework test root
  whose commit matches the Parent gitlink.
- The local Apache bootstrap requires an ownership-capable filesystem to
  complete its runtime phase. Its isolated `/var/tmp` root reached the module
  build but failed later at `chown(...)=EINVAL`; the corrected hosted rerun is
  still required for full runtime evidence.

## Remaining risks

- `FND-PARENT-1098` (Apache 403 versus 413) remains
  `blocked_missing_evidence`; changing `AP_FILTER_ERROR` before tracing the
  initial terminal condition could regress a fail-closed path.
- `FND-PARENT-1094` is Framework-owned and has no checked-in default
  `t:hexDecode` reachability. Exact external CRS content must be inspected in
  a separately authorized Framework assessment before any Framework patch.
- `FND-PARENT-1095` and `FND-PARENT-1099` are environment blockers. Archive
  owner restoration and NGINX `chown(...)=EINVAL` need a suitable host; no
  owner, ACL, symlink, or mode check was relaxed.

## Final diff and review status

This record documents local evidence for the current existing-Draft-PR update.
After delivery, local, remote-branch, and PR-head SHAs must be compared
exactly, and hosted checks, SonarQube, review state, and any later merge remain
separate observed facts. No merge is asserted.
