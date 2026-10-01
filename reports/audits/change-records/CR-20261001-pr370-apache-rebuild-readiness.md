# Change Record: CR-20261001-pr370-apache-rebuild-readiness

**Language:** English | [Deutsch](CR-20261001-pr370-apache-rebuild-readiness.de.md)

Scoped Parent follow-up for PR #370. New NGINX work and an actual merge are excluded.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261001-pr370-apache-rebuild-readiness |
| Date (UTC) | 2026-10-01 |
| Base revision | `327daf723e0e6798ee82a39577ecca1077f6188d` |

## Motivation and problem statement

The requested merge-preparation review found that the Apache APXS wrapper
rejected its own regular profile-registry staging directory on a second build
or retry. A focused regression reproduced the failure. The previous green
single-build CI could not detect it. This record covers that corrective
increment, not complete G1–G9 acceptance of the nine non-NGINX logical profiles.

Fresh CI at intermediate head `ac76cdbe` then exposed another current merge
blocker: pinned HTTPD 2.4.68 was no longer served by its configured download
endpoint (HTTP 404), before the Apache connector build. The official archive
matched the reviewed pinned SHA-256. A second focused Parent correction restores
that source without changing Framework pins or weakening source verification.

The subsequent user authorization permits a separate Framework fix/PR and
integration of its verified published commit. Framework PR
[#133](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/133)
repairs the second downloader that discarded the Parent-verified archive and
retried the unavailable endpoint. This Parent increment advances only the
Framework gitlink and its exact CI SHA projections; upstream component pins
and MRTS remain unchanged.

## Acceptance criteria

- Repeated builds and retry after APXS failure work under the same external root.
- Staged registry symlinks/artifacts are not trusted or overwritten; symlinked
  children and checkout-contained output remain rejected.
- CI explicitly runs the containment/retry unit tests and two real builds;
  failure of either build fails the gate rather than being hidden by a retry.
- Retired official HTTPD download endpoints may use the official archive only
  on typed HTTP 404, with identical filename/version and reviewed literal hash.
- EN/DE documentation and traceability remain equivalent. Delivery requires
  fresh current-head CI and Sonar, including 0.0% new-code duplication.
- Framework delivery is separate and verified before the authorized Parent
  pointer update. Exact workflow/test SHA consumers follow the published commit.
- No new NGINX implementation or manually initiated NGINX runs, MRTS changes,
  weakened controls, direct `master` writes, merge, or nine-profile B promotion.

## Implementation decision and rationale

When a regular registry `connectors` stage already exists, allocate a private
`rebuild.XXXXXX` directory below the canonical external staging root. Each
invocation then copies registry sources into its fresh `connectors` child.
Do not delete, overwrite, or reuse previous registry inputs/libtool artifacts.
Common-source staging retains its existing behavior. The bootstrap check runs
`make` twice with the same staging root and explicitly propagates each error:
`set -e` alone does not protect a loop inside `if ! (...)`.

The HTTPD-only downloader accepts the exact `downloads.apache.org/httpd/`
`.tar.bz2` URL and literal SHA-256 before considering an official
`archive.apache.org/dist/httpd/` fallback on typed HTTP 404. Other HTTP/network
errors, unexpected URLs/components, missing hashes, and integrity failures do
not select another source. Verify the same digest before tar inspection.
Keep the canonical configured URL/cache identity; the component JSON records
the actual `download_url`. A verified cache hit uses empty `download_url` and
`download_status=cached`, rather than inventing original-fetch provenance.

The Framework dependency advances from
`9181dc77dfb0685d87fa109e6800dc6052d77cc9` to the remotely available verified
`a35ac6d02a4e2e7a94ec7679e4e94877cc0126f9`. The Framework-owned change rechecks
safe regular HTTPD cache bytes, recovers only on direct HTTP 404/curl 22/zero
redirects, retains canonical metadata validation, and extracts a private
rehashed copy. Its shared downloader, APR-util controls, upstream pins and MRTS
gitlink are unchanged. The native Parent synchronizer projects exactly four
workflow SHA literals and one test fixture; dynamic identities and protected
NGINX projections are preserved.

## Changed files

- `connectors/apache/build/apxs-wrapper.in`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `tests/test_apache_httpd_archive_fallback.py`
- `ci/provisioning/components/prepare-runtime-components.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `.github/workflows/test-apache.yml`
- `modules/ModSecurity-test-Framework` (gitlink only; separately delivered source)
- `.github/workflows/test-connectors-with-crs-no-mrts.yml`
- `tests/test_ci_security_workflows.py` (exact Framework SHA fixture)
- `connectors/apache/README.md` and `connectors/apache/README.de.md`
- This Change Record pair and `reports/audits/change-records/README.md` /
  `reports/audits/change-records/README.de.md`

## Commands executed

Commands ran in the task-owned external Parent worktree through RTK. Outputs
and temporary files used the external task run root; no package was installed.

- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 MODSECURITY_INCLUDE_DIR=/usr/include MODSECURITY_LIB_DIR=/usr/lib/x86_64-linux-gnu python3 -m unittest tests.test_apache_apxs_profile_registry_staging tests.test_apache_request_transaction_cleanup tests.test_envoy_transport_hardening_contract connectors.lighttpd.tests.test_stock_sidecar_contract -q`
  — 95 tests passed with CPython 3.14.7 and the installed ModSecurity SDK;
  includes stock-sidecar loopback tests, not stock-lighttpd host acceptance.
- The repeated-build regression failed before the wrapper correction. The
  bootstrap error-propagation regression failed for first-build failure before
  explicit per-iteration error handling; both now pass.
- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONDONTWRITEBYTECODE=1 timeout 120s make check-common-helpers-c17 check-http-authorization-service-timeout BUILD_ROOT=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/build PYTHON=python3`
  — passed, including real authorization-service and response-companion
  lifecycle smoke checks. These are not complete connector-host results.
- `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp APACHE_AUTOTOOLS_TEST_PARENT=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp MODSECURITY_PREFIX=/usr timeout 120s make check-apache-autotools-bootstrap`
  — both APXS builds succeeded; the overall target failed before host startup
  because local `chown` returned `EINVAL` on the mapped filesystem. This was
  before the subsequent explicit loop error-propagation correction.
- `rtk proxy sh -n connectors/apache/build/apxs-wrapper.in`,
  `rtk proxy sh -n ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
  and `rtk proxy git diff --check` — passed during implementation; final rerun
  and exact-head hosted delivery status are recorded in PR #370.
- `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 make check-bilingual-docs PYTHON=python3`
  — initially blocked by existing Framework links because the task worktree's
  pinned Framework submodule was not materialized. After initializing only the
  unchanged pinned Framework checkout, the following command passed:
  `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp timeout 60s make check-bilingual-docs check-doc-links PYTHON=python3`.
  MRTS was not initialized; no links or checker were weakened.
- A system-Python CI-security test attempt lacked `yaml`; the existing Parent
  CPython 3.14.7 environment with PyYAML 6.0.3 was then selected read-only.
  `rtk proxy env TMPDIR=/var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/tmp PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /var/tmp/codex/ModSecurity-conector/pr393-python3147-hInzILPJ/venv/bin/python -m unittest tests.test_ci_security_workflows tests.test_change_record -q`
  — 51 tests passed. No environment or dependency mutation.
- `rtk proxy env PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 python3 ci/tools/new-change-record.py check`
  — Change Record structure passed; this is not runtime/evidence validation.
- Successor suite: the same focused command above with additional module
  `tests.test_apache_httpd_archive_fallback` passed 105/105 tests. The ten new
  source tests include managed-cache identity/reuse and literal-before-list CI
  caller wiring. The HTTP-404 regression failed before its correction.
- `rtk proxy curl --fail --location --silent --show-error --max-time 60 --output /var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/httpd-2.4.68-archive.tar.bz2 https://archive.apache.org/dist/httpd/httpd-2.4.68.tar.bz2`
  and `rtk proxy sha256sum /var/tmp/codex/ModSecurity-conector/runs/pr370-ready-without-nginx-20261001/httpd-2.4.68-archive.tar.bz2`
  — download passed; exact pinned SHA-256
  `68c74d4df38c26bed4dfbdb8f3baf1eb532f3872357becc1bba5d136f6b63c06`.
- An actual non-mocked `prepare_archive("httpd", ..., required_literal_sha256=True, verify_digest_before_archive_list=True)`
  call through RTK/CPython 3.14.7 passed the primary-404/official-archive route,
  matching that same hash before successful tar inspection. Only source
  preparation was tested; no additional host-runtime claim follows from it.
- Framework candidate data was materialized under the external controlled
  temporary root and bound to the published commit: both Git blob identity and
  copied-data `git hash-object` equal `e206cb6595c08aa1a13781d47e86a981ce96d1e5`.
  Through RTK and the Parent-owned Python3.14.7 environment,
  `ci/tools/sync-framework-component-versions.py --validate`, then `--sync` and
  `--check` with `--framework-sha a35ac6d02a4e2e7a94ec7679e4e94877cc0126f9`
  passed. Only workflow/test SHA projections changed; the final check lists
  no differences. `ci/tools/verify-framework-candidate-contract.py` passed
  before and after projection with the corresponding expected Parent SHA.
  These are static compatibility checks, not NGINX execution or runtime proof.
- The native `make check-ci-security-contract` rerun with the existing Parent
  Python and external `BUILD_ROOT` supplied as an environment variable passed:
  170 tests, five explicit unavailable namespace/identity integration skips,
  and actionlint/zizmor/gitleaks lock validation. The first attempt used a Make
  command-line `BUILD_ROOT` override, which inherited through `MAKEFLAGS` and
  invalidated the nested-Make precedence fixture; this was independently
  reproduced. No test or runtime helper was changed to obtain the pass.

## Security impact

Build-output isolation is preserved. Existing registry source/artifact symlinks
cannot redirect a rebuild into the checkout; each rebuild gets fresh inputs.
Existing absolute-root, canonical containment, and child-symlink checks remain
active. Tests cover rejected roots, rejected symlink children, stale staged
source symlinks, APXS retry, and failure of either CI build. No authentication,
runtime fail-closed behavior, compiler warnings, CI requirements, or Quality
Gate is weakened. The externally selected root remains a trusted build input;
this change is not a defense against concurrent malicious directory owners.

The HTTPD source recovery preserves canonical source/version/hash/cache
identity and adds digest-before-list enforcement; no new dependency pin or
NGINX source path is selected. Its independent review found no concrete bypass;
managed-cache and caller-guard tests supplement the initially reviewed eight
cases. Actual archive contents were hash-verified, not trusted from HTTP status.

## Runtime evidence

The local native Apache check proved two compilations, not host startup or
traffic: ownership setup failed before the worker ran. Local Common/sidecar
smokes prove only their service/component layers. Earlier exact-head receipts
at `327daf72` proved the selected Apache, HAProxy SPOP request, Envoy ext_proc,
Traefik native, and patched-lighttpd CRS cells; they did not prove complete
G1–G9 acceptance. A new successor needs fresh hosted evidence. At that earlier
head, Sonar reported Quality Gate `OK` and new duplication density/lines/blocks
`0.0%` / `0` / `0`; those values are not successor evidence.

Intermediate `ac76cdbe`: fresh Apache bootstrap passed (including eight staging
units and real non-root traffic), four CRS cells passed, and Apache CRS failed
before its build on HTTPD HTTP 404; the fail-closed aggregate consequently
failed. These results remain retained rather than being erased by retries.
Sonar at that exact intermediate head reported gate `OK`, 0.0% new duplication,
zero OPEN/CONFIRMED issues and zero TO_REVIEW hotspots. The source-recovery
successor requires its own new CI/Sonar round.

The source-fallback head `8a3999f3` retained 0.0% new duplication but Sonar
reported four new maintainability issues: duplicated SHA-256 regex and verbose
digit classes. The final focused correction shares a compiled lowercase digest
pattern and uses `\d` with `re.ASCII`, retaining the original ASCII-only URL
contract. Unicode-digit URL rejection is included in the existing regression.
No NGINX function or source contract is changed by this correction.
After that correction, the focused 105-test suite passed again, as did all
seven `tests.test_apr_util_static_contract` tests, bilingual/docs links,
Change Record structure and diff whitespace. Independent review confirmed
equivalent regex matching; published-head Sonar/CI still require fresh readback.

At Parent head `221e1068ecde20ec04355b8009aabcb0302c4cbb`, Apache bootstrap
passed but the Apache CRS cell failed with `missing_local_httpd_build` and the
aggregate failed closed; the other four cells passed. A direct unchanged
Framework-helper reproducer returned HTTP 404/exit 77 after discarding its
task-owned verified staged copy. The original archive remained retained.

The separately delivered Framework dependency at `a35ac6d0` has 13 successful
exact-head checks, three expected event skips and no pending/failing checks,
including both full hosted lint runs and CodeQL. Sonar analysis
`2026-10-01T17:39:04+0000` binds to that exact Framework head: gate OK, new
duplication 0.0%, duplicated lines/blocks zero, open/confirmed issues zero and
pending hotspots zero. Framework-owned 18 HTTPD, 13 APR-util and 20 downloader
regressions passed independently, and its real HTTPD2.4.68/APXS diagnostic build
passed without starting a host. These are external dependency facts, not
Parent host-runtime results. The new Parent/Framework combination requires
fresh Parent CI, Sonar and runtime receipts after publication.

## Known limitations

Complete G1–G9 acceptance of all nine non-NGINX profiles remains unproven:
HAProxy HTX, Envoy ext_authz, Traefik forwardAuth, and stock lighttpd lack the
required complete host campaign, and SPOP request-only results cannot prove
its response companion. Three complete starts per profile, complete phase
boundaries, failure/restart checks, and concurrency probes with RSS/FD
measurements remain separate evidence requirements. No production approval.

## Remaining risks

Fresh hosted CI/Sonar must validate the published successor. Private registry
stages accumulate until the owning external build root is cleaned; the wrapper
does not delete potentially user-owned previous output. The local filesystem
cannot supply the required non-root Apache startup evidence. Full nine-profile
acceptance cannot be replaced by this bounded build fix or green selected-cell CI.

## Checks not run and rationale

No new dedicated NGINX runs, full nine-profile G1–G9 campaign, load/production
approval, MRTS implementation, or merge was performed. Framework implementation
was explicitly authorized, delivered and verified in its own PR #133; this
Parent commit includes only the gitlink and its projections, not Framework
source files. Missing full
host prerequisites and profile-specific acceptance evidence are retained as
gaps, not waived. Current-head hosted verification occurs after publication
and is reported separately in PR #370.

## Final diff and review status

Independent read-only review confirmed the rebuild containment correction and
identified the loop's initially masked first failure; the latter was reproduced,
corrected, and covered by the new shell-control-flow regression. Final current
diff review, exact successor SHA, checks, Sonar, base freshness, conversations,
and draft/readiness status are delivery facts maintained in PR #370. No actual
merge or complete nine-profile readiness-B claim is made by this record.
