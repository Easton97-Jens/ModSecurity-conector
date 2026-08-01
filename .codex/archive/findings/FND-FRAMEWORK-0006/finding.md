# FND-FRAMEWORK-0006 — NGINX archive digest can be unset before Framework provisioning

## Identity

| Field | Value |
| --- | --- |
| ID | `FND-FRAMEWORK-0006` |
| Category | `security_validated` |
| Repository / ownership | `framework` / `framework` |
| Priority | `P2` |
| Severity / confidence | `medium` / `validated` |
| Status / feasibility | `fixed` / `feasible_now` |
| Release blocker / security relevance | `false` / `true` |

## Summary and impact

Before the repair, the Framework NGINX GitHub release-archive path accepted an
empty `NGINX_SHA256`, recorded a local-only hash, and extracted the selected
archive. Substituted release bytes could consequently reach the NGINX build
path without a reviewed matching digest.

The task branch now defaults to a reviewed official release tuple:
`release-1.31.2`, `nginx-1.31.2.tar.gz`, and SHA-256
`af2a957c41da636ddc4f883e4523c6d140b4784dbce42000c364ae5092aa473c`.
It rejects an explicitly empty, malformed, mismatching, or tuple-inconsistent
configuration before network use, verifies cached or refreshed candidates,
stages a private archive below `NGINX_BUILD_DIR`, reverifies that exact
extraction input, and passes only it to `tar`. The source-archive control is
locally fixed; post-merge verification remains required before this finding can
become `verified` or `closed`.

## Observed and expected behavior

The pre-fix path did not reject unset, whitespace-only, trailing-whitespace,
or malformed digest values before archive selection/download. It conditionally
compared a digest only when non-empty, so the selected candidate could be
extracted after a local hash was recorded.

Every `github-release` candidate must now have a non-empty syntactically valid
digest before latest resolution, cache use, download, extraction, or build
work. A matching digest must cover both the selected candidate and the exact
private archive input passed to `tar`. For a fixed release, the source ref must
equal the release tag and the asset name must be the expected NGINX release
asset for that tag.

## Affected files and symbols

- `modules/ModSecurity-test-Framework/ci/lib/common.sh` — `NGINX_SHA256`
  configuration contract.
- `modules/ModSecurity-test-Framework/ci/provisioning/prepare-nginx-build.sh`
  — `validate_nginx_archive_configuration`, `resolve_nginx_release_tag`,
  `verify_nginx_archive_digest`, `stage_verified_nginx_archive`, and
  `download_nginx_source`.
- `modules/ModSecurity-test-Framework/ci/tools/check-common-versions.py` —
  release-asset metadata and no-partial-update provenance verification.
- `modules/ModSecurity-test-Framework/tests/security_regression/test_nginx_archive_digest.py`
  and `tests/fixtures/nginx-archive-digest/` — isolated local regression
  fixtures and archive boundary controls.
- `modules/ModSecurity-test-Framework/tests/security_regression/test_nginx_release_provenance.py`
  — no-network release metadata tuple regression controls.

## Preconditions and reproduction

1. The Framework `github-release` NGINX source-build path is invoked with a
   digest, source, release-tag, cache, or refresh configuration.
2. The retained assessment and task-run evidence are available.
3. Pre-fix, run `tests.security_regression.test_nginx_archive_digest` and
   observe required empty/whitespace/malformed fail-closed assertions fail.
4. Post-fix, run
   `rtk env TMPDIR=<task-run>/tmp python3 -B -m unittest tests.security_regression.test_nginx_archive_digest tests.security_regression.test_nginx_release_provenance -v`.
   All twelve cases must pass.

## Root cause and remediation

The release-archive path conditionally compared `NGINX_SHA256` only when it
was non-empty; otherwise it recorded a local hash and extracted the candidate
archive. This was the Framework NGINX release-archive integrity boundary.

The repair requires `NGINX_SHA256` before preparation and again at the use
point. It validates fixed and `latest`-resolved tags, reuses an existing
candidate only without `REFRESH=1`, refreshes through a temporary download
path, validates the candidate, stages and revalidates a private copy, and
extracts only the final verified copy. The fixed default binds the reviewed
official release tag, asset name, and published release-asset digest; an
explicitly empty override remains fail closed.

## Evidence and validation

