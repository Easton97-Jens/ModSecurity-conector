# Change Record: Parent CI checks SonarQube Cloud remediation

**Language:** English | [Deutsch](CR-20260801-sonar-ci-checks-remediation.de.md)

## Identity

| Field | Value |
| --- | --- |
| Change ID | `CR-20260801-sonar-ci-checks-remediation` |
| Date (UTC) | 2026-08-01 |
| Base revision | `3ff87de53df34cecbc9c6489c858e64bdf3fd198` |
| Tracking | Current SonarQube Cloud component inventory for Parent `ci/checks`: 6 security findings, 2 security hotspots, 32 maintainability findings, and 0.0% duplicated lines. |
| Boundary | Parent `ci/checks`, one focused Parent test, and this English/German Change Record/index pair. Framework, MRTS, Gitlinks, workflows, scanner settings, suppressions, and `master` are unchanged. |

## Motivation and problem statement

The current `ci/checks` component contains security findings for report-write
path confinement and fixed policy paths, security hotspots for static URL
policy examples, and maintainability findings for long checkers, repeated
literal ownership, regular expressions, and configuration metadata dispatch.
The remediation must preserve each checker’s fail-closed policy contract while
removing the concrete source-level causes without a SonarQube Cloud setting,
suppression, exclusion, or Quality-Gate workaround.

## Acceptance criteria

- Each current `ci/checks` source finding has a source-level remediation in
  this change; no scanner rule, exclusion, suppression, or Quality Gate is
  changed.
- Bilingual documentation, generated-report, configuration-reference,
  lifecycle, HAProxy HTX, runtime-path, and Common-adoption checks preserve
  their previous successful controls.
- Generated test-matrix reports are rewritten only when they are regular,
  non-symlink files below the checked-out Parent root.
- The exact PR head receives fresh GitHub Actions and SonarQube Cloud evidence
  before any merge decision.

## Implementation decision and rationale

Small purpose-specific helpers now own report-path trust checks, document and
lifecycle sub-checks, scanner-result parsing, HAProxy HTX contracts, and
configuration-reference rendering. The large Envoy and Traefik YAML metadata
dispatchers use explicit path matching rather than nested conditional chains;
their output remains checked against the committed inventory and bilingual
references.

Static URL test policy is assembled from named scheme and host components, so
the checker continues to reject insecure repository references without
retaining a hard-coded insecure URL sink. Shared fixed roots and repeated
Markdown patterns have one private owner. The new regression test covers the
regular in-tree report control plus symlink and outside-root write rejection.

## Changed files

- `ci/checks/analysis/clang_analysis_baseline.py`
- `ci/checks/connectors/all/check-remaining-connectors-common-adoption.py`
- `ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py`
- `ci/checks/documentation/check-bilingual-docs.py`
- `ci/checks/documentation/check-connector-config-reference.py`
- `ci/checks/documentation/check-generated-report-layout.py`
- `ci/checks/documentation/check-no-crs-doc-consistency.py`
- `ci/checks/documentation/connector_config_reference.py`
- `ci/checks/documentation/ensure-test-matrix-language-switches.py`
- `ci/checks/evidence/check-full-lifecycle-evidence.py`
- `ci/checks/evidence/check-six-connector-core-completion.py`
- `ci/checks/security/check-runtime-path-policy.py`
- `tests/test_ensure_test_matrix_language_switches.py`
- `reports/audits/change-records/README.md`, its German companion, and this
  English/German Change Record pair.

## Commands executed

| Command | Result |
| --- | --- |
| `python -m unittest tests.test_bilingual_docs tests.test_runtime_path_policy tests.test_clang_analysis_baseline tests.test_full_lifecycle_evidence tests.test_full_lifecycle_gate_wiring tests.test_connector_config_reference tests.test_ensure_test_matrix_language_switches` | passed: 60 tests. |
| `python -m unittest tests.test_generated_report_evidence_integrity` | passed: 76 tests; the embedded generated-report layout check passed. |
| `python ci/checks/documentation/check-bilingual-docs.py` | passed: `bilingual docs ok`. |
| `python ci/checks/documentation/check-connector-config-reference.py` | passed for Apache, NGINX, HAProxy, Envoy, Traefik, lighttpd, Common Runtime, and Engine inventories. |
| `python ci/checks/documentation/check-no-crs-doc-consistency.py` | passed. |
| `python ci/checks/connectors/all/check-remaining-connectors-common-adoption.py` | passed for all connectors. |
| `python ci/checks/connectors/haproxy/check-haproxy-htx-overlay.py` | passed: all 26 static contracts. |
| `python ci/checks/security/check-runtime-path-policy.py` | passed; its expected negative self-checks rejected unsafe roots. |
| `git diff --check` | passed before the Change Record was added; rerun after all documentation updates and before delivery. |

## Security impact

The report-language updater now refuses a symbolic link, a non-regular file,
or a resolved path outside the checkout before reading or writing it. Runtime
path-policy roots remain governed by the shared trusted helper. URL checks,
artifact validation, and all existing fail-closed policy paths remain active;
this change does not broaden network, filesystem, credential, or CI authority.

## Runtime evidence

Not applicable. These are static Parent CI-check and documentation-generator
changes. The HAProxy HTX static contract and the in-tree/symlink/outside-path
tests are control evidence, not a connector runtime claim.

## Checks not run and rationale

- Full connector builds and runtime matrices were not run because no connector
  product source or runtime behavior changed.
- Framework and MRTS checks were not run because neither repository nor either
  Gitlink is in scope.
- Fresh exact-head GitHub Actions, review state, and SonarQube Cloud are
  delivery evidence and cannot exist until the task branch is pushed as a PR.

## Known limitations

The current remote default branch must be incorporated before delivery. The
source-level remediation is not externally closed until a SonarQube Cloud
analysis for the final PR head confirms the absence of the listed component
findings and reports no new issues or new-code duplication.

## Remaining risks

The structural refactors preserve checker outputs through the focused suites,
but an unexercised unusual YAML path or malformed report layout could still
reveal a diagnostic-order difference. The final exact-head hosted and
SonarQube Cloud checks are required to detect that class of integration issue.
The path-update negative tests mitigate the security-sensitive write boundary;
no raw report content or credentials are retained in this record.

## Final diff and review status

At record authoring, the candidate is limited to Parent `ci/checks`, its
focused test, and traceability documentation. No Framework/MRTS/Gitlink,
workflow, dependency, scanner configuration, suppression, or `master` change
is present. Local controls have passed as listed; final scoped review, commit,
push, and exact-head hosted verification remain pending. This record does not
authorize a merge.
