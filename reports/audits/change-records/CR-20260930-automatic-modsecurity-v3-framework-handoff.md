# Change Record: automatic ModSecurity v3 Framework handoff

**Language:** English | [Deutsch](CR-20260930-automatic-modsecurity-v3-framework-handoff.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | CR-20260930-automatic-modsecurity-v3-framework-handoff |
| Date (UTC) | 2026-09-30 |
| Base revision | `d75d36d6118714e6d92c3e498c500783c3fd028e` |

## Motivation and problem statement

GitHub Actions run 36728825605 resolved Framework candidate `bc8217d325809b9aba9a1d8c16964d71a01933ee` but validation stopped because that candidate advances the official ModSecurity v3 pin from v3.0.16 to v3.0.17. The existing structure digest intentionally covered every ModSecurity assignment, so the submodule updater could not carry a reviewed stable ModSecurity maintenance tuple through its normal bounded projection path.

## Acceptance criteria

Allow only the official ModSecurity-v3 repository, a stable `v3.x.y` tag and an exact lowercase SHA-1 commit to move as registered Framework source data. Project only the two documentation command constants that consume that tuple, regenerate the existing compiler guides in the publisher, retain the closed update-path allowlist, and keep NGINX plus every other ModSecurity field structurally reviewed. Automatic merge remains disabled.

## Implementation decision and rationale

Extend the existing closed source registry with exactly `MODSECURITY_V3_APPROVED_REPO_URL`, `MODSECURITY_V3_APPROVED_COMMIT` and `MODSECURITY_V3_RELEASE_TAG`. The repository value remains fixed to the official OWASP ModSecurity repository, the release is restricted to stable v3 tags, and the commit must be forty lowercase hexadecimal characters. The verifier normalizes only those same three assignments when computing the reviewed Framework structure digest.

The compiler-guide generator and its regression fixture expose two explicit managed command constants. The synchronizer may update only those constants; the existing generator then produces the bilingual documentation. The publisher allowlist and raw-diff gate explicitly register the two source files rather than admitting a directory or wildcard.

## Changed files

The Framework source-data synchronizer and candidate verifier; the reviewed-version handoff checker; compiler-guide generator and tests; submodule update workflow and its security contract tests; focused synchronizer/verifier regressions; and this paired Change Record.

## Commands executed

Repository state, failing Actions logs and the exact Framework candidate commit were inspected through the GitHub connection. The implementation is delivered as a Draft pull request so repository-native CI can execute the full configured test and security workflow set on the final head. No pending hosted check is claimed as passed in this record.

## Security impact

The change does not source or execute candidate `common.sh`. It does not accept arbitrary `MODSECURITY_*` names, mutable repositories, moving branches, NGINX pins, shell expressions, new write directories or broader workflow permissions. Existing path, raw-diff, candidate lineage, read-only namespace, App-token and no-auto-merge controls remain in place.

## Runtime evidence

This change enables a maintenance tuple to reach the existing runtime validation gates; it does not itself certify ModSecurity v3.0.17 ABI, WAF behavior or connector compatibility. Those claims require the repository's existing hosted/runtime checks for the generated candidate PR.

## Known limitations

Only the current official ModSecurity-v3 provenance tuple is automated. A future major release, repository migration, different pin shape or additional Framework ModSecurity field remains fail-closed and requires a separate review.

## Remaining risks

A syntactically valid upstream maintenance release can still introduce API, ABI, build, dependency or behavioral changes. The updater therefore continues to create a Draft PR and relies on the existing candidate and runtime gates rather than merging automatically.

## Checks not run and rationale

No hosted final-head checks are reported before the Draft PR exists. No independent claim is made that v3.0.17 passes native connector runtime validation solely because its tag and commit satisfy the bounded source-data contract.

## Final diff and review status

Deliver as a Draft PR against `master`. Review the exact final diff and hosted checks before any merge. No direct master write or automatic merge is authorized.
