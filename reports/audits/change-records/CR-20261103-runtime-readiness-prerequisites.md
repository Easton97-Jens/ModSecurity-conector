# Change Record: CR-20261103-runtime-readiness-prerequisites

**Language:** English | [Deutsch](CR-20261103-runtime-readiness-prerequisites.de.md)

Scoped readiness prerequisites.

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20261103-runtime-readiness-prerequisites |
| Date (UTC) | 2026-11-03 |
| Base revision | `11fab78a5447f75cb254ddf963eca770fa04ba04` |

## Motivation and problem statement

The current one-job delegated NGINX caller is rejected by its immutable five-job broker admission contract. The ordinary hosted NGINX smoke success does not qualify this protected path. Parent Python also remained3.15.1 while the reviewed stable patch is3.15.2.

## Acceptance criteria

Generate the actual inline caller from the exact selected Framework Git blob, retain all master/non-fork/dispatch gates and protected identities, and make ordinary Framework revision synchronization understand this typed projection. Apply the Python patch through its native atomic updater. Preserve both enclosing revision selections pending separate merge authorization.

## Implementation decision and rationale

The Framework canonical caller already satisfies the immutable broker parser. Project its exact reviewed bytes, changing only the invocation trigger and adding provenance comments. Add framework-inline-caller to the existing transactional Parent synchronizer: bounded fixed-path Git data, a reviewed source hash, previous-output verification and one exact historical migration input. Candidate Python is never imported. No new broker publication is necessary. The native Python updater changed .python-version and the central lock together; official Python3.15.2 release notes identify a security patch, rather than version age being treated as a vulnerability finding.

## Changed files

The generated .github/workflows/run-protected-nginx-root-broker.yml, ci/tools/sync-framework-component-versions.py, .python-version, ci/tooling/project-versions.lock.json, paired docs/build/README, docs/security/ci-security-tooling and docs/reference/version-pins, and this record pair. The paired rules-review report and its before/after JSON refresh the unapplied merge-rule proposal from live checks; their scope is recorded here. Framework runners, fixtures, capture generation, coverage binding and partial SBOM export are delivered in the separate Framework Draft; MRTS inherited policy corrections are in MRTS PR #6.

## Commands executed

RTK-wrapped native scripts/update-python-version.py --check --json and --update --expected-version3.15.2 --json selected the stable patch. Exact private Parent/Framework interpreters are regular CPython3.15.2. Framework tests against actual immutable broker source passed9 new projection/negative/atomic checks and6 selected existing fixture/pin checks. The Parent synchronizer --check with the exact bb6c758 common.sh blob and explicit existing Framework object repository returned changed=[]. The Framework caller generator --check passed. Documentation, interpreter contract and final whitespace checks are recorded with the final PR validation; no unexecuted result is claimed here.

## Security impact

Deny-default permissions, exact protected master/non-fork dispatch gates, concurrency, immutable broker8ae707d72f1a8acb25d239e55e28a73cbc7522b1 and protected Framework99a7985c1be92a2297b1b59208f64df6768f2cbf are preserved. Fixed Git source bytes are data only. No broker, publisher, root lifecycle or administrative rule application is launched. See the official [Python3.15.2 security release](https://www.python.org/downloads/release/python-3152/) for the interpreter patch.

## Runtime evidence

This Parent diff changes orchestration and tooling. Actual narrow NGINX protocol evidence is produced separately with the Framework candidate runner and admitted baseline product artifacts; it cannot qualify this protected-master broker lifecycle. Parser success is a caller compatibility result only.

## Known limitations

Parent remains based on11fab78a5447f75cb254ddf963eca770fa04ba04 and pins Frameworkbb6c7580208a05c17d6d6674571731b6a71028cb/MRTS75394f9a687ca2f09fd7623b23ac527bba10d7d9. The caller provenance header truthfully records that existing exact Framework source blob. New Framework and MRTS changes are not yet merged or selected by these gitlinks. Pin their actual merged commits only after separate authorization, then regenerate and verify the final pair.

## Remaining risks

Hosted current-head checks and final pair validation remain separate delivery gates. A protected broker runtime requires a separately authorized protected-master dispatch. No comprehensive profile/protocol acceptance or vulnerability completeness is claimed.

## Checks not run and rationale

No full default suite, complete runtime matrix, privileged broker, publisher, administrative application or merge. Local Sonar is suspended by the explicit current user instruction; existing hosted Sonar/CodeQL remain unchanged. No alternative mandatory scanner was introduced.

## Final diff and review status

Scoped generation and transactional boundary review completed. Separate Draft delivery retains source and evidence. The final PR records terminal checks and exact commit identities; no merge or master update is authorized by this preparation.
