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

## Acceptance criteria

- Repeated builds and retry after APXS failure work under the same external root.
- Staged registry symlinks/artifacts are not trusted or overwritten; symlinked
  children and checkout-contained output remain rejected.
- CI explicitly runs the containment/retry unit tests and two real builds;
  failure of either build fails the gate rather than being hidden by a retry.
- EN/DE documentation and traceability remain equivalent. Delivery requires
  fresh current-head CI and Sonar, including 0.0% new-code duplication.
- No new NGINX changes/runs, Framework/MRTS source or Gitlink changes, weakened
  controls, direct `master` writes, merge, or nine-profile B promotion.

## Implementation decision and rationale

When a regular registry `connectors` stage already exists, allocate a private
`rebuild.XXXXXX` directory below the canonical external staging root. Each
invocation then copies registry sources into its fresh `connectors` child.
Do not delete, overwrite, or reuse previous registry inputs/libtool artifacts.
Common-source staging retains its existing behavior. The bootstrap check runs
`make` twice with the same staging root and explicitly propagates each error:
`set -e` alone does not protect a loop inside `if ! (...)`.

## Changed files

- `connectors/apache/build/apxs-wrapper.in`
- `tests/test_apache_apxs_profile_registry_staging.py`
- `ci/checks/connectors/apache/check-apache-autotools-bootstrap.sh`
- `.github/workflows/test-apache.yml`
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

## Security impact

Build-output isolation is preserved. Existing registry source/artifact symlinks
cannot redirect a rebuild into the checkout; each rebuild gets fresh inputs.
Existing absolute-root, canonical containment, and child-symlink checks remain
active. Tests cover rejected roots, rejected symlink children, stale staged
source symlinks, APXS retry, and failure of either CI build. No authentication,
runtime fail-closed behavior, compiler warnings, CI requirements, or Quality
Gate is weakened. The externally selected root remains a trusted build input;
this change is not a defense against concurrent malicious directory owners.

## Runtime evidence

The local native Apache check proved two compilations, not host startup or
traffic: ownership setup failed before the worker ran. Local Common/sidecar
smokes prove only their service/component layers. Earlier exact-head receipts
at `327daf72` proved the selected Apache, HAProxy SPOP request, Envoy ext_proc,
Traefik native, and patched-lighttpd CRS cells; they did not prove complete
G1–G9 acceptance. A new successor needs fresh hosted evidence. At that earlier
head, Sonar reported Quality Gate `OK` and new duplication density/lines/blocks
`0.0%` / `0` / `0`; those values are not successor evidence.

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
approval, Framework/MRTS implementation, or merge was performed. Missing full
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