- Retained assessment run `20260716T193351Z-repository-full-assessment-0cb855ad`:
  `.codex/reports/repository-full-assessment.md:221-227,238-244`, SHA-256
  `5721a77efe2baf948a163ae0ee1d981fbba37119b89b9becdd5ccebdf99c5ed4`, exit
  `0`, observed `2026-07-16T22:46:50Z`.
- Retained task run `20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1`:
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1/evidence/fnd-framework-0006-local-validation.md`,
  SHA-256 `dd220e8700629516ceb87c3a330b2ad6d8b9f8ebf64f010f46457ec4fa11a488`,
  exit `0`, observed `2026-07-18T10:15:25Z`.
- Retained delivery evidence for Framework Draft PR [#25](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/25):
  `/var/tmp/codex/ModSecurity-conector/runs/20260718T092116Z-fnd-framework-0006-nginx-digest-5251a4f1/evidence/fnd-framework-0006-delivery-blocker.md`,
  SHA-256 `89e9d095ee8648b7970919ae5913a5a1624590b0a14bdeb0d994721dc259d162`,
  evidence collection exit `0`, observed `2026-07-18T10:35:27Z`.
- Retained release-provenance continuation run
  `20260719T081017Z-framework-pr-resolution-20260719-840082e0`:
  official metadata receipt SHA-256
  `037826df6ebd25594a9b4cc7068cf72aeb804aa43672ccb6f44d8890df863c53`,
  direct asset verification receipt SHA-256
  `d2d27b6770d7d6c345762b771e7dde3bcda021c729d8fb887aa25c739c8efcd5`,
  and local-validation receipt
  `/var/tmp/codex/ModSecurity-conector/runs/20260719T081017Z-framework-pr-resolution-20260719-840082e0/evidence/pr25-release-provenance-local-validation.md`,
  SHA-256 `6b448efd1ca708e7e51a74f181dc320e6115743f4d7a937492861c1f651fb2af`.

The local evidence records a vulnerable baseline and the post-fix result. The
post-fix seven-test suite covers empty, whitespace-only, trailing-whitespace,
malformed, mismatch, matching control, candidate replacement after first hashing, cached latest
metadata, release/source overrides, existing archive revalidation, and refresh.
No negative case reaches `tar`; the matching control reaches it only through
`verified-archives`. Shell syntax, Framework documentation checks, static
Framework lint, and `git diff --check` also passed.

## Acceptance criteria and legitimate controls

- Unset, whitespace-only, trailing-whitespace, malformed, and mismatching
  digests fail before extraction.
- A matching digest succeeds and `tar` receives only the reverified private
  archive copy.
- Latest, source/release overrides, cache/refresh, existing archives, and
  candidate replacement retain the same fail-closed control.
- Matching fixed-tag, latest-cache, and `REFRESH=1` local fixture controls
  remain successful.
- The configured fixed tag, matching source ref, expected release-asset name,
  and published SHA-256 remain one reviewed tuple; a newer release must produce
  no automatic tag-only edit.

## Root-cause triage, dependencies, and boundaries

The root-cause group is `RC-FW-004-nginx-archive-digest-fail-closed`; it is a
singleton and is related to `FND-FRAMEWORK-0005` only as an archive-integrity
family. It must not share a patch or PR with FND-FRAMEWORK-0005.

This remains a Framework-only delivery. Draft PR [#25](https://github.com/Easton97-Jens/ModSecurity-test-Framework/pull/25)
has matching local, remote, and PR-head SHA; SonarCloud and `scaffold-lint`
passed and no review thread exists. Its applicable `test-common` /
`common-structure` check is a pre-existing baseline failure: it expects 141
YAML cases and finds 179, and the same workflow already fails on `master` at
`cdc91a398d6c156eaff927d742b23018a3817fb6`. No Parent Gitlink update, merge,
MRTS change, or unrelated CI repair is authorized.

## Blockers, residual risk, and disposition

There is no local implementation blocker. The finding remains `fixed`, not
`verified`: the reviewed default now has direct release-asset digest evidence,
but its new PR head has not yet received current external checks/review or a
post-merge current-master rerun. No NGINX source build or real archive
substitution was attempted; deterministic local archives exercised the control
boundary. No risk has been accepted.

## History

- `2026-07-17T10:43:59Z`: `bootstrap_created` — retained assessment evidence
  was registered without remediation or closure.
- `2026-07-18T08:09:21Z`: `root_cause_triaged` — optional NGINX digest
  enforcement was confirmed as independent from FND-FRAMEWORK-0005.
- `2026-07-18T10:15:25Z`: `local_fail_closed_remediation_validated` — the task
  branch passed the focused seven-test suite, including trailing-whitespace
  rejection, plus shell/documentation/lint/diff checks and retained
  hash-addressed local evidence; Draft-PR and post-merge verification remain
  pending.
- `2026-07-18T10:35:27Z`: `delivery_blocked_preexisting_ci_baseline` — Draft
  PR #25 matched local/remote/PR SHA `7a61a34ed5531f1f399a88e26e6242c7cacae412`;
  SonarCloud and `scaffold-lint` passed
  with no review threads, but `test-common/common-structure` failed on the
  existing master YAML-count mismatch (`expected 141`, `found 179`). The
  unrelated repair is outside this task, so the state is blocked, not
  `verified_pr`.

### Current release-provenance continuation

The 2026-07-19 continuation supersedes the old missing-evidence disposition.
It retains the existing `release-1.31.2` version rather than silently upgrading
to current `release-1.31.3`, but now pins the exact official release asset and
its published SHA-256. GitHub's tag metadata resolves the annotated tag to
`2fd01ed47a1fd2965754c83f53b33a789d0e07f1`; GitHub marks the tag unsigned, so
the implemented integrity boundary is the reviewed release-asset SHA rather
than an unmade signature claim.

The new local worktree passed 12 focused archive/provenance tests, shell/Python
syntax checks, the native full Framework lint, documentation, whitespace, and
a live updater readback. The updater verified the configured asset and digest,
then reported newer `release-1.31.3` as `unknown` with no update edits. This
preserves the required reviewed atomic tag/asset/digest update procedure.

Delivery remains pending only on the new exact Framework PR #25 head's external
checks/review and the independent current-master gates; it is not a waiver of
the dynamically failed GitHub Advanced Security run or `FND-SONAR-0002`.

## History continuation

- `2026-07-19T09:15:37Z`: `release_provenance_default_locally_validated` —
  official release metadata and a direct asset digest comparison established
  the reviewed default tuple; the 12-test suite, syntax/static checks, full
  native lint, no-partial-update check, Parent-clean check, and no-MRTS-diff
  check passed. Exact-new-head delivery and post-merge verification remain
  pending.

### Master-integration continuation

PR #25 was made ready after the current exact-head review and normally
squash-merged at `2026-07-19T09:50:22Z`. The authoritative PR merge/resulting
Framework `master` SHA is `9954b99a31fab0006cdf903ab477c8158c50fea8`; the
pre-merge task head was `c6ba5e11359d6eb30e8717b766d49697f9bed74f`. The exact
master lint, test-common/common-structure, and CodeQL runs succeeded, but the
master SonarCloud Quality Gate failed. That check is the independently tracked
pre-existing `FND-SONAR-0002` backlog, not evidence that this NGINX control
regressed. The finding remains `fixed`, not `verified` or `closed`, until the
required current-master Quality-Gate evidence is available. Parent and MRTS
remain unchanged.

- `2026-07-19T09:52:00Z`: `pr25_squash_merged_master_gate_blocked` — exact
  merge and master evidence retained at
  `pr25-9954b99-post-merge-master-verification.md`, SHA-256
  `fdda0551354ccc8cb28794a1f7ca8e35f6aa333a9d6272743e15e7e12aacca34`.

### Direct stale-PR reintroduction hazard — 2026-07-19

The current Framework `master` already contains the reviewed, fail-closed
release-tag / release-asset / nonempty SHA-256 binding. Direct comparisons show
that stale unmerged heads #24, #26, #27, and #29 remove it and restore a
tag-only archive path with a conditional digest comparison before extraction.
This is a merge blocker only: `master`
`9954b99a31fab0006cdf903ab477c8158c50fea8` remains `fixed` and the finding
is not reopened.

Retained evidence: run `20260719T081017Z-framework-pr-resolution-20260719-840082e0`,
`analysis/direct-merge-hazards.md`, SHA-256
`d28d88c9b1f034e1798cfa805d3b4e7210e3e3742dc4014d19ef78238c5c2004`;
observed `2026-07-19T12:01:55Z` by RTK-prefixed direct-diff and static NGINX
source-to-sink review.
